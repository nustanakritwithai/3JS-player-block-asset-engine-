# P1 verification — 2026-09-10

## Executed

- Node 22.16.0: `node --test tests/ground.test.mjs` — 21/21 passed.
- Strict TypeScript compilation of the original 20.9.4 Simulation dependency
  graph and WorldSurfacePresentation selector — zero compiler errors.
- Actual Simulation instances: seed 29051, 16x16 (256 cells) and 64x64 (4096 cells).
- Projection + JSON roundtrip + geometry generation accepted both real worlds.
- Original snapshots unchanged after projection; simulation tick unchanged.
- Calling the producer's own `advanceFrame(1/30)` advances tick 0 to 1, and the
  resulting frame is accepted. The consumer modules do not call advanceFrame.
- Injecting the existing producer `worldSurfaceBiome` selector succeeds.
- Unit tests cover malformed input, frozen state, soil ownership, actual coverage,
  water datum, explicit transforms, global boundary normals/UVs, batching,
  texture ownership, cleanup, shader patch markers and identity-cache behavior.

The source ZIP is not copied into this public patch. Reproduce simulator tests
with the authorized source and a local TypeScript compiler using the script
in `tests/ground-worldsim-integration.mjs` and its CLI help.

## Not claimed

Node renderer tests use explicit Three.js contract doubles; they do not certify
real GPU shader compilation. The development container could not download the
Three.js CDN module, so real WebGL rendering, image quality and Android FPS have
NOT been verified. The preview clearly falls back to a 2D snapshot display.

No mobile performance number, live server binding, merged PR or production
deployment is implied. Visual acceptance must use real Three.js 0.179.1 plus
representative texture maps on the target Android device.

Source archive SHA-256: `0fd09ff165fc63238036138bbb29075ac2001f45b3318f2346d85f2e56546ead`.
