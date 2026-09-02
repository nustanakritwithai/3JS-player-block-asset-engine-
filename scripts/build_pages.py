#!/usr/bin/env python3
from pathlib import Path
import base64, lzma, shutil, hashlib

root=Path(__file__).resolve().parents[1]
parts=sorted((root/'deploy'/'source_v1_8'/'parts').glob('studio_v1_8.html.xz.b64.part*'))
if not parts:
    raise SystemExit('No V1.8 source parts found')
encoded=''.join(p.read_text(encoding='ascii').strip() for p in parts)
html=lzma.decompress(base64.b64decode(encoded))
if b'Character Prototype Studio V1.8' not in html:
    raise SystemExit('Reconstructed source is not V1.8')
site=root/'_site'
if site.exists(): shutil.rmtree(site)
site.mkdir(parents=True)
(site/'index.html').write_bytes(html)
if (root/'assets').exists(): shutil.copytree(root/'assets',site/'assets',dirs_exist_ok=True)
(site/'.nojekyll').write_text('',encoding='utf-8')
print(f'Built {site}/index.html ({len(html)} bytes) from {len(parts)} source parts')
print('sha256',hashlib.sha256(html).hexdigest())
