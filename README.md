# 3JS Player Block Asset Engine

Checkpoint repository for **Three.js Character Prototype Studio**.

## Current checkpoint

**V1.0 — Center of Mass / Support Area / Balance**

The project is a mobile-first Three.js tool for building blocky / stylized characters, editing rigid pivot rigs, authoring poses and animation clips, validating animation quality, exporting game-ready animation runtime assets, and now analyzing physical weight/balance cues for more believable motion.

### Current pipeline

Reference / Concept → img2threejs Adapter → CharacterSpec → Body / Rig / LookDev → Pose Library → Animation Timeline → Weight & Contact → Animation QA → Game Animation Runtime → **Animation Weight Engine (COM / Support / Balance)** → Export

### V1.0 additions

- Relative mass profile per body region
- Optional equipment mass
- Center of Mass (COM) calculation
- COM debug marker
- Supporting-foot detection
- Support-area visualization
- Weight vector to ground
- Current-pose balance analysis
- Full authored-animation balance sampling
- Timed balance warnings/hard issues with Timeline jump
- Balance data in Quality Report

### Existing foundation retained

- CharacterSpec V1 as source of truth
- Blocky humanoid procedural generator
- THREE.Group rigid pivot rig
- Pose Library / pose delta / joint chains
- Authored Animation Timeline and keyframes
- Procedural animation baking
- Weight & foot-contact timeline
- Foot sliding inspector / Foot Lock Assist
- Animation Quality Inspector
- Runtime states, transitions and events
- img2threejs staging adapter
- Game-oriented runtime/export contracts

## Development rule

Future development must **continue from the latest committed/checkpointed version of this project instead of rebuilding the Studio from scratch**.

Current roadmap for realism:

V1.0 COM & Support → V1.1 Weight Transfer Curve → V1.2 Weight-driven Pelvis → V1.3 Spine/Chest/Head Response → V1.4 Compression/Impact → V1.5 Momentum → V1.6 Equipment Mass Response → V1.7 Attack Weight → V1.8 Foot Plant/IK → V1.9 Weight QA → V2.0 Animation Weight Studio.

See `checkpoints/v1.0/` for the V1.0 checkpoint notes.
