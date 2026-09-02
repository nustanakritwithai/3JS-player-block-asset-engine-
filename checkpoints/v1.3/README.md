# Character Prototype Studio V1.3 Checkpoint

**V1.3 — Spine / Chest / Neck / Head Weight Response**

This checkpoint continues directly from V1.2. It does not replace the existing CharacterSpec, animation timeline, weight transfer, pelvis solver, QA, or game animation runtime.

## New in V1.3

Weight response now propagates upward through the rigid hierarchy:

`Pelvis → Chest → Neck → Head`

Added controls:

- Chest Counter Twist
- Chest Counter Bend
- Chest Lean under single-leg loading
- Neck Counter response
- Head yaw/roll stabilization
- Head pitch stabilization
- Response Strength
- Response Smoothing

## Runtime behavior

The V1.3 response is additive on top of authored animation and the V1.2 pelvis solver.

The head compensates for part of the accumulated Pelvis + Chest + Neck rotation so the upper body does not behave as one rigid block.

## Authoring workflow

- Preview Chain: runtime-only / non-destructive
- Bake Chain to Keys: writes only Chest / Neck / Head rotation deltas
- Clear Bake: removes only provenance-tracked V1.3 deltas

Bake metadata is stored per keyframe in `meta.upperBodySolverBake`.

## QA / Runtime

- Animation QA samples the full weight-response chain
- Balance QA samples the full weight-response chain
- Quality Report includes upper-body solver config/result
- exported lightweight AnimationRuntime applies the upper-body response from the same weight metadata

## Next roadmap

V1.4 — Impact / Compression / Recovery phases.

Development rule remains unchanged: future work must continue from the latest checkpoint instead of rebuilding the Studio from scratch.
