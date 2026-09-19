"""armlab -- a promptable arm in the MiniHannover lab scene.

Three layers, each usable on its own:

    scene / embodiment / ik / skills   the robot and what it can be told to do
    policies                           any lerobot checkpoint, bound to that robot
    runtime / server                   the sim loop and the console on top of it

Run the console with `python -m armlab` from `simulation/`.
"""

__all__ = ['embodiment', 'ik', 'planner', 'policies', 'runtime', 'scene', 'skills']
