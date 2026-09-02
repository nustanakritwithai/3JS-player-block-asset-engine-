#!/usr/bin/env python3
from pathlib import Path
import base64,lzma,shutil,hashlib
root=Path(__file__).resolve().parents[1]
parts=sorted((root/'deploy'/'source_v1_8'/'parts').glob('studio_v1_8.html.xz.b64.part*'))
if not parts: raise SystemExit('No V1.8 source parts found')
encoded=''.join(x.read_text(encoding='ascii').strip() for x in parts)
html=lzma.decompress(base64.b64decode(encoded)).decode('utf-8')
def rep(old,new,label):
    global html
    if old not in html: raise SystemExit('Patch anchor missing: '+label)
    html=html.replace(old,new,1)
html=html.replace('Character Prototype Studio V1.8','Character Prototype Studio V1.8.1')
html=html.replace('V1.8 · High-Quality Skin / PBR / Texture Quality Gate','V1.8.1 · Natural Walk / Reduced Pelvis Sway / Skin PBR')
html=html.replace('generatorVersion:"1.8.0"','generatorVersion:"1.8.1"')
rep('''  motionPreview:{
    clip:"walk",speed:1.0,hipSwing:34,kneeLift:52,armSwing:38,
    pelvisShift:.055,pelvisBob:.045,pelvisTwist:5,chestTwist:7,
    compression:.022,headStabilization:true,showContacts:true
  },''','''  motionPreview:{
    clip:"walk",speed:1.0,hipSwing:34,kneeLift:52,armSwing:38,
    pelvisShift:.028,pelvisBob:.040,pelvisTwist:3.5,chestTwist:5.5,
    compression:.020,headStabilization:true,showContacts:true,tuningVersion:"1.8.1"
  },''','motion defaults')
rep('''    pelvisSolver:{
      enabled:true,lateralInfluence:.55,maxShift:.14,hipDropDeg:5,twistDeg:6,
      compression:.025,comGain:.45,comMaxCorrection:.10,smoothing:.65
    },''','''    pelvisSolver:{
      enabled:true,lateralInfluence:.32,maxShift:.075,hipDropDeg:2.5,twistDeg:4,
      compression:.020,comGain:.26,comMaxCorrection:.05,smoothing:.78,tuningVersion:"1.8.1"
    },''','pelvis defaults')
rep('''    const pelvisBase=motionState.basePose.pelvis;
    const weightDir=s>=0?-1:1;
    joints.pelvis.position.x=pelvisBase.pos[0]+weightDir*c.pelvisShift*(.35+.65*absS);
    joints.pelvis.position.y=pelvisBase.pos[1]+Math.cos(motionState.phase*2)*c.pelvisBob-(absS*c.compression);''','''    const pelvisBase=motionState.basePose.pelvis;
    const lateralWave=-s;
    const lateralEase=lateralWave*Math.pow(Math.abs(lateralWave),.18);
    joints.pelvis.position.x=pelvisBase.pos[0]+lateralEase*c.pelvisShift;
    joints.pelvis.position.y=pelvisBase.pos[1]+Math.cos(motionState.phase*2)*c.pelvisBob-(absS*c.compression);''','procedural pelvis')
