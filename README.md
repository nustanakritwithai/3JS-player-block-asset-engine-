# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.10 — Monster Ball Action Pack**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Complete the character's **main Pocket Monster gameplay animations before Weapon Attachment**.

The highest-priority character actions are now:

1. Throw a capture ball at a monster.
2. Summon a monster from a ball.
3. Command / direct the summoned monster.
4. Preserve the existing movement, dodge, reaction and recovery animation foundation.

Weapon Attachment remains deferred.

## V1.8.10 — Monster Ball Action Pack

V1.8.10 makes ball throwing a first-class Body Dynamics action instead of borrowing Sword Slash/Punch behavior.

### New Body Dynamics action

`actionType = throw`

Throw kinetic chain:

`Back-foot load → Pelvis lead → Chest rotation → Shoulder → Elbow/Wrist → Ball Release → Follow-through → Recover`

The throw profile exists in both Studio preview and standalone runtime export.

### Added Pose Library states

- Ball Ready
- Ball Aim
- Throw Wind-up
- Throw Release
- Throw Follow-through
- Monster Command

### Added Animation Library templates

- Ball Aim Loop
- Capture Throw R
- Capture Throw L
- Quick Throw R
- Power Throw R
- Summon Monster R
- Monster Command

Capture throwing is intentionally emphasized with multiple signatures instead of one generic throw.

### Throw timing signatures

- Quick Throw — release around `0.34s`
- Standard Capture Throw — release around `0.56s`
- Power Throw — release around `0.68s`
- Summon Throw — release around `0.55s`

### Game event contract

The throw clips emit gameplay events at authored release timing:

- `ball.aim`
- `ball.release`
- `capture.throw`
- `monster.summon`
- `throw.follow_through`
- `monster.command`

`ball.release` uses `hand.R` or `hand.L` according to the throwing side so Pocket Monster runtime can spawn/release the ball on the exact animation frame.

Summon Throw emits `monster.summon` on the same release frame so the monster system can synchronize VFX, ball trajectory and monster appearance.

## Preserved core animation systems

- V1.8.5.2 Twist Isolation and Animation Library restore
- V1.8.5.3 Natural Walk pelvis lateral cap `±0.016m`
- V1.8.6 Walk / Run / Sprint / Start / Stop / Turn / Strafe dynamics
- V1.8.7 Foot Plant + Leg Response with bounded root correction
- V1.8.8 Jump / Fall / Land / Crouch movement pack
- V1.8.9 Dodge / Hit / Knockback / Get Up / Death / Faint / Interact pack
- rigid `THREE.Group` rig architecture
- 2K PBR quality gate

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → V1.8.9 → V1.8.10 → SHA-256 gate → Pages`

## Animation roadmap before weapons

- **V1.8.10** — Monster Ball Action Pack: capture throw variants + summon + monster command
- **V1.8.11** — Core Animation QA / Transitions: Idle↔Walk↔Run, Jump→Fall→Land, Crouch enter/exit, Dodge/Reaction recovery, Ball Aim→Throw→Recover, Summon→Command, contact consistency and visual acceptance
- **V1.8.12** — Gameplay Animation Polish if visual acceptance finds missing main actions or timing problems

Only after the main gameplay animation set is visually accepted should Weapon Attachment be reconsidered.

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.
