# 3JS Player Block Asset Engine

Checkpoint repository for **Three.js Character Prototype Studio**.

## Current checkpoint

**V1.5 — Momentum / Acceleration / Braking / Turn Inertia**

The project is a mobile-first Three.js tool for building blocky / stylized characters, editing rigid pivot rigs, authoring poses and animation clips, validating animation quality, exporting game-ready animation runtime assets, and progressively adding believable weight, balance, impact and inertia response.

### Current pipeline

Reference / Concept → img2threejs Adapter → CharacterSpec → Body / Rig / LookDev → Pose Library → Animation Timeline → Foot Contact → Weight Transfer Curve → Weight-Driven Pelvis → Upper Body Weight Response → Impact / Compression / Recovery → **Momentum / Acceleration / Braking** → Animation QA / Balance QA → Game Animation Runtime → Export

### V1.5 additions

- semantic runtime motion class per clip: idle / walk / run / action / custom
- per-clip target motion speed
- desired velocity, acceleration, braking and turn-rate signals
- automatic idle / walk / run selection from desired speed
- spring-damped start lean and brake lean
- turn lean scaled by speed and turn rate
- forward/back inertial body shift
- live velocity / acceleration / lean diagnostics
- animation movement response does not own world position or collision
- exported AnimationRuntime supports `setDesiredVelocity()` and `setTurnRate()`

### Existing foundation retained

- CharacterSpec V1 as source of truth
- Blocky humanoid procedural generator
- THREE.Group rigid pivot rig
- Body mass / equipment mass / Center of Mass / support area
- Pose Library / pose delta / joint chains
- Authored Animation Timeline and keyframes
- Procedural animation baking
- Weight & foot-contact timeline
- Foot sliding inspector / Foot Lock Assist
- V1.1 continuous Weight Transfer Curve
- V1.2 Weight-Driven Pelvis Solver / COM feedback
- V1.3 Chest / Neck / Head weight-response chain
- V1.4 Impact / Compression / Recovery
- Animation Quality Inspector
- Runtime states, transitions and animation events
- img2threejs staging adapter
- Game-oriented runtime/export contracts

## Development rule

Future development must **continue from the latest committed/checkpointed version of this project instead of rebuilding the Studio from scratch**.

Realism roadmap:

V1.0 COM & Support → V1.1 Weight Transfer Curve → V1.2 Weight-driven Pelvis → V1.3 Spine/Chest/Neck/Head Response → V1.4 Compression/Impact/Recovery → **V1.5 Momentum** → V1.6 Equipment Mass Response → V1.7 Attack Weight → V1.8 Foot Plant/IK → V1.9 Weight QA → V2.0 Animation Weight Studio.

See `checkpoints/v1.5/` for the current checkpoint notes and momentum runtime contract.
