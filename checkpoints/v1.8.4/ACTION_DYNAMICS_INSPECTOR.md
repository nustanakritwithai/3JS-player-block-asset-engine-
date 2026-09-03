# V1.8.4 — Action Dynamics Inspector

## Why this exists

A visually plausible pose at one frame can still produce an unnatural action across time.

The Inspector therefore samples the entire clip and evaluates the kinetic chain as a time series.

## Time-series channels

- Pelvis yaw
- Chest yaw
- Active shoulder yaw
- Arm composite yaw
- Head/neck counter yaw
- Pelvis visual X/Z offset
- Active hip drive

From these channels the Inspector derives angular velocity and angular acceleration.

## Kinetic-chain ordering

During the main drive window the expected order is:

Pelvis → Chest → Shoulder → Arm

The Inspector compares the peak angular-velocity times, not only static joint angles.

## Abrupt reversal

Rapid velocity sign changes can make an action look robotic even if all poses are inside joint limits.

The Inspector identifies repeated high-speed reversals within the action drive window.

## Head stabilization

Head-follow ratio compares head/neck additive rotation to total core rotation.

A high ratio means the head is being carried by the torso too strongly rather than remaining visually stabilized.

## Support / COM

The Inspector combines authored foot-contact tags with sampled COM/support-area checks.

This is especially important for Punch, Heavy Slash and Kick. Kick additionally expects the opposite foot to support the body during the main drive.

## Root ownership

Pelvis X/Z values checked here are presentation-layer additive offsets from Body Dynamics. Gameplay/world root motion remains external.

## Sensitivity

- Normal: default production tuning.
- Strict: 80% of the normal velocity/acceleration/support thresholds.
- Lenient: 125% of the normal thresholds.

Sensitivity changes do not alter the animation. They only alter QA thresholds.
