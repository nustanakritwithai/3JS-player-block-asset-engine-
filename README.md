# 3JS Player Block Asset Engine

Checkpoint repository for **Three.js Character Prototype Studio**.

## Current checkpoint

**V0.9 — Game Animation Runtime / Events / Transitions**

The project is a mobile-first Three.js tool for building blocky / stylized characters, editing rigid pivot rigs, authoring poses and animation clips, validating animation quality, and exporting game-ready runtime assets.

### Current pipeline

Reference / Concept → img2threejs Adapter → CharacterSpec → Body / Rig / LookDev → Pose Library → Animation Timeline → Weight & Contact → Animation QA → Game Animation Runtime → Export

### V0.9 capabilities

- CharacterSpec V1 as source of truth
- Blocky humanoid procedural generator
- Body proportion editor
- THREE.Group rigid pivot rig
- Joint limits, mirror and pivot editing
- Material / lighting presets
- Pose Library and pose-delta custom poses
- Timeline / authored keyframes
- Procedural Idle / Walk / Run baking
- Weight and foot-contact timeline
- Foot sliding inspector and Foot Lock Assist
- Animation Quality Inspector
- img2threejs artifact adapter with staging/diff
- Runtime animation states
- `play()`, `transition()`, `stop()`, `update(dt)` contract
- animation events: footstep / hit / VFX / SFX / custom
- sockets for hand/head/chest/root/feet/back
- CharacterSpec / runtime / TypeScript / QA exports

## Checkpoint policy

This repository is now the checkpoint/source location for the tool. Future development should **continue from the latest committed version here instead of rebuilding the project from scratch**.

See `checkpoints/v0.9/` for the exact V0.9 snapshot and documentation.
