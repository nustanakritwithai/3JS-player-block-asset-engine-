# Character Prototype Studio V1.8.6 — Natural Locomotion Dynamics

V1.8.6 is an incremental extension of V1.8.5.3. It keeps the rigid `THREE.Group` rig, preserves the V1.8.5.2 Twist Isolation and Animation Library restore, and preserves the V1.8.5.3 Walk pelvis translation cap.

## Goal

Give locomotion a dedicated body-dynamics layer so Walk, Run, Sprint, Start, Stop, Turn and Strafe have different physical signatures instead of sharing one speed-scaled gait.

## Locomotion signatures

- Walk: restrained lateral travel, light forward lean, pelvis yaw and chest counter-rotation.
- Run: stronger stride/knee/arm drive, stronger lean, shorter contact and a flight phase.
- Sprint: higher cadence and impulse than Run with a much deeper forward lean.
- Start: progressive acceleration and forward-lean ramp.
- Stop: progressive drive reduction and braking lean.
- Turn: larger pelvis/root yaw and directional body lean.
- Strafe: lateral stepping and side lean without increasing Walk hip sway.

## Solver ownership

- Weight / COM owns support truth, lateral weight response, hip drop and compression.
- Locomotion Dynamics owns gait pelvis yaw, chest counter-yaw, forward/side lean, shoulder follow and head stabilization.
- Action Body Dynamics remains action-only and owns action core twist.
- Weight/Pelvis core yaw is zeroed when Locomotion Dynamics owns the locomotion clip.

## Runtime/export

Animation clips carry `locomotionDynamics` with mode, direction, intensity and baked state. Runtime export includes that contract and the standalone generated runtime applies the equivalent locomotion solver/ownership rules.

## Preserved acceptance fixes

- V1.8.5.2 transient Twist Isolation remains present.
- Animation Library stays above Timeline on mobile.
- V1.8.5.3 Natural Walk remains `pelvisShift = 0.014m` with visual cap `±0.016m`.
- COM correction remains fully calculated for balance and QA.

## Development gate

V1.8.7 Foot Plant + Leg Response should begin only after live acceptance of the V1.8.6 locomotion signatures.

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → SHA-256 gate → Pages`
