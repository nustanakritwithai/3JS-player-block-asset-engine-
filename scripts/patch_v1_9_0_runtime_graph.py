#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    def rep(old, new, label, count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: ' + label)
        html = html.replace(old, new, count)

    anchor = 'async function buildPocketRuntimePackageV190({requireQa=false}={}){'
    funcs = r'''function pocketRuntimeTextureRefV190(texture){
  if(!texture)return null;const image=texture.image||texture.source?.data||null;
  const source=typeof image?.currentSrc==="string"&&image.currentSrc?image.currentSrc:typeof image?.src==="string"?image.src:null;
  return {uuid:texture.uuid||null,name:texture.name||null,source,width:Number(image?.width)||0,height:Number(image?.height)||0,colorSpace:texture.colorSpace||null,wrapS:texture.wrapS??null,wrapT:texture.wrapT??null,flipY:typeof texture.flipY==="boolean"?texture.flipY:null};
}
function pocketRuntimeMaterialSnapshotV190(material){
  if(Array.isArray(material))return material.map(pocketRuntimeMaterialSnapshotV190);
  if(!material)return null;
  const colorValue=c=>c&&typeof c.getHexString==="function"?`#${c.getHexString()}`:null;
  return {
    type:material.type||"Material",name:material.name||null,
    color:colorValue(material.color),emissive:colorValue(material.emissive),emissiveIntensity:Number(material.emissiveIntensity)||0,
    roughness:Number.isFinite(material.roughness)?material.roughness:null,metalness:Number.isFinite(material.metalness)?material.metalness:null,
    opacity:Number.isFinite(material.opacity)?material.opacity:1,transparent:!!material.transparent,alphaTest:Number(material.alphaTest)||0,
    side:material.side??null,vertexColors:!!material.vertexColors,flatShading:!!material.flatShading,
    maps:{map:pocketRuntimeTextureRefV190(material.map),normalMap:pocketRuntimeTextureRefV190(material.normalMap),roughnessMap:pocketRuntimeTextureRefV190(material.roughnessMap),metalnessMap:pocketRuntimeTextureRefV190(material.metalnessMap),emissiveMap:pocketRuntimeTextureRefV190(material.emissiveMap),aoMap:pocketRuntimeTextureRefV190(material.aoMap),alphaMap:pocketRuntimeTextureRefV190(material.alphaMap)}
  };
}
function pocketRuntimeGeometrySnapshotV190(geometry){
  if(!geometry)return null;const attributes={};
  for(const [name,attr] of Object.entries(geometry.attributes||{})){
    if(!attr?.array)continue;attributes[name]={itemSize:attr.itemSize,normalized:!!attr.normalized,count:attr.count,arrayType:attr.array?.constructor?.name||"Float32Array",array:Array.from(attr.array)};
  }
  return {
    type:geometry.type||"BufferGeometry",name:geometry.name||null,
    parameters:sanitizePocketRuntimeValueV190(geometry.parameters||{})||{},
    attributes,index:geometry.index?.array?{itemSize:1,count:geometry.index.count,arrayType:geometry.index.array?.constructor?.name||"Uint16Array",array:Array.from(geometry.index.array)}:null,
    groups:(geometry.groups||[]).map(g=>({start:g.start,count:g.count,materialIndex:g.materialIndex})),
    drawRange:geometry.drawRange?{start:geometry.drawRange.start,count:geometry.drawRange.count}:null
  };
}
function pocketRuntimeTransformSnapshotV190(node){
  return {
    position:[Number(node?.position?.x)||0,Number(node?.position?.y)||0,Number(node?.position?.z)||0],
    rotation:[Number(node?.rotation?.x)||0,Number(node?.rotation?.y)||0,Number(node?.rotation?.z)||0,node?.rotation?.order||"XYZ"],
    scale:[Number(node?.scale?.x)||1,Number(node?.scale?.y)||1,Number(node?.scale?.z)||1]
  };
}
function pocketRuntimeSceneNodeV190(node,stats){
  const isMesh=!!node?.isMesh||node?.type==="Mesh",cleanUser=sanitizePocketRuntimeValueV190(node?.userData||{},stats)||{};
  const out={name:node?.name||"",nodeType:isMesh?"mesh":"group",visible:node?.visible!==false,transform:pocketRuntimeTransformSnapshotV190(node),userData:cleanUser,children:[]};
  if(isMesh){out.geometry=pocketRuntimeGeometrySnapshotV190(node.geometry);out.material=pocketRuntimeMaterialSnapshotV190(node.material);out.castShadow=!!node.castShadow;out.receiveShadow=!!node.receiveShadow}
  for(const child of node?.children||[])out.children.push(pocketRuntimeSceneNodeV190(child,stats));
  return out;
}
function pocketRuntimeSceneGraphV190(root,stats){
  const graph=pocketRuntimeSceneNodeV190(root,stats),counts={nodes:0,meshes:0,vertices:0,triangles:0,externalTextureRefs:0};
  const countTexture=ref=>{if(ref?.source)counts.externalTextureRefs++};
  const visit=node=>{counts.nodes++;if(node.nodeType==="mesh"){counts.meshes++;const pos=node.geometry?.attributes?.position;counts.vertices+=Number(pos?.count)||0;const idx=node.geometry?.index?.count;counts.triangles+=idx?Math.floor(idx/3):Math.floor((Number(pos?.count)||0)/3);const mats=Array.isArray(node.material)?node.material:[node.material];for(const mat of mats)for(const ref of Object.values(mat?.maps||{}))countTexture(ref)}for(const child of node.children||[])visit(child)};
  visit(graph);return {schema:"three-group-scenegraph-v1",root:graph,stats:counts};
}
function pocketRuntimeJointBindingsV190(root){
  const paths=new Map();
  const visit=(node,path)=>{paths.set(node,path);(node?.children||[]).forEach((child,index)=>visit(child,[...path,index]))};
  visit(root,[]);const bindings={};
  for(const [jointKey,node] of Object.entries(joints||{})){
    const path=paths.get(node);if(!path)continue;
    bindings[jointKey]={path,nodeName:node?.name||null};
  }
  return bindings;
}

'''+anchor
    rep(anchor, funcs, 'runtime scene graph serializer')

    rep('''    character:cleanSpec,\n    rig:{architecture:"THREE.Group"''',
        '''    character:cleanSpec,\n    sceneGraph:pocketRuntimeSceneGraphV190(characterRoot,stats),\n    rig:{architecture:"THREE.Group"''',
        'runtime scene graph package field')

    rep('''    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),sockets},''',
        '''    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),jointBindings:pocketRuntimeJointBindingsV190(characterRoot),sockets},''',
        'deterministic joint bindings')

    rep('''  if(!pkg?.rig?.sockets?.rightHand||!pkg?.rig?.sockets?.leftHand)errors.push("hand sockets missing");\n  const leaks=pocketRuntimeGameplayLeaksV190(pkg);''',
        '''  if(!pkg?.rig?.sockets?.rightHand||!pkg?.rig?.sockets?.leftHand)errors.push("hand sockets missing");\n  if(!pkg?.rig?.jointBindings||!Object.keys(pkg.rig.jointBindings).length)errors.push("joint bindings missing");\n  if(pkg?.sceneGraph?.schema!=="three-group-scenegraph-v1"||!pkg?.sceneGraph?.root)errors.push("portable scene graph missing");\n  if(!(pkg?.sceneGraph?.stats?.meshes>0))warnings.push("scene graph contains no mesh nodes");\n  if(pkg?.sceneGraph?.stats?.externalTextureRefs)warnings.push(`${pkg.sceneGraph.stats.externalTextureRefs} texture map reference(s) remain external; material scalar fallback is included`);\n  const leaks=pocketRuntimeGameplayLeaksV190(pkg);''',
        'runtime scene graph validation')

    return html


if __name__ == '__main__':
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
