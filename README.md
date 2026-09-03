# 3JS Player Block Asset Engine

Current live checkpoint: **Character Prototype Studio V1.8.5.3 — Walk Pelvis Translation Hotfix**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → High-Quality Skin/PBR → Natural Walk → Full-Body Twist Chain → Action-Specific Dynamics → Action Dynamics Inspector → Dynamics Auto-Tuner → Runtime Export.

## V1.8.5.3 — Walk Pelvis Translation Hotfix

V1.8.5.3 reduces excessive visible left/right hip sliding during Walk without weakening Weight Transfer or COM truth.

The issue was two separate lateral motion paths: procedural Walk applied `pelvisShift` directly to `pelvis.position.x`, while authored Walk clips could receive additional pelvis translation from the Weight/Pelvis Solver. V1.8.1 reduced sway, but the visual mapping was still too large.

Natural Walk now uses:

- procedural pelvisShift: **0.028m → 0.014m**
- authored/game-runtime Walk visual pelvis cap: **±0.016m**
- post-smoothing Walk clamp so previous solver history cannot restore a larger offset
- COM correction remains fully calculated for balance/QA
- pelvis twist, hip drop and chest counter-rotation remain intact
- Run is intentionally left unchanged for V1.8.6 Natural Locomotion Dynamics

Preset lateral tuning:

- Natural: `0.014m`, cap `0.016m`
- Subtle: `0.010m`, cap `0.012m`
- Stylized: `0.020m`, cap `0.024m`

Existing saves using the exact V1.8.1 Natural default `0.028m` migrate to `0.014m`; custom values are preserved.

## V1.8.5.2 — Twist Isolation + Animation Library Restore

Twist Demo is a transient isolation mode using neutral authored keyframes and Body Dynamics as the only action solver. It never enters `CharacterSpec.animations`, keeps the Animation Library clean, and preserves the visible Pelvis → Chest → Shoulder chain.

The existing Walk / Run / Attack / Idle **Animation Library remains at the top of the Anim tab** for mobile visibility.

## V1.8.5 — Dynamics Auto-Tuner

V1.8.5 converts Action Dynamics Inspector findings into reversible Body Dynamics modifier proposals with Conservative / Natural / Strong Fix modes, Preview before Apply, Undo support, stale-proposal protection and authored-keyframe locking.

## Build chain

The exact V1.8.4 HTML base remains stored losslessly in `deploy/source_v1_8_4/parts/`.

CI builds:

`V1.8.4 source` → `patch_v1_8_4_1.py` → `patch_v1_8_5.py` → `patch_v1_8_5_guard.py` → `patch_v1_8_5_1.py` → `patch_v1_8_5_2.py` → `patch_v1_8_5_3.py` → SHA-256 verification → `_site/index.html`

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
- **V1.8.5.3** — Walk Pelvis Translation Hotfix

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.

Next planned version after live Walk acceptance: **V1.8.6 — Natural Locomotion Dynamics**.
