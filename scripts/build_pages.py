#!/usr/bin/env python3
from pathlib import Path
import base64, lzma, shutil, hashlib, json, sys, re

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
from patch_v1_8_10_6_solver_runtime import patch as patch_v1_8_10_6_solver_runtime
from patch_v1_8_10_7_tripo_primary import patch as patch_v1_8_10_7_tripo_primary
from compile_tripo_rigid import compile_glb

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

v18105_actual = hashlib.sha256(html.encode('utf-8')).hexdigest()
expected_blue = 'e624b724c47b0adf50c762f350ff4e92188af63317f83f9ff601f38ae8be5a47'
if v18105_actual != expected_blue:
    raise SystemExit(f'V1.8.10.5 source checksum mismatch: {v18105_actual}')

html = patch_v1_8_10_6_solver_runtime(html)

# Generate the canonical solver module from the exact same standalone runtime source
# embedded by Character Studio. Only the manifest literal is replaced by neutral
# defaults so PocketMonster can provide the exported package options at runtime.
start = html.index('function gameRuntimeCode(){')
source_start = html.index('  return `', start) + len('  return `')
source_end = html.index('\n`;\n}\nfunction exportGameRuntime', source_start)
solver_source = html[source_start:source_end]
solver_source = re.sub(
    r'export const ANIMATION_RUNTIME_MANIFEST = \$\{JSON\.stringify\(manifest,null,2\)\};',
    'export const ANIMATION_RUNTIME_MANIFEST = Object.freeze({\n  defaultState:"idle", transitionDefault:.15, weight:{}, footPlantLegResponse:{}, momentum:{}, equipment:{}, states:[]\n});',
    solver_source,
    count=1,
)
solver_source = re.sub(
    r'^// Generated by Character Prototype Studio V1\.8\.10\.6\n// Standalone rigid-rig animation runtime for a model created by the Studio\.',
    '// Canonical Studio Solver Runtime v1\n// Source-identical to Character Prototype Studio standalone solver chain.',
    solver_source,
    count=1,
)
solver_sha = hashlib.sha256(solver_source.encode('utf-8')).hexdigest()
solver_marker = '__POCKET_STUDIO_SOLVER_RUNTIME_SHA256__'
if solver_marker not in html:
    raise SystemExit('solver runtime checksum marker missing')
html = html.replace(solver_marker, solver_sha, 1)

solver_tokens = [
    'Character Prototype Studio V1.8.10.6',
    'studio-solver-runtime-v1',
    'same-standalone-runtime-source',
    'assets/runtime/studio-solver-runtime-v1.mjs',
    '"sample-blend","pelvis-weight","upper-body-weight","locomotion-dynamics","attack-weight"',
    '"body-dynamics","impact","momentum","equipment","foot-plant-leg-response"',
    'solverRuntime:pocketStudioSolverRuntimeContract()',
]
for token in solver_tokens:
    if token not in html:
        raise SystemExit('V1.8.10.6 solver runtime patch failed: ' + token)

# V1.8.10.7 promotes the user-selected Tripo GLB while preserving Blue Explorer
# as a deterministic fallback. The source GLB is compiled into rigid regions at
# build time; the browser only reconstructs THREE.Group/BufferGeometry/PBR data.
html = patch_v1_8_10_7_tripo_primary(html)
tripo_tokens = [
    'Character Prototype Studio V1.8.10.7',
    'TRIPO_PRIMARY_ID="tripo-5889e73e-rigid-v1"',
    'TRIPO_PRIMARY_SOURCE="assets/imports/tripo_5889e73e/tripo_5889e73e.glb"',
    'TRIPO_PRIMARY_DESCRIPTOR_URL="./assets/runtime/tripo_5889e73e/rigid-model.json"',
    'function buildTripoPrimaryCharacter(preserve=true){',
    'function buildCharacter(preserve=true){return buildTripoPrimaryCharacter(preserve)}',
    'return buildBlueExplorerPrimaryCharacter(preserve)',
    'socket(joints.wristR,"hand.R",[0,-.34,.10])',
    'socket(joints.ankleR,"foot.R",[0,-.40,.45])',
    'sourceCharacter:"tripo-5889e73e-rigid-v1"',
    'studio-rigid-glb-v1',
]
for token in tripo_tokens:
    if token not in html:
        raise SystemExit('V1.8.10.7 Tripo primary adapter failed: ' + token)

site = root / '_site'
if site.exists():
    shutil.rmtree(site)
site.mkdir(parents=True)
if (root / 'assets').exists():
    shutil.copytree(root / 'assets', site / 'assets', dirs_exist_ok=True)

tripo_source = root / 'assets' / 'imports' / 'tripo_5889e73e' / 'tripo_5889e73e.glb'
if not tripo_source.is_file():
    raise SystemExit('Tripo primary source GLB missing')
tripo_runtime_dir = site / 'assets' / 'runtime' / 'tripo_5889e73e'
tripo_descriptor = compile_glb(tripo_source, tripo_runtime_dir)
tripo_stats = tripo_descriptor['stats']
if tripo_stats['sourceVertices'] != 34566:
    raise SystemExit(f"Tripo source vertex count mismatch: {tripo_stats['sourceVertices']}")
if tripo_stats['sourceTriangles'] != 46897:
    raise SystemExit(f"Tripo source triangle count mismatch: {tripo_stats['sourceTriangles']}")
if tripo_stats['rigidTriangles'] != tripo_stats['sourceTriangles']:
    raise SystemExit('Tripo rigid partition did not preserve every source triangle')
required_regions = ['pelvis','chest','head','upperArmL','lowerArmL','handL','upperArmR','lowerArmR','handR','thighL','shinL','footL','thighR','shinR','footR']
missing_regions = [name for name in required_regions if tripo_stats['regions'].get(name, 0) <= 0]
if missing_regions:
    raise SystemExit('Tripo rigid partition empty region(s): ' + ','.join(missing_regions))

(site / 'index.html').write_text(html, encoding='utf-8')
solver_path = site / 'assets' / 'runtime' / 'studio-solver-runtime-v1.mjs'
solver_path.parent.mkdir(parents=True, exist_ok=True)
solver_path.write_text(solver_source, encoding='utf-8')
(site / '.nojekyll').write_text('', encoding='utf-8')
actual = hashlib.sha256(html.encode('utf-8')).hexdigest()
print(f'Built V1.8.10.7 Tripo primary rigid adapter {len(html.encode("utf-8"))} bytes')
print('base-v1.8.10.4-sha256', base_actual)
print('v1.8.10.5-sha256', v18105_actual)
print('blue-explorer-factory-sha256', blue_factory_sha)
print('solver-runtime-sha256', solver_sha)
print('tripo-source-vertices', tripo_stats['sourceVertices'])
print('tripo-source-triangles', tripo_stats['sourceTriangles'])
print('tripo-rigid-regions', json.dumps(tripo_stats['regions'], sort_keys=True))
print('sha256', actual)
