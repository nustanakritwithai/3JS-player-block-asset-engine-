# 3JS Player Block Asset Engine

Current live checkpoint: **Character Prototype Studio V1.8.4.1 — Twist Activation Hotfix**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → High-Quality Skin/PBR → Natural Walk → Full-Body Twist Chain → Action-Specific Dynamics → Action Dynamics Inspector → Runtime Export.

## V1.8.4.1 — Twist Activation Hotfix

The previous V1.8.2–V1.8.4 Body Dynamics engine existed, but the stock `Attack_PoseLibrary` template was created with `runtime.motionClass = "custom"`. Body Dynamics intentionally runs only for `motionClass === "action"`, so the visible twist response was being bypassed for the stock attack template.

V1.8.4.1 fixes the activation path:

- Pose Library templates now get the correct runtime class at creation time
- Attack → `action`
- Walk → `walk`
- Run → `run`
- Idle → `idle`
- old saved Pose Library templates incorrectly stored as `custom` are migrated
- imported Pose Library templates are repaired by `normalizeClip()`
- Attack 4-Key gets explicit action timing + Natural Slash Body Dynamics
- Body Dynamics UI displays `BYPASS` when the current clip is not an action
- new **Twist Demo** button creates/selects a valid attack clip and plays the Pelvis → Chest → Shoulder twist chain immediately

## Recent animation development

- **V1.8.1** — Natural Walk tuning; reduced excessive left/right pelvis sway
- **V1.8.2** — Full-Body Twist Chain with Pelvis lead, Chest/Shoulder/Arm lag and head stabilization
- **V1.8.3** — Action-Specific Dynamics for Punch, Slash, Heavy Slash, Thrust, Kick and Dodge
- **V1.8.4** — Action Dynamics Inspector / kinetic-chain QA
- **V1.8.4.1** — fixed stock animation template runtime classification so Body Dynamics is actually visible in playback

## High-quality texture rule

Stylized High Quality character skins use high-resolution master assets. The Pages workflow generates the starter PBR texture pack natively at 2048×2048 and blocks deployment if the texture quality gate fails.

## Repository / Pages strategy

The exact V1.8.4 HTML base is stored losslessly in `deploy/source_v1_8_4/parts/` as XZ + Base64 parts. `scripts/patch_v1_8_4_1.py` applies the verified hotfix during CI. `scripts/build_pages.py` reconstructs the base, applies the patch, verifies the final V1.8.4.1 SHA-256, and publishes it with generated 2K PBR textures.

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.

Current live hotfix: **V1.8.4.1**.
