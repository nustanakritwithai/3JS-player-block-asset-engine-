#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    def rep(old, new, label, count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: ' + label)
        html = html.replace(old, new, count)

    html = html.replace('Character Prototype Studio V1.8.9', 'Character Prototype Studio V1.8.10')
    html = html.replace('V1.8.9 · Core Action / Reaction Pack', 'V1.8.10 · Core Animation QA / Transitions')
    html = html.replace('generatorVersion:"1.8.9"', 'generatorVersion:"1.8.10"')

    hint = 'Core Animation Pack · Movement + Dodge L/R + Hit + Knockback + Get Up + Death/Faint + Interact · Weapon ยังไม่เริ่ม'
    qa_ui = hint + '''\n          <div class="chainbox" id="coreAnimationQaBox" style="margin-top:8px">\n            <h3>CORE ANIMATION QA / TRANSITIONS <span class="posebadge" id="coreAnimationQaStatus">READY</span></h3>\n            <div class="hint">V1.8.10 ตรวจ state transition, contact seam, recovery และ terminal state โดยไม่แก้ authored keyframes</div>\n            <div class="qaKpi" style="margin-top:7px">\n              <div><b id="coreQaHard">0</b><small>HARD</small></div>\n              <div><b id="coreQaWarn">0</b><small>WARN</small></div>\n              <div><b id="coreQaPass">0</b><small>PASS</small></div>\n              <div><b id="coreQaContracts">0</b><small>CONTRACTS</small></div>\n            </div>\n            <div class="row" style="margin-top:7px">\n              <button class="btn good grow" id="btnRunCoreAnimationQa">Run Core QA</button>\n              <button class="btn grow" id="btnStampCoreTransitions">Stamp Contracts</button>\n            </div>\n            <div class="row" style="margin-top:7px">\n              <button class="btn grow" id="btnPreviewMovementChain">Preview Movement</button>\n              <button class="btn grow" id="btnPreviewAirChain">Preview Air Chain</button>\n              <button class="btn grow" id="btnPreviewRecoveryChain">Preview Recovery</button>\n            </div>\n            <div class="qaIssues" id="coreAnimationQaIssues" style="margin-top:7px">\n              <div class="qaIssue good">พร้อมตรวจ Core Animation Pack</div>\n            </div>\n          </div>'''
    rep(hint, qa_ui, 'core animation qa panel')

    anchor = 'function createAttackTemplate(){'
    funcs = r'''const CORE_ANIMATION_TRANSITIONS_V1_8_10=Object.freeze({
  idle:["walk","run","sprint","jump","crouch_idle","dodge_l","dodge_r","hit_react","knockback","interact","death","faint"],
  walk:["idle","run","sprint","stop","turn","strafe","jump","crouch_walk","dodge_l","dodge_r","hit_react","knockback","interact","death","faint"],
  run:["idle","walk","sprint","stop","turn","strafe","jump","dodge_l","dodge_r","hit_react","knockback","death","faint"],
  sprint:["run","walk","stop","jump","dodge_l","dodge_r","hit_react","knockback","death","faint"],
  start:["walk","run","sprint","stop"],stop:["idle","walk","run"],turn:["idle","walk","run"],strafe:["idle","walk","run"],
  jump:["fall","land"],fall:["land"],land:["idle","walk","run","crouch_idle"],
  crouch_idle:["idle","crouch_walk","dodge_l","dodge_r","hit_react","interact","death","faint"],
  crouch_walk:["crouch_idle","idle","dodge_l","dodge_r","hit_react","death","faint"],
  dodge_l:["idle","walk","run"],dodge_r:["idle","walk","run"],
  hit_react:["idle","walk","run","knockback","death","faint"],knockback:["idle","get_up","death","faint"],
  get_up:["idle","crouch_idle"],interact:["idle"],death:[],faint:["get_up","idle"]
});
const CORE_ANIMATION_TERMINAL_V1_8_10=new Set(["death"]);
const CORE_ANIMATION_RECOVERY_V1_8_10=new Set(["dodge_l","dodge_r","hit_react","knockback","get_up","interact","land"]);
let coreAnimationQaState={last:null,previewToken:0,timers:[]};
function coreAnimationStateV1810(clip){
  const explicit=String(clip?.runtime?.state||"").toLowerCase();
  if(explicit){
    if(explicit==="dodge_l"||explicit==="dodge_r")return explicit;
    if(CORE_ANIMATION_TRANSITIONS_V1_8_10[explicit])return explicit;
  }
  const n=String(clip?.name||"").toLowerCase();
  if(n.includes("dodge_l"))return "dodge_l";if(n.includes("dodge_r"))return "dodge_r";
  if(n.includes("hit_react"))return "hit_react";if(n.includes("knockback"))return "knockback";if(n.includes("get_up"))return "get_up";
  if(n.includes("death"))return "death";if(n.includes("faint"))return "faint";if(n.includes("interact"))return "interact";
  if(n.includes("crouch_walk"))return "crouch_walk";if(n.includes("crouch_idle"))return "crouch_idle";
  if(n.includes("fall"))return "fall";if(n.includes("land"))return "land";if(n.includes("jump"))return "jump";
  if(n.includes("sprint"))return "sprint";if(n.includes("strafe"))return "strafe";if(n.includes("turn"))return "turn";
  if(n.includes("start"))return "start";if(n.includes("stop"))return "stop";if(n.includes("run"))return "run";if(n.includes("walk"))return "walk";if(n.includes("idle"))return "idle";
  return null;
}
function coreTransitionBlendV1810(state){
  if(state==="jump"||state==="fall")return {in:.06,out:.08};
  if(state==="land")return {in:.06,out:.12};
  if(state.startsWith("dodge_"))return {in:.055,out:.11};
  if(state==="hit_react")return {in:.035,out:.10};
  if(state==="knockback")return {in:.025,out:.14};
  if(state==="get_up")return {in:.08,out:.14};
  if(state==="death"||state==="faint")return {in:.05,out:0};
  if(state==="interact")return {in:.08,out:.12};
  if(state==="walk"||state==="run"||state==="sprint"||state==="turn"||state==="strafe")return {in:.12,out:.12};
  return {in:.10,out:.10};
}
function stampCoreTransitionContractV1810(clip){
  const state=coreAnimationStateV1810(clip);if(!state)return false;
  normalizeClip(clip);const blend=coreTransitionBlendV1810(state),allowed=CORE_ANIMATION_TRANSITIONS_V1_8_10[state]||[];
  clip.runtime.transition={schema:"core-transition-v1",studioVersion:"1.8.10",state,allowedNext:[...allowed],blendIn:blend.in,blendOut:blend.out,interruptible:!CORE_ANIMATION_TERMINAL_V1_8_10.has(state),terminal:CORE_ANIMATION_TERMINAL_V1_8_10.has(state)};
  return true;
}
function upgradeExistingCoreTransitionsV1810(){
  let changed=0;for(const clip of spec.animations||[]){const before=JSON.stringify(clip.runtime?.transition||null);if(stampCoreTransitionContractV1810(clip)&&JSON.stringify(clip.runtime.transition)!==before)changed++}return changed;
}
function coreContactV1810(k){const c=k?.meta?.contact;return c&&typeof c.L==="boolean"&&typeof c.R==="boolean"?{L:c.L,R:c.R}:null}
function sameContactV1810(a,b){return !!a&&!!b&&a.L===b.L&&a.R===b.R}
function supportedV1810(c){return !!c&&(c.L||c.R)}
function runCoreAnimationQaV1810(){
  const clips=(spec.animations||[]).filter(c=>coreAnimationStateV1810(c));const issues=[];let pass=0,contracts=0;
  const add=(severity,clip,code,message)=>issues.push({severity,clip:clip?.name||"Core Pack",code,message});
  if(!clips.length)add("warn",null,"NO_CORE_CLIPS","ยังไม่มี Core Animation clip ใน library — สร้าง template ก่อนตรวจ");
  for(const clip of clips){
    normalizeClip(clip);const state=coreAnimationStateV1810(clip),keys=clip.keyframes||[],tr=clip.runtime?.transition;
    if(!keys.length){add("hard",clip,"NO_KEYS","ไม่มี authored keyframes");continue}
    let ordered=true;for(let i=1;i<keys.length;i++)if(keys[i].time+1e-6<keys[i-1].time)ordered=false;
    if(!ordered)add("hard",clip,"KEY_ORDER","keyframe time ไม่เรียงจากน้อยไปมาก");else pass++;
    if(Math.abs((keys[0]?.time||0))>.001)add("warn",clip,"START_TIME","clip ควรเริ่มที่ time 0");else pass++;
    if(Math.abs((keys.at(-1)?.time||0)-clip.duration)>.012)add("warn",clip,"END_TIME","keyframe สุดท้ายไม่ตรง duration");else pass++;
    const contacts=keys.map(coreContactV1810),missing=contacts.filter(c=>!c).length;
    if(missing)add("warn",clip,"CONTACT_META",`${missing} keyframe ไม่มี contact metadata ที่อ่านได้`);else pass++;
    const first=contacts[0],last=contacts.at(-1);
    if(clip.loop&&first&&last&&!sameContactV1810(first,last))add("hard",clip,"LOOP_SEAM","loop seam เปลี่ยน contact ข้ามขอบ clip");else if(clip.loop)pass++;
    if((state==="jump"||state==="fall")&&!contacts.some(c=>c&&!c.L&&!c.R))add("hard",clip,"AIR_CONTACT",`${state} ต้องมีช่วง airborne contact=false/false`);else if(state==="jump"||state==="fall")pass++;
    if(state==="land"&&last&&!supportedV1810(last))add("hard",clip,"LAND_SUPPORT","Land ต้องจบด้วย ground support");else if(state==="land")pass++;
    if(CORE_ANIMATION_RECOVERY_V1_8_10.has(state)&&last&&!supportedV1810(last))add("hard",clip,"RECOVERY_SUPPORT",`${state} ต้องคืน support ก่อนจบ transition`);else if(CORE_ANIMATION_RECOVERY_V1_8_10.has(state))pass++;
    if(tr?.schema==="core-transition-v1"&&tr?.studioVersion==="1.8.10"&&tr.state===state){contracts++;pass++}else add("warn",clip,"TRANSITION_CONTRACT","ยังไม่ได้ stamp V1.8.10 transition contract");
    if(tr?.allowedNext?.some(next=>!(next in CORE_ANIMATION_TRANSITIONS_V1_8_10)))add("hard",clip,"UNKNOWN_NEXT","transition contract อ้าง state ที่ไม่รู้จัก");
    if(state==="death"&&tr?.allowedNext?.length)add("hard",clip,"TERMINAL_EXIT","Death เป็น terminal state และต้องไม่มี allowedNext");
  }
  const hard=issues.filter(i=>i.severity==="hard").length,warn=issues.filter(i=>i.severity==="warn").length;
  coreAnimationQaState.last={version:"1.8.10",hard,warn,pass,contracts,total:clips.length,issues,checkedAt:new Date().toISOString()};
  renderCoreAnimationQaV1810();toast(hard?`Core Animation QA BLOCKED · ${hard} hard / ${warn} warn`:`Core Animation QA PASS · ${warn} warn`);return coreAnimationQaState.last;
}
function renderCoreAnimationQaV1810(){
  const r=coreAnimationQaState.last,status=$("#coreAnimationQaStatus"),wrap=$("#coreAnimationQaIssues");
  if($("#coreQaHard"))$("#coreQaHard").textContent=r?.hard??0;if($("#coreQaWarn"))$("#coreQaWarn").textContent=r?.warn??0;if($("#coreQaPass"))$("#coreQaPass").textContent=r?.pass??0;if($("#coreQaContracts"))$("#coreQaContracts").textContent=r?.contracts??0;
  if(status){status.textContent=!r?"READY":r.hard?"BLOCKED":r.warn?"PASS+WARN":"PASS";status.className="posebadge "+(r&&!r.hard?"good":"")}
  if(!wrap)return;wrap.innerHTML="";
  if(!r){wrap.innerHTML='<div class="qaIssue good">พร้อมตรวจ Core Animation Pack</div>';return}
  if(!r.issues.length){wrap.innerHTML='<div class="qaIssue good"><b>PASS</b> Transition contract, contact seam และ recovery ผ่านทั้งหมด</div>';return}
  for(const i of r.issues){const el=document.createElement("div");el.className="qaIssue "+(i.severity==="hard"?"bad":i.severity==="warn"?"warn":"good");el.innerHTML=`<b>${escapeHtml(i.code)} · ${escapeHtml(i.clip)}</b>${escapeHtml(i.message)}`;wrap.appendChild(el)}
}
function stampAllCoreTransitionsV1810(){
  let changed=0;withCommand("V1.8.10 Transition Contracts",()=>{for(const clip of spec.animations||[]){const before=JSON.stringify(clip.runtime?.transition||null);if(stampCoreTransitionContractV1810(clip)&&JSON.stringify(clip.runtime.transition)!==before)changed++}});
  autoSave();runCoreAnimationQaV1810();toast(`V1.8.10 stamped ${changed} transition contract${changed===1?"":"s"}`);
}
function stopCoreTransitionPreviewV1810(){
  coreAnimationQaState.previewToken++;for(const t of coreAnimationQaState.timers)clearTimeout(t);coreAnimationQaState.timers=[];
  if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);
}
function previewCoreTransitionSequenceV1810(states,label){
  stopCoreTransitionPreviewV1810();const token=coreAnimationQaState.previewToken,clips=[];
  for(const state of states){const clip=(spec.animations||[]).find(c=>coreAnimationStateV1810(c)===state);if(!clip){toast(`${label}: missing ${state} clip`);return}stampCoreTransitionContractV1810(clip);clips.push(clip)}
  let delay=0;clips.forEach((clip,index)=>{const timer=setTimeout(()=>{if(token!==coreAnimationQaState.previewToken)return;if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);animationState.selectedClipId=clip.id;animationState.time=0;startAnimationPlayback();toast(`${label} · ${coreAnimationStateV1810(clip)} ${index+1}/${clips.length}`)},Math.round(delay*1000));coreAnimationQaState.timers.push(timer);delay+=Math.max(.18,clip.duration-(clip.runtime?.transition?.blendOut||.1))});
  coreAnimationQaState.timers.push(setTimeout(()=>{if(token!==coreAnimationQaState.previewToken)return;if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);runCoreAnimationQaV1810()},Math.round((delay+.12)*1000)));
}
const addTemplateClipV1810Base=addTemplateClip;
addTemplateClip=function(clip){stampCoreTransitionContractV1810(clip);return addTemplateClipV1810Base(clip)};
'''+anchor
    rep(anchor, funcs, 'core transition contract and qa functions')

    bind = '$("#btnTemplateAttack").onclick=createAttackTemplate;'
    bindings = bind + r'''
$("#btnRunCoreAnimationQa").onclick=runCoreAnimationQaV1810;
$("#btnStampCoreTransitions").onclick=stampAllCoreTransitionsV1810;
$("#btnPreviewMovementChain").onclick=()=>previewCoreTransitionSequenceV1810(["idle","walk","run","walk","idle"],"Movement QA");
$("#btnPreviewAirChain").onclick=()=>previewCoreTransitionSequenceV1810(["idle","jump","fall","land","idle"],"Air QA");
$("#btnPreviewRecoveryChain").onclick=()=>previewCoreTransitionSequenceV1810(["idle","dodge_r","hit_react","knockback","get_up","idle"],"Recovery QA");'''
    rep(bind, bindings, 'core qa bindings')

    rep('loadLocal();const purgedLegacyTwistDemos=purgeLegacyTwistDemoClips();',
        'loadLocal();const upgradedCoreTransitionsV1810=upgradeExistingCoreTransitionsV1810();const purgedLegacyTwistDemos=purgeLegacyTwistDemoClips();',
        'upgrade saved transition contracts')
    html = html.replace('if(purgedLegacyTwistDemos)autoSave();', 'if(purgedLegacyTwistDemos||upgradedCoreTransitionsV1810)autoSave();', 1)

    html = html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.9"', 'localStorage.setItem("characterPrototypeStudio.v1.8.10"', 1)
    html = html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.9")||',
                        'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10")||localStorage.getItem("characterPrototypeStudio.v1.8.9")||', 1)
    html = html.replace('// Generated by Character Prototype Studio V1.8.9', '// Generated by Character Prototype Studio V1.8.10')
    return html


if __name__ == '__main__':
    import sys
    p = Path(sys.argv[1])
    p.write_text(patch(p.read_text(encoding='utf-8')), encoding='utf-8')
