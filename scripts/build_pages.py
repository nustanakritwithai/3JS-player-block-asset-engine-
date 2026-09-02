#!/usr/bin/env python3
from pathlib import Path
import lzma, shutil

root=Path(__file__).resolve().parents[1]
src=root/'deploy'/'source_v1_8'/'studio_v1_8.html.xz'
if not src.exists():
    raise SystemExit('Missing V1.8 compressed source')
html=lzma.decompress(src.read_bytes())
site=root/'_site'
if site.exists(): shutil.rmtree(site)
site.mkdir(parents=True)
(site/'index.html').write_bytes(html)
if (root/'assets').exists(): shutil.copytree(root/'assets',site/'assets',dirs_exist_ok=True)
(site/'.nojekyll').write_text('',encoding='utf-8')
print(f'Built {site}/index.html ({len(html)} bytes)')
