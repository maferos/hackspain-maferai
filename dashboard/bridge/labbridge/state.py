"""Builders for the console's ``LabState`` document.

This is the Python side of ``dashboard/src/state/types.ts``. Everything is a
plain ``dict`` so it serialises to JSON as is and merges with ``deep_merge``
the same way the console merges a ``state_update`` patch: objects merge,
arrays and scalars replace.

Frames: the simulation world frame, metres. Perception fields must hold what
the cameras and the barcode reader produce; simulator poses go under
``evaluator`` only.
"""

from __future__ import annotations

from typing import Any, Iterable, Literal, Sequence

Vec3 = dict[str, float]
CameraId = Literal["overview", "robot", "wrist"]
Phase = Literal["liquid", "powder"]
ModuleStatus = Literal["idle", "active", "ok", "warn", "error"]
StepStatus = Literal["queued", "active", "completed", "retrying", "failed"]

PIPELINE_NODES: tuple[tuple[str, str], ...] = (
    ("camera", "Camera"),
    ("detection", "Object detection"),
    ("localization", "3D localization"),
    ("barcode", "Barcode ID"),
    ("planner", "Task planner"),
    ("motion", "Motion"),
    ("dosing", "Dosing"),
    ("verification", "Verification"),
)
"""The eight modules of the autonomy pipeline, in display order."""


def vec3(x: float, y: float, z: float) -> Vec3:
    """Build a position in the world frame."""
    return {"x": float(x), "y": float(y), "z": float(z)}


