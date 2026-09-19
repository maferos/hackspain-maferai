# Running Isaac Sim on RunPod (headless GPU → RGB to disk)

How to run NVIDIA Isaac Sim **headless** on a RunPod GPU pod, render RGB frames to
disk with Replicator, pull them back, and tear down. This is the Isaac/Omniverse
counterpart to [`runpod-render.md`](runpod-render.md) (MuJoCo/AutoBio via EGL) and
closes the "Stand up Isaac Sim on RunPod" item in [`todo.md`](todo.md).

**Verified 2026-09-18** on an RTX A5000 (Secure Cloud, `$0.27/h`): image pull +
extract ~6 min, Isaac first boot ~4.5 min, then a 1280×720 RGB frame written to
disk. Whole de-risk cost ~\$0.15.

---

## The catch that shapes everything: the official image's ENTRYPOINT

The official image `nvcr.io/nvidia/isaac-sim:4.5.0` is **public** (no NGC login;
only `ACCEPT_EULA=Y` at runtime) and runs as **root** — but its ENTRYPOINT is
hardcoded:

```
Entrypoint = ["/bin/sh","-c","/isaac-sim/runheadless.sh"]   Cmd = null   User = root
```

It **always launches the WebRTC streaming app** and ignores any CMD you pass (the
CMD just becomes ignored positional args to `sh -c`). Consequences:

- RunPod's **GraphQL API / `runpodctl pod create`** only override the CMD
  (`dockerArgs`), **not** the entrypoint. Deploy that way and the pod boots the
  streaming app — you can't start `sshd` or run your own script. (Confirmed: the
  pod logged `Isaac Sim Full Streaming App is loaded`, no shell.)
- RunPod's **REST API v2** (`POST https://rest.runpod.io/v1/pods`) exposes
  **`dockerEntrypoint`** and **`dockerStartCmd`** as separate string arrays →
  override the entrypoint to `bash -lc`, bootstrap `sshd`, and you're in.
  **This is the whole trick.** (An empty `dockerEntrypoint` keeps the image
  default, so pass an explicit one.)

Inspect any image's entrypoint without pulling it (nvcr.io is public):

```bash
REPO=nvidia/isaac-sim; TAG=4.5.0
TOKEN=$(curl -s "https://nvcr.io/proxy_auth?scope=repository:${REPO}:pull&service=nvcr.io" | jq -r .token)
MAN=$(curl -s -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  "https://nvcr.io/v2/$REPO/manifests/$TAG")
CFG=$(echo "$MAN" | jq -r .config.digest)
curl -sL -H "Authorization: Bearer $TOKEN" "https://nvcr.io/v2/$REPO/blobs/$CFG" \
  | jq '{Entrypoint:.config.Entrypoint, Cmd:.config.Cmd, User:.config.User}'
```

---

## 0. Prerequisites (one-time)

- A RunPod account with credit and `export RUNPOD_API_KEY=rpa_...` (see
  `runpod-render.md` §0). `runpodctl` optional; the deploy below is raw REST.
- A throwaway SSH keypair:
  ```bash
  mkdir -p ~/.runpod-render
  ssh-keygen -t ed25519 -N "" -f ~/.runpod-render/id_ed25519 -q
  ```
- `curl`, `jq`, `ssh`, `scp` locally.

---

## 1. Deploy via REST v2 with an ENTRYPOINT override

The start command (`scripts/runpod_isaac_sshd_boot.sh`) installs and runs `sshd`
so we can get a shell; `$PUBLIC_KEY` is injected from the pod env.

```bash
PUB=$(cat ~/.runpod-render/id_ed25519.pub)
BOOT=$(cat simulation/scripts/runpod_isaac_sshd_boot.sh)   # from your checkout

PAYLOAD=$(jq -n --arg img "nvcr.io/nvidia/isaac-sim:4.5.0" --arg pub "$PUB" --arg boot "$BOOT" '{
  name:"isaac-derisk", imageName:$img, cloudType:"SECURE",
  gpuTypeIds:["NVIDIA RTX A5000"], gpuCount:1,
  containerDiskInGb:60, ports:["22/tcp"], supportPublicIp:true,
  env:{ACCEPT_EULA:"Y", PUBLIC_KEY:$pub},
  dockerEntrypoint:["/bin/bash","-lc"], dockerStartCmd:[$boot]
}')

curl -s -X POST "https://rest.runpod.io/v1/pods" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" -H "Content-Type: application/json" \
  -d "$PAYLOAD" | jq -r '.id' | tee ~/.runpod-render/isaac_pod_id
```

