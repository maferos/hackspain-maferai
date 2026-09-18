#!/usr/bin/env bash
# Fetch the AutoBio lab models and create the MuJoCo 3.3.0 env needed to view them.
# Usage: ./setup_autobio.sh     (then: .venv-autobio/bin/python scripts/view_autobio.py)
set -euo pipefail

cd "$(dirname "$0")"
DEST=third_party/AutoBio

if [ ! -d "$DEST/.git" ]; then
  echo ">> Cloning AutoBio into $DEST (~100 MB)"
  git clone --depth 1 https://github.com/autobio-bench/AutoBio.git "$DEST"
else
  echo ">> $DEST already present, pulling latest"
  git -C "$DEST" pull --ff-only
fi

# AutoBio targets Python 3.11 (see its autobio/README.md).
if command -v uv >/dev/null 2>&1; then
  echo ">> Creating .venv-autobio (Python 3.11) with uv"
  uv venv --python 3.11 .venv-autobio
  uv pip install --python .venv-autobio/bin/python -r requirements-autobio.txt
else
  echo ">> Creating .venv-autobio with ${PYTHON:-python3.11}"
  "${PYTHON:-python3.11}" -m venv .venv-autobio
  .venv-autobio/bin/python -m pip install -r requirements-autobio.txt
fi

echo ">> Verifying: loading every AutoBio scene"
.venv-autobio/bin/python scripts/view_autobio.py --check

cat <<'MSG'

Done. Launch the 3D viewer with:
  .venv-autobio/bin/python scripts/view_autobio.py            # default scene: pickup
  .venv-autobio/bin/python scripts/view_autobio.py --list     # list available scenes
  .venv-autobio/bin/python scripts/view_autobio.py mani_thermal_cycler
MSG
