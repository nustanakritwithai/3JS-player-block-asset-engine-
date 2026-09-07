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
from patch_v1_8_10_1 import patch as patch_v1_8_10_1
from patch_v1_8_10_2 import patch as patch_v1_8_10_2
from patch_v1_8_10_3 import patch as patch_v1_8_10_3
from patch_v1_8_10_4 import patch as patch_v1_8_10_4

html = patch_v1_8_4_1(html)
html = patch_v1_8_5(html)
html = patch_v1_8_5_guard(html)
html = patch_v1_8_5_1(html)
html = patch_v1_8_5_2(html)
html = patch_v1_8_5_3(html)
html = patch_v1_8_6(html)
html = patch_v1_8_7(html)
html = patch_v1_8_8(html)
html = patch_v1_8_9(html)
html = patch_v1_8_10(html)
html = patch_v1_8_10_1(html)
html = patch_v1_8_10_2(html)
html = patch_v1_8_10_3(html)
html = patch_v1_8_10_4(html)

if 'Character Prototype Studio V1.8.10.4' not in html or 'throwStyle:"overhand-baseball"' not in html or 'style:"overhead"' not in html:
    raise SystemExit('V1.8.10.4 Baseball Throw Motion Hotfix patch failed')

expected = 'fa11b83a76efad0ee8480ab1f02e4b8a2461939442795170d28d6595f18a7616'
actual = hashlib.sha256(html.encode('utf-8')).hexdigest()
if actual != expected:
    raise SystemExit(f'V1.8.10.4 source checksum mismatch: {actual}')

site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)
(site / 'index.html').write_text(html, encoding='utf-8')
if (root / 'assets').exists():
    shutil.copytree(root / 'assets', site / 'assets', dirs_exist_ok=True)
(site / '.nojekyll').write_text('', encoding='utf-8')
print(f'Built V1.8.10.4 {len(html.encode("utf-8"))} bytes')
print('sha256', actual)
