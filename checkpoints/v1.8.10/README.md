# Character Prototype Studio V1.8.10 — Monster Ball Action Pack

V1.8.10 is an incremental extension of V1.8.9. Weapon Attachment remains deferred because capture-ball throwing and monster summoning are main Pocket Monster gameplay actions.

## Goal

Make ball throwing visually readable and runtime-synchronized as a first-class animation action.

## New Body Dynamics action

`throw`

Kinetic chain:

`Back-foot load → Pelvis → Chest → Shoulder → Elbow/Wrist → Release → Follow-through → Recovery`

The action profile is included in both Studio and standalone runtime Body Dynamics tables.

## Pose Library additions

- Ball Ready
- Ball Aim
- Throw Wind-up
- Throw Release
- Throw Follow-through
- Monster Command

## Animation Library additions

- Ball Aim Loop
- Capture Throw R
- Capture Throw L
- Quick Throw R
- Power Throw R
- Summon Monster R
- Monster Command

## Throw signatures

- Quick: short wind-up, release about `0.34s`
- Standard capture: full transfer, release about `0.56s`
- Power: deeper load/follow-through, release about `0.68s`
- Summon: release about `0.55s` with summon event contract

## Runtime event contract

Throw clips expose:

- `ball.aim`
- `ball.release`
- `capture.throw`
- `monster.summon`
- `throw.follow_through`
- `monster.command`

The release event is bound to `hand.R` or `hand.L` based on throw side.

`monster.summon` fires on the same authored frame as `ball.release` for the Summon Throw so gameplay, trajectory, VFX and monster appearance can synchronize.

## Ownership

- Body Dynamics `throw` owns throw torso/arm kinetic response.
- Authored keyframes define the readable ball-hand pose sequence.
- Weight / contact metadata defines back-foot → front-foot transfer.
- Foot Plant remains enabled for grounded throw support.
- Locomotion Dynamics is disabled for ball-throw clips.
- No Weapon Attachment dependency is introduced.

## Preserved regressions

- Twist Isolation
- Walk lateral cap `0.016m`
- Run/Sprint distinction
- Foot Plant root safety cap `0.028m`
- Jump/Fall/Land/Crouch
- Dodge/Hit/Knockback/Get Up/Death/Faint/Interact
- Animation Library above Timeline
- rigid `THREE.Group` rig
- 2K PBR texture gate

## Next

**V1.8.11 — Core Animation QA / Transitions** should include Ball Aim → Capture Throw → Recover and Summon Throw → Monster Command alongside the existing movement/reaction transition groups.

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → V1.8.9 → V1.8.10 → SHA-256 gate → Pages`
