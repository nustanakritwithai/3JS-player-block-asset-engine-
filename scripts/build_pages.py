#!/usr/bin/env python3
from pathlib import Path
import base64, lzma, shutil, hashlib

root = Path(__file__).resolve().parents[1]
parts_dir = root / 'deploy' / 'source_v1_8_4' / 'parts'
parts = sorted(parts_dir.glob('studio_v1_8_4.html.xz.b64.part*'))
if not parts:
    raise SystemExit('No V1.8.4 source parts found')

encoded = ''.join(p.read_text(encoding='ascii').strip() for p in parts)
html = lzma.decompress(base64.b64decode(encoded))
if b'Character Prototype Studio V1.8.4' not in html:
    raise SystemExit('Reconstructed source is not V1.8.4')

expected = 'd55bd0beca0839bd59fb45a827879293bde6c15de372826bafe6356b2a617484'
actual = hashlib.sha256(html).hexdigest()
if actual != expected:
    raise SystemExit(f'V1.8.4 source checksum mismatch: {actual}')

site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)
(site / 'index.html').write_bytes(html)
if (root / 'assets').exists():
    shutil.copytree(root / 'assets', site / 'assets', dirs_exist_ok=True)
(site / '.nojekyll').write_text('', encoding='utf-8')
print(f'Built V1.8.4 {len(html)} bytes from {len(parts)} source parts')
print('sha256', actual)
