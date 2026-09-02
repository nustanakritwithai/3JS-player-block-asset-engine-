#!/usr/bin/env python3
from pathlib import Path
import sys, json
from PIL import Image

folder=Path(sys.argv[1] if len(sys.argv)>1 else 'assets/textures')
minimum=int(sys.argv[2] if len(sys.argv)>2 else 2048)
rows=[]; failures=[]
for path in sorted(folder.glob('*')):
    if path.suffix.lower() not in {'.png','.webp','.jpg','.jpeg'}: continue
    with Image.open(path) as im: w,h=im.size
    rows.append({'file':path.name,'width':w,'height':h})
    if min(w,h)<minimum: failures.append(f'{path.name}: {w}x{h} < {minimum}')
report={'minimum':minimum,'pixelArtAllowed':False,'count':len(rows),'passed':not failures,'textures':rows,'failures':failures}
(folder/'quality_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'count':len(rows),'minimum':minimum,'passed':not failures},indent=2))
if failures:
    print('\n'.join(failures),file=sys.stderr);sys.exit(1)
