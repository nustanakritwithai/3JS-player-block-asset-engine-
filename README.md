# 3JS Player Block Asset Engine

Checkpoint repository for **Three.js Character Prototype Studio**.

## Current checkpoint

**V1.2 — Weight-Driven Pelvis Solver / COM Feedback**

The project is a mobile-first Three.js tool for building blocky / stylized characters, editing rigid pivot rigs, authoring poses and animation clips, validating animation quality, exporting game-ready animation runtime assets, and building progressively more believable weight response.

### Current pipeline

Reference / Concept → img2threejs Adapter → CharacterSpec → Body / Rig / LookDev → Pose Library → Animation Timeline → Foot Contact → Weight Transfer Curve → **Weight-Driven Pelvis Solver** → Animation QA / Balance QA → Game Animation Runtime → Export

### V1.2 additions

- V1.1 continuous Left/Right weight curve drives pelvis response
- weighted support-foot target
- live Center of Mass feedback
- bounded lateral pelvis shift
- hip drop/lift
- pelvis twist
- vertical compression under strong single-leg support
- non-destructive runtime preview
- explicit Bake Solver to authored keyframes
- provenance-tracked Clear Bake
- Animation QA and Balance QA evaluate the solver layer
- exported game runtime includes a lightweight deterministic pelvis-weight solver

### Existing foundation retained

- CharacterSpec V1 as source of truth
- Blocky humanoid procedural generator
- THREE.Group rigid pivot rig
- Body mass / equipment mass / COM / support area
- Pose Library / pose delta / joint chains
- Authored Animation Timeline and keyframes
- Procedural animation baking
- Weight & foot-contact timeline
- Foot sliding inspector / Foot Lock Assist
- V1.1 Weight Transfer Curve
- Animation Quality Inspector
- Runtime states, transitions and animation events
- img2threejs staging adapter
- Game-oriented runtime/export contracts

## Development rule

Future development must **continue from the latest committed/checkpointed version of this project instead of rebuilding the Studio from scratch**.

Realism roadmap:

V1.0 COM & Support → V1.1 Weight Transfer Curve → **V1.2 Weight-driven Pelvis** → V1.3 Spine/Chest/Head Response → V1.4 Compression/Impact → V1.5 Momentum → V1.6 Equipment Mass Response → V1.7 Attack Weight → V1.8 Foot Plant/IK → V1.9 Weight QA → V2.0 Animation Weight Studio.

See `checkpoints/v1.2/` for the V1.2 checkpoint notes and solver contract.
