"""What the vision system hands the rest of the lab: bottles found, named and placed

A :class:`PerceivedBottle` is one bottle the fixed camera proposed and, if the
wrist camera confirmed it, its sample: where it stands on the bench, how sure
each stage was and whether the position was refined from the wrist. Nothing
in it comes from the simulator's state.

:func:`to_dashboard` turns a list of them into the ``vessels`` array of the
lab state's ``perception`` block (``perception_state`` in
``dashboard/bridge/labbridge/state.py``), so the bridge can publish what the
cameras really saw in place of its mock:

    from labbridge import state as S
    from labvision.world import to_dashboard

    S.perception_state(active_camera="overview", vessels=to_dashboard(found))
"""

import math
from dataclasses import dataclass, replace

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


def to_dashboard(
    bottles: list[PerceivedBottle], *, spare_from: int | None = None
) -> list[dict]:
    """The console's ``PerceivedVessel`` records

    ``index`` is each bottle's :attr:`PerceivedBottle.track`. The console
    joins records to its scene vessels on it, so a bottle with no track must
    not borrow a vessel's number: those are numbered on from ``spare_from``,
    skipping every track. Pass the number of vessels the console draws there;
    by default the count starts one past the largest track.

    Args:
        bottles: What the vision system found.
        spare_from: First index for bottles without a track.

    Example:
        >>> to_dashboard([PerceivedBottle((0.1, -0.4, 0.9), 0.87, "SMP-0005",
        ...     4, "liquid", refined=True)])[0]["cls"]
        'amber bottle'
    """
    tracks = {b.track for b in bottles if b.track is not None}
    spare = spare_from if spare_from is not None else max(tracks, default=-1) + 1
    records = []
    for bottle in bottles:
        index = bottle.track
        if index is None:
            while spare in tracks:
                spare += 1
            index, spare = spare, spare + 1
        records.append(
            {
                "index": index,
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
        )
    return records


def one_per_sample(bottles: list[PerceivedBottle]) -> list[PerceivedBottle]:
    """Drop the second sighting of a sample, keeping the best one in place

    Two proposals a few centimetres apart on one bottle both send the wrist to
    it, and both come back with its name. A sample stands in one place, so
    one record is kept: refined over unrefined, then the higher score. Bottles
    not named are all kept, since nothing says they are the same.

    Example:
        >>> a = PerceivedBottle((0.0, 0.0, 0.9), 0.4, "SMP-0001", refined=True)
        >>> b = PerceivedBottle((0.04, 0.0, 0.9), 0.9, "SMP-0001")
        >>> one_per_sample([b, a]) == [a]
        True
    """
    best: dict[str, int] = {}
    for i, bottle in enumerate(bottles):
        if bottle.sample_id is None:
            continue
        kept = best.get(bottle.sample_id)
        rank = (bottle.refined, bottle.confidence)
        if kept is None or rank > (bottles[kept].refined, bottles[kept].confidence):
            best[bottle.sample_id] = i
    keep = set(best.values())
    return [b for i, b in enumerate(bottles) if b.sample_id is None or i in keep]


def assign_tracks(
    bottles: list[PerceivedBottle],
    anchors: dict[int, tuple[float, float]],
    *,
    max_m: float = 0.08,
) -> list[PerceivedBottle]:
    """Give each bottle the index of the anchor it stands on, nearest pairs first

    The console draws its scene vessels by index and joins ``vessels`` to them
    on it, so a publisher that knows where those vessels are (the bridge knows
    its scene, for display) can hand them in as anchors. Pairs are made one to
    one, the closest first; a bottle with no anchor within ``max_m`` keeps its
    track as it was.

    Args:
        bottles: What the vision system found.
        anchors: Index to (x, y) of each vessel the console knows.
        max_m: Farthest a bottle may stand from its anchor.

    Returns:
        The same bottles, in the same order, with ``track`` set where matched.

    Example:
        >>> found = [PerceivedBottle((0.51, 0.0, 0.9), 0.8)]
        >>> assign_tracks(found, {3: (0.5, 0.0), 4: (0.0, 0.0)})[0].track
        3
    """
    pairs = sorted(
        (math.dist(bottle.position[:2], xy), i, index)
        for i, bottle in enumerate(bottles)
        for index, xy in anchors.items()
    )
    taken_bottles, taken_anchors = set(), set()
    tracked = list(bottles)
    for distance, i, index in pairs:
        if distance > max_m or i in taken_bottles or index in taken_anchors:
            continue
        tracked[i] = replace(bottles[i], track=index)
        taken_bottles.add(i)
        taken_anchors.add(index)
    return tracked
