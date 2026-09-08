import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
// Run the production bridge from built output, including its public exporter.
const html=fs.readFileSync('_site/index.html','utf8');
const start=html.indexOf('const POCKET_STUDIO_BRIDGE_REQUEST=');
const end=html.indexOf('function createAttackTemplate(){',start);
assert.ok(start>=0&&end>start);
const location={href:'https://studio.example/index.html',origin:'https://studio.example'};
const root={name:'root',children:[{name:'body',isMesh:true,material:{},children:[]}]};
const context=vm.createContext({URL,location,window:{location,addEventListener(){}},characterRoot:root,joints:{},spec:{look:{shadows:true}},
rad:v=>v*Math.PI/180,poseSnapshotFromLibrary:()=>({chest:{rotation:[0,0,0],position:[0,0,0]}}),cloneAnimationPose:v=>structuredClone(v),
makeAnimationClip:(name,duration)=>({name,duration,runtime:{}}),createTemplateClip:(name,duration,fps,keys,loop)=>({name,duration,loop,runtime:{},keyframes:keys})});
vm.runInContext(html.slice(start,end),context);
const build=context.window.POCKET_STUDIO_CHARACTER_BRIDGE.buildPackage;
const slots=['map','normalMap','roughnessMap','metalnessMap','emissiveMap','aoMap','alphaMap'];
for(const value of [null,undefined,{}, {image:{}}]){
 root.children[0].material=Object.fromEntries(slots.map(slot=>[slot,value]));
 const pkg=build();assert.equal(pkg.renderProfile.textures.length,0);assert.equal(Object.keys(pkg.renderProfile.materials[0].textureSlots).length,0);assert.ok(pkg.animations.length>=8);assert.equal(pkg.gameplayPolicy.included,false);
}
for(const source of [undefined,null,'','   ',123,{},[],false,'http://studio.example/a.png','https://other.example/a.png','data:image/png;base64,AA'])assert.equal(context.pocketStudioSafeTextureSource(source),null);
for(const ref of [null,undefined,false,123,'',[],{},{source:null},{source:''}]){
 const profile=context.pocketStudioRenderProfile({root:{nodeType:'mesh',material:{maps:{map:ref}}}});assert.equal(profile.textures.length,0);
}
const integrity='a'.repeat(64);
for(const source of ['/assets/textures/base.png','https://studio.example/assets/textures/base.png']){
 root.children[0].material=Object.fromEntries(slots.map(slot=>[slot,{image:{src:source},colorSpace:'srgb',userData:{pocketIntegritySha256:integrity}}]));
 const pkg=build();assert.equal(pkg.renderProfile.textures.length,1);const texture=pkg.renderProfile.textures[0];assert.equal(texture.source,'https://studio.example/assets/textures/base.png');assert.equal(texture.integrity,integrity);assert.equal(texture.colorSpace,'srgb');for(const slot of slots)assert.equal(pkg.renderProfile.materials[0].textureSlots[slot],texture.id);
}
console.log('PASS: built exporter handles absent maps and malformed refs, preserves valid texture metadata and motion pack');
