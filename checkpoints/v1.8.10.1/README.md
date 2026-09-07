# Character Prototype Studio V1.8.10.1 — Character Boot Recovery Hotfix

V1.8.10.1 is an incremental hotfix on top of V1.8.10 Monster Ball Action Pack.

## Regression addressed

Reported live symptom:

- Studio page/UI loads
- main 3D character does not appear in the viewport

## Boot reliability changes

### Multi-source Three.js loader

The Studio boot module now tries:

1. jsDelivr
2. esm.sh fallback

for:

- `three@0.169.0`
- `OrbitControls`
- `TransformControls`

Each source has an 8-second boot timeout. If both sources fail, the page shows a visible 3D-engine error overlay and reload control instead of failing silently.

### Saved-state recovery

The normal startup sequence remains:

`loadLocal → migrate → initUI → buildCharacter → applyCapturedPose → render`

If that sequence throws, V1.8.10.1:

1. backs up the previous saved state to `characterPrototypeStudio.v1.8.10.1.recoveryBackup`
2. resets only the in-memory spec to `DEFAULT`
3. rebuilds the default character
4. applies Idle
5. starts the renderer

The previous saved state is not silently discarded.

## Preserved gameplay work

No Monster Ball animation/runtime behavior is changed by this hotfix.

Preserved:

- Ball Aim Loop
- Capture Throw R/L
- Quick Throw R
- Power Throw R
- Summon Monster R
- Monster Command
- Body Dynamics `throw`
- `ball.release`
- `capture.throw`
- `monster.summon`

Also preserved:

- Twist Isolation
- Walk lateral cap `0.016m`
- Run/Sprint signatures
- Foot Plant root cap `0.028m`
- Jump/Fall/Land/Crouch
- Dodge/Hit/Knockback/Get Up/Death/Faint/Interact
- rigid `THREE.Group` rig

## Deployment gate

CI requires:

- final HTML SHA-256
- both runtime-source definitions
- timeout/fallback loader
- safe boot/recovery path
- recovery backup key
- no static Three.js import owning the initial boot path
- prior gameplay regression tokens
- module JavaScript syntax
- 2K PBR texture gate

## Next

Do not start V1.8.11 until the user confirms that the main character is visible again on the live V1.8.10.1 page.
