# PocketMonster Studio Render Fidelity Plan

Status: Studio transport metadata is emitted in the `pocket-character-runtime-v1`
1.1 export. PocketMonster does not yet consume it, so it is not a claim that
textures or Studio lighting are visible in the game. This document deliberately
does not add a renderer, change gameplay authority, or enable a new sandbox
capability.

## Current boundary

Character Studio currently exports geometry, scalar PBR values, mesh
`castShadow`/`receiveShadow` flags, and texture URL references. PocketMonster
rebuilds geometry and scalar `MeshStandardMaterial` values on the existing
Pirate Fruit renderer. It does not currently load or assign texture maps, and
Studio's editor lights are not part of the package. Shadow flags therefore
arrive, but whether they cast a visible shadow depends on the existing host
renderer and its lights.

## Proposed `pocket-character-render-profile-v1`

Studio now sends the following *presentation-only* field; PocketMonster must
implement the bounded host consumer below before it becomes a render feature:

```json
{
  "renderProfile": {
    "schema": "pocket-character-render-profile-v1",
    "version": "1.0.0",
    "textures": [
      {
        "id": "skin-albedo",
        "url": "https://.../skin-albedo.png",
        "sha256": null,
        "role": "map",
        "colorSpace": "srgb",
        "flipY": false,
        "wrapS": 1001,
        "wrapT": 1001
      }
    ],
    "materials": [{
      "name": "Skin",
      "model": "MeshStandardMaterial",
      "textureSlots": { "map": "skin-albedo" },
      "roughness": 0.72,
      "metalness": 0.0,
      "normalScale": [1, 1]
    }],
    "shadow": { "cast": true, "receive": true },
    "lightingProfile": {
      "id": "pirate-world-pbr-neutral-v1",
      "exposure": 1.0,
      "requiresExistingHostShadows": true
    }
  }
}
```

Studio exports only same-origin HTTPS texture URLs and includes texture sampling
metadata (`colorSpace`, `flipY`, wrap, filters, mipmaps, anisotropy, and UV
transform). It emits a SHA-256 only when an upstream texture supplies one; the
browser's synchronous Three.js export path cannot truthfully calculate bytes it
cannot read. The Pocket host must therefore obtain and verify an integrity value
before binding a texture. The package does not send image bytes, executable
code, light objects, gameplay data, or renderer commands.

## Bounded host implementation

1. The existing `AssetEngine` texture cache fetches only allowlisted HTTPS URLs,
   deduplicates by integrity hash, and disposes textures with the character
   handle.
2. The existing Pirate Three.js runtime creates textures and assigns approved
   slots (`map`, `normalMap`, `roughnessMap`, `metalnessMap`, `emissiveMap`,
   `aoMap`, `alphaMap`) to its existing materials. On failure it retains the
   scalar material fallback and the visible Pirate fallback character.
3. A host-owned adapter may select a named `lightingProfile`; it may verify
   existing renderer shadow support and host lights, but must not add a second
   renderer, modify world ownership, or accept arbitrary Studio light objects.
4. `castShadow` and `receiveShadow` remain mesh flags. The adapter only enables
   a pre-approved host shadow setting if it is already supported by the Pirate
   renderer budget.

## Acceptance gates

- Texture URL, origin, checksum, dimensions, and decode failure cases.
- Every assigned texture has the declared color space, flip, and wrapping.
- Existing renderer remains the only renderer and no Studio iframe remains
  after package delivery.
- Mesh material screenshots demonstrate albedo/normal/PBR response and a
  visible host shadow under the named profile; low-end devices may use scalar
  fallback with a diagnostic reason.
- The game keeps identity, movement, collision, combat, HP, save, server, and
  sandbox authority unchanged.
