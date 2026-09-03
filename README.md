# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.9 — Core Action / Reaction Pack**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Complete the character's **core animation set before any Weapon Attachment work**.

Weapon Attachment remains deferred until movement, action/reaction, and animation-transition checkpoints are visually accepted.

## V1.8.9 — Core Action / Reaction Pack

V1.8.9 extends the Animation Library and Pose Library with the missing core non-weapon action/reaction states.

New Animation Library templates:

- Dodge Right
- Dodge Left
- Hit React
- Knockback
- Get Up
- Death
- Faint
- Interact

New Pose Library states:

- Dodge Lean
- Hit React
- Knockback
- Down / Back
- Faint
- Interact Reach

### Dynamics ownership

- **Dodge L/R** uses the existing V1.8.3 Body Dynamics `actionType = dodge`, so the lateral evade/body lean remains part of the action-dynamics system.
- **Hit React / Knockback / Get Up / Death / Faint / Interact** are authored `custom` states, not attack states.
- Those reaction/custom clips explicitly disable Body Dynamics and Attack Weight so a reaction cannot accidentally receive slash/attack twist.
- Hit React and Knockback may use the existing Impact/Compression/Recovery solver through explicit hit impact markers.
- Interact emits an `interact.commit` animation event at the reach/commit moment.

### Contact / Foot Plant behavior

- Dodge temporarily disables runtime Foot Plant so the evade is not cancelled by a planted-foot anchor.
- Hit React and Interact can remain grounded and use Foot Plant.
- Knockback, Death, Faint, and Get Up control their contact state explicitly and avoid locomotion gait overlays.

## V1.8.8 — Core Movement Animation Pack

Movement library remains complete for the current core slice:

- Walk / Run / Sprint / Start / Stop
- Turn L/R
- Strafe L/R
- Jump / Fall / Land
- Crouch Idle / Crouch Walk

## Preserved animation systems

- V1.8.5.2 Twist Isolation and Animation Library restore
- V1.8.5.3 Natural Walk pelvis lateral cap `±0.016m`
- V1.8.6 distinct Walk / Run / Sprint / Start / Stop / Turn / Strafe dynamics
- V1.8.7 Foot Plant + Leg Response with bounded root correction
- V1.8.8 Jump/Fall/Land/Crouch movement states
- rigid `THREE.Group` rig architecture
- 2K PBR quality gate

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → V1.8.9 → SHA-256 gate → Pages`

## Animation roadmap before weapons

- **V1.8.8** — Core Movement Animation Pack
- **V1.8.9** — Core Action / Reaction Pack
- **V1.8.10** — Core Animation QA / transitions: Idle↔Walk↔Run, Jump→Fall→Land, Crouch enter/exit, Dodge recovery, reaction recovery, contact consistency and visual acceptance

Only after V1.8.10 is accepted should Weapon Attachment be reconsidered.

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.
