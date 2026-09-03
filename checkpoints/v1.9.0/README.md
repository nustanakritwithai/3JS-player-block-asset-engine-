# Character Prototype Studio V1.9.0 — Pocket Runtime Character Export

V1.9.0 is an incremental extension of V1.8.10. It begins the game-facing Pocket Monster integration phase without rebuilding the Studio or changing gameplay authority.

## Goal

A character authored in Character Prototype Studio can be exported as a self-contained runtime package for the Pocket Monster Asset Engine.

Export format:

`<character-id>.pocket-character.json`

Schema:

`pocket-character-runtime-v1`

Target provider:

`studio-character`

## Package contents

- presentation-only manifest
- Pocket Monster catalog entry
- sanitized visual/authoring character specification
- rigid `THREE.Group` rig declaration
- joint-name list
- runtime socket locators
- authored animation clips
- animation index with V1.8.10 transition contracts
- dynamics metadata
- Core Animation QA acceptance summary
- gameplay-field exclusion policy
- SHA-256 integrity metadata when Web Crypto is available

## Default sockets

- `rightHand`
- `leftHand`
- `head`
- `back`
- `waist`
- `vfxOrigin`
- `attackOrigin`
- `throwOrigin`

Each socket is exported as a joint locator plus a local offset. V1.9.1 can map those locators into Pocket Monster `AssetHandle.anchor()` behavior.

## Gameplay authority boundary

V1.9.0 exports presentation/runtime character data only.

The exporter recursively strips forbidden gameplay/save fields such as:

- HP / HP current / HP max
- ATK / DEF / SPATK / SPDEF / SPD
- Vitality / Combat / Blade / Ranged / Fruit Power / Mastery
- Mana / Coins / Capture / Save
- Level / EXP / Experience / Damage

The exported package sets:

`gameplayPolicy.included = false`

Gameplay, combat, progression and save authority remain in Pocket Monster / Pirate Fruit server-domain systems.

## Export gate

`Export for Pocket Monster` runs V1.8.10 Core Animation QA first.

- hard QA failures block download
- warnings remain visible but do not block
- package validation rejects gameplay-field leaks
- package validation requires the `studio-character` provider contract
- package validation requires rigid `THREE.Group` rig architecture and hand sockets

`Validate Package` can build and inspect the package without downloading it.

## Transport decision

V1.9.0 intentionally uses one self-contained JSON envelope instead of ZIP/GLB.

Reasons:

- works directly in the browser and on mobile
- no new archive dependency
- keeps the current procedural `THREE.Group` authoring model intact
- Pocket Monster can validate one schema before provider construction
- V1.9.1 can add caching/splitting internally without changing the authoring format

## Dependency

V1.9.0 is stacked on V1.8.10 Core Animation QA / Transitions. V1.8.10 remains the owner of transition semantics and acceptance checks.

## Next checkpoint

V1.9.1 — Pocket Monster `studio-character` provider + runtime package loader.
