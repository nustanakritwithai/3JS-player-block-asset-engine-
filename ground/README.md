# WorldSim Ground Lab — P1 (presentation only)

Additive Asset Engine module. Existing Studio, characters, rig, sockets, animation,
exports, game entrypoints and deployment settings are unchanged. This is an
isolated preview + adapter, **not a completed live-game integration**.

## Run

From the repository root:

```sh
node --test tests/ground.test.mjs
python3 -m http.server 8080
# Open http://localhost:8080/ground/
```

The page loads pinned Three.js 0.179.1 from a CDN. It retains a 2D snapshot viewer
when Three.js/WebGL is unavailable. No new renderer should be constructed by the
module inside the real game; inject the host's existing THREE instance and scene.

Upload a complete WorldSim 20.9.4 RenderSnapshot/RenderWorldSnapshot JSON or a
validated `worldsim-ground/1` packet. The sample is an actual producer export,
seed 29051, 4x4, tick 0, with the producer's original `worldSurfaceBiome` selector.
It is **not** a live server connection and contains no simulated texture preview states.

The initial preview uses palette materials. High-resolution ground photographs
are **not bundled**. Each material accepts separate albedo, normal, roughness and
AO images; the loader caps each image at 512/1024/2048 px without upscaling.
Images stay in the browser, not uploaded to a service. No fake normal/roughness
maps are synthesized from a color image. Use licensed seamless assets.

## Audited data, not a new simulation

Audited against the user's `Living_World_Physics_Simulator_20.9.4_Full_Source.zip`:

| Producer field | Presentation use |
| --- | --- |
| `world.cells[i].elevation` | Ground height with explicit visual scale |
| `world.cells[i].totalWaterHeight` | Water surface datum, not elevation plus this value |
| `world.cells[i].surfaceWater` | Surface water depth; no precipitation integration |
| `world.cells[i].isOceanCell`, `isFlooded` | Producer flags, never threshold reclassification |
| `world.soil.cells[i].waterContent / saturationCapacity` | Normalized optical wetness, active soil only |
| `world.vegetation.cells[i].coverage`, `active` | Actual vegetation coverage, not fertility-based generation |
| `world.biomes.cells[i].primaryBiome` | Classified biome preserved in the packet |
| `world.fire.cells[i].burnSeverity` | Optical burn darkening |

The compatibility `world.cells[i].soilMoisture` is NOT another water reservoir.
Temperature/humidity/fertility never create new grass, mud, lakes or biome truth.
`surfaceBiome` may be supplied by the producer using its **existing**
`src/rendering/WorldSurfacePresentation.ts::worldSurfaceBiome`. The adapter does
not copy that classifier. Without it, material selection uses primaryBiome.
Both modes retain primary biome identity separately from visual material choice.

## Integration boundary

On the producer/server which already owns the simulator:

```js
import { projectWorldSimGround } from './ground/worldsim-ground-adapter.mjs';
// Reuse the producer's existing selector, when available:
// import { worldSurfaceBiome } from './rendering/WorldSurfacePresentation.js';
const packet = projectWorldSimGround(simulation.getSnapshot());
// or projectWorldSimGround(snapshot, { surfaceBiome: worldSurfaceBiome });
// Publish using the existing trusted transport. No new transport in this patch.
```

On the consumer:

```js
import { createWorldGroundRenderer } from './ground/three-ground-renderer.mjs';
const ground = createWorldGroundRenderer({
  THREE, scene,
  transform: { horizontalScale: 0.04, elevationScale: 15, textureWorldSize: 4 },
  quality: 'medium',
  maxAnisotropy: renderer.capabilities.getMaxAnisotropy(),
});
// Call from the existing snapshot listener, NOT the render loop.
ground.setFrame(packet);
// The existing game loop still calls renderer.render(scene, camera).
// On scene exit:
ground.dispose();
```

**These example transforms are visual tuning, not physical units.** Source world
coordinates are 1200x1800 by default and source elevations are normalized, not
metres. Adopt the game's agreed mapping before integrating player/collision
positions. Geometry is centered in x/z; it does not provide navigation or physics.

Offline export:

```sh
node ground/export-worldsim.mjs snapshot.json ground.json
```

## Resource and safety boundaries

Input must be a complete, indexed, finite 20.9.4 snapshot. Unknown versions,
partial arrays, malformed enums/flags and grids over 65,536 cells fail explicitly.
Packets are copied and deeply frozen. `presentationOnly` is not authentication;
never accept this rendering format as authoritative movement/combat/world input.

A frame builds at most seven terrain batches plus water, not one mesh per cell.
UVs and corner normals are globally consistent across material batches. Invalid
packets leave the existing visible frame unchanged. Caller textures are cloned;
only owned clones/materials/geometries are disposed. Repeated disposal is safe.

Albedo uses sRGB; normal/roughness/AO use data color space. AO uses channel 1.
The WebGL shader uses wetness/burn only for optical darkening and roughness.
The normal Y convention is explicit. Upstream docs:
https://threejs.org/manual/en/color-management.html
https://threejs.org/docs/#api/en/materials/MeshStandardMaterial
https://threejs.org/docs/#api/en/materials/Material.onBeforeCompile

## Deliberately not finished in P1

- No production game hook, websocket subscription, auto-merge or deployment.
- No licensed photographic texture pack, KTX2 build pipeline or texture residency manager.
- No splat blending/anti-tiling/vegetation instancing/parallax/terrain LOD.
- Material boundaries remain cell-based. Water is piecewise flat per cell.
- Geometry corner smoothing is only visual; land/water seams require later QA.
- Full-frame rebuild on a new snapshot; dirty-chunk updates/sequence handling and
  replay-reset protocol must precede high-frequency live streaming.
- Quality tiers cap imported image dimensions and anisotropy; they are NOT an
  Android FPS or thermal-performance certification.

See QA.md for actual checks and remaining device/rendering acceptance gates.
