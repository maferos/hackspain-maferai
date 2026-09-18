# Rendering lab scenes on RunPod (headless GPU)

How to spin up an NVIDIA GPU pod on RunPod, render MuJoCo / AutoBio lab scenes
offscreen (EGL, no display), pull the PNGs back, and tear the pod down so it
stops billing. This is the path we use because AutoBio's renderer needs a real
NVIDIA GPU and a Linux box, and it gives the computer-vision team real rendered
frames.

Everything below is copy-pasteable from a **Linux or macOS** shell. It talks to
RunPod over its GraphQL API with `curl` — do **not** use `python-urllib`/`requests`,
RunPod's WAF returns `403` for those user-agents.

---

## 0. Prerequisites (one-time)

- A RunPod account **with credit** (a few dollars is plenty — a render pod is
  ~$0.20–0.35/h). Eki has the account + API key.
- Export the API key (never hard-code it):
  ```bash
  export RUNPOD_API_KEY=rpa_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
- An SSH keypair to reach the pod. Make a throwaway one:
  ```bash
  mkdir -p ~/.runpod-render
  ssh-keygen -t ed25519 -N "" -f ~/.runpod-render/id_ed25519 -q
  ```
- `curl`, `ssh`, `scp`, `jq` installed locally.
- Check the key works and you have balance:
  ```bash
  curl -s "https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"query":"query{myself{clientBalance currentSpendPerHr}}"}' | jq
  ```

---

## 1. Deploy a GPU pod

Any RTX/datacenter card renders fine. Cheap ones are often supply-constrained, so
we try a few in order and stop at the first that deploys. The `runpod/pytorch`
image ships `sshd` and injects our `PUBLIC_KEY` into `authorized_keys`.

```bash
PUB=$(cat ~/.runpod-render/id_ed25519.pub)
URL="https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY"
IMAGE="runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04"

deploy() {  # $1 = gpuTypeId
  local q
  q=$(cat <<EOF
mutation{ podFindAndDeployOnDemand(input:{
  cloudType: ALL, gpuCount:1, gpuTypeId:"$1",
  name:"lab-render", imageName:"$IMAGE",
  ports:"22/tcp", volumeInGb:0, containerDiskInGb:20, minVcpuCount:2, minMemoryInGb:8,
  env:[{key:"PUBLIC_KEY", value:"$PUB"}]
}){ id costPerHr } }
EOF
)
  curl -s "$URL" -H "Content-Type: application/json" \
    --data "$(jq -nc --arg q "$q" '{query:$q}')"
}

POD=""
for GPU in "NVIDIA RTX A5000" "NVIDIA GeForce RTX 3090" "NVIDIA RTX A6000" \
           "NVIDIA GeForce RTX 4090" "NVIDIA A40" "NVIDIA L4"; do
  RES=$(deploy "$GPU")
  POD=$(echo "$RES" | jq -r '.data.podFindAndDeployOnDemand.id // empty')
  if [ -n "$POD" ]; then
    echo "deployed $GPU -> pod $POD ($(echo "$RES" | jq -r '.data.podFindAndDeployOnDemand.costPerHr')/h)"
    break
  fi
  echo "-- $GPU: $(echo "$RES" | jq -r '.errors[0].extensions.code // .errors[0].message')"
done
[ -n "$POD" ] || { echo "no GPU available right now, retry later"; }
echo "$POD" > ~/.runpod-render/pod_id
```

> List all GPU types + prices any time:
> ```bash
> curl -s "$URL" -H "Content-Type: application/json" \
>   -d '{"query":"query{gpuTypes{id displayName memoryInGb lowestPrice(input:{gpuCount:1}){uninterruptablePrice}}}"}' \
>   | jq -r '.data.gpuTypes[] | "\(.lowestPrice.uninterruptablePrice)\t\(.id)"' | sort -n
> ```

---

## 2. Wait for the SSH endpoint

```bash
POD=$(cat ~/.runpod-render/pod_id)
for i in $(seq 1 30); do
  P=$(curl -s "$URL" -H "Content-Type: application/json" \
      -d "{\"query\":\"query{pod(input:{podId:\\\"$POD\\\"}){runtime{ports{ip publicPort privatePort isIpPublic}}}}\"}" \
      | jq -r '.data.pod.runtime.ports[]? | select(.privatePort==22 and .isIpPublic) | "\(.ip) \(.publicPort)"')
  [ -n "$P" ] && { echo "$P" > ~/.runpod-render/ssh_target; echo "SSH: $P"; break; }
  echo "waiting for ssh..."; sleep 10
done
```

Define a helper for the rest of the session:

```bash
read IP PORT < ~/.runpod-render/ssh_target
SSHK=~/.runpod-render/id_ed25519
SSHOPTS="-i $SSHK -p $PORT -o StrictHostKeyChecking=accept-new -o ConnectTimeout=25"
SCPOPTS="-i $SSHK -P $PORT -o StrictHostKeyChecking=accept-new"
ssh $SSHOPTS root@$IP 'nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader'
```

---

## 3. Upload AutoBio + the render script

AutoBio's scenes need three things on the pod: the prebuilt plugin
`libmjlab.so.3.3.0`, the `model/` tree, and the `assets/` tree (meshes). They live
in the submodule at `simulation/third_party/AutoBio/autobio/`. **Ship them as one
tarball** — `scp -r` of the ~180 small mesh files is painfully slow.

```bash
AB=simulation/third_party/AutoBio/autobio        # adjust to your checkout
tar -C "$AB" -czf /tmp/autobio.tgz model assets libmjlab.so.3.3.0 meshplane.so

