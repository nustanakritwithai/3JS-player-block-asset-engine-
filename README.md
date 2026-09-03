# 3JS Player Block Asset Engine

Current live checkpoint: **Character Prototype Studio V1.8.5 — Dynamics Auto-Tuner**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → High-Quality Skin/PBR → Natural Walk → Full-Body Twist Chain → Action-Specific Dynamics → Action Dynamics Inspector → Dynamics Auto-Tuner → Runtime Export.

## V1.8.5 — Dynamics Auto-Tuner

V1.8.5 continues directly from V1.8.4.1. It converts Action Dynamics Inspector findings into reversible Body Dynamics modifier proposals.

Workflow:

- Run Action Dynamics Inspector
- choose Conservative / Natural / Strong Fix
- Analyze & Propose
- review parameter deltas and predicted hard/warn counts
- Preview Proposed Fix on the character
- Apply through command history so Undo works
- Inspector reruns automatically after Apply

The tuner changes only Body Dynamics modifier parameters. Authored animation keyframes remain locked and are verified unchanged during Apply. Stale proposals are rejected if the Body Dynamics profile changes after Analyze.

## Build chain

The exact V1.8.4 HTML base remains stored losslessly in `deploy/source_v1_8_4/parts/`.

CI builds:

`V1.8.4 source` → `patch_v1_8_4_1.py` → `patch_v1_8_5.py` → `patch_v1_8_5_guard.py` → SHA-256 verification → `_site/index.html`

High-quality starter PBR textures are generated natively at 2048×2048 and verified before deployment.

## Recent animation development

- **V1.8.1** — Natural Walk tuning
- **V1.8.2** — Full-Body Twist Chain
- **V1.8.3** — Action-Specific Dynamics
- **V1.8.4** — Action Dynamics Inspector
- **V1.8.4.1** — Twist Activation Hotfix
- **V1.8.5** — Dynamics Auto-Tuner

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.
