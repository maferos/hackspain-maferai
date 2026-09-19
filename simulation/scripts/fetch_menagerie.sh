#!/usr/bin/env bash
# Fetch just the MuJoCo Menagerie models the rail scene needs.
#
# A full clone of mujoco_menagerie is several hundred megabytes; this pulls the
# UR10e and the Robotiq 2F-85 only (~47 MB) via a blobless sparse checkout into
# simulation/third_party/, which is gitignored. Run from simulation/:
#   bash scripts/fetch_menagerie.sh
set -euo pipefail

DEST="$(cd "$(dirname "$0")/.." && pwd)/third_party/mujoco_menagerie"
MODELS=(universal_robots_ur10e robotiq_2f85)

if [ -d "$DEST/.git" ]; then
  echo "Menagerie already present at $DEST; updating."
  git -C "$DEST" sparse-checkout set "${MODELS[@]}"
  git -C "$DEST" pull --ff-only
else
  git clone --filter=blob:none --no-checkout --depth 1 \
    https://github.com/google-deepmind/mujoco_menagerie.git "$DEST"
  git -C "$DEST" sparse-checkout init --cone
  git -C "$DEST" sparse-checkout set "${MODELS[@]}"
  git -C "$DEST" checkout
fi

for model in "${MODELS[@]}"; do
  test -f "$DEST/$model/$model.xml" || test -d "$DEST/$model" \
    || { echo "missing $model" >&2; exit 1; }
done
echo "Menagerie models ready: ${MODELS[*]}"