ssh $SSHOPTS root@$IP 'mkdir -p /root/autobio'
scp $SCPOPTS /tmp/autobio.tgz root@$IP:/root/autobio/
scp $SCPOPTS simulation/scripts/render_autobio.py root@$IP:/root/autobio/   # see Appendix if you don't have it
ssh $SSHOPTS root@$IP 'cd /root/autobio && tar xzf autobio.tgz && rm autobio.tgz'
```

---

## 4. Render

The plugin is built against **MuJoCo 3.3.0 exactly**, so pin it. `MUJOCO_GL=egl`
selects headless GPU rendering.

```bash
ssh $SSHOPTS root@$IP 'set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq && apt-get install -y -qq libegl1 libgl1 libglib2.0-0 libgomp1 >/dev/null
pip -q install "mujoco==3.3.0" pillow numpy
cd /root/autobio && MUJOCO_GL=egl python3 render_autobio.py \
  lab mani_thermal_cycler mani_centrifuge_5430 mani_pipette vortex_mixer pickup'
```

Scene names are the stems in `model/scene/*.xml`. List them with:
`ssh $SSHOPTS root@$IP 'ls /root/autobio/model/scene'`.

---

## 5. Fetch the images

```bash
mkdir -p renders
for s in lab mani_thermal_cycler mani_centrifuge_5430 mani_pipette vortex_mixer pickup; do
  scp $SCPOPTS root@$IP:/root/autobio/$s.png renders/ && echo "got $s.png"
done
```

---

## 6. Tear down (stop billing!)

The pod bills for every hour it exists, running or not. Terminate it when done:

```bash
POD=$(cat ~/.runpod-render/pod_id)
curl -s "$URL" -H "Content-Type: application/json" \
  -d "{\"query\":\"mutation{podTerminate(input:{podId:\\\"$POD\\\"})}\"}"
```

Verify nothing is left running: <https://www.runpod.io/console/pods>.

---

## Notes & gotchas

- **Cost**: RTX A5000/3090 ≈ $0.16–0.27/h. Community cloud is cheapest but can be
  preempted; `cloudType: ALL` picks the cheapest available across community+secure.
- **`403 Forbidden`** from the API → you used a non-curl HTTP client; RunPod's WAF
  blocks `python-urllib`/default `requests` user-agents. Use `curl`.
- **`SUPPLY_CONSTRAINT`** → that GPU has no free instances; the loop in step 1
  falls through to the next type. Retry later if all are constrained.
- **`Image width N > framebuffer width 640`** → the offscreen framebuffer defaults
  to 640×480. `render_autobio.py` bumps it via `model.vis.global_.offwidth/offheight`;
  if you write your own, set those before creating the `Renderer`.
- **MuJoCo version**: AutoBio's plugin is `libmjlab.so.3.3.0` and only loads with
  `mujoco==3.3.0`. For plain (non-AutoBio) MJCF scenes any `mujoco>=3.13` is fine
  and you can skip the plugin entirely.
- **Security**: keep the API key in `$RUNPOD_API_KEY` / a 600-mode file, never in
  a committed file. Rotate it if it ever leaks.

---

## Appendix — `render_autobio.py`

Offscreen EGL render of AutoBio scenes to PNG. If it's not already in
`simulation/scripts/`, save this on the pod as `/root/autobio/render_autobio.py`.

```python
#!/usr/bin/env python3
"""Offscreen EGL render of AutoBio lab scenes -> PNG. Loads AutoBio's plugin first."""
import os, sys
os.environ.setdefault("MUJOCO_GL", "egl")
import mujoco
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.join(BASE, f"libmjlab.so.{mujoco.__version__}")
SCENES = os.path.join(BASE, "model", "scene")
W, H = 1280, 720

print("mujoco", mujoco.__version__, "MUJOCO_GL", os.environ.get("MUJOCO_GL"))
if not os.path.exists(PLUGIN):
    sys.exit(f"plugin not found: {PLUGIN} (need mujoco==3.3.0)")
mujoco.mj_loadPluginLibrary(PLUGIN)

for name in (sys.argv[1:] or ["pickup"]):
    path = os.path.join(SCENES, f"{name}.xml")
    try:
        m = mujoco.MjModel.from_xml_path(path)
    except Exception as e:
        print(f"FAIL load  {name}: {str(e).splitlines()[0]}"); continue
    m.vis.global_.offwidth, m.vis.global_.offheight = W, H
    d = mujoco.MjData(m)
    mujoco.mj_forward(m, d)                 # authored pose, no settling
    cam = 0 if m.ncam > 0 else -1           # use an authored camera if present
    with mujoco.Renderer(m, height=H, width=W) as r:
        r.update_scene(d, camera=cam)
        Image.fromarray(r.render()).save(os.path.join(BASE, f"{name}.png"))
    print(f"OK   {name}  bodies={m.nbody} cams={m.ncam}")
```

For a plain MJCF scene (no AutoBio, any `mujoco>=3.13`), drop the plugin lines and
point `from_xml_path` at your `.xml` — or use `scripts/render_dataset.py`, which
renders randomised camera poses for a CV dataset.
