# Character Prototype Studio V1.8.9 — Core Action / Reaction Pack

V1.8.9 is an incremental extension of V1.8.8. Weapon Attachment remains deferred while the non-weapon core animation set is completed.

## Added Animation Library templates

- Dodge Right
- Dodge Left
- Hit React
- Knockback
- Get Up
- Death
- Faint
- Interact

## Added Pose Library states

- Dodge Lean
- Hit React
- Knockback
- Down / Back
- Faint
- Interact Reach

## Ownership rules

### Dodge

Dodge remains an `action` clip and explicitly uses Body Dynamics `actionType = dodge`.

- Body Dynamics owns evade lean/lateral action signature.
- Attack Weight is disabled.
- Impact solver is disabled.
- Runtime Foot Plant is disabled during the evade so the plant anchor does not cancel visible dodge displacement.

### Reactions / utility actions

Hit React, Knockback, Get Up, Death, Faint, and Interact are authored `custom` states.

They explicitly disable:

- locomotion dynamics
- Body Dynamics
- Attack Weight

This prevents reaction clips from inheriting slash/attack body twist merely because a clip name contains terms such as `hit`.

Hit React and Knockback retain explicit hit `impactMarkers` so the Impact/Compression/Recovery solver can add bounded recoil/compression.

Interact emits `interact.commit` at the authored reach/commit moment.

## Contact behavior

- Dodge includes support → air → landing contact phases but Foot Plant stays disabled during the evade.
- Hit React remains grounded and may use Foot Plant.
- Knockback temporarily releases plant ownership during displacement.
- Death/Faint settle into non-locomotion states.
- Get Up moves from down → supported recovery → crouch → stand.
- Interact stays grounded and may use Foot Plant.

## Preserved acceptance rules

- Animation Library remains above Timeline.
- V1.8.5.2 Twist Isolation remains available.
- V1.8.5.3 Walk visual lateral cap remains `0.016m`.
- V1.8.6 Run/Sprint signatures remain distinct.
- V1.8.7 Foot Plant safety/root limits remain present.
- V1.8.8 Jump/Fall/Land/Crouch templates remain present.
- rigid `THREE.Group` rig remains unchanged.
- 2K PBR texture gate and module JavaScript syntax gate remain required.

## Next

**V1.8.10 — Core Animation QA / Transitions** should connect and validate the core set before any Weapon Attachment work.

Target transition groups:

- Idle ↔ Walk ↔ Run ↔ Sprint
- Start / Stop
- Turn / Strafe recovery
- Jump → Fall → Land → Idle/Run
- Crouch enter / idle / walk / exit
- Dodge → recovery
- Hit / Knockback → recovery
- Get Up → Idle
- Death/Faint terminal behavior
- Interact → Idle

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → V1.8.9 → SHA-256 gate → Pages`
