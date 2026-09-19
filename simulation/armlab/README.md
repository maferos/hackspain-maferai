# armlab — a promptable arm in the MiniHannover lab

Type an instruction, watch the UR10e on its rail carry it out. Runs on
`models/minihannover_rail_scene.xml` — the team's scene, unmodified.

```bash
./setup_act.sh                                   # .venv-act (Python 3.12) + Menagerie
.venv-act/bin/python -m armlab                   # http://localhost:8080
```

```bash
# one instruction, no server, exit code says whether it worked
.venv-act/bin/python -m armlab --headless --prompt "pick up SMP-0044 and bring it to balance 2"
```

## What is where

| | |
|---|---|
| `scene.py` | Loads the rail scene; the liftable vessels and the balances |
| `embodiment.py` | Which actuators an action vector maps onto, and in what units |
| `skills.py` | `pick` / `place` / `home`, as generators of action vectors |
| `policies.py` | **The swap seam** — any lerobot checkpoint, bound to the robot |
| `config/policies.toml` | The model catalogue. Adding a checkpoint is adding a block. |
| `planner.py` | Instruction → plan. Claude, falling back to a regex grammar. |
| `runtime.py` | The sim loop: physics, rendering, the policy router, hot swap |
| `server.py` + `web/` | The console (FastAPI, port 8080) |

## What it reuses

Almost all of the robot knowledge is the team's, not this package's:

- **`scripts/rail_kinematics.py`** — `reach()` (which steps the carriage along the
  rail to escape the arm's inner dead zone), `solve_any()`, `set_rail()`,
  `bottles()`, and `read_grip()` off the 2F-85's pad sensors.
- **`scripts/grasp_test.py`** — the grasp sequence `skills.pick` follows: approach,
  descend to `GRASP_FRACTION` up the vessel wall, close until the pads report
  contact, lift. It scores 12/12 on this bench with physics running.

There is no IK in this package. There was, and it was deleted: besides
duplicating the above, it assumed the tool site's **+X** pointed out of the
fingers, which is ALOHA's convention. Here the approach axis is the **+Z** of
`arm_grip_pinch`. It would have aimed the wrist sideways and raised nothing.

## Swapping the model

The point of the design: **the model is a config value, not a code path.**

Nothing in `policies.py` branches on policy class. A lerobot checkpoint describes
itself — `config.json` names its type, and `input_features` / `output_features`
declare what it wants and what it returns — so the adapter builds the observation
dict from that declaration and renders each camera at the shape the feature asks
for. ACT, Diffusion Policy, SmolVLA and π0 all load through the same path.

**The catalogue ships empty, on purpose.** This bench runs eight actuators — the
rail, six arm joints and the Robotiq 2F-85 — and nothing on the Hugging Face Hub
is trained for that. The ACT checkpoints there are ALOHA (14-dim bimanual),
SO-100/SO-101 (6), Koch; every one a different robot. Load one and you get:

```
lerobot/act_aloha_sim_transfer_cube_human emits 14-dim actions but embodiment
'ur10e_rail' has 8 actuators -- wrong robot for this checkpoint
```

which is the seam doing its job rather than letting a mismatched checkpoint drive
the arm. So the console runs on the scripted skills, and the first checkpoint for
this embodiment drops into `config/policies.toml` with no code change —
`repo_id` takes a local directory as happily as a Hub id, which is where the
`research/experiments.md` P0/B1 path lands.

One more consequence worth knowing: if a checkpoint declares a **language** input,
the operator's prompt is passed into the model verbatim. With ACT the prompt only
*selects* a skill — ACT has no language input. With SmolVLA the same prompt
becomes a model input, and the arm is genuinely language-conditioned.

Checkpoints pushed before lerobot 0.5 keep normalisation inside the model rather
than in processor files, and fail to load with a migration error. `policies.py`
catches that, runs lerobot's migration into `~/.cache/armlab/policies/` once, and
loads from there.

## Known limits

- **Three of the four balances cannot receive anything.** `assets/balance/
  balance.xml` is an analytical balance with a closed glass draft shield,
  modelled as one collision box over the whole 0.311 m instrument — no pan, no
  joint, no force sensor, so weighing is not simulated either
  (`research/experiments.md` §1 flags the same). `place` therefore brings the
  vessel to the named balance and sets it on the bench beside it, which is what
  a technician would do before opening the shield.

  The exception is `balance_2_`, the middle front-row station, which
  `generate_rail_scene.py` swaps for `assets/balance_open/` — no shield, a pan
  that collides, and the beaker standing on it. Both tools' scenes get it: it is
  the bench's weighing station, not the pipette's.
- **Only the twelve `dyn_*` vessels are pickable.** The seven hand-placed
  `loose_*` work samples are free bodies too, but they sit at the bench's far
  edge or behind the gantry beam, outside the envelope the rail was sized for.
  They are not in the inventory, so asking for one is refused by name.
- **Set-down spots are searched, not assumed.** The carriage rides at y = 0.14
  and the arm reaches 1.30 m, so the aisle side of a balance at y = -1.16 is out
  of reach; `skills.SET_DOWN` steps towards the rail and takes the first spot
  that solves.
- **The sim runs at roughly 0.5-0.7× real time** on CPU. `--fast` removes the
  real-time cap, not the cost.
