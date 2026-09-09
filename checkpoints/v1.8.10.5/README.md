# Character Prototype Studio V1.8.10.5 — Blue Explorer Primary Character

V1.8.10.5 is an incremental character-model integration on top of the verified V1.8.10.4 + Pocket Studio bridge producer.

## Goal

Make the supplied Blue Explorer procedural model the default Character Engine character while preserving every accepted animation/runtime system and the live Pocket Studio export contract.

## Model source

The user-supplied `blue_explorer_3d-2.html` contains a procedural `createBlueExplorer(THREE)` factory. Only the runtime factory is retained; UI, reference-image base64 and standalone viewer code are excluded.

Factory source SHA-256:

`7bb50a22bf892f8f79200d732e9aa1b00b22b0a046e37070122818ed343b76d2`

The factory is LZMA-compressed and split into four deterministic source parts under `assets/characters/`.

## Engine adapter

- previous builder renamed to `buildLegacyCharacter`
- `buildCharacter()` now selects `buildBlueExplorerPrimaryCharacter()`
- source pivots are converted into the engine hierarchy without moving visible bind-pose geometry
- spatial-side mapping preserves existing engine left/right rotation signs
- all core joints and hand/foot/chest/head/root sockets are registered
- Blue Explorer material names are mapped to existing skin/shirt/pants/boots/hair/eyes/accent export roles
- Legacy/Debug builder remains the runtime fallback if construction fails

## Preserved

- V1.8.10.4 overhand baseball-style Capture/Summon Throw
- Monster Ball release/summon events
- Walk / Run / Sprint / Jump / Fall / Land / Crouch
- Dodge / Hit / Knockback / Get Up / Death / Faint / Interact
- Foot Plant + Leg Response
- Twist / action dynamics ownership
- Pocket Studio live bridge
- deterministic PBR material export
- rigid `THREE.Group` architecture

## Gates

CI must verify:

1. Blue Explorer source checksum
2. Blue Explorer is the default `buildCharacter()` path
3. Legacy/Debug builder remains available
4. engine right-hand joint/socket mapping exists for Monster Ball release
5. existing throw, locomotion, Foot Plant and reaction regression tokens remain
6. Pocket Studio bridge/render profile/material-pack contract remains
7. module syntax passes `node --check`
8. final built HTML matches the V1.8.10.5 deterministic checksum
