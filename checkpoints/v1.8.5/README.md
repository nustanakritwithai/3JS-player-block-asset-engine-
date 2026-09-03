# Character Prototype Studio V1.8.5 — Dynamics Auto-Tuner

V1.8.5 is an incremental extension of the verified V1.8.4.1 Twist Activation Hotfix. It does not rebuild the Studio and does not replace the rigid `THREE.Group` rig architecture.

## Goal

Turn Action Dynamics Inspector findings into reversible Body Dynamics modifier proposals while preserving authored animation keyframes.

## Workflow

1. Run Action Dynamics Inspector.
2. Choose Auto-Tuner mode: Conservative, Natural, or Strong Fix.
3. Analyze & Propose.
4. Review proposed parameter deltas and predicted hard/warn counts.
5. Preview Proposed Fix on the character without saving the changes.
6. Apply to persist the modifier changes.
7. Action Dynamics Inspector reruns automatically after Apply.
8. Undo remains available through the Studio command history.

## Modifier-only contract

The tuner may adjust only:

- intensity
- pelvisShare
- chestShare
- shoulderShare
- armShare
- pelvisLead
- chestLag
- shoulderLag
- armLag
- counterRotation
- followThrough
- forwardLeanShare
- sideLeanShare
- headStability

It must not rewrite authored animation keyframes. Apply verifies this invariant by comparing the keyframe JSON before and after the command and throws if a keyframe changed.

## Inspector-guided behavior

Examples:

- chain timing order → increase the downstream lag
- excessive chain lag → compress shoulder/arm lag
- excessive angular velocity/acceleration → reduce the owning joint share
- natural range pressure → reduce the owning joint share
- weak head stabilization → increase headStability
- COM/support conflict → reduce intensity and lean shares
- recovery residual → reduce followThrough
- thrust rotation pressure → reduce core/shoulder twist shares
- insufficient dodge read → increase intensity and side lean

## Preview semantics

Preview temporarily overlays the proposed Body Dynamics parameters on the current clip and plays the animation. It does not autosave the proposal. Cancel restores the exact pre-preview Body Dynamics snapshot. Apply first restores the pre-preview state, then commits the proposal through `withCommand(...)` so Undo works correctly.

## Build chain

`V1.8.4 lossless source` → `patch_v1_8_4_1.py` → `patch_v1_8_5.py` → SHA-256 verification → `_site/index.html`
