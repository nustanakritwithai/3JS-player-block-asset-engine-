#!/usr/bin/env python3
from pathlib import Path
import base64, lzma, shutil, hashlib, json, sys

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
from patch_pocket_studio_live_bridge import patch as patch_pocket_studio_live_bridge
from patch_pocket_studio_material_pack import patch as patch_pocket_studio_material_pack
from patch_v1_8_10_5_blue_explorer import patch as patch_v1_8_10_5_blue_explorer

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
base_actual = hashlib.sha256(html.encode('utf-8')).hexdigest()
if base_actual != expected:
    raise SystemExit(f'V1.8.10.4 source checksum mismatch: {base_actual}')

html = patch_pocket_studio_live_bridge(html)
html = patch_pocket_studio_material_pack(html)
texture_root = root / 'assets' / 'textures'
texture_integrity = {
    path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(texture_root.rglob('*'))
    if path.is_file() and path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}
}
marker = '__POCKET_STUDIO_TEXTURE_INTEGRITY__'
if marker not in html:
    raise SystemExit('Pocket Studio texture integrity marker missing')
html = html.replace(marker, json.dumps(texture_integrity, sort_keys=True, separators=(',', ':')), 1)
bridge_tokens = [
    'POCKET_STUDIO_CHARACTER_REQUEST',
    'POCKET_STUDIO_CHARACTER_PACKAGE',
    'window.POCKET_STUDIO_CHARACTER_BRIDGE',
    'pocket-character-runtime-v1',
    'three-group-scenegraph-v1',
    'provider:"studio-character"',
    'gameplayPolicy:{included:false',
    'POCKET_STUDIO_TEXTURE_INTEGRITY=',
    'studio-starter-pbr-2k-v1',
    'colorDataSeparated:true',
]
for token in bridge_tokens:
    if token not in html:
        raise SystemExit('Pocket Studio live bridge patch failed: ' + token)

blue_parts = sorted((root / 'assets' / 'characters').glob('blue_explorer_factory.js.xz.b64.part*'))
if len(blue_parts) != 4:
    raise SystemExit(f'Expected 4 Blue Explorer factory parts, found {len(blue_parts)}')
blue_encoded = ''.join(p.read_text(encoding='ascii').strip() for p in blue_parts)
blue_factory = lzma.decompress(base64.b64decode(blue_encoded)).decode('utf-8')
blue_factory_sha = hashlib.sha256(blue_factory.encode('utf-8')).hexdigest()
if blue_factory_sha != '7bb50a22bf892f8f79200d732e9aa1b00b22b0a046e37070122818ed343b76d2':
    raise SystemExit(f'Blue Explorer factory checksum mismatch: {blue_factory_sha}')
html = patch_v1_8_10_5_blue_explorer(html, blue_factory)

blue_tokens = [
    'Character Prototype Studio V1.8.10.5',
    'BLUE_EXPLORER_PRIMARY_ID="blue-explorer-primary-v1"',
    'function createBlueExplorer(THREE)',
    'function buildLegacyCharacter(preserve=true){',
    'function buildBlueExplorerPrimaryCharacter(preserve=true){',
    'function buildCharacter(preserve=true){return buildBlueExplorerPrimaryCharacter(preserve)}',
    'blueExplorerRegisterJoint("wristR",r.wrist_left)',
    'socket(joints.wristR,"hand.R",[0,-.34,.10])',
    'model.root.userData.engineRole="primary-character"',
    'throwStyle:"overhand-baseball"',
    'POCKET_STUDIO_CHARACTER_REQUEST',
]
for token in blue_tokens:
    if token not in html:
        raise SystemExit('Blue Explorer primary-character patch failed: ' + token)

actual = hashlib.sha256(html.encode('utf-8')).hexdigest()
expected_blue = '43ee6d2bbb726dffedb60468b6f21fd9cf50886481be4f4fa50e9c9d2a039b5c'
if actual != expected_blue:
    raise SystemExit(f'V1.8.10.5 source checksum mismatch: {actual}')

site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)
(site / 'index.html').write_text(html, encoding='utf-8')
if (root / 'assets').exists():
    shutil.copytree(root / 'assets', site / 'assets', dirs_exist_ok=True)
(site / '.nojekyll').write_text('', encoding='utf-8')
print(f'Built V1.8.10.5 Blue Explorer Primary + Pocket Studio live bridge {len(html.encode("utf-8"))} bytes')
print('base-v1.8.10.4-sha256', base_actual)
print('blue-explorer-factory-sha256', blue_factory_sha)
print('sha256', actual)
