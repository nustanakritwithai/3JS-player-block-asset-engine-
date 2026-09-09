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

    old_sockets = r'''function pocketStudioSockets(){return {
  rightHand:{joint:pocketStudioJoint(["handR","wristR","elbowR"]),offset:[0,0,0]},leftHand:{joint:pocketStudioJoint(["handL","wristL","elbowL"]),offset:[0,0,0]},
  head:{joint:pocketStudioJoint(["head","neck"]),offset:[0,0,0]},back:{joint:pocketStudioJoint(["chest","spine","pelvis"]),offset:[0,0,.12]},waist:{joint:pocketStudioJoint(["pelvis","chest"]),offset:[0,0,0]},
  vfxOrigin:{joint:pocketStudioJoint(["chest","pelvis"]),offset:[0,.12,-.18]},attackOrigin:{joint:pocketStudioJoint(["handR","wristR","elbowR"]),offset:[0,0,-.08]},throwOrigin:{joint:pocketStudioJoint(["handR","wristR","elbowR"]),offset:[0,0,-.08]}}}'''
    new_sockets = r'''const POCKET_STUDIO_SOCKET_TRANSFORM_SCHEMA="studio-socket-transform-v1";
const POCKET_STUDIO_WEAPON_ATTACHMENT_SCHEMA="studio-weapon-attachment-v1";
function pocketStudioSocket(joint,offset,quaternion=[0,0,0,1]){
  return {schema:POCKET_STUDIO_SOCKET_TRANSFORM_SCHEMA,joint,offset:[...offset],quaternion:[...quaternion]};
}
function pocketStudioSockets(){
  const right=pocketStudioJoint(["wristR","handR","elbowR"]),left=pocketStudioJoint(["wristL","handL","elbowL"]);
  const rightGrip=right==="wristR"?[0,-.34,.10]:[0,0,0],leftGrip=left==="wristL"?[0,-.34,.10]:[0,0,0];
  const rightOrigin=[rightGrip[0],rightGrip[1],rightGrip[2]-.08];
  return {
    rightHand:pocketStudioSocket(right,rightGrip),leftHand:pocketStudioSocket(left,leftGrip),
    weaponGripR:pocketStudioSocket(right,rightGrip),weaponGripL:pocketStudioSocket(left,leftGrip),
    head:pocketStudioSocket(pocketStudioJoint(["head","neck"]),[0,0,0]),
    back:pocketStudioSocket(pocketStudioJoint(["chest","spine","pelvis"]),[0,0,.12]),
    waist:pocketStudioSocket(pocketStudioJoint(["pelvis","chest"]),[0,0,0]),
    vfxOrigin:pocketStudioSocket(pocketStudioJoint(["chest","pelvis"]),[0,.12,-.18]),
    attackOrigin:pocketStudioSocket(right,rightOrigin),throwOrigin:pocketStudioSocket(right,rightOrigin)
  };
}
function pocketStudioWeaponAttachmentContract(){
  return {schema:POCKET_STUDIO_WEAPON_ATTACHMENT_SCHEMA,version:"1.0.0",presentationOnly:true,
    socketSchema:POCKET_STUDIO_SOCKET_TRANSFORM_SCHEMA,socketSpace:"joint-local",orientation:"quaternion-xyzw",
    primarySocket:"weaponGripR",secondarySocket:"weaponGripL",composition:"characterSocket * inverse(weaponGrip)",
    sourceOfTruth:"character-engine"};
}'''
    if old_sockets not in html:
        raise RuntimeError('missing legacy Pocket socket exporter')
    html = html.replace(old_sockets, new_sockets, 1)

    extension = r'''const POCKET_STUDIO_SOLVER_RUNTIME_SCHEMA="studio-solver-runtime-v1";
const POCKET_STUDIO_SOLVER_RUNTIME_VERSION="1.0.0";
const POCKET_STUDIO_SOLVER_RUNTIME_SHA256="__POCKET_STUDIO_SOLVER_RUNTIME_SHA256__";
const POCKET_STUDIO_SOLVER_RUNTIME_CHAIN=Object.freeze([
  "sample-blend","pelvis-weight","upper-body-weight","locomotion-dynamics","attack-weight",
  "body-dynamics","impact","momentum","equipment","foot-plant-leg-response"
]);
function pocketStudioSolverRuntimeContract(){
  const runtime=spec?.animationRuntime||{};
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
      defaultState:String(runtime.defaultState||"idle"),
      transitionDefault:Number.isFinite(Number(runtime.transitionDefault))?Number(runtime.transitionDefault):.15,
      weight:pocketStudioSanitize(spec?.weight||{})||{},
      footPlantLegResponse:pocketStudioSanitize(spec?.footPlantLegResponse||{})||{},
      momentum:pocketStudioSanitize(runtime.momentum||{})||{},
      equipment:pocketStudioSanitize(spec?.weight?.equipment||{})||{}
    }
  };
}
'''
    html = html.replace(anchor, extension + '\n' + anchor, 1)

    old = '    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),jointBindings:pocketStudioJointBindings(characterRoot),sockets:pocketStudioSockets()},\n    motionPack:'
    new = '    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),jointBindings:pocketStudioJointBindings(characterRoot),sockets:pocketStudioSockets(),attachmentContract:pocketStudioWeaponAttachmentContract()},\n    solverRuntime:pocketStudioSolverRuntimeContract(),\n    motionPack:'
    if old not in html:
        raise RuntimeError('missing rig/motionPack package anchor')
    html = html.replace(old, new, 1)
    return html
