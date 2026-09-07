# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.10.2 — Core-First Character Boot Hotfix**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Keep the main 3D character visible first; animation QA remains blocked until live visual acceptance passes.

## V1.8.10.2 — Core-First Character Boot Hotfix

V1.8.10.2 changes boot ownership so editor controls can no longer prevent the main character from rendering.

Boot rules:

1. Three.js **core** is the only mandatory 3D dependency.
2. Core sources: jsDelivr → esm.sh → unpkg.
3. OrbitControls / TransformControls are optional.
4. If editor controls fail, the Studio uses no-op fallback controls and still renders the character.
5. Saved-state recovery from V1.8.10.1 remains available; backup key is `characterPrototypeStudio.v1.8.10.2.recoveryBackup`.
6. A visible error overlay is reserved for failure to load Three.js core / WebGL boot, not ordinary editor-control failure.

This preserves all Monster Ball animation behavior from V1.8.10, including `actionType = throw`, Capture/Quick/Power/Summon throw timings, `ball.release`, `capture.throw`, and `monster.summon`.

## Preserved systems

- Twist Isolation
- Walk lateral cap `0.016m`
- distinct Run/Sprint
- Foot Plant max root correction `0.028m`
- Jump/Fall/Land/Crouch
- Dodge/Hit/Knockback/Get Up/Death/Faint/Interact
- Monster Ball Action Pack
- rigid `THREE.Group` rig
- 2K PBR gate

## Roadmap

- **V1.8.10.2** — Core-first character boot reliability
- **V1.8.11** — blocked until the main character is visibly restored on the user's device
- then Core Animation QA / Transitions

## Development rule

Continue incrementally from the latest checkpoint; do not rebuild the Studio from scratch.
