#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    anchor = 'function createAttackTemplate(){'
    if anchor not in html:
        raise RuntimeError('missing anchor: Pocket Studio live bridge')

    bridge = r'''const POCKET_STUDIO_BRIDGE_REQUEST="POCKET_STUDIO_CHARACTER_REQUEST";
const POCKET_STUDIO_BRIDGE_RESPONSE="POCKET_STUDIO_CHARACTER_PACKAGE";
const POCKET_STUDIO_BRIDGE_ERROR="POCKET_STUDIO_CHARACTER_ERROR";
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
  return {source,name:texture.name||null,colorSpace:texture.colorSpace||null,wrapS:texture.wrapS??null,wrapT:texture.wrapT??null,flipY:typeof texture.flipY==="boolean"?texture.flipY:null};
}
function pocketStudioMaterial(material){
  if(Array.isArray(material))return material.map(pocketStudioMaterial);if(!material)return null;
  const color=c=>c&&typeof c.getHexString==="function"?`#${c.getHexString()}`:null;
  return {type:material.type||"Material",name:material.name||null,color:color(material.color),emissive:color(material.emissive),emissiveIntensity:Number(material.emissiveIntensity)||0,
    roughness:Number.isFinite(material.roughness)?material.roughness:null,metalness:Number.isFinite(material.metalness)?material.metalness:null,
    opacity:Number.isFinite(material.opacity)?material.opacity:1,transparent:!!material.transparent,alphaTest:Number(material.alphaTest)||0,side:material.side??null,
    vertexColors:!!material.vertexColors,flatShading:!!material.flatShading,
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
function buildPocketStudioCharacterPackage(request={}){
  if(!characterRoot)throw new Error("Studio characterRoot is not ready");
  const requested=String(request.characterId||"character.human.pirate.studio-live").trim();const id=/^character\.[a-z0-9][a-z0-9._-]*$/i.test(requested)?requested:"character.human.pirate.studio-live";
  const name=String(request.displayName||"Studio Player").trim().slice(0,80)||"Studio Player";const clean=pocketStudioSanitize(spec)||{};const animations=Array.isArray(clean.animations)?clean.animations:[];delete clean.animations;
  const heightCandidates=[spec?.body?.height,spec?.character?.height,spec?.metrics?.height];let height=1.8;for(const value of heightCandidates){const n=Number(value);if(Number.isFinite(n)&&n>.2&&n<10){height=n;break}}
  const common={id,kind:"character",provider:"studio-character",style:"blocky-bighead-studio-v1",surfaceStyle:"pbr-studio-v1",rig:"studio-three-group-v1",metrics:{height},roles:{player:{}}};
  return {schema:"pocket-character-runtime-v1",schemaVersion:"1.0.0",generatedBy:{product:"3JS Player Block Asset Engine",studioVersion:"1.8.10.4",generatorVersion:"live-bridge-v1",generatedAt:new Date().toISOString()},
    target:{game:"PocketMonster",assetEngine:"asset-presentation",provider:"studio-character",assetHandleContract:["root","rig","play","update","anchor","bounds","setAppearance","dispose"]},
    manifest:{...common,name,contract:"presentation-only"},catalogEntry:{...common},character:clean,sceneGraph:pocketStudioSceneGraph(characterRoot),
    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),jointBindings:pocketStudioJointBindings(characterRoot),sockets:pocketStudioSockets()},
    animations,animationIndex:animations.map(clip=>({id:clip.id||null,name:clip.name||"Animation",state:pocketStudioState(clip),duration:Number(clip.duration)||0,loop:!!clip.loop})),
    gameplayPolicy:{included:false,authority:"Pocket Monster / Pirate Fruit server-domain systems",forbiddenKeys:[...POCKET_STUDIO_FORBIDDEN_KEYS].sort()},transport:{format:"postmessage-json-envelope",encoding:"structured-clone"}};
}
function pocketStudioAllowedOrigin(origin){
  if(origin===window.location.origin)return true;
  try{const u=new URL(origin);return (u.protocol==="https:"&&(u.hostname==="pocketmonster-game.web.app"||u.hostname==="nustanakritwithai.github.io"))||((u.hostname==="localhost"||u.hostname==="127.0.0.1")&&(u.protocol==="http:"||u.protocol==="https:"))}catch{return false}
}
if(typeof window!=="undefined"){
  window.POCKET_STUDIO_CHARACTER_BRIDGE=Object.freeze({version:"1",buildPackage:buildPocketStudioCharacterPackage});
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
