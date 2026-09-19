#!/usr/bin/env bash
# Create the env for `armlab`, the promptable arm console.
# Usage: ./setup_act.sh          (then: .venv-act/bin/python -m armlab)
set -euo pipefail

cd "$(dirname "$0")"

# armlab attaches AutoBio's aloha_left.xml, so the submodule must be present.
# Only the XML and its meshes are used -- no plugin, hence no MuJoCo 3.3.0 pin.
if [ ! -f third_party/AutoBio/autobio/model/robot/aloha_left.xml ]; then
  ROOT="$(git rev-parse --show-toplevel)"
  REL="${PWD#"$ROOT"/}"
  echo ">> Fetching AutoBio submodule (~100 MB)"
  git -C "$ROOT" submodule update --init --depth 1 "$REL/third_party/AutoBio"
fi

# lerobot >= 0.5 requires Python >= 3.12, so .venv-autobio's 3.11 is too old.
if command -v uv >/dev/null 2>&1; then
  echo ">> Creating .venv-act (Python 3.12) with uv -- this pulls torch, ~1 GB"
  uv venv --clear --python 3.12 .venv-act
  uv pip install --python .venv-act/bin/python --torch-backend=cpu -r requirements-act.txt
else
  echo ">> Creating .venv-act with ${PYTHON:-python3.12}"
  "${PYTHON:-python3.12}" -m venv .venv-act
  .venv-act/bin/python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements-act.txt
fi

echo ">> Verifying: scene loads with actuators, lerobot imports"
.venv-act/bin/python - <<'PY'
import mujoco, lerobot  # noqa: F401
m = mujoco.MjModel.from_xml_path("models/minihannover_open_aloha_scene.xml")
names = [mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_ACTUATOR, i) for i in range(m.nu)]
assert m.nu == 14, f"expected 14 actuators, got {m.nu}: {names}"
print(f"  OK  mujoco {mujoco.__version__}, nu={m.nu}")
print(f"      {', '.join(names)}")
PY

cat <<'MSG'

Done. Launch the console with:
  .venv-act/bin/python -m armlab                      # http://localhost:8080
  .venv-act/bin/python -m armlab --headless --prompt "pick up SMP-0009 and put it on balance 1"
MSG
