"""Scan YOLO proposals with the gantry's downward-facing hand camera.

Only perception tracks choose targets. MuJoCo contacts validate clearance;
sample identities come exclusively from the shared marker reader.
"""
import json
import math
import time

import mujoco
import numpy as np

import grasp_test as gt
import pipetting as pt
import vision_pick as vp
from gantry_motion import JOINTS, SITE, move_to

# Mixing. Nothing is grasped at a flask and nothing is drawn: the hand is
# planted over the vessel as though it were about to, waits, and leaves. That
# pause is the uncapping and the pipetting, and the only trace of it is the
# liquid, which comes off the flask's column and goes into the beaker's.
PLANT_SECONDS = 1.5         # the cage stands over the flask this long, doing nothing
POUR_SECONDS = 1.2          # and over the beaker this long while its column rises
POUR_STEPS = 12
POUR_ABOVE = 0.06           # how far over the beaker's mouth the hand stands to dose
# The camera and its drop bar hang below the hand, further down than the cage
# reaches. Planting the cage around a vessel the way the arm does --- 35 mm under
# its mouth --- puts the lens through the worktop, and the path check refuses the
# whole move: 'blocked by (minihannover_worktop, gantry_camera_drop)'. On this
# machine the hand therefore stands ON the vessel rather than around it, which is
# all the mimed pipetting needs, and never lower than the lens can go.
CAMERA_CLEAR = 0.02         # the lens keeps this much over the bench
# Where the finished mixture is set down: the right-hand end of the worktop,
# past the last flask and clear of all three balances.
DELIVERY = (1.15, -0.55)


def machine_contacts(model, data, allow=()):
    """Contacts involving the moving machine, excluding its own hand internals.

    Args:
        allow: Body names the machine is expected to touch. Handling a vessel
            means touching it, so the flask being stood over and the beaker
            being carried are not obstacles while they are the job.
    """
    def machine(geom):
        body = model.geom_bodyid[geom]
        while body:
            if model.body(body).name == 'gantry_bridge':
                return True
            body = model.body_parentid[body]
        return False

    def spared(geom):
        body = model.geom_bodyid[geom]
        while body:
            if model.body(body).name in allow:
                return True
            body = model.body_parentid[body]
        return False
    return [(model.geom(c.geom1).name, model.geom(c.geom2).name)
            for c in data.contact if c.dist < -0.001
            and machine(c.geom1) != machine(c.geom2)
            and not (spared(c.geom1) or spared(c.geom2))]


def path(model, data, target, allow=(), *, level=False):
    """Validate a raised transit or a constant-height scan leg every 1 cm.

    Args:
        allow: Body names the machine is expected to touch on the way.
        level: Hold the height instead of raising and lowering, for a scan leg.
    """
    mujoco.mj_forward(model, data)
    scratch = mujoco.MjData(model)
    mujoco.mj_copyData(scratch, model, data)
    start = data.site(SITE).xpos.copy()
    # The Z=0 position is the raised position, derived from the model.
    high = start[2] - data.qpos[model.joint('gantry_z').qposadr[0]]
    if level:
        if abs(start[2] - target[2]) > .01:
            raise ValueError('A level scan leg cannot change height')
        points = [start.copy(), np.asarray(target).copy()]
    else:
        points = [start.copy(), np.array([*start[:2], high]),
                  np.array([*target[:2], high]), np.asarray(target).copy()]
    for first, last in zip(points, points[1:]):
        for alpha in np.linspace(0, 1, max(2, math.ceil(np.linalg.norm(last-first)/.01)+1)):
            move_to(model, scratch, first + alpha * (last-first))
            contacts = machine_contacts(model, scratch, allow)
            if contacts:
                raise ValueError(f'Gantry path blocked by {contacts[0]}')
    return points


