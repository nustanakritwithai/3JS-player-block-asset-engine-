# 3JS Player Block Asset Engine

Current checkpoint: **Character Prototype Studio V1.8.10 — Core Animation QA / Transitions**.

Live GitHub Pages:

https://nustanakritwithai.github.io/3JS-player-block-asset-engine-/

## Current priority

Finish and visually accept the **complete non-weapon core animation runtime contract** before Weapon Attachment begins.

V1.8.10 is stacked on V1.8.9. The V1.8.9 action/reaction authored keyframes remain owned by V1.8.9; V1.8.10 adds transition metadata, QA, recovery checks, contact checks and preview sequences without rewriting those authored poses.

## V1.8.10 — Core Animation QA / Transitions

V1.8.10 closes the core-animation phase with a runtime-facing transition contract and an in-Studio QA gate.

### Transition contract

Each recognized core clip receives `runtime.transition` using schema `core-transition-v1`:

- normalized runtime state
- allowed next states
- blend-in / blend-out guidance
- interruptible flag
- terminal-state flag
- Studio version stamp

The contract covers:

- Idle / Walk / Run / Sprint / Start / Stop
- Turn / Strafe
- Jump → Fall → Land
- Crouch Idle / Crouch Walk
- Dodge L/R recovery
- Hit React / Knockback / Get Up recovery
- Interact recovery
- Death terminal behavior
- Faint recovery

### Core Animation QA

The Animation Library now contains a **CORE ANIMATION QA / TRANSITIONS** panel that checks:

- keyframe time ordering
- clip start/end timing consistency
- contact metadata readability
- loop contact seam consistency
- airborne contact for Jump/Fall
- supported landing state
- supported recovery for Dodge/Hit/Knockback/Get Up/Interact/Land
- V1.8.10 transition-contract presence
- unknown next-state references
- Death terminal-state exit violations

Hard failures block acceptance; warnings remain visible for manual review.

### Preview sequences

Three transient QA sequences are available when their clips exist in the current Animation Library:

- **Movement QA** — Idle → Walk → Run → Walk → Idle
- **Air QA** — Idle → Jump → Fall → Land → Idle
- **Recovery QA** — Idle → Dodge R → Hit React → Knockback → Get Up → Idle

The preview sequencer uses existing clips and does not author or mutate keyframes.

### Authoring invariant

V1.8.10 may add/update transition metadata but must **not rewrite V1.8.9 authored keyframes**.

New template clips created after the patch are automatically stamped with the V1.8.10 transition contract. Existing recognized clips are upgraded on load and retained through normal save/autosave.

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

## Preserved animation systems

- V1.8.5.2 Twist Isolation and Animation Library restore
- V1.8.5.3 Natural Walk pelvis lateral cap `±0.016m`
- V1.8.6 distinct Walk / Run / Sprint / Start / Stop / Turn / Strafe dynamics
- V1.8.7 Foot Plant + Leg Response with bounded root correction
- V1.8.8 Jump/Fall/Land/Crouch movement states
- V1.8.9 Dodge/Reaction/Recovery/Interact authored states
- rigid `THREE.Group` rig architecture
- 2K PBR quality gate

## Build chain

`V1.8.4 → V1.8.4.1 → V1.8.5 → V1.8.5 guard → V1.8.5.1 → V1.8.5.2 → V1.8.5.3 → V1.8.6 → V1.8.7 → V1.8.8 → V1.8.9 → V1.8.10 → SHA-256 / semantic gates → Pages`

## Next phase

After V1.8.10 passes CI and visual acceptance, the next major phase may begin the game-facing/runtime work planned for Pocket Monster integration. Weapon Attachment remains deferred until this checkpoint is accepted.

## Development rule

Future development must **continue from the latest committed/checkpointed version instead of rebuilding the Studio from scratch**.
