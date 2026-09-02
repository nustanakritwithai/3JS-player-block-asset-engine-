# Character Prototype Studio V1.5 — Momentum / Acceleration / Braking

V1.5 continues directly from V1.4. No subsystem is rebuilt from scratch.

## New in V1.5

- semantic runtime motion class per animation clip: idle / walk / run / action / custom
- per-clip target motion speed
- desired velocity signal
- acceleration and braking limits
- turn-rate signal
- automatic idle / walk / run selection from desired speed
- spring-damped inertial lean
- start lean during acceleration
- backward/braking lean during deceleration
- turn lean scaled by speed and turn rate
- forward/back inertial body shift
- live velocity / acceleration / lean diagnostics
- momentum response layered after Weight + Impact
- exported AnimationRuntime exposes `setDesiredVelocity()` and `setTurnRate()`

## Motion ownership boundary

The Animation Runtime does **not** own world position, collision or authoritative player velocity. The game/movement system owns those values. The animation layer consumes movement signals and produces visual body response and locomotion-state selection.

## Current motion stack

Authored Keyframes → Weight Transfer → Pelvis Solver → Upper Body Response → Impact / Compression / Recovery → Momentum / Inertia → Animation Runtime

## Next planned checkpoint

V1.6 — Equipment Mass Response: weapon/equipment mass affects shoulder, chest, pelvis counterbalance, stance width and recovery timing.
