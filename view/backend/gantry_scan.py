"""Scan YOLO proposals with the gantry's downward-facing hand camera.

Only perception tracks choose targets. MuJoCo contacts validate clearance;
sample identities come exclusively from the shared marker reader.
"""
import json
import math
import time

import mujoco
import numpy as np

import vision_pick as vp
from gantry_motion import JOINTS, SITE, move_to

# How high the hand camera stands while it reads a label, tried in this order.
# The camera is bolted to the lift at a fixed 45 degrees, so the gantry cannot
# turn it: the only thing it can change about a view is how close it comes, and
# coming closer is the whole of its aim. The first height clears everything on
# the bench, and each one after it is a descent worth making only because the
# ring did not read from the one above --- a marker 55 cm away spans half the
# pixels it spans at 27, and that is the difference between a read and a miss.
LOOK_HEIGHTS = (1.34, 1.24, 1.15)


def machine_contacts(model, data):
    """Contacts involving the moving machine, excluding its own hand internals."""
    def machine(geom):
        body = model.geom_bodyid[geom]
        while body:
            if model.body(body).name == 'gantry_bridge':
                return True
            body = model.body_parentid[body]
        return False
    return [(model.geom(c.geom1).name, model.geom(c.geom2).name)
            for c in data.contact if c.dist < -0.001
            and machine(c.geom1) != machine(c.geom2)]


def path(model, data, target):
    """Raise, translate, then lower; validate every 1 cm before starting."""
    mujoco.mj_forward(model, data)
    scratch = mujoco.MjData(model)
    mujoco.mj_copyData(scratch, model, data)
    start = data.site(SITE).xpos.copy()
    # The Z=0 position is the raised position, derived from the model.
    high = start[2] - data.qpos[model.joint('gantry_z').qposadr[0]]
    points = [start.copy(), np.array([*start[:2], high]),
              np.array([*target[:2], high]), np.asarray(target).copy()]
    for first, last in zip(points, points[1:]):
        for alpha in np.linspace(0, 1, max(2, math.ceil(np.linalg.norm(last-first)/.01)+1)):
            move_to(model, scratch, first + alpha * (last-first))
            contacts = machine_contacts(model, scratch)
            if contacts:
                raise ValueError(f'Gantry path blocked by {contacts[0]}')
    return points