> Need ≥50 GB container disk (the image extracts to ~20 GB). Any RTX with RT cores
> works (A5000/A6000/4090/A40/L4); introspection is disabled so pick a known
> `gpuTypeId` from `runpodctl gpu list`.

## 2. Wait for SSH

The port maps as soon as the pod is rented, but `sshd` only answers after the
pull + `apt install openssh-server`. Poll for the banner:

```bash
POD=$(cat ~/.runpod-render/isaac_pod_id)
URL="https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY"
for i in $(seq 1 90); do
  P=$(curl -s "$URL" -H "Content-Type: application/json" \
      -d "{\"query\":\"query{pod(input:{podId:\\\"$POD\\\"}){runtime{ports{ip publicPort privatePort isIpPublic}}}}\"}" \
      | jq -r '.data.pod.runtime.ports[]? | select(.privatePort==22 and .isIpPublic) | "\(.ip) \(.publicPort)"')
  if [ -n "$P" ] && ssh-keyscan -T 5 -p ${P#* } ${P% *} 2>/dev/null | grep -qi ssh; then
    echo "$P" > ~/.runpod-render/isaac_ssh_target; echo "SSH: $P"; break
  fi
  echo "waiting ($i)..."; sleep 20
done
```

## 3. Render

```bash
read IP PORT < ~/.runpod-render/isaac_ssh_target
SSHK=~/.runpod-render/id_ed25519
scp -i "$SSHK" -P "$PORT" -o StrictHostKeyChecking=accept-new \
    simulation/scripts/render_isaac.py root@"$IP":/root/render_isaac.py
ssh -i "$SSHK" -p "$PORT" -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 root@"$IP" \
    'OUT_DIR=/root/out /isaac-sim/python.sh /root/render_isaac.py'
```

`render_isaac.py` builds a trivial scene (plane + cube + sphere + distant light),
one camera, and a Replicator `BasicWriter` → `rgb_0000.png` (1280×720) + metadata.
Use Isaac's bundled interpreter `/isaac-sim/python.sh`, **not** system python.

## 4. Fetch the images + tear down (stop billing!)

```bash
scp -i "$SSHK" -P "$PORT" -o StrictHostKeyChecking=accept-new "root@$IP:/root/out/*" ./renders/
curl -s -X DELETE "https://rest.runpod.io/v1/pods/$(cat ~/.runpod-render/isaac_pod_id)" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" -w "\nHTTP %{http_code}\n"   # 204 = gone
```

Verify nothing is left: <https://www.runpod.io/console/pods>.

---

## Notes & gotchas

- **First boot ~4.5 min**: `Simulation App Startup Complete` came at ~275 s while
  it downloads/compiles kit extensions and shaders. Later runs on the same pod are
  much faster. Keep the SSH session alive (`ServerAliveInterval=30`).
- **GLFW warnings are harmless**: `GLFW initialization failed` / `carb.windowing`
  — there's no window in headless mode; the offscreen RTX render still writes PNGs.
- **Deprecation spam** (`omni.isaac.* has been deprecated in favor of isaacsim.*`)
  is noise in 4.5; the code still runs.
- **Replicator API**: `rep.orchestrator.run_until_complete(num_frames=N)` renders
  N frames; a few frames lets the first-frame warmup/denoiser settle.
- **Why not `runpod/pytorch` + `pip install isaacsim`**: it works and gives
  guaranteed SSH, but Isaac's pip path is heavy (~15 GB wheels, NVIDIA labels it
  experimental) and doesn't validate the official container. The REST entrypoint
  override reuses the official image with one 20 GB pull — prefer it. Keep pip as
  the fallback if REST override ever breaks.
- **No interactive GUI** — see [`runpod-interactive.md`](runpod-interactive.md).
  This path is render-to-disk only, which is all Replicator SDG needs.

---

## Rendering an existing MuJoCo scene in Isaac RTX

Render the perfumery-lab scene (`models/minihannover_scene.xml`, MuJoCo/MJCF) in
Isaac's RTX renderer. **Verified 2026-09-18 on an RTX 4090** (7 authored views,
1920×1080).

