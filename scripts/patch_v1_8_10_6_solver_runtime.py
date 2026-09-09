#!/usr/bin/env python3


def patch(html: str) -> str:
    html = html.replace('Character Prototype Studio V1.8.10.5', 'Character Prototype Studio V1.8.10.6')
    html = html.replace('V1.8.10.5 · Blue Explorer Primary Character', 'V1.8.10.6 · Shared Solver Runtime')
    html = html.replace('studioVersion:"1.8.10.5"', 'studioVersion:"1.8.10.6"')

    anchor = 'function buildPocketStudioCharacterPackage(request={}){'
    if anchor not in html:
        raise RuntimeError('missing Pocket package builder anchor')
    if 'studio-solver-runtime-v1' in html:
        raise RuntimeError('solver runtime contract already injected')

    extension = r'''const POCKET_STUDIO_SOLVER_RUNTIME_SCHEMA="studio-solver-runtime-v1";
const POCKET_STUDIO_SOLVER_RUNTIME_VERSION="1.0.0";
const POCKET_STUDIO_SOLVER_RUNTIME_SHA256="__POCKET_STUDIO_SOLVER_RUNTIME_SHA256__";
const POCKET_STUDIO_SOLVER_RUNTIME_CHAIN=Object.freeze([
  "sample-blend","pelvis-weight","upper-body-weight","locomotion-dynamics","attack-weight",
  "body-dynamics","impact","momentum","equipment","foot-plant-leg-response"
]);
function pocketStudioSolverRuntimeContract(){
  const runtime=runtimeManifest();
  return {
    schema:POCKET_STUDIO_SOLVER_RUNTIME_SCHEMA,
    version:POCKET_STUDIO_SOLVER_RUNTIME_VERSION,
    source:new URL("assets/runtime/studio-solver-runtime-v1.mjs",location.href).href,
    sha256:POCKET_STUDIO_SOLVER_RUNTIME_SHA256,
    sourceStudioVersion:"1.8.10.6",
    sourceCharacter:"blue-explorer-primary-v1",
    chain:[...POCKET_STUDIO_SOLVER_RUNTIME_CHAIN],
    parity:"same-standalone-runtime-source",
    options:{
      defaultState:runtime.defaultState,
      transitionDefault:runtime.transitionDefault,
      weight:pocketStudioSanitize(runtime.weight||{})||{},
      footPlantLegResponse:pocketStudioSanitize(runtime.footPlantLegResponse||{})||{},
      momentum:pocketStudioSanitize(runtime.momentum||{})||{},
      equipment:pocketStudioSanitize(runtime.equipment||{})||{}
    }
  };
}
'''
    html = html.replace(anchor, extension + '\n' + anchor, 1)

    old = '    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),jointBindings:pocketStudioJointBindings(characterRoot),sockets:pocketStudioSockets()},\n    motionPack:'
    new = '    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),jointBindings:pocketStudioJointBindings(characterRoot),sockets:pocketStudioSockets()},\n    solverRuntime:pocketStudioSolverRuntimeContract(),\n    motionPack:'
    if old not in html:
        raise RuntimeError('missing rig/motionPack package anchor')
    html = html.replace(old, new, 1)
    return html
