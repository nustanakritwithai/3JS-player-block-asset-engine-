#!/usr/bin/env python3

def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)

    html=html.replace('Character Prototype Studio V1.8.5','Character Prototype Studio V1.8.5.1')
    html=html.replace('V1.8.5 · Dynamics Auto-Tuner / Inspector-Guided Modifier Preview',
                      'V1.8.5.1 · Twist Visual Recovery Hotfix / Deterministic Demo Path')
    html=html.replace('generatorVersion:"1.8.5"','generatorVersion:"1.8.5.1"')

    old='''function twistDemo(){
  let clip=selectedAnimationClip();
  if(!clip||clip.runtime?.motionClass!=="action"){
    createAttackTemplate();
    clip=selectedAnimationClip();
  }
  normalizeClip(clip);
  clip.bodyDynamics.enabled=true;
  if(clip.bodyDynamics.actionType==="auto")clip.bodyDynamics.actionType="slash";
  if(clip.bodyDynamics.intensity<.85)clip.bodyDynamics.intensity=.92;
  animationState.time=0;
  if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);
  startAnimationPlayback();
  toast("Twist Demo: ดู Pelvis → Chest → Shoulder ช่วง Wind-up → Impact");
}'''
    new=r'''function makeKnownGoodTwistDemoClip(){
  const clip=createTemplateClip("Twist_Demo_V1_8_5_1",.96,30,[
    {time:0.00,pose:"idle"},
    {time:0.30,pose:"attackWindup",side:"R"},
    {time:0.52,pose:"attackImpact",side:"R"},
    {time:0.96,pose:"idle"}
  ],false,"smooth");
  clip.source={kind:"twist-visual-demo",studioVersion:"1.8.5.1"};
  clip.runtime.motionClass="action";
  clip.runtime.state="twist_demo_v1_8_5_1";
  Object.assign(clip.attackProfile,{
    enabled:true,side:"R",style:"horizontal",
    anticipationEnd:.12,windupEnd:.31,impactTime:.52,impactHold:.055,
    followThroughEnd:.74,recoveryEnd:.96,
    windupTwistDeg:20,swingTwistDeg:34,followThroughDeg:18,forwardLeanDeg:7
  });
  Object.assign(clip.bodyDynamics,BODY_DYNAMICS_PRESETS.natural,{
    enabled:true,preset:"natural",actionType:"slash",intensity:1.0,
    pelvisShare:.34,chestShare:.66,shoulderShare:.92,armShare:1.05,
    pelvisLead:.040,chestLag:.014,shoulderLag:.040,armLag:.068,
    counterRotation:.18,followThrough:.58,headStability:.86,
    forwardLeanShare:.36,sideLeanShare:.14,
    naturalPelvisDeg:14,naturalChestDeg:28,naturalShoulderDeg:48,
    naturalArmDeg:58,naturalHeadDeg:16,softLimitStart:.72,qa:null
  });
  return clip;
}
function ensureKnownGoodTwistDemoClip(){
  if(animationState.playing||animationState.basePose)stopAnimationPlayback(true);
  const fresh=makeKnownGoodTwistDemoClip();
  let clip=(spec.animations||[]).find(c=>c.source?.kind==="twist-visual-demo");
  if(clip){
    const id=clip.id;
    Object.assign(clip,fresh,{id});
  }else{
    clip=fresh;
    spec.animations.push(clip);
  }
  normalizeClip(clip);
  animationState.selectedClipId=clip.id;
  animationState.time=0;
  buildAnimationUI(false);
  return clip;
}
function twistDemoPeakReport(clip){
  let pelvis=0,chest=0,shoulder=0,arm=0;
  for(let i=0;i<=120;i++){
    const r=evaluateBodyDynamics(clip,clip.duration*i/120);
    pelvis=Math.max(pelvis,Math.abs(deg(r.pelvisY||0)));
    chest=Math.max(chest,Math.abs(deg(r.chestY||0)));
    shoulder=Math.max(shoulder,Math.abs(deg(r.shoulderY||0)));
    arm=Math.max(arm,Math.abs(deg(r.elbowY||0)));
  }
  return {pelvis,chest,shoulder,arm,visible:pelvis>=6&&chest>=10&&shoulder>=14};
}
function twistDemo(){
  const clip=ensureKnownGoodTwistDemoClip();
  const report=twistDemoPeakReport(clip);
  if(!report.visible){
    console.error("V1.8.5.1 Twist Demo preflight failed",report,clip.bodyDynamics);
    toast("Twist Demo BLOCKED · generated profile failed visibility threshold");
    return;
  }
  // Demo view is deterministic: neutral root + 3/4 camera. This does not rewrite authored user clips.
  characterRoot.rotation.y=0;
  setCamera("iso");
  renderBodyDynamicsStatus(evaluateBodyDynamics(clip,0));
  startAnimationPlayback();
  toast(`Twist Demo locked · Pelvis ${report.pelvis.toFixed(1)}° → Chest ${report.chest.toFixed(1)}° → Shoulder ${report.shoulder.toFixed(1)}°`);
}'''
    rep(old,new,'deterministic twist demo')

    # Use a new save namespace but migrate the previous V1.8.5 browser state.
    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.5"',
                      'localStorage.setItem("characterPrototypeStudio.v1.8.5.1"',1)
    html=html.replace(
      'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.5")||localStorage.getItem("characterPrototypeStudio.v1.8.4.1")||',
      'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.5.1")||localStorage.getItem("characterPrototypeStudio.v1.8.5")||localStorage.getItem("characterPrototypeStudio.v1.8.4.1")||',
      1)
    return html
