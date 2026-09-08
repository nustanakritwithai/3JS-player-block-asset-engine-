import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { spawnSync } from 'node:child_process';
import os from 'node:os';
import path from 'node:path';
// Run the production bridge from built output, including its public exporter.
const html=fs.readFileSync('_site/index.html','utf8');
// Check the actual ES module, not just the permissive VM script context.
const moduleCode=[...html.matchAll(/<script type="module">([\s\S]*?)<\/script>/g)].at(-1)?.[1];
assert.ok(moduleCode);
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'studio-module-'));
try{const file=path.join(temp,'studio.mjs');fs.writeFileSync(file,moduleCode);const check=spawnSync(process.execPath,['--check',file],{encoding:'utf8'});assert.equal(check.status,0,check.stderr)}
finally{fs.rmSync(temp,{recursive:true,force:true})}
const start=html.indexOf('const POCKET_STUDIO_BRIDGE_REQUEST=');
const end=html.indexOf('function createAttackTemplate(){',start);
assert.ok(start>=0&&end>start);
const location={href:'https://studio.example/index.html',origin:'https://studio.example'};
const root={name:'root',children:[{name:'body',isMesh:true,material:{},children:[]}]};
const context=vm.createContext({URL,location,window:{location,addEventListener(){}},characterRoot:root,joints:{},spec:{look:{shadows:true}},
rad:v=>v*Math.PI/180,poseSnapshotFromLibrary:()=>({chest:{rotation:[0,0,0],position:[0,0,0]}}),cloneAnimationPose:v=>structuredClone(v),
makeAnimationClip:(name,duration)=>({name,duration,runtime:{}}),createTemplateClip:(name,duration,fps,keys,loop)=>({name,duration,loop,runtime:{},keyframes:keys.map(key=>({time:key.time,joints:{chest:{rotation:[0,0,Number(key.time)||0],position:[0,0,0]}}}))})});
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
 const pkg=build();assert.equal(pkg.renderProfile.textures.length,2);const texture=pkg.renderProfile.textures.find(t=>t.colorSpace==='srgb');assert.equal(texture.source,'https://studio.example/assets/textures/base.png');assert.equal(texture.integrity,integrity);assert.equal(texture.colorSpace,'srgb');const mapped=pkg.renderProfile.materials[0].textureSlots;assert.equal(mapped.map,mapped.emissiveMap);assert.notEqual(mapped.map,mapped.normalMap);assert.equal(pkg.renderProfile.textures.find(t=>t.id===mapped.normalMap).colorSpace,'');
}
const pkg=build();
assert.equal(pkg.motionPack.version,'1.1.0');
assert.equal(pkg.motionPack.actionMap.capture_throw,'capture_throw_r');
assert.equal(pkg.motionPack.actionMap.summon_monster_throw,'summon_monster_throw');
assert.equal(pkg.motionPack.actionMap.monster_command,'monster_command');
assert.equal(pkg.motionPack.actionMap.skill,undefined,'generic skill must not masquerade as Capture Throw');
assert.equal(pkg.motionPack.actionMap['attack-ranged'],undefined,'ranged attack must not masquerade as Capture Throw');
assert.match(pkg.motionPack.unsupportedActions.skill,/No distinct authored generic skill pose/);
assert.match(pkg.motionPack.unsupportedActions['attack-ranged'],/No distinct authored ranged-weapon attack pose/);
for(const required of ['idle','walk','run','jump','attack','hurt','dead','capture_throw','summon_monster_throw','monster_command'])assert.ok(pkg.motionPack.requiredActions.includes(required));
const capture=pkg.animations.find(clip=>clip.runtime?.state==='capture_throw_r');
const summon=pkg.animations.find(clip=>clip.runtime?.state==='summon_monster_throw');
const attack=pkg.animations.find(clip=>clip.runtime?.state==='attack');
function assertEvent(clip,type,time){assert.equal(clip.events?.length,1);assert.equal(clip.events[0].type,type);assert.equal(clip.events[0].time,time)}
assertEvent(capture,'release',.56);
assertEvent(summon,'release',.55);
assertEvent(attack,'impact',.48);
for(const clip of [capture,summon,attack])assert.ok(clip.keyframes.length>=2);
assert.ok(pkg.animationIndex.find(item=>item.state==='capture_throw_r')?.events?.some(event=>event.type==='release'&&event.time===.56));
console.log('PASS: built exporter handles texture edge cases, preserves truthful motion semantics, and exports authored action event timing');

// Selected material sources/UVs must not depend on async loader timing.
context.spec.skinSystem={enabled:true,anisotropy:4,slots:{skin:{asset:'skin_warm',repeat:[2,3],offset:[.1,.2],rotation:30,normalScale:.4}}};
context.textureSourceFor=(_role,type)=>({baseColor:'/assets/textures/skin_warm_basecolor.webp',normal:'/assets/textures/skin_warm_normal.png'}[type]||null);
root.children[0].material={name:'skin',maps:{}};
const cold=build();
root.children[0].material={name:'skin',map:{image:{src:'old-cached-canvas'}},normalMap:{image:{src:'old-cached-canvas'}}};
const warm=build();
assert.equal(JSON.stringify(cold.renderProfile),JSON.stringify(warm.renderProfile),'cold/warm exports must have identical material descriptors');
assert.equal(cold.renderProfile.textures.length,2);
for(const texture of cold.renderProfile.textures){assert.match(texture.integrity,/^[a-f0-9]{64}$/);assert.equal(texture.repeat[0],2);assert.equal(texture.repeat[1],3);assert.ok(Math.abs(texture.rotation-Math.PI/6)<1e-9)}
const stable=build();assert.equal(stable.animations[0].id,build().animations[0].id,'default template ids must be stable');
context.textureSourceFor=()=> 'blob:https://studio.example/creator-image';
const custom=build();assert.equal(custom.renderProfile.textures.length,0,'custom blob must not silently become starter material');assert.ok(custom.renderProfile.rejectedSources.length>0);
context.spec.skinSystem.enabled=false;
root.children[0].material={name:'skin'};
assert.equal(build().renderProfile.textures.length,0,'explicitly disabled skins remain untextured');
// A genuinely authored skill fills the gap; no substitution with Capture Throw.
context.spec.animations=[{id:'authored-skill',name:'Skill',duration:1,runtime:{state:'skill'},keyframes:[{time:0,joints:{chest:{rotation:[0,0,0]}}},{time:1,joints:{chest:{rotation:[1,0,0]}}}]}];
const authored=build();assert.equal(authored.motionPack.actionMap.skill,'skill');assert.equal(authored.motionPack.unsupportedActions.skill,undefined);assert.equal(authored.animations.find(c=>c.id==='authored-skill').keyframes.length,2);
console.log('PASS: final module syntax, selected PBR 2K sources, cold/warm equality, per-slot color data, custom/disabled preservation, stable ids, and authored overrides');
