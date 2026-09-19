#!/usr/bin/env python3
"""Liquid in the scene, and the rules for moving it with the pipette.

The liquid is a level and a number, not a fluid: MuJoCo has no fluid solver and
hundreds of spheres per flask would be slow, unstable and ugly at this scale.
Each container carries a cylinder geom whose height is its contents, and this
module keeps the two in step.

What is *not* faked is whether the pipette may draw or deliver. Aspirating
needs the tip inside the bore and under the surface; dispensing needs it inside
the bore. Both are checked against the running simulation, so a bad approach
fails here the way it would on a bench --- which is the point of simulating it
at all.
"""
from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import numpy as np

SIM = Path(__file__).resolve().parents[1]

DENSITY = 0.91          # g/ml, a typical fragrance oil
TIP_CAPACITY = 1.0      # ml the pipette can hold
SUBMERGE = 0.002        # how far under the surface the tip must be to draw


@dataclass
class Container:
    """A vessel with a liquid level the simulation can show.

    Attributes:
        name: Sample id, or ``beaker``.
        body: Body name in the compiled scene.
        liquid: Name of the geom that stands for its contents.
        mouth: Name of the site at its opening.
        inner_radius: Radius of the liquid column, in metres.
        floor: Height of the inside of the base, in the body's frame.
        bore_radius: Radius of the opening, in metres.
        volume: Current contents in millilitres.
    """

    name: str
    body: str
    liquid: str
    mouth: str
    inner_radius: float
    floor: float
    bore_radius: float
    volume: float = 0.0

    @property
    def mass(self) -> float:
        """Contents in grams."""
        return self.volume * DENSITY

    def height(self) -> float:
        """Height of the liquid column, in metres."""
        return self.volume * 1e-6 / (np.pi * self.inner_radius**2)


@dataclass
class Pipette:
    """What the tool is holding."""

    volume: float = 0.0
    events: list[str] = field(default_factory=list)


def containers(model: mujoco.MjModel, data: mujoco.MjData,
               volumes: dict[str, float] | None = None) -> dict[str, Container]:
    """Find every container in the scene and read its geometry off the model.

    The dimensions come from the compiled scene rather than from the generator
    that wrote it, so this cannot drift out of step with what is actually
    loaded.

    Args:
        model: Compiled scene.
        data: Forward-evaluated data.
        volumes: Starting contents in millilitres, keyed by name. When omitted,
            the levels already built into the scene are read back.

    Returns:
        One Container per vessel and the beaker, by name.
    """
    out = {}
    for i in range(model.ngeom):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i) or ''
        if not name.endswith('_liquid') or name.startswith('arm_'):
            continue
        prefix = name[:-len('_liquid')]
        label = prefix.removeprefix('dyn_')
        inner = float(model.geom_size[i][0])
        half = float(model.geom_size[i][1])
        centre = float(model.geom_pos[i][2])
        site = model.site(f'{prefix}_mouth')
        out[label] = Container(
            name=label, body=prefix, liquid=name, mouth=f'{prefix}_mouth',
            inner_radius=inner, floor=centre - half,
            bore_radius=float(model.site_size[site.id][0]),
            volume=np.pi * inner**2 * (2 * half) * 1e6)
    if volumes:
        for label, millilitres in volumes.items():
            if label in out:
                out[label].volume = millilitres
    return out


def sync(model: mujoco.MjModel, vessels: dict[str, Container],
         pipette: Pipette | None = None) -> None:
    """Resize every liquid column to match its container's contents.

    Args:
        model: Compiled scene; its geom sizes are written.
        vessels: The containers to show.
        pipette: What the tool holds, drawn in the tip when given.
    """
    for vessel in vessels.values():
        i = model.geom(vessel.liquid).id
        half = max(vessel.height() / 2, 1e-5)
        model.geom_size[i][1] = half
        model.geom_pos[i][2] = vessel.floor + half
    if pipette is not None:
        i = model.geom('arm_pip_pip_liquid_0').id
        # Shown as a stub in the tip; its length is the fraction held, not a
        # true volume, because the tip is a cone and this is a readout.
        model.geom_size[i][1] = max(0.012 * pipette.volume / TIP_CAPACITY, 1e-5)


def tip_radius(model: mujoco.MjModel) -> float:
    """The widest part of the tip, which is what has to pass a bore.

    Measured off the compiled model so it cannot drift from the generator.

    Args:
        model: Compiled scene.

    Returns:
        Radius in metres.
    """
    return max(float(model.geom_size[i][0]) for i in range(model.ngeom)
               if (mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i) or '')
               .startswith('arm_pip_pip_tip_'))


def tip_pose(model: mujoco.MjModel, data: mujoco.MjData) -> np.ndarray:
    """World position of the pipette tip."""
    return data.site('arm_pip_tip').xpos.copy()


def entry(model: mujoco.MjModel, data: mujoco.MjData,
          vessel: Container) -> tuple[float, float]:
    """How well the tip is lined up with a container's mouth.

    Args:
        model: Compiled scene.
        data: Forward-evaluated data.
        vessel: The container being approached.

    Returns:
        Horizontal miss from the container's axis, and the tip's height above
        the liquid surface --- negative once it is submerged. Both in metres.
    """
    tip = tip_pose(model, data)
    axis = data.body(vessel.body).xpos
    miss = float(np.hypot(tip[0] - axis[0], tip[1] - axis[1]))
    surface = float(axis[2]) + vessel.floor + vessel.height()
    return miss, float(tip[2]) - surface


