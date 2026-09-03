#!/usr/bin/env python3
from pathlib import Path

def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)

    html=html.replace('Character Prototype Studio V1.8.5.3','Character Prototype Studio V1.8.6')
    html=html.replace('V1.8.5.3 · Walk Pelvis Translation Hotfix','V1.8.6 · Natural Locomotion Dynamics')
    html=html.replace('generatorVersion:"1.8.5.3"','generatorVersion:"1.8.6"')

    rep('''          <select id="motionClip" class="grow">\n            <option value="idle">Idle Motion</option>\n            <option value="walk">Walk</option>\n            <option value="run">Run</option>\n          </select>\n          <button class="btn good" id="btnMotionPlay">▶ Play</button>''','''          <select id="motionClip" class="grow">\n            <option value="idle">Idle Motion</option>\n            <option value="walk">Walk</option>\n            <option value="run">Run</option>\n            <option value="sprint">Sprint</option>\n            <option value="start">Start / Accelerate</option>\n            <option value="stop">Stop / Brake</option>\n            <option value="turn">Turn Step</option>\n            <option value="strafe">Strafe</option>\n          </select>\n          <select id="motionDirection" title="Turn / Strafe direction">\n            <option value="R">Right</option>\n            <option value="L">Left</option>\n          </select>\n          <button class="btn good" id="btnMotionPlay">▶ Play</button>''','procedural locomotion mode selector')

    rep('''        <div id="motionControls" class="stack" style="margin-top:9px"></div>\n        <div class="row" style="margin-top:7px">''','''        <div id="motionControls" class="stack" style="margin-top:9px"></div>\n        <div class="solverBox" id="locomotionDynamicsBox" style="margin-top:8px">\n          <h3>NATURAL LOCOMOTION DYNAMICS <span class="pill good">V1.8.6</span></h3>\n          <div class="responseKpi">\n            <div><b id="locoModeValue">IDLE</b><small>MODE</small></div>\n            <div><b id="locoPelvisYaw">0.0°</b><small>PELVIS YAW</small></div>\n            <div><b id="locoChestYaw">0.0°</b><small>CHEST COUNTER</small></div>\n            <div><b id="locoLeanValue">0.0°</b><small>LEAN</small></div>\n          </div>\n          <div class="hint" id="locoDetail">Weight/COM owns balance · Locomotion Dynamics owns gait core yaw/lean · Action Body Dynamics remains action-only.</div>\n        </div>\n        <div class="row" style="margin-top:7px">''','locomotion status panel')

    rep('''            <button class="btn" id="btnTemplateWalk">Walk 4-Phase</button>\n            <button class="btn" id="btnTemplateRun">Run 4-Phase</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>\n            <button class="btn" id="btnTemplateIdle">Idle Breathing</button>''','''            <button class="btn" id="btnTemplateWalk">Walk 4-Phase</button>\n            <button class="btn" id="btnTemplateRun">Run 4-Phase</button>\n            <button class="btn" id="btnTemplateSprint">Sprint</button>\n            <button class="btn" id="btnTemplateStart">Start</button>\n            <button class="btn" id="btnTemplateStop">Stop</button>\n            <button class="btn" id="btnTemplateTurn">Turn R</button>\n            <button class="btn" id="btnTemplateStrafe">Strafe R</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>\n            <button class="btn" id="btnTemplateIdle">Idle Breathing</button>''','animation locomotion library')
    html=html.replace('Library อยู่บนสุดของ Anim tab และ Twist Demo จะไม่เพิ่ม/ลบ clip ใน library นี้อีก','Library อยู่บนสุดของ Anim tab · V1.8.6 เพิ่ม Sprint / Start / Stop / Turn / Strafe โดยไม่เปลี่ยน Action Library',1)

    rep('''    compression:.020,headStabilization:true,showContacts:true,\n    tuningVersion:"1.8.5.3"\n  },\n  weight:{''','''    compression:.020,headStabilization:true,showContacts:true,direction:"R",\n    tuningVersion:"1.8.6"\n  },\n  locomotionDynamics:{enabled:true,intensity:1,direction:"R",version:"1.8.6"},\n  weight:{''','default locomotion spec')

    rep('''let motionState = {\n  playing:false, phase:0, basePose:null, baseRoot:null, maxSlide:0,\n  contact:{L:false,R:false}, lockPos:{L:null,R:null}, slide:{L:0,R:0}\n};''','''let motionState = {\n  playing:false, phase:0, basePose:null, baseRoot:null, maxSlide:0,\n  contact:{L:false,R:false}, lockPos:{L:null,R:null}, slide:{L:0,R:0}\n};\nlet locomotionDynamicsState={last:null};''','locomotion runtime state')

    rep('''    bodyDynamics:{\n      enabled:true,preset:"natural",actionType:"auto",intensity:.82,''','''    locomotionDynamics:{enabled:true,mode:"auto",direction:"R",intensity:1,bakedAt:null,version:"1.8.6"},\n    bodyDynamics:{\n      enabled:true,preset:"natural",actionType:"auto",intensity:.82,''','clip locomotion contract')

    anchor='''  clip.weightTransfer={\n    curve:["smooth","linear","step"].includes(clip.weightTransfer?.curve)?clip.weightTransfer.curve:"smooth",'''
    loco_norm=r'''  {
    const l=clip.locomotionDynamics||{},state=String(clip.runtime?.state||clip.name||"").toLowerCase();
    const inferred=/sprint/.test(state)?"sprint":/start|accelerat/.test(state)?"start":/stop|brake/.test(state)?"stop":/turn/.test(state)?"turn":/strafe|sidestep/.test(state)?"strafe":clip.runtime?.motionClass==="run"?"run":clip.runtime?.motionClass==="walk"?"walk":"none";
    clip.locomotionDynamics={
      enabled:l.enabled!==false,
      mode:["auto","walk","run","sprint","start","stop","turn","strafe","none"].includes(l.mode)?l.mode:"auto",
      direction:["L","R"].includes(l.direction)?l.direction:"R",
      intensity:clamp(Number.isFinite(Number(l.intensity))?Number(l.intensity):1,0,1.5),
      bakedAt:l.bakedAt||null,
      version:"1.8.6"
    };
    if(clip.locomotionDynamics.mode==="auto"&&inferred==="none"&&clip.runtime?.motionClass==="action")clip.locomotionDynamics.enabled=false;
  }
'''+anchor
    rep(anchor,loco_norm,'normalize locomotion contract')

    start=html.index('function updateMotion(dt){')
    end=html.index('function updateFootContacts(){',start)
    new=r'''const LOCOMOTION_PROFILES={
  walk:{cadence:1.00,hip:1.00,knee:1.00,arm:1.00,ankle:9,elbow:20,pelvisYaw:3.5,chestYaw:5.8,shoulderYaw:1.6,forwardLean:1.8,sideLean:.6,bob:.038,compression:.018,lateral:.014,pelvisLead:.08,chestLag:.08,shoulderLag:.13,headStability:.86},
  run:{cadence:1.48,hip:1.30,knee:1.38,arm:1.38,ankle:14,elbow:46,pelvisYaw:4.2,chestYaw:7.4,shoulderYaw:2.4,forwardLean:7.5,sideLean:.9,bob:.054,compression:.024,lateral:.009,pelvisLead:.10,chestLag:.10,shoulderLag:.18,headStability:.82},
  sprint:{cadence:1.88,hip:1.58,knee:1.68,arm:1.62,ankle:18,elbow:62,pelvisYaw:3.8,chestYaw:8.8,shoulderYaw:3.0,forwardLean:14,sideLean:.8,bob:.070,compression:.030,lateral:.006,pelvisLead:.12,chestLag:.12,shoulderLag:.22,headStability:.76},
  start:{cadence:.90,hip:1.22,knee:1.35,arm:1.30,ankle:13,elbow:44,pelvisYaw:4.0,chestYaw:7.0,shoulderYaw:2.5,forwardLean:12,sideLean:.7,bob:.046,compression:.032,lateral:.008,pelvisLead:.10,chestLag:.10,shoulderLag:.18,headStability:.80},
  stop:{cadence:.78,hip:1.08,knee:1.15,arm:1.05,ankle:11,elbow:38,pelvisYaw:3.2,chestYaw:5.6,shoulderYaw:2.0,forwardLean:7,sideLean:.8,bob:.040,compression:.036,lateral:.008,pelvisLead:.07,chestLag:.10,shoulderLag:.16,headStability:.86},
  turn:{cadence:.92,hip:.92,knee:.90,arm:.92,ankle:10,elbow:28,pelvisYaw:7.5,chestYaw:4.8,shoulderYaw:2.1,forwardLean:2.8,sideLean:4.5,bob:.034,compression:.020,lateral:.010,pelvisLead:.06,chestLag:.11,shoulderLag:.16,headStability:.88,turnRoot:34},
  strafe:{cadence:1.05,hip:.78,knee:.92,arm:.84,ankle:10,elbow:30,pelvisYaw:1.8,chestYaw:3.4,shoulderYaw:1.8,forwardLean:2.0,sideLean:5.2,bob:.032,compression:.020,lateral:.034,pelvisLead:.05,chestLag:.10,shoulderLag:.15,headStability:.90}
};
function ensureLocomotionDynamicsSpec(){
  spec.locomotionDynamics={...{enabled:true,intensity:1,direction:"R",version:"1.8.6"},...(spec.locomotionDynamics||{})};
  spec.locomotionDynamics.enabled=spec.locomotionDynamics.enabled!==false;
  spec.locomotionDynamics.intensity=clamp(Number(spec.locomotionDynamics.intensity)||1,0,1.5);
  spec.locomotionDynamics.direction=["L","R"].includes(spec.locomotionDynamics.direction)?spec.locomotionDynamics.direction:"R";
  spec.locomotionDynamics.version="1.8.6";
  spec.motionPreview.direction=["L","R"].includes(spec.motionPreview?.direction)?spec.motionPreview.direction:spec.locomotionDynamics.direction;
  return spec.locomotionDynamics;
}
function smooth01(t){t=clamp(t,0,1);return t*t*(3-2*t)}
function resolveLocomotionMode(clip){
  if(!clip)return "none";normalizeClip(clip);
  const l=clip.locomotionDynamics||{},m=l.mode||"auto";
  if(m!=="auto")return m;
  const s=String(clip.runtime?.state||clip.name||"").toLowerCase();
  if(/sprint/.test(s))return "sprint";if(/start|accelerat/.test(s))return "start";if(/stop|brake/.test(s))return "stop";if(/turn/.test(s))return "turn";if(/strafe|sidestep/.test(s))return "strafe";
  return clip.runtime?.motionClass==="run"?"run":clip.runtime?.motionClass==="walk"?"walk":"none";
}
function locomotionOwnsCoreYaw(clip){
  if(!clip?.locomotionDynamics?.enabled||clip.locomotionDynamics?.bakedAt)return false;
  return ["walk","run","sprint","start","stop","turn","strafe"].includes(resolveLocomotionMode(clip));
}
function locomotionWave(mode,phase,progress,dir=1,intensity=1){
  const p=LOCOMOTION_PROFILES[mode]||LOCOMOTION_PROFILES.walk;
  let drive=1,lean=p.forwardLean,rootYaw=0,sideBias=0;
  if(mode==="start"){const r=smooth01(progress);drive=.20+.80*r;lean=p.forwardLean*(.45+.55*r)}
  if(mode==="stop"){const r=smooth01(progress);drive=1-.72*r;lean=p.forwardLean*(1-r)-4.5*r}
  if(mode==="turn"){rootYaw=dir*p.turnRoot*(.5-.5*Math.cos(phase));sideBias=dir*p.sideLean}
  if(mode==="strafe")sideBias=-dir*p.sideLean;
  const pelvisWave=Math.sin(phase+p.pelvisLead)*drive;
  const chestWave=Math.sin(phase-p.chestLag)*drive;
  const shoulderWave=Math.sin(phase-p.shoulderLag)*drive;
  const pelvisY=rad(p.pelvisYaw*pelvisWave*intensity);
  const chestY=rad(-p.chestYaw*chestWave*intensity);
  const chestX=rad(lean*intensity);
  const chestZ=rad(sideBias*intensity + (mode==="walk"?-.25*pelvisWave:mode==="run"?-.35*pelvisWave:0));
  const shoulder=rad(p.shoulderYaw*shoulderWave*intensity);
  const neckY=-(pelvisY+chestY)*.18;
  const headY=-(pelvisY+chestY+neckY)*p.headStability;
  const headX=-chestX*p.headStability*.42;
  const headZ=-chestZ*p.headStability*.55;
  return {mode,profile:p,drive,pelvisY,chestY,chestX,chestZ,shoulder,neckY,headY,headX,headZ,rootYaw,sideBias,phase,progress};
}
function evaluateLocomotionDynamics(clip,time){
  const empty={mode:"none",pelvisY:0,chestY:0,chestX:0,chestZ:0,shoulder:0,neckY:0,headY:0,headX:0,headZ:0};
  if(!clip?.keyframes?.length)return empty;normalizeClip(clip);
  if(!clip.locomotionDynamics?.enabled||clip.locomotionDynamics?.bakedAt)return empty;
  const mode=resolveLocomotionMode(clip);if(!LOCOMOTION_PROFILES[mode])return empty;
  const duration=Math.max(.001,clip.duration),progress=clamp(time/duration,0,1),phase=progress*Math.PI*2;
  const dir=(clip.locomotionDynamics.direction||"R")==="L"?-1:1;
  return locomotionWave(mode,phase,progress,dir,clip.locomotionDynamics.intensity??1);
}
function applyLocomotionDynamicsRuntime(clip,time){
  const r=evaluateLocomotionDynamics(clip,time),pelvis=joints.pelvis,chest=joints.chest,neck=joints.neck,head=joints.head,sL=joints.shoulderL,sR=joints.shoulderR;
  if(pelvis)pelvis.rotation.y+=r.pelvisY||0;
  if(chest){chest.rotation.y+=r.chestY||0;chest.rotation.x+=r.chestX||0;chest.rotation.z+=r.chestZ||0}
  if(sL)sL.rotation.y-=r.shoulder||0;if(sR)sR.rotation.y+=r.shoulder||0;
  if(neck)neck.rotation.y+=r.neckY||0;
  if(head){head.rotation.y+=r.headY||0;head.rotation.x+=r.headX||0;head.rotation.z+=r.headZ||0}
  locomotionDynamicsState.last=r;renderLocomotionStatus(r);scene.updateMatrixWorld(true);return r;
}
function renderLocomotionStatus(r=locomotionDynamicsState.last){
  if(!$("#locoModeValue"))return;
  const mode=(r?.mode||spec.motionPreview?.clip||"idle").toUpperCase();
  $("#locoModeValue").textContent=mode;
  $("#locoPelvisYaw").textContent=deg(r?.pelvisY||0).toFixed(1)+"°";
  $("#locoChestYaw").textContent=deg(r?.chestY||0).toFixed(1)+"°";
  $("#locoLeanValue").textContent=deg(r?.chestX||0).toFixed(1)+"°";
  if($("#locoDetail"))$("#locoDetail").textContent=mode==="IDLE"?"Idle has no locomotion owner":"Weight/COM = balance truth · Locomotion = pelvis/chest gait yaw + lean · Action Body Dynamics = action only";
}
function updateMotion(dt){
  if(!motionState.playing)return;
  ensureLocomotionDynamicsSpec();
  const c=spec.motionPreview,mode=c.clip||"walk";
  const profile=LOCOMOTION_PROFILES[mode];
  const cadence=mode==="idle"?.45:(profile?.cadence||1);
  motionState.phase += dt*c.speed*Math.PI*2*cadence;
  const phase=motionState.phase,progress=((phase/(Math.PI*2))%1+1)%1;
  const s=Math.sin(phase),co=Math.cos(phase),absS=Math.abs(s);
  restoreRuntimeBase();
  if(mode==="idle"){
    const breathe=Math.sin(phase*.5);
    applyJointRuntime("chest",breathe*1.4,0,breathe*.4);applyJointRuntime("shoulderL",1.5+breathe,0,-2);applyJointRuntime("shoulderR",-1.5-breathe,0,2);
    const pb=motionState.basePose.pelvis;joints.pelvis.position.y=pb.pos[1]+breathe*.012;
    locomotionDynamicsState.last={mode:"idle",pelvisY:0,chestY:0,chestX:0};renderLocomotionStatus();
  }else{
    const p=profile||LOCOMOTION_PROFILES.walk,dir=(spec.motionPreview.direction||spec.locomotionDynamics.direction)==="L"?-1:1;
    const wave=locomotionWave(mode,phase,progress,dir,spec.locomotionDynamics.intensity);
    const drive=wave.drive;
    const hip=c.hipSwing*p.hip*drive,arm=c.armSwing*p.arm*drive,kneeBase=c.kneeLift*p.knee*drive;
    let kneeL=Math.max(0,-s)*kneeBase,kneeR=Math.max(0,s)*kneeBase;
    if(mode==="run"||mode==="sprint"){kneeL+=Math.max(0,s)*kneeBase*.18;kneeR+=Math.max(0,-s)*kneeBase*.18}
    const armWave=Math.sin(phase-p.shoulderLag);
    applyJointRuntime("hipL",s*hip,0,mode==="strafe"?-dir*14*co:0);applyJointRuntime("hipR",-s*hip,0,mode==="strafe"?-dir*14*co:0);
    applyJointRuntime("kneeL",kneeL,0,0);applyJointRuntime("kneeR",kneeR,0,0);
    applyJointRuntime("ankleL",-s*p.ankle,0,mode==="strafe"?dir*5:0);applyJointRuntime("ankleR",s*p.ankle,0,mode==="strafe"?dir*5:0);
    applyJointRuntime("shoulderL",-armWave*arm,0,-7);applyJointRuntime("shoulderR",armWave*arm,0,7);
    applyJointRuntime("elbowL",-p.elbow-Math.max(0,armWave)*p.elbow*.55,0,-3);applyJointRuntime("elbowR",-p.elbow-Math.max(0,-armWave)*p.elbow*.55,0,3);
    const pelvisBase=motionState.basePose.pelvis,chestBase=motionState.basePose.chest,neckBase=motionState.basePose.neck,headBase=motionState.basePose.head;
    if(joints.pelvis)joints.pelvis.rotation.y=pelvisBase.rot[1]+wave.pelvisY;
    if(joints.chest){joints.chest.rotation.y=chestBase.rot[1]+wave.chestY;joints.chest.rotation.x=chestBase.rot[0]+wave.chestX;joints.chest.rotation.z=chestBase.rot[2]+wave.chestZ}
    if(joints.neck)joints.neck.rotation.y=neckBase.rot[1]+wave.neckY;
    if(c.headStabilization&&joints.head){joints.head.rotation.y=headBase.rot[1]+wave.headY;joints.head.rotation.x=headBase.rot[0]+wave.headX;joints.head.rotation.z=headBase.rot[2]+wave.headZ}
    const lateralWave=-s,lateralEase=lateralWave*Math.pow(Math.abs(lateralWave),.18);
    let lateral=p.lateral;
    if(mode==="walk")lateral=Math.min(lateral,spec.weight?.pelvisSolver?.walkVisualShiftCap??.016);
    if(mode==="strafe")joints.pelvis.position.x=pelvisBase.pos[0]+dir*(.012+.022*Math.abs(s))*Math.sign(s||1);
    else joints.pelvis.position.x=pelvisBase.pos[0]+lateralEase*lateral;
    let bob=Math.cos(phase*2)*p.bob-(absS*p.compression);
    if(mode==="run")bob+=Math.max(0,-Math.cos(phase*2))*.018;
    if(mode==="sprint")bob+=Math.max(0,-Math.cos(phase*2))*.032;
    if(mode==="start")bob-=(1-smooth01(progress))*.018;
    if(mode==="stop")bob-=smooth01(progress)*.020;
    joints.pelvis.position.y=pelvisBase.pos[1]+bob;
    if(mode==="turn"&&motionState.baseRoot)characterRoot.rotation.y=motionState.baseRoot.rot[1]+rad(wave.rootYaw);
    locomotionDynamicsState.last=wave;renderLocomotionStatus(wave);
  }
  updateFootContacts();
}
'''
    html=html[:start]+new+html[end:]

    rep('''  if(clip==="idle"){stanceL=true;stanceR=true}\n  else{\n    const s=Math.sin(motionState.phase);\n    stanceL=s<-.08;stanceR=s>.08;\n  }''','''  if(clip==="idle"){stanceL=true;stanceR=true}\n  else{\n    const s=Math.sin(motionState.phase);\n    if(clip==="run"||clip==="sprint"){stanceL=s<-.58;stanceR=s>.58}\n    else{stanceL=s<-.08;stanceR=s>.08}\n  }''','run sprint flight contact')

    rep('''  let hipDrop=rad(cfg.hipDropDeg*dominance);\n  let twist=rad(cfg.twistDeg*dominance);\n  let compression=cfg.compression*Math.abs(dominance);''','''  let hipDrop=rad(cfg.hipDropDeg*dominance);\n  let twist=rad(cfg.twistDeg*dominance);\n  if(locomotionOwnsCoreYaw(clip))twist=0;\n  let compression=cfg.compression*Math.abs(dominance);''','pelvis yaw ownership')

    rep('''function applyCompleteWeightMotionRuntime(clip,time){\n  const weight=applyFullWeightResponseRuntime(clip,time);\n  const attack=applyAttackWeightResponseRuntime(clip,time);\n  const body=applyBodyDynamicsRuntime(clip,time);\n  const impact=applyImpactResponseRuntime(clip,time);\n  return {weight,attack,body,impact};\n}''','''function applyCompleteWeightMotionRuntime(clip,time){\n  const weight=applyFullWeightResponseRuntime(clip,time);\n  const locomotion=applyLocomotionDynamicsRuntime(clip,time);\n  const attack=applyAttackWeightResponseRuntime(clip,time);\n  const body=applyBodyDynamicsRuntime(clip,time);\n  const impact=applyImpactResponseRuntime(clip,time);\n  return {weight,locomotion,attack,body,impact};\n}''','locomotion runtime layer')

    rep('''  $("#motionClip").value=spec.motionPreview.clip||"walk";\n  $("#contactToggle").checked=spec.motionPreview.showContacts!==false;''','''  $("#motionClip").value=spec.motionPreview.clip||"walk";\n  if($("#motionDirection"))$("#motionDirection").value=spec.motionPreview.direction||"R";\n  renderLocomotionStatus();\n  $("#contactToggle").checked=spec.motionPreview.showContacts!==false;''','build locomotion controls')
    rep('''$("#motionClip").onchange=e=>withCommand("Motion clip",()=>{\n  if(motionState.playing)stopMotionPreview(true);\n  spec.motionPreview.clip=e.target.value;motionState.maxSlide=0;updateContactUI();\n});''','''$("#motionClip").onchange=e=>withCommand("Motion clip",()=>{\n  if(motionState.playing)stopMotionPreview(true);\n  spec.motionPreview.clip=e.target.value;motionState.maxSlide=0;locomotionDynamicsState.last=null;updateContactUI();renderLocomotionStatus();\n});\n$("#motionDirection").onchange=e=>withCommand("Locomotion direction",()=>{spec.motionPreview.direction=e.target.value;ensureLocomotionDynamicsSpec().direction=e.target.value;renderLocomotionStatus()});''','locomotion direction binding')

    rep('''  const duration=(proc==="idle"?2.0:proc==="run"?0.72:1.05)/Math.max(.2,spec.motionPreview.speed||1);''','''  const baseDuration={idle:2.0,walk:1.05,run:.72,sprint:.58,start:1.0,stop:1.10,turn:1.0,strafe:.95}[proc]||1.05;\n  const duration=baseDuration/Math.max(.2,spec.motionPreview.speed||1);''','procedural locomotion bake duration')
    rep('''    const clip=makeAnimationClip(`Baked_${proc[0].toUpperCase()+proc.slice(1)}`,duration,fps);\n    clip.interpolation="smooth";clip.loop=proc!=="attack";clip.keyframes=frames;\n    spec.animations.push(clip);animationState.selectedClipId=clip.id;animationState.time=0;''','''    const clip=makeAnimationClip(`Baked_${proc[0].toUpperCase()+proc.slice(1)}`,duration,fps);\n    clip.interpolation="smooth";clip.loop=!( ["start","stop"].includes(proc));clip.keyframes=frames;\n    clip.runtime.motionClass=proc==="idle"?"idle":(["run","sprint"].includes(proc)?"run":"walk");\n    clip.runtime.motionSpeed=proc==="sprint"?6.8:proc==="run"?4.5:proc==="idle"?0:1.8;\n    Object.assign(clip.locomotionDynamics,{enabled:true,mode:proc,direction:spec.motionPreview.direction||"R",bakedAt:new Date().toISOString(),version:"1.8.6"});\n    spec.animations.push(clip);animationState.selectedClipId=clip.id;animationState.time=0;''','baked locomotion contract')

    rep('''  clip.runtime.state=n.replace(/[^a-z0-9]+/g,"_").replace(/^_|_$/g,"")||motionClass;\n  clip.loop=loop;clip.interpolation=interpolation;''','''  clip.runtime.state=n.replace(/[^a-z0-9]+/g,"_").replace(/^_|_$/g,"")||motionClass;\n  const locoMode=/sprint/.test(n)?"sprint":/start/.test(n)?"start":/stop/.test(n)?"stop":/turn/.test(n)?"turn":/strafe/.test(n)?"strafe":motionClass==="run"?"run":motionClass==="walk"?"walk":"none";\n  Object.assign(clip.locomotionDynamics,{enabled:locoMode!=="none",mode:locoMode,direction:"R",intensity:1,version:"1.8.6"});\n  clip.loop=loop;clip.interpolation=interpolation;''','template locomotion inference')

    anchor='''function createAttackTemplate(){'''
    funcs=r'''function createSprintTemplate(){
  const clip=createTemplateClip("Sprint_PoseLibrary",.58,30,[{time:0,pose:"runContact",side:"L"},{time:.145,pose:"walkPassing",side:"L"},{time:.29,pose:"runContact",side:"R"},{time:.435,pose:"walkPassing",side:"R"},{time:.58,pose:"runContact",side:"L"}],true,"smooth");
  clip.runtime.motionClass="run";clip.runtime.motionSpeed=6.8;clip.locomotionDynamics.mode="sprint";addTemplateClip(clip);
}
function createStartTemplate(){
  const clip=createTemplateClip("Start_Accelerate",1.0,30,[{time:0,pose:"idle"},{time:.24,pose:"runContact",side:"L"},{time:.54,pose:"walkPassing",side:"L"},{time:1,pose:"runContact",side:"R"}],false,"smooth");
  clip.runtime.motionClass="walk";clip.runtime.motionSpeed=2.8;clip.locomotionDynamics.mode="start";addTemplateClip(clip);
}
function createStopTemplate(){
  const clip=createTemplateClip("Stop_Brake",1.10,30,[{time:0,pose:"runContact",side:"L"},{time:.32,pose:"walkPassing",side:"L"},{time:.72,pose:"walkContact",side:"R"},{time:1.10,pose:"idle"}],false,"smooth");
  clip.runtime.motionClass="walk";clip.runtime.motionSpeed=0;clip.locomotionDynamics.mode="stop";addTemplateClip(clip);
}
function createTurnTemplate(){
  const clip=createTemplateClip("Turn_R_PoseLibrary",1.0,30,[{time:0,pose:"walkContact",side:"L"},{time:.25,pose:"walkPassing",side:"L"},{time:.5,pose:"walkContact",side:"R"},{time:.75,pose:"walkPassing",side:"R"},{time:1,pose:"walkContact",side:"L"}],true,"smooth");
  clip.runtime.motionClass="walk";clip.runtime.motionSpeed=1.4;clip.locomotionDynamics.mode="turn";clip.locomotionDynamics.direction="R";addTemplateClip(clip);
}
function createStrafeTemplate(){
  const clip=createTemplateClip("Strafe_R_PoseLibrary",.95,30,[{time:0,pose:"walkContact",side:"L"},{time:.24,pose:"walkPassing",side:"L"},{time:.48,pose:"walkContact",side:"R"},{time:.72,pose:"walkPassing",side:"R"},{time:.95,pose:"walkContact",side:"L"}],true,"smooth");
  clip.runtime.motionClass="walk";clip.runtime.motionSpeed=1.6;clip.locomotionDynamics.mode="strafe";clip.locomotionDynamics.direction="R";addTemplateClip(clip);
}
'''+anchor
    rep(anchor,funcs,'locomotion library functions')

    rep('''$("#btnTemplateWalk").onclick=createWalkTemplate;\n$("#btnTemplateRun").onclick=createRunTemplate;''','''$("#btnTemplateWalk").onclick=createWalkTemplate;\n$("#btnTemplateRun").onclick=createRunTemplate;\n$("#btnTemplateSprint").onclick=createSprintTemplate;\n$("#btnTemplateStart").onclick=createStartTemplate;\n$("#btnTemplateStop").onclick=createStopTemplate;\n$("#btnTemplateTurn").onclick=createTurnTemplate;\n$("#btnTemplateStrafe").onclick=createStrafeTemplate;''','locomotion library bindings')

    rep('''      attackProfile:structuredClone(c.attackProfile||{}),\n      keyframeCount:c.keyframes.length''','''      attackProfile:structuredClone(c.attackProfile||{}),\n      locomotionDynamics:structuredClone(c.locomotionDynamics||{}),\n      keyframeCount:c.keyframes.length''','runtime locomotion manifest')

    rep('''  c.bodyDynamics=c.bodyDynamics||{};\n  return c;''','''  c.bodyDynamics=c.bodyDynamics||{};\n  c.locomotionDynamics=c.locomotionDynamics||{enabled:true,mode:"auto",direction:"R",intensity:1,bakedAt:null,version:"1.8.6"};\n  return c;''','runtime normalize locomotion')

    runtime_anchor='''function applyRuntimePelvisSolver(joints,clip,time,weightCfg){'''
    runtime_loco=r'''const RUNTIME_LOCOMOTION_PROFILES={
  walk:{pelvisYaw:3.5,chestYaw:5.8,shoulderYaw:1.6,forwardLean:1.8,sideLean:.6,pelvisLead:.08,chestLag:.08,shoulderLag:.13,headStability:.86},
  run:{pelvisYaw:4.2,chestYaw:7.4,shoulderYaw:2.4,forwardLean:7.5,sideLean:.9,pelvisLead:.10,chestLag:.10,shoulderLag:.18,headStability:.82},
  sprint:{pelvisYaw:3.8,chestYaw:8.8,shoulderYaw:3.0,forwardLean:14,sideLean:.8,pelvisLead:.12,chestLag:.12,shoulderLag:.22,headStability:.76},
  start:{pelvisYaw:4.0,chestYaw:7.0,shoulderYaw:2.5,forwardLean:12,sideLean:.7,pelvisLead:.10,chestLag:.10,shoulderLag:.18,headStability:.80},
  stop:{pelvisYaw:3.2,chestYaw:5.6,shoulderYaw:2.0,forwardLean:7,sideLean:.8,pelvisLead:.07,chestLag:.10,shoulderLag:.16,headStability:.86},
  turn:{pelvisYaw:7.5,chestYaw:4.8,shoulderYaw:2.1,forwardLean:2.8,sideLean:4.5,pelvisLead:.06,chestLag:.11,shoulderLag:.16,headStability:.88},
  strafe:{pelvisYaw:1.8,chestYaw:3.4,shoulderYaw:1.8,forwardLean:2.0,sideLean:5.2,pelvisLead:.05,chestLag:.10,shoulderLag:.15,headStability:.90}
};
function runtimeLocomotionMode(clip){
  const l=clip?.locomotionDynamics||{},m=l.mode||"auto",s=String(clip?.runtime?.state||clip?.name||"").toLowerCase();if(m!=="auto")return m;
  if(/sprint/.test(s))return "sprint";if(/start|accelerat/.test(s))return "start";if(/stop|brake/.test(s))return "stop";if(/turn/.test(s))return "turn";if(/strafe|sidestep/.test(s))return "strafe";return clip?.runtime?.motionClass==="run"?"run":clip?.runtime?.motionClass==="walk"?"walk":"none";
}
function runtimeLocomotionOwns(clip){return clip?.locomotionDynamics?.enabled!==false&&!clip?.locomotionDynamics?.bakedAt&&!!RUNTIME_LOCOMOTION_PROFILES[runtimeLocomotionMode(clip)]}
function runtimeSmooth01(t){t=clamp(t,0,1);return t*t*(3-2*t)}
function applyRuntimeLocomotionDynamics(joints,clip,time){
  if(!runtimeLocomotionOwns(clip))return;
  const mode=runtimeLocomotionMode(clip),p=RUNTIME_LOCOMOTION_PROFILES[mode],l=clip.locomotionDynamics||{},progress=clamp(time/Math.max(.001,clip.duration),0,1),phase=progress*Math.PI*2,dir=(l.direction||"R")==="L"?-1:1,intensity=l.intensity??1;
  let drive=1,lean=p.forwardLean,sideBias=0;
  if(mode==="start"){const r=runtimeSmooth01(progress);drive=.20+.80*r;lean=p.forwardLean*(.45+.55*r)}
  if(mode==="stop"){const r=runtimeSmooth01(progress);drive=1-.72*r;lean=p.forwardLean*(1-r)-4.5*r}
  if(mode==="turn")sideBias=dir*p.sideLean;if(mode==="strafe")sideBias=-dir*p.sideLean;
  const pelvisY=(p.pelvisYaw*Math.PI/180)*Math.sin(phase+p.pelvisLead)*drive*intensity,chestY=-(p.chestYaw*Math.PI/180)*Math.sin(phase-p.chestLag)*drive*intensity,chestX=(lean*Math.PI/180)*intensity,chestZ=(sideBias*Math.PI/180)*intensity,shoulder=(p.shoulderYaw*Math.PI/180)*Math.sin(phase-p.shoulderLag)*drive*intensity,neckY=-(pelvisY+chestY)*.18,headY=-(pelvisY+chestY+neckY)*p.headStability,headX=-chestX*p.headStability*.42,headZ=-chestZ*p.headStability*.55;
  const pelvis=joints.pelvis,chest=joints.chest,neck=joints.neck,head=joints.head,sL=joints.shoulderL,sR=joints.shoulderR;
  if(pelvis)pelvis.rotation.y+=pelvisY;if(chest){chest.rotation.y+=chestY;chest.rotation.x+=chestX;chest.rotation.z+=chestZ}if(sL)sL.rotation.y-=shoulder;if(sR)sR.rotation.y+=shoulder;if(neck)neck.rotation.y+=neckY;if(head){head.rotation.y+=headY;head.rotation.x+=headX;head.rotation.z+=headZ}
}

'''+runtime_anchor
    rep(runtime_anchor,runtime_loco,'standalone runtime locomotion functions')
    rep('''  p.rotation.y+=((s.twistDeg??4)*Math.PI/180)*dominance;''','''  if(!runtimeLocomotionOwns(clip))p.rotation.y+=((s.twistDeg??4)*Math.PI/180)*dominance;''','runtime pelvis yaw ownership')
    rep('''  const pelvisTwist=((p.twistDeg??4)*Math.PI/180)*dominance;''','''  const pelvisTwist=runtimeLocomotionOwns(clip)?0:((p.twistDeg??4)*Math.PI/180)*dominance;''','runtime upper yaw ownership')
    rep('''    applyRuntimePelvisSolver(this.joints,this.current,this.time,this.weight);\n    applyRuntimeUpperBodySolver(this.joints,this.current,this.time,this.weight);\n    applyRuntimeAttackWeight(this.joints,this.current,this.time,this.weight);''','''    applyRuntimePelvisSolver(this.joints,this.current,this.time,this.weight);\n    applyRuntimeUpperBodySolver(this.joints,this.current,this.time,this.weight);\n    applyRuntimeLocomotionDynamics(this.joints,this.current,this.time);\n    applyRuntimeAttackWeight(this.joints,this.current,this.time,this.weight);''','standalone runtime locomotion apply')

    rep('''ensureRuntimeSettings();ensureWeightSpec();ensureSkinSystem();migrateNaturalWalkTuning();migrateWalkPelvisTranslationHotfix();''','''ensureRuntimeSettings();ensureWeightSpec();ensureSkinSystem();migrateNaturalWalkTuning();migrateWalkPelvisTranslationHotfix();ensureLocomotionDynamicsSpec();''','locomotion spec migration')
    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.5.3"','localStorage.setItem("characterPrototypeStudio.v1.8.6"',1)
    html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.5.3")||','const raw=localStorage.getItem("characterPrototypeStudio.v1.8.6")||localStorage.getItem("characterPrototypeStudio.v1.8.5.3")||',1)
    html=html.replace('// Generated by Character Prototype Studio V1.8.5.3','// Generated by Character Prototype Studio V1.8.6')
    return html

if __name__=='__main__':
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
