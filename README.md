# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.10.5 — Blue Explorer Primary Character**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current primary character

**Blue Explorer** is now the default visual/rig character of the Character Engine.

The previous generated block character is preserved as **Legacy/Debug fallback**. V1.8.10.5 does not rebuild the animation engine; it retargets the existing engine to the Blue Explorer rigid-pivot model.

## Blue Explorer integration

Source model characteristics:

- procedural Three.js geometry; no GLB/OBJ dependency
- rigid-part pivot rig
- articulated shoulder → elbow → wrist chains
- articulated hip → knee → ankle chains
- neck → head hierarchy
- generated local materials/textures

Engine adapter:

- converts presentation pivots into `pelvis → chest → neck/head`
- reparents shoulders under chest and hips under pelvis while preserving bind-pose geometry
- maps Blue Explorer spatial sides to engine `L/R` joint conventions
- exposes engine joints `pelvis`, `chest`, `neck`, `head`, shoulders, elbows, wrists, hips, knees and ankles
- exposes `hand.L`, `hand.R`, `foot.L`, `foot.R`, `chest`, `back`, `head` and `root` sockets
- keeps the old `buildCharacter` implementation as `buildLegacyCharacter`
- falls back to Legacy/Debug if Blue Explorer construction fails

## Existing animation/runtime systems preserved

- Baseball-style Monster Ball Capture Throw / Summon Throw
- `ball.release`, `capture.throw`, `monster.summon`
- Walk / Run / Sprint
- Jump / Fall / Land / Crouch
- Dodge / Hit / Knockback / Get Up / Death / Faint / Interact
- Foot Plant + Leg Response
- Twist Isolation / Action Body Dynamics
- Walk lateral cap `0.016m`
- Foot Plant max root correction `0.028m`

## Pocket Studio bridge preserved

V1.8.10.5 is layered **after** the current Pocket Studio live bridge and deterministic PBR material export patches. The producer contract remains presentation-only and continues to export scene graph, rig bindings, sockets, motion pack and render-profile metadata.

## Source integrity

The Blue Explorer runtime factory is stored as deterministic compressed source parts under `assets/characters/`. CI reconstructs the factory and verifies its SHA-256 before injecting it into the final Studio artifact.

## Roadmap

- **V1.8.10.5** — Blue Explorer becomes primary Character Engine model
- **V1.8.11** — Blue Explorer animation QA / transitions / visual acceptance

## Development rule

Continue incrementally from the latest checkpoint; do not rebuild the Studio from scratch.
