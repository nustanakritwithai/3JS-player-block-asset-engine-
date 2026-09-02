# Upper Body Weight Response — V1.3

## Goal

Reduce the rigid-block feeling by propagating stance and pelvis response into the upper body while keeping the existing THREE.Group rig and authored keyframes intact.

## Response chain

Pelvis → Chest → Neck → Head

### Chest

- counter-twists against pelvis Y rotation
- counter-bends against pelvis hip drop
- adds a small forward lean under strong single-leg loading

### Neck

Partially counters chest response so the neck/head chain does not simply inherit the whole torso motion.

### Head

Offsets a configurable fraction of accumulated pelvis + chest + neck rotation.

This is stylized stabilization rather than ragdoll or physical simulation.

## Non-destructive preview

The solver is an additive runtime projection until Bake is explicitly requested.

## Bake contract

Bake modifies only local rotations for:

- `chest`
- `neck`
- `head`

Each keyframe stores exact applied deltas in `meta.upperBodySolverBake`.

Clear Bake subtracts only those tracked deltas, preserving authored animation outside the solver layer.

A baked clip is marked through `weightTransfer.upperBodySolverBakedAt` so the additive layer is not applied twice.

## Main parameters

- `chestCounterTwist`
- `chestCounterBend`
- `chestLeanDeg`
- `neckCounter`
- `headStabilization`
- `headPitchStabilization`
- `strength`
- `smoothing`

## Runtime export

The generated AnimationRuntime evaluates the same continuous stance weights and applies a lightweight deterministic response to Chest / Neck / Head.

The Studio implementation remains richer because the V1.2 pelvis layer can incorporate live COM feedback.

## Next phase

V1.4 should add animation phases for Anticipation → Impact → Compression → Recovery and connect them to contact/event timing.
