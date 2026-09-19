#!/usr/bin/env bash
# Train the bench detector unattended on a GPU pod, as docs/YOLO26_TRAINING.md
# describes: select the training set from the rendered frames, crop it to the
# bench, fine-tune YOLO26n at 1920 px, score it on every test set, and leave
# behind everything the presentation needs.
#
#   R=/workspace/code SRC=/workspace/fixedcam OUT=/workspace/out \
#     bash computer-vision/scripts/train_pod.sh [NAME]
#
# R is this repository, SRC the rendered splits (their gt.json and frames), NAME
# the run's name (default n_sel_1920). Every stage is skipped if its output is
# there, so a dropped pod resumes. Progress: $OUT/STAGE and $OUT/run.log.
#
# $OUT when it ends:
#   weights/<NAME>.pt                      the model
#   run/                                   Ultralytics' own folder: results.csv,
#                                          results.png, PR and F1 curves, confusion
#                                          matrix, train and validation batches
#   plots/pose_map_train.png               where the camera stood, training set
#   plots/training_curves.png              losses and scores by epoch
#   plots/before_after.png                 rail against NAME on every test set
#   score_<detector>.md, viewpoint/        the numbers behind before_after
#   selection.json                         the frames kept in every cell
set -uo pipefail
R=${R:-/workspace/code}; SRC=${SRC:-/workspace/fixedcam}; OUT=${OUT:-/workspace/out}
NAME=${1:-n_sel_1920}
START=${START:-weights/yolo26n_rail_general.pt}   # fine-tune from the detector in use
DATA=${DATA:-/root/yolo_sel}
TESTS=${TESTS:-rail_test,rail_test_shift,orbit_test,close_test,overhead_test,dark_test,orbit_dark_test}
mkdir -p "$OUT/plots" "$OUT/weights"
exec > >(tee -a "$OUT/run.log") 2>&1
stage() { echo "== $(date -u +%H:%M:%S) $*"; echo "$*" > "${STAGE_FILE:-$OUT/STAGE}"; }
fail() { stage "FAILED: $*"; exit 1; }

stage deps
(apt-get update -qq && apt-get install -y -qq libgl1 libglib2.0-0 > /dev/null)
pip install -q -r "$R/computer-vision/requirements.txt" mujoco ultralytics matplotlib \
  > "$OUT/pip.log" 2>&1 || fail pip
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
cd "$R/computer-vision" || fail "no repository at $R"
[ -f "$START" ] || fail "no starting weights at $START"

stage select
# The selection lives on the pod's own disk and is linked into SRC, so it costs
# the volume nothing: SRC may be a network volume with a quota.
SEL=${SEL:-/root/sel}
if [ ! -f "$SEL/sel_train/gt.json" ]; then
  rm -rf "$SEL" "$SRC/sel_train" "$SRC/sel_val" && mkdir -p "$SEL"
  python scripts/select_frames.py --src "$SRC" --out "$SEL" || fail select
fi
for s in sel_train sel_val; do rm -rf "$SRC/$s"; ln -sfn "$SEL/$s" "$SRC/$s" || fail "link $s"; done
cp "$SEL/selection.json" "$OUT/"
python scripts/pose_map.py sel_train --src "$SRC" --title "the training set" \
  --out "$OUT/plots/pose_map_train.png" || fail "pose map"

stage convert
[ -f "$DATA/data.yaml" ] || python scripts/fixedcam_to_yolo.py sel_train:train sel_val:val \
  --src "$SRC" --out "$DATA" --crop || fail convert

# Ultralytics nests project= under runs/detect/.
best=$(ls runs/detect/runs/orbit/"$NAME"/weights/best.pt runs/orbit/"$NAME"/weights/best.pt 2>/dev/null | head -1)
if [ -z "$best" ]; then
  stage "train $NAME"
  python runs/orbit/train_yolo26_gpu.py "$DATA/data.yaml" --size n --imgsz 1920 \
    --weights "$START" --name "$NAME" --epochs "${EPOCHS:-50}"     --patience "${PATIENCE:-12}" --workers "${WORKERS:-16}" --cache "${CACHE:-ram}" || fail train
  best=$(ls runs/detect/runs/orbit/"$NAME"/weights/best.pt runs/orbit/"$NAME"/weights/best.pt 2>/dev/null | head -1)
fi
[ -n "$best" ] || fail "no best.pt after training"
run=$(dirname "$(dirname "$best")")
cp "$best" "$OUT/weights/$NAME.pt"
rm -rf "$OUT/run" && mkdir "$OUT/run" && cp "$run"/*.csv "$run"/*.png "$run"/*.jpg "$run"/*.yaml "$OUT/run/" 2>/dev/null

# Both detectors the same way: on the bench crop, threshold from the validation set.
for pair in "rail_now:$START" "$NAME:$best"; do
  stage "score ${pair%%:*}"
  python scripts/viewpoint_study.py "${pair#*:}" --name "${pair%%:*}" --crop --src "$SRC" \
    --pick-on sel_val --splits "$TESTS" > "$OUT/score_${pair%%:*}.md" || fail "score ${pair%%:*}"
done
rm -rf "$OUT/viewpoint" && cp -r results/viewpoint "$OUT/viewpoint"

stage plots
python scripts/training_plots.py --run "$run" --out "$OUT/plots" \
  --scores "rail, before=results/viewpoint/rail_now" "$NAME, retrained=results/viewpoint/$NAME" \
  || fail plots
stage DONE