def controller(model, data, world, perception, bench_map_to):
    """Servo Cartesian viewpoints and request actual marker reads at each stop."""
    indices = np.array([model.joint(n).qposadr[0] for n in JOINTS])
    actuators = np.array([model.actuator(n).id for n in JOINTS])
    scratch = mujoco.MjData(model)
    dt = model.opt.timestep
    began = float(data.time)

    def hold(seconds, caption):
        for _ in range(max(1, math.ceil(seconds/dt))):
            mujoco.mj_step(model, data)
            yield caption

    def drive(target, caption):
        points = path(model, data, target)
        for point in points[1:]:
            mujoco.mj_copyData(scratch, model, data)
            move_to(model, scratch, point)
            initial, goal = data.ctrl[actuators].copy(), scratch.qpos[indices].copy()
            seconds = max(.3, float(np.max(np.abs(goal-initial)/np.array([.45,.3,.18]))) * 1.6)
            steps = math.ceil(seconds/dt)
            for step in range(steps):
                alpha = .5-.5*math.cos(math.pi*(step+1)/steps)
                data.ctrl[actuators] = initial + alpha*(goal-initial)
                mujoco.mj_step(model, data)
                if machine_contacts(model, data):
                    data.ctrl[actuators] = data.qpos[indices]
                    raise RuntimeError('Gantry stopped: unexpected contact on planned path')
                yield caption
            yield from hold(.25, caption)
        if np.linalg.norm(data.site(SITE).xpos-target) > .01:
            raise RuntimeError('Gantry did not settle within 10 mm of the requested view')

    yield from hold(.5, 'Gantry: settling')
    # Park at an end so the carriage does not mask the first survey.
    mujoco.mj_forward(model, data)
    park = data.site(SITE).xpos.copy()
    park[0] = 1.35
    try:
        yield from drive(park, 'Gantry: clearing the survey camera')
    except ValueError as exc:
        world.log(data.time, str(exc))
    since = world.cycles
    while world.cycles < since + vp.CONFIRM_HITS:
        yield from hold(.1, 'Gantry: surveying the bench')
    attempted = []
    quiet = False
    while True:
        todo = [t for t in world.snapshot() if t.state == 'proposed'
                and not any(math.dist(t.seen_xy, xy) < .025 for xy in attempted)]
        if not todo:
            if quiet:
                break
            quiet = True
            since = world.cycles
            while world.cycles < since + vp.CONFIRM_HITS:
                yield from hold(.1, 'Gantry: final survey')
            continue
        quiet = False
        track = min(todo, key=lambda t: math.dist(t.seen_xy, data.site(SITE).xpos[:2]))
        attempted.append(track.seen_xy)
        target = np.array([*track.seen_xy, vp.rk.BENCH_TOP + vp.LOOK_ABOVE_BENCH])
        # The fixed 45-degree view sees the lateral marker ring. The lens hangs
        # below and ahead of the cage, so the hand remains above the vessels.
        mujoco.mj_forward(model, data)
        camera_id = model.camera('arm_eih').id
        offset = data.cam_xpos[camera_id] - data.site(SITE).xpos
        direction = -data.cam_xmat[camera_id].reshape(3, 3)[:, 2]
        result, rings, refused, looks = None, [], [], 0
        for rung, height in enumerate(LOOK_HEIGHTS):
            # Where the lens has to be for the target to sit on the fixed ray,
            # and where the pinch site goes to put it there.
            distance = (target[2] - height) / direction[2]
            point = target - distance * direction - offset
            try:
                yield from drive(point, f'Gantry: looking at track {track.id} '
                                        f'from {distance * 100:.0f} cm')
            except ValueError as exc:
                refused.append(str(exc))
                continue
            looks += 1
            request = perception.read(target)
            deadline = time.monotonic() + 30
            while not request.done.is_set():
                if time.monotonic() > deadline:
                    raise RuntimeError('Gantry marker reader timed out after 30 seconds')
                yield from hold(.05, f'Gantry: reading track {track.id}')
            result, rings = request.result, rings + request.rings
            if result and result.sample_id:
                break
            if rung + 1 < len(LOOK_HEIGHTS):
                lower = (target[2] - LOOK_HEIGHTS[rung + 1]) / direction[2]
                world.log(data.time, f'track {track.id}: no ring from {distance * 100:.0f} cm, '
                                     f'coming down to {lower * 100:.0f} cm')
        if not looks:
            with world.lock:
                track.state, track.note = 'unreachable', refused[0] if refused else 'no view'
            world.log(data.time, f'track {track.id}: {track.note}')
            continue
        with world.lock:
            track.confirmation = result
            track.state = 'named' if result and result.sample_id else 'empty'
            track.note = (f'ring read, {result.votes} markers' if result and result.sample_id
                          else f'no marker from {looks} descents')
        if track.sample:
            world.named(track, data.time)
        world.sighted(rings, data.time, track)
        world.log(data.time, f'track {track.id}: {track.sample or track.note}')
    # Return to the raised pose at the current XY, then preserve the scan report.
    home = data.site(SITE).xpos.copy()
    home[2] -= data.qpos[model.joint('gantry_z').qposadr[0]]
    yield from drive(home, 'Gantry: raising the hand')
    world.scan = vp.bench_map(world, began, float(data.time))
    if bench_map_to:
        bench_map_to.parent.mkdir(parents=True, exist_ok=True)
        bench_map_to.write_text(json.dumps(world.scan, indent=1)+'\n')
    world.log(data.time, 'Gantry scan complete')
    while True:
        yield from hold(.1, 'Gantry scan complete; manipulation is not configured')
