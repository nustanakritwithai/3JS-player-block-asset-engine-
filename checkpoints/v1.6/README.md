# Character Prototype Studio V1.6 — Equipment Mass Response

V1.6 is patched directly on top of V1.5.

## New
- Equipment identity/category/socket/mass profile
- Presets: None / Sword / Great Sword / Hammer
- Equipment mass participates in V1.0 Center of Mass
- Socket-aware COM point
- Shoulder drop on carrying side
- Chest counter-balance
- Pelvis counter-shift
- Wider stance under heavy load
- Momentum inertia scales with equipment load
- Action recovery slows under heavy load
- Preview / Bake / Clear Bake
- Generated Game Animation Runtime supports the same load response

## Ownership boundary
Equipment response changes visual animation only.
Game equipment/inventory/combat remains outside this animation system.

## Examples
Light sword:
- small shoulder/chest compensation
- little momentum penalty

Great sword:
- larger counter-balance
- wider stance
- slower action recovery

Hammer:
- high inertia
- strongest stance/counter-balance
- longest recovery

## Local artifact checkpoint
The exact generated V1.6 artifact for this checkpoint is `character_prototype_studio_v1_6.html` in the working artifact package.

SHA-256 (HTML): `91ebb594075451655b76265d9871294d089d301ae9cf239c102b8c26147bc0f9`

SHA-256 (ZIP): `55692987089e10603aad795b64dd88b2a7aa1e2eeeda6909165e8746d1675e40`

Development rule: continue from V1.6; do not rebuild the Studio from scratch.
