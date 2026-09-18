#!/usr/bin/env bash
# Install MuJoCo + the interactive 3D viewer into a local virtualenv (.venv).
# Usage: ./install.sh            (then: source .venv/bin/activate)
set -euo pipefail

cd "$(dirname "$0")"
PYTHON="${PYTHON:-python3}"

# The viewer needs OpenGL + a windowing system. GLFW itself comes bundled with the
# `glfw` pip package; on Debian/Ubuntu we only warn if the GL runtime is missing.
if command -v dpkg >/dev/null 2>&1; then
  missing=()
  for pkg in libgl1 libegl1; do
    dpkg -s "$pkg" >/dev/null 2>&1 || missing+=("$pkg")
  done
  if [ ${#missing[@]} -gt 0 ]; then
    echo ">> WARNING: missing OpenGL libraries for the viewer. Run:"
    echo "     sudo apt-get install -y ${missing[*]}"
  fi
fi

if command -v uv >/dev/null 2>&1; then
  echo ">> Creating .venv with uv"
  uv venv --python "$PYTHON" .venv
  uv pip install --python .venv/bin/python -r requirements.txt
else
  echo ">> Creating .venv with venv/pip"
  "$PYTHON" -m venv .venv
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -r requirements.txt
fi

echo ">> Verifying installation"
.venv/bin/python scripts/check_install.py

cat <<'MSG'

Done. Next steps:
  source .venv/bin/activate
  python scripts/view_model.py                  # passive viewer running the demo scene
  python -m mujoco.viewer --mjcf=models/hello.xml   # standalone viewer app
(On macOS use `mjpython scripts/view_model.py` for the passive viewer.)
MSG
