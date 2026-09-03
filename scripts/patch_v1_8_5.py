from pathlib import Path


def patch(html):
    def rep(old, new, label, count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError("missing anchor: " + label)
        html = html.replace(old, new, count)

    html = html.replace("Character Prototype Studio V1.8.4.1", "Character Prototype Studio V1.8.5")
    html = html.replace(
        "V1.8.4.1 · Twist Activation Hotfix / Action Template Runtime Fix",
        "V1.8.5 · Dynamics Auto-Tuner / Inspector-Guided Modifier Preview",
    )
    html = html.replace('generatorVersion:"1.8.4.1"', 'generatorVersion:"1.8.5"')

    ui_anchor = '''        <div class="weightBox">\n          <h3>BALANCE QUALITY</h3>'''
    ui = '''        <div class="dynInspectorBox" id="dynamicsAutoTunerBox">\n          <h3>DYNAMICS AUTO-TUNER <span class="posebadge" id="autoTunerStatus">READY</span></h3>\n          <div class="hint">V1.8.5 ปรับเฉพาะ Body Dynamics modifier parameters จากผล Inspector — ไม่แก้ authored keyframes.</div>\n          <div class="row" style="margin-top:7px">\n            <label class="grow" style="font-size:9px;color:var(--muted)">Mode\n              <select id="autoTunerMode">\n                <option value="conservative">Conservative</option>\n                <option value="natural" selected>Natural</option>\n                <option value="strong">Strong Fix</option>\n              </select>\n            </label>\n            <button class="btn good grow" id="btnAnalyzeAutoTune">Analyze &amp; Propose</button>\n          </div>\n          <div class="qaKpi">\n            <div><b id="autoTunerChangeCount">0</b><small>CHANGES</small></div>\n            <div><b id="autoTunerPredHard">—</b><small>PRED HARD</small></div>\n            <div><b id="autoTunerPredWarn">—</b><small>PRED WARN</small></div>\n            <div><b id="autoTunerKeyframes">LOCKED</b><small>KEYFRAMES</small></div>\n          </div>\n          <div class="qaIssues" id="autoTunerProposal">\n            <div class="qaIssue good">Run Inspector แล้วกด Analyze &amp; Propose</div>\n          </div>\n          <div class="row" style="margin-top:7px">\n            <button class="btn good grow" id="btnPreviewAutoTune" disabled>Preview Proposed Fix</button>\n            <button class="btn grow" id="btnApplyAutoTune" disabled>Apply</button>\n            <button class="btn grow" id="btnCancelAutoTune" disabled>Cancel Preview</button>\n          </div>\n        </div>\n\n''' + ui_anchor
    rep(ui_anchor, ui, "auto tuner UI")

    fn_anchor = "function syncBodyDynamicsUI(){"
    funcs = r'''const AUTO_TUNER_MODIFIERS=["intensity","pelvisShare","chestShare","shoulderShare","armShare","pelvisLead","chestLag","shoulderLag","armLag","counterRotation","followThrough","forwardLeanShare","sideLeanShare","headStability"];
const AUTO_TUNER_LIMITS={
  intensity:[0,1.5],pelvisShare:[0,1.5],chestShare:[0,1.5],shoulderShare:[0,1.8],armShare:[0,2],
  pelvisLead:[0,.2],chestLag:[0,.25],shoulderLag:[0,.3],armLag:[0,.35],counterRotation:[0,.8],followThrough:[0,1.5],
  forwardLeanShare:[0,1.2],sideLeanShare:[0,1.2],headStability:[0,1]
};
let dynamicsAutoTunerState={proposal:null,preview:null};
function autoTunerModeFactor(mode){return mode==="conservative"?.55:mode==="strong"?1.4:1}
function autoTunerRound(v){return Math.round(v*1000)/1000}
function autoTunerClamp(key,v){const r=AUTO_TUNER_LIMITS[key]||[-Infinity,Infinity];return autoTunerRound(clamp(v,r[0],r[1]))}
function autoTunerSet(target,key,value,reason,reasons){
  if(!AUTO_TUNER_MODIFIERS.includes(key))return;
  const next=autoTunerClamp(key,value),prev=target[key];
  if(Math.abs(next-prev)<.0005)return;
  target[key]=next;
  (reasons[key]||(reasons[key]=[])).push(reason);
}
function autoTunerAdjust(target,key,delta,reason,reasons){autoTunerSet(target,key,(target[key]||0)+delta,reason,reasons)}
function autoTunerParamForMetric(k){return k==="pelvis"?"pelvisShare":k==="chest"?"chestShare":k==="shoulder"?"shoulderShare":k==="arm"?"armShare":null}
function buildDynamicsAutoTuneProposal(clip,result,mode){
  normalizeClip(clip);
  const f=autoTunerModeFactor(mode),base=structuredClone(clip.bodyDynamics),target=structuredClone(base),reasons={};
  const m=result?.metrics||{},p=m.peaks||{},issues=result?.issues||[];
  const gap=Math.max(.012,clip.duration/Math.max(90,result?.samples||90)*1.2);
  if(p.pelvis&&p.chest&&p.chest.time<p.pelvis.time+gap)autoTunerAdjust(target,"chestLag",.018*f,"Chest peak needs to follow pelvis",reasons);
  if(p.chest&&p.shoulder&&p.shoulder.time<p.chest.time+gap)autoTunerAdjust(target,"shoulderLag",.020*f,"Shoulder peak needs to follow chest",reasons);
  if(p.shoulder&&p.arm&&p.arm.time<p.shoulder.time+gap)autoTunerAdjust(target,"armLag",.024*f,"Arm peak needs to follow shoulder",reasons);
  if(p.pelvis&&p.arm&&p.arm.time-p.pelvis.time>.22){
    autoTunerAdjust(target,"armLag",-.025*f,"Pelvis-to-arm lag is disconnected",reasons);
    autoTunerAdjust(target,"shoulderLag",-.012*f,"Compress excessive chain delay",reasons);
  }
  for(const issue of issues){
    const code=issue.code||"",msg=String(issue.message||"");
    if(code==="HEAD_STABILIZATION")autoTunerAdjust(target,"headStability",.08*f,"Inspector: head follows torso too much",reasons);
    if(code==="RECOVERY_RESIDUAL")autoTunerAdjust(target,"followThrough",-.10*f,"Inspector: recovery retains too much follow-through",reasons);
    if(code==="COM_SUPPORT_CONFLICT"||code==="BODY_NO_SUPPORT"||code==="KICK_SUPPORT_FOOT"){
      autoTunerAdjust(target,"intensity",-.055*f,"Inspector: reduce body drive during support conflict",reasons);
      autoTunerAdjust(target,"forwardLeanShare",-.045*f,"Inspector: reduce forward COM pressure",reasons);
      autoTunerAdjust(target,"sideLeanShare",-.035*f,"Inspector: reduce lateral COM pressure",reasons);
    }
    if(code==="THRUST_CHAIN_ROTATION"){
      autoTunerAdjust(target,"pelvisShare",-.07*f,"Thrust should favor forward drive over twist",reasons);
      autoTunerAdjust(target,"chestShare",-.09*f,"Thrust torso rotation is high",reasons);
      autoTunerAdjust(target,"shoulderShare",-.06*f,"Thrust shoulder rotation is high",reasons);
    }
    if(code==="DODGE_INSUFFICIENT_SHIFT"){
      autoTunerAdjust(target,"intensity",.07*f,"Dodge needs clearer lateral displacement",reasons);
      autoTunerAdjust(target,"sideLeanShare",.06*f,"Dodge needs clearer side read",reasons);
    }
    if(code==="ANGULAR_VELOCITY"||code==="ANGULAR_ACCELERATION"||code==="NATURAL_RANGE_PRESSURE"){
      const k=["pelvis","chest","shoulder","arm"].find(x=>msg.toLowerCase().startsWith(x)||msg.toLowerCase().includes(x+" "));
      const param=autoTunerParamForMetric(k);
      if(param)autoTunerAdjust(target,param,-.045*f,`Inspector: ${k} drive is too aggressive`,reasons);
      else autoTunerAdjust(target,"intensity",-.035*f,"Inspector: global action drive is too aggressive",reasons);
    }
    if(code==="ABRUPT_REVERSAL"){
      autoTunerAdjust(target,"followThrough",-.045*f,"Reduce abrupt reversal pressure",reasons);
      autoTunerAdjust(target,"counterRotation",-.025*f,"Reduce counter-rotation reversal",reasons);
    }
  }
  if((m.headRatio||0)>.42)autoTunerAdjust(target,"headStability",.04*f,"Metrics: improve head stabilization margin",reasons);
  const changes=AUTO_TUNER_MODIFIERS.filter(k=>Math.abs((target[k]??0)-(base[k]??0))>.0005).map(k=>({key:k,from:base[k],to:target[k],delta:autoTunerRound(target[k]-base[k]),reasons:reasons[k]||[]}));
  return {version:"1.8.5",mode,clipId:clip.id,sourceFingerprint:actionDynamicsFingerprint(clip),base,target,changes,sourceResult:{hard:result?.hard||0,warn:result?.warn||0},createdAt:new Date().toISOString()};
}
function evaluateDynamicsAutoTuneProposal(clip,proposal){
  if(!clip||!proposal)return null;
  const saved=structuredClone(clip.bodyDynamics),savedQA=structuredClone(actionDynamicsQAState.last);
  try{
    Object.assign(clip.bodyDynamics,proposal.target,{qa:null});
    const cfg=actionInspectorConfig(),m=actionDynamicsMetrics(clip,cfg),issues=buildActionDynamicsIssues(clip,m,cfg);
    return {hard:issues.filter(i=>i.severity==="hard").length,warn:issues.filter(i=>i.severity==="warn").length,issues};
  }finally{
    clip.bodyDynamics=saved;actionDynamicsQAState.last=savedQA;
  }
}
function renderDynamicsAutoTuner(){
  const p=dynamicsAutoTunerState.proposal,preview=dynamicsAutoTunerState.preview,status=$("#autoTunerStatus");
  if(status){status.textContent=preview?"PREVIEW":p?"PROPOSED":"READY";status.className="posebadge "+(p?"good":"")}
  if($("#autoTunerChangeCount"))$("#autoTunerChangeCount").textContent=p?.changes?.length||0;
  if($("#autoTunerPredHard"))$("#autoTunerPredHard").textContent=p?.prediction?.hard??"—";
  if($("#autoTunerPredWarn"))$("#autoTunerPredWarn").textContent=p?.prediction?.warn??"—";
  const wrap=$("#autoTunerProposal");if(wrap){wrap.innerHTML="";
    if(!p)wrap.innerHTML='<div class="qaIssue good">Run Inspector แล้วกด Analyze &amp; Propose</div>';
    else if(!p.changes.length)wrap.innerHTML='<div class="qaIssue good"><b>NO CHANGE NEEDED</b>Inspector ไม่พบ modifier adjustment ที่ Auto-Tuner ควรแก้</div>';
    else for(const c of p.changes){const el=document.createElement("div");el.className="qaIssue";el.innerHTML=`<b>${escapeHtml(c.key)} ${c.delta>=0?"+":""}${c.delta.toFixed(3)}</b>${Number(c.from).toFixed(3)} → ${Number(c.to).toFixed(3)} · ${escapeHtml(c.reasons[0]||"Inspector-guided adjustment")}`;wrap.appendChild(el)}
  }
  if($("#btnPreviewAutoTune"))$("#btnPreviewAutoTune").disabled=!p?.changes?.length||!!preview;
  if($("#btnApplyAutoTune"))$("#btnApplyAutoTune").disabled=!p?.changes?.length;
  if($("#btnCancelAutoTune"))$("#btnCancelAutoTune").disabled=!preview;
}
function analyzeAndProposeDynamicsAutoTune(){
  cancelDynamicsAutoTunePreview(false);
  const clip=selectedAnimationClip();if(!clip?.keyframes?.length){toast("ไม่มี authored action clip");return}
  normalizeClip(clip);if(!clip.bodyDynamics?.enabled||clip.runtime.motionClass!=="action"){toast("Auto-Tuner ใช้กับ action clip ที่เปิด Body Dynamics");return}
  let result=actionDynamicsResultForClip(clip);if(!result||result.stale)result=runActionDynamicsInspector();if(!result)return;
  const mode=$("#autoTunerMode")?.value||"natural",proposal=buildDynamicsAutoTuneProposal(clip,result,mode);
  proposal.prediction=evaluateDynamicsAutoTuneProposal(clip,proposal);
  dynamicsAutoTunerState.proposal=proposal;renderDynamicsAutoTuner();
  toast(proposal.changes.length?`Auto-Tuner proposed ${proposal.changes.length} modifier changes`:"Auto-Tuner: no modifier changes needed");
}
function previewDynamicsAutoTune(){
  const clip=selectedAnimationClip(),p=dynamicsAutoTunerState.proposal;if(!clip||!p||p.clipId!==clip.id||!p.changes.length)return;
  if(dynamicsAutoTunerState.preview)cancelDynamicsAutoTunePreview(false);
  const keyframesBefore=JSON.stringify(clip.keyframes);
  dynamicsAutoTunerState.preview={clipId:clip.id,bodyDynamics:structuredClone(clip.bodyDynamics),keyframes:keyframesBefore};
  Object.assign(clip.bodyDynamics,p.target,{qa:null});actionDynamicsQAState.last=null;
  syncBodyDynamicsUI();renderActionDynamicsInspector();renderDynamicsAutoTuner();
  animationState.time=0;if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);startAnimationPlayback();
  toast("Preview only · keyframes locked · Apply เพื่อบันทึก");
}
function cancelDynamicsAutoTunePreview(showToast=true){
  const prev=dynamicsAutoTunerState.preview;if(!prev)return;
  const clip=(spec.animations||[]).find(c=>c.id===prev.clipId);
  if(clip){clip.bodyDynamics=structuredClone(prev.bodyDynamics);actionDynamicsQAState.last=null;syncBodyDynamicsUI();renderActionDynamicsInspector()}
  dynamicsAutoTunerState.preview=null;renderDynamicsAutoTuner();if(showToast)toast("Auto-Tuner preview cancelled");
}
function applyDynamicsAutoTune(){
  const clip=selectedAnimationClip(),p=dynamicsAutoTunerState.proposal;if(!clip||!p||p.clipId!==clip.id||!p.changes.length)return;
  const authoredBefore=JSON.stringify(clip.keyframes);
  if(dynamicsAutoTunerState.preview)cancelDynamicsAutoTunePreview(false);
  withCommand("Dynamics Auto-Tuner V1.8.5",()=>{
    for(const c of p.changes)clip.bodyDynamics[c.key]=c.to;
    clip.bodyDynamics.qa=null;
  });
  if(JSON.stringify(clip.keyframes)!==authoredBefore)throw new Error("Auto-Tuner invariant failed: authored keyframes changed");
  dynamicsAutoTunerState.proposal=null;actionDynamicsQAState.last=null;syncBodyDynamicsUI();
  const rerun=runActionDynamicsInspector();renderDynamicsAutoTuner();autoSave();
  toast(rerun?`Auto-Tuner applied · Inspector ${rerun.hard?"BLOCKED":"PASS"} (${rerun.warn} warn)`:"Auto-Tuner applied · rerun Inspector");
}
'''
    rep(fn_anchor, funcs + fn_anchor, "auto tuner functions")

    bind_anchor = '$("#btnExportActionInspector").onclick=exportActionDynamicsInspector;'
    bind = bind_anchor + r'''
$("#btnAnalyzeAutoTune").onclick=analyzeAndProposeDynamicsAutoTune;
$("#btnPreviewAutoTune").onclick=previewDynamicsAutoTune;
$("#btnApplyAutoTune").onclick=applyDynamicsAutoTune;
$("#btnCancelAutoTune").onclick=()=>cancelDynamicsAutoTunePreview(true);
$("#autoTunerMode").onchange=()=>{if(dynamicsAutoTunerState.proposal)analyzeAndProposeDynamicsAutoTune()};'''
    rep(bind_anchor, bind, "auto tuner bindings")

    init_anchor = "syncBodyDynamicsUI();renderBodyDynamicsStatus();renderActionDynamicsInspector();syncSkinUI();"
    rep(
        init_anchor,
        "syncBodyDynamicsUI();renderBodyDynamicsStatus();renderActionDynamicsInspector();renderDynamicsAutoTuner();syncSkinUI();",
        "auto tuner init",
    )

    switch_anchor = "animationState.selectedClipId=e.target.value;animationState.time=0;animationQAState.last=null;actionDynamicsQAState.last=null;buildAnimationUI();renderAnimationQA();renderActionDynamicsInspector();"
    switch_new = "cancelDynamicsAutoTunePreview(false);dynamicsAutoTunerState.proposal=null;animationState.selectedClipId=e.target.value;animationState.time=0;animationQAState.last=null;actionDynamicsQAState.last=null;buildAnimationUI();renderAnimationQA();renderActionDynamicsInspector();renderDynamicsAutoTuner();"
    rep(switch_anchor, switch_new, "clip switch tuner reset")

    html = html.replace('version:"1.8.4",clipId:clip.id', 'version:"1.8.5",clipId:clip.id', 1)
    html = html.replace('studio:"Character Prototype Studio V1.8.4.1"', 'studio:"Character Prototype Studio V1.8.5"', 1)
    html = html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.4.1"', 'localStorage.setItem("characterPrototypeStudio.v1.8.5"', 1)
    html = html.replace(
        'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.4.1")||',
        'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.5")||localStorage.getItem("characterPrototypeStudio.v1.8.4.1")||',
        1,
    )
    return html
