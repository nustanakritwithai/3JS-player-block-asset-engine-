#!/usr/bin/env python3
from pathlib import Path


def _function_end(source: str, signature: str) -> int:
    start = source.index(signature)
    brace = source.index('{', start)
    depth = 0
    quote = None
    escape = False
    line_comment = False
    block_comment = False
    i = brace
    while i < len(source):
        ch = source[i]
        nxt = source[i+1] if i+1 < len(source) else ''
        if line_comment:
            if ch == '\n': line_comment = False
            i += 1; continue
        if block_comment:
            if ch == '*' and nxt == '/': block_comment = False; i += 2; continue
            i += 1; continue
        if quote:
            if escape: escape = False
            elif ch == '\\': escape = True
            elif ch == quote: quote = None
            i += 1; continue
        if ch == '/' and nxt == '/': line_comment = True; i += 2; continue
        if ch == '/' and nxt == '*': block_comment = True; i += 2; continue
        if ch in ('\"', "'", '`'): quote = ch; i += 1; continue
        if ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: return i + 1
        i += 1
    raise RuntimeError('unterminated function: ' + signature)


def patch(html: str, factory_source: str) -> str:
    if 'function buildCharacter(preserve=true){' not in html:
        raise RuntimeError('missing buildCharacter anchor')
    if 'function createBlueExplorer(THREE)' in html:
        raise RuntimeError('Blue Explorer already injected')

    html = html.replace('function buildCharacter(preserve=true){', 'function buildLegacyCharacter(preserve=true){', 1)
    legacy_end = _function_end(html, 'function buildLegacyCharacter(preserve=true){')

    adapter = r'''
let blueExplorerInstance=null;
const BLUE_EXPLORER_PRIMARY_ID="blue-explorer-primary-v1";
function blueExplorerRetargetMaterialRoles(model){
  for(const material of model?.materials||[]){
    const original=String(material.name||"");material.userData??={};material.userData.blueExplorerOriginalName=original;
    const n=original.toLowerCase();
    if(n.includes("skin")||n.includes("mouth"))material.name="skin";
    else if(n.includes("eye"))material.name="eyes";
    else if(n.includes("hair")||n.includes("brow"))material.name="hair";
    else if(n.includes("navy")||n.includes("trouser"))material.name="pants";
    else if(n.includes("leather")||n.includes("sole")||n.includes("pouch"))material.name="boots";
    else if(n.includes("jacket")||n.includes("shirt")||n.includes("cuff")||n.includes("blue"))material.name="shirt";
    else material.name="accent";
  }
}
function blueExplorerMovePivotKeepWorld(group,x,y,z){
  const dx=x-group.position.x,dy=y-group.position.y,dz=z-group.position.z;
  for(const child of group.children){child.position.x-=dx;child.position.y-=dy;child.position.z-=dz}
  group.position.set(x,y,z);
}
function blueExplorerRegisterJoint(key,node){
  if(!node)throw new Error(`Blue Explorer joint missing: ${key}`);
  node.rotation.set(0,0,0);
  const base=node.position.toArray(),off=spec.skeleton?.pivotOffsets?.[key]||[0,0,0];
  node.userData.basePivot=[...base];
  node.position.set(base[0]+(off[0]||0),base[1]+(off[1]||0),base[2]+(off[2]||0));
  node.userData.restLocalPosition=node.position.toArray();
  node.userData.restLocalRotation=[0,0,0];
  node.userData.engineJointKey=key;
  joints[key]=node;
  return node;
}
function buildBlueExplorerPrimaryCharacter(preserve=true){
  if(gameRuntimeState.playing||gameRuntimeState.basePose)runtimePreviewStop(true);
  if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);
  if(motionState.playing)stopMotionPreview(true);
  const oldPose=preserve?capturePose():(spec.pose.joints||{});
  if(blueExplorerInstance){
    characterRoot.remove(blueExplorerInstance.root);
    try{blueExplorerInstance.dispose?.()}catch(err){console.warn("Blue Explorer dispose",err)}
    blueExplorerInstance=null;
  }
  clearCharacter();makeMaterials();
  try{
    const model=createBlueExplorer(THREE);blueExplorerInstance=model;
    const r=model.rig;
    characterRoot.scale.setScalar(spec.proportions.overallScale);
    characterRoot.add(model.root);
    model.root.userData.primaryCharacter=BLUE_EXPLORER_PRIMARY_ID;
    model.root.userData.engineRole="primary-character";
    characterRoot.userData.primaryCharacter=BLUE_EXPLORER_PRIMARY_ID;

    blueExplorerMovePivotKeepWorld(r.pelvis,0,1.985,0);
    blueExplorerMovePivotKeepWorld(r.torso,0,2.165,0);
    r.pelvis.attach(r.torso);
    r.torso.attach(r.shoulder_left);r.torso.attach(r.shoulder_right);r.torso.attach(r.neck);
    r.pelvis.attach(r.hip_left);r.pelvis.attach(r.hip_right);
    if(model.parts?.pouch)r.pelvis.attach(model.parts.pouch);

    blueExplorerRegisterJoint("pelvis",r.pelvis);
    blueExplorerRegisterJoint("chest",r.torso);
    blueExplorerRegisterJoint("neck",r.neck);
    blueExplorerRegisterJoint("head",r.head);
    blueExplorerRegisterJoint("shoulderL",r.shoulder_right);
    blueExplorerRegisterJoint("elbowL",r.elbow_right);
    blueExplorerRegisterJoint("wristL",r.wrist_right);
    blueExplorerRegisterJoint("shoulderR",r.shoulder_left);
    blueExplorerRegisterJoint("elbowR",r.elbow_left);
    blueExplorerRegisterJoint("wristR",r.wrist_left);
    blueExplorerRegisterJoint("hipL",r.hip_right);
    blueExplorerRegisterJoint("kneeL",r.knee_right);
    blueExplorerRegisterJoint("ankleL",r.ankle_right);
    blueExplorerRegisterJoint("hipR",r.hip_left);
    blueExplorerRegisterJoint("kneeR",r.knee_left);
    blueExplorerRegisterJoint("ankleR",r.ankle_left);

    blueExplorerRetargetMaterialRoles(model);
    model.root.traverse(o=>{if(o.isMesh){o.castShadow=spec.look.shadows;o.receiveShadow=spec.look.shadows;meshes.push(o);partCounter++}});

    socket(characterRoot,"root",[0,0,0]);
    socket(joints.chest,"chest",[0,.73,.42]);socket(joints.chest,"back",[0,.62,-.42]);
    socket(joints.head,"head",[0,.74,0]);
    socket(joints.wristL,"hand.L",[0,-.34,.10]);socket(joints.wristR,"hand.R",[0,-.34,.10]);
    socket(joints.ankleL,"foot.L",[0,-.40,.45]);socket(joints.ankleR,"foot.R",[0,-.40,.45]);

    compensatePivotOnly();
    applyCapturedPose(oldPose);
    if(!Object.keys(oldPose||{}).length)applyPose("idle");
    refreshHierarchy();
    selectJoint(selectedJoint in joints?selectedJoint:"pelvis");
    updatePartCount();
    if($("#animationClipSelect"))buildAnimationUI(false);
  }catch(error){
    console.error("Blue Explorer primary character failed; using Legacy/Debug character",error);
    if(blueExplorerInstance){characterRoot.remove(blueExplorerInstance.root);try{blueExplorerInstance.dispose?.()}catch{}blueExplorerInstance=null}
    characterRoot.userData.primaryCharacter="legacy-debug-fallback";
    return buildLegacyCharacter(preserve);
  }
}
function buildCharacter(preserve=true){return buildBlueExplorerPrimaryCharacter(preserve)}
'''
    injection = '\n' + factory_source.strip() + '\n\n' + adapter + '\n'
    html = html[:legacy_end] + injection + html[legacy_end:]

    html = html.replace('Character Prototype Studio V1.8.10.4', 'Character Prototype Studio V1.8.10.5')
    html = html.replace('V1.8.10.4 · Baseball Throw Motion Hotfix', 'V1.8.10.5 · Blue Explorer Primary Character')
    html = html.replace('studioVersion:"1.8.10.4"', 'studioVersion:"1.8.10.5"')
    return html
