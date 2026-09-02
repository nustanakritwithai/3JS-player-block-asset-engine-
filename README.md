# 3JS Player Block Asset Engine

Current live checkpoint: **Character Prototype Studio V1.8 — High-Quality Skin & PBR Material System**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current pipeline

CharacterSpec → Blocky/Big-Head Geometry → Rigid Pivot Rig → Pose/Animation → Foot Contact → Weight Transfer → COM/Pelvis → Upper Body Response → Impact/Recovery → Momentum → Equipment Mass → Attack Weight → **High-Quality Skin/PBR** → Runtime Export.

## V1.8

- High-Quality Skin Library
- PBR maps: BaseColor / Normal / Roughness / Metalness / AO / Emissive
- material slots: skin / shirt / pants / accent / boots / hair / eyes
- part-to-material mapping
- UV repeat / offset / rotation / normal strength
- custom high-resolution PBR map import
- Texture Quality Gate: **2048×2048 minimum master source**
- no low-resolution upscaling as a master asset
- runtime-derived 2048 / 1024 / 512 tiers
- starter 2K material pack generated reproducibly during Pages build

## Repository / Pages asset strategy

V1.8 now needs many high-resolution texture files. To keep Git history manageable while still serving real files on GitHub Pages:

1. The exact V1.8 HTML source is stored losslessly in `deploy/source_v1_8/` as gzip+base64 parts.
2. `scripts/build_pages.py` reconstructs the exact HTML during CI.
3. `scripts/generate_textures.py` creates the native 2K PBR starter texture files.
4. `scripts/verify_textures.py` blocks deployment if any generated master texture is below 2048px.
5. GitHub Actions publishes `_site/index.html` plus `assets/textures/*` to Pages.

This means the live site still serves many normal image files from `assets/textures/`; the repository does not need to accumulate large generated binary copies on every checkpoint.

## Development rule

Continue from the latest checkpoint. Do not rebuild the Studio from scratch.

Next planned phase: **V1.9 — Weapon Attachment & Sample Weapon Kit**, reusing the V1.8 PBR pipeline for blade, guard, handle and emissive weapon materials.
