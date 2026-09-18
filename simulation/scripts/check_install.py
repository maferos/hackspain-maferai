"""Headless sanity check: load the demo model and step the physics."""
from pathlib import Path

import mujoco

MODEL = Path(__file__).resolve().parent.parent / "models" / "hello.xml"

model = mujoco.MjModel.from_xml_path(str(MODEL))
data = mujoco.MjData(model)
start_z = data.qpos[2]
while data.time < 1.0:
    mujoco.mj_step(model, data)

print(f"MuJoCo {mujoco.__version__} OK — box fell from z={start_z:.2f} to z={data.qpos[2]:.2f}")
