# Weight-Driven Pelvis Solver — V1.2

## Solver flow

`Weight Transfer Curve → weighted support-foot target → COM feedback → pelvis response`

## Inputs

- continuous `weightValue.L` / `weightValue.R`
- `foot.L` and `foot.R` sockets
- Center of Mass from the V1.0 mass model
- solver limits/configuration

## Response channels

- `shiftX` — bounded lateral pelvis shift toward weighted support
- `comCorrection` — bounded Center-of-Mass feedback correction
- `hipDrop` — pelvis Z rotation from left/right weight dominance
- `twist` — pelvis Y rotation
- `compression` — pelvis vertical lowering under strong single-leg support

## Default configuration

```json
{
  "enabled": true,
  "lateralInfluence": 0.55,
  "maxShift": 0.14,
  "hipDropDeg": 5,
  "twistDeg": 6,
  "compression": 0.025,
  "comGain": 0.45,
  "comMaxCorrection": 0.10,
  "smoothing": 0.65
}
```

## Non-destructive preview

The authored animation remains the source clip. Runtime preview applies the solver additively after the authored pose has been evaluated.

## Bake contract

Bake writes only pelvis position/rotation deltas and stores provenance on the keyframe:

```json
{
  "meta": {
    "pelvisSolverBake": {
      "version": "1.2",
      "shiftX": 0.04,
      "compression": 0.02,
      "hipDrop": 0.05,
      "twist": -0.03,
      "comCorrection": 0.01
    }
  }
}
```

When a clip is marked baked, the additive solver is skipped so the response is not applied twice. `Clear Bake` subtracts the provenance-tracked delta.

## Runtime export

The in-Studio solver can use live COM and foot socket positions. The exported lightweight runtime uses the same authored weight curve with a deterministic bounded pelvis response suitable for the existing rigid `THREE.Group` rig.

## Next layer

V1.3 should propagate motion upward:

`Pelvis → Chest/Spine counter-motion → Neck → Head stabilization`.
