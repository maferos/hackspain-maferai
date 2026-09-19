"""What the vision system hands the rest of the lab: bottles found, named and placed

A :class:`PerceivedBottle` is one bottle the fixed camera proposed and, if the
wrist camera confirmed it, its sample: where it stands on the bench, how sure
each stage was and whether the position was refined from the wrist. Nothing
in it comes from the simulator's state.

:func:`to_dashboard` turns a list of them into the ``vessels`` array of the
console's ``perception`` block (``dashboard/src/state/types.ts``,
``PerceivedVessel``), so the bridge can publish what the cameras really saw
in place of its mock:

    from labbridge import state as S
    from labvision.world import to_dashboard

    S.perception_state(active_camera="overview", vessels=to_dashboard(found))
"""

from dataclasses import dataclass

CLASS_NAMES = {"liquid": "amber bottle", "powder": "hdpe bottle"}
"""The console's class name for each phase's bottle kit."""
UNKNOWN_CLASS = "bottle"
"""Class name while the bottle is not yet named, so its kit is not known."""


@dataclass
class PerceivedBottle:
    """One bottle the vision system found

    Attributes:
        position: (x, y, z) of the base centre on the bench, world metres.
        confidence: The fixed camera detector's score for the proposal.
        sample_id: The sample the wrist camera read, or None if not confirmed.
        marker_id: The ArUco marker it read, or None.
        phase: ``liquid`` or ``powder`` from the sample's record, or None.
        refined: True if the position comes from the wrist camera's view of
            the ring rather than the fixed camera's box.
        stale: True if the estimate predates the last change to the scene.
        track: A stable index for this bottle across frames, or None. The
            console joins ``vessels`` to its scene by ``index``, so whoever
            publishes them should associate each bottle with a scene vessel
            (by position, which the bridge knows) and put its index here.
    """

    position: tuple[float, float, float]
    confidence: float
    sample_id: str | None = None
    marker_id: int | None = None
    phase: str | None = None
    refined: bool = False
    stale: bool = False
    track: int | None = None

    @property
    def cls(self) -> str:
        """The console's class name: by kit once the sample is known"""
        return CLASS_NAMES.get(self.phase or "", UNKNOWN_CLASS)


def to_dashboard(bottles: list[PerceivedBottle]) -> list[dict]:
    """The console's ``PerceivedVessel`` records

    ``index`` is each bottle's :attr:`PerceivedBottle.track`, or its place in
    the list when it has none. Only a track joins a record to the console's
    scene vessel; list order is just a number.

    Example:
        >>> to_dashboard([PerceivedBottle((0.1, -0.4, 0.9), 0.87, "SMP-0005",
        ...     4, "liquid", refined=True)])[0]["cls"]
        'amber bottle'
    """
    return [
        {
            "index": index if bottle.track is None else bottle.track,
            "id": bottle.sample_id,
            "cls": bottle.cls,
            "confidence": round(float(bottle.confidence), 3),
            "position": {
                "x": float(bottle.position[0]),
                "y": float(bottle.position[1]),
                "z": float(bottle.position[2]),
            },
            "stale": bool(bottle.stale),
        }
        for index, bottle in enumerate(bottles)
    ]
