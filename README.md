# 3JS Player Block Asset Engine

Current live checkpoint: **Character Prototype Studio V1.8.5.2 — Twist Isolation + Animation Library Restore**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → High-Quality Skin/PBR → Natural Walk → Full-Body Twist Chain → Action-Specific Dynamics → Action Dynamics Inspector → Dynamics Auto-Tuner → Runtime Export.

## V1.8.5.2 — Twist Isolation + Animation Library Restore

This hotfix responds to the live report that the character still did not visibly twist and that the Animation Library appeared to be gone.

The previous Twist Demo still used authored Attack keyframes that already contained pelvis/chest yaw. Runtime Body Dynamics was added on top, so authored yaw and runtime yaw could partially cancel on the same joints even though Inspector metrics showed large angles.

V1.8.5.2 changes Twist Demo into a **transient isolation mode**:

- neutral authored keyframes only
- Body Dynamics is the only action solver applied during the demo
- the demo is never added to `CharacterSpec.animations`
- legacy generated Twist Demo clips are purged from saved animation lists
- the demo loops until `Stop Twist Demo` is pressed
- ISO / 3-quarter camera and neutral root yaw are used for readability
- preflight requires an ordered visible Pelvis → Chest → Shoulder chain

Locked isolation output is approximately:

- Pelvis ~15.4° @ 1.34s
- Chest ~30.1° @ 1.44s
- Shoulder ~46.1° @ 1.50s

The existing Walk / Run / Attack / Idle **Animation Library is restored to the top of the Anim tab** so it remains visible on mobile.

## V1.8.5 — Dynamics Auto-Tuner

V1.8.5 converts Action Dynamics Inspector findings into reversible Body Dynamics modifier proposals with Conservative / Natural / Strong Fix modes, Preview before Apply, Undo support, stale-proposal protection and authored-keyframe locking.

## Build chain

The exact V1.8.4 HTML base remains stored losslessly in `deploy/source_v1_8_4/parts/`.

CI builds:

`V1.8.4 source` → `patch_v1_8_4_1.py` → `patch_v1_8_5.py` → `patch_v1_8_5_guard.py` → `patch_v1_8_5_1.py` → `patch_v1_8_5_2.py` → SHA-256 verification → `_site/index.html`

High-quality starter PBR textures are generated natively at 2048×2048 and verified before deployment.

## Recent animation development

- **V1.8.1** — Natural Walk tuning
- **V1.8.2** — Full-Body Twist Chain
- **V1.8.3** — Action-Specific Dynamics
- **V1.8.4** — Action Dynamics Inspector
- **V1.8.4.1** — Twist Activation Hotfix
- **V1.8.5** — Dynamics Auto-Tuner
- **V1.8.5.1** — Twist Visual Recovery Hotfix
- **V1.8.5.2** — Twist Isolation + Animation Library Restore

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.

V1.8.6 remains blocked until the live V1.8.5.2 viewport receives explicit visual acceptance.
