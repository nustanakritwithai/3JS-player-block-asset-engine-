# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.10.3 — clip Reference Hotfix**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Restore the main 3D character renderer before any V1.8.11 animation work.

## V1.8.10.3 — clip Reference Hotfix

The live boot error was identified exactly as:

`clip is not defined`

Root cause was in `renderContactAnalysis()`:

- the function read `clip.footPlant` during `initUI()`
- no local `clip` variable had been declared
- both normal boot and recovery call `initUI()`, so both paths failed before `buildCharacter()` could finish

V1.8.10.3 fixes the scope explicitly:

- `const clip = selectedAnimationClip()`
- `contactStateAtTime(clip, animationState.time)`
- null-safe `clip?.footPlant?.enabled !== false`

CI now contains a dedicated regression gate that rejects the old free-variable expression.

## V1.8.10.2 boot reliability remains preserved

- Three.js core is the only mandatory 3D dependency
- core sources: jsDelivr → esm.sh → unpkg
- OrbitControls / TransformControls are optional and may fall back to no-op controls
- saved-state recovery remains available

## Preserved gameplay systems

- Monster Ball Action Pack / `actionType = throw`
- `ball.release`, `capture.throw`, `monster.summon`
- Capture / Quick / Power / Summon throw timing signatures
- Twist Isolation
- Walk lateral cap `0.016m`
- distinct Run/Sprint
- Foot Plant max root correction `0.028m`
- Jump/Fall/Land/Crouch
- Dodge/Hit/Knockback/Get Up/Death/Faint/Interact
- rigid `THREE.Group` rig
- 2K PBR gate

## Roadmap

- **V1.8.10.3** — undefined `clip` boot regression fix
- **V1.8.11** — blocked until live visual acceptance confirms the main character is visible
- then Core Animation QA / Transitions

## Development rule

Continue incrementally from the latest checkpoint; do not rebuild the Studio from scratch.
