import { MATERIALS, readGroundFrame } from './worldsim-ground-adapter.mjs';
import { buildGroundGeometry, validateGroundTransform } from './ground-geometry.mjs';
export const QUALITY = Object.freeze({low:Object.freeze({textureSize:512,anisotropy:2}),medium:Object.freeze({textureSize:1024,anisotropy:4}),high:Object.freeze({textureSize:2048,anisotropy:8})});
const COLORS=[0x788b43,0x65583d,0x655849,0xc7b78c,0x898b87,0xa28b60,0x403c38];
const MAP_SLOTS={albedo:'map',normal:'normalMap',roughness:'roughnessMap',ao:'aoMap'};
/** Patch only presentation values; no change to simulation wetness/fire stores. */
export function installSurfaceShader(material) {
  material.onBeforeCompile=shader=>{
    for (const marker of ['#include <common>','#include <begin_vertex>']) if (!shader.vertexShader.includes(marker)) throw new Error(`Unsupported Three.js vertex shader: ${marker}`);
    for (const marker of ['#include <common>','#include <color_fragment>','#include <roughnessmap_fragment>']) if (!shader.fragmentShader.includes(marker)) throw new Error(`Unsupported Three.js fragment shader: ${marker}`);
    shader.vertexShader=shader.vertexShader.replace('#include <common>','#include <common>\nattribute vec2 groundSurface;\nvarying vec2 vGroundSurface;').replace('#include <begin_vertex>','#include <begin_vertex>\nvGroundSurface = groundSurface;');
    shader.fragmentShader=shader.fragmentShader.replace('#include <common>','#include <common>\nvarying vec2 vGroundSurface;').replace('#include <color_fragment>','#include <color_fragment>\ndiffuseColor.rgb *= mix(1.0, 0.63, vGroundSurface.x) * mix(1.0, 0.4, vGroundSurface.y);').replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\nroughnessFactor = clamp(roughnessFactor * mix(1.0, 0.48, vGroundSurface.x), 0.12, 1.0);');
  };
  material.customProgramCacheKey=()=> 'worldsim-ground-surface-v1';
}
/** Inject the game's existing THREE instance and scene. Does not construct a
 * WebGLRenderer, timer, simulation, physics body, or network connection. */
export function createWorldGroundRenderer({THREE,scene,transform,quality='medium',maxAnisotropy=1}) {
  if (!THREE || !scene?.add || !QUALITY[quality]) throw new TypeError('THREE, scene and a supported quality are required');
  transform=validateGroundTransform(transform);
  if(!Number.isFinite(maxAnisotropy)||maxAnisotropy<1)throw new RangeError('Invalid maxAnisotropy');
  const root=new THREE.Group();root.name='WorldSimGroundPresentation';scene.add(root);
  const materials=MATERIALS.map((_,i)=>{const m=new THREE.MeshStandardMaterial({color:COLORS[i],roughness:0.95,metalness:0});installSurfaceShader(m);return m;});
  const waterMaterial=new THREE.MeshStandardMaterial({color:0x3a879c,roughness:0.24,metalness:0,transparent:true,opacity:0.62,depthWrite:false});
  let disposed=false,lastInput=null,currentFrame=null;
  const ownedTextures=new Set();
  function alive(){if(disposed) throw new Error('Ground renderer has been disposed');}
  function clearGeometry(){for(const mesh of [...root.children]){root.remove(mesh);mesh.geometry.dispose();}}
  function mesh(data,material,name){
    if (!data.position.length) return;
    const geometry=new THREE.BufferGeometry();
    for(const [key,itemSize] of [['position',3],['normal',3],['uv',2]]) geometry.setAttribute(key,new THREE.BufferAttribute(data[key],itemSize));
    // AO can use a second UV channel; retain uv2 for older consumers too.
    geometry.setAttribute('uv1',new THREE.BufferAttribute(data.uv.slice(),2));
    geometry.setAttribute('uv2',new THREE.BufferAttribute(data.uv.slice(),2));
    geometry.setAttribute('groundSurface',new THREE.BufferAttribute(data.surface,2));
    geometry.computeBoundingSphere();
    const object=new THREE.Mesh(geometry,material);object.name=name;object.receiveShadow=true;root.add(object);
  }
  function setFrame(input){
    alive();if(input===lastInput && Object.isFrozen(input) && Object.isFrozen(input.channels) && Object.values(input.channels).every(Object.isFrozen))return false;
    // Validate and build before replacing the currently visible frame.
    const frame=readGroundFrame(input),data=buildGroundGeometry(frame,transform);
    clearGeometry();data.terrain.forEach((b,i)=>mesh(b,materials[i],MATERIALS[i]));mesh(data.water,waterMaterial,'authoritative-water-surface');
    lastInput=input;currentFrame=frame;return true;
  }
  /** Texture objects stay owned by caller; this renderer clones/configures its own.
   * Albedo is sRGB; normal/roughness/AO are data maps. No synthetic PBR from albedo.
   * Quality resizing belongs to the image loader before creating the textures. */
  function setTexture(materialId,slot,texture,{normalConvention='opengl'}={}){
    alive();const index=MATERIALS.indexOf(materialId),property=MAP_SLOTS[slot];
    if(index<0||!property)throw new TypeError('Unknown material/texture slot');
    if(!['opengl','directx'].includes(normalConvention))throw new TypeError('Unknown normal convention');
    if(texture!==null&&!texture?.isTexture)throw new TypeError('A THREE.Texture or null is required');
    const material=materials[index],old=material[property];
    const next=texture?.clone()??null;
    if(next){
      next.colorSpace=slot==='albedo'?THREE.SRGBColorSpace:THREE.NoColorSpace;
      next.wrapS=next.wrapT=THREE.RepeatWrapping;next.generateMipmaps=true;
      next.minFilter=THREE.LinearMipmapLinearFilter;next.magFilter=THREE.LinearFilter;
      next.anisotropy=Math.max(1,Math.min(maxAnisotropy,QUALITY[quality].anisotropy));
      next.channel=slot==='ao'?1:0;next.needsUpdate=true;ownedTextures.add(next);
    }
    material[property]=next;
    if(slot==='albedo')material.color.set(next?0xffffff:COLORS[index]);
    if(slot==='normal')material.normalScale.set(1,normalConvention==='directx'?-1:1);
    material.needsUpdate=true;
    if(old&&ownedTextures.delete(old))old.dispose();
  }
  return Object.freeze({root,setFrame,setTexture,getFrame:()=>currentFrame,getBudget:()=>QUALITY[quality],
    dispose(){if(disposed)return;clearGeometry();for(const t of ownedTextures)t.dispose();ownedTextures.clear();for(const m of materials)m.dispose();waterMaterial.dispose();scene.remove(root);currentFrame=null;lastInput=null;disposed=true;}
  });
}
