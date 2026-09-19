"""The simulation loop, and the router that decides where actions come from.

One thread owns `MjModel`, `MjData` and every `mujoco.Renderer`. That is not
tidiness, it is required: a Renderer's GL context is bound to the thread that
created it, and rendering from a web server's request pool silently yields black
frames. The server only ever reads the latest bytes this thread published.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass, field
from queue import Empty, Queue
from typing import Any, Iterator

import cv2
import mujoco
import numpy as np

from armlab import policies, skills
from armlab.embodiment import ALOHA_BIMANUAL, BoundEmbodiment
from armlab.scene import DEFAULT_SCENE, Scene

STREAM_SIZE = (640, 480)
STREAM_FPS = 15.0


@dataclass
class Step:
    """One entry of a plan. Either a scripted skill or a stretch of policy control."""

    skill: str
    args: dict = field(default_factory=dict)
    status: str = 'pending'          # pending | active | done | failed
    detail: str = ''

    def describe(self) -> str:
        if self.skill == 'policy':
            return f"policy {self.args.get('policy', 'current')}"
        arg = self.args.get('sample_id') or self.args.get('target_id') or ''
        return f'{self.skill} {arg}'.strip()

    def as_dict(self) -> dict:
        return {'skill': self.skill, 'args': self.args, 'status': self.status,
                'detail': self.detail, 'label': self.describe()}


class Runtime:
    def __init__(self, scene_path=DEFAULT_SCENE, policy_name: str | None = None,
                 realtime: bool = True):
        self.scene = Scene(scene_path)
        self.binding = BoundEmbodiment(ALOHA_BIMANUAL, self.scene.model)
        self.binding_cameras = {
            mujoco.mj_id2name(self.scene.model, mujoco.mjtObj.mjOBJ_CAMERA, i)
            for i in range(self.scene.model.ncam)}
        self.control_hz = 50.0
        self.ctx = skills.SkillContext(self.scene, self.binding, self.control_hz)
        self.realtime = realtime

        self._commands: Queue[dict] = Queue()
        self._lock = threading.RLock()
        self._renderers: dict[tuple[int, int], mujoco.Renderer] = {}
        self._frames: dict[str, bytes] = {}
        self._events: deque[dict] = deque(maxlen=200)
        self._plan: list[Step] = []
        self._cursor = 0
        self._actions: Iterator[np.ndarray] | None = None
        self._policy: policies.LeRobotPolicy | None = None
        self._policy_status = {'state': 'none'}
        self._prompt: str | None = None
        self._plan_note: dict = {}
        self._mode = 'idle'
        self._policy_until = 0.0
        self._stop = threading.Event()
        self._steps_done = 0
        self._speed = 1.0
        if policy_name:
            self.submit({'type': 'set_policy', 'name': policy_name})

    # -- public, thread safe -----------------------------------------------
    def submit(self, command: dict) -> None:
        self._commands.put(command)

    def prompt(self, text: str) -> None:
        """Plan `text` and queue the result.

        Planning happens on its own thread: the Claude backend makes a network
        call, and neither the sim loop nor the web server's event loop should
        block on it.
        """
        def work() -> None:
            from armlab import planner
            parsed = planner.plan(text, self.scene.inventory())
            with self._lock:
                self._plan_note = {'prompt': text, 'reason': parsed.reason,
                                   'source': parsed.source}
            self.event(f'[{parsed.source}] {text!r}: {parsed.reason or "plan ready"}',
                       'info' if parsed.steps else 'warn')
            self.submit({'type': 'plan', 'steps': parsed.steps, 'prompt': text})

        threading.Thread(target=work, daemon=True, name='armlab-planner').start()

    def event(self, message: str, level: str = 'info') -> None:
        with self._lock:
            self._events.append({'time': round(self.scene.data.time, 2),
                                 'message': message, 'level': level})

    def frame(self, camera: str) -> bytes | None:
        with self._lock:
            return self._frames.get(camera)

    def telemetry(self) -> dict:
        with self._lock:
            state = self.binding.state(self.scene.data)
            return {
                'time': round(self.scene.data.time, 2),
                'mode': self._mode,
                'speed': round(self._speed, 2),
                'state': np.round(state, 4).tolist(),
                'command': np.round(self.ctx.command, 4).tolist(),
                'actuators': list(self.binding.spec.actuators),
                'plan': [s.as_dict() for s in self._plan],
                'planner': self._plan_note,
                'policy': self._policy_status,
                'events': list(self._events)[-40:],
                'inventory': self.scene.inventory(),
                'cameras': sorted(self.binding_cameras),
            }

    @property
    def running(self) -> bool:
        return not self._stop.is_set()

    def stop(self) -> None:
        self._stop.set()

    # -- the loop ----------------------------------------------------------
    def run(self) -> None:
        timestep = self.scene.model.opt.timestep
        decimation = max(1, round(1.0 / (self.control_hz * timestep)))
        next_render = 0.0
        started, sim_start = time.perf_counter(), self.scene.data.time
        self.event(f'scene {self.scene.path.name} loaded, {self.binding.dim} actuators')

        while not self._stop.is_set():
            self._drain_commands()
            if self._steps_done % decimation == 0:
                self._control()
            mujoco.mj_step(self.scene.model, self.scene.data)
            self._steps_done += 1

            if self.scene.data.time >= next_render:
                self._publish_frames()
                next_render = self.scene.data.time + 1.0 / STREAM_FPS

            elapsed = time.perf_counter() - started
            simulated = self.scene.data.time - sim_start
            self._speed = simulated / elapsed if elapsed > 0 else 1.0
            if self.realtime and simulated > elapsed:
                time.sleep(min(simulated - elapsed, 0.02))
        self._close_renderers()

    # -- commands ----------------------------------------------------------
    def _drain_commands(self) -> None:
        while True:
            try:
                command = self._commands.get_nowait()
            except Empty:
                return
            kind = command.get('type')
            if kind == 'plan':
                self._start_plan([Step(**s) for s in command['steps']],
                                 command.get('prompt'))
            elif kind == 'set_policy':
                self._load_policy(command['name'])
            elif kind == 'reset':
                self._reset()
            elif kind == 'stop':
                self._abort('stopped by operator')

    def _reset(self) -> None:
        with self._lock:
            self.scene.reset()
            self.ctx.command = self.binding.home()
            self._plan, self._cursor, self._actions = [], 0, None
            self._mode = 'idle'
        if self._policy:
            self._policy.reset()
        self.event('scene reset')

    def _abort(self, reason: str) -> None:
        with self._lock:
            for step in self._plan[self._cursor:]:
                if step.status in ('pending', 'active'):
                    step.status, step.detail = 'failed', reason
            self._actions, self._mode = None, 'idle'
        self.event(reason, 'warn')

    def _start_plan(self, steps: list[Step], prompt: str | None) -> None:
        with self._lock:
            self._plan, self._cursor, self._actions = steps, 0, None
            self._prompt = prompt
            self._mode = 'idle'
        self.event(f'plan: {" -> ".join(s.describe() for s in steps) or "(empty)"}')

    def _load_policy(self, name: str) -> None:
        """Load a checkpoint off the loop so physics keeps stepping while it downloads."""
        with self._lock:
            self._policy_status = {'state': 'loading', 'name': name}
        self.event(f'loading policy {name}')

        def work() -> None:
            try:
                policy = policies.load(name, self.binding, self._render,
                                       lambda: self.binding.state(self.scene.data),
                                       self.binding_cameras)
            except Exception as exc:  # a bad repo id must not take the sim down
                with self._lock:
                    self._policy_status = {'state': 'error', 'name': name, 'error': str(exc)}
                self.event(f'policy {name} rejected: {exc}', 'error')
                return
            with self._lock:
                self._policy = policy
                self.control_hz = policy.spec.control_hz
                self.ctx.control_hz = policy.spec.control_hz
                self._policy_status = {'state': 'loaded', **policy.info()}
            policy.reset()
            self.event(f'policy {policy.spec.display} ready '
                       f'({policy.info()["type"]}, {policy.info()["action_dim"]}-dim)')

        threading.Thread(target=work, daemon=True, name='policy-load').start()

    # -- control -----------------------------------------------------------
    def _control(self) -> None:
        with self._lock:
            if self._mode == 'policy':
                self._policy_tick()
            elif self._actions is not None:
                self._scripted_tick()
            elif self._cursor < len(self._plan):
                self._begin_step()
            self.binding.apply(self.scene.data, self.ctx.command)

    def _begin_step(self) -> None:
        step = self._plan[self._cursor]
        step.status = 'active'
        if step.skill == 'policy':
            if self._policy is None:
                step.status, step.detail = 'failed', 'no policy loaded'
                self._cursor += 1
                return
            self._mode = 'policy'
            self._policy.reset()
            self._policy_until = self.scene.data.time + float(step.args.get('seconds', 20))
            return
        skill = skills.SKILLS.get(step.skill)
        if skill is None:
            step.status, step.detail = 'failed', f'unknown skill {step.skill!r}'
            self._cursor += 1
            return
        try:
            self._actions = skill(self.ctx, **step.args)
        except skills.SkillError as exc:
            step.status, step.detail = 'failed', str(exc)
            self.event(f'{step.describe()}: {exc}', 'error')
            self._cursor += 1

    def _scripted_tick(self) -> None:
        step = self._plan[self._cursor]
        try:
            self.ctx.command = next(self._actions)
            return
        except StopIteration:
            step.status = 'done'
            self.event(f'{step.describe()} done', 'ok')
        except skills.SkillError as exc:
            step.status, step.detail = 'failed', str(exc)
            self.event(f'{step.describe()}: {exc}', 'error')
        self._actions = None
        self._cursor += 1

    def _policy_tick(self) -> None:
        step = self._plan[self._cursor] if self._cursor < len(self._plan) else None
        if step is not None and self.scene.data.time >= self._policy_until:
            step.status = 'done'
            self._mode = 'idle'
            self._cursor += 1
            self.event(f'{step.describe()} done', 'ok')
            return
        try:
            self.ctx.command = self._policy.act(self._prompt)
            self._policy_status['latency_ms'] = round(self._policy.latency_ms, 1)
        except Exception as exc:
            self._mode = 'idle'
            if step is not None:
                step.status, step.detail = 'failed', str(exc)
                self._cursor += 1
            self.event(f'policy inference failed: {exc}', 'error')

    def run_policy(self, seconds: float) -> None:
        """Hand control to the loaded policy for a while. Used by --headless."""
        self.submit({'type': 'plan', 'steps': [{'skill': 'policy',
                                                'args': {'seconds': seconds}}]})

    # -- rendering (sim thread only) ---------------------------------------
    def _render(self, camera: str, width: int, height: int) -> np.ndarray:
        key = (int(width), int(height))
        renderer = self._renderers.get(key)
        if renderer is None:
            renderer = mujoco.Renderer(self.scene.model, height=key[1], width=key[0])
            self._renderers[key] = renderer
        renderer.update_scene(self.scene.data, camera=camera)
        return renderer.render()

    def _publish_frames(self) -> None:
        width, height = STREAM_SIZE
        for camera in ('top', 'l/wrist_cam_left', 'general'):
            if camera not in self.binding_cameras:
                continue
            frame = self._render(camera, width, height)
            ok, buffer = cv2.imencode('.jpg', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR),
                                      [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if ok:
                with self._lock:
                    self._frames[camera] = buffer.tobytes()

    def _close_renderers(self) -> None:
        for renderer in self._renderers.values():
            try:
                renderer.close()
            except Exception:
                pass
        self._renderers.clear()


def spawn(**kwargs: Any) -> tuple[Runtime, threading.Thread]:
    runtime = Runtime(**kwargs)
    thread = threading.Thread(target=runtime.run, daemon=True, name='armlab-sim')
    thread.start()
    return runtime, thread
