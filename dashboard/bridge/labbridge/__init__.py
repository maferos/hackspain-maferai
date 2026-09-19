"""Bridge between the simulation loop and the dashboard.

Two WebSocket servers, both safe to call from the synchronous simulation
thread:

- :class:`StateServer` broadcasts ``LabState`` messages (``snapshot``,
  ``state_update``, ``event``, ``mass_sample``) on ``ws://host:8765/state``.
- :class:`FrameServer` broadcasts JPEG frames per camera on
  ``ws://host:8766/frames/<camera>``.

:mod:`labbridge.state` builds the JSON documents in the shape the console
expects, and :mod:`labbridge.mujoco_adapter` reads furniture, free containers
and camera images out of a MuJoCo model.
"""

from labbridge.server import FrameServer, StateServer
from labbridge.state import (
    balance_state,
    camera,
    deep_merge,
    empty_state,
    event,
    ingredient,
    perception_state,
    pipeline_node,
    robot_state,
    step,
    vec3,
    workcell,
)

__all__ = [
    "FrameServer",
    "StateServer",
    "balance_state",
    "camera",
    "deep_merge",
    "empty_state",
    "event",
    "ingredient",
    "perception_state",
    "pipeline_node",
    "robot_state",
    "step",
    "vec3",
    "workcell",
]
