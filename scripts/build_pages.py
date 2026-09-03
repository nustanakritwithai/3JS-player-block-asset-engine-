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

html = patch_v1_8_4_1(html)
if 'Character Prototype Studio V1.8.4.1' not in html:
    raise SystemExit('V1.8.4.1 twist activation patch failed')

html = patch_v1_8_5(html)
if 'Character Prototype Studio V1.8.5' not in html or 'DYNAMICS AUTO-TUNER' not in html:
    raise SystemExit('V1.8.5 Dynamics Auto-Tuner patch failed')

expected = '7c4d6e01c75c777e94714411b8b4e529e32d3282a311b192470c5dc4d09619e6'
actual = hashlib.sha256(html.encode('utf-8')).hexdigest()
if actual != expected:
    raise SystemExit(f'V1.8.5 source checksum mismatch: {actual}')

site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)
(site / 'index.html').write_text(html, encoding='utf-8')
if (root / 'assets').exists():
    shutil.copytree(root / 'assets', site / 'assets', dirs_exist_ok=True)
(site / '.nojekyll').write_text('', encoding='utf-8')
print(f'Built V1.8.5 {len(html.encode("utf-8"))} bytes from V1.8.4 + V1.8.4.1 + V1.8.5 patches')
print('sha256', actual)
