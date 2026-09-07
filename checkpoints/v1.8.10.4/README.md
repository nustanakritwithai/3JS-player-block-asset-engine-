# Character Prototype Studio V1.8.10.4 — Baseball Throw Motion Hotfix

V1.8.10.4 is an incremental animation hotfix on top of V1.8.10.3.

## Visual issue

Capture Throw looked like a side-arm / frisbee throw because the authored arm path, Attack Weight style and Body Dynamics all emphasized horizontal sweep.

## Corrected throw signature

`Back-foot load → high elbow / cocked arm → front-foot step → elbow lead → overhand release → wrist snap → cross-body follow-through → recovery`

## Changes

- `attackProfile.style = overhead` for Monster Ball throws.
- reduced throw horizontal twist and side lean.
- increased forward drive and arm contribution.
- wind-up elbow is higher and more deeply flexed.
- release arm extends above shoulder level.
- follow-through crosses the torso.
- metadata: `throwStyle = overhand-baseball`.

## Preserved

- Quick / Standard / Power / Summon release timings
- `ball.release`, `capture.throw`, `monster.summon`
- V1.8.10.3 clip-reference boot fix
- V1.8.10.2 core-first renderer fallback
- locomotion, Foot Plant, Jump/Crouch, Dodge/Reaction, Twist
- rigid THREE.Group rig
- 2K PBR gate

## Acceptance

The standard Capture Throw must visually read like throwing a baseball overhand and must not resemble throwing a frisbee/disc.
