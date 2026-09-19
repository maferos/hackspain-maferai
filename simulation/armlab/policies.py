"""The swap seam: turn a Hugging Face checkpoint into a source of actions.

Nothing here branches on policy class. A lerobot checkpoint describes itself --
`config.json` names its type, and `input_features` / `output_features` declare
exactly which observations it wants and what shape it returns. So the adapter
reads that description and builds the observation dict to match, which is what
makes ACT -> Diffusion -> SmolVLA a config change rather than a code change.

One consequence worth knowing: if a checkpoint declares a LANGUAGE input (SmolVLA,
pi0, ...), the user's prompt is handed to it verbatim. With ACT loaded the prompt
can only *select* a behaviour; with a VLA loaded the prompt *is* an input.
"""

from __future__ import annotations

import subprocess
import sys
import time
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Protocol

import numpy as np

from armlab.embodiment import EMBODIMENTS, BoundEmbodiment

CATALOGUE = Path(__file__).resolve().parent / 'config' / 'policies.toml'
#: Checkpoints predating lerobot's processor format are rewritten here rather
#: than in the shared HF cache, which we must not mutate.
MIGRATED = Path.home() / '.cache' / 'armlab' / 'policies'

#: (camera name, width, height) -> HxWx3 uint8. Owned by the runtime, because the
#: GL context is bound to the thread that created it.
Renderer = Callable[[str, int, int], np.ndarray]
#: () -> the current proprioceptive vector.
StateReader = Callable[[], np.ndarray]


@dataclass(frozen=True)
class PolicySpec:
    key: str
    repo_id: str
    embodiment: str = 'ur10e_rail'
    cameras: dict[str, str] = field(default_factory=dict)
    control_hz: float = 50.0
    label: str = ''

    @property
    def display(self) -> str:
        return self.label or self.key


def catalogue() -> dict[str, PolicySpec]:
    raw = tomllib.loads(CATALOGUE.read_text())
    return {key: PolicySpec(key=key, **body) for key, body in raw.items()}


def resolve_spec(name: str) -> PolicySpec:
    """Look `name` up in the catalogue, or treat it as a bare HF repo id.

    Typing an unlisted repo id into the console is meant to work: we fall back to
    catalogue defaults and let the shape check at load time say whether the model
    actually fits the robot.
    """
    known = catalogue()
    if name in known:
        return known[name]
    return PolicySpec(key=name, repo_id=name, label=name)


class Policy(Protocol):
    """Anything the runtime can pull actions from."""

    def reset(self) -> None: ...
    def act(self, prompt: str | None) -> np.ndarray: ...
    def info(self) -> dict: ...


def resolve_checkpoint(repo_id: str) -> str:
    """Return a path/repo id whose processor pipelines can be loaded.

    lerobot >= 0.5 keeps normalisation in separate processor files rather than in
    the model. Checkpoints pushed before that -- including
    lerobot/act_aloha_sim_transfer_cube_human -- have none, and loading them
    raises ProcessorMigrationError pointing at a migration script. Run it once
    into our own cache so that, from the console, an old checkpoint is
    indistinguishable from a new one.
    """
    from lerobot.configs.policies import PreTrainedConfig
    from lerobot.policies.factory import make_pre_post_processors
    from lerobot.processor.pipeline import ProcessorMigrationError

    if Path(repo_id).is_dir():
        return repo_id
    cached = MIGRATED / repo_id.replace('/', '__')
    if (cached / 'policy_preprocessor.json').exists():
        return str(cached)
    config = PreTrainedConfig.from_pretrained(repo_id)
    try:
        make_pre_post_processors(config, pretrained_path=repo_id)
        return repo_id
    except ProcessorMigrationError:
        cached.parent.mkdir(parents=True, exist_ok=True)
        done = subprocess.run(
            [sys.executable, '-m', 'lerobot.processor.migrate_policy_normalization',
             '--pretrained-path', repo_id, '--output-dir', str(cached)],
            capture_output=True, text=True)
        if done.returncode:
            # Without this the caller sees a bare CalledProcessError and no clue
            # which checkpoint failed or why.
            detail = (done.stderr or done.stdout or '').strip().splitlines()
            raise PolicyMismatch(
                f'{repo_id} predates lerobot\'s processor format and could not be '
                f'migrated: {detail[-1] if detail else "no output"}') from None
        return str(cached)


