# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.10.1 — Character Boot Recovery Hotfix**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Complete the character's **main Pocket Monster gameplay animations before Weapon Attachment** while keeping the main character renderer reliable on mobile/browser environments.

## V1.8.10.1 — Character Boot Recovery Hotfix

V1.8.10.1 fixes the visual-boot regression reported after V1.8.10 where the Studio UI could load while the main 3D character did not appear.

### 3D engine fallback

The Studio no longer has a single CDN failure point for Three.js startup.

Boot order:

1. Try Three.js + OrbitControls + TransformControls from **jsDelivr**.
2. If that source fails or times out, automatically retry from **esm.sh**.
3. If both fail, show a visible boot-error overlay instead of silently leaving an empty viewport.

### Saved-state recovery

If a browser-saved CharacterSpec causes `initUI()` / `buildCharacter()` startup to fail:

- the previous state is backed up under `characterPrototypeStudio.v1.8.10.1.recoveryBackup`
- the Studio boots the default character in Idle
- the viewport remains usable instead of staying blank

The main hotfix storage key is `characterPrototypeStudio.v1.8.10.1`, with fallback migration from V1.8.10 and earlier.

### Preserved gameplay animation work

V1.8.10 Monster Ball actions remain unchanged:

- Ball Aim Loop
- Capture Throw R / L
- Quick Throw R
- Power Throw R
- Summon Monster R
- Monster Command
- Body Dynamics `actionType = throw`
- `ball.release`, `capture.throw`, and `monster.summon` event contracts

All previous Walk/Run/Sprint, Foot Plant, Jump/Fall/Land/Crouch, Dodge/Reaction and Twist systems remain regression-gated.

## V1.8.10 — Monster Ball Action Pack

Throw kinetic chain:

`Back-foot load → Pelvis lead → Chest rotation → Shoulder → Elbow/Wrist → Ball Release → Follow-through → Recover`

Throw timing signatures:

- Quick Throw — release around `0.34s`
- Standard Capture Throw — release around `0.56s`
- Power Throw — release around `0.68s`
- Summon Throw — release around `0.55s`

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → V1.8.9 → V1.8.10 → V1.8.10.1 → SHA-256 gate → Pages`

## Animation roadmap before weapons

- **V1.8.10.1** — Character boot recovery / renderer reliability hotfix
- **V1.8.11** — Core Animation QA / Transitions including Ball Aim→Throw→Recover and Summon→Command
- **V1.8.12** — Gameplay Animation Polish if visual acceptance finds missing main actions or timing problems

Weapon Attachment remains deferred until the main gameplay animation set is visually accepted.

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.
