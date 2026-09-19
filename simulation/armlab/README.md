# armlab — a promptable arm in the MiniHannover lab

A bimanual ALOHA cell on the open desk, driven either by scripted skills or by a
Hugging Face checkpoint, and a console you type instructions into.

```bash
./setup_act.sh                                   # creates .venv-act (Python 3.12)
.venv-act/bin/python -m armlab                   # http://localhost:8080
```

```bash
# one instruction, no server, exit code says whether it worked
.venv-act/bin/python -m armlab --headless --prompt "pick up SMP-0009 and put it on the tray"

# run a Hugging Face checkpoint closed-loop
.venv-act/bin/python -m armlab --headless --policy act_transfer_cube --seconds 20

# just look at the scene
.venv-act/bin/python scripts/view_model.py models/minihannover_open_aloha_scene.xml
```

## What is where

| | |
|---|---|
| `scene.py` | Loads the scene; maps `loose_N ↔ SMP-xxxx`, placement targets, grasp geometry |
| `embodiment.py` | Which actuators an action vector maps onto, and in what units |
| `ik.py` | Damped least-squares IK with restarts (~90 lines, no dependency) |
| `skills.py` | `pick` / `place` / `home`, as generators of action vectors |
| `policies.py` | **The swap seam** — any lerobot checkpoint, bound to the robot |
| `config/policies.toml` | The model catalogue. Adding a checkpoint is adding a block. |
| `planner.py` | Instruction → plan. Claude, falling back to a regex grammar. |
| `runtime.py` | The sim loop: physics, rendering, the policy router, hot swap |
| `server.py` + `web/` | The console (FastAPI, port 8080) |

The scene itself is generated — `scripts/generate_minihannover_open.py`
(`build_arm_scene`) writes `models/minihannover_open_aloha_scene.xml`. Don't edit
that file; change the generator and re-run it.

## Swapping the model

The point of the design: **the model is a config value, not a code path.**

```toml
[act_insertion]
repo_id = "lerobot/act_aloha_sim_insertion_human"
embodiment = "aloha_bimanual"
cameras = { "observation.images.top" = "top" }
control_hz = 50
label = "ACT · ALOHA insertion"
```

Nothing in `policies.py` branches on policy class. A lerobot checkpoint describes
itself — `config.json` names its type, and `input_features` / `output_features`
declare what it wants and what it returns — so the adapter builds the observation
dict from that declaration and renders each camera at the shape the feature asks
for. ACT, Diffusion Policy, SmolVLA and π0 all load through the same path.

Two consequences worth knowing:

- A checkpoint whose action shape doesn't match the robot's 14 actuators is
  **rejected at load**, naming both numbers, with the previous policy left running.
- If a checkpoint declares a **language** input, the operator's prompt is passed
  into the model verbatim. With ACT loaded the prompt only *selects* a skill —
  ACT has no language input. Load SmolVLA and the same prompt becomes a model
  input, and the arm is genuinely language-conditioned. Same runtime, same scene.

Checkpoints pushed before lerobot 0.5 keep normalisation inside the model rather
than in processor files, and fail to load with a migration error. `policies.py`
catches that, runs lerobot's migration into `~/.cache/armlab/policies/` once, and
loads from there — so from the console an old checkpoint is indistinguishable
from a new one.

## Known limits

- **The balances cannot receive anything.** `assets/balance` is an analytical
  balance with a closed glass draft shield, modelled as one collision box over
  the whole instrument — there is no exposed pan, and no joint or force sensor, so
  weighing is not simulated either. This is the gap `research/experiments.md` §1
  flags. The cell has a **tray** instead, which is what `place` targets.
- **The gripper opens to 57.5 mm**, which rules out the wider powder bottles.
  `pick` refuses them by name rather than failing halfway.
- **ACT is not promptable and was not trained here.** The checkpoint knows
  gym-aloha cube-transfer. The cell reproduces gym-aloha's arm spacing, `top`
  camera and cube exactly, and adds a mat and a backdrop so the camera sees
  something close to the dark tabletop it was trained on — but the surrounding lab
  is still out of distribution. Treat its behaviour as a demonstration that the
  policy path is real, not as a lab capability.
- **The sim runs at roughly 0.2–0.5× real time** on CPU. 3724 geoms with
  `noslip_iterations` and `multiccd` is not cheap; those settings are what make
  grasping work at all. `--fast` removes the real-time cap but not the cost.
