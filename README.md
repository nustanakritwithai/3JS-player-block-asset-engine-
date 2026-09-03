# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.8 — Core Movement Animation Pack**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Complete the character's **core animation set before any Weapon Attachment work**.

Weapon Attachment is deferred until the essential movement/action/reaction library is complete and visually accepted.

## V1.8.8 — Core Movement Animation Pack

V1.8.8 extends the Animation Library and Pose Library with the missing core movement states while preserving V1.8.5.2–V1.8.7 animation/dynamics fixes.

New movement templates:

- Turn Left
- Strafe Left
- Jump
- Fall Loop
- Land
- Crouch Idle
- Crouch Walk

New Pose Library states:

- Jump Takeoff
- Jump Air
- Fall
- Land
- Crouch
- Crouch Step

Jump and Fall explicitly use air contact metadata. Landing/Crouch return to ground contact so V1.8.7 Foot Plant can take over when appropriate. Fall disables Foot Plant while airborne.

## Preserved animation systems

- V1.8.5.2 Twist Isolation and Animation Library restore
- V1.8.5.3 Natural Walk pelvis lateral cap `±0.016m`
- V1.8.6 distinct Walk / Run / Sprint / Start / Stop / Turn / Strafe dynamics
- V1.8.7 Foot Plant + Leg Response with bounded root correction
- rigid `THREE.Group` rig architecture
- 2K PBR quality gate

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → SHA-256 gate → Pages`

## Animation roadmap before weapons

- **V1.8.8** — Core Movement Animation Pack: Turn L/R, Strafe L/R, Jump, Fall, Land, Crouch
- **V1.8.9** — Core Action / Reaction Pack: Dodge L/R, Hit React, Knockback, Get Up, Death/Faint, Interact
- **V1.8.10** — Core Animation QA / transitions: state transitions, contact consistency, recovery and visual acceptance

Only after those core animation checkpoints are accepted should Weapon Attachment be reconsidered.

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.