**Do NOT use Isaac's MJCF importer for this.** It doesn't expand MuJoCo
`<include>` (so `minihannover_scene.xml`, which only `<include>`s the bench,
imports nearly empty), and it targets robots, not decorative scenes with 300+
visual meshes and colliding mesh basenames. It reports success yet writes a ~20 KB
empty USD.

**The path that works: MuJoCo's own USD exporter, then Isaac only renders.**

1. On the pod, add MuJoCo + USD + Pillow to the **system** python (not Isaac's):
   ```bash
   apt-get install -y python3-pip
   python3 -m pip install mujoco usd-core pillow
   ```
2. Export the scene to a USD package with `scripts/export_usd.py` — `mujoco.usd`'s
   `USDExporter` loads the full scene (all includes, 319 meshes, materials, the 7
   authored cameras, the lights):
   ```bash
   python3 export_usd.py /root/scene/models/minihannover_scene.xml /root/out
   # -> /root/out/lab_usd/frames/frame_1.usdc (+ assets/texture_*.png), ~25 MB
   ```
3. Render that USD with Isaac + Replicator via `scripts/render_usd.py`:
   ```bash
   OUT_DIR=/root/out/lab W=1920 H=1080 LIGHTMUL=40 \
     /isaac-sim/python.sh render_usd.py /root/out/lab_usd/frames/frame_1.usdc [cam_path ...]
   ```
   It renders each camera prim (or the ones you pass) and boosts every imported
   light (see the lighting gotcha).
4. SCP the PNGs back, terminate the pod.

### Gotchas (each cost real time)

- **RTX 5090 (Blackwell) is NOT compatible with Isaac Sim 4.5** — even a trivial
  headless render segfaults at startup (in the urdf importer's UI build), driver
  580.95.05. Use **Ada/Ampere**: RTX 4090, A5000/A6000, A40, L40 — exclude the 5090
  from `gpuTypeIds`. (The interactive note already flagged the 50-series.)
- **Lighting: it's a CLOSED room.** A DomeLight (sky) can't get in, so it does
  nothing; MuJoCo's exported ceiling lights import far too dim for RTX.
  `render_usd.py` multiplies every light's intensity by `LIGHTMUL` (≈40 looked
  right here). Without it the render is near-black.
- **First Isaac boot on a fresh pod takes minutes; after that ~10 s** (extensions
  cached), so iterating the render/lighting is fast.
- USD export runs on plain python (mujoco + usd-core + pillow), no Isaac. Keep it
  off `/isaac-sim/python.sh` (which has USD but not mujoco).
- Uploading the 57 MB scene tarball over scp from the Mac is the slow step
  (~7 min); the pod's own bandwidth (pip, image pull) is fast.
- **Driver too NEW also breaks it, not just the 5090.** A 4090/A40 worker with
  driver **595.91.07** segfaults Isaac at startup (`_wait_for_viewport`) exactly
  like the 5090; driver **570.x / 580.x** works. RunPod may hand you the same bad
  host repeatedly. Pin `dataCenterIds: ["CA-MTL-1","CA-MTL-2","CA-MTL-3"]`
  (Montreal gave 570/580) and **check `nvidia-smi` driver before rendering**.
- **Don't install `usd-core` on the render pod's system python.** Its `pxr` can
  collide with Isaac's and segfault the viewport when `render_usd.py` runs under
  `/isaac-sim/python.sh`. Instead export the USD elsewhere — locally on the Mac via
  `uv run --with mujoco --with usd-core --with pillow python export_usd.py …`, or a
  throwaway venv — and upload only the ~12 MB USD package (`lab_usd/`) to a clean
  render pod. Splits export (needs mujoco+usd) from render (needs only Isaac).
- **Sanitise names for USD.** MuJoCo names with `-` (asset dirs `gc-ms`,
  `uv-vs-nr`) make USD prim paths invalid → `Path must be an absolute path: <>` and
  an empty/partial export. `export_usd.py` monkeypatches the exporter to map every
  generated name to `[A-Za-z0-9_]`. The shelf-free `open` scene lacked those
  assets, so it exported fine while `full` didn't until sanitised.

## Next (toward the real dataset)

This de-risks the cloud path. To turn it into a labelled CV dataset, extend
`render_isaac.py` with Replicator writers for **segmentation + depth + bbox**,
domain-randomise camera/lighting, and swap the trivial scene for the lab bench
(`minihannover` URDF→USD). See the `todo.md` "Not yet specified" items.
