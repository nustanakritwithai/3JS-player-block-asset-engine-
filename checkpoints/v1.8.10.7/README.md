# V1.8.10.7 — Tripo Primary Rigid Adapter

## Decision

Use the imported Tripo mesh `5889e73e` as the Character Studio primary visual source.

Source asset:

`assets/imports/tripo_5889e73e/tripo_5889e73e.glb`

Source facts retained from import acceptance:

- glTF 2.0 binary
- static PBR mesh
- 34,566 vertices
- 46,897 triangles
- no skin
- no source animation

## Architecture decision

Do not add a second skeletal animation stack and do not discard the existing rigid rig.

Compile the static GLB at build time into `studio-rigid-glb-v1`, partitioning complete source triangles into body regions attached to the existing `THREE.Group` pivots.

This keeps all accepted animation/solver/socket code operating on the same joint names.

## Runtime primary/fallback order

1. `tripo-5889e73e-rigid-v1`
2. `blue-explorer-primary-v1`
3. Legacy/Debug

## Required joints

`pelvis`, `chest`, `neck`, `head`, `shoulderL/R`, `elbowL/R`, `wristL/R`, `hipL/R`, `kneeL/R`, `ankleL/R`.

## Required compatibility

- canonical Studio solver runtime unchanged
- foot socket parity preserved
- authoritative hand/weapon sockets preserved
- existing animation clips continue to target the same joint API
- Pocket Studio package remains presentation-only
- imported PBR materials/textures remain visual data only

## Acceptance

The build must parse the actual GLB and verify all 46,897 triangles survive rigid partitioning. Empty core body/limb regions are a hard failure. Blue Explorer fallback and solver runtime syntax are regression-gated.
