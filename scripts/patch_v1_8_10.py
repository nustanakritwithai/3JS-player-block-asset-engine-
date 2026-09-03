#!/usr/bin/env python3
from pathlib import Path

def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)

    html=html.replace('Character Prototype Studio V1.8.9','Character Prototype Studio V1.8.10')
    html=html.replace('V1.8.9 · Core Action / Reaction Pack','V1.8.10 · Monster Ball Action Pack')
    html=html.replace('generatorVersion:"1.8.9"','generatorVersion:"1.8.10"')

    rep('''          <button class="btn" data-librarypose="interactReach">Interact Reach</button>\n          <button class="btn" data-librarypose="attackWindup">Attack Wind-up</button>''',
        '''          <button class="btn" data-librarypose="interactReach">Interact Reach</button>\n          <button class="btn" data-librarypose="ballReady">Ball Ready</button>\n          <button class="btn" data-librarypose="ballAim">Ball Aim</button>\n          <button class="btn" data-librarypose="throwWindup">Throw Wind-up</button>\n          <button class="btn" data-librarypose="throwRelease">Throw Release</button>\n          <button class="btn" data-librarypose="throwFollow">Throw Follow-through</button>\n          <button class="btn" data-librarypose="monsterCommand">Monster Command</button>\n          <button class="btn" data-librarypose="attackWindup">Attack Wind-up</button>''','monster ball pose buttons')

    rep('''            <button class="btn" id="btnTemplateInteract">Interact</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>''',
        '''            <button class="btn" id="btnTemplateInteract">Interact</button>\n            <button class="btn good" id="btnTemplateBallAim">Ball Aim Loop</button>\n            <button class="btn good" id="btnTemplateCaptureThrowR">Capture Throw R</button>\n            <button class="btn" id="btnTemplateCaptureThrowL">Capture Throw L</button>\n            <button class="btn" id="btnTemplateQuickThrowR">Quick Throw R</button>\n            <button class="btn" id="btnTemplatePowerThrowR">Power Throw R</button>\n            <button class="btn good" id="btnTemplateSummonThrowR">Summon Monster R</button>\n            <button class="btn" id="btnTemplateMonsterCommand">Monster Command</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>''','monster ball animation buttons')
    html=html.replace('Core Animation Pack · Movement + Dodge L/R + Hit + Knockback + Get Up + Death/Faint + Interact · Weapon ยังไม่เริ่ม',
                      'MONSTER BALL CORE · Aim → Wind-up → Step → Release → Follow-through → Recover · Capture Throw + Summon Monster เป็นท่าหลัก · Weapon ยังไม่เริ่ม',1)

    rep('''              <option value="dodge">Dodge / Evade</option>\n            </select>''',
        '''              <option value="dodge">Dodge / Evade</option>\n              <option value="throw">Ball Throw</option>\n            </select>''','body action throw option')

    html=html.replace('["auto","punch","slash","heavy_slash","thrust","kick","dodge"].includes(b.actionType)',
                      '["auto","punch","slash","heavy_slash","thrust","kick","dodge","throw"].includes(b.actionType)')

    anchor='''  dodge:{\n    label:"Dodge / Evade",shape:"pulse",twistScale:.22,pelvisMul:.55,chestMul:.42,shoulderMul:.28,armMul:.20,\n    pelvisLeadAdd:0,chestLagAdd:.008,shoulderLagAdd:.015,armLagAdd:.020,followMul:.30,\n    forwardDrive:-.018,lateralDrive:.115,chestLeanMul:.40,sideLeanMul:2.4,\n    activeHipPitchDeg:0,supportHipRollDeg:6.0,kickLeg:false\n  }\n};'''
    replacement='''  dodge:{\n    label:"Dodge / Evade",shape:"pulse",twistScale:.22,pelvisMul:.55,chestMul:.42,shoulderMul:.28,armMul:.20,\n    pelvisLeadAdd:0,chestLagAdd:.008,shoulderLagAdd:.015,armLagAdd:.020,followMul:.30,\n    forwardDrive:-.018,lateralDrive:.115,chestLeanMul:.40,sideLeanMul:2.4,\n    activeHipPitchDeg:0,supportHipRollDeg:6.0,kickLeg:false\n  },\n  throw:{\n    label:"Ball Throw",shape:"attack",twistScale:.82,pelvisMul:1.10,chestMul:1.14,shoulderMul:1.28,armMul:1.48,\n    pelvisLeadAdd:.014,chestLagAdd:.004,shoulderLagAdd:.012,armLagAdd:.026,followMul:1.22,\n    forwardDrive:.045,lateralDrive:.006,chestLeanMul:1.18,sideLeanMul:.72,\n    activeHipPitchDeg:0,supportHipRollDeg:2.8,kickLeg:false\n  }\n};'''
    rep(anchor,replacement,'studio throw action profile')
    rep('''  if(/dodge|evade|sidestep|roll/.test(n))return "dodge";''',
        '''  if(/throw|capture.?ball|monster.?ball|ball.?throw|summon.?throw|quick.?throw|power.?throw/.test(n))return "throw";\n  if(/dodge|evade|sidestep|roll/.test(n))return "dodge";''','studio throw action inference')

    anchor='''  dodge:{shape:"pulse",twistScale:.22,pelvisMul:.55,chestMul:.42,shoulderMul:.28,armMul:.20,pelvisLeadAdd:0,chestLagAdd:.008,shoulderLagAdd:.015,armLagAdd:.020,followMul:.30,forwardDrive:-.018,lateralDrive:.115,chestLeanMul:.40,sideLeanMul:2.4,activeHipPitchDeg:0,supportHipRollDeg:6,kickLeg:false}\n};'''
    replacement='''  dodge:{shape:"pulse",twistScale:.22,pelvisMul:.55,chestMul:.42,shoulderMul:.28,armMul:.20,pelvisLeadAdd:0,chestLagAdd:.008,shoulderLagAdd:.015,armLagAdd:.020,followMul:.30,forwardDrive:-.018,lateralDrive:.115,chestLeanMul:.40,sideLeanMul:2.4,activeHipPitchDeg:0,supportHipRollDeg:6,kickLeg:false},\n  throw:{shape:"attack",twistScale:.82,pelvisMul:1.10,chestMul:1.14,shoulderMul:1.28,armMul:1.48,pelvisLeadAdd:.014,chestLagAdd:.004,shoulderLagAdd:.012,armLagAdd:.026,followMul:1.22,forwardDrive:.045,lateralDrive:.006,chestLeanMul:1.18,sideLeanMul:.72,activeHipPitchDeg:0,supportHipRollDeg:2.8,kickLeg:false}\n};'''
    rep(anchor,replacement,'runtime throw action profile')
    rep('''  if(/dodge|evade|sidestep|roll/.test(n))return "dodge";''',
        '''  if(/throw|capture.?ball|monster.?ball|ball.?throw|summon.?throw|quick.?throw|power.?throw/.test(n))return "throw";\n  if(/dodge|evade|sidestep|roll/.test(n))return "dodge";''','runtime throw action inference',1)

    rep('''    dodge:"Dodge Lean",hitReact:"Hit React",knockback:"Knockback",downBack:"Down / Back",faint:"Faint",interactReach:"Interact Reach",\n    attackWindup:"Attack Wind-up",attackImpact:"Attack Impact"\n  };\n  const sided=["walkContact","walkPassing","runContact","crouchStep","dodge","hitReact","knockback","interactReach","attackWindup","attackImpact"].includes(name);''',
        '''    dodge:"Dodge Lean",hitReact:"Hit React",knockback:"Knockback",downBack:"Down / Back",faint:"Faint",interactReach:"Interact Reach",\n    ballReady:"Ball Ready",ballAim:"Ball Aim",throwWindup:"Throw Wind-up",throwRelease:"Throw Release",throwFollow:"Throw Follow-through",monsterCommand:"Monster Command",\n    attackWindup:"Attack Wind-up",attackImpact:"Attack Impact"\n  };\n  const sided=["walkContact","walkPassing","runContact","crouchStep","dodge","hitReact","knockback","interactReach","ballReady","ballAim","throwWindup","throwRelease","throwFollow","monsterCommand","attackWindup","attackImpact"].includes(name);''','monster ball pose display map')

    anchor='''  if(name==="attackWindup"){\n    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),other=S("shoulderR","shoulderL");'''
    poses=r'''  if(name==="ballReady"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",2,-sgn*3,0);r("pelvis",0,sgn*1,0);r(arm,-24,0,left?-22:22);r(elbow,-74,0,left?-7:7);r(wrist,4,0,left?-10:10);r(other,4,0,left?12:-12);
    r(S("hipL","hipR"),-4,0,0);r(S("kneeL","kneeR"),10,0,0);
  }
  if(name==="ballAim"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",4,-sgn*5,0);r("pelvis",0,sgn*2,0);r(arm,-48,0,left?-15:15);r(elbow,-48,0,left?-5:5);r(wrist,-3,0,left?-8:8);r(other,7,0,left?13:-13);
    r("neck",0,sgn*2,0);r("head",-2,sgn*4,0);
  }
  if(name==="throwWindup"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",5,sgn*27,-sgn*2);r("pelvis",-2,-sgn*12,sgn*2);r(arm,44,0,left?-62:62);r(elbow,-106,0,left?-12:12);r(wrist,10,0,left?-14:14);r(other,-8,0,left?18:-18);
    r(S("hipL","hipR"),-10,0,-sgn*3);r(S("hipR","hipL"),10,0,sgn*3);r(S("kneeL","kneeR"),18,0,0);r(S("kneeR","kneeL"),10,0,0);
  }
  if(name==="throwRelease"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",-8,-sgn*18,sgn*3);r("pelvis",5,sgn*9,-sgn*2);r(arm,-78,0,left?-6:6);r(elbow,-12,0,left?-3:3);r(wrist,-10,0,left?-6:6);r(other,18,0,left?22:-22);
    r(S("hipL","hipR"),12,0,-sgn*2);r(S("hipR","hipL"),-18,0,sgn*2);r(S("kneeL","kneeR"),16,0,0);r(S("kneeR","kneeL"),30,0,0);
  }
  if(name==="throwFollow"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",10,-sgn*25,sgn*5);r("pelvis",4,sgn*12,-sgn*3);r(arm,-52,0,left?26:-26);r(elbow,-28,0,left?8:-8);r(wrist,-6,0,left?12:-12);r(other,16,0,left?18:-18);
    r(S("hipL","hipR"),16,0,-sgn*2);r(S("hipR","hipL"),-10,0,sgn*2);r(S("kneeL","kneeR"),18,0,0);r(S("kneeR","kneeL"),22,0,0);
  }
  if(name==="monsterCommand"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",3,-sgn*7,0);r("pelvis",0,sgn*3,0);r(arm,-62,0,left?-10:10);r(elbow,-10,0,left?-2:2);r(wrist,0,0,left?-4:4);r(other,8,0,left?14:-14);r("head",-2,sgn*5,0);
  }
'''+anchor
    rep(anchor,poses,'monster ball pose definitions')

    anchor='''function createAttackTemplate(){'''
    funcs=r'''function ballThrowKey(time,pose,side="R",contact={L:true,R:true},weight="both"){
  return corePackKey(time,pose,side,contact,weight);
}
function configureBallThrowClip(clip,side="R",variant="standard",mode="capture"){
  const settings={
    standard:{duration:.94,release:.56,windup:.34,follow:.72,intensity:.98,twist:32,lean:8},
    quick:{duration:.68,release:.34,windup:.20,follow:.50,intensity:.82,twist:24,lean:6},
    power:{duration:1.16,release:.68,windup:.43,follow:.91,intensity:1.10,twist:38,lean:11},
    summon:{duration:.98,release:.55,windup:.32,follow:.74,intensity:.94,twist:29,lean:7}
  }[variant]||null;
  if(!settings)return clip;
  clip.duration=settings.duration;clip.loop=false;clip.interpolation="smooth";
  clip.runtime.motionClass="action";clip.runtime.state=`${mode}_ball_throw_${side.toLowerCase()}_${variant}`;clip.runtime.motionSpeed=0;
  clip.locomotionDynamics.enabled=false;clip.footPlant.enabled=true;clip.impactProfile.enabled=false;
  Object.assign(clip.attackProfile,{
    enabled:true,side,style:"horizontal",anticipationEnd:Math.max(.06,settings.windup*.36),windupEnd:settings.windup,
    impactTime:settings.release,impactHold:.025,followThroughEnd:settings.follow,recoveryEnd:settings.duration,
    windupTwistDeg:Math.round(settings.twist*.72),swingTwistDeg:settings.twist,followThroughDeg:Math.round(settings.twist*.56),forwardLeanDeg:settings.lean
  });
  Object.assign(clip.bodyDynamics,{enabled:true,actionType:"throw",preset:"natural",intensity:settings.intensity,pelvisShare:.32,chestShare:.62,shoulderShare:.94,armShare:1.12,pelvisLead:.045,chestLag:.014,shoulderLag:.044,armLag:.074,counterRotation:.16,followThrough:.70,headStability:.86,forwardLeanShare:.42,sideLeanShare:.12});
  clip.source={kind:"monster-ball-action-pack",studioVersion:"1.8.10",mode,variant};
  return clip;
}
function createBallAimTemplate(){
  const clip=makeAnimationClip("Ball_Aim_Loop",1.6,30),a=poseSnapshotFromLibrary("ballAim","R"),b=cloneAnimationPose(a);
  if(b.shoulderR)b.shoulderR.rotation[0]-=rad(2);if(b.head)b.head.rotation[1]-=rad(1.5);
  clip.loop=true;clip.interpolation="smooth";clip.runtime.motionClass="custom";clip.runtime.state="ball_aim";clip.runtime.motionSpeed=0;
  clip.keyframes=[{time:0,joints:a,meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}},{time:.8,joints:b,meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}},{time:1.6,joints:cloneAnimationPose(a),meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}}];
  clip.locomotionDynamics.enabled=false;clip.bodyDynamics.enabled=false;clip.attackProfile.enabled=false;clip.footPlant.enabled=true;clip.source={kind:"monster-ball-action-pack",studioVersion:"1.8.10",mode:"aim"};addTemplateClip(clip);
}
function createBallThrowTemplate(side="R",variant="standard",mode="capture"){
  const names={standard:"Capture_Throw",quick:"Quick_Capture_Throw",power:"Power_Capture_Throw",summon:"Summon_Monster_Throw"};
  const clip=configureBallThrowClip(makeAnimationClip(`${names[variant]||"Ball_Throw"}_${side}_Core`,1,30),side,variant,mode);
  const s=clip.attackProfile,back=side,front=side==="R"?"L":"R",frontContact=front==="L"?{L:true,R:false}:{L:false,R:true},backContact=back==="L"?{L:true,R:false}:{L:false,R:true};
  const aimT=variant==="quick"?.08:.15,windT=s.windupEnd,releaseT=s.impactTime,followT=s.followThroughEnd,endT=s.recoveryEnd;
  clip.keyframes=[
    ballThrowKey(0,"ballReady",side,{L:true,R:true},"both"),
    ballThrowKey(aimT,"ballAim",side,{L:true,R:true},"both"),
    ballThrowKey(windT,"throwWindup",side,backContact,back),
    ballThrowKey(releaseT,"throwRelease",side,frontContact,front),
    ballThrowKey(followT,"throwFollow",side,frontContact,front),
    ballThrowKey(endT,"idle",side,{L:true,R:true},"both")
  ];
  const releasePayload={mode,variant,side,trajectory:variant==="power"?"long":variant==="summon"?"summon":"capture"};
  clip.events=[
    {id:animationId(),time:aimT,type:"ball",name:"ball.aim",socket:`hand.${side}`,payload:{mode,side}},
    {id:animationId(),time:releaseT,type:"ball",name:"ball.release",socket:`hand.${side}`,payload:releasePayload},
    {id:animationId(),time:releaseT,type:mode==="summon"?"summon":"capture",name:mode==="summon"?"monster.summon":"capture.throw",socket:`hand.${side}`,payload:releasePayload},
    {id:animationId(),time:followT,type:"action",name:"throw.follow_through",socket:"",payload:{mode,variant,side}}
  ];
  addTemplateClip(clip);
}
function createMonsterCommandTemplate(){
  const clip=makeAnimationClip("Monster_Command_Core",.82,30);clip.loop=false;clip.interpolation="smooth";clip.runtime.motionClass="custom";clip.runtime.state="monster_command";clip.runtime.motionSpeed=0;
  clip.keyframes=[corePackKey(0,"idle","R"),corePackKey(.18,"monsterCommand","R"),corePackKey(.50,"monsterCommand","R"),corePackKey(.82,"idle","R")];
  clip.locomotionDynamics.enabled=false;clip.bodyDynamics.enabled=false;clip.attackProfile.enabled=false;clip.footPlant.enabled=true;clip.source={kind:"monster-ball-action-pack",studioVersion:"1.8.10",mode:"command"};
  clip.events=[{id:animationId(),time:.38,type:"monster",name:"monster.command",socket:"hand.R",payload:{command:"forward"}}];addTemplateClip(clip);
}
'''+anchor
    rep(anchor,funcs,'monster ball animation templates')

    rep('''$("#btnTemplateInteract").onclick=createInteractTemplate;\n$("#btnTemplateAttack").onclick=createAttackTemplate;''',
        '''$("#btnTemplateInteract").onclick=createInteractTemplate;\n$("#btnTemplateBallAim").onclick=createBallAimTemplate;\n$("#btnTemplateCaptureThrowR").onclick=()=>createBallThrowTemplate("R","standard","capture");\n$("#btnTemplateCaptureThrowL").onclick=()=>createBallThrowTemplate("L","standard","capture");\n$("#btnTemplateQuickThrowR").onclick=()=>createBallThrowTemplate("R","quick","capture");\n$("#btnTemplatePowerThrowR").onclick=()=>createBallThrowTemplate("R","power","capture");\n$("#btnTemplateSummonThrowR").onclick=()=>createBallThrowTemplate("R","summon","summon");\n$("#btnTemplateMonsterCommand").onclick=createMonsterCommandTemplate;\n$("#btnTemplateAttack").onclick=createAttackTemplate;''','monster ball bindings')

    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.9"','localStorage.setItem("characterPrototypeStudio.v1.8.10"',1)
    html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.9")||',
                      'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10")||localStorage.getItem("characterPrototypeStudio.v1.8.9")||',1)
    html=html.replace('// Generated by Character Prototype Studio V1.8.9','// Generated by Character Prototype Studio V1.8.10')
    return html

if __name__=='__main__':
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
