# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.10.4 — Baseball Throw Motion Hotfix**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Make the capture-ball throw read visually as an **overhand baseball-style throw**, not a side-arm / frisbee throw, while preserving the renderer and all existing gameplay animation systems.

## V1.8.10.4 — Baseball Throw Motion Hotfix

The previous Monster Ball throw used too much horizontal sweep and side lean. V1.8.10.4 changes the throw signature to:

`Back-foot load → arm cocked above/behind shoulder → front-foot step → elbow leads → overhand release → wrist snap → cross-body follow-through → recover`

### Throw changes

- Attack-weight style changes from `horizontal` to `overhead` for capture/summon throw clips.
- Throw Body Dynamics reduce lateral/side motion and increase forward drive.
- Throwing arm now carries more of the motion while pelvis/chest rotation remains supporting rather than dominating.
- Wind-up keeps the elbow high and bent behind the shoulder.
- Release extends the arm above shoulder level instead of sweeping sideways.
- Follow-through crosses the body like a baseball throw.
- Clip metadata records `throwStyle = overhand-baseball`.

Quick / Standard / Power / Summon retain their separate release timings from V1.8.10.

## Preserved fixes and systems

- V1.8.10.3 `clip is not defined` boot fix
- V1.8.10.2 core-first Three.js boot and optional editor-control fallback
- Monster Ball `ball.release`, `capture.throw`, `monster.summon`
- Twist Isolation
- Walk lateral cap `0.016m`
- distinct Run/Sprint
- Foot Plant max root correction `0.028m`
- Jump/Fall/Land/Crouch
- Dodge/Hit/Knockback/Get Up/Death/Faint/Interact
- rigid `THREE.Group` rig
- 2K PBR gate

## Roadmap

- **V1.8.10.4** — baseball-style capture/summon throw visual hotfix
- **V1.8.11** — Core Animation QA / Transitions after live visual acceptance

## Development rule

Continue incrementally from the latest checkpoint; do not rebuild the Studio from scratch.
