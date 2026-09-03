# 3JS Player Block Asset Engine

Current live checkpoint: **Character Prototype Studio V1.8.5.1 — Twist Visual Recovery Hotfix**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → High-Quality Skin/PBR → Natural Walk → Full-Body Twist Chain → Action-Specific Dynamics → Action Dynamics Inspector → Dynamics Auto-Tuner → Runtime Export.

## V1.8.5.1 — Twist Visual Recovery Hotfix

The V1.8.4.1 activation fix corrected the stock Attack template `motionClass`, but the Twist Demo could still reuse any currently selected action clip. A saved or Auto-Tuned action could therefore remain technically active while its current shares/timing produced little visible twist.

V1.8.5.1 makes the demo deterministic:

- Twist Demo uses a dedicated `Twist_Demo_V1_8_5_1` clip instead of trusting the current action clip
- locks action classification, Slash timing and a known-good Body Dynamics profile
- resets the character root orientation and switches to ISO / 3-quarter camera before playback
- runs a full-clip visibility preflight before Play
- requires peak solver output of at least Pelvis 6°, Chest 10°, Shoulder 14°
- keeps the generated demo separate from authored animation keyframes
- preserves the V1.8.5 Auto-Tuner and its keyframe-lock / stale-proposal guards

The locked demo profile is expected to produce approximately Pelvis ~12°, Chest ~24° and Shoulder ~36° while remaining inside Natural soft limits.

## V1.8.5 — Dynamics Auto-Tuner

V1.8.5 converts Action Dynamics Inspector findings into reversible Body Dynamics modifier proposals.

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

`V1.8.4 source` → `patch_v1_8_4_1.py` → `patch_v1_8_5.py` → `patch_v1_8_5_guard.py` → `patch_v1_8_5_1.py` → SHA-256 verification → `_site/index.html`

High-quality starter PBR textures are generated natively at 2048×2048 and verified before deployment.

## Recent animation development

- **V1.8.1** — Natural Walk tuning
- **V1.8.2** — Full-Body Twist Chain
- **V1.8.3** — Action-Specific Dynamics
- **V1.8.4** — Action Dynamics Inspector
- **V1.8.4.1** — Twist Activation Hotfix
- **V1.8.5** — Dynamics Auto-Tuner
- **V1.8.5.1** — Twist Visual Recovery Hotfix

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.

V1.8.6 remains blocked until the live V1.8.5.1 Twist Demo receives actual viewport visual acceptance.
