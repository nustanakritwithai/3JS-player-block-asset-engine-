# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.9.0 — Pocket Runtime Character Export**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Turn the accepted Character Prototype Studio output into a **presentation-only runtime character package that Pocket Monster can load through its Asset Engine**.

V1.9.0 is stacked on V1.8.10. It does not rebuild the Studio, replace the rigid `THREE.Group` rig, or move gameplay/combat authority into the asset package.

## V1.9.0 — Pocket Runtime Character Export

The Animation Library now includes **POCKET MONSTER RUNTIME EXPORT**.

The Studio can validate and download:

`<character-id>.pocket-character.json`

Schema:

`pocket-character-runtime-v1`

Target provider:

`studio-character`

### Runtime package

The single JSON envelope contains:

- presentation-only `manifest`
- Pocket Monster-ready `catalogEntry`
- sanitized visual character specification
- rigid `THREE.Group` rig declaration
- exported joint-name list
- socket locators for hands/head/back/waist/VFX/attack/throw origins
- authored animation clips
- animation index and V1.8.10 transition contracts
- dynamics metadata
- Core Animation QA acceptance summary
- gameplay exclusion policy
- SHA-256 integrity metadata when Web Crypto is available

### Export UI

The user can set:

- Character ID, default `character.human.pirate.custom001`
- Display Name

Actions:

- **Validate Package** — builds the runtime envelope and reports validation/warnings without downloading.
- **Export for Pocket Monster** — runs the V1.8.10 Core Animation QA gate, validates the package, then downloads the `.pocket-character.json` file.

### Gameplay authority boundary

The runtime package is explicitly:

`contract: presentation-only`

The exporter recursively strips gameplay/save fields including HP, combat stats, progression, currency, capture and save data before packaging.

The package sets:

`gameplayPolicy.included = false`

Pocket Monster / Pirate Fruit server-domain systems remain authoritative for gameplay, combat, progression and persistence.

### Target Pocket Monster contract

The package declares the target `AssetHandle` surface expected by the Pocket Monster Asset Engine:

- `root`
- `rig`
- `play()`
- `update()`
- `anchor()`
- `bounds()`
- `setAppearance()`
- `dispose()`

V1.9.0 only authors/exports the package. The actual Pocket Monster loader/provider belongs to V1.9.1.

## V1.8.10 — Core Animation QA / Transitions

V1.8.10 remains the owner of the runtime transition contract and pre-export animation acceptance gate.

It provides:

- `core-transition-v1`
- Idle/Walk/Run/Sprint/Jump/Fall/Land/Crouch transitions
- Dodge and reaction recovery
- contact and loop-seam checks
- terminal Death behavior
- Movement / Air / Recovery preview sequences

V1.9.0 consumes this metadata; it does not rewrite V1.8.9 authored keyframes.

## V1.8.9 — Core Action / Reaction Pack

V1.8.9 remains the owner of the core non-weapon action/reaction authored clips:

- Dodge Right / Left
- Hit React
- Knockback
- Get Up
- Death
- Faint
- Interact

## V1.8.8 — Core Movement Animation Pack

Movement library remains complete for the current core slice:

- Walk / Run / Sprint / Start / Stop
- Turn L/R
- Strafe L/R
- Jump / Fall / Land
- Crouch Idle / Crouch Walk

## Preserved systems

- V1.8.5.2 Twist Isolation and Animation Library restore
- V1.8.5.3 Natural Walk pelvis lateral cap `±0.016m`
- V1.8.6 distinct Walk / Run / Sprint / Start / Stop / Turn / Strafe dynamics
- V1.8.7 Foot Plant + Leg Response with bounded root correction
- V1.8.8 movement/air contact states
- V1.8.9 action/reaction states
- V1.8.10 transition/QA contract
- rigid `THREE.Group` rig architecture
- 2K PBR quality gate

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → V1.8.9 → V1.8.10 → V1.9.0 → semantic gates → Pages`

## Next checkpoint

**V1.9.1 — Pocket Monster Runtime Loader / `studio-character` Provider**

Planned flow:

`Studio export → .pocket-character.json → Pocket Monster package loader → studio-character provider → AssetHandle → game player visual`

Weapon Attachment remains deferred while this game-runtime bridge is established.

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.
