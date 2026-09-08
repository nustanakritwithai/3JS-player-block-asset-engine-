#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    anchor = 'function createAttackTemplate(){'
    if anchor not in html:
        raise RuntimeError('missing anchor: Pocket Studio live bridge')

    bridge = r'''const POCKET_STUDIO_BRIDGE_REQUEST="POCKET_STUDIO_CHARACTER_REQUEST";
const POCKET_STUDIO_BRIDGE_RESPONSE="POCKET_STUDIO_CHARACTER_PACKAGE";
const POCKET_STUDIO_BRIDGE_ERROR="POCKET_STUDIO_CHARACTER_ERROR";
/* build_pages.py replaces this marker with SHA-256 values for shipped textures. */
const POCKET_STUDIO_TEXTURE_INTEGRITY=__POCKET_STUDIO_TEXTURE_INTEGRITY__;
const POCKET_STUDIO_FORBIDDEN_KEYS=new Set([
  "hp","hpcurrent","hpmax","atk","def","spatk","spdef","spd","speed","vitality","combat","blade","ranged","fruitpower","mastery",
  "mana","coins","capture","capturechance","skill","collider","interactionradius","save","savepayload","level","exp","experience","damage"
]);
function pocketStudioKey(key){return String(key||"").replace(/[_-]/g,"").toLowerCase()}
function pocketStudioSanitize(value,seen=new WeakSet()){
  if(value===null||typeof value==="string"||typeof value==="number"||typeof value==="boolean")return value;
  if(typeof value==="undefined"||typeof value==="function"||typeof value==="symbol")return undefined;
  if(Array.isArray(value))return value.map(v=>pocketStudioSanitize(v,seen)).filter(v=>typeof v!=="undefined");
  if(typeof value==="object"){
    if(seen.has(value))return null;seen.add(value);const out={};
    for(const [key,child] of Object.entries(value)){
      if(POCKET_STUDIO_FORBIDDEN_KEYS.has(pocketStudioKey(key)))continue;
      const clean=pocketStudioSanitize(child,seen);if(typeof clean!=="undefined")out[key]=clean;
    }
    seen.delete(value);return out;
  }
  return undefined;
}
function pocketStudioTextureRef(texture){
  if(!texture)return null;const image=texture.image||texture.source?.data||null;
  const source=typeof image?.currentSrc==="string"&&image.currentSrc?image.currentSrc:typeof image?.src==="string"?image.src:null;
  const suppliedIntegrity=typeof texture?.userData?.pocketIntegritySha256==="string"?texture.userData.pocketIntegritySha256:typeof texture?.userData?.sha256==="string"?texture.userData.sha256:null;
  let builtIntegrity=null;try{const path=new URL(source,location.href).pathname;const marker="/assets/";const at=path.indexOf(marker);builtIntegrity=at>=0?POCKET_STUDIO_TEXTURE_INTEGRITY[`assets/${path.slice(at+marker.length)}`]||null:null}catch{}
  const integrity=/^[a-f0-9]{64}$/i.test(suppliedIntegrity||builtIntegrity||"")?String(suppliedIntegrity||builtIntegrity).toLowerCase():null;
  return {source,name:texture.name||null,colorSpace:texture.colorSpace||null,wrapS:texture.wrapS??null,wrapT:texture.wrapT??null,
    minFilter:texture.minFilter??null,magFilter:texture.magFilter??null,generateMipmaps:typeof texture.generateMipmaps==="boolean"?texture.generateMipmaps:null,
    anisotropy:Number.isFinite(texture.anisotropy)?texture.anisotropy:null,flipY:typeof texture.flipY==="boolean"?texture.flipY:null,
    repeat:texture.repeat?[Number(texture.repeat.x)||1,Number(texture.repeat.y)||1]:[1,1],offset:texture.offset?[Number(texture.offset.x)||0,Number(texture.offset.y)||0]:[0,0],
    center:texture.center?[Number(texture.center.x)||0,Number(texture.center.y)||0]:[0,0],rotation:Number(texture.rotation)||0,
    integrity,integrityStatus:integrity?"producer-supplied":"unavailable-in-sync-export"};
}
function pocketStudioMaterial(material){
  if(Array.isArray(material))return material.map(pocketStudioMaterial);if(!material)return null;
  const color=c=>c&&typeof c.getHexString==="function"?`#${c.getHexString()}`:null;
  return {type:material.type||"Material",name:material.name||null,color:color(material.color),emissive:color(material.emissive),emissiveIntensity:Number(material.emissiveIntensity)||0,
    roughness:Number.isFinite(material.roughness)?material.roughness:null,metalness:Number.isFinite(material.metalness)?material.metalness:null,
    opacity:Number.isFinite(material.opacity)?material.opacity:1,transparent:!!material.transparent,alphaTest:Number(material.alphaTest)||0,side:material.side??null,
    vertexColors:!!material.vertexColors,flatShading:!!material.flatShading,normalScale:material.normalScale?[material.normalScale.x,material.normalScale.y]:null,
    maps:{map:pocketStudioTextureRef(material.map),normalMap:pocketStudioTextureRef(material.normalMap),roughnessMap:pocketStudioTextureRef(material.roughnessMap),metalnessMap:pocketStudioTextureRef(material.metalnessMap),emissiveMap:pocketStudioTextureRef(material.emissiveMap),aoMap:pocketStudioTextureRef(material.aoMap),alphaMap:pocketStudioTextureRef(material.alphaMap)}};
}
function pocketStudioGeometry(geometry){
  if(!geometry)return null;const attributes={};
  for(const [name,attr] of Object.entries(geometry.attributes||{}))if(attr?.array)attributes[name]={itemSize:attr.itemSize,normalized:!!attr.normalized,count:attr.count,arrayType:attr.array?.constructor?.name||"Float32Array",array:Array.from(attr.array)};
  return {type:geometry.type||"BufferGeometry",name:geometry.name||null,attributes,
    index:geometry.index?.array?{itemSize:1,count:geometry.index.count,arrayType:geometry.index.array?.constructor?.name||"Uint16Array",array:Array.from(geometry.index.array)}:null,
    groups:(geometry.groups||[]).map(g=>({start:g.start,count:g.count,materialIndex:g.materialIndex})),drawRange:geometry.drawRange?{start:geometry.drawRange.start,count:geometry.drawRange.count}:null};
}
function pocketStudioTransform(node){return {position:[Number(node?.position?.x)||0,Number(node?.position?.y)||0,Number(node?.position?.z)||0],rotation:[Number(node?.rotation?.x)||0,Number(node?.rotation?.y)||0,Number(node?.rotation?.z)||0,node?.rotation?.order||"XYZ"],scale:[Number(node?.scale?.x)||1,Number(node?.scale?.y)||1,Number(node?.scale?.z)||1]}}
function pocketStudioSceneNode(node){
  const isMesh=!!node?.isMesh||node?.type==="Mesh";const out={name:node?.name||"",nodeType:isMesh?"mesh":"group",visible:node?.visible!==false,transform:pocketStudioTransform(node),userData:pocketStudioSanitize(node?.userData||{})||{},children:[]};
  if(isMesh){out.geometry=pocketStudioGeometry(node.geometry);out.material=pocketStudioMaterial(node.material);out.castShadow=!!node.castShadow;out.receiveShadow=!!node.receiveShadow}
  for(const child of node?.children||[])out.children.push(pocketStudioSceneNode(child));return out;
}
function pocketStudioSceneGraph(root){
  const graph=pocketStudioSceneNode(root),stats={nodes:0,meshes:0,vertices:0,triangles:0,externalTextureRefs:0};
  const visit=node=>{stats.nodes++;if(node.nodeType==="mesh"){stats.meshes++;const pos=node.geometry?.attributes?.position;stats.vertices+=Number(pos?.count)||0;const idx=node.geometry?.index?.count;stats.triangles+=idx?Math.floor(idx/3):Math.floor((Number(pos?.count)||0)/3);const mats=Array.isArray(node.material)?node.material:[node.material];for(const mat of mats)for(const ref of Object.values(mat?.maps||{}))if(ref?.source)stats.externalTextureRefs++}for(const child of node.children||[])visit(child)};
  visit(graph);return {schema:"three-group-scenegraph-v1",root:graph,stats};
}
function pocketStudioStableId(prefix,value){let hash=2166136261;for(const ch of String(value||"")){hash^=ch.charCodeAt(0);hash=Math.imul(hash,16777619)}return `${prefix}-${(hash>>>0).toString(36)}`}
function pocketStudioSafeTextureSource(source){
  if(typeof source!=="string"||!source.trim())return null;
  try{const url=new URL(source.trim(),location.href);if(url.protocol!=="https:"||url.origin!==location.origin)return null;return url.href}catch{return null}
}
/* Metadata only: PocketMonster's host must fetch, verify and bind textures. */
function pocketStudioRenderProfile(sceneGraph){
  const textures=[],materials=[],rejectedSources=[];const textureBySource=new Map();
  const textureId=(ref,slot)=>{
    if(!ref||typeof ref!=="object"||Array.isArray(ref))return null;
    const source=pocketStudioSafeTextureSource(ref.source);
    if(!source){if(ref?.source)rejectedSources.push({source:String(ref.source),slot,reason:"requires same-origin HTTPS Studio asset"});return null}
    const colorSpace=slot==="map"||slot==="emissiveMap"?(ref.colorSpace||"srgb"):"";
    const key=JSON.stringify([source,colorSpace,ref.flipY??true,ref.wrapS,ref.wrapT,ref.minFilter,ref.magFilter,ref.generateMipmaps,ref.anisotropy,ref.repeat,ref.offset,ref.center,ref.rotation,ref.integrity]);
    if(!textureBySource.has(key)){
      const id=pocketStudioStableId("studio-texture",key);textureBySource.set(key,id);
      textures.push({id,source,colorSpace,flipY:ref.flipY??true,wrapS:ref.wrapS??null,wrapT:ref.wrapT??null,
        minFilter:ref.minFilter??null,magFilter:ref.magFilter??null,generateMipmaps:ref.generateMipmaps??null,anisotropy:ref.anisotropy??null,
        repeat:ref.repeat||[1,1],offset:ref.offset||[0,0],center:ref.center||[0,0],rotation:ref.rotation||0,
        integrity:ref.integrity||null,integrityStatus:ref.integrityStatus||"unavailable-in-sync-export"});
    }
    return textureBySource.get(key);
  };
  const visit=(node,path=[])=>{
    if(node?.nodeType==="mesh"){
      const list=Array.isArray(node.material)?node.material:[node.material];
      list.forEach((material,index)=>{
        const textureSlots={};for(const [slot,ref] of Object.entries(material?.maps||{})){const id=textureId(ref,slot);if(id)textureSlots[slot]=id}
        materials.push({id:pocketStudioStableId("studio-material",`${path.join(".")}:${index}:${material?.name||""}`),nodePath:path,materialIndex:index,
          name:material?.name||null,model:material?.type||"MeshStandardMaterial",textureSlots,
          scalar:{color:material?.color??null,emissive:material?.emissive??null,emissiveIntensity:material?.emissiveIntensity??0,roughness:material?.roughness??null,metalness:material?.metalness??null,opacity:material?.opacity??1,transparent:!!material?.transparent,alphaTest:material?.alphaTest??0,side:material?.side??null,vertexColors:!!material?.vertexColors,flatShading:!!material?.flatShading}});
      });
    }
    (node?.children||[]).forEach((child,index)=>visit(child,[...path,index]));
  };
  visit(sceneGraph?.root,[]);
  const look=spec?.look||{};
  return {schema:"pocket-character-render-profile-v1",version:"1.0.0",mode:"metadata-only-host-applied",
    sourcePolicy:{allowlistedOrigins:[location.origin],sameOriginHttpsOnly:true,hostMustVerifyIntegrity:true},textures,materials,rejectedSources,
    shadow:{cast:!!look.shadows,receive:!!look.shadows,requiresExistingHostRenderer:true},
    lightingProfile:{id:`studio-${String(look.preset||"studio").replace(/[^a-z0-9_-]/gi,"-").toLowerCase()}-advisory-v1`,mode:"host-advisory-no-light-objects",requiresExistingHostRenderer:true,createsRenderer:false,createsLights:false,
      settings:{exposure:Number(look.exposure)||1,key:Number(look.key)||0,rim:Number(look.rim)||0,ambient:Number(look.ambient)||0,keyColor:look.keyColor||null,rimColor:look.rimColor||null,fillColor:look.fillColor||null,shadowEnabled:!!look.shadows}}};
}
function pocketStudioJointBindings(root){
  const paths=new Map();const visit=(node,path)=>{paths.set(node,path);(node?.children||[]).forEach((child,index)=>visit(child,[...path,index]))};visit(root,[]);const bindings={};
  for(const [jointKey,node] of Object.entries(joints||{})){const path=paths.get(node);if(path)bindings[jointKey]={path,nodeName:node?.name||null}}
  return bindings;
}
function pocketStudioJoint(candidates){for(const name of candidates)if(joints?.[name])return name;return candidates[0]}
function pocketStudioSockets(){return {
  rightHand:{joint:pocketStudioJoint(["handR","wristR","elbowR"]),offset:[0,0,0]},leftHand:{joint:pocketStudioJoint(["handL","wristL","elbowL"]),offset:[0,0,0]},
  head:{joint:pocketStudioJoint(["head","neck"]),offset:[0,0,0]},back:{joint:pocketStudioJoint(["chest","spine","pelvis"]),offset:[0,0,.12]},waist:{joint:pocketStudioJoint(["pelvis","chest"]),offset:[0,0,0]},
  vfxOrigin:{joint:pocketStudioJoint(["chest","pelvis"]),offset:[0,.12,-.18]},attackOrigin:{joint:pocketStudioJoint(["handR","wristR","elbowR"]),offset:[0,0,-.08]},throwOrigin:{joint:pocketStudioJoint(["handR","wristR","elbowR"]),offset:[0,0,-.08]}}}
function pocketStudioState(clip){return String(clip?.runtime?.transition?.state||clip?.runtime?.state||clip?.name||"idle").trim().replace(/[\s-]+/g,"_").toLowerCase()}
const POCKET_STUDIO_MOTION_PACK_SCHEMA="pocket-character-motion-pack-v1";
const POCKET_STUDIO_MOTION_PACK_VERSION="1.1.0";
function pocketStudioReadyMotionPack(){
  const clip=(name,state,duration,loop,keys,options={})=>{
    const out=createTemplateClip(name,duration,30,keys,loop,"smooth");
    out.id=`pocket-template-${state}`;out.runtime.state=state;out.runtime.motionClass=options.motionClass||out.runtime.motionClass;
    out.runtime.motionSpeed=Number.isFinite(options.motionSpeed)?options.motionSpeed:out.runtime.motionSpeed;
    out.source={kind:"pocketmonster-default-motion-pack",studioVersion:"1.8.10.4",template:name};
    if(Array.isArray(options.events))out.events=options.events.map(event=>({...event}));
    return out;
  };
  const k=(time,pose,side="R")=>({time,pose,side});
  const idleA=poseSnapshotFromLibrary("idle","L"),idleB=cloneAnimationPose(idleA);
  if(idleB.chest){idleB.chest.rotation[0]=(idleB.chest.rotation[0]||0)+rad(2);idleB.chest.position[1]=(idleB.chest.position[1]||0)+.015}
  if(idleB.head)idleB.head.rotation[0]=(idleB.head.rotation[0]||0)-rad(1);
  const idle=makeAnimationClip("Idle_Breathing",2,30);
  idle.id="pocket-template-idle";idle.loop=true;idle.interpolation="smooth";idle.runtime.state="idle";idle.runtime.motionClass="idle";idle.runtime.motionSpeed=0;
  idle.keyframes=[
    {time:0,joints:idleA,meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}},
    {time:1,joints:idleB,meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}},
    {time:2,joints:cloneAnimationPose(idleA),meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}}
  ];
  idle.source={kind:"pocketmonster-default-motion-pack",studioVersion:"1.8.10.4",template:"Idle_Breathing"};
  const clips=[
    idle,
    clip("Walk_PoseLibrary","walk",1,true,[k(0,"walkContact","L"),k(.25,"walkPassing","L"),k(.5,"walkContact","R"),k(.75,"walkPassing","R"),k(1,"walkContact","L")],{motionSpeed:1.8}),
    clip("Run_PoseLibrary","run",.72,true,[k(0,"runContact","L"),k(.18,"walkPassing","L"),k(.36,"runContact","R"),k(.54,"walkPassing","R"),k(.72,"runContact","L")],{motionSpeed:4.5}),
    clip("Sprint_PoseLibrary","sprint",.58,true,[k(0,"runContact","L"),k(.145,"walkPassing","L"),k(.29,"runContact","R"),k(.435,"walkPassing","R"),k(.58,"runContact","L")],{motionSpeed:6.8}),
    clip("Start_Accelerate","start",1,false,[k(0,"idle"),k(.24,"runContact","L"),k(.54,"walkPassing","L"),k(1,"runContact","R")],{motionSpeed:2.8}),
    clip("Stop_Brake","stop",1.1,false,[k(0,"runContact","L"),k(.32,"walkPassing","L"),k(.72,"walkContact","R"),k(1.1,"idle")],{motionSpeed:0}),
    clip("Turn_R_PoseLibrary","turn_r",1,true,[k(0,"walkContact","L"),k(.25,"walkPassing","L"),k(.5,"walkContact","R"),k(.75,"walkPassing","R"),k(1,"walkContact","L")],{motionSpeed:1.4}),
    clip("Turn_L_PoseLibrary","turn_l",1,true,[k(0,"walkContact","R"),k(.25,"walkPassing","R"),k(.5,"walkContact","L"),k(.75,"walkPassing","L"),k(1,"walkContact","R")],{motionSpeed:1.4}),
    clip("Strafe_R_PoseLibrary","strafe_r",.95,true,[k(0,"walkContact","L"),k(.24,"walkPassing","L"),k(.48,"walkContact","R"),k(.72,"walkPassing","R"),k(.95,"walkContact","L")],{motionSpeed:1.6}),
    clip("Strafe_L_PoseLibrary","strafe_l",.95,true,[k(0,"walkContact","R"),k(.24,"walkPassing","R"),k(.48,"walkContact","L"),k(.72,"walkPassing","L"),k(.95,"walkContact","R")],{motionSpeed:1.6}),
    clip("Jump_Core","jump",1.08,false,[k(0,"idle"),k(.16,"jumpTakeoff"),k(.36,"jumpAir"),k(.66,"fall"),k(.88,"land"),k(1.08,"idle")],{motionClass:"custom",motionSpeed:0}),
    clip("Fall_Loop_Core","fall",1,true,[k(0,"fall"),k(.5,"jumpAir"),k(1,"fall")],{motionClass:"custom",motionSpeed:0}),
    clip("Land_Core","land",.72,false,[k(0,"fall"),k(.12,"land"),k(.38,"crouch"),k(.72,"idle")],{motionClass:"custom",motionSpeed:0}),
    clip("Crouch_Idle_Core","crouch_idle",1.2,true,[k(0,"crouch"),k(.6,"crouch"),k(1.2,"crouch")],{motionClass:"custom",motionSpeed:0}),
    clip("Crouch_Walk_Core","crouch_walk",1.15,true,[k(0,"crouchStep","L"),k(.2875,"crouch","L"),k(.575,"crouchStep","R"),k(.8625,"crouch","R"),k(1.15,"crouchStep","L")],{motionClass:"custom",motionSpeed:.85}),
    clip("Dodge_R_Core","dodge_r",.72,false,[k(0,"idle","R"),k(.12,"crouchStep","L"),k(.34,"dodge","R"),k(.52,"crouchStep","R"),k(.72,"idle","R")],{motionClass:"action",motionSpeed:0}),
    clip("Dodge_L_Core","dodge_l",.72,false,[k(0,"idle","L"),k(.12,"crouchStep","R"),k(.34,"dodge","L"),k(.52,"crouchStep","L"),k(.72,"idle","L")],{motionClass:"action",motionSpeed:0}),
    clip("Hit_React_Core","hurt",.56,false,[k(0,"idle"),k(.10,"hitReact","R"),k(.27,"hitReact","L"),k(.56,"idle")],{motionClass:"custom",motionSpeed:0}),
    clip("Knockback_Core","knockback",.82,false,[k(0,"idle"),k(.10,"hitReact","R"),k(.30,"knockback","R"),k(.58,"crouch","R"),k(.82,"idle")],{motionClass:"custom",motionSpeed:0}),
    clip("Get_Up_Core","get_up",1.2,false,[k(0,"downBack","R"),k(.36,"faint","R"),k(.72,"crouch","R"),k(1,"jumpTakeoff","R"),k(1.2,"idle")],{motionClass:"custom",motionSpeed:0}),
    clip("Death_Core","dead",1.05,false,[k(0,"idle"),k(.18,"hitReact","R"),k(.48,"knockback","R"),k(.80,"downBack","R"),k(1.05,"downBack","R")],{motionClass:"custom",motionSpeed:0}),
    clip("Faint_Core","faint",.92,false,[k(0,"idle"),k(.20,"crouch","R"),k(.54,"faint","R"),k(.92,"faint","R")],{motionClass:"custom",motionSpeed:0}),
    clip("Interact_Core","interact",.86,false,[k(0,"idle","R"),k(.18,"interactReach","R"),k(.46,"interactReach","R"),k(.68,"idle","R"),k(.86,"idle","R")],{motionClass:"custom",motionSpeed:0}),
    clip("Ball_Aim_Loop","ball_aim",1.6,true,[k(0,"ballAim","R"),k(.8,"ballAim","R"),k(1.6,"ballAim","R")],{motionClass:"custom",motionSpeed:0}),
    clip("Attack_PoseLibrary","attack",.9,false,[k(0,"idle","R"),k(.28,"attackWindup","R"),k(.48,"attackImpact","R"),k(.9,"idle","R")],{motionClass:"action",motionSpeed:0,events:[{type:"impact",time:.48}]}),
    clip("Monster_Command_Core","monster_command",.82,false,[k(0,"idle","R"),k(.18,"monsterCommand","R"),k(.50,"monsterCommand","R"),k(.82,"idle","R")],{motionClass:"custom",motionSpeed:0,events:[{type:"command",time:.50}]})
  ];
  const throwClip=(name,state,duration,releaseTime,points)=>clip(name,state,duration,false,points,{motionClass:"action",motionSpeed:0,events:[{type:"release",time:releaseTime}]});
  clips.push(
    throwClip("Capture_Throw_R_Core","capture_throw_r",.94,.56,[k(0,"ballReady","R"),k(.15,"ballAim","R"),k(.34,"throwWindup","R"),k(.56,"throwRelease","R"),k(.72,"throwFollow","R"),k(.94,"idle","R")]),
    throwClip("Capture_Throw_L_Core","capture_throw_l",.94,.56,[k(0,"ballReady","L"),k(.15,"ballAim","L"),k(.34,"throwWindup","L"),k(.56,"throwRelease","L"),k(.72,"throwFollow","L"),k(.94,"idle","L")]),
    throwClip("Quick_Capture_Throw_R_Core","quick_capture_throw",.68,.34,[k(0,"ballReady","R"),k(.08,"ballAim","R"),k(.20,"throwWindup","R"),k(.34,"throwRelease","R"),k(.50,"throwFollow","R"),k(.68,"idle","R")]),
    throwClip("Power_Capture_Throw_R_Core","power_capture_throw",1.16,.68,[k(0,"ballReady","R"),k(.15,"ballAim","R"),k(.43,"throwWindup","R"),k(.68,"throwRelease","R"),k(.91,"throwFollow","R"),k(1.16,"idle","R")]),
    throwClip("Summon_Monster_Throw_R_Core","summon_monster_throw",.98,.55,[k(0,"ballReady","R"),k(.15,"ballAim","R"),k(.32,"throwWindup","R"),k(.55,"throwRelease","R"),k(.74,"throwFollow","R"),k(.98,"idle","R")])
  );
  const actionMap=Object.freeze({
    idle:"idle",walk:"walk",run:"run",sprint:"sprint",start:"start",stop:"stop",
    turn_r:"turn_r",turn_l:"turn_l",strafe_r:"strafe_r",strafe_l:"strafe_l",
    jump:"jump",fall:"fall",land:"land",attack:"attack","attack-melee":"attack",
    hurt:"hurt",dead:"dead",knockback:"knockback",dodge_l:"dodge_l",dodge_r:"dodge_r",interact:"interact",
    crouch_idle:"crouch_idle",crouch_walk:"crouch_walk",faint:"faint",get_up:"get_up",ball_aim:"ball_aim",
    monster_command:"monster_command",capture_throw:"capture_throw_r",capture_throw_r:"capture_throw_r",capture_throw_l:"capture_throw_l",
    quick_capture_throw:"quick_capture_throw",power_capture_throw:"power_capture_throw",summon_monster_throw:"summon_monster_throw"
  });
  const unsupportedActions=Object.freeze({
    skill:"No distinct authored generic skill pose exists in the Studio template set; gameplay should remain on locomotion or select a specific authored visual.",
    "attack-ranged":"No distinct authored ranged-weapon attack pose exists; capture throw is not a ranged-attack substitute."
  });
  const requiredActions=["idle","walk","run","jump","attack","hurt","dead","capture_throw","summon_monster_throw","monster_command"];
  return {schema:POCKET_STUDIO_MOTION_PACK_SCHEMA,version:POCKET_STUDIO_MOTION_PACK_VERSION,
    source:"Character Studio ready-made templates",clips,actionMap,unsupportedActions,requiredActions};
}
function pocketStudioAssertMotionPack(pack){
  const states=new Set(pack.clips.map(pocketStudioState));
  for(const action of pack.requiredActions){
    const state=pack.actionMap[action];const found=pack.clips.find(clip=>pocketStudioState(clip)===state);
    if(!found||!Array.isArray(found.keyframes)||found.keyframes.length<2)throw new Error(`Pocket motion pack missing usable ${action} clip`);
  }
  for(const action of Object.keys(pack.unsupportedActions||{}))if(pack.actionMap[action])throw new Error(`Unsupported Pocket motion action must not be mapped: ${action}`);
  if(states.size!==pack.clips.length)throw new Error("Pocket motion pack has duplicate runtime states");
}
function buildPocketStudioCharacterPackage(request={}){
  if(!characterRoot)throw new Error("Studio characterRoot is not ready");
  const requested=String(request.characterId||"character.human.pirate.studio-live").trim();const id=/^character\.[a-z0-9][a-z0-9._-]*$/i.test(requested)?requested:"character.human.pirate.studio-live";
  const name=String(request.displayName||"Studio Player").trim().slice(0,80)||"Studio Player";const clean=pocketStudioSanitize(spec)||{};const authored=Array.isArray(clean.animations)?clean.animations:[];delete clean.animations;
  const motionPack=pocketStudioReadyMotionPack();pocketStudioAssertMotionPack(motionPack);
  const authoredStates=new Set(authored.map(pocketStudioState));const animations=[...motionPack.clips.filter(clip=>!authoredStates.has(pocketStudioState(clip))),...authored];
  const actionMap={...motionPack.actionMap},unsupportedActions={...motionPack.unsupportedActions};
  for(const action of Object.keys(unsupportedActions)){
    const state=action.replace(/-/g,"_");
    if(authoredStates.has(state)){actionMap[action]=state;delete unsupportedActions[action]}
  }
  pocketStudioAssertMotionPack({...motionPack,clips:animations,actionMap,unsupportedActions});
  const heightCandidates=[spec?.body?.height,spec?.character?.height,spec?.metrics?.height];let height=1.8;for(const value of heightCandidates){const n=Number(value);if(Number.isFinite(n)&&n>.2&&n<10){height=n;break}}
  const common={id,kind:"character",provider:"studio-character",style:"blocky-bighead-studio-v1",surfaceStyle:"pbr-studio-v1",rig:"studio-three-group-v1",metrics:{height},roles:{player:{}}};
  const sceneGraph=pocketStudioSceneGraph(characterRoot);const renderProfile=pocketStudioRenderProfile(sceneGraph);
  return {schema:"pocket-character-runtime-v1",schemaVersion:"1.2.0",generatedBy:{product:"3JS Player Block Asset Engine",studioVersion:"1.8.10.4",generatorVersion:"live-bridge-v1",generatedAt:new Date().toISOString()},
    target:{game:"PocketMonster",assetEngine:"asset-presentation",provider:"studio-character",assetHandleContract:["root","rig","play","update","anchor","bounds","setAppearance","dispose"]},
    manifest:{...common,name,contract:"presentation-only"},catalogEntry:{...common},character:clean,sceneGraph,renderProfile,
    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),jointBindings:pocketStudioJointBindings(characterRoot),sockets:pocketStudioSockets()},
    motionPack:{schema:motionPack.schema,version:motionPack.version,source:motionPack.source,requiredActions:motionPack.requiredActions,actionMap,unsupportedActions},
    animations,animationIndex:animations.map(clip=>({id:clip.id||null,name:clip.name||"Animation",state:pocketStudioState(clip),duration:Number(clip.duration)||0,loop:!!clip.loop,keyframeCount:Array.isArray(clip.keyframes)?clip.keyframes.length:0,events:Array.isArray(clip.events)?clip.events.map(event=>({...event})):[]})),
    gameplayPolicy:{included:false,authority:"Pocket Monster / Pirate Fruit server-domain systems",forbiddenKeys:[...POCKET_STUDIO_FORBIDDEN_KEYS].sort()},transport:{format:"postmessage-json-envelope",encoding:"structured-clone"}};
}
function pocketStudioAllowedOrigin(origin){
  if(origin===window.location.origin)return true;
  try{const u=new URL(origin);return (u.protocol==="https:"&&(u.hostname==="pocketmonster-game.web.app"||u.hostname==="nustanakritwithai.github.io"))||((u.hostname==="localhost"||u.hostname==="127.0.0.1")&&(u.protocol==="http:"||u.protocol==="https:"))}catch{return false}
}
if(typeof window!=="undefined"){
  window.POCKET_STUDIO_CHARACTER_BRIDGE=Object.freeze({version:"1.2",buildPackage:buildPocketStudioCharacterPackage});
  window.addEventListener("message",event=>{
    if(event?.data?.type!==POCKET_STUDIO_BRIDGE_REQUEST||!pocketStudioAllowedOrigin(event.origin)||!event.source)return;
    const requestId=String(event.data.requestId||"");
    try{event.source.postMessage({type:POCKET_STUDIO_BRIDGE_RESPONSE,requestId,package:buildPocketStudioCharacterPackage(event.data)},event.origin)}
    catch(error){event.source.postMessage({type:POCKET_STUDIO_BRIDGE_ERROR,requestId,message:String(error?.message||error)},event.origin)}
  });
}
'''
    return html.replace(anchor, bridge + '\n' + anchor, 1)


if __name__ == '__main__':
    import sys
    p = Path(sys.argv[1])
    p.write_text(patch(p.read_text(encoding='utf-8')), encoding='utf-8')
