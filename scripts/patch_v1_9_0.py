#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    def rep(old, new, label, count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: ' + label)
        html = html.replace(old, new, count)

    html = html.replace('Character Prototype Studio V1.8.10', 'Character Prototype Studio V1.9.0')
    html = html.replace('V1.8.10 · Core Animation QA / Transitions', 'V1.9.0 · Pocket Runtime Character Export')
    html = html.replace('generatorVersion:"1.8.10"', 'generatorVersion:"1.9.0"')

    qa_anchor = '''            <div class="qaIssues" id="coreAnimationQaIssues" style="margin-top:7px">\n              <div class="qaIssue good">พร้อมตรวจ Core Animation Pack</div>\n            </div>\n          </div>'''
    export_ui = qa_anchor + '''\n          <div class="chainbox" id="pocketRuntimeExportBox" style="margin-top:8px">\n            <h3>POCKET MONSTER RUNTIME EXPORT <span class="posebadge" id="pocketRuntimeExportStatus">READY</span></h3>\n            <div class="hint">V1.9.0 สร้าง self-contained .pocket-character.json สำหรับ Pocket Monster Asset Engine · presentation-only · ไม่ส่ง gameplay stats</div>\n            <div class="row" style="margin-top:7px">\n              <label class="grow" style="font-size:9px;color:var(--muted)">Character ID\n                <input id="pocketRuntimeCharacterId" value="character.human.pirate.custom001" spellcheck="false">\n              </label>\n              <label class="grow" style="font-size:9px;color:var(--muted)">Display Name\n                <input id="pocketRuntimeCharacterName" value="Custom Pirate" spellcheck="false">\n              </label>\n            </div>\n            <div class="qaKpi" style="margin-top:7px">\n              <div><b id="pocketRuntimeClipCount">0</b><small>CLIPS</small></div>\n              <div><b id="pocketRuntimeSocketCount">0</b><small>SOCKETS</small></div>\n              <div><b id="pocketRuntimeStrippedCount">0</b><small>STRIPPED</small></div>\n              <div><b id="pocketRuntimeSize">0</b><small>KB</small></div>\n            </div>\n            <div class="row" style="margin-top:7px">\n              <button class="btn grow" id="btnPreviewPocketRuntime">Validate Package</button>\n              <button class="btn good grow" id="btnExportPocketRuntime">Export for Pocket Monster</button>\n            </div>\n            <div class="qaIssues" id="pocketRuntimeExportIssues" style="margin-top:7px">\n              <div class="qaIssue good">พร้อมสร้าง Runtime Character Package</div>\n            </div>\n          </div>'''
    rep(qa_anchor, export_ui, 'pocket runtime export panel')

    anchor = 'const CORE_ANIMATION_TRANSITIONS_V1_8_10=Object.freeze({'
    funcs = r'''const POCKET_RUNTIME_SCHEMA_V1_9_0="pocket-character-runtime-v1";
const POCKET_RUNTIME_PROVIDER_V1_9_0="studio-character";
const POCKET_RUNTIME_FORBIDDEN_KEYS_V1_9_0=new Set([
  "hp","hpcurrent","hpmax","atk","def","spatk","spdef","spd","vitality","combat","blade","ranged","fruitpower","mastery","mana","coins","capture","save","level","exp","experience","damage"
]);
let pocketRuntimeExportStateV190={last:null,error:null};
function pocketRuntimeNormalizedKeyV190(key){return String(key||"").replace(/[_-]/g,"").toLowerCase()}
function sanitizePocketRuntimeValueV190(value,stats={stripped:0,cycles:0},seen=new WeakSet()){
  if(value===null||typeof value==="string"||typeof value==="number"||typeof value==="boolean")return value;
  if(typeof value==="undefined"||typeof value==="function"||typeof value==="symbol")return undefined;
  if(Array.isArray(value))return value.map(v=>sanitizePocketRuntimeValueV190(v,stats,seen)).filter(v=>typeof v!=="undefined");
  if(typeof value==="object"){
    if(seen.has(value)){stats.cycles++;return null}seen.add(value);
    const out={};
    for(const [key,v] of Object.entries(value)){
      if(POCKET_RUNTIME_FORBIDDEN_KEYS_V1_9_0.has(pocketRuntimeNormalizedKeyV190(key))){stats.stripped++;continue}
      const clean=sanitizePocketRuntimeValueV190(v,stats,seen);if(typeof clean!=="undefined")out[key]=clean;
    }
    seen.delete(value);return out;
  }
  return undefined;
}
function pocketRuntimeCharacterIdV190(){
  const raw=String($("#pocketRuntimeCharacterId")?.value||"character.human.pirate.custom001").trim();
  return /^character\.[a-z0-9][a-z0-9._-]*$/i.test(raw)?raw:null;
}
function pocketRuntimeDisplayNameV190(){return String($("#pocketRuntimeCharacterName")?.value||"Custom Pirate").trim().slice(0,80)||"Custom Pirate"}
function pocketRuntimeHeightV190(){
  const candidates=[spec?.body?.height,spec?.character?.height,spec?.metrics?.height];
  for(const value of candidates){const n=Number(value);if(Number.isFinite(n)&&n>.2&&n<10)return n}
  return 1.8;
}
function pocketRuntimeJointLocatorV190(names){for(const name of names)if(joints?.[name])return name;return names[0]}
function pocketRuntimeSocketsV190(){
  return {
    rightHand:{joint:pocketRuntimeJointLocatorV190(["handR","wristR","elbowR"]),offset:[0,0,0]},
    leftHand:{joint:pocketRuntimeJointLocatorV190(["handL","wristL","elbowL"]),offset:[0,0,0]},
    head:{joint:pocketRuntimeJointLocatorV190(["head","neck"]),offset:[0,0,0]},
    back:{joint:pocketRuntimeJointLocatorV190(["chest","spine","pelvis"]),offset:[0,0,.12]},
    waist:{joint:pocketRuntimeJointLocatorV190(["pelvis","chest"]),offset:[0,0,0]},
    vfxOrigin:{joint:pocketRuntimeJointLocatorV190(["chest","pelvis"]),offset:[0,.12,-.18]},
    attackOrigin:{joint:pocketRuntimeJointLocatorV190(["handR","wristR","elbowR"]),offset:[0,0,-.08]},
    throwOrigin:{joint:pocketRuntimeJointLocatorV190(["handR","wristR","elbowR"]),offset:[0,0,-.08]}
  };
}
function pocketRuntimeAnimationIndexV190(animations){
  return (animations||[]).map(clip=>({
    id:clip.id||null,name:clip.name||"Animation",state:coreAnimationStateV1810(clip),duration:Number(clip.duration)||0,loop:!!clip.loop,
    transition:clip.runtime?.transition||null,
    dynamics:{locomotion:clip.locomotionDynamics||null,body:clip.bodyDynamics||null,footPlant:clip.footPlant||null,attack:clip.attackProfile||null,impact:clip.impactProfile||null}
  }));
}
function pocketRuntimeGameplayLeaksV190(value,path="$"){
  const leaks=[];
  if(Array.isArray(value)){value.forEach((v,i)=>leaks.push(...pocketRuntimeGameplayLeaksV190(v,`${path}[${i}]`)));return leaks}
  if(!value||typeof value!=="object")return leaks;
  for(const [key,v] of Object.entries(value)){
    const next=`${path}.${key}`;
    if(POCKET_RUNTIME_FORBIDDEN_KEYS_V1_9_0.has(pocketRuntimeNormalizedKeyV190(key)))leaks.push(next);
    else leaks.push(...pocketRuntimeGameplayLeaksV190(v,next));
  }
  return leaks;
}
async function pocketRuntimeSha256V190(text){
  if(!globalThis.crypto?.subtle||typeof TextEncoder==="undefined")return null;
  const digest=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,"0")).join("");
}
function validatePocketRuntimePackageV190(pkg){
  const errors=[],warnings=[];
  if(pkg?.schema!==POCKET_RUNTIME_SCHEMA_V1_9_0)errors.push("schema mismatch");
  if(!pkg?.manifest?.id||!/^character\./i.test(pkg.manifest.id))errors.push("invalid character id");
  if(pkg?.manifest?.provider!==POCKET_RUNTIME_PROVIDER_V1_9_0)errors.push("provider must be studio-character");
  if(pkg?.manifest?.contract!=="presentation-only")errors.push("visual contract must be presentation-only");
  if(pkg?.rig?.architecture!=="THREE.Group")errors.push("rig architecture must remain THREE.Group");
  if(!Array.isArray(pkg?.animations))errors.push("animations must be an array");
  if(!pkg?.rig?.sockets?.rightHand||!pkg?.rig?.sockets?.leftHand)errors.push("hand sockets missing");
  const leaks=pocketRuntimeGameplayLeaksV190(pkg);if(leaks.length)errors.push(`gameplay fields leaked: ${leaks.slice(0,4).join(", ")}`);
  if(!(pkg?.animations||[]).length)warnings.push("package has no authored animation clips");
  if(pkg?.acceptance?.coreAnimationQa?.warn)warnings.push(`Core Animation QA has ${pkg.acceptance.coreAnimationQa.warn} warning(s)`);
  return {valid:errors.length===0,errors,warnings};
}
async function buildPocketRuntimePackageV190({requireQa=false}={}){
  const id=pocketRuntimeCharacterIdV190();if(!id)throw new Error("Character ID ต้องขึ้นต้นด้วย character. และใช้ a-z 0-9 . _ - เท่านั้น");
  upgradeExistingCoreTransitionsV1810();
  const qa=runCoreAnimationQaV1810();if(requireQa&&qa?.hard)throw new Error(`Core Animation QA blocked export: ${qa.hard} hard issue(s)`);
  const stats={stripped:0,cycles:0},cleanSpec=sanitizePocketRuntimeValueV190(spec,stats)||{};
  const cleanAnimations=Array.isArray(cleanSpec.animations)?cleanSpec.animations:[];delete cleanSpec.animations;
  const sockets=pocketRuntimeSocketsV190(),height=pocketRuntimeHeightV190(),displayName=pocketRuntimeDisplayNameV190();
  const packageBase={
    schema:POCKET_RUNTIME_SCHEMA_V1_9_0,
    schemaVersion:"1.0.0",
    generatedBy:{product:"3JS Player Block Asset Engine",studioVersion:"1.9.0",generatorVersion:"1.9.0",generatedAt:new Date().toISOString()},
    target:{game:"PocketMonster",assetEngine:"asset-presentation",provider:POCKET_RUNTIME_PROVIDER_V1_9_0,assetHandleContract:["root","rig","play","update","anchor","bounds","setAppearance","dispose"]},
    manifest:{id,name:displayName,kind:"character",provider:POCKET_RUNTIME_PROVIDER_V1_9_0,contract:"presentation-only",style:"blocky-bighead-studio-v1",surfaceStyle:"pbr-studio-v1",rig:"studio-three-group-v1",metrics:{height},roles:{player:{}}},
    catalogEntry:{id,kind:"character",provider:POCKET_RUNTIME_PROVIDER_V1_9_0,style:"blocky-bighead-studio-v1",surfaceStyle:"pbr-studio-v1",rig:"studio-three-group-v1",metrics:{height},roles:{player:{}}},
    character:cleanSpec,
    rig:{architecture:"THREE.Group",schema:"studio-rig-v1",root:"characterRoot",jointNames:Object.keys(joints||{}),sockets},
    animations:cleanAnimations,
    animationIndex:pocketRuntimeAnimationIndexV190(cleanAnimations),
    acceptance:{coreAnimationQa:qa?{version:qa.version,hard:qa.hard,warn:qa.warn,pass:qa.pass,contracts:qa.contracts,total:qa.total}:null},
    gameplayPolicy:{included:false,authority:"Pocket Monster / Pirate Fruit server-domain systems",forbiddenKeys:[...POCKET_RUNTIME_FORBIDDEN_KEYS_V1_9_0].sort(),strippedFields:stats.stripped},
    transport:{format:"single-json-envelope",extension:".pocket-character.json",encoding:"utf-8"}
  };
  const validation=validatePocketRuntimePackageV190(packageBase);if(requireQa&&!validation.valid)throw new Error(validation.errors.join("; "));
  const canonical=JSON.stringify(packageBase),sha256=await pocketRuntimeSha256V190(canonical);
  const pkg={...packageBase,integrity:{algorithm:sha256?"SHA-256":"none",sha256,canonicalBytes:new TextEncoder().encode(canonical).byteLength},validation};
  pocketRuntimeExportStateV190.last=pkg;pocketRuntimeExportStateV190.error=null;renderPocketRuntimeExportV190(pkg);return pkg;
}
function renderPocketRuntimeExportV190(pkg=null,error=null){
  const status=$("#pocketRuntimeExportStatus"),wrap=$("#pocketRuntimeExportIssues");
  if(error){if(status){status.textContent="BLOCKED";status.className="posebadge"}if(wrap)wrap.innerHTML=`<div class="qaIssue bad"><b>EXPORT BLOCKED</b>${escapeHtml(String(error.message||error))}</div>`;return}
  if(!pkg){if(status){status.textContent="READY";status.className="posebadge"}return}
  const bytes=Number(pkg.integrity?.canonicalBytes)||0,validation=pkg.validation||{valid:false,errors:[],warnings:[]};
  if($("#pocketRuntimeClipCount"))$("#pocketRuntimeClipCount").textContent=pkg.animations?.length||0;
  if($("#pocketRuntimeSocketCount"))$("#pocketRuntimeSocketCount").textContent=Object.keys(pkg.rig?.sockets||{}).length;
  if($("#pocketRuntimeStrippedCount"))$("#pocketRuntimeStrippedCount").textContent=pkg.gameplayPolicy?.strippedFields||0;
  if($("#pocketRuntimeSize"))$("#pocketRuntimeSize").textContent=(bytes/1024).toFixed(1);
  if(status){status.textContent=validation.valid?(validation.warnings.length?"VALID+WARN":"VALID"):"BLOCKED";status.className="posebadge "+(validation.valid?"good":"")}
  if(!wrap)return;wrap.innerHTML="";
  if(validation.valid&&!validation.warnings.length)wrap.innerHTML=`<div class="qaIssue good"><b>RUNTIME PACKAGE VALID</b>${escapeHtml(pkg.manifest.id)} · ${pkg.animations.length} clips · SHA-256 ${escapeHtml(String(pkg.integrity?.sha256||"unavailable").slice(0,12))}…</div>`;
  for(const msg of validation.errors){const el=document.createElement("div");el.className="qaIssue bad";el.innerHTML=`<b>ERROR</b>${escapeHtml(msg)}`;wrap.appendChild(el)}
  for(const msg of validation.warnings){const el=document.createElement("div");el.className="qaIssue warn";el.innerHTML=`<b>WARN</b>${escapeHtml(msg)}`;wrap.appendChild(el)}
}
async function previewPocketRuntimePackageV190(){
  try{const pkg=await buildPocketRuntimePackageV190({requireQa:false});renderPocketRuntimeExportV190(pkg)}catch(error){pocketRuntimeExportStateV190.error=error;renderPocketRuntimeExportV190(null,error);toast("Pocket runtime validation blocked")}
}
function downloadPocketRuntimePackageV190(pkg){
  const safe=String(pkg.manifest.id).replace(/[^a-z0-9._-]+/gi,"-");
  const blob=new Blob([JSON.stringify(pkg,null,2)],{type:"application/json;charset=utf-8"}),url=URL.createObjectURL(blob),a=document.createElement("a");
  a.href=url;a.download=`${safe}.pocket-character.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
async function exportPocketRuntimePackageV190(){
  try{const pkg=await buildPocketRuntimePackageV190({requireQa:true});downloadPocketRuntimePackageV190(pkg);toast(`Exported ${pkg.manifest.id} for Pocket Monster`)}catch(error){pocketRuntimeExportStateV190.error=error;renderPocketRuntimeExportV190(null,error);toast("Pocket runtime export blocked")}
}

'''+anchor
    rep(anchor, funcs, 'pocket runtime package functions')

    bind = '$("#btnPreviewRecoveryChain").onclick=()=>previewCoreTransitionSequenceV1810(["idle","dodge_r","hit_react","knockback","get_up","idle"],"Recovery QA");'
    bindings = bind + r'''
$("#btnPreviewPocketRuntime").onclick=previewPocketRuntimePackageV190;
$("#btnExportPocketRuntime").onclick=exportPocketRuntimePackageV190;'''
    rep(bind, bindings, 'pocket runtime export bindings')

    html = html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.10"', 'localStorage.setItem("characterPrototypeStudio.v1.9.0"', 1)
    html = html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10")||',
                        'const raw=localStorage.getItem("characterPrototypeStudio.v1.9.0")||localStorage.getItem("characterPrototypeStudio.v1.8.10")||', 1)
    html = html.replace('// Generated by Character Prototype Studio V1.8.10', '// Generated by Character Prototype Studio V1.9.0')
    return html


if __name__ == '__main__':
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
