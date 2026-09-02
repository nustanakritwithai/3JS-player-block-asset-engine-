# Character Prototype Studio V1.8 — High-Quality Skin & PBR Material System

V1.8 is patched directly on top of V1.7.

## High-Quality texture rule

Stylized High Quality character skins must start from high-resolution master textures.

- Master minimum: 2048×2048
- Hero/large atlas target: 4096×4096
- Low-resolution sources are rejected by the Texture Quality Gate
- Pixel-art mode is not accepted for this product direction
- Mobile 1024/512 textures are runtime derivatives, never the source master

## PBR stack
Supported per material slot:
- BaseColor
- Normal
- Roughness
- Metalness
- AO
- Emissive

## Material slots
- skin
- shirt
- pants
- accent
- boots
- hair
- eyes

## Part Mapping
Character mesh groups can be routed to material slots without rebuilding geometry.

## Starter pack
The bundled starter pack is generated natively at 2048×2048:
- warm skin
- navy cloth
- red cloth
- brown leather
- steel
- gold
- dark hair
- green monster scales
- cyan emissive

These are not upscaled low-resolution textures.

## Presets
- Pirate Hero — High
- Adventure Hero — High
- Night Hero — High
- Monster Green — High

## Runtime optimization
The master assets stay 2K.
Runtime can derive:
- 2048 High
- 1024 Medium
- 512 Low

Downsampling happens from the high-resolution source with high-quality canvas filtering.

## Custom import
PNG/JPEG/WebP maps can be imported.
Any source below the configured 2K master gate is rejected.

## Export
Skin metadata is included in runtime exports and has a dedicated Skin Manifest.
