"""Spawn lab workers that drop tubes into the spawn zones of a scene.

MuJoCo cannot add bodies to a compiled model, so the scene pre-allocates them
(see models/autobio_lab.xml) and this module only moves them around:

- sites named ``spawn_zone_<name>``: the circles on the table,
- mocap bodies named ``worker_<name>``: one stick figure per zone,
- free bodies named ``drop_tube_<i>``: the tube pool, reused round-robin.

Every ``interval`` seconds of simulation time a worker walks up to the end of the
table, drops a tube from its hand into its zone and walks away again.
"""
import math

import mujoco
import numpy as np

HIDDEN = np.array([0.0, 0.0, -10.0])
REACH = 0.62  # horizontal distance from a worker's feet to its hand (human_figure.xml)
HAND_HEIGHT = 1.08
WALK_DISTANCE = 2.5
WALK_IN, WAIT, WALK_OUT = 1.2, 0.8, 1.2  # seconds


def _names(model, objtype, count):
    return [(i, mujoco.mj_id2name(model, objtype, i) or "") for i in range(count)]


class Worker:
    def __init__(self, model, data, zone_site: int, body: int, table_center):
        self.mocap = model.body_mocapid[body]
        zone = data.site_xpos[zone_site].copy()
        outward = zone[:2] - table_center[:2]
        outward /= np.linalg.norm(outward)
        self.zone = zone
        self.stand = np.array([*(zone[:2] + outward * REACH), 0.0])
        self.away = np.array([*(zone[:2] + outward * (REACH + WALK_DISTANCE)), 0.0])
        yaw = math.atan2(-outward[1], -outward[0])  # face the table
        self.quat = np.array([math.cos(yaw / 2), 0, 0, math.sin(yaw / 2)])
        self.start = None
        self.dropped = False

    @property
    def busy(self) -> bool:
        return self.start is not None

    def begin(self, t: float) -> None:
        self.start, self.dropped = t, False

    def update(self, data, t: float) -> bool:
        """Move the figure; return True at the moment the tube should drop."""
        if self.start is None:
            data.mocap_pos[self.mocap] = HIDDEN
            return False
        s = t - self.start
        if s < WALK_IN:
            pos = self.away + (self.stand - self.away) * (s / WALK_IN)
        elif s < WALK_IN + WAIT:
            pos = self.stand
        elif s < WALK_IN + WAIT + WALK_OUT:
            pos = self.stand + (self.away - self.stand) * ((s - WALK_IN - WAIT) / WALK_OUT)
        else:
            self.start = None
            data.mocap_pos[self.mocap] = HIDDEN
            return False
        walking = s < WALK_IN or s >= WALK_IN + WAIT
        bob = 0.025 * abs(math.sin(s * 2 * math.pi)) if walking else 0.0
        data.mocap_pos[self.mocap] = pos + [0, 0, bob]
        data.mocap_quat[self.mocap] = self.quat
        if not self.dropped and s >= WALK_IN:
            self.dropped = True
            return True
        return False


class Spawner:
    def __init__(self, model, data, interval: float = 3.0, seed: int | None = None):
        self.model, self.data, self.interval = model, data, interval
        self.rng = np.random.default_rng(seed)
        mujoco.mj_forward(model, data)
        center = data.xpos[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "table")]
        self.workers = []
        for site, name in _names(model, mujoco.mjtObj.mjOBJ_SITE, model.nsite):
            if name.startswith("spawn_zone_"):
                body = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "worker_" + name[len("spawn_zone_"):])
                if body < 0 or model.body_mocapid[body] < 0:
                    raise ValueError(f"{name} has no mocap body worker_{name[len('spawn_zone_'):]}")
                self.workers.append(Worker(model, data, site, body, center))
        # The pool bodies themselves, not the tube bodies attached under them.
        pool = [
            b for b, name in _names(model, mujoco.mjtObj.mjOBJ_BODY, model.nbody)
            if name.startswith("drop_tube_") and model.body_jntnum[b] == 1
        ]
        self.tubes = [model.jnt_qposadr[model.body_jntadr[b]] for b in pool]
        self.tube_dofs = [model.jnt_dofadr[model.body_jntadr[b]] for b in pool]
        self.next_tube = 0
        self.next_worker = 0
        self.next_spawn = 0.5
        self.spawned = 0

    @staticmethod
    def applies_to(model) -> bool:
        return any(name.startswith("spawn_zone_") for _, name in _names(model, mujoco.mjtObj.mjOBJ_SITE, model.nsite))

    def _drop(self, zone) -> None:
        qadr, dadr = self.tubes[self.next_tube], self.tube_dofs[self.next_tube]
        self.next_tube = (self.next_tube + 1) % len(self.tubes)
        r, a = 0.08 * math.sqrt(self.rng.random()), self.rng.uniform(0, 2 * math.pi)
        pos = zone[:2] + r * np.array([math.cos(a), math.sin(a)])
        quat = np.zeros(4)
        tilt = self.rng.normal(0, 0.15, 3) * [1, 1, 0] + [0, 0, self.rng.uniform(-math.pi, math.pi)]
        mujoco.mju_euler2Quat(quat, tilt, "xyz")
        # The tube's origin is its bottom; hang it just under the hand.
        self.data.qpos[qadr:qadr + 7] = [*pos, HAND_HEIGHT - 0.13, *quat]
        self.data.qvel[dadr:dadr + 6] = 0

    def step(self) -> None:
        """Call once after every mj_step."""
        t = self.data.time
        if self.workers and t >= self.next_spawn:
            for k in range(len(self.workers)):
                worker = self.workers[(self.next_worker + k) % len(self.workers)]
                if not worker.busy:
                    worker.begin(t)
                    self.next_worker = (self.next_worker + k + 1) % len(self.workers)
                    self.next_spawn = t + self.interval
                    break
        for worker in self.workers:
            if worker.update(self.data, t) and self.tubes:
                self._drop(worker.zone)
                self.spawned += 1
