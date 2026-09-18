"""Open an AutoBio lab scene in the MuJoCo interactive 3D viewer.

Requires the MuJoCo 3.3.0 env created by setup_autobio.sh:
    .venv-autobio/bin/python scripts/view_autobio.py [scene] [--list] [--check]

`scene` is a name from models/ (e.g. autobio_lab, the default) or from
third_party/AutoBio/autobio/model/scene (e.g. pickup, mani_thermal_cycler), or a
path to an MJCF file. Scenes with spawn zones (autobio_lab) also run
scripts/spawner.py: lab workers walk up to the table ends and drop tubes. The stock
`python -m mujoco.viewer` cannot open most AutoBio scenes because it has no way
to load AutoBio's plugin library first.
"""
import argparse
import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer

from spawner import Spawner

REPO = Path(__file__).resolve().parent.parent
LOCAL_SCENES = REPO / "models"
AUTOBIO = REPO / "third_party" / "AutoBio" / "autobio"
SCENES = AUTOBIO / "model" / "scene"
PLUGIN = AUTOBIO / f"libmjlab.so.{mujoco.__version__}"


def load_plugin() -> None:
    if not PLUGIN.exists():
        sys.exit(
            f"AutoBio plugin not found at {PLUGIN}.\n"
            "Run ./setup_autobio.sh first (AutoBio needs mujoco==3.3.0, "
            f"this interpreter has {mujoco.__version__})."
        )
    mujoco.mj_loadPluginLibrary(str(PLUGIN))


def resolve_scene(name: str) -> Path:
    path = Path(name)
    if path.suffix == ".xml" and path.exists():
        return path
    for path in (LOCAL_SCENES / f"{name}.xml", SCENES / f"{name}.xml"):
        if path.exists():
            return path
    sys.exit(f"Unknown scene '{name}'. Available: {', '.join(list_scenes())}")


def list_scenes() -> list[str]:
    return ["autobio_lab"] + sorted(p.stem for p in SCENES.glob("*.xml"))


def check_all() -> None:
    failed = 0
    for name in list_scenes():
        try:
            model = mujoco.MjModel.from_xml_path(str(resolve_scene(name)))
            data = mujoco.MjData(model)
            mujoco.mj_step(model, data, nstep=100)
            extra = ""
            if Spawner.applies_to(model):
                extra = check_spawner(model, data)
            print(f"  OK    {name:24s} bodies={model.nbody}{extra}")
        except Exception as exc:  # report every scene, don't stop at the first
            failed += 1
            print(f"  FAIL  {name:24s} {str(exc).splitlines()[0]}")
    sys.exit(1 if failed else 0)


def check_spawner(model, data) -> str:
    """Drop enough tubes to recycle the whole pool; every tube must end up on the table."""
    spawner = Spawner(model, data, interval=1.5, seed=0)
    while data.time < 30.0:
        mujoco.mj_step(model, data)
        spawner.step()
    top = 0.824
    heights = [data.qpos[adr + 2] for adr in spawner.tubes]
    if spawner.spawned <= len(spawner.tubes) or not all(top - 0.01 < z < top + 0.2 for z in heights):
        raise RuntimeError(f"spawner: {spawner.spawned} drops, tube heights {heights}")
    return f"  spawner: {spawner.spawned} tubes dropped and on the table"


def view(path: Path, interval: float) -> None:
    model = mujoco.MjModel.from_xml_path(str(path))
    data = mujoco.MjData(model)
    spawner = Spawner(model, data, interval) if Spawner.applies_to(model) else None
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            step_start = time.time()
            mujoco.mj_step(model, data)
            if spawner:
                spawner.step()
            viewer.sync()
            remaining = model.opt.timestep - (time.time() - step_start)
            if remaining > 0:
                time.sleep(remaining)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("scene", nargs="?", default="autobio_lab")
    parser.add_argument("--list", action="store_true", help="list available scenes")
    parser.add_argument("--check", action="store_true", help="load and step every scene headless")
    parser.add_argument("--interval", type=float, default=3.0,
                        help="seconds between worker spawns in scenes with spawn zones")
    args = parser.parse_args()

    if args.list:
        print("\n".join(list_scenes()))
        return
    load_plugin()
    if args.check:
        check_all()
    view(resolve_scene(args.scene), args.interval)


if __name__ == "__main__":
    main()