rep('''  const target=solverFootTargetLocal(weight);
  const pelvisWorld=new THREE.Vector3();pelvis.getWorldPosition(pelvisWorld);
  const pelvisLocal=characterRoot.worldToLocal(pelvisWorld.clone());
  const com=solverComLocal();

  const targetDeltaX=(target.x-pelvisLocal.x)*cfg.lateralInfluence;
  const comErrorX=target.x-com.x;
  const comCorrection=clamp(comErrorX*cfg.comGain,-cfg.comMaxCorrection,cfg.comMaxCorrection);
  let shiftX=clamp(targetDeltaX+comCorrection,-cfg.maxShift,cfg.maxShift);

  const dominance=weight.R-weight.L;
  const hipDrop=rad(cfg.hipDropDeg*dominance);
  const twist=rad(cfg.twistDeg*dominance);
  const compression=cfg.compression*Math.abs(weight.L-weight.R);

  if(options.smooth!==false&&pelvisSolverState.last){
    const retain=clamp(cfg.smoothing*.35,0,.35);
    shiftX=THREE.MathUtils.lerp(shiftX,pelvisSolverState.last.shiftX,retain);
  }
  return {shiftX,hipDrop,twist,compression,comCorrection,weight,targetX:target.x,comX:com.x};''','''  const rawDominance=weight.R-weight.L,mag=Math.abs(rawDominance),dead=.08;
  const n=mag<=dead?0:clamp((mag-dead)/(1-dead),0,1);
  let dominance=Math.sign(rawDominance)*Math.pow(n,1.25);
  const visualL=.5+(weight.L-.5)*.55,visualWeight={L:visualL,R:1-visualL};
  const target=solverFootTargetLocal(visualWeight);
  const pelvisWorld=new THREE.Vector3();pelvis.getWorldPosition(pelvisWorld);
  const pelvisLocal=characterRoot.worldToLocal(pelvisWorld.clone());
  const com=solverComLocal();
  const targetDeltaX=(target.x-pelvisLocal.x)*cfg.lateralInfluence;
  const comErrorX=target.x-com.x,feedbackScale=.25+.75*Math.abs(dominance);
  let comCorrection=clamp(comErrorX*cfg.comGain*feedbackScale,-cfg.comMaxCorrection,cfg.comMaxCorrection);
  let shiftX=clamp(targetDeltaX+comCorrection,-cfg.maxShift,cfg.maxShift);
  let hipDrop=rad(cfg.hipDropDeg*dominance),twist=rad(cfg.twistDeg*dominance);
  let compression=cfg.compression*Math.abs(dominance);
  if(options.smooth!==false&&pelvisSolverState.last){
    const retain=clamp(cfg.smoothing*.55,0,.55);
    shiftX=THREE.MathUtils.lerp(shiftX,pelvisSolverState.last.shiftX||0,retain);
    hipDrop=THREE.MathUtils.lerp(hipDrop,pelvisSolverState.last.hipDrop||0,retain);
    twist=THREE.MathUtils.lerp(twist,pelvisSolverState.last.twist||0,retain);
    compression=THREE.MathUtils.lerp(compression,pelvisSolverState.last.compression||0,retain);
  }
  return {shiftX,hipDrop,twist,compression,comCorrection,weight,visualWeight,visualDominance:dominance,targetX:target.x,comX:com.x};''','solver response')
