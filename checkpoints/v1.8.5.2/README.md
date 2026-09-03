# Character Prototype Studio V1.8.5.2 — Twist Isolation + Animation Library Restore

V1.8.5.2 is an incremental hotfix on top of V1.8.5.1. It addresses two user-visible regressions: the viewport still did not show a clear Pelvis → Chest → Shoulder twist, and the Animation Library became difficult to find / polluted by the generated Twist Demo clip.

## Twist root cause

The V1.8.5.1 demo still used authored Attack keyframes that already contained pelvis/chest yaw. Body Dynamics then added runtime yaw on top. Because the authored pose and runtime solver can rotate the same joints in opposite directions, part of the pelvis motion can cancel even though the solver metrics report large angles.

## V1.8.5.2 fix

Twist Demo is now a transient isolation mode:

- it is not inserted into `CharacterSpec.animations`
- it uses neutral authored keyframes
- Body Dynamics is the only action solver applied during the demo
- Attack Weight, Impact and authored Attack yaw do not participate in the isolation playback
- the demo loops until the user presses Stop Twist Demo
- root yaw is neutralized and the camera uses the ISO / 3-quarter view
- preflight verifies visible ordered peaks before playback

Expected isolated peaks from the locked profile:

- Pelvis ~15.4° around 1.34s
- Chest ~30.1° around 1.44s
- Shoulder ~46.1° around 1.50s

The timing order must remain Pelvis → Chest → Shoulder.

## Animation Library restore

The existing Walk / Run / Attack / Idle template library is moved to the top of the Anim tab for mobile visibility. V1.8.5.2 also purges legacy generated Twist Demo clips from saved animation lists. User-authored animation clips are preserved.

## Development gate

V1.8.6 remains blocked until the user confirms the live V1.8.5.2 viewport visibly twists.

## Build chain

`V1.8.4 source → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → SHA-256 gate → Pages`
