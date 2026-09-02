# High-Quality Skin & PBR System — V1.8

## Product requirement

Do not use blurred, pixelated, stretched or low-resolution images as the master character skin.

The quality gate checks source resolution before a custom texture is accepted.

## Skin Asset Contract

A skin consists of:
- material slots
- PBR maps
- UV transforms
- part-to-slot assignments
- master source resolution
- runtime resolution policy
- quality status

## PBR material model

The Studio uses `THREE.MeshStandardMaterial` with:
- `map`
- `normalMap`
- `roughnessMap`
- `metalnessMap`
- `aoMap`
- `emissiveMap`

Box geometries receive `uv2` so AO maps can work.

## UV controls

Each slot exposes:
- repeat X/Y
- offset X/Y
- texture rotation
- normal strength

## Part mapping

Logical character groups are mapped to slots:
Head/Neck, Hair, Eyes, Torso, Upper Arms, Forearms/Hands,
Pelvis/Legs, Feet/Boots and Accent pieces.

## Quality tiers

High-resolution source is preserved.
Runtime textures are derived at 2048 / 1024 / 512.

## Starter textures

Bundled files are generated directly at 2048×2048.
No 512→2048 enlargement is used.

## Future extension

V1.9 Weapon Attachment should reuse the same PBR asset pipeline for:
Blade → steel
Guard → gold/steel
Handle → leather
Gem → emissive
