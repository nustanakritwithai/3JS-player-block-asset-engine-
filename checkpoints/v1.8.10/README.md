# Character Prototype Studio V1.8.10 — Core Animation QA / Transitions

V1.8.10 is an incremental extension of V1.8.9 and is intentionally scoped to validation and runtime transition metadata.

## Goals

- close the non-weapon core animation phase
- establish a game-facing transition contract without coupling the Studio to Pocket Monster gameplay code
- catch contact/recovery/terminal-state defects before runtime export work
- preserve all V1.8.9 authored action/reaction keyframes

## Added runtime contract

Recognized core clips receive `runtime.transition` with schema `core-transition-v1`.

Fields:

- `studioVersion: "1.8.10"`
- `state`
- `allowedNext[]`
- `blendIn`
- `blendOut`
- `interruptible`
- `terminal`

Death is terminal and cannot expose an exit transition. Faint remains recoverable.

## QA gates

The in-Studio Core Animation QA checks:

1. keyframe ordering
2. clip start time
3. keyframe end time vs clip duration
4. contact metadata availability
5. loop contact seam consistency
6. airborne contact in Jump/Fall
7. ground support at Land completion
8. support recovery for Dodge/Hit/Knockback/Get Up/Interact/Land
9. transition contract version/state consistency
10. unknown next-state references
11. Death terminal-state exits

## Preview chains

- Movement: Idle → Walk → Run → Walk → Idle
- Air: Idle → Jump → Fall → Land → Idle
- Recovery: Idle → Dodge R → Hit React → Knockback → Get Up → Idle

Preview only uses clips already present in the Animation Library. It does not synthesize replacement authored keys.

## Invariants

- V1.8.9 keyframes are not rewritten.
- V1.8.7 Foot Plant safety limits stay in force.
- V1.8.8 air/ground contact metadata stays authoritative for movement clips.
- V1.8.9 reaction ownership stays unchanged.
- Weapon Attachment remains deferred.
- rigid `THREE.Group` architecture remains unchanged.
- 2K PBR quality gate remains enabled.

## Integration readiness

This checkpoint is the final animation-contract gate before the planned Pocket Monster runtime-export/provider work. The transition metadata is presentation/runtime guidance only and does not contain gameplay stats, combat authority or save-state ownership.
