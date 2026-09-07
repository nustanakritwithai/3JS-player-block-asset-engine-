# V1.8.10.2 — Core-First Character Boot Hotfix

Regression: the Studio UI loaded but the main character remained invisible and an error overlay appeared.

Fix:
- Three.js core is the only mandatory boot dependency.
- Core fallback order: jsDelivr → esm.sh → unpkg.
- OrbitControls and TransformControls are optional; failed editor controls fall back to no-op classes so the character can still render.
- V1.8.10.1 saved-state recovery remains available with a V1.8.10.2 backup key.
- Monster Ball and all prior animation systems are unchanged.

V1.8.11 remains blocked until the character is visibly present on the user's device.
