# Character Prototype Studio V1.8.4 — Action Dynamics Inspector

Patched directly from V1.8.3.

## Goal

V1.8.4 adds a dedicated full-clip QA system for the Body Dynamics / Action Dynamics stack.

It does not create another motion solver. It observes the existing V1.8.2/V1.8.3 output and reports unnatural timing or instability.

## Inspector checks

- Pelvis → Chest → Shoulder → Arm peak timing
- Excessive kinetic-chain lag
- Angular velocity
- Angular acceleration
- High-speed direction reversals
- Head stabilization / excessive head follow
- Natural soft-range pressure
- Support-foot tag conflicts
- Kick opposite-support-foot requirement
- Center of Mass vs support area
- Recovery residual angle / translation
- Thrust over-rotation
- Dodge lateral readability

## Click-to-debug

Every issue has a timestamp. Clicking an issue jumps the Animation Timeline to that exact time.

The peak timeline exposes P = Pelvis, C = Chest, S = Shoulder and A = Arm. Click a peak marker to inspect the sampled frame.

## Result freshness

The Inspector stores a fingerprint made from Body Dynamics profile, Attack profile, duration/runtime class, and keyframe time/contact/weight metadata.

If those inputs change, the previous result becomes `STALE`.

## Production gate

`validateSpec()` now:
- warns if Action Dynamics Inspector has not been run
- warns if its result is stale
- blocks Game Ready if a current Action Dynamics QA result has hard issues

## QA persistence and staleness

The compact Inspector result is stored under `clip.bodyDynamics.qa`. `normalizeClip()` preserves it.

The freshness fingerprint intentionally excludes the QA object itself. A result also becomes stale when Inspector sample count or sensitivity changes.