rep('''function applyRuntimePelvisSolver(joints,clip,time,weightCfg){
  const p=joints.pelvis,s=weightCfg?.pelvisSolver;if(!p||!s||s.enabled===false||clip.weightTransfer?.pelvisSolverBakedAt)return;
  const w=runtimeWeightAt(clip,time),dominance=w.R-w.L,maxShift=s.maxShift??.14;
  p.position.x+=clamp(dominance*maxShift*(s.lateralInfluence??.55),-maxShift,maxShift);
  p.position.y-=(s.compression??.025)*Math.abs(w.L-w.R);
  p.rotation.z+=((s.hipDropDeg??5)*Math.PI/180)*dominance;
  p.rotation.y+=((s.twistDeg??6)*Math.PI/180)*dominance;
}''','''function applyRuntimePelvisSolver(joints,clip,time,weightCfg){
  const p=joints.pelvis,s=weightCfg?.pelvisSolver;if(!p||!s||s.enabled===false||clip.weightTransfer?.pelvisSolverBakedAt)return;
  const w=runtimeWeightAt(clip,time),raw=w.R-w.L,mag=Math.abs(raw),dead=.08;
  const n=mag<=dead?0:clamp((mag-dead)/(1-dead),0,1),dominance=Math.sign(raw)*Math.pow(n,1.25);
  const maxShift=s.maxShift??.075;
  p.position.x+=clamp(dominance*.55*maxShift*(s.lateralInfluence??.32),-maxShift,maxShift);
  p.position.y-=(s.compression??.020)*Math.abs(dominance);
  p.rotation.z+=((s.hipDropDeg??2.5)*Math.PI/180)*dominance;
  p.rotation.y+=((s.twistDeg??4)*Math.PI/180)*dominance;
}''','runtime pelvis')
insert='''function migrateNaturalWalkTuning(){
  const m=spec.motionPreview||{};
  if(m.tuningVersion!=="1.8.1"){
    if(Math.abs((Number(m.pelvisShift)||0)-.055)<.00001)m.pelvisShift=.028;
    if(Math.abs((Number(m.pelvisBob)||0)-.045)<.00001)m.pelvisBob=.040;
    if(Math.abs((Number(m.pelvisTwist)||0)-5)<.00001)m.pelvisTwist=3.5;
    if(Math.abs((Number(m.chestTwist)||0)-7)<.00001)m.chestTwist=5.5;
    if(Math.abs((Number(m.compression)||0)-.022)<.00001)m.compression=.020;
    m.tuningVersion="1.8.1";
  }
  const p=ensureWeightSpec().pelvisSolver;
  if(p.tuningVersion!=="1.8.1"){
    if(Math.abs((Number(p.lateralInfluence)||0)-.55)<.00001)p.lateralInfluence=.32;
    if(Math.abs((Number(p.maxShift)||0)-.14)<.00001)p.maxShift=.075;
    if(Math.abs((Number(p.hipDropDeg)||0)-5)<.00001)p.hipDropDeg=2.5;
    if(Math.abs((Number(p.twistDeg)||0)-6)<.00001)p.twistDeg=4;
    if(Math.abs((Number(p.compression)||0)-.025)<.00001)p.compression=.020;
    if(Math.abs((Number(p.comGain)||0)-.45)<.00001)p.comGain=.26;
    if(Math.abs((Number(p.comMaxCorrection)||0)-.10)<.00001)p.comMaxCorrection=.05;
    if(Math.abs((Number(p.smoothing)||0)-.65)<.00001)p.smoothing=.78;
    p.tuningVersion="1.8.1";
  }
}
'''
rep('const MOTION_FIELDS=[',insert+'const MOTION_FIELDS=[','migration insert')
rep('function initUI(){\n  ensureRuntimeSettings();ensureWeightSpec();ensureSkinSystem();','function initUI(){\n  ensureRuntimeSettings();ensureWeightSpec();ensureSkinSystem();migrateNaturalWalkTuning();','migration call')
html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8"','localStorage.setItem("characterPrototypeStudio.v1.8.1"',1)
html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8")||localStorage.getItem("characterPrototypeStudio.v1.7")||','const raw=localStorage.getItem("characterPrototypeStudio.v1.8.1")||localStorage.getItem("characterPrototypeStudio.v1.8")||localStorage.getItem("characterPrototypeStudio.v1.7")||',1)
html=html.replace('id="pelvisLateralInfluence" min="0" max="1.5" step=".05" value=".55"','id="pelvisLateralInfluence" min="0" max="1.5" step=".05" value=".32"')
html=html.replace('id="pelvisMaxShift" min="0" max=".5" step=".01" value=".14"','id="pelvisMaxShift" min="0" max=".5" step=".01" value=".075"')
html=html.replace('id="pelvisHipDrop" min="0" max="20" step=".5" value="5"','id="pelvisHipDrop" min="0" max="20" step=".5" value="2.5"')
html=html.replace('id="pelvisTwistWeight" min="0" max="25" step=".5" value="6"','id="pelvisTwistWeight" min="0" max="25" step=".5" value="4"')
if 'Character Prototype Studio V1.8.1' not in html: raise SystemExit('V1.8.1 patch failed')
site=root/'_site'
if site.exists(): shutil.rmtree(site)
site.mkdir(parents=True)
(site/'index.html').write_text(html,encoding='utf-8')
if (root/'assets').exists(): shutil.copytree(root/'assets',site/'assets',dirs_exist_ok=True)
(site/'.nojekyll').write_text('',encoding='utf-8')
print('Built V1.8.1',len(html.encode('utf-8')),'bytes')
print('sha256',hashlib.sha256(html.encode('utf-8')).hexdigest())
