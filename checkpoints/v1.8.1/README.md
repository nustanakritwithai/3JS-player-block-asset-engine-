# Character Prototype Studio V1.8.1 — Natural Walk Tuning

Incremental animation tuning on top of V1.8.

## Fixed
- reduced excessive left/right pelvis sway during walk
- procedural pelvis transfer now crosses center continuously instead of flipping sides with a minimum offset
- reduced default pelvis lateral shift, hip drop, twist and COM correction
- increased smoothing of pelvis response
- underlying weight transfer remains intact; visual pelvis follows a softer response
- old V1.8 default settings migrate automatically, while custom values are preserved

## Natural defaults
- procedural pelvis shift: 0.028m
- pelvis solver lateral influence: 0.32
- max shift: 0.075m
- hip drop: 2.5°
- pelvis twist: 4°
- COM gain: 0.26
- COM correction max: 0.05m
- smoothing: 0.78

This patch is intended to make walking feel planted rather than hip-swing driven.