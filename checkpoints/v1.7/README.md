# Character Prototype Studio V1.7 — Attack Weight System

V1.7 continues directly from V1.6. It adds an equipment-aware attack phase layer without replacing the existing authored animation, Weight Engine, Impact Engine, Momentum Runtime, or game-event contract.

## Attack phases

Anticipation → Wind-up → Acceleration → Impact → Follow-through → Recovery

## V1.7 additions

- per-clip `attackProfile`
- attack side: auto / R / L
- attack styles: horizontal / overhead / thrust
- editable phase times
- Attack lane on the animation timeline
- equipment load affects phase playback timing
- equipment load increases visual follow-through/power response
- pelvis/chest/shoulder/wrist attack response
- partial head stabilization
- Auto Setup from existing hit event
- Sync Hit Event at attack impact time
- non-destructive preview
- Bake Attack Phases to authored keys
- provenance-aware Clear Bake
- Animation QA checks hit sync and heavy-weapon timing
- exported `CharacterAnimationRuntime` evaluates attack timing and response

## Ownership boundary

Animation owns timing and visual response only. A `hit` event is a timing signal. Combat/gameplay code remains responsible for hit validation, damage calculation, HP changes, effects and authoritative world state.

## Artifact

Generated artifact name: `Character_Prototype_Studio_V1.7_Attack_Weight.zip`

Development must continue from V1.7 rather than rebuilding the Studio from scratch.
