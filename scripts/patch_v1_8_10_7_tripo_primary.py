#!/usr/bin/env python3
from pathlib import Path


def patch(html: str) -> str:
    anchor = 'function buildCharacter(preserve=true){return buildBlueExplorerPrimaryCharacter(preserve)}'
    if anchor not in html:
        raise RuntimeError('missing Blue Explorer buildCharacter anchor')
    if 'TRIPO_PRIMARY_ID="tripo-5889e73e-rigid-v1"' in html:
        raise RuntimeError('Tripo primary adapter already injected')

    adapter = r'''
let tripoPrimaryDescriptor=null;
let tripoPrimaryMaterials=null;
let tripoPrimaryInstance=null;
let tripoPrimaryLoading=null;
const TRIPO_PRIMARY_ID="tripo-5889e73e-rigid-v1";
const TRIPO_PRIMARY_DESCRIPTOR_URL="./assets/runtime/tripo_5889e73e/rigid-model.json";
const TRIPO_PRIMARY_SOURCE="assets/imports/tripo_5889e73e/tripo_5889e73e.glb";

function tripoPrimaryVec(v,fallback=[0,0,0]){
  return Array.isArray(v)&&v.length>=3?v:fallback;
}
function tripoPrimaryDisposeInstance(){
  if(!tripoPrimaryInstance)return;
  try{characterRoot.remove(tripoPrimaryInstance.root)}catch{}
  try{tripoPrimaryInstance.dispose?.()}catch(err){console.warn("Tripo primary dispose",err)}
  tripoPrimaryInstance=null;
}
async function tripoPrimaryLoadTexture(ref,srgb=false){
  if(!ref?.path)return null;
  try{
    const texture=await new THREE.TextureLoader().loadAsync(ref.path);
    texture.flipY=false;
    if(srgb&&THREE.SRGBColorSpace)texture.colorSpace=THREE.SRGBColorSpace;
    texture.userData??={};texture.userData.tripoPrimarySource=ref.path;
    return texture;
  }catch(error){
    console.warn("Tripo texture fallback",ref.path,error);return null;
  }
}
async function tripoPrimaryBuildMaterials(descriptor){
  const textureDefs=descriptor?.textures||[],textureCache=new Map();
  const textureFor=async(index,srgb=false)=>{
    if(index==null||index<0||!textureDefs[index])return null;
    const key=`${index}:${srgb?1:0}`;
    if(!textureCache.has(key))textureCache.set(key,tripoPrimaryLoadTexture(textureDefs[index],srgb));
    return textureCache.get(key);
  };
  const result=[];
  for(const [index,def] of (descriptor?.materials||[]).entries()){
    const rgba=Array.isArray(def.baseColorFactor)?def.baseColorFactor:[1,1,1,1];
    const emissive=Array.isArray(def.emissiveFactor)?def.emissiveFactor:[0,0,0];
    const params={
      color:new THREE.Color(rgba[0]??1,rgba[1]??1,rgba[2]??1),
      opacity:Number.isFinite(rgba[3])?rgba[3]:1,
      transparent:def.alphaMode==="BLEND"||(rgba[3]??1)<.999,
      alphaTest:def.alphaMode==="MASK"?(Number(def.alphaCutoff)||.5):0,
      roughness:Number.isFinite(def.roughnessFactor)?def.roughnessFactor:.72,
      metalness:Number.isFinite(def.metallicFactor)?def.metallicFactor:0,
      emissive:new THREE.Color(emissive[0]||0,emissive[1]||0,emissive[2]||0),
      side:def.doubleSided?THREE.DoubleSide:THREE.FrontSide
    };
    params.map=await textureFor(def.baseColorTexture,true);
    const mr=await textureFor(def.metallicRoughnessTexture,false);
    if(mr){params.roughnessMap=mr;params.metalnessMap=mr}
    params.normalMap=await textureFor(def.normalTexture,false);
    params.emissiveMap=await textureFor(def.emissiveTexture,true);
    params.aoMap=await textureFor(def.occlusionTexture,false);
    for(const key of Object.keys(params))if(params[key]==null)delete params[key];
    const material=new THREE.MeshStandardMaterial(params);
    material.name=def.name||`tripo_material_${index}`;
    material.userData??={};material.userData.tripoPrimary=true;material.userData.tripoMaterialIndex=index;
    result.push(material);
  }
  return result;
}
function tripoPrimaryGeometry(primitive){
  const geometry=new THREE.BufferGeometry();
  const pos=new THREE.Float32BufferAttribute(primitive.positions||[],3);
  geometry.setAttribute("position",pos);
  if(primitive.normals?.length)geometry.setAttribute("normal",new THREE.Float32BufferAttribute(primitive.normals,3));
  if(primitive.uvs?.length){
    const uv=new THREE.Float32BufferAttribute(primitive.uvs,2);geometry.setAttribute("uv",uv);
    if(uv.clone)geometry.setAttribute("uv1",uv.clone());
  }
  if(primitive.indices?.length)geometry.setIndex(primitive.indices);
  if(!geometry.getAttribute("normal"))geometry.computeVertexNormals();
  geometry.computeBoundingBox();geometry.computeBoundingSphere();
  geometry.userData={tripoPrimary:true,regionVertexCount:primitive.vertexCount||0,regionTriangleCount:primitive.triangleCount||0};
  return geometry;
}
function tripoPrimaryRegisterJoint(key,node){
  if(!node)throw new Error(`Tripo joint missing: ${key}`);
  node.rotation.set(0,0,0);
  const base=node.position.toArray(),off=spec.skeleton?.pivotOffsets?.[key]||[0,0,0];
  node.userData.basePivot=[...base];
  node.position.set(base[0]+(off[0]||0),base[1]+(off[1]||0),base[2]+(off[2]||0));
  node.userData.restLocalPosition=node.position.toArray();node.userData.restLocalRotation=[0,0,0];node.userData.engineJointKey=key;
  joints[key]=node;return node;
}
function tripoPrimaryRig(descriptor,root){
  const world=descriptor?.rig?.joints||{};
  const groups={};
  const create=(key,parent,parentKey=null)=>{
    const p=tripoPrimaryVec(world[key]);const pp=parentKey?tripoPrimaryVec(world[parentKey]):[0,0,0];
    const g=new THREE.Group();g.name=`TripoRig_${key}`;g.position.set(p[0]-pp[0],p[1]-pp[1],p[2]-pp[2]);parent.add(g);groups[key]=g;return g;
  };
  create("pelvis",root);
  create("chest",groups.pelvis,"pelvis");create("neck",groups.chest,"chest");create("head",groups.neck,"neck");
  create("shoulderL",groups.chest,"chest");create("elbowL",groups.shoulderL,"shoulderL");create("wristL",groups.elbowL,"elbowL");
  create("shoulderR",groups.chest,"chest");create("elbowR",groups.shoulderR,"shoulderR");create("wristR",groups.elbowR,"elbowR");
  create("hipL",groups.pelvis,"pelvis");create("kneeL",groups.hipL,"hipL");create("ankleL",groups.kneeL,"kneeL");
  create("hipR",groups.pelvis,"pelvis");create("kneeR",groups.hipR,"hipR");create("ankleR",groups.kneeR,"kneeR");
  for(const [key,node] of Object.entries(groups))tripoPrimaryRegisterJoint(key,node);
  return groups;
}
function tripoPrimaryAttachParts(descriptor,root,groups,materials,owned){
  const pivotWorld=descriptor?.rig?.joints||{};
  for(const [region,part] of Object.entries(descriptor?.parts||{})){
    const jointKey=part?.joint,holder=groups[jointKey]||root,pivot=jointKey?tripoPrimaryVec(pivotWorld[jointKey]):[0,0,0];
    for(const [index,primitive] of (part?.primitives||[]).entries()){
      if(!primitive?.positions?.length)continue;
      const geometry=tripoPrimaryGeometry(primitive);owned.geometries.push(geometry);
      const material=materials[primitive.material]||materials[0];
      const mesh=new THREE.Mesh(geometry,material);mesh.name=`Tripo_${region}_${index}`;
      mesh.position.set(-pivot[0],-pivot[1],-pivot[2]);mesh.castShadow=spec.look.shadows;mesh.receiveShadow=spec.look.shadows;
      mesh.userData={tripoPrimary:true,region,jointKey,source:TRIPO_PRIMARY_SOURCE};holder.add(mesh);meshes.push(mesh);partCounter++;
    }
  }
}
function buildTripoPrimaryCharacter(preserve=true){
  if(!tripoPrimaryDescriptor||!tripoPrimaryMaterials?.length)return buildBlueExplorerPrimaryCharacter(preserve);
  if(gameRuntimeState.playing||gameRuntimeState.basePose)runtimePreviewStop(true);
  if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);
  if(motionState.playing)stopMotionPreview(true);
  const oldPose=preserve?capturePose():(spec.pose.joints||{});
  if(blueExplorerInstance){
    try{characterRoot.remove(blueExplorerInstance.root);blueExplorerInstance.dispose?.()}catch(err){console.warn("Blue Explorer fallback dispose",err)}
    blueExplorerInstance=null;
  }
  tripoPrimaryDisposeInstance();clearCharacter();makeMaterials();
  try{
    const descriptor=tripoPrimaryDescriptor,root=new THREE.Group();root.name="Tripo_Primary_Root";
    root.userData={primaryCharacter:TRIPO_PRIMARY_ID,engineRole:"primary-character",sourceFormat:"glTF-2.0-static-to-rigid",source:TRIPO_PRIMARY_SOURCE};
    characterRoot.scale.setScalar(spec.proportions.overallScale);characterRoot.add(root);characterRoot.userData.primaryCharacter=TRIPO_PRIMARY_ID;
    const groups=tripoPrimaryRig(descriptor,root),owned={geometries:[]};
    tripoPrimaryAttachParts(descriptor,root,groups,tripoPrimaryMaterials,owned);
    socket(characterRoot,"root",[0,0,0]);
    socket(joints.chest,"chest",[0,.73,.42]);socket(joints.chest,"back",[0,.62,-.42]);socket(joints.head,"head",[0,.74,0]);
    socket(joints.wristL,"hand.L",[0,-.34,.10]);socket(joints.wristR,"hand.R",[0,-.34,.10]);
    socket(joints.ankleL,"foot.L",[0,-.40,.45]);socket(joints.ankleR,"foot.R",[0,-.40,.45]);
    tripoPrimaryInstance={root,materials:tripoPrimaryMaterials,descriptor,dispose(){
      for(const g of owned.geometries)g.dispose?.();
    }};
    compensatePivotOnly();applyCapturedPose(oldPose);if(!Object.keys(oldPose||{}).length)applyPose("idle");
    refreshHierarchy();selectJoint(selectedJoint in joints?selectedJoint:"pelvis");updatePartCount();if($("#animationClipSelect"))buildAnimationUI(false);
    toast(`Tripo primary · ${(descriptor.stats?.sourceTriangles||0).toLocaleString()} tris · ${descriptor.rig?.pose||"rigid"}`);
    return root;
  }catch(error){
    console.error("Tripo primary character failed; using Blue Explorer fallback",error);tripoPrimaryDisposeInstance();characterRoot.userData.primaryCharacter=BLUE_EXPLORER_PRIMARY_ID;
    return buildBlueExplorerPrimaryCharacter(preserve);
  }
}
async function preloadTripoPrimaryCharacter(){
  if(tripoPrimaryDescriptor&&tripoPrimaryMaterials?.length)return tripoPrimaryDescriptor;
  if(tripoPrimaryLoading)return tripoPrimaryLoading;
  tripoPrimaryLoading=(async()=>{
    const response=await fetch(TRIPO_PRIMARY_DESCRIPTOR_URL,{cache:"no-cache"});
    if(!response.ok)throw new Error(`Tripo descriptor HTTP ${response.status}`);
    const descriptor=await response.json();
    if(descriptor?.schema!=="studio-rigid-glb-v1"||descriptor?.id!==TRIPO_PRIMARY_ID)throw new Error("Tripo rigid descriptor contract mismatch");
    tripoPrimaryDescriptor=descriptor;tripoPrimaryMaterials=await tripoPrimaryBuildMaterials(descriptor);
    buildTripoPrimaryCharacter(true);return descriptor;
  })().catch(error=>{
    console.error("Tripo primary preload failed; keeping Blue Explorer fallback",error);toast("Tripo model load failed · using Blue Explorer fallback");return null;
  });
  return tripoPrimaryLoading;
}
function buildCharacter(preserve=true){return buildTripoPrimaryCharacter(preserve)}
if(typeof window!=="undefined"){
  window.TRIPO_PRIMARY_CHARACTER={id:TRIPO_PRIMARY_ID,source:TRIPO_PRIMARY_SOURCE,load:preloadTripoPrimaryCharacter};
  const boot=()=>setTimeout(()=>{preloadTripoPrimaryCharacter()},0);
  if(document.readyState==="loading")window.addEventListener("DOMContentLoaded",boot,{once:true});else boot();
}
'''
    html = html.replace(anchor, adapter, 1)
    html = html.replace('Character Prototype Studio V1.8.10.6', 'Character Prototype Studio V1.8.10.7')
    html = html.replace('studioVersion:"1.8.10.6"', 'studioVersion:"1.8.10.7"')
    html = html.replace('sourceCharacter:"blue-explorer-primary-v1"', 'sourceCharacter:"tripo-5889e73e-rigid-v1"')
    return html


if __name__ == '__main__':
    import sys
    path = Path(sys.argv[1])
    path.write_text(patch(path.read_text(encoding='utf-8')), encoding='utf-8')
