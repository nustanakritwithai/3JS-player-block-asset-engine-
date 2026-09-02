# Impact / Compression / Recovery Contract — V1.4

## Purpose

V1.4 adds a stylized impact-response layer on top of the existing authored animation and weight stack.

It reuses existing data from:

- V0.7 Foot Contact
- V0.9 animation events
- V1.1 Weight Transfer Curve
- V1.2 Weight-Driven Pelvis
- V1.3 Upper Body Weight Response

This keeps CharacterSpec / authored clips as the source of truth.

## Impact marker

```ts
interface ImpactMarker {
  id: string;
  time: number;
  type: "foot.L" | "foot.R" | "hit" | "custom";
  strength: number;
  generatedFrom?: string | null;
}
```

## Impact profile

```ts
interface ImpactProfile {
  enabled: boolean;
  anticipation: number;
  compressionTime: number;
  recovery: number;
  pelvisCompression: number;
  kneeCompressionDeg: number;
  chestRecoilDeg: number;
  headLagDeg: number;
  overshoot: number;
  damping: number;
  footStrength: number;
  hitStrength: number;
  maxCombined: number;
  bakedAt?: string;
}
```

## Response phases

### Anticipation

Before an impact marker, the body performs a small brace / pre-load response. This can slightly raise the pelvis and pre-rotate the chest before load arrives.

### Impact

The marker time is the peak load point. Foot and hit markers can use different default strengths.

### Compression

The body absorbs the load:

- pelvis moves downward
- stance knee bends most strongly
- opposite knee may react slightly
- chest recoils
- head lags behind torso response

### Recovery

A damped overshoot returns the body toward the authored animation trajectory rather than snapping immediately back to neutral.

## Multiple impact overlap

Marker envelopes may overlap. Contributions are summed and bounded by `maxCombined` so a dense sequence of contacts/events cannot create unbounded deformation.

## Bake behavior

`Bake Impact Keys` may insert authored keys at:

- anticipation start
- impact time
- compression end
- mid recovery
- recovery end

Each baked key records `meta.impactSolverBake` with the exact additive deltas.

Keys created only by the baker are marked `meta.impactGeneratedKey=true`.

If a generated key is manually re-keyed, it becomes authored and is no longer treated as disposable by Clear Bake.

## Runtime boundary

The animation runtime can dispatch `hit` events and render impact motion, but gameplay remains outside the animation system.

For example:

- animation event says when the sword reaches impact
- socket identifies where VFX can attach
- combat system decides whether damage actually applies

## QA

Animation QA warns when:

- impact markers exist but pelvis compression is nearly zero
- recovery duration is so short that motion is likely to snap
- foot impacts have almost no knee compression

Future V1.5 momentum should use impact/recovery state as part of start/stop and braking transitions.
