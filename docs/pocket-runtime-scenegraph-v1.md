# Pocket Runtime Scene Graph v1

V1.9.0 exports the live Character Prototype Studio model as a portable scene snapshot in addition to the authoring specification.

Package field:

`sceneGraph`

Schema id:

`three-group-scenegraph-v1`

## Why this exists

Pocket Monster must not need a copy of the Character Prototype Studio builder just to render an exported character.

The runtime package therefore serializes the actual built `THREE.Group` hierarchy into data that a generic Pocket Monster provider can reconstruct.

## Node representation

Every node contains:

- `name`
- `nodeType`: `group` or `mesh`
- `visible`
- local `position`
- local Euler `rotation` + order
- local `scale`
- sanitized `userData`
- recursive `children[]`

Mesh nodes additionally contain:

- BufferGeometry snapshot
- material/PBR snapshot
- shadow flags

## BufferGeometry snapshot

For each geometry, V1.9.0 exports:

- geometry `type`
- serializable geometry parameters when available
- all current BufferGeometry attributes such as position/normal/uv
- attribute item size, normalized flag and count
- index buffer
- material groups
- draw range

This means V1.9.1 can reconstruct a generic `THREE.BufferGeometry` even when it does not know which Studio primitive originally produced the mesh.

## Material snapshot

For each material, V1.9.0 exports presentation properties including:

- type/name
- base color
- emissive color/intensity
- roughness
- metalness
- opacity/transparency
- alpha test
- side
- vertex-color / flat-shading flags
- texture map references

The scalar material values are always available as a fallback.

Texture map sources are references in V1.9.0 rather than duplicated 2K image bytes inside every character JSON. Package validation reports them as warnings so the Pocket loader can decide whether to fetch, cache or replace them.

## Runtime statistics

`sceneGraph.stats` records:

- node count
- mesh count
- vertex count
- triangle count
- external texture-reference count

These values let V1.9.1 apply mobile/runtime budgets before constructing the Three.js objects.

## Gameplay boundary

Scene node `userData` is passed through the same gameplay-field sanitizer as the rest of the package.

The scene graph remains presentation-only and cannot carry HP, combat stats, progression or save authority into Pocket Monster.

## V1.9.1 reconstruction target

The Pocket Monster provider can implement this generic path:

`sceneGraph.root → THREE.Group / THREE.Mesh → BufferGeometry → MeshStandardMaterial → AssetHandle`

This is the key portability layer that makes the Studio export usable without copying the entire Studio implementation into the game.
