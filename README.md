# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.10.7 — Tripo Primary Rigid Adapter**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current primary character

**Tripo 5889e73e** is the selected primary visual source for the Character Engine.

Source:

`assets/imports/tripo_5889e73e/tripo_5889e73e.glb`

The original GLB is a static PBR glTF 2.0 mesh with **34,566 vertices / 46,897 triangles** and no authored skin/animation. V1.8.10.7 therefore does not pretend that the source is already rigged. Instead, the build pipeline compiles it into a deterministic rigid-pivot representation compatible with the existing Studio animation system.

## V1.8.10.7 — Tripo Primary Rigid Adapter

Build-time compiler:

`scripts/compile_tripo_rigid.py`

The compiler:

- reads the actual GLB 2.0 binary at build time
- resolves scene/node transforms
- preserves POSITION / NORMAL / TEXCOORD_0 data
- preserves triangle/material assignment
- extracts embedded PBR images when present
- normalizes the source to the Character Engine scale
- detects an arms-down vs spread source pose
- partitions complete triangles into rigid body regions
- emits `studio-rigid-glb-v1`

Runtime descriptor:

`assets/runtime/tripo_5889e73e/rigid-model.json`

Rigid regions:

- pelvis / chest / neck / head
- upper arm / lower arm / hand L/R
- thigh / shin / foot L/R

## Existing rig contract preserved

The imported visual is mapped back onto the existing rigid `THREE.Group` hierarchy:

- `pelvis`
- `chest`
- `neck`
- `head`
- `shoulderL/R`
- `elbowL/R`
- `wristL/R`
- `hipL/R`
- `kneeL/R`
- `ankleL/R`

Existing sockets remain authoritative:

- `root`
- `chest`
- `back`
- `head`
- `hand.L` / `hand.R`
- `foot.L` / `foot.R`
- weapon / attack / throw sockets from the existing Pocket Studio contract

This lets the existing animation runtime and solver chain continue to operate on the same joint/socket API instead of creating a second animation engine.

## PBR handling

The GLB compiler preserves scalar glTF metallic/roughness/base-color/emissive properties and extracts embedded texture images when present. The browser reconstructs these as `THREE.MeshStandardMaterial` resources. If an individual texture cannot load, the material keeps its scalar PBR fallback instead of blocking the character.

## Fallback

**Blue Explorer remains the deterministic fallback.**

If the Tripo descriptor, geometry or material reconstruction fails, the Studio falls back to the already accepted Blue Explorer primary implementation. The original Legacy/Debug character remains behind Blue Explorer as its existing fallback.

Fallback chain:

`Tripo 5889e73e → Blue Explorer → Legacy/Debug`

## Preserved animation/runtime systems

- canonical shared solver runtime
- Foot Plant + Leg Response
- foot sockets required for solver parity
- authoritative weapon socket transforms
- baseball-style Capture / Summon Throw
- Walk / Run / Sprint
- Jump / Fall / Land / Crouch
- Dodge / Hit / Knockback / Get Up / Death / Faint / Interact
- Twist / body / momentum / equipment dynamics
- Pocket Studio live bridge
- presentation-only Pocket Monster package boundary
- deterministic 2K PBR starter gate

## Acceptance gates

V1.8.10.7 CI validates the real source GLB and requires:

- glTF 2.0 binary header
- exactly 34,566 source vertices
- exactly 46,897 source triangles
- every source triangle retained in one rigid body region
- non-empty primary body/limb regions
- complete Character Engine joint map
- Tripo primary builder present in final HTML
- Blue Explorer fallback still present
- solver module syntax / existing runtime contracts preserved

## Development rule

Continue incrementally from the latest checkpoint. Do not rebuild the Studio from scratch and do not discard accepted animation, solver, socket or Pocket Monster contracts.
