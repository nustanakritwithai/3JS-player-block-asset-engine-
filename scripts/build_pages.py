#!/usr/bin/env python3
from pathlib import Path
import base64, lzma, shutil, hashlib, sys

root = Path(__file__).resolve().parents[1]
parts_dir = root / 'deploy' / 'source_v1_8_4' / 'parts'
parts = sorted(parts_dir.glob('studio_v1_8_4.html.xz.b64.part*'))
if not parts:
    raise SystemExit('No V1.8.4 source parts found')

encoded = ''.join(p.read_text(encoding='ascii').strip() for p in parts)
html = lzma.decompress(base64.b64decode(encoded)).decode('utf-8')
if 'Character Prototype Studio V1.8.4' not in html:
    raise SystemExit('Reconstructed source is not V1.8.4')

sys.path.insert(0, str(root / 'scripts'))
from patch_v1_8_4_1 import patch as patch_v1_8_4_1
from patch_v1_8_5 import patch as patch_v1_8_5
from patch_v1_8_5_guard import patch as patch_v1_8_5_guard
from patch_v1_8_5_1 import patch as patch_v1_8_5_1
from patch_v1_8_5_2 import patch as patch_v1_8_5_2
from patch_v1_8_5_3 import patch as patch_v1_8_5_3
from patch_v1_8_6 import patch as patch_v1_8_6
from patch_v1_8_7 import patch as patch_v1_8_7
from patch_v1_8_8 import patch as patch_v1_8_8
from patch_v1_8_9 import patch as patch_v1_8_9
from patch_v1_8_10 import patch as patch_v1_8_10

html = patch_v1_8_4_1(html)
if 'Character Prototype Studio V1.8.4.1' not in html:
    raise SystemExit('V1.8.4.1 twist activation patch failed')

html = patch_v1_8_5(html)
html = patch_v1_8_5_guard(html)
if 'Character Prototype Studio V1.8.5' not in html or 'DYNAMICS AUTO-TUNER' not in html:
    raise SystemExit('V1.8.5 Dynamics Auto-Tuner patch failed')

html = patch_v1_8_5_1(html)
if 'Character Prototype Studio V1.8.5.1' not in html or 'Twist_Demo_V1_8_5_1' not in html:
    raise SystemExit('V1.8.5.1 deterministic twist visual recovery patch failed')

html = patch_v1_8_5_2(html)
if 'Character Prototype Studio V1.8.5.2' not in html or 'Twist_Isolation_V1_8_5_2' not in html or 'ANIMATION LIBRARY' not in html:
    raise SystemExit('V1.8.5.2 twist isolation/library restore patch failed')

html = patch_v1_8_5_3(html)
if 'Character Prototype Studio V1.8.5.3' not in html or 'walkVisualShiftCap' not in html:
    raise SystemExit('V1.8.5.3 walk pelvis translation patch failed')

html = patch_v1_8_6(html)
if 'Character Prototype Studio V1.8.6' not in html or 'LOCOMOTION_PROFILES' not in html or 'applyLocomotionDynamicsRuntime' not in html:
    raise SystemExit('V1.8.6 Natural Locomotion Dynamics patch failed')

html = patch_v1_8_7(html)
if 'Character Prototype Studio V1.8.7' not in html or 'FOOT PLANT + LEG RESPONSE' not in html or 'applyRuntimeFootPlantLegResponse' not in html:
    raise SystemExit('V1.8.7 Foot Plant + Leg Response patch failed')

html = patch_v1_8_8(html)
if 'Character Prototype Studio V1.8.8' not in html or 'Jump_Core' not in html or 'Crouch_Walk_Core' not in html:
    raise SystemExit('V1.8.8 Core Movement Animation Pack patch failed')

html = patch_v1_8_9(html)
if 'Character Prototype Studio V1.8.9' not in html or 'createDodgeCoreTemplate' not in html or 'Interact_Core' not in html:
    raise SystemExit('V1.8.9 Core Action / Reaction Pack patch failed')

html = patch_v1_8_10(html)
if 'Character Prototype Studio V1.8.10' not in html or 'Ball Throw' not in html or 'ball.release' not in html or 'monster.summon' not in html:
    raise SystemExit('V1.8.10 Monster Ball Action Pack patch failed')

expected = 'e7371b14c1fc227399e24fcfbfa86bc83426fe50507e87ff654fb2eee2d7521b'
actual = hashlib.sha256(html.encode('utf-8')).hexdigest()
if actual != expected:
    raise SystemExit(f'V1.8.10 source checksum mismatch: {actual}')

site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)
(site / 'index.html').write_text(html, encoding='utf-8')
if (root / 'assets').exists():
    shutil.copytree(root / 'assets', site / 'assets', dirs_exist_ok=True)
(site / '.nojekyll').write_text('', encoding='utf-8')
print(f'Built V1.8.10 {len(html.encode("utf-8"))} bytes from incremental V1.8.4 → V1.8.10 patch chain')
print('sha256', actual)
