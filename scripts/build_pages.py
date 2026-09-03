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
from patch_v1_8_4_1 import patch
html = patch(html)

if 'Character Prototype Studio V1.8.4.1' not in html:
    raise SystemExit('V1.8.4.1 twist activation patch failed')

expected = '3e84a4e259dd7fcec4976bb000c59d0a0911c0249f07d6fd30b2b940cdfd51a2'
actual = hashlib.sha256(html.encode('utf-8')).hexdigest()
if actual != expected:
    raise SystemExit(f'V1.8.4.1 source checksum mismatch: {actual}')

site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)
(site / 'index.html').write_text(html, encoding='utf-8')
if (root / 'assets').exists():
    shutil.copytree(root / 'assets', site / 'assets', dirs_exist_ok=True)
(site / '.nojekyll').write_text('', encoding='utf-8')
print(f'Built V1.8.4.1 {len(html.encode("utf-8"))} bytes from V1.8.4 + hotfix patch')
print('sha256', actual)
