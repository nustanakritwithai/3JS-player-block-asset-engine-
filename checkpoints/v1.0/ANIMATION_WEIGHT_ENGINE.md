# Animation Weight Engine — V1.0

## Center of Mass

The Studio evaluates an approximate COM using relative animation masses:

`COM = Σ(position × mass) / Σ(mass)`

V1.0 uses the world-space bounding-box center of each procedural body part. The values are relative animation masses, not kilograms.

## Mass profile

Default categories include torso, pelvis, head, left/right upper arms, forearms, hands, thighs, shins and feet. An additional equipment mass can be attached at `hand.R`, falling back to `hand.L` or `back`.

## Support area

Feet closest to the current ground level are treated as support contacts using configurable ground tolerance. Their footprints are combined into a support rectangle with optional padding.

## Balance

The X/Z projection of COM is checked against the support rectangle plus a configurable balance margin.

Debug visualization includes:

- COM marker
- support area
- vertical weight vector
- balanced/outside state

## Full animation analysis

The selected authored clip can be sampled through time. Each sample evaluates COM and the supporting feet. Timed issues are generated when COM leaves the support area.

## Boundary

V1.0 measures and visualizes weight; it does not yet automatically modify pelvis/spine animation from COM. V1.1+ will use these results to drive weight transfer and body response without replacing the existing keyframe/runtime system.
