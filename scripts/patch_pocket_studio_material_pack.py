#!/usr/bin/env python3
"""Export selected Studio materials deterministically on cold and warm loads."""
from pathlib import Path


def patch(html):
    anchor = 'function createAttackTemplate(){'
    if anchor not in html:
        raise RuntimeError('missing anchor: Pocket Studio material pack')
    extension = r'''// Only exported snapshots are changed; editor materials and user choices are untouched.
const pocketStudioBaseRenderProfile=pocketStudioRenderProfile;
const POCKET_STUDIO_MAP_TYPES=Object.freeze({baseColor:"map",normal:"normalMap",roughness:"roughnessMap",metalness:"metalnessMap",ao:"aoMap",emissive:"emissiveMap"});
function pocketStudioDeclaredTexture(slotName,type){
  const sys=spec?.skinSystem,slot=sys?.slots?.[slotName];
  if(!sys?.enabled||!slot||typeof textureSourceFor!=="function")return undefined;
  const source=textureSourceFor(slotName,type);
  if(!source)return null;
  // Blob/data/custom URLs are NOT replaced by starter images. The base exporter
  // records its same-origin rejection; scalar PBR stays available to the game.
  let integrity=null;
  try{const url=new URL(source,location.href),marker="/assets/",at=url.pathname.indexOf(marker);
    if(url.origin===location.origin&&at>=0)integrity=POCKET_STUDIO_TEXTURE_INTEGRITY[`assets/${url.pathname.slice(at+marker.length)}`]||null;
  }catch{}
  const color=type==="baseColor"||type==="emissive";
  return {source,colorSpace:color?"srgb":"",integrity,integrityStatus:integrity?"producer-supplied":"unavailable-in-sync-export",
    flipY:true,wrapS:1000,wrapT:1000,minFilter:1008,magFilter:1006,generateMipmaps:true,
    anisotropy:Math.max(1,Math.min(16,Number(sys.anisotropy)||8)),
    repeat:Array.isArray(slot.repeat)?[...slot.repeat]:[1,1],offset:Array.isArray(slot.offset)?[...slot.offset]:[0,0],center:[.5,.5],rotation:(Number(slot.rotation)||0)*Math.PI/180};
}
pocketStudioRenderProfile=function pocketStudioRenderProfileWithDeclaredMaterials(sceneGraph){
  let declared=0;
  function visit(node){
    const list=Array.isArray(node?.material)?node.material:node?.material?[node.material]:[];
    for(const material of list){
      const role=String(material?.name||"");
      if(!spec?.skinSystem?.enabled||!spec.skinSystem.slots?.[role])continue;
      material.maps??={};
      for(const [type,slot] of Object.entries(POCKET_STUDIO_MAP_TYPES)){
        const ref=pocketStudioDeclaredTexture(role,type);
        if(ref===undefined)continue;
        material.maps[slot]=ref;
        if(ref){declared++;if(type==="emissive"){material.emissive="#ffffff";material.emissiveIntensity=.75}}
      }
      const strength=Number(spec.skinSystem.slots[role].normalScale);
      if(Number.isFinite(strength))material.normalScale=[strength,strength];
    }
    for(const child of node?.children||[])visit(child);
  }
  visit(sceneGraph?.root);
  const base=pocketStudioBaseRenderProfile(sceneGraph);
  return {...base,generatedMaterialPack:{id:"studio-starter-pbr-2k-v1",masterResolution:2048,hostApplied:true,colorDataSeparated:true,
    source:"selected-studio-skin-config",declaredBindings:declared,readiness:"source-declared-host-loads"}};
};
'''
    return html.replace(anchor, extension + '\n' + anchor, 1)


if __name__ == '__main__':
    import sys
    p = Path(sys.argv[1])
    p.write_text(patch(p.read_text(encoding='utf-8')), encoding='utf-8')
