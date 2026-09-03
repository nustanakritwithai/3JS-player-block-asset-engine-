# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.6 — Natural Locomotion Dynamics**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Natural Locomotion Dynamics → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → High-Quality Skin/PBR → Full-Body Twist Chain → Action-Specific Dynamics → Action Dynamics Inspector → Dynamics Auto-Tuner → Runtime Export.

## V1.8.6 — Natural Locomotion Dynamics

V1.8.6 gives locomotion its own dynamics layer instead of treating every gait as a speed-scaled Walk.

Supported signatures:

- Walk — restrained lateral travel, light forward lean, pelvis yaw with chest counter-rotation
- Run — stronger stride/knee/arm drive, stronger lean, shorter ground contact and an explicit flight phase
- Sprint — higher cadence/impulse, deeper forward lean and stronger arm/knee drive than Run
- Start / Accelerate — progressive drive and forward-lean ramp
- Stop / Brake — progressive drive reduction and braking lean
- Turn — stronger pelvis/root yaw with directional body lean
- Strafe — lateral stepping and side lean without restoring excessive Walk hip sway

### Dynamics ownership

- Weight / COM owns balance truth, support, lateral shift, hip drop and compression.
- Locomotion Dynamics owns locomotion core pelvis yaw, chest counter-yaw, gait lean, shoulder follow and head stabilization.
- Action Body Dynamics remains the core action-twist owner for attacks.
- Weight/Pelvis Solver yields its core yaw whenever Locomotion Dynamics owns the current locomotion clip.

This prevents multiple solvers from directly competing over pelvis yaw.

### Runtime parity

The `locomotionDynamics` contract is included in animation/runtime export. The standalone generated runtime applies the same locomotion ownership layer, so the Studio preview is not a Studio-only effect.

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

`V1.8.4 source` → `V1.8.4.1` → `V1.8.5` → `V1.8.5 guard` → `V1.8.5.1` → `V1.8.5.2` → `V1.8.5.3` → `V1.8.6` → SHA-256 verification → `_site/index.html`

The Pages gate also checks the 2K PBR texture rule, Animation Library placement, V1.8.5.2 Twist Isolation preservation, V1.8.5.3 Walk lateral cap, V1.8.6 locomotion signatures/ownership and module JavaScript syntax.

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

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.

Next planned version after live locomotion acceptance: **V1.8.7 — Foot Plant + Leg Response**.
