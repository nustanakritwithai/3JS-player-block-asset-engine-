#!/usr/bin/env python3
from pathlib import Path
import base64, lzma, shutil

root = Path(__file__).resolve().parents[1]
src_b64 = root / 'deploy' / 'source_v1_8' / 'studio_v1_8.html.xz.b64'
if not src_b64.exists():
    raise SystemExit('Missing V1.8 compressed base64 source')

try:
    compressed = base64.b64decode(src_b64.read_text(encoding='ascii'), validate=True)
    html = lzma.decompress(compressed)
except Exception as exc:
    raise SystemExit(f'Failed to reconstruct V1.8 source: {exc}')

site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)
(site / 'index.html').write_bytes(html)

if (root / 'assets').exists():
    shutil.copytree(root / 'assets', site / 'assets', dirs_exist_ok=True)

(site / '.nojekyll').write_text('', encoding='utf-8')
print(f'Built {site}/index.html ({len(html)} bytes)')