def controller(model, data, world, perception, bench_map_to):
    """Servo Cartesian viewpoints and request actual marker reads at each stop."""
    indices = np.array([model.joint(n).qposadr[0] for n in JOINTS])
    actuators = np.array([model.actuator(n).id for n in JOINTS])
    fingers = model.actuator('arm_grip_fingers_actuator').id
    vessels = pt.containers(model, data)
    scratch = mujoco.MjData(model)
    dt = model.opt.timestep
    began = float(data.time)

    def hold(seconds, caption):
        for _ in range(max(1, math.ceil(seconds/dt))):
            mujoco.mj_step(model, data)
            yield caption

    def drive(target, caption, allow=(), grip=None, *, level=False):
        points = path(model, data, target, allow, level=level)
        for point in points[1:]:
            mujoco.mj_copyData(scratch, model, data)
            move_to(model, scratch, point)
            initial, goal = data.ctrl[actuators].copy(), scratch.qpos[indices].copy()
            seconds = max(.3, float(np.max(np.abs(goal-initial)/np.array([.45,.3,.18]))) * 1.6)
            steps = math.ceil(seconds/dt)
            for step in range(steps):
                alpha = .5-.5*math.cos(math.pi*(step+1)/steps)
                data.ctrl[actuators] = initial + alpha*(goal-initial)
                if grip is not None:
                    data.ctrl[fingers] = grip
                mujoco.mj_step(model, data)
                if machine_contacts(model, data, allow):
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
    park[0] += model.joint('gantry_x').range[0] - data.qpos[indices[0]] + .1
    try:
        yield from drive(park, 'Gantry: clearing the survey camera')
    except ValueError as exc:
        world.log(data.time, str(exc))
    since = world.cycles
    while world.cycles < since + vp.CONFIRM_HITS:
        yield from hold(.1, 'Gantry: surveying the bench')
    general = vp.camera_at(model, data, 'general')
    heights = [vp.box_height(t, general) for t in world.snapshot()
               if t.state != 'lost' and t.bbox is not None]
    tallest = max(heights, default=vp.FLASK_HEIGHT)
    camera_height = vp.rk.BENCH_TOP + tallest + .12
    world.log(data.time, f'Left-to-right scan: tallest detected vessel {tallest*100:.1f} cm; '
                         f'constant lens height {camera_height:.3f} m (12 cm clearance)')
    attempted = []
    frontier = -math.inf
    at_scan_height = False
    quiet = False
    while True:
        todo = [t for t in world.snapshot() if t.state in ('proposed', 'named')
                and not t.wrist_only and t.seen_xy[0] >= frontier - .025
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
        track = min(todo, key=lambda t: (t.seen_xy[0], t.seen_xy[1]))
        frontier = track.seen_xy[0]
        attempted.append(track.seen_xy)
        target = np.array([*track.seen_xy, vp.rk.BENCH_TOP + vp.LOOK_ABOVE_BENCH])
        # The fixed 45-degree view sees the lateral marker ring. The lens hangs
        # below and ahead of the cage, so the hand remains above the vessels.
        mujoco.mj_forward(model, data)
        camera_id = model.camera('arm_eih').id
        offset = data.cam_xpos[camera_id] - data.site(SITE).xpos
        direction = -data.cam_xmat[camera_id].reshape(3, 3)[:, 2]
        distance = (target[2] - camera_height) / direction[2]
        eye = target - distance * direction
        point = eye - offset
        try:
            yield from drive(point, f'Gantry: looking at track {track.id}', level=at_scan_height)
            at_scan_height = True
        except ValueError as exc:
            with world.lock:
                track.state, track.note = 'unreachable', str(exc)
            world.log(data.time, f'track {track.id}: {exc}')
            continue
        request = perception.read(target)
        deadline = time.monotonic() + 30
        while not request.done.is_set():
            if time.monotonic() > deadline:
                raise RuntimeError('Gantry marker reader timed out after 30 seconds')
            yield from hold(.05, f'Gantry: reading track {track.id}')
        result = request.result
        with world.lock:
            if result and result.sample_id:
                track.confirmation = result
            track.state = 'named' if track.sample else 'empty'
            track.note = (f'ring read, {result.votes} markers' if result and result.sample_id
                          else 'No marker identified from this view')
        if track.sample:
            world.named(track, data.time)
        world.sighted(request.rings, data.time, track)
        world.log(data.time, f'track {track.id}: {track.sample or track.note}')
    # Return to the raised pose at the current XY, then preserve the scan report.
    home = data.site(SITE).xpos.copy()
    home[2] -= data.qpos[model.joint('gantry_z').qposadr[0]]
    yield from drive(home, 'Gantry: raising the hand')
    world.scan = vp.bench_map(world, began, float(data.time))
    world.scan['gantry'] = {'direction': 'left-to-right', 'camera_height_m': camera_height,
                            'tallest_detected_m': tallest, 'clearance_m': .12,
                            'visited_positions': attempted}
    if bench_map_to:
        bench_map_to.parent.mkdir(parents=True, exist_ok=True)
        bench_map_to.write_text(json.dumps(world.scan, indent=1)+'\n')
    world.log(data.time, 'Gantry scan complete')

    def camera_floor():
        """The lowest the pinch site may go before the lens reaches the bench."""
        mujoco.mj_forward(model, data)
        drop = data.site(SITE).xpos[2] - data.cam_xpos[model.camera('arm_eih').id][2]
        return vp.rk.BENCH_TOP + drop + CAMERA_CLEAR

    def plant(track, millilitres):
        """Stand the cage over one flask, mime the pipetting, take the dose.

        Nothing is grasped and nothing is lifted. The hand comes down until the
        cage is around the top of the vessel, waits, and goes back up: on the
        real tool that is where the cap comes off and the pipette goes in. The
        flask is left standing exactly where the scan found it.
        """
        sample = track.sample
        row = perception.rows.get(track.confirmation.marker_id) if track.confirmation else None
        height = vp.vessel_height(row['vessel_class']) if row else vp.FLASK_HEIGHT
        over = np.array([*track.xy, max(vp.rk.BENCH_TOP + vp.grasp_height(model, height),
                                        camera_floor())])
        body = f'dyn_{sample}'
        held = body if mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body) >= 0 else None
        drawn = min(millilitres, vessels[sample].volume) if sample in vessels else 0.0
        yield from drive(over, f'standing over {sample}', allow=(held,) if held else ())
        yield from hold(PLANT_SECONDS,
                        f'standing over {sample}: uncapping and drawing {drawn:.1f} ml')
        if drawn > 0:
            vessels[sample].volume -= drawn
            pt.sync(model, vessels)
            world.log(data.time, f'{sample}: {drawn:.1f} ml drawn, '
                                 f'{vessels[sample].volume:.1f} ml left in the flask')
        return drawn

    def dose(sample, millilitres):
        """Stand over the mixing beaker and let the pipette's load down into it."""
        if 'beaker' not in vessels or millilitres <= 0:
            return
        mouth = np.array(data.site(vessels['beaker'].mouth).xpos)
        yield from drive(mouth + (0, 0, POUR_ABOVE),
                         f'over the beaker with {sample}', allow=('beaker',))
        was = vessels['beaker'].volume
        for step in range(POUR_STEPS):
            vessels['beaker'].volume = was + millilitres * (step + 1) / POUR_STEPS
            pt.sync(model, vessels)
            yield from hold(POUR_SECONDS / POUR_STEPS,
                            f'dosing {millilitres:.1f} ml of {sample} into the beaker')
        world.log(data.time, f'{sample}: {millilitres:.1f} ml into the beaker, '
                             f'which now holds {vessels["beaker"].volume:.1f} ml')

    def deliver():
        """Take the finished mixture to the end of the bench.

        The one thing in the whole run that is really carried: the cage closes
        on the beaker, lifts it off the balance, crosses the bench and sets it
        down. Everything before this was mimed, so if the beaker does not come
        with the hand it is worth knowing, and the grip is checked rather than
        assumed.
        """
        if 'beaker' not in vessels:
            return
        mujoco.mj_forward(model, data)
        stood = data.body('beaker').xpos.copy()
        on = np.array([stood[0], stood[1],
                       max(stood[2] + vp.grasp_height(model, 0.10), camera_floor())])
        yield from drive(on, 'reaching down for the beaker', allow=('beaker',))
        for step in range(int(0.8 / dt)):
            data.ctrl[fingers] = gt.SHUT * min((step + 1) / (0.4 / dt), 1.0)
            mujoco.mj_step(model, data)
            yield 'closing on the beaker'
        shut = float(data.ctrl[fingers])
        lifted = on + (0, 0, 0.12)
        yield from drive(lifted, 'lifting the beaker', allow=('beaker',), grip=shut)
        if data.body('beaker').xpos[2] < stood[2] + 0.05:
            world.log(data.time, 'the beaker did not come with the hand; it stays on the balance')
            data.ctrl[fingers] = gt.OPEN
            return
        down = np.array([*DELIVERY, max(vp.rk.BENCH_TOP + vp.grasp_height(model, 0.10) + 0.01,
                                        camera_floor())])
        yield from drive(np.array([*DELIVERY, lifted[2]]),
                         'carrying the mixture to the end of the bench',
                         allow=('beaker',), grip=shut)
        yield from drive(down, 'setting the mixture down', allow=('beaker',), grip=shut)
        for _ in range(int(0.5 / dt)):
            data.ctrl[fingers] = gt.OPEN
            mujoco.mj_step(model, data)
            yield 'letting go of the mixture'
        yield from drive(down + (0, 0, 0.15), 'clear of the mixture')
        world.log(data.time, f'the mixture stands at the end of the bench, '
                             f'{vessels["beaker"].volume:.1f} ml')

    # The formula, one compound at a time, as the executor asks for them.
    by_id = {}
    while True:
        with world.lock:
            asked = [c for c in world.commands if c.get('cmd') in ('pick', 'deliver')]
            world.commands[:] = [c for c in world.commands if c not in asked]
        if not asked:
            yield from hold(.1, 'idle: the bench is scanned and waiting for a formula')
            continue
        by_id = {t.id: t for t in world.snapshot()}
        for command in asked:
            # A move the machine will not make is this compound's problem, not
            # the run's: it is reported and the next compound is tried. Letting
            # it out of the generator kills the controller, and then the bench
            # is left with no scan and no arm over one blocked approach.
            if command['cmd'] == 'deliver':
                try:
                    yield from deliver()
                except (ValueError, RuntimeError) as exc:
                    data.ctrl[fingers] = gt.OPEN
                    world.log(data.time, f'the mixture stays on the balance: {exc}')
                continue
            track = by_id.get(command.get('track'))
            if track is None or not track.sample:
                continue
            try:
                drawn = yield from plant(track, command.get('ml') or vp.DOSE_ML)
                yield from dose(track.sample, drawn)
            except (ValueError, RuntimeError) as exc:
                with world.lock:
                    track.note = str(exc)
                world.log(data.time, f'{track.sample}: {exc}')
            track.picks += 1
