# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.7 — Foot Plant + Leg Response**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Natural Locomotion Dynamics → Foot Plant + Leg Response → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → High-Quality Skin/PBR → Full-Body Twist Chain → Action-Specific Dynamics → Action Dynamics Inspector → Dynamics Auto-Tuner → Runtime Export.

## V1.8.7 — Foot Plant + Leg Response

V1.8.7 turns foot contact from a marker/QA concept into a live playback response layer for the current rigid `THREE.Group` rig.

During procedural and authored locomotion playback the runtime now uses:

`Contact → Plant Anchor → Root micro-compensation → Support Hip/Knee → Ankle flatten/roll → Swing Toe Lift → Landing compression`

### What it changes

- stance foot captures a world-space plant anchor when contact begins
- small root X/Z compensation reduces visible planted-foot drift
- support knee flexes under load and gets a short landing-compression pulse
- support hip receives a small pitch response without taking pelvis-balance ownership
- ankle pitch/roll counteracts accumulated leg rotation so the planted foot reads flatter
- swing foot gets toe lift for clearer ground clearance
- slide metrics are measured after the plant correction instead of before it
- authored clips can enable/disable runtime Foot Plant per clip
- V0.7 Foot Lock Assist remains available as an optional offline keyframe compensation tool

### Safety / visual limits

Default runtime tuning:

- Plant strength: `0.92`
- Root micro-compensation: `0.45`
- Maximum root correction: `0.028m`
- Support knee response: `7°`
- Landing compression: `5°`
- Swing toe lift: `12°`

The rigid rig also soft-clamps the affected joints:

- hip X: about `-108° … 74°`
- knee X: `0° … 142°`
- ankle X: `-42° … 42°`
- ankle Z: `-22° … 22°`

### Solver ownership

- Weight / COM still owns pelvis balance truth, lateral shift, hip drop and compression.
- V1.8.6 Locomotion Dynamics still owns gait pelvis yaw, chest counter-yaw and gait lean.
- V1.8.7 Foot Plant owns contact anchoring and distal support-leg response only.
- Action Body Dynamics remains action-only and owns attack core twist.

This keeps the new plant solver from reintroducing the excessive Walk pelvis sway fixed in V1.8.5.3.

### Runtime parity

The runtime manifest now carries the Foot Plant contract, contact settings and authored contact keyframes. The standalone generated animation runtime applies the same support-leg response and bounded root micro-compensation after the other animation/dynamics layers.

## V1.8.6 — Natural Locomotion Dynamics

Locomotion signatures remain distinct for Walk, Run, Sprint, Start, Stop, Turn and Strafe. Run/Sprint retain their shorter contact windows / flight phase and are not speed-scaled Walks.

## V1.8.5.3 — Walk Pelvis Translation Hotfix

Natural Walk keeps the reduced visible lateral mapping:

- procedural pelvisShift: **0.014m**
- authored/game-runtime Walk visual pelvis cap: **±0.016m**
- COM correction remains fully calculated for balance/QA

## V1.8.5.2 — Twist Isolation + Animation Library Restore

Twist Demo remains a transient isolation mode and does not enter `CharacterSpec.animations`. The Animation Library remains at the top of the Anim tab.

## Build chain

The exact V1.8.4 HTML base remains stored losslessly in `deploy/source_v1_8_4/parts/`.

CI builds:

`V1.8.4 source` → `V1.8.4.1` → `V1.8.5` → `V1.8.5 guard` → `V1.8.5.1` → `V1.8.5.2` → `V1.8.5.3` → `V1.8.6` → `V1.8.7` → SHA-256 verification → `_site/index.html`

The Pages gate checks the 2K PBR texture rule, Animation Library placement, Twist Isolation preservation, Walk lateral cap, V1.8.6 locomotion ownership/signatures, V1.8.7 plant/root/joint safety tokens and module JavaScript syntax.

## Recent animation development

- **V1.8.1** — Natural Walk tuning
- **V1.8.2** — Full-Body Twist Chain
- **V1.8.3** — Action-Specific Dynamics
- **V1.8.4** — Action Dynamics Inspector
- **V1.8.4.1** — Twist Activation Hotfix
- **V1.8.5** — Dynamics Auto-Tuner
- **V1.8.5.1** — Twist Visual Recovery Hotfix
- **V1.8.5.2** — Twist Isolation + Animation Library Restore
- **V1.8.5.3** — Walk Pelvis Translation Hotfix
- **V1.8.6** — Natural Locomotion Dynamics
- **V1.8.7** — Foot Plant + Leg Response

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.

Next planned version after live Foot Plant acceptance: **V1.9 — Weapon Attachment**.
