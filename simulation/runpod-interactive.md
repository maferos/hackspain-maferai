# Interactive viewing of Isaac Sim on a remote RunPod GPU

Research note (2026-09-18). Question: can we get MuJoCo-viewer-style **interactive**
viewing (navigate camera, select/drag objects, play/pause) of NVIDIA Isaac Sim
running on a remote RunPod GPU pod reached over SSH on a mapped TCP port, with no
local display on the Mac? And what is the least-friction way for the hackathon?

Companion to [`runpod-render.md`](runpod-render.md) (headless render-to-disk) and
answers the open item in [`todo.md`](todo.md): *"Interactive Isaac Sim on RunPod?"*.

Facts are cited to primary sources. Statements marked **(inference)** are my
reasoning from those facts, not something a source states directly.

---

## Bottom line (TL;DR)

- **Isaac Sim's supported remote path is WebRTC livestreaming, which needs UDP.**
  RunPod pods do **not** forward UDP. So the *supported* interactive path is
  **blocked on RunPod** — signaling connects, the video never flows.
- **What works on RunPod is VNC/noVNC** (all TCP), where Isaac renders to a
  *virtual display* on the pod's GPU and you view it in a browser or VNC client.
  This is **not officially supported by NVIDIA** and is version-fragile (a known
  working combo is Isaac Sim 4.0.0 + RTX 4090), but it functions.
- **MuJoCo already runs interactively on your Mac** — no cloud needed for
  interactive authoring/debugging.
- **Recommendation:** don't burn hackathon time on remote interactive Isaac.
  Author/debug interactively in **MuJoCo locally**, run Isaac **headless →
  render to disk** on RunPod (the existing plan). If you truly must eyeball an
  Isaac scene live, use **noVNC over an SSH tunnel** as a throwaway — steps at the
  bottom.

---

## 1. Isaac Sim remote-interaction mechanisms (WebRTC)

Isaac Sim's built-in remote interaction is **WebRTC livestreaming**: the pod runs
Isaac Sim headless, encodes rendered frames from CUDA buffers, and streams them to
a client that sends back mouse/keyboard/camera input — i.e. full interaction.

- The streaming server is the extension **`omni.kit.livestream.webrtc`**, which
  "provides implementations of the streaming server interface (`IServer`) for both
  WebRTC and native protocols" and does "streaming video frames from CUDA buffers
  to remote clients with support for bidirectional messaging and input handling."
  [omni.kit.livestream.webrtc Overview](https://docs.omniverse.nvidia.com/kit/docs/omni.kit.livestream.webrtc/latest/Overview.html)

- You launch Isaac Sim in streaming mode via the shipped launcher, not by
  hand-enabling the extension. Per the
  [Livestream Clients docs](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/manual_livestream_clients.html):
  - Linux install: `./isaac-sim.streaming.sh`
  - Docker (x86_64): `./runheadless.sh`
  - pip: `isaacsim isaacsim.exp.full.streaming --no-window`
  - Python API: `standalone_examples/api/isaacsim.simulation_app/livestream.py`
  The experience file is `isaacsim.exp.full.streaming`.

- **Clients** (same doc):
  - **Isaac Sim WebRTC Streaming Client** — a native desktop app (Win/macOS/Linux),
    described as "the recommended streaming client to view Isaac Sim remotely on
    your desktop or workstation without a powerful GPU." This is the primary path.
  - **Web/browser client** — a browser viewer (deployed via Docker Compose in
    recent versions, served on TCP **8210**; older Omniverse builds exposed a
    WebRTC browser client at `http://<ip>:8211/streaming/webrtc-client?server=<ip>`).
    Port/URL is version-dependent.
  - To connect: start Isaac Sim in streaming mode on the pod, then point the client
    at the pod's IP. For internet use the docs add
    `--/exts/omni.kit.livestream.app/primaryStream/publicIp=<PUBLIC_IP>`.

## 2. Network requirements of WebRTC

From the [Livestream Clients docs](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/manual_livestream_clients.html)
and the extension overview:

| Port    | Protocol | Purpose                          |
| ------- | -------- | -------------------------------- |
| 49100   | **TCP**  | WebRTC signaling                 |
| 47998   | **UDP**  | WebRTC media stream              |
| 8210    | TCP      | Web viewer (Docker Compose only) |

- The docs are explicit: **"opening only TCP ports is not sufficient for WebRTC
  media"** — both the TCP signaling port and the UDP media port must be open.
- The signaling/media ports are effectively hardcoded (the extension config shows
  `signalPort = 49100`, `streamPort = 47998/47999`).
- For a remote host the media socket binds to a routable address, hence the
  `publicIp=` flag; in Docker, `--network=host` is required because the streaming
  SDK binds its UDP socket to a real host interface that bridge/`-p` publishing
  doesn't expose **(inference from the docs' `publicIp` guidance + Docker notes)**.
