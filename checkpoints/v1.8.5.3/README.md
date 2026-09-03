# Character Prototype Studio V1.8.5.3 — Walk Pelvis Translation Hotfix

V1.8.5.3 is an incremental hotfix on top of V1.8.5.2. It reduces excessive visible side-to-side pelvis translation during Walk without reducing the underlying Weight Transfer or Center-of-Mass calculations.

## Root cause

Walk had two independent visual lateral-motion paths:

1. Procedural Walk applied `motionPreview.pelvisShift` directly to `pelvis.position.x`.
2. Authored Walk clips could receive additional lateral translation from the Weight/Pelvis Solver through foot target and COM correction.

V1.8.1 reduced the original sway, but the visible mapping was still too large. The simulation truth was not the problem; the visual mapping from weight/COM to pelvis translation was.

## Hotfix

Natural Walk now uses:

- procedural `pelvisShift`: `0.028m → 0.014m`
- authored/game-runtime Walk visual shift cap: `±0.016m`
- a second post-smoothing cap so solver history cannot reintroduce a larger Walk offset

The hotfix keeps these systems intact:

- Weight Transfer curve
- COM calculation and COM correction
- pelvis hip drop
- pelvis yaw/twist
- chest counter-rotation
- head stabilization
- V1.8.5.2 Twist Isolation
- Animation Library placement and contents

## Preset tuning

- Natural: pelvisShift `0.014m`, visual cap `0.016m`
- Subtle: pelvisShift `0.010m`, visual cap `0.012m`
- Stylized: pelvisShift `0.020m`, visual cap `0.024m`

Run is intentionally not capped by this hotfix. Run will receive its own dynamics design in V1.8.6 so it does not become a faster Walk.

## Migration

Existing saves using the exact V1.8.1 Natural default `pelvisShift = 0.028` migrate to `0.014`. Custom user values are preserved, while the Walk visual cap prevents excessive rendered translation.

## Development gate

V1.8.6 remains the next planned feature after live acceptance of the reduced Walk pelvis translation.

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → SHA-256 gate → Pages`
