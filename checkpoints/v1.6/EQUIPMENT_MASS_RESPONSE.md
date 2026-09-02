# Equipment Mass Response — V1.6

## Inputs
- equipment mass
- reference mass
- attachment socket
- response strength

## Response
- carrying-side shoulder drop
- chest counter-bend/twist
- pelvis counter-shift
- stance widening
- momentum inertia factor
- action recovery-rate multiplier

## COM
Equipment mass is positioned at the configured socket for Center-of-Mass analysis.

## Momentum
Effective animation acceleration/braking is reduced by:

`1 + loadRatio × inertiaScale`

This is visual motion inertia only; it does not change authoritative world movement.

## Recovery
For `runtime.motionClass = action`, the latter part of a clip can play slower:

`recoveryRate = 1 / (1 + loadRatio × recoverySlowdown)`

## Bake
Equipment posture can be baked to animation keys.
Bake provenance is stored at `meta.equipmentResponseBake`.

## Runtime ownership
The animation runtime only modifies visual response. Inventory, equipment rules, combat damage, authoritative position and collision remain owned by the game systems.

## Next
V1.7 — Attack Weight System:
Anticipation → Wind-up → Acceleration → Impact → Recovery,
with equipment mass directly affecting swing timing and follow-through.
