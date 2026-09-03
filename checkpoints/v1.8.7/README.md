# Character Prototype Studio V1.8.7 — Foot Plant + Leg Response

V1.8.7 is an incremental extension of V1.8.6. It preserves the rigid `THREE.Group` rig, V1.8.5.2 Twist Isolation, V1.8.5.3 Walk lateral cap and V1.8.6 locomotion ownership.

## Goal

Convert foot contact from marker/analysis data into a live support-leg response layer during procedural preview, authored animation playback and standalone runtime playback.

## Runtime chain

`Contact → Plant Anchor → Root micro-compensation → Support Hip/Knee → Ankle flatten/roll → Swing Toe Lift → Landing compression`

## Ownership

- Weight / COM owns pelvis balance truth, lateral shift, hip drop and compression.
- Locomotion Dynamics owns gait pelvis yaw, chest counter-yaw and gait lean.
- Foot Plant + Leg Response owns plant anchors, bounded root X/Z micro-correction and distal support-leg response.
- Action Body Dynamics remains action-only.

## Default tuning

- plant strength: `0.92`
- root compensation: `0.45`
- max root correction: `0.028m`
- support knee: `7°`
- landing compression: `5°`
- support hip pitch: `2°`
- swing toe lift: `12°`
- ankle flatten: `0.82`
- ankle roll flatten: `0.70`

## Joint safety limits

Runtime response clamps the rigid pivots approximately to:

- hip X `-108° … 74°`
- knee X `0° … 142°`
- ankle X `-42° … 42°`
- ankle Z `-22° … 22°`

## Procedural preview

Procedural locomotion performs a contact pass to capture stance anchors, applies support-leg response and root micro-compensation, then measures contact/slide again. The displayed max-slide metric therefore reflects the post-plant result rather than the uncorrected pose.

## Authored animation

Each clip has a `footPlant` contract with enabled/strength/baked state. Contact tags and Weight Transfer drive support-leg load during playback. Manual scrubbing resets the runtime anchor state so the user can inspect a deterministic frame.

V0.7 Foot Lock Assist is retained as a separate offline keyframe tool.

## Runtime/export

The runtime manifest includes Foot Plant settings, per-clip Foot Plant data, contact settings and keyframes required for contact lookup. The generated standalone runtime keeps its own plant-anchor state and applies Foot Plant after the other animation/dynamics modifiers.

## Preserved acceptance rules

- Animation Library remains above Timeline.
- V1.8.5.2 Twist Isolation stays available.
- Natural Walk keeps `pelvisShift = 0.014m` and `walkVisualShiftCap = 0.016m`.
- V1.8.6 Run/Sprint signatures and flight contact rules remain intact.
- 2K PBR quality gate remains required.
- module JavaScript syntax and final HTML SHA-256 remain deployment gates.

## Development gate

Proceed to **V1.9 — Weapon Attachment** only after live acceptance confirms that planted feet look more stable without introducing excessive root/body drift or unnatural knee/ankle deformation.

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → SHA-256 gate → Pages`