def deep_merge(base: dict, patch: dict) -> dict:
    """Merge ``patch`` into a copy of ``base``: dicts merge, everything else replaces."""
    out = dict(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def camera(cam_id: CameraId, name: str, label: str, resolution: str) -> dict:
    """Describe one camera of the workcell.

    Args:
        cam_id: Slot in the console: ``overview``, ``robot`` or ``wrist``.
        name: Camera name in the scene, e.g. ``general``.
        label: Short uppercase label drawn over the viewport.
        resolution: e.g. ``1920×1080``.
    """
    return {"id": cam_id, "name": name, "label": label, "resolution": resolution}


def workcell(
    bench: dict[str, float],
    balances: Sequence[dict],
    cameras: Sequence[dict],
    rail: dict[str, float] | None = None,
) -> dict:
    """Static description of the workcell, sent once in the snapshot.

    Args:
        bench: ``{x0, x1, y0, y1, top}`` worktop extent, metres.
        balances: ``[{id, position, active}]``; ``active`` marks the one that
            holds the formulation vessel.
        cameras: From :func:`camera`.
        rail: ``{x0, x1, y}`` if the arm rides a linear axis.
    """
    return {"bench": dict(bench), "balances": list(balances), "rail": dict(rail) if rail else None, "cameras": list(cameras)}


def ingredient(
    ing_id: str,
    compound: str,
    target_mass: float,
    phase: Phase = "liquid",
    cas: str | None = None,
    dispensed_mass: float | None = None,
    container_id: str | None = None,
    container_ml: float | None = None,
    status: str = "queued",
) -> dict:
    """One recipe line. ``container_id`` stays ``None`` until the barcode is verified."""
    return {
        "id": ing_id,
        "compound": compound,
        "cas": cas,
        "phase": phase,
        "targetMass": float(target_mass),
        "dispensedMass": None if dispensed_mass is None else float(dispensed_mass),
        "containerId": container_id,
        "containerMl": container_ml,
        "status": status,
    }


def step(
    step_id: str,
    label: str,
    ingredient_id: str | None = None,
    status: StepStatus = "queued",
    attempt: int = 1,
    started_at: float | None = None,
    completed_at: float | None = None,
    detail: Iterable[tuple[str, str]] = (),
) -> dict:
    """One row of the execution plan."""
    return {
        "id": step_id,
        "label": label,
        "ingredientId": ingredient_id,
        "status": status,
        "attempt": attempt,
        "startedAt": started_at,
        "completedAt": completed_at,
        "detail": [list(kv) for kv in detail],
    }


def pipeline_node(
    node_id: str,
    model: str,
    lines: Sequence[str],
    status: ModuleStatus = "ok",
    details: Iterable[tuple[str, str]] = (),
    title: str | None = None,
) -> dict:
    """One module card of the autonomy pipeline; ``node_id`` is one of PIPELINE_NODES."""
    titles = dict(PIPELINE_NODES)
    return {
        "id": node_id,
        "title": title or titles.get(node_id, node_id),
        "model": model,
        "lines": list(lines),
        "status": status,
        "details": [list(kv) for kv in details],
    }


def event(time: float, message: str, level: str = "info") -> dict:
    """An ``event`` message for :meth:`StateServer.event`; ``level`` is info/ok/warn/error."""
    return {"type": "event", "time": float(time), "message": message, "level": level}


def robot_state(
    fsm_state: str,
    base_position: Vec3,
    ee_position: Vec3,
    arm: str = "Franka Panda",
    end_effector: str = "GRIPPER",
    target_object: str | None = None,
    compound: str | None = None,
    gripper: str = "open",
    current_action: str = "",
    tilt_deg: float = 0.0,
    ik_error_mm: float = 0.0,
    distance_to_target: float | None = None,
    recoveries: int = 0,
    replans: int = 0,
) -> dict:
    """Arm and planner telemetry."""
    return {
        "fsmState": fsm_state,
        "arm": arm,
        "endEffector": end_effector,
        "targetObject": target_object,
        "compound": compound,
        "basePosition": base_position,
        "eePosition": ee_position,
        "gripper": gripper,
        "currentAction": current_action,
        "tiltDeg": float(tilt_deg),
        "ikErrorMm": float(ik_error_mm),
        "distanceToTarget": distance_to_target,
        "recoveries": recoveries,
        "replans": replans,
    }


def perception_state(
    active_camera: CameraId = "overview",
    vessels: Sequence[dict] = (),
    target_index: int | None = None,
    target: str | None = None,
    target_class: str | None = None,
    confidence: float | None = None,
    barcode: str | None = None,
    barcode_status: str = "idle",
    identity: str | None = None,
    container_ml: float | None = None,
    estimated_position: Vec3 | None = None,
    localization_error_mm: float | None = None,
    target_box: dict | None = None,
    modules: dict[str, ModuleStatus] | None = None,
) -> dict:
    """What the cameras, detector and barcode reader produced.

    ``vessels`` are ``{index, id, cls, confidence, position, stale}``; ``id`` is
    the sample ID once its barcode has been read, else ``None``.
    """
    return {
        "activeCamera": active_camera,
        "detections": len(vessels),
        "vessels": list(vessels),
        "targetIndex": target_index,
        "target": target,
        "targetClass": target_class,
        "confidence": confidence,
        "barcode": barcode,
        "barcodeStatus": barcode_status,
        "identity": identity,
        "containerMl": container_ml,
        "estimatedPosition": estimated_position,
        "localizationErrorMm": localization_error_mm,
        "targetBox": target_box,
        "modules": modules or {"detector": "idle", "localizer": "idle", "barcode": "idle", "wristCam": "idle"},
    }


def balance_state(
    balance_id: str | None,
    net_mass: float = 0.0,
    total_mass: float = 0.0,
    target_mass: float = 0.0,
    batch_target_mass: float = 0.0,
    flow_rate: float = 0.0,
    mode: str = "stopped",
    stable: bool = True,
    ingredient_id: str | None = None,
    history: Sequence[dict] = (),
    history_window: float = 30.0,
) -> dict:
    """Balance readout. Send ``mass_sample`` messages to grow the chart instead of resending history."""
    return {
        "id": balance_id,
        "netMass": float(net_mass),
        "totalMass": float(total_mass),
        "targetMass": float(target_mass),
        "batchTargetMass": float(batch_target_mass),
        "flowRate": float(flow_rate),
        "mode": mode,
        "stable": bool(stable),
        "ingredientId": ingredient_id,
        "history": list(history),
        "historyWindow": float(history_window),
    }


def empty_state(run_id: str = "RUN-000", workcell_doc: dict | None = None) -> dict:
    """A complete ``LabState`` with nothing running, to start a snapshot from."""
    return {
        "run": {"id": run_id, "status": "idle", "mode": "autonomous", "elapsedSeconds": 0.0, "progress": 0.0, "phase": None, "simulated": True},
        "recipe": {"id": "—", "name": "No recipe loaded", "targetMass": 0.0, "ingredients": []},
        "execution": {"currentStepId": None, "steps": []},
        "balance": balance_state(None),
        "robot": robot_state("IDLE", vec3(0, -1.05, 0.9), vec3(0, -0.7, 1.22), current_action="Waiting for state"),
        "perception": perception_state(),
        "pipeline": [pipeline_node(node_id, "—", ["waiting", "—"], "idle") for node_id, _ in PIPELINE_NODES],
        "events": [],
        "summary": None,
        "workcell": workcell_doc
        or workcell(
            {"x0": -3.0, "x1": 3.0, "y0": -0.75, "y1": 0.75, "top": 0.9},
            [],
            [camera("overview", "general", "GENERAL", "1920×1080"), camera("robot", "room_aisle", "AISLE", "1280×720"), camera("wrist", "wrist", "WRIST", "1280×720")],
        ),
        "evaluator": None,
    }


def snapshot(state: dict, timestamp: float | None = None) -> dict:
    """Wrap a full state as a ``snapshot`` message."""
    msg: dict[str, Any] = {"type": "snapshot", "state": state}
    if timestamp is not None:
        msg["timestamp"] = timestamp
    return msg


def state_update(patch: dict, timestamp: float | None = None) -> dict:
    """Wrap a deep-partial state as a ``state_update`` message."""
    msg: dict[str, Any] = {"type": "state_update", "patch": patch}
    if timestamp is not None:
        msg["timestamp"] = timestamp
    return msg
