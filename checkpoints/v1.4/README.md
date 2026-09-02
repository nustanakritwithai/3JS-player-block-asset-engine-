# Character Prototype Studio V1.4 — Impact / Compression / Recovery

V1.4 is an incremental checkpoint built directly on top of V1.3.

## New motion layer

The animation stack is now:

Authored Keyframes
→ Weight Transfer
→ Weight-Driven Pelvis
→ Upper Body Weight Response
→ **Impact / Compression / Recovery**
→ Animation QA / Balance QA
→ Game Animation Runtime

## Impact sources

Impact markers reuse existing Studio data instead of creating a separate animation system:

- foot contact transitions
- `footstep` animation events
- `hit` animation events
- manually-authored impact markers at the playhead

Supported marker types:

- `foot.L`
- `foot.R`
- `hit`
- `custom`

## Four-phase response

1. Anticipation — small brace / pre-impact rise
2. Impact — peak load at the marker
3. Compression — pelvis lowers, knees bend, chest recoils, head lags
4. Recovery — damped overshoot back toward the authored trajectory

## Controls

- anticipation time
- compression time
- recovery time
- pelvis compression
- knee compression
- chest recoil
- head lag
- recovery overshoot
- damping
- foot impact strength
- hit impact strength
- maximum combined response

## Authoring workflow

- Generate impact markers from Contact / Events
- Add manual marker at current playhead
- Preview current impact response
- Bake Impact Keys
- Clear Bake

Bake may insert phase keys around an impact when the authored timeline has no key at a required phase boundary.
Generated phase keys are provenance-marked so Clear Bake can remove only generated impact keys.

## Runtime

The exported game AnimationRuntime evaluates the same impact marker envelopes. A clip that has been baked marks the impact profile as baked so the additive runtime layer is not applied twice.

## Development rule

Continue from this checkpoint. Do not rebuild the Studio from scratch.

Next planned layer: **V1.5 — Momentum / Start / Stop / Acceleration / Recovery**.