def inside(model: mujoco.MjModel, data: mujoco.MjData,
           vessel: Container) -> bool:
    """Whether the tip is down the bore rather than outside or above it."""
    miss, _ = entry(model, data, vessel)
    tip = tip_pose(model, data)
    rim = float(data.site(vessel.mouth).xpos[2])
    return miss + tip_radius(model) < vessel.bore_radius and tip[2] < rim


def aspirate(model: mujoco.MjModel, data: mujoco.MjData, vessel: Container,
             pipette: Pipette, millilitres: float) -> bool:
    """Draw liquid, if the tip is actually in it.

    Args:
        model: Compiled scene.
        data: Forward-evaluated data.
        vessel: Container to draw from.
        pipette: The tool's state, updated on success.
        millilitres: How much to try to draw.

    Returns:
        True when liquid moved.
    """
    miss, depth = entry(model, data, vessel)
    if not inside(model, data, vessel):
        pipette.events.append(
            f'{vessel.name}: tip not in the bore, {miss * 1000:.1f} mm off axis')
        return False
    if depth > -SUBMERGE:
        pipette.events.append(
            f'{vessel.name}: tip {depth * 1000:+.1f} mm from the surface, too high')
        return False
    drawn = min(millilitres, vessel.volume, TIP_CAPACITY - pipette.volume)
    if drawn <= 0:
        pipette.events.append(f'{vessel.name}: nothing to draw')
        return False
    vessel.volume -= drawn
    pipette.volume += drawn
    pipette.events.append(f'{vessel.name}: drew {drawn:.2f} ml')
    sync(model, {vessel.name: vessel}, pipette)
    return True


def dispense(model: mujoco.MjModel, data: mujoco.MjData, vessel: Container,
             pipette: Pipette, millilitres: float | None = None) -> bool:
    """Deliver into a container, if the tip is over its opening.

    Args:
        model: Compiled scene.
        data: Forward-evaluated data.
        vessel: Container to deliver into.
        pipette: The tool's state, updated on success.
        millilitres: How much to deliver; everything held when omitted.

    Returns:
        True when liquid moved.
    """
    if not inside(model, data, vessel):
        miss, _ = entry(model, data, vessel)
        pipette.events.append(
            f'{vessel.name}: not over the mouth, {miss * 1000:.1f} mm off axis')
        return False
    given = min(pipette.volume if millilitres is None else millilitres,
                pipette.volume)
    if given <= 0:
        pipette.events.append('pipette is empty')
        return False
    pipette.volume -= given
    vessel.volume += given
    pipette.events.append(f'{vessel.name}: delivered {given:.2f} ml')
    sync(model, {vessel.name: vessel}, pipette)
    return True


# The balance's readout, as generate_open_balance.py builds it: five digits of
# seven segments and a decimal point, all lit, waiting to be switched off.
NUMERALS = {
    '0': 'abcdef', '1': 'bc', '2': 'abdeg', '3': 'abcdg', '4': 'bcfg',
    '5': 'acdfg', '6': 'acdefg', '7': 'abc', '8': 'abcdefg', '9': 'abcdfg',
    ' ': '',
}
LIT = np.array([0.09, 0.11, 0.13, 1.0])
DARK = np.array([0.55, 0.62, 0.68, 0.10])
PLACES = 4


def display_prefix(model: mujoco.MjModel) -> str | None:
    """Attach prefix of the balance carrying the readout, or None if absent.

    Args:
        model: Compiled scene.

    Returns:
        The prefix, e.g. ``balance_5_``.
    """
    for i in range(model.ngeom):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i) or ''
        if name.endswith('seg_0_a'):
            return name[:-len('seg_0_a')]
    return None


def show_mass(model: mujoco.MjModel, grams: float,
              prefix: str | None = None) -> str:
    """Write a mass onto the balance's display.

    The original model's "0.0000" is extruded geometry, not a texture, so the
    number is changed by switching segments rather than by redrawing a bitmap.
    Writing `geom_rgba` is enough: both the interactive viewer and the
    offscreen renderer read it every frame.

    Args:
        model: Compiled scene; its geom colours are written.
        grams: Mass to show. More than the display holds reads as dashes, the
            way a real balance shows an over-range.
        prefix: Attach prefix of the balance in the scene; found when omitted.

    Returns:
        The string that was shown, or an empty string when the scene has no
        readout to write to.
    """
    prefix = prefix or display_prefix(model)
    if prefix is None:
        return ''
    text = f'{grams:.{PLACES}f}'
    if grams < 0 or len(text.split('.')[0]) > 1:
        text = '-' * (PLACES + 1)
    digits = text.replace('.', '')

    for index in range(PLACES + 1):
        glyph = digits[index] if index < len(digits) else ' '
        lit = NUMERALS.get(glyph, 'adg')       # anything odd reads as a dash
        for segment in 'abcdefg':
            name = f'{prefix}seg_{index}_{segment}'
            model.geom_rgba[model.geom(name).id] = (
                LIT if segment in lit else DARK)
    model.geom_rgba[model.geom(f'{prefix}point').id] = LIT
    return text