- Real-world corroboration that UDP is the sticking point on cloud hosts: Isaac Sim
  [issue #308](https://github.com/isaac-sim/IsaacSim/issues/308) — the kit process
  listens on TCP 49100 but shows "complete absence of a line for UDP 47998", so
  external livestreaming fails; also
  [issue #539](https://github.com/isaac-sim/IsaacSim/issues/539) and
  [discussion #597](https://github.com/isaac-sim/IsaacSim/discussions/597)
  (WebRTC client greyed out on a Vast.AI instance).

## 3. RunPod feasibility of WebRTC — blocked

RunPod's port model has three shapes: an **HTTP proxy** (per-port URL
`https://[POD_ID]-[PORT].proxy.runpod.net`, auto-HTTPS), **direct TCP ports** (a
public IP + a randomly-mapped external port), and stable public IPs on Secure
Cloud. See [Expose ports](https://docs.runpod.io/pods/configuration/expose-ports).

The decisive fact, from that same doc: **"Pods do not support UDP connections. If
your application relies on UDP, you'll need to modify your application to use
TCP-based communication instead."**

- Direct TCP ports carry only TCP; external ports are dynamic ("External port
  mappings change whenever your Pod resets"). Symmetrical mapping exists (request
  port numbers above 70000; discover via `$RUNPOD_TCP_PORT_*` env vars) but is
  still TCP-only.
- Even a Secure Cloud "stable public IP" pod does not add UDP — the no-UDP
  statement is unconditional.

**Conclusion:** Isaac Sim WebRTC media (UDP 47998) **cannot flow through RunPod**.
You could route signaling over a mapped TCP port, but the media stream dies. A
TURN relay forcing WebRTC media over TCP is theoretically possible but Isaac Sim's
embedded SDK doesn't offer a TCP media fallback and the docs call TCP-only
insufficient — so it is not a hackathon-appropriate option **(inference)**. Isaac
Sim WebRTC on RunPod is **not practical**.

## 4. Alternative — virtual display + VNC/noVNC (works on RunPod)

VNC is **TCP**, so it rides RunPod's proxy (HTTP/websocket) *or* a mapped TCP port
*or* an SSH tunnel. The catch is Isaac Sim's renderer, not the transport.

**Isaac Sim needs a Vulkan swapchain even when "headless".** NVIDIA's
[Container Installation docs](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_container.html)
state GUI mode "requires a **real local display**. It does not work over a remote
or virtual display (for example, NoMachine, VNC, or DCV) or on a headless server
with no connected monitor: the renderer cannot create a Vulkan swapchain and
aborts with `Failed to initialize graphics environment`." Their recommended fix is
"headless mode with livestreaming" (WebRTC) — which §3 just ruled out on RunPod.

**But the virtual-display route can be made to work** by giving Isaac a real X
display to present into, backed by the GPU, then screen-scraping that display over
VNC. A purpose-built reference exists:
[Sa3d-99/runpod_noVNC_isaac_sim](https://github.com/Sa3d-99/runpod_noVNC_isaac_sim)
— tagline: *"Isaac's built-in streaming needs UDP, which RunPod never forwards —
so instead we render Isaac to a virtual display and serve it over plain HTTP with
noVNC. One command, one HTTP port, no WebRTC."*

- Architecture: `Xvfb (virtual X screen, on the GPU) → x11vnc (VNC on
  localhost:5900) → websockify + noVNC → RunPod HTTP proxy → browser`, all on a
  **single HTTP port 8080**. Connect via *Connect → HTTP Service → port 8080* in
  the RunPod console.
- One-command bootstrap:
  `curl -fsSL https://raw.githubusercontent.com/Sa3d-99/runpod_noVNC_isaac_sim/main/bootstrap.sh | bash`
- GPU acceleration: the README claims Isaac renders natively to the virtual
  display (full GPU); the heavy RTX/Vulkan work stays on the GPU and the frame is
  copied into the virtual framebuffer **(inference)**.
- **Caveats (important):**
  - Unsupported by NVIDIA and version-fragile: README says "RTX 4090 + Isaac 4.0.0
    is the combination that works"; Isaac 5.x/6.x run as an unprivileged user with
    read-only `/usr`, which breaks the desktop install; RTX 50-series is unsupported
    by Isaac 4.0.0.
  - No VNC auth by default (set `VNC_PASSWORD` before sharing a URL).
  - RunPod's HTTP proxy sits behind Cloudflare with a "default timeout of
    approximately 100 seconds if the connection is not kept alive"
    ([proxy guide](https://www.runpod.io/blog/runpod-proxy-guide)). A live noVNC
    websocket carries continuous traffic so it normally stays alive, but the proxy
    also adds latency; for a smoother session, bypass the proxy — expose VNC as a
    direct TCP port, or tunnel it over your existing SSH **(inference)**.

General-purpose variant (better for plain OpenGL apps than for Isaac's Vulkan
renderer): **VirtualGL + TurboVNC**. VirtualGL "works fine with headless nVidia
GPUs" using a GPU-backed virtual X screen created with
`nvidia-xconfig -a --allow-empty-initial-configuration --use-display-device=None
--virtual=1920x1200 --busid <id>`
([VirtualGL HeadlessNV](https://virtualgl.org/Documentation/HeadlessNV)). VirtualGL
intercepts **OpenGL/GLX**; it is not a Vulkan solution, so it's the right tool for
MuJoCo-style GL apps, not for Isaac's RTX path **(inference)**. A GPU-backed Xorg
virtual screen (vs. software Xvfb) is likely the more robust way to satisfy Isaac's
Vulkan swapchain **(inference)**.

## 5. Does MuJoCo's own viewer work remotely?

MuJoCo's interactive viewer needs an on-screen OpenGL context/window. Per the
[MuJoCo visualization docs](https://mujoco.readthedocs.io/en/stable/programming/visualization.html):
"On Linux, MuJoCo currently supports GLX for rendering to an X11 window, OSMesa for
headless software rendering, and EGL for hardware accelerated headless rendering."
The viewer (`mujoco.viewer` / `launch_passive` / `python -m mujoco.viewer`) uses
**GLFW** and thus needs a window/display; **EGL/OSMesa are offscreen only** (what
`runpod-render.md` already uses for render-to-disk).

So *remotely* MuJoCo's viewer would need the same VNC/virtual-display trick as
§4 (VirtualGL + TurboVNC/noVNC over TCP; all works on RunPod). **But this is moot:
MuJoCo already runs interactively on the Mac** (`mjpython scripts/view_model.py`,
per the simulation README), so there is no reason to run the MuJoCo viewer in the
cloud. Cloud interaction only matters for the Isaac/NVIDIA path.

## 6. Recommendation for the hackathon

Ranked by setup friction / reliability:

1. **Don't do remote interactive Isaac (recommended).** Interactive authoring and
   debugging happens **locally in MuJoCo on the Mac** (already working). Isaac Sim
   stays **headless → render to disk** on RunPod (the plan in `todo.md` /
   `runpod-render.md`). Zero new infra, nothing fragile.
2. **noVNC + virtual display**, only if you genuinely must see an Isaac scene live.
   It's the only interactive Isaac path that survives RunPod's TCP-only network.
   Fragile (Isaac 4.0.0 + RTX 4090), unsupported by NVIDIA, throwaway.
3. **WebRTC** — best UX/latency and NVIDIA-supported, but **not possible on
   RunPod** (no UDP). Would require a different host that gives a public IP with
   open UDP.

**If you take option 2, least-friction concrete steps (via your existing SSH):**

1. Deploy a pod (Isaac Sim 4.0.0 image, RTX 4090) and SSH in as you already do
   (`ssh root@<ip> -p <port>`).
2. Fastest: run the reference bootstrap on the pod and open its printed URL —
   `curl -fsSL https://raw.githubusercontent.com/Sa3d-99/runpod_noVNC_isaac_sim/main/bootstrap.sh | bash`
   then *Connect → HTTP Service → port 8080* in the RunPod console. Set
   `VNC_PASSWORD` first if the URL will be shared.
3. Lower-latency / no-proxy alternative: have the stack bind VNC to
   `localhost:5900`, then from the Mac tunnel it over the SSH you already have —
   `ssh -L 5901:localhost:5900 root@<ip> -p <port>` — and connect a local viewer to
   `vnc://localhost:5901` (macOS Screen Sharing speaks `vnc://`, or use TigerVNC).
   This avoids exposing any extra RunPod port and dodges the proxy's 100 s timeout.

**One-paragraph recommendation.** For a hackathon, skip remote interactive Isaac
Sim: its only NVIDIA-supported remote transport is WebRTC, whose UDP media port
(47998) cannot traverse RunPod, which forwards TCP/HTTP only. Do interactive work
in MuJoCo locally on the Mac (already set up) and keep Isaac on RunPod strictly
headless, rendering frames to disk as `runpod-render.md` describes. Only if you
must eyeball an Isaac scene live, reach for noVNC on a GPU-backed virtual display
(the `runpod_noVNC_isaac_sim` reference, or VNC over your existing SSH tunnel) — it
works over TCP and needs a single port, but treat it as a fragile, version-pinned
(Isaac 4.0.0 + RTX 4090), unsupported throwaway, not part of the deliverable.
