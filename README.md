# 3JS Player Block Asset Engine

Current live checkpoint: **Character Prototype Studio V1.8.4 — Action Dynamics Inspector**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → High-Quality Skin/PBR → **Natural Walk → Full-Body Twist Chain → Action-Specific Dynamics → Action Dynamics Inspector** → Runtime Export.

## V1.8.4

V1.8.4 continues directly from V1.8.3 and adds production QA for action-body dynamics:

- Pelvis → Chest → Shoulder → Arm kinetic-chain peak timing
- angular velocity / angular acceleration checks
- abrupt high-speed reversal detection
- head stabilization / head-follow ratio
- natural soft-range pressure
- foot-support and Center-of-Mass conflict checks
- Kick opposite-support-foot checks
- recovery residual checks
- Thrust and Dodge action-specific checks
- clickable P/C/S/A peak timeline and issue timestamps
- Normal / Strict / Lenient QA sensitivity
- persisted `clip.bodyDynamics.qa` results with `PASS / BLOCKED / STALE`
- validation warns on missing/stale Inspector results and blocks current hard QA issues

## Recent animation development

- **V1.8.1** — Natural Walk tuning; reduced excessive left/right pelvis sway
- **V1.8.2** — Full-Body Twist Chain with Pelvis lead, Chest/Shoulder/Arm lag and head stabilization
- **V1.8.3** — Action-Specific Dynamics for Punch, Slash, Heavy Slash, Thrust, Kick and Dodge
- **V1.8.4** — Action Dynamics Inspector / kinetic-chain QA

## High-quality texture rule

Stylized High Quality character skins use high-resolution master assets. The Pages workflow generates the starter PBR texture pack natively at 2048×2048 and blocks deployment if the texture quality gate fails.

## Repository / Pages strategy

The exact V1.8.4 HTML is stored losslessly in `deploy/source_v1_8_4/parts/` as XZ + Base64 parts. `scripts/build_pages.py` reconstructs it during CI and validates SHA-256 before publishing. High-resolution PBR starter textures are generated into `assets/textures/` during the Pages build.

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.

The current source checkpoint is `checkpoints/v1.8.4/`.
