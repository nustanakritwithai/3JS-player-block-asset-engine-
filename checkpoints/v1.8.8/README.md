# Character Prototype Studio V1.8.8 — Core Movement Animation Pack

V1.8.8 is an incremental extension of V1.8.7. Weapon Attachment is intentionally deferred so the character's main animation set can be completed first.

## Added Animation Library templates

- Turn Left
- Strafe Left
- Jump
- Fall Loop
- Land
- Crouch Idle
- Crouch Walk

Existing Walk, Run, Sprint, Start, Stop, Turn Right, Strafe Right, Attack and Idle templates remain.

## Added Pose Library states

- Jump Takeoff
- Jump Air
- Fall
- Land
- Crouch
- Crouch Step

## Contact / dynamics integration

- Jump Takeoff begins grounded.
- Jump Air and Fall use air contact metadata.
- Fall Loop disables runtime Foot Plant while airborne.
- Land and Crouch re-enable ground contact so V1.8.7 Foot Plant + Leg Response can participate.
- V1.8.6 Locomotion Dynamics is disabled for Jump/Fall/Land/Crouch clips so it does not apply Walk/Run gait yaw to non-gait states.

## Preserved acceptance fixes

- V1.8.5.2 Twist Isolation
- Animation Library remains above Timeline
- V1.8.5.3 Walk visual lateral cap `0.016m`
- V1.8.6 Run/Sprint distinct signatures and locomotion ownership
- V1.8.7 Foot Plant + Leg Response safety limits
- rigid THREE.Group rig

## Next animation-first roadmap

- V1.8.9 Core Action / Reaction Pack
- V1.8.10 Core Animation QA / transitions
- Weapon work remains deferred until these are visually accepted.

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → SHA-256 gate → Pages`
