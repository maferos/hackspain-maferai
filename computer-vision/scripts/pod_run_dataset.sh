#!/usr/bin/env bash
# Runs unattended on a RunPod pod as /root/repo/pod_run.sh: render the whole
# rail dataset (wall mount, orbit, close, low cameras; seeded bench patterns;
# varied labs) with MuJoCo on EGL, check it, then hand over to train_pod.sh,
# which selects the training set, trains YOLO26n, scores it and draws the
# figures. Everything the laptop needs afterwards is left under /root/out,
# which the pod serves over its HTTPS proxy:
#   STAGE, run.log          progress
#   report.tgz              dataset_report.py: data.json, thumbnail sheets, samples
#   gt.tgz                  the gt.json of every split
#   train.tgz               weights, Ultralytics' run folder, plots, scores
# The frames stay on the network volume under $DATA.
set -uo pipefail
OUT=/root/out; R=/root/repo; CV=$R/computer-vision
DATA=${DATA:-/workspace/fixedcam_v2}
NPROC=$(nproc); PARTS=$(( NPROC > 24 ? 24 : NPROC ))
stage() { echo "== $(date -u +%H:%M:%S) $*"; echo "$*" > "$OUT/STAGE"; }
fail() { stage "FAILED: $*"; exit 1; }

stage deps
# The bundle comes from a Windows checkout: shell scripts carry CRLF endings.
find "$R" -name "*.sh" -exec sed -i 's/\r$//' {} +
(apt-get update -qq && apt-get install -y -qq libegl1 libgl1 libglib2.0-0 libgomp1 git > /dev/null) &
pip install -q "mujoco==3.13.0" "ultralytics==8.4.155" "python-barcode>=0.16" "requests>=2.31" \
    matplotlib psutil > "$OUT/pip.log" 2>&1 &
wait
export MUJOCO_GL=egl
python -c "import mujoco, cv2, matplotlib; print('mujoco', mujoco.__version__, 'cv2', cv2.__version__)" || fail deps
(cd "$R/simulation" && bash scripts/fetch_menagerie.sh) > "$OUT/menagerie.log" 2>&1 || fail menagerie
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
echo "cpus $NPROC, parts $PARTS"; free -g | head -2; df -h /workspace | tail -1
mkdir -p "$DATA" "$OUT/render_logs"
# The code the data was rendered with, next to the data.
rm -rf /workspace/code_v2 && cp -r "$R" /workspace/code_v2 && rm -rf /workspace/code_v2/simulation/third_party

stage render
cd "$CV" || fail cd
SPECS="rail_train:2500 rail_val:250 rail_test:150 rail_test_shift:100 \
orbit_train:3000 orbit_val:300 orbit_test:300 \
close_train:1500 close_val:150 close_test:150 \
low_train:800 low_val:100 low_test:100 \
dark_test:150 orbit_dark_test:150 overhead_test:150 \
pattern_test:100 pattern_orbit_test:100 lab_test:150 lab_rail_test:100"
complete() {  # split frames: is its merged gt.json already there, whole?
  [ "$(python -c "import json,sys; print(len(json.load(open(sys.argv[1]))['frames']))"        "$DATA/$1/gt.json" 2>/dev/null)" = "$2" ]
}
TODO=""
for spec in $SPECS; do complete "${spec%%:*}" "${spec#*:}" || TODO="$TODO $spec"; done
echo "to render:${TODO:- nothing, every split is complete}"
render_part() {  # split frames part
  python scripts/fixedcam_dataset.py --splits "$1" --frames "$2" --part "$3/$PARTS" \
      --out "$DATA" > "/root/out/render_logs/$1_$3.log" 2>&1
}
export -f render_part; export PARTS DATA
for spec in $TODO; do
  for i in $(seq 0 $((PARTS - 1))); do echo "${spec%%:*} ${spec#*:} $i"; done
done | xargs -P "$PARTS" -n 3 bash -c 'render_part "$0" "$1" "$2" || echo "render failed: $0 part $2"'
# A part that died keeps no gt file past its last write: render it again, alone.
for spec in $TODO; do
  s=${spec%%:*}; n=${spec#*:}
  for i in $(seq 0 $((PARTS - 1))); do
    want=$(( (n - i + PARTS - 1) / PARTS ))
    have=$(python -c "import json,sys; print(len(json.load(open(sys.argv[1]))['frames']))" \
           "$DATA/$s/gt.part${i}of${PARTS}.json" 2>/dev/null || echo 0)
    if [ "$have" != "$want" ]; then
      echo "retry $s part $i ($have of $want)"; render_part "$s" "$n" "$i" || echo "retry failed: $s part $i"
    fi
  done
done
ALL=$(for spec in $TODO; do printf '%s,' "${spec%%:*}"; done)
[ -z "$ALL" ] || python scripts/fixedcam_dataset.py --splits "${ALL%,}" --merge --out "$DATA" || fail merge
for spec in $SPECS; do
  s=${spec%%:*}; n=${spec#*:}
  have=$(python -c "import json,sys; print(len(json.load(open(sys.argv[1]))['frames']))" "$DATA/$s/gt.json")
  echo "$s: $have of $n frames"
  [ "$have" = "$n" ] || fail "render incomplete: $s $have of $n"
done
du -sh "$DATA"

stage report
rm -rf "$DATA/sel_train" "$DATA/sel_val"   # a selection is not a split of the render
if [ -f /workspace/out_v2/report.tgz ] && [ -z "$TODO" ]; then
  cp /workspace/out_v2/report.tgz "$OUT/report.tgz"
else
  python scripts/dataset_report.py "$DATA" "$OUT/report" --workers "$PARTS" || fail report
  tar czf "$OUT/report.tgz" -C "$OUT" report
fi
tar czf "$OUT/gt.tgz" -C "$(dirname "$DATA")" $(cd "$(dirname "$DATA")" && ls "$(basename "$DATA")"/*/gt.json)

# Train, score and draw. train_pod.sh writes its own stages from here on.
export R SRC="$DATA" OUT_TRAIN="$OUT/train" EPOCHS="${EPOCHS:-25}" PATIENCE="${PATIENCE:-8}"
export TESTS="rail_test,rail_test_shift,orbit_test,close_test,overhead_test,low_test,dark_test,orbit_dark_test,pattern_test,pattern_orbit_test,lab_test,lab_rail_test"
OUT="$OUT_TRAIN" STAGE_FILE="$OUT/STAGE" bash "$CV/scripts/train_pod.sh" n_full_1920
status=$?
tar czf "$OUT/train.tgz" -C "$OUT" train
mkdir -p /workspace/out_v2 && cp -r "$OUT/train" "$OUT/report.tgz" "$OUT/gt.tgz" /workspace/out_v2/ 2>/dev/null
[ "$status" = 0 ] && stage DONE || stage "FAILED: training, see train/run.log"
