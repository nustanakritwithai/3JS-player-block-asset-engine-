#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    anchor = 'function createAttackTemplate(){'
    if anchor not in html:
        raise RuntimeError('missing anchor: Pocket Studio material pack')
    extension = r'''
/* Deterministic host-applied 2K PBR fallback for the default Studio material roles.
 * It does not mutate the Studio editor materials or create renderer/lights. */
const pocketStudioBaseRenderProfile=pocketStudioRenderProfile;
const POCKET_STUDIO_GENERATED_MATERIAL_PACK=Object.freeze({
  skin:Object.freeze({map:"skin_warm_basecolor.webp",normalMap:"skin_warm_normal.png",roughnessMap:"skin_warm_roughness.webp",aoMap:"skin_warm_ao.webp"}),
  hair:Object.freeze({map:"hair_dark_basecolor.webp",normalMap:"hair_dark_normal.png",roughnessMap:"hair_dark_roughness.webp",aoMap:"hair_dark_ao.webp"}),
  shirt:Object.freeze({map:"cloth_navy_basecolor.webp",normalMap:"cloth_weave_normal.png",roughnessMap:"cloth_roughness.webp",aoMap:"cloth_ao.webp"}),
  pants:Object.freeze({map:"cloth_navy_basecolor.webp",normalMap:"cloth_weave_normal.png",roughnessMap:"cloth_roughness.webp",aoMap:"cloth_ao.webp"}),
  accent:Object.freeze({map:"gold_basecolor.webp",normalMap:"gold_normal.png",roughnessMap:"gold_roughness.webp",metalnessMap:"gold_metalness.webp",aoMap:"gold_ao.webp"}),
  boots:Object.freeze({map:"leather_brown_basecolor.webp",normalMap:"leather_brown_normal.png",roughnessMap:"leather_brown_roughness.webp",aoMap:"leather_brown_ao.webp"}),
  eyes:Object.freeze({map:"emissive_cyan_basecolor.webp",emissiveMap:"emissive_cyan_emissive.webp",roughnessMap:"emissive_cyan_roughness.webp"})
});
function pocketStudioGeneratedTextureMeta(file,slot){
  const source=new URL(`assets/textures/${file}`,location.href).href;
  const integrity=POCKET_STUDIO_TEXTURE_INTEGRITY[`assets/textures/${file}`]||null;
  const colorData=slot==="map"||slot==="emissiveMap"?"color":"data";
  return {source,integrity,colorData,colorSpace:colorData==="color"?"srgb":null,flipY:false,wrapS:null,wrapT:null,minFilter:null,magFilter:null,generateMipmaps:true,anisotropy:4,repeat:[1,1],offset:[0,0],center:[0,0],rotation:0};
}
pocketStudioRenderProfile=function pocketStudioRenderProfileWithGeneratedPack(sceneGraph){
  const base=pocketStudioBaseRenderProfile(sceneGraph);
  const textures=[...(base.textures||[])];
  const byKey=new Map();
  for(const texture of textures){const role=texture.colorData||(texture.colorSpace?"color":"data");byKey.set(`${texture.source}|${role}`,texture.id)}
  const ensure=(file,slot)=>{
    const meta=pocketStudioGeneratedTextureMeta(file,slot);const key=`${meta.source}|${meta.colorData}`;
    if(byKey.has(key))return byKey.get(key);
    const id=pocketStudioStableId("studio-texture",key);byKey.set(key,id);textures.push({id,...meta});return id;
  };
  const materials=(base.materials||[]).map(material=>{
    if(Object.keys(material.textureSlots||{}).length)return material;
    const role=String(material.name||"").trim().toLowerCase();const pack=POCKET_STUDIO_GENERATED_MATERIAL_PACK[role];
    if(!pack)return material;
    const textureSlots={};for(const [slot,file] of Object.entries(pack))textureSlots[slot]=ensure(file,slot);
    return {...material,textureSlots,generatedMaterialRole:role};
  });
  return {...base,textures,materials,generatedMaterialPack:{id:"studio-starter-pbr-2k-v1",masterResolution:2048,hostApplied:true,colorDataSeparated:true}};
};
'''
    return html.replace(anchor, extension + '\n' + anchor, 1)


if __name__ == '__main__':
    import sys
    p = Path(sys.argv[1])
    p.write_text(patch(p.read_text(encoding='utf-8')), encoding='utf-8')
