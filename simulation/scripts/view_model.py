"""Open a MuJoCo model in the interactive 3D viewer and simulate it in real time.

Usage:
    python scripts/view_model.py [path/to/model.xml]
On macOS run with `mjpython` instead of `python` (required by launch_passive).
"""
import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer

DEFAULT_MODEL = Path(__file__).resolve().parent.parent / "models" / "hello.xml"


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MODEL
    model = mujoco.MjModel.from_xml_path(str(path))
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            step_start = time.time()
            mujoco.mj_step(model, data)
            viewer.sync()
            # Keep simulation time roughly in sync with wall-clock time.
            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    main()
