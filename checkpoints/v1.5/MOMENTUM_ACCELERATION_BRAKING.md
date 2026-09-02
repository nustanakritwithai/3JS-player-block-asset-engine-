# Momentum / Acceleration / Braking — V1.5

## Runtime signals

The runtime now tracks:

- `velocity`
- `targetVelocity`
- `acceleration`
- `turnRate`
- `targetTurnRate`
- pitch/roll inertial lean state

## Velocity integration

The runtime approaches target velocity using separate acceleration and braking limits. This does not move the character in world space; it only models the animation response to the movement system's signals.

## Inertial response

Acceleration produces forward start lean. Negative acceleration produces brake lean. Turn rate produces lateral lean scaled by current speed. Lean is solved with a spring-damped response rather than instant interpolation, allowing controlled lag and overshoot.

## Locomotion auto-state

When enabled, desired speed maps to semantic classes:

- below walk threshold → `idle`
- between walk/run thresholds → `walk`
- above run threshold → `run`

The system searches authored clips by `runtime.motionClass` and reuses the existing animation transition/crossfade runtime.

## Clip runtime metadata

Each authored clip can define:

```json
{
  "runtime": {
    "state": "walk",
    "motionClass": "walk",
    "motionSpeed": 1.8
  }
}
```

## Game API

```ts
runtime.setDesiredVelocity(speed, {
  turnRate,
  autoState: true
});

runtime.setTurnRate(turnRate);
runtime.update(dt);
```

## Ownership boundary

Movement owns world position, collision, and authoritative velocity. Animation owns visual lean, body lag, braking response, turn lean, and locomotion animation-state selection.
