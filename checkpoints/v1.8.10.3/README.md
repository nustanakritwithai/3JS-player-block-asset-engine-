# Character Prototype Studio V1.8.10.3 — clip Reference Hotfix

V1.8.10.3 is an incremental hotfix on top of V1.8.10.2.

## Live regression

The Studio displayed:

`Character renderer failed to start`

with:

`clip is not defined | recovery: clip is not defined`

## Root cause

`renderContactAnalysis()` used `clip.footPlant` without declaring `clip`.

Because `renderContactAnalysis()` is reached during `initUI()`, both normal boot and recovery failed before the character could finish rendering.

## Fix

- declare `const clip = selectedAnimationClip()` inside `renderContactAnalysis()`
- reuse that clip for `contactStateAtTime()`
- make the Foot Plant toggle read null-safe with `clip?.footPlant?.enabled !== false`

## Regression gate

CI now rejects the old expression:

`checked=clip.footPlant?.enabled!==false`

and requires the scoped/null-safe version.

## Preserved

- V1.8.10 Monster Ball Action Pack
- V1.8.10.2 core-first Three.js boot and optional editor-control fallbacks
- Walk/Run/Sprint, Foot Plant, Jump/Crouch, Dodge/Reaction and Twist systems
- rigid THREE.Group rig
- 2K PBR gate

## Next

V1.8.11 remains blocked until the user confirms the main character is visible again on the live page.
