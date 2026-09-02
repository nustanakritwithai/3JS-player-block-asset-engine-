# Character Prototype Studio V1.0 Checkpoint

Baseline: **V0.9 Game Animation Runtime**, extended incrementally to **V1.0 Center of Mass / Support Area / Balance**.

## Added in this checkpoint

- Relative mass profile per body region
- Equipment mass input
- Center of Mass (COM) calculation from weighted world-space part centers
- COM debug marker
- Foot support detection and support rectangle
- Weight vector visualization
- Current-pose balance analysis
- Full authored-animation balance sampling
- Timed balance warnings/hard issues
- Click balance issue → jump Animation Timeline
- Balance analysis included in Quality Report

## Architecture rule

This is **not a new project**. V1.0 is a patch on the existing Studio and retains CharacterSpec, Rig, Pose Library, Animation Timeline, Contact/Weight lanes, Animation QA, Game Animation Runtime and img2threejs Adapter.

CharacterSpec remains the source of truth; COM/support visualization is runtime analysis.

## Next

V1.1 should add a continuous left/right Weight Transfer Curve using the existing authored keyframes/contact metadata and the V1.0 COM/support foundation.
