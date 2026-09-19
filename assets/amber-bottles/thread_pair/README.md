# Threaded neck/cap pairs

Step 1 of [`simulation/CAP_GRIPPER_PLAN.md`](../../../simulation/CAP_GRIPPER_PLAN.md):
a cap that actually engages the neck, so the unscrewing can be simulated in
Isaac instead of animated.

The catalogue's cap is a **smooth bore with clearance** over the neck thread
(`cap_dims()`: `ri = N/2 - 0.3 + 0.35`) — it slips on, it cannot grip. These
pairs add the matching internal helix.

Regenerate (no Blender install needed — `bpy` is a pip package):

    uv run --python 3.11 --with bpy python generate_amber_bottles.py --pair 30 --out thread_pair

`--pair <ml>` builds the flask and a threaded cap, runs the screw check, writes
the GLBs and a `.blend`, and exits non-zero if the check fails.

## What is in here

| File | What |
| --- | --- |
| `neck_PP<N>.glb` | The whole flask, thread included — the neck is the part that matters |
| `cap_PP<N>_threaded.glb` | The cap with the internal helix |
| `thread_pair_PP<N>.blend` | Both, the cap posed closed on the flask |

## The numbers

Thread parameters are the ones the kit already used for the neck
(`pitch = 0.11·N`, `tdepth = 0.04·N`, `THREAD_TURNS = 2.0`) on standard PP
necks. Two clearances were added, both module constants so they can be swept:

- `THREAD_CLEARANCE = 0.15 mm` — radial, between the cap's crest and the neck's
  root. **This is the number that decides whether a recap cross-threads**, so it
  is a parameter, not an accident.
- `SEAT_CLEARANCE = 0.15 mm` — axial, over the lip when closed. Without it the
  cap's inner ceiling lands exactly on the lip (both at `z = H`): two coincident
  faces, which a rigid solver reads as interpenetration rather than contact.
  The thread carries the cap and the lip is touched by contact, like the real
  liner. Applied only when `threaded=True`.

| Neck | Pitch | Neck crest | Cap crest | Unscrew |
| --- | --- | --- | --- | --- |
| PP18 | 1.98 mm | 0.72 mm | 0.92 mm | 720°, **3.96 mm** |
| PP20 | 2.20 mm | 0.80 mm | 1.00 mm | 720°, **4.40 mm** |
| PP25 | 2.75 mm | 1.00 mm | 1.20 mm | 720°, **5.50 mm** |
| PP28 | 3.08 mm | 1.12 mm | 1.32 mm | 720°, **6.16 mm** |

The 30 ml flask — the one the pipetting work already uses — is PP20: **two
turns, 4.4 mm of travel.** That sets the iris clamp's regrip budget: a 120°
stroke means 6 regrips per cap, 180° means 4.

## How the check works

Rotating by α about Z *and* rising by `pitch·α/2π` maps a helix onto itself, so
that transform is exactly the unscrewing motion. `screw_clearance()` steps the
cap through 720° in 72 steps and asks a `BVHTree.overlap()` whether any face
pair intersects. With the clearances above, none do, at any size.

This is geometry, not physics — it proves the two threads can pass through each
other's space, which is the precondition for step 2 (SDF contact in PhysX), not
a substitute for it.

## Note

The catalogue is untouched: `make_cap(N)` still defaults to the smooth bore, and
every mesh the kit produces hashes identically to before this change — verified
across all four neck sizes and all six bottle sizes.
