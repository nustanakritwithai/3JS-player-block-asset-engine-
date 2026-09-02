# Checkpoint V1.2 — Weight-Driven Pelvis Solver

This checkpoint continues directly from V1.1. Do not rebuild the Studio from scratch.

## Scope

V1.2 connects the V1.1 continuous Left/Right weight curve to actual pelvis response.

### Inputs
- `weightValue.L / weightValue.R`
- `foot.L / foot.R` sockets
- V1.0 Center of Mass
- support-foot target
- pelvis solver configuration

### Runtime response
- lateral pelvis shift
- COM feedback correction
- hip drop/lift
- pelvis twist
- vertical compression under strong single-leg support

### Authoring behavior
The solver is an additive runtime preview layer and does not silently mutate authored keyframes.

`Bake Solver to Keys` explicitly commits pelvis deltas into authored animation keys.
Each baked key stores `meta.pelvisSolverBake` provenance so `Clear Bake` can remove that exact solver delta later.

A baked clip disables the additive pelvis solver to prevent double application.

### QA
Animation QA and Balance QA evaluate the solver layer so COM/support changes are visible in quality checks.

### Export
The generated game AnimationRuntime receives a lightweight deterministic pelvis-weight solver compatible with the existing rigid `THREE.Group` rig.

## Next
V1.3: propagate weight response from Pelvis → Chest/Spine → Neck → Head stabilization/counter-motion.
