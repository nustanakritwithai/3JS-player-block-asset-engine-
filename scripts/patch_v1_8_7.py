#!/usr/bin/env python3
from pathlib import Path

def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)

    html=html.replace('Character Prototype Studio V1.8.6','Character Prototype Studio V1.8.7')
    html=html.replace('V1.8.6 · Natural Locomotion Dynamics','V1.8.7 · Foot Plant + Leg Response')
    html=html.replace('generatorVersion:"1.8.6"','generatorVersion:"1.8.7"')

    # Motion Lab status + tuning controls.
    anchor='''        <div class="solverBox" id="locomotionDynamicsBox" style="margin-top:8px">\n          <h3>NATURAL LOCOMOTION DYNAMICS <span class="pill good">V1.8.6</span></h3>\n          <div class="responseKpi">\n            <div><b id="locoModeValue">IDLE</b><small>MODE</small></div>\n            <div><b id="locoPelvisYaw">0.0°</b><small>PELVIS YAW</small></div>\n            <div><b id="locoChestYaw">0.0°</b><small>CHEST COUNTER</small></div>\n            <div><b id="locoLeanValue">0.0°</b><small>LEAN</small></div>\n          </div>\n          <div class="hint" id="locoDetail">Weight/COM owns balance · Locomotion Dynamics owns gait core yaw/lean · Action Body Dynamics remains action-only.</div>\n        </div>'''
    repl=anchor+'''\n        <div class="solverBox" id="footPlantLegResponseBox" style="margin-top:8px">\n          <h3>FOOT PLANT + LEG RESPONSE <span class="pill good">V1.8.7</span></h3>\n          <div class="responseKpi">\n            <div><b id="plantStanceValue">AIR</b><small>STANCE</small></div>\n            <div><b id="plantErrorValue">0.000m</b><small>LOCK ERROR</small></div>\n            <div><b id="plantKneeValue">0.0°</b><small>SUPPORT KNEE</small></div>\n            <div><b id="plantAnkleValue">0.0°</b><small>ANKLE FLATTEN</small></div>\n          </div>\n          <div class="clipmeta" style="margin-top:7px">\n            <label>Plant strength<input id="plantStrength" type="number" min="0" max="1" step=".05" value=".92"></label>\n            <label>Root micro-comp<input id="plantRootComp" type="number" min="0" max="1" step=".05" value=".45"></label>\n            <label>Support knee °<input id="plantKneeDeg" type="number" min="0" max="24" step="1" value="7"></label>\n            <label>Swing toe lift °<input id="plantToeLiftDeg" type="number" min="0" max="30" step="1" value="12"></label>\n          </div>\n          <div class="hint" id="plantDetail">Contact anchor owns only foot lock + distal leg response. Weight/COM keeps pelvis balance ownership; V1.8.6 keeps locomotion core yaw.</div>\n        </div>'''
    rep(anchor,repl,'foot plant motion panel')

    # Contact tools authored-animation controls/status.
    anchor='''          <div class="row" style="margin-top:6px">\n            <button class="btn good grow" id="btnFootLockAssist">Foot Lock Assist</button>\n            <button class="btn grow" id="btnClearContactTags">Clear Tags</button>\n          </div>'''
    repl=anchor+'''\n          <div class="switch"><span>Runtime Foot Plant + Leg Response</span><input id="authoredFootPlantToggle" type="checkbox" checked></div>\n          <div class="hint" style="margin-top:5px">V1.8.7 runtime plant uses contact tags during Play. V0.7 Foot Lock Assist remains an optional offline keyframe tool.</div>'''
    rep(anchor,repl,'authored foot plant toggle')

    # Default spec contract.
    rep('''  locomotionDynamics:{enabled:true,intensity:1,direction:"R",version:"1.8.6"},\n  weight:{''','''  locomotionDynamics:{enabled:true,intensity:1,direction:"R",version:"1.8.6"},\n  footPlantLegResponse:{\n    enabled:true,plantStrength:.92,rootCompensation:.45,maxRootCorrection:.028,\n    supportKneeDeg:7,landingCompressionDeg:5,supportHipPitchDeg:2.0,\n    ankleFlatten:.82,ankleRollFlatten:.70,swingToeLiftDeg:12,releaseRate:6.5,\n    version:"1.8.7"\n  },\n  weight:{''','default foot plant spec')

    # Runtime state extends procedural motion state with landing pulse.
    rep('''let motionState = {\n  playing:false, phase:0, basePose:null, baseRoot:null, maxSlide:0,\n  contact:{L:false,R:false}, lockPos:{L:null,R:null}, slide:{L:0,R:0}\n};\nlet locomotionDynamicsState={last:null};''','''let motionState = {\n  playing:false, phase:0, basePose:null, baseRoot:null, maxSlide:0,\n  contact:{L:false,R:false}, lockPos:{L:null,R:null}, slide:{L:0,R:0},\n  landing:{L:0,R:0}\n};\nlet locomotionDynamicsState={last:null};\nlet footPlantLegResponseState={last:null};\nlet authoredFootPlantState={clipId:null,lastTime:0,active:{L:false,R:false},anchors:{L:null,R:null},landing:{L:0,R:0},maxError:0};''','foot plant runtime state')

    # Clip contract.
    rep('''    locomotionDynamics:{enabled:true,mode:"auto",direction:"R",intensity:1,bakedAt:null,version:"1.8.6"},\n    bodyDynamics:{''','''    locomotionDynamics:{enabled:true,mode:"auto",direction:"R",intensity:1,bakedAt:null,version:"1.8.6"},\n    footPlant:{enabled:true,strength:1,bakedAt:null,version:"1.8.7"},\n    bodyDynamics:{''','clip foot plant contract')

    # Normalize clip contract before contact settings.
    anchor='''  clip.contactSettings={\n    groundTolerance:clamp(Number(clip.contactSettings?.groundTolerance)||.08,.005,.5),'''
    new='''  {\n    const f=clip.footPlant||{};\n    clip.footPlant={\n      enabled:f.enabled!==false,\n      strength:clamp(Number.isFinite(Number(f.strength))?Number(f.strength):1,0,1.5),\n      bakedAt:f.bakedAt||null,\n      version:"1.8.7"\n    };\n    if(clip.runtime?.motionClass==="action"&&!clip.keyframes?.some(k=>k.meta?.contact?.L||k.meta?.contact?.R))clip.footPlant.enabled=false;\n  }\n'''+anchor
    rep(anchor,new,'normalize foot plant clip')

    # Reset procedural state on stop/start.
    rep('''  motionState.contact={L:false,R:false};motionState.lockPos={L:null,R:null};motionState.slide={L:0,R:0};''','''  motionState.contact={L:false,R:false};motionState.lockPos={L:null,R:null};motionState.slide={L:0,R:0};motionState.landing={L:0,R:0};\n  footPlantLegResponseState.last=null;renderFootPlantLegResponseStatus();''','stop motion foot plant reset')
    rep('''  motionState.phase=0;motionState.maxSlide=0;motionState.lockPos={L:null,R:null};motionState.slide={L:0,R:0};''','''  motionState.phase=0;motionState.maxSlide=0;motionState.lockPos={L:null,R:null};motionState.slide={L:0,R:0};motionState.landing={L:0,R:0};\n  footPlantLegResponseState.last=null;''','start motion foot plant reset')

    # Insert solver functions before updateMotion.
    anchor='''function updateMotion(dt){'''
    solver=r'''function ensureFootPlantLegResponseSpec(){
  const d={enabled:true,plantStrength:.92,rootCompensation:.45,maxRootCorrection:.028,supportKneeDeg:7,landingCompressionDeg:5,supportHipPitchDeg:2,ankleFlatten:.82,ankleRollFlatten:.70,swingToeLiftDeg:12,releaseRate:6.5,version:"1.8.7"};
  spec.footPlantLegResponse={...d,...(spec.footPlantLegResponse||{})};
  const f=spec.footPlantLegResponse;
  f.enabled=f.enabled!==false;f.plantStrength=clamp(Number(f.plantStrength),0,1);f.rootCompensation=clamp(Number(f.rootCompensation),0,1);f.maxRootCorrection=clamp(Number(f.maxRootCorrection),0,.08);
  f.supportKneeDeg=clamp(Number(f.supportKneeDeg),0,24);f.landingCompressionDeg=clamp(Number(f.landingCompressionDeg),0,18);f.supportHipPitchDeg=clamp(Number(f.supportHipPitchDeg),0,12);
  f.ankleFlatten=clamp(Number(f.ankleFlatten),0,1);f.ankleRollFlatten=clamp(Number(f.ankleRollFlatten),0,1);f.swingToeLiftDeg=clamp(Number(f.swingToeLiftDeg),0,30);f.releaseRate=clamp(Number(f.releaseRate),1,20);f.version="1.8.7";
  return f;
}
function resetAuthoredFootPlantState(clip=null,time=0){
  authoredFootPlantState={clipId:clip?.id||null,lastTime:time,active:{L:false,R:false},anchors:{L:null,R:null},landing:{L:0,R:0},maxError:0};
  footPlantLegResponseState.last=null;
}
function footPlantStanceLabel(active){return active.L&&active.R?"BOTH":active.L?"LEFT":active.R?"RIGHT":"AIR"}
function footPlantWorldFeet(){
  scene.updateMatrixWorld(true);
  const out={};
  for(const side of ["L","R"]){const s=sockets["foot."+side];if(!s)continue;const v=new THREE.Vector3();s.getWorldPosition(v);out[side]=v}
  return out;
}
function applySupportLegResponse(side,load,landing,swing,f){
  const hip=joints["hip"+side],knee=joints["knee"+side],ankle=joints["ankle"+side];if(!hip||!knee||!ankle)return {knee:0,ankle:0};
  let kneeAdd=0,ankleFix=0;
  if(load>0){
    kneeAdd=rad((f.supportKneeDeg*load)+(f.landingCompressionDeg*landing));
    knee.rotation.x+=kneeAdd;
    hip.rotation.x-=rad(f.supportHipPitchDeg*load);
    const sagittal=hip.rotation.x+knee.rotation.x+ankle.rotation.x;
    const lateral=hip.rotation.z+knee.rotation.z+ankle.rotation.z;
    const ax=-sagittal*f.ankleFlatten,az=-lateral*f.ankleRollFlatten;
    ankle.rotation.x+=ax;ankle.rotation.z+=az;ankleFix=Math.hypot(ax,az);
  }else if(swing>0){
    const toe=rad(f.swingToeLiftDeg*swing);ankle.rotation.x-=toe;ankleFix=toe;
  }
  hip.rotation.x=clamp(hip.rotation.x,rad(-108),rad(74));
  knee.rotation.x=clamp(knee.rotation.x,rad(0),rad(142));
  ankle.rotation.x=clamp(ankle.rotation.x,rad(-42),rad(42));
  ankle.rotation.z=clamp(ankle.rotation.z,rad(-22),rad(22));
  return {knee:kneeAdd,ankle:ankleFix};
}
function rootMicroCompensateFromAnchors(active,anchors,f,strength=1){
  if(!f.enabled||f.rootCompensation<=0||!characterRoot)return {error:0,correction:0};
  scene.updateMatrixWorld(true);const feet=footPlantWorldFeet(),errors=[];
  for(const side of ["L","R"]){if(active[side]&&anchors[side]&&feet[side])errors.push({x:feet[side].x-anchors[side].x,z:feet[side].z-anchors[side].z})}
  if(!errors.length)return {error:0,correction:0};
  const avg=errors.reduce((a,e)=>({x:a.x+e.x,z:a.z+e.z}),{x:0,z:0});avg.x/=errors.length;avg.z/=errors.length;
  const err=Math.hypot(avg.x,avg.z),gain=f.rootCompensation*f.plantStrength*strength;
  let dx=-avg.x*gain,dz=-avg.z*gain;const mag=Math.hypot(dx,dz),max=f.maxRootCorrection;
  if(mag>max&&mag>0){dx*=max/mag;dz*=max/mag}
  characterRoot.position.x+=dx;characterRoot.position.z+=dz;scene.updateMatrixWorld(true);
  return {error:err,correction:Math.hypot(dx,dz)};
}
function proceduralSwingAmount(side){
  const s=Math.sin(motionState.phase);return side==="L"?Math.max(0,s):Math.max(0,-s);
}
function applyProceduralFootPlantLegResponse(dt){
  const f=ensureFootPlantLegResponseSpec();if(!f.enabled)return null;
  const active={L:!!motionState.contact.L,R:!!motionState.contact.R};
  const load=active.L&&active.R?{L:.5,R:.5}:active.L?{L:1,R:0}:active.R?{L:0,R:1}:{L:0,R:0};
  let knee=0,ankle=0;
  for(const side of ["L","R"]){
    motionState.landing[side]=Math.max(0,(motionState.landing[side]||0)-dt*f.releaseRate);
    const r=applySupportLegResponse(side,load[side],motionState.landing[side],active[side]?0:proceduralSwingAmount(side),f);knee=Math.max(knee,Math.abs(r.knee));ankle=Math.max(ankle,Math.abs(r.ankle));
  }
  const lock=rootMicroCompensateFromAnchors(active,motionState.lockPos,f,1);
  const r={stance:footPlantStanceLabel(active),error:lock.error,correction:lock.correction,knee,ankle,active};footPlantLegResponseState.last=r;renderFootPlantLegResponseStatus(r);return r;
}
function applyAuthoredFootPlantLegResponse(clip,time,dt=0){
  const f=ensureFootPlantLegResponseSpec();normalizeClip(clip);
  if(!f.enabled||clip.footPlant?.enabled===false||clip.footPlant?.bakedAt)return null;
  if(authoredFootPlantState.clipId!==clip.id||time+1e-5<authoredFootPlantState.lastTime)resetAuthoredFootPlantState(clip,time);
  const state=contactStateAtTime(clip,time),feet=footPlantWorldFeet(),active={L:!!state.L,R:!!state.R};
  for(const side of ["L","R"]){
    if(active[side]&&!authoredFootPlantState.active[side]){authoredFootPlantState.anchors[side]=feet[side]?.clone()||null;authoredFootPlantState.landing[side]=1}
    if(!active[side])authoredFootPlantState.anchors[side]=null;
    authoredFootPlantState.active[side]=active[side];
  }
  const w=weightTransferAtTime(clip,time),strength=clip.footPlant?.strength??1;let knee=0,ankle=0;
  for(const side of ["L","R"]){
    authoredFootPlantState.landing[side]=Math.max(0,(authoredFootPlantState.landing[side]||0)-Math.max(0,dt)*f.releaseRate);
    const load=active[side]?clamp(side==="L"?w.L:w.R,.15,1):0;
    const swing=active[side]?0:(side==="L"?w.R:w.L)*.65;
    const r=applySupportLegResponse(side,load,authoredFootPlantState.landing[side],swing,f);knee=Math.max(knee,Math.abs(r.knee));ankle=Math.max(ankle,Math.abs(r.ankle));
  }
  const lock=rootMicroCompensateFromAnchors(active,authoredFootPlantState.anchors,f,strength);authoredFootPlantState.maxError=Math.max(authoredFootPlantState.maxError,lock.error);authoredFootPlantState.lastTime=time;
  const r={stance:footPlantStanceLabel(active),error:lock.error,correction:lock.correction,knee,ankle,active};footPlantLegResponseState.last=r;renderFootPlantLegResponseStatus(r);return r;
}
function renderFootPlantLegResponseStatus(r=footPlantLegResponseState.last){
  if(!$("#plantStanceValue"))return;const f=ensureFootPlantLegResponseSpec();
  $("#plantStanceValue").textContent=r?.stance||"AIR";$("#plantErrorValue").textContent=(r?.error||0).toFixed(3)+"m";$("#plantKneeValue").textContent=deg(r?.knee||0).toFixed(1)+"°";$("#plantAnkleValue").textContent=deg(r?.ankle||0).toFixed(1)+"°";
  if($("#plantStrength"))$("#plantStrength").value=f.plantStrength;if($("#plantRootComp"))$("#plantRootComp").value=f.rootCompensation;if($("#plantKneeDeg"))$("#plantKneeDeg").value=f.supportKneeDeg;if($("#plantToeLiftDeg"))$("#plantToeLiftDeg").value=f.swingToeLiftDeg;
}
function updateFootPlantSettingsFromUI(){
  withCommand("Foot Plant settings",()=>{const f=ensureFootPlantLegResponseSpec();f.plantStrength=clamp(Number($("#plantStrength")?.value),0,1);f.rootCompensation=clamp(Number($("#plantRootComp")?.value),0,1);f.supportKneeDeg=clamp(Number($("#plantKneeDeg")?.value),0,24);f.swingToeLiftDeg=clamp(Number($("#plantToeLiftDeg")?.value),0,30)});renderFootPlantLegResponseStatus();
}
'''+anchor
    rep(anchor,solver,'foot plant solver functions')

    # Procedural update: two contact passes, plant between them.
    rep('''  updateFootContacts();\n}\nfunction updateFootContacts(){''','''  updateFootContacts(false,false);\n  applyProceduralFootPlantLegResponse(dt);\n  updateFootContacts(true,true);\n}\nfunction updateFootContacts(render=true,recordSlide=true){''','procedural plant order')
    rep('''  processContact("L",stanceL,pL);processContact("R",stanceR,pR);\n  updateContactUI();\n}\nfunction processContact(side,isContact,pos){''','''  processContact("L",stanceL,pL,recordSlide);processContact("R",stanceR,pR,recordSlide);\n  if(render)updateContactUI();\n}\nfunction processContact(side,isContact,pos,recordSlide=true){''','contact two-pass signature')
    rep('''  if(isContact&&!prev)motionState.lockPos[side]=new THREE.Vector3(pos.x,0,pos.z);''','''  if(isContact&&!prev){motionState.lockPos[side]=new THREE.Vector3(pos.x,0,pos.z);motionState.landing[side]=1}''','landing pulse capture')
    rep('''    motionState.maxSlide=Math.max(motionState.maxSlide,slide);''','''    if(recordSlide)motionState.maxSlide=Math.max(motionState.maxSlide,slide);''','post-plant slide metric')

    # Animation playback integration/reset.
    rep('''  if(!animationState.basePose)captureAnimationBase();\n  animationState.playing=!animationState.playing;''','''  if(!animationState.basePose)captureAnimationBase();\n  if(!animationState.playing)resetAuthoredFootPlantState(clip,animationState.time);\n  animationState.playing=!animationState.playing;''','animation plant start')
    rep('''  animationState.playing=false;animationState.time=0;animationState.basePose=null;animationState.baseRoot=null;''','''  animationState.playing=false;animationState.time=0;animationState.basePose=null;animationState.baseRoot=null;resetAuthoredFootPlantState();''','animation plant stop')
    rep('''  if(apply){\n    if(!animationState.basePose)captureAnimationBase();\n    restoreAnimationBase();\n    applyAnimationAtTime(clip,animationState.time);\n    applyCompleteWeightMotionRuntime(clip,animationState.time);applyEquipmentResponseRuntime(clip,animationState.time);\n  }''','''  if(apply){\n    if(!animationState.basePose)captureAnimationBase();\n    resetAuthoredFootPlantState(clip,animationState.time);\n    restoreAnimationBase();\n    applyAnimationAtTime(clip,animationState.time);\n    applyCompleteWeightMotionRuntime(clip,animationState.time);applyEquipmentResponseRuntime(clip,animationState.time);\n    applyAuthoredFootPlantLegResponse(clip,animationState.time,0);\n  }''','animation seek plant')
    rep('''  if(animationState.time>clip.duration){\n    if(clip.loop)animationState.time=animationState.time%clip.duration;''','''  if(animationState.time>clip.duration){\n    if(clip.loop){animationState.time=animationState.time%clip.duration;resetAuthoredFootPlantState(clip,animationState.time)}''','animation loop plant reset')
    html=html.replace('''resetAuthoredFootPlantState(clip,animationState.time)}\n    else{animationState.time=clip.duration;''','''resetAuthoredFootPlantState(clip,animationState.time)}\n    else{animationState.time=clip.duration;''',1)
    rep('''  applyAnimationAtTime(clip,animationState.time);\n  applyCompleteWeightMotionRuntime(clip,animationState.time);applyEquipmentResponseRuntime(clip,animationState.time);\n  updateAnimationTimelineUI(false);''','''  applyAnimationAtTime(clip,animationState.time);\n  applyCompleteWeightMotionRuntime(clip,animationState.time);applyEquipmentResponseRuntime(clip,animationState.time);\n  applyAuthoredFootPlantLegResponse(clip,animationState.time,dt);\n  updateAnimationTimelineUI(false);''','animation playback plant')

    # Runtime preview state + integration.
    rep('''  eventCursor:0,\n  selectedEventId:null,''','''  eventCursor:0,\n  footPlant:{clipId:null,lastTime:0,active:{L:false,R:false},anchors:{L:null,R:null},landing:{L:0,R:0},maxError:0},\n  selectedEventId:null,''','game runtime foot plant state')
    rep('''    gameRuntimeState.current=clip;gameRuntimeState.target=null;gameRuntimeState.time=0;gameRuntimeState.blending=false;gameRuntimeState.eventCursor=0;''','''    gameRuntimeState.current=clip;gameRuntimeState.target=null;gameRuntimeState.time=0;gameRuntimeState.blending=false;gameRuntimeState.eventCursor=0;resetAuthoredFootPlantState(clip,0);''','game runtime play reset')
    rep('''  gameRuntimeState.basePose=null;gameRuntimeState.time=0;gameRuntimeState.targetTime=0;\n  resetMomentumState();''','''  gameRuntimeState.basePose=null;gameRuntimeState.time=0;gameRuntimeState.targetTime=0;\n  resetAuthoredFootPlantState();resetMomentumState();''','game runtime stop reset')
    rep('''  applyMomentumResponseRuntime();\n  if(!gameRuntimeState.current?.runtime?.equipmentBakedAt)applyEquipmentResponseRuntime(gameRuntimeState.current,gameRuntimeState.time);\n  renderRuntimeUI();''','''  applyMomentumResponseRuntime();\n  if(!gameRuntimeState.current?.runtime?.equipmentBakedAt)applyEquipmentResponseRuntime(gameRuntimeState.current,gameRuntimeState.time);\n  applyAuthoredFootPlantLegResponse(gameRuntimeState.current,gameRuntimeState.time,dt);\n  renderRuntimeUI();''','game runtime foot plant apply')

    # UI init/bindings.
    rep('''  renderLocomotionStatus();\n  $("#contactToggle").checked=spec.motionPreview.showContacts!==false;''','''  renderLocomotionStatus();renderFootPlantLegResponseStatus();\n  $("#contactToggle").checked=spec.motionPreview.showContacts!==false;''','build foot plant UI')
    bind_anchor='''$("#motionDirection").onchange=e=>withCommand("Locomotion direction",()=>{spec.motionPreview.direction=e.target.value;ensureLocomotionDynamicsSpec().direction=e.target.value;renderLocomotionStatus()});'''
    bind_new=bind_anchor+'''\nfor(const id of ["plantStrength","plantRootComp","plantKneeDeg","plantToeLiftDeg"])$("#"+id).onchange=updateFootPlantSettingsFromUI;'''
    rep(bind_anchor,bind_new,'foot plant UI bindings')
    rep('''  $("#authoredWeightState").textContent=state.weight.toUpperCase();''','''  $("#authoredWeightState").textContent=state.weight.toUpperCase();\n  if($("#authoredFootPlantToggle"))$("#authoredFootPlantToggle").checked=clip.footPlant?.enabled!==false;''','authored foot plant UI state')
    bind='''$("#btnFootLockAssist").onclick=footLockAssist;'''
    bindnew=bind+'''\n$("#authoredFootPlantToggle").onchange=e=>{const clip=selectedAnimationClip();if(!clip)return;withCommand("Runtime Foot Plant",()=>{normalizeClip(clip);clip.footPlant.enabled=e.target.checked});resetAuthoredFootPlantState(clip,animationState.time);renderFootPlantLegResponseStatus()};'''
    rep(bind,bindnew,'authored foot plant toggle binding')

    # Runtime manifest + standalone runtime contract.
    rep('''      locomotionDynamics:structuredClone(c.locomotionDynamics||{}),\n      keyframeCount:c.keyframes.length''','''      locomotionDynamics:structuredClone(c.locomotionDynamics||{}),\n      footPlant:structuredClone(c.footPlant||{}),\n      contactSettings:structuredClone(c.contactSettings||{}),\n      keyframes:structuredClone(c.keyframes||[]),\n      keyframeCount:c.keyframes.length''','runtime manifest foot plant state')
    rep('''    weight:structuredClone(spec.weight||{}),\n    equipment:structuredClone(spec.weight?.equipment||{}),''','''    weight:structuredClone(spec.weight||{}),\n    footPlantLegResponse:structuredClone(ensureFootPlantLegResponseSpec()),\n    equipment:structuredClone(spec.weight?.equipment||{}),''','runtime manifest foot plant config')
    rep('''  c.locomotionDynamics=c.locomotionDynamics||{enabled:true,mode:"auto",direction:"R",intensity:1,bakedAt:null,version:"1.8.6"};\n  return c;''','''  c.locomotionDynamics=c.locomotionDynamics||{enabled:true,mode:"auto",direction:"R",intensity:1,bakedAt:null,version:"1.8.6"};\n  c.footPlant=c.footPlant||{enabled:true,strength:1,bakedAt:null,version:"1.8.7"};\n  c.contactSettings=c.contactSettings||{groundTolerance:.08,slideLimit:.12,lockStrength:1,samples:60};\n  c.keyframes=Array.isArray(c.keyframes)?c.keyframes:[];\n  return c;''','standalone normalize foot plant')

    # Standalone runtime solver before class.
    runtime_anchor='''export class CharacterAnimationRuntime {'''
    runtime_solver=r'''function runtimeContactStateAtTime(clip,time){
  if(!clip?.keyframes?.length)return {L:false,R:false};let key=clip.keyframes[0],t=clamp(time,0,clip.duration);for(const k of clip.keyframes){if(k.time<=t+.00001)key=k;else break}return {L:!!key.meta?.contact?.L,R:!!key.meta?.contact?.R};
}
function runtimeWeightAtTime(clip,time){
  if(!clip?.keyframes?.length)return {L:.5,R:.5};let key=clip.keyframes[0],t=clamp(time,0,clip.duration);for(const k of clip.keyframes){if(k.time<=t+.00001)key=k;else break}const v=key.meta?.weightValue;if(v&&Number.isFinite(+v.L)&&Number.isFinite(+v.R)){const s=+v.L + +v.R;return s>0?{L:+v.L/s,R:+v.R/s}:{L:.5,R:.5}}return key.meta?.contact?.L&&!key.meta?.contact?.R?{L:.92,R:.08}:key.meta?.contact?.R&&!key.meta?.contact?.L?{L:.08,R:.92}:{L:.5,R:.5};
}
function runtimeFootWorld(socket,root){if(!socket?.getWorldPosition)return null;const v=root.position.clone();socket.getWorldPosition(v);return v}
function resetRuntimeFootPlantState(clip=null,time=0){return {clipId:clip?.id||null,lastTime:time,active:{L:false,R:false},anchors:{L:null,R:null},landing:{L:0,R:0},maxError:0}}
function applyRuntimeFootPlantLegResponse(root,joints,sockets,clip,time,dt,state,cfg){
  if(!root||!clip||cfg?.enabled===false||clip.footPlant?.enabled===false||clip.footPlant?.bakedAt)return state;normalizeClip(clip);
  if(!state||state.clipId!==clip.id||time+1e-5<state.lastTime)state=resetRuntimeFootPlantState(clip,time);
  root.updateMatrixWorld?.(true);const contact=runtimeContactStateAtTime(clip,time),active={L:contact.L,R:contact.R},feet={L:runtimeFootWorld(sockets?.["foot.L"],root),R:runtimeFootWorld(sockets?.["foot.R"],root)};
  for(const side of ["L","R"]){if(active[side]&&!state.active[side]){state.anchors[side]=feet[side]?.clone?.()||null;state.landing[side]=1}if(!active[side])state.anchors[side]=null;state.active[side]=active[side]}
  const f={plantStrength:.92,rootCompensation:.45,maxRootCorrection:.028,supportKneeDeg:7,landingCompressionDeg:5,supportHipPitchDeg:2,ankleFlatten:.82,ankleRollFlatten:.70,swingToeLiftDeg:12,releaseRate:6.5,...(cfg||{})},w=runtimeWeightAtTime(clip,time);
  for(const side of ["L","R"]){state.landing[side]=Math.max(0,(state.landing[side]||0)-Math.max(0,dt)*(f.releaseRate||6.5));const hip=joints["hip"+side],knee=joints["knee"+side],ankle=joints["ankle"+side];if(!hip||!knee||!ankle)continue;const load=active[side]?clamp(side==="L"?w.L:w.R,.15,1):0;if(load>0){knee.rotation.x+=((f.supportKneeDeg*load+f.landingCompressionDeg*state.landing[side])*Math.PI/180);hip.rotation.x-=(f.supportHipPitchDeg*load*Math.PI/180);ankle.rotation.x-= (hip.rotation.x+knee.rotation.x+ankle.rotation.x)*(f.ankleFlatten??.82);ankle.rotation.z-= (hip.rotation.z+knee.rotation.z+ankle.rotation.z)*(f.ankleRollFlatten??.70)}else{const swing=(side==="L"?w.R:w.L)*.65;ankle.rotation.x-=(f.swingToeLiftDeg*swing*Math.PI/180)}hip.rotation.x=clamp(hip.rotation.x,-108*Math.PI/180,74*Math.PI/180);knee.rotation.x=clamp(knee.rotation.x,0,142*Math.PI/180);ankle.rotation.x=clamp(ankle.rotation.x,-42*Math.PI/180,42*Math.PI/180);ankle.rotation.z=clamp(ankle.rotation.z,-22*Math.PI/180,22*Math.PI/180)}
  root.updateMatrixWorld?.(true);const errors=[];for(const side of ["L","R"]){if(active[side]&&state.anchors[side]){const p=runtimeFootWorld(sockets?.["foot."+side],root);if(p)errors.push({x:p.x-state.anchors[side].x,z:p.z-state.anchors[side].z})}}
  if(errors.length&&f.rootCompensation>0){const a=errors.reduce((o,e)=>({x:o.x+e.x,z:o.z+e.z}),{x:0,z:0});a.x/=errors.length;a.z/=errors.length;const err=Math.hypot(a.x,a.z),gain=f.rootCompensation*(f.plantStrength??.92)*(clip.footPlant?.strength??1);let dx=-a.x*gain,dz=-a.z*gain,mag=Math.hypot(dx,dz),max=f.maxRootCorrection??.018;if(mag>max&&mag>0){dx*=max/mag;dz*=max/mag}root.position.x+=dx;root.position.z+=dz;state.maxError=Math.max(state.maxError,err)}
  state.lastTime=time;return state;
}

'''+runtime_anchor
    rep(runtime_anchor,runtime_solver,'standalone foot plant solver')

    # Runtime class config/state and apply order.
    rep('''    this.weight=options.weight||ANIMATION_RUNTIME_MANIFEST.weight||{};\n    this.momentumConfig={...(ANIMATION_RUNTIME_MANIFEST.momentum||{}),...(options.momentum||{})};''','''    this.weight=options.weight||ANIMATION_RUNTIME_MANIFEST.weight||{};\n    this.footPlantConfig={...(ANIMATION_RUNTIME_MANIFEST.footPlantLegResponse||{}),...(options.footPlantLegResponse||{})};\n    this.footPlant=resetRuntimeFootPlantState();\n    this.momentumConfig={...(ANIMATION_RUNTIME_MANIFEST.momentum||{}),...(options.momentum||{})};''','runtime class foot plant config')
    rep('''    this.current=clip;this.target=null;this.time=opts.startTime??0;this.playing=true;this.blending=false;''','''    this.current=clip;this.target=null;this.time=opts.startTime??0;this.playing=true;this.blending=false;this.footPlant=resetRuntimeFootPlantState(clip,this.time);''','runtime play foot plant reset')
    rep('''  stop(){this.playing=false;this.current=null;this.target=null;this.blending=false;return this}''','''  stop(){this.playing=false;this.current=null;this.target=null;this.blending=false;this.footPlant=resetRuntimeFootPlantState();return this}''','runtime stop foot plant reset')
    rep('''    applyRuntimeMomentumSolver(this.joints,this.momentum);\n    applyRuntimeEquipmentResponse(this.joints,this.current,this.weight);''','''    applyRuntimeMomentumSolver(this.joints,this.momentum);\n    applyRuntimeEquipmentResponse(this.joints,this.current,this.weight);\n    this.footPlant=applyRuntimeFootPlantLegResponse(this.root,this.joints,this.sockets,this.current,this.time,dt,this.footPlant,this.footPlantConfig);''','runtime foot plant final apply')

    # Migrate/init/save version.
    rep('''ensureRuntimeSettings();ensureWeightSpec();ensureSkinSystem();migrateNaturalWalkTuning();migrateWalkPelvisTranslationHotfix();ensureLocomotionDynamicsSpec();''','''ensureRuntimeSettings();ensureWeightSpec();ensureSkinSystem();migrateNaturalWalkTuning();migrateWalkPelvisTranslationHotfix();ensureLocomotionDynamicsSpec();ensureFootPlantLegResponseSpec();''','foot plant spec init')
    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.6"','localStorage.setItem("characterPrototypeStudio.v1.8.7"',1)
    html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.6")||','const raw=localStorage.getItem("characterPrototypeStudio.v1.8.7")||localStorage.getItem("characterPrototypeStudio.v1.8.6")||',1)
    html=html.replace('// Generated by Character Prototype Studio V1.8.6','// Generated by Character Prototype Studio V1.8.7')
    return html

if __name__=='__main__':
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
