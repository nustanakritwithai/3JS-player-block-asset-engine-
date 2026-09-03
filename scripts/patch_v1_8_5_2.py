#!/usr/bin/env python3


def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)

    html=html.replace('Character Prototype Studio V1.8.5.1','Character Prototype Studio V1.8.5.2')
    html=html.replace('V1.8.5.1 · Twist Visual Recovery Hotfix / Deterministic Demo Path',
                      'V1.8.5.2 · Twist Isolation + Animation Library Restore')
    html=html.replace('generatorVersion:"1.8.5.1"','generatorVersion:"1.8.5.2"')

    # Move the existing animation template library to the top of Animation Lab.
    library='''        <div class="chainbox">\n          <h3>ANIMATION TEMPLATES FROM POSE LIBRARY</h3>\n          <div class="posegrid">\n            <button class="btn" id="btnTemplateWalk">Walk 4-Phase</button>\n            <button class="btn" id="btnTemplateRun">Run 4-Phase</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>\n            <button class="btn" id="btnTemplateIdle">Idle Breathing</button>\n          </div>\n          <div class="hint" style="margin-top:7px">สร้าง clip ใหม่จาก Pose Library แล้วแก้ keyframe ต่อใน Timeline ได้ทันที</div>\n        </div>\n\n'''
    if html.count(library)!=1:
        raise RuntimeError('animation library block count changed')
    html=html.replace(library,'',1)
    anchor='''        <h3>ANIMATION LAB <span class="pill good" id="animStatus">READY</span></h3>\n'''
    top_library='''        <h3>ANIMATION LAB <span class="pill good" id="animStatus">READY</span></h3>\n        <div class="chainbox" id="animationLibraryTop">\n          <h3>ANIMATION LIBRARY <span class="posebadge good">RESTORED</span></h3>\n          <div class="posegrid">\n            <button class="btn" id="btnTemplateWalk">Walk 4-Phase</button>\n            <button class="btn" id="btnTemplateRun">Run 4-Phase</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>\n            <button class="btn" id="btnTemplateIdle">Idle Breathing</button>\n          </div>\n          <div class="hint" style="margin-top:7px">Library อยู่บนสุดของ Anim tab และ Twist Demo จะไม่เพิ่ม/ลบ clip ใน library นี้อีก</div>\n        </div>\n'''
    rep(anchor,top_library,'animation library restore')

    # bodyDynamicsState gets a transient status clip override for isolation demo.
    rep('''let bodyDynamicsState={\n  last:null\n};''','''let bodyDynamicsState={\n  last:null,\n  statusClip:null\n};''','body dynamics transient status')
    rep('''function renderBodyDynamicsStatus(r=bodyDynamicsState.last){\n  if(!$("#bodyPhaseValue"))return;\n  const clip=selectedAnimationClip();''','''function renderBodyDynamicsStatus(r=bodyDynamicsState.last){\n  if(!$("#bodyPhaseValue"))return;\n  const clip=bodyDynamicsState.statusClip||selectedAnimationClip();''','body status override')

    # Replace V1.8.5.1 persisted demo path with a pure transient Body Dynamics isolation demo.
    start=html.index('function makeKnownGoodTwistDemoClip(){')
    end=html.index('function previewBodyDynamicsCurrent(){',start)
    new=r'''let twistVisualState={playing:false,time:0,clip:null,basePose:null,baseRoot:null};
function makeTwistIsolationClip(){
  const clip=makeAnimationClip("Twist_Isolation_V1_8_5_2",2.40,30);
  clip.loop=true;clip.interpolation="smooth";
  clip.source={kind:"transient-twist-isolation",studioVersion:"1.8.5.2"};
  clip.runtime.motionClass="action";clip.runtime.state="twist_isolation_v1_8_5_2";
  const neutral=poseSnapshotFromLibrary("reset","R");
  const key=t=>({time:t,joints:cloneAnimationPose(neutral),meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}});
  clip.keyframes=[key(0),key(.72),key(1.30),key(1.82),key(2.40)];
  Object.assign(clip.attackProfile,{
    enabled:false,side:"R",style:"horizontal",
    anticipationEnd:.30,windupEnd:.78,impactTime:1.30,impactHold:.10,
    followThroughEnd:1.82,recoveryEnd:2.40,
    windupTwistDeg:24,swingTwistDeg:40,followThroughDeg:22,forwardLeanDeg:6
  });
  clip.impactProfile.enabled=false;
  Object.assign(clip.bodyDynamics,BODY_DYNAMICS_PRESETS.natural,{
    enabled:true,preset:"natural",actionType:"slash",intensity:1.08,
    pelvisShare:.40,chestShare:.72,shoulderShare:1.00,armShare:1.08,
    pelvisLead:.070,chestLag:.030,shoulderLag:.090,armLag:.145,
    counterRotation:.16,followThrough:.62,headStability:.88,
    forwardLeanShare:.28,sideLeanShare:.10,
    naturalPelvisDeg:16,naturalChestDeg:32,naturalShoulderDeg:52,
    naturalArmDeg:60,naturalHeadDeg:16,softLimitStart:.76,qa:null
  });
  normalizeClip(clip);
  return clip;
}
function twistDemoPeakReport(clip){
  let pelvis=0,chest=0,shoulder=0,arm=0,pelvisT=0,chestT=0,shoulderT=0;
  for(let i=0;i<=240;i++){
    const t=clip.duration*i/240,r=evaluateBodyDynamics(clip,t);
    const pv=Math.abs(deg(r.pelvisY||0)),cv=Math.abs(deg(r.chestY||0)),sv=Math.abs(deg(r.shoulderY||0)),av=Math.abs(deg(r.elbowY||0));
    if(pv>pelvis){pelvis=pv;pelvisT=t} if(cv>chest){chest=cv;chestT=t} if(sv>shoulder){shoulder=sv;shoulderT=t} arm=Math.max(arm,av);
  }
  const ordered=pelvisT<=chestT+.001&&chestT<=shoulderT+.001;
  return {pelvis,chest,shoulder,arm,pelvisT,chestT,shoulderT,ordered,visible:pelvis>=7&&chest>=13&&shoulder>=18};
}
function restoreTwistVisualBase(){
  if(!twistVisualState.basePose)return;
  for(const [name,v] of Object.entries(twistVisualState.basePose)){
    if(joints[name]){joints[name].rotation.set(...v.rot);joints[name].position.fromArray(v.pos)}
  }
  if(twistVisualState.baseRoot){
    characterRoot.position.fromArray(twistVisualState.baseRoot.pos);
    characterRoot.rotation.set(twistVisualState.baseRoot.rot[0],0,twistVisualState.baseRoot.rot[2]);
  }
}
function stopTwistVisualDemo(restore=true){
  if(restore)restoreTwistVisualBase();
  twistVisualState.playing=false;twistVisualState.time=0;twistVisualState.clip=null;
  twistVisualState.basePose=null;twistVisualState.baseRoot=null;
  bodyDynamicsState.statusClip=null;bodyDynamicsState.last=null;
  const b=$("#btnTwistDemo");if(b)b.textContent="Twist Demo";
  renderBodyDynamicsStatus();
}
function updateTwistVisualDemo(dt){
  if(!twistVisualState.playing||!twistVisualState.clip)return;
  const clip=twistVisualState.clip;
  twistVisualState.time=(twistVisualState.time+dt)%clip.duration;
  restoreTwistVisualBase();
  applyAnimationAtTime(clip,twistVisualState.time);
  applyBodyDynamicsRuntime(clip,twistVisualState.time);
  scene.updateMatrixWorld(true);
}
function purgeLegacyTwistDemoClips(){
  if(!Array.isArray(spec.animations))return 0;
  const before=spec.animations.length,selected=animationState.selectedClipId;
  spec.animations=spec.animations.filter(c=>c.source?.kind!=="twist-visual-demo"&&c.source?.kind!=="transient-twist-isolation");
  if(!spec.animations.some(c=>c.id===selected))animationState.selectedClipId=spec.animations[0]?.id||null;
  return before-spec.animations.length;
}
function twistDemo(){
  if(twistVisualState.playing){stopTwistVisualDemo(true);toast("Twist Isolation stopped");return}
  if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);
  if(gameRuntimeState.playing||gameRuntimeState.basePose)runtimePreviewStop(true);
  if(motionState.playing)stopMotionPreview(true);
  const clip=makeTwistIsolationClip(),report=twistDemoPeakReport(clip);
  if(!report.visible||!report.ordered){
    console.error("V1.8.5.2 Twist Isolation preflight failed",report);
    toast("Twist Isolation BLOCKED · visual chain preflight failed");
    return;
  }
  twistVisualState.clip=clip;twistVisualState.time=0;
  twistVisualState.basePose=captureRuntimeBase();
  twistVisualState.baseRoot={pos:characterRoot.position.toArray(),rot:[characterRoot.rotation.x,characterRoot.rotation.y,characterRoot.rotation.z]};
  twistVisualState.playing=true;bodyDynamicsState.statusClip=clip;
  characterRoot.rotation.y=0;setCamera("iso");openTab("animation");
  const b=$("#btnTwistDemo");if(b)b.textContent="Stop Twist Demo";
  renderBodyDynamicsStatus(evaluateBodyDynamics(clip,0));
  toast(`ISOLATED Body Dynamics · Pelvis ${report.pelvis.toFixed(1)}° → Chest ${report.chest.toFixed(1)}° → Shoulder ${report.shoulder.toFixed(1)}°`);
}
'''
    html=html[:start]+new+html[end:]

    rep('''function startAnimationPlayback(){\n  if(gameRuntimeState.playing||gameRuntimeState.basePose)runtimePreviewStop(true);''','''function startAnimationPlayback(){\n  if(twistVisualState.playing)stopTwistVisualDemo(true);\n  if(gameRuntimeState.playing||gameRuntimeState.basePose)runtimePreviewStop(true);''','animation stops twist isolation')

    rep('''  if(spec.look.autoRotate&&!motionState.playing&&!animationState.playing&&!gameRuntimeState.playing) characterRoot.rotation.y+=dt*.45;\n  if(gameRuntimeState.playing)updateGameRuntime(dt);\n  else if(animationState.playing)updateAnimationPlayback(dt);\n  else updateMotion(dt);''','''  if(spec.look.autoRotate&&!twistVisualState.playing&&!motionState.playing&&!animationState.playing&&!gameRuntimeState.playing) characterRoot.rotation.y+=dt*.45;\n  if(twistVisualState.playing)updateTwistVisualDemo(dt);\n  else if(gameRuntimeState.playing)updateGameRuntime(dt);\n  else if(animationState.playing)updateAnimationPlayback(dt);\n  else updateMotion(dt);''','isolation render ownership')

    rep('''loadLocal();initUI();buildCharacter(false);applyCapturedPose(spec.pose.joints);$("#poseLabel").textContent=spec.pose.name||"Custom";updateHistoryButtons();onResize();animate(performance.now());''','''loadLocal();const purgedLegacyTwistDemos=purgeLegacyTwistDemoClips();initUI();buildCharacter(false);applyCapturedPose(spec.pose.joints);$("#poseLabel").textContent=spec.pose.name||"Custom";updateHistoryButtons();if(purgedLegacyTwistDemos)autoSave();onResize();animate(performance.now());''','purge legacy twist demos')

    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.5.1"',
                      'localStorage.setItem("characterPrototypeStudio.v1.8.5.2"',1)
    html=html.replace(
      'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.5.1")||',
      'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.5.2")||localStorage.getItem("characterPrototypeStudio.v1.8.5.1")||',1)
    return html

if __name__=='__main__':
    from pathlib import Path
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
