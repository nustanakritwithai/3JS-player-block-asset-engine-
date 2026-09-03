# Character Prototype Studio V1.8.5.1 — Twist Visual Recovery Hotfix

V1.8.5.1 is an incremental hotfix on top of V1.8.5. It exists because the Twist Demo could still reuse any currently selected `action` clip. If that clip had saved or Auto-Tuned Body Dynamics shares/timing that produced little visible rotation, the demo could play without showing a clear kinetic twist even though Body Dynamics was technically active.

## Root cause

The V1.8.4.1 activation fix corrected `motionClass`, but the Twist Demo path was not deterministic. When the current clip already had `runtime.motionClass === "action"`, the demo reused it and only forced `bodyDynamics.enabled = true` plus a minimum intensity. It did not restore a known-good pelvis/chest/shoulder share profile or attack phase timing.

## Hotfix

`Twist Demo` now creates or refreshes a dedicated `Twist_Demo_V1_8_5_1` clip and never depends on the user's currently selected action clip.

The demo locks:

- `motionClass = action`
- Slash action profile
- explicit anticipation / wind-up / impact / follow-through / recovery timing
- known-good pelvis/chest/shoulder/arm shares and lead/lag values
- Natural soft limits
- head stabilization
- neutral character root orientation
- ISO / 3-quarter camera for better visual readability

## Visibility preflight

Before playback, V1.8.5.1 samples the Body Dynamics solver across the full demo clip. Playback is blocked if peak solver output is below these minimum visibility thresholds:

- Pelvis >= 6 degrees
- Chest >= 10 degrees
- Shoulder >= 14 degrees

The locked profile is expected to produce approximately:

- Pelvis ~12 degrees
- Chest ~24 degrees
- Shoulder ~36 degrees

while remaining inside the configured natural soft limits.

## State safety

The demo uses a dedicated generated clip so it does not rewrite the authored keyframes of the user's selected animation. Browser storage moves to `characterPrototypeStudio.v1.8.5.1` and migrates existing V1.8.5 data as fallback.

## Development gate

Do not begin V1.8.6 until the live V1.8.5.1 Twist Demo receives actual viewport visual acceptance.

## Build chain

`V1.8.4 source` → `V1.8.4.1 activation hotfix` → `V1.8.5 Auto-Tuner` → `V1.8.5 stale guard` → `V1.8.5.1 Twist Visual Recovery` → SHA-256 verification → Pages artifact