class LeRobotPolicy:
    """A lerobot checkpoint bound to a MuJoCo embodiment and camera set."""

    def __init__(self, spec: PolicySpec, binding: BoundEmbodiment, render: Renderer,
                 read_state: StateReader, scene_cameras: set[str]):
        import torch
        from lerobot.configs.policies import PreTrainedConfig
        from lerobot.configs.types import FeatureType
        from lerobot.policies.factory import get_policy_class, make_pre_post_processors

        self._torch = torch
        self._FeatureType = FeatureType
        self.spec = spec
        self.binding = binding
        self.render = render
        self.read_state = read_state
        self.latency_ms = 0.0

        path = resolve_checkpoint(spec.repo_id)
        self.config = PreTrainedConfig.from_pretrained(path)
        self.config.device = 'cpu'
        self.policy = get_policy_class(self.config.type).from_pretrained(path)
        self.policy.to('cpu').eval()
        self.pre, self.post = make_pre_post_processors(self.config, pretrained_path=path)

        action = self.config.output_features.get('action')
        if action is None:
            raise PolicyMismatch(f'{spec.repo_id} declares no action output')
        if action.shape[-1] != binding.dim:
            raise PolicyMismatch(
                f'{spec.repo_id} emits {action.shape[-1]}-dim actions but embodiment '
                f'{binding.spec.name!r} has {binding.dim} actuators -- wrong robot for '
                f'this checkpoint')
        self.cameras = self._map_cameras(scene_cameras)
        self.language_keys = [k for k, f in self.config.input_features.items()
                              if f.type is FeatureType.LANGUAGE]

    def _map_cameras(self, scene_cameras: set[str]) -> dict[str, str]:
        """Decide which MuJoCo camera feeds each visual feature.

        Explicit catalogue mapping wins; otherwise the trailing part of the
        feature key (`observation.images.top` -> `top`) is looked up as a logical
        camera on the embodiment and then as a raw camera name.
        """
        logical = self.binding.spec.cameras
        mapped = {}
        for key, feature in self.config.input_features.items():
            if feature.type is not self._FeatureType.VISUAL:
                continue
            wanted = self.spec.cameras.get(key, key.rsplit('.', 1)[-1])
            camera = logical.get(wanted, wanted)
            if camera not in scene_cameras:
                raise PolicyMismatch(
                    f'{self.spec.repo_id} wants image {key!r}; mapped it to camera '
                    f'{camera!r}, which this scene does not have. Add a `cameras` entry '
                    f'to config/policies.toml. Scene cameras: {sorted(scene_cameras)}')
            mapped[key] = camera
        return mapped

    def reset(self) -> None:
        self.policy.reset()

    def observe(self, prompt: str | None) -> dict:
        torch, FeatureType = self._torch, self._FeatureType
        batch: dict = {}
        for key, feature in self.config.input_features.items():
            if feature.type is FeatureType.VISUAL:
                channels, height, width = feature.shape
                frame = self.render(self.cameras[key], width, height)
                image = torch.from_numpy(np.ascontiguousarray(frame))
                batch[key] = image.permute(2, 0, 1)[:channels].float().div_(255.0)[None]
            elif feature.type is FeatureType.STATE:
                batch[key] = torch.from_numpy(self.read_state()).float()[None]
        for key in self.language_keys:
            batch[key] = [prompt or '']
        if self.language_keys:
            batch.setdefault('task', [prompt or ''])
        return batch

    def act(self, prompt: str | None = None) -> np.ndarray:
        started = time.perf_counter()
        with self._torch.no_grad():
            action = self.post(self.policy.select_action(self.pre(self.observe(prompt))))
        self.latency_ms = (time.perf_counter() - started) * 1000
        return np.asarray(action.squeeze(0).cpu().numpy(), dtype=float)

    def info(self) -> dict:
        features = {k: list(f.shape) for k, f in self.config.input_features.items()}
        return {
            'key': self.spec.key,
            'label': self.spec.display,
            'repo_id': self.spec.repo_id,
            'type': self.config.type,
            'action_dim': self.config.output_features['action'].shape[-1],
            'features': features,
            'cameras': self.cameras,
            'language': bool(self.language_keys),
            'chunk_size': getattr(self.config, 'chunk_size', None),
            'n_action_steps': getattr(self.config, 'n_action_steps', None),
            'control_hz': self.spec.control_hz,
            'latency_ms': round(self.latency_ms, 1),
        }


class PolicyMismatch(RuntimeError):
    """The checkpoint does not fit the robot. Raised before anything moves."""


def load(name: str, binding: BoundEmbodiment, render: Renderer, read_state: StateReader,
         scene_cameras: set[str]) -> LeRobotPolicy:
    spec = resolve_spec(name)
    if spec.embodiment not in EMBODIMENTS:
        raise PolicyMismatch(f'unknown embodiment {spec.embodiment!r}')
    if EMBODIMENTS[spec.embodiment].name != binding.spec.name:
        raise PolicyMismatch(
            f'{spec.repo_id} targets embodiment {spec.embodiment!r}, but the scene is '
            f'{binding.spec.name!r}')
    return LeRobotPolicy(spec, binding, render, read_state, scene_cameras)
