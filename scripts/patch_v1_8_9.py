#!/usr/bin/env python3
from pathlib import Path

def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)

    html=html.replace('Character Prototype Studio V1.8.8','Character Prototype Studio V1.8.9')
    html=html.replace('V1.8.8 · Core Movement Animation Pack','V1.8.9 · Core Action / Reaction Pack')
    html=html.replace('generatorVersion:"1.8.8"','generatorVersion:"1.8.9"')

    rep('''          <button class="btn" data-librarypose="crouchStep">Crouch Step</button>\n          <button class="btn" data-librarypose="attackWindup">Attack Wind-up</button>''',
        '''          <button class="btn" data-librarypose="crouchStep">Crouch Step</button>\n          <button class="btn" data-librarypose="dodge">Dodge Lean</button>\n          <button class="btn" data-librarypose="hitReact">Hit React</button>\n          <button class="btn" data-librarypose="knockback">Knockback</button>\n          <button class="btn" data-librarypose="downBack">Down / Back</button>\n          <button class="btn" data-librarypose="faint">Faint</button>\n          <button class="btn" data-librarypose="interactReach">Interact Reach</button>\n          <button class="btn" data-librarypose="attackWindup">Attack Wind-up</button>''','pose library action reaction buttons')

    rep('''            <button class="btn" id="btnTemplateCrouchWalk">Crouch Walk</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>''',
        '''            <button class="btn" id="btnTemplateCrouchWalk">Crouch Walk</button>\n            <button class="btn" id="btnTemplateDodgeR">Dodge R</button>\n            <button class="btn" id="btnTemplateDodgeL">Dodge L</button>\n            <button class="btn" id="btnTemplateHitReact">Hit React</button>\n            <button class="btn" id="btnTemplateKnockback">Knockback</button>\n            <button class="btn" id="btnTemplateGetUp">Get Up</button>\n            <button class="btn" id="btnTemplateDeath">Death</button>\n            <button class="btn" id="btnTemplateFaint">Faint</button>\n            <button class="btn" id="btnTemplateInteract">Interact</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>''','animation library action reaction buttons')
    html=html.replace('Core Movement Pack · Walk / Run / Sprint / Start / Stop / Turn L-R / Strafe L-R / Jump / Fall / Land / Crouch · Weapon ยังไม่เริ่ม',
                      'Core Animation Pack · Movement + Dodge L/R + Hit + Knockback + Get Up + Death/Faint + Interact · Weapon ยังไม่เริ่ม',1)

    rep('''    jumpTakeoff:"Jump Takeoff",jumpAir:"Jump Air",fall:"Fall",land:"Land",crouch:"Crouch",crouchStep:"Crouch Step",\n    attackWindup:"Attack Wind-up",attackImpact:"Attack Impact"\n  };\n  const sided=["walkContact","walkPassing","runContact","crouchStep","attackWindup","attackImpact"].includes(name);''',
        '''    jumpTakeoff:"Jump Takeoff",jumpAir:"Jump Air",fall:"Fall",land:"Land",crouch:"Crouch",crouchStep:"Crouch Step",\n    dodge:"Dodge Lean",hitReact:"Hit React",knockback:"Knockback",downBack:"Down / Back",faint:"Faint",interactReach:"Interact Reach",\n    attackWindup:"Attack Wind-up",attackImpact:"Attack Impact"\n  };\n  const sided=["walkContact","walkPassing","runContact","crouchStep","dodge","hitReact","knockback","interactReach","attackWindup","attackImpact"].includes(name);''','pose display action reaction map')

    anchor='''  if(name==="attackWindup"){\n    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),other=S("shoulderR","shoulderL");'''
    poses=r'''  if(name==="dodge"){
    r("chest",7,-sgn*5,-sgn*15);r("pelvis",-2,sgn*3,-sgn*8);
    r(S("hipL","hipR"),-28,0,-sgn*8);r(S("hipR","hipL"),6,0,sgn*4);
    r(S("kneeL","kneeR"),62,0,0);r(S("kneeR","kneeL"),28,0,0);
    r(S("ankleL","ankleR"),16,0,-sgn*5);r(S("ankleR","ankleL"),-8,0,sgn*3);
    r(S("shoulderL","shoulderR"),16,0,left?-28:28);r(S("shoulderR","shoulderL"),-20,0,left?24:-24);
    r("elbowL",-34,0,-8);r("elbowR",-34,0,8);
  }
  if(name==="hitReact"){
    r("chest",-18,sgn*10,-sgn*6);r("pelvis",5,-sgn*4,sgn*3);r("neck",8,-sgn*4,0);r("head",12,-sgn*8,sgn*3);
    r(S("shoulderL","shoulderR"),-32,0,left?-34:34);r(S("shoulderR","shoulderL"),20,0,left?26:-26);
    r(S("elbowL","elbowR"),-58,0,left?-8:8);r(S("elbowR","elbowL"),-30,0,left?8:-8);
    r(S("hipL","hipR"),8,0,-sgn*2);r(S("hipR","hipL"),-10,0,sgn*2);r("kneeL",16,0,0);r("kneeR",20,0,0);
  }
  if(name==="knockback"){
    r("chest",-26,sgn*8,-sgn*5);r("pelvis",10,-sgn*4,sgn*3);r("neck",12,0,0);r("head",18,-sgn*4,0);
    r("shoulderL",-38,0,-42);r("shoulderR",-38,0,42);r("elbowL",-44,0,-12);r("elbowR",-44,0,12);
    r(S("hipL","hipR"),16,0,-sgn*4);r(S("hipR","hipL"),-28,0,sgn*4);r(S("kneeL","kneeR"),28,0,0);r(S("kneeR","kneeL"),54,0,0);
    if(J.pelvis)J.pelvis.position.z+=.055;
  }
  if(name==="downBack"){
    r("pelvis",72,0,8);r("chest",24,-8,-6);r("neck",-10,4,0);r("head",-16,6,4);
    r("hipL",20,0,-18);r("hipR",28,0,14);r("kneeL",62,0,0);r("kneeR",44,0,0);
    r("ankleL",-14,0,-8);r("ankleR",-10,0,8);
    r("shoulderL",-28,0,-62);r("shoulderR",-12,0,48);r("elbowL",-34,0,-12);r("elbowR",-48,0,14);
    if(J.pelvis)J.pelvis.position.y-=.34;
  }
  if(name==="faint"){
    r("chest",30,-8,7);r("pelvis",-12,5,-5);r("neck",20,4,0);r("head",28,6,-5);
    r("hipL",-42,0,-7);r("hipR",-32,0,6);r("kneeL",108,0,0);r("kneeR",92,0,0);
    r("ankleL",22,0,-7);r("ankleR",18,0,5);
    r("shoulderL",22,0,-48);r("shoulderR",8,0,36);r("elbowL",-54,0,-12);r("elbowR",-42,0,10);
    if(J.pelvis)J.pelvis.position.y-=.18;
  }
  if(name==="interactReach"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",4,-sgn*6,0);r("pelvis",0,sgn*2,0);r(arm,-52,0,left?-10:10);r(elbow,-18,0,left?-4:4);r(wrist,0,0,left?-8:8);r(other,8,0,left?12:-12);
    r(S("hipL","hipR"),-8,0,0);r(S("kneeL","kneeR"),14,0,0);
  }
'''+anchor
    rep(anchor,poses,'action reaction pose definitions')

    anchor='''function createAttackTemplate(){'''
    funcs=r'''function corePackKey(time,pose,side="R",contact={L:true,R:true},weight="both"){
  const weightValue=weight==="L"?{L:.92,R:.08}:weight==="R"?{L:.08,R:.92}:{L:.5,R:.5};
  return {time,joints:poseSnapshotFromLibrary(pose,side),meta:{contact:{L:!!contact.L,R:!!contact.R},weight,weightValue}};
}
function finalizeCoreReactionClip(clip,state,{loop=false,footPlant=false,impact=false}={}){
  clip.loop=loop;clip.interpolation="smooth";clip.runtime.motionClass="custom";clip.runtime.state=state;clip.runtime.motionSpeed=0;
  clip.locomotionDynamics.enabled=false;clip.bodyDynamics.enabled=false;clip.attackProfile.enabled=false;clip.footPlant.enabled=footPlant;
  clip.source={kind:"core-action-reaction-pack",studioVersion:"1.8.9"};
  if(!impact)clip.impactProfile.enabled=false;
  return clip;
}
function createDodgeCoreTemplate(side="R"){
  const support=side==="R"?"L":"R",clip=makeAnimationClip(`Dodge_${side}_Core`,.72,30);
  clip.loop=false;clip.interpolation="smooth";clip.runtime.motionClass="action";clip.runtime.state=`dodge_${side.toLowerCase()}`;clip.runtime.motionSpeed=0;
  clip.keyframes=[
    corePackKey(0,"idle",side,{L:true,R:true},"both"),
    corePackKey(.12,"crouchStep",support,support==="L"?{L:true,R:false}:{L:false,R:true},support),
    corePackKey(.34,"dodge",side,{L:false,R:false},"air"),
    corePackKey(.52,"crouchStep",side,side==="L"?{L:true,R:false}:{L:false,R:true},side),
    corePackKey(.72,"idle",side,{L:true,R:true},"both")
  ];
  clip.locomotionDynamics.enabled=false;clip.footPlant.enabled=false;clip.attackProfile.enabled=false;clip.impactProfile.enabled=false;
  Object.assign(clip.bodyDynamics,{enabled:true,actionType:"dodge",intensity:.92,sideLeanShare:.20,headStability:.88});
  clip.attackProfile.side=side;clip.source={kind:"core-action-reaction-pack",studioVersion:"1.8.9"};
  clip.events=[
    {id:animationId(),time:.12,type:"action",name:"dodge.start",socket:"",payload:{side}},
    {id:animationId(),time:.54,type:"action",name:"dodge.recover",socket:"",payload:{side}}
  ];addTemplateClip(clip);
}
function createHitReactTemplate(){
  const clip=finalizeCoreReactionClip(makeAnimationClip("Hit_React_Core",.56,30),"hit_react",{footPlant:true,impact:true});
  clip.keyframes=[corePackKey(0,"idle"),corePackKey(.10,"hitReact","R"),corePackKey(.27,"hitReact","L"),corePackKey(.56,"idle")];
  clip.impactMarkers=[{id:animationId(),time:.10,type:"hit",strength:.72,generatedFrom:"core-action-reaction-pack"}];
  Object.assign(clip.impactProfile,{enabled:true,anticipation:.02,compressionTime:.10,recovery:.30,pelvisCompression:.022,kneeCompressionDeg:8,chestRecoilDeg:7,headLagDeg:5,hitStrength:.78,maxCombined:1.15});addTemplateClip(clip);
}
function createKnockbackTemplate(){
  const clip=finalizeCoreReactionClip(makeAnimationClip("Knockback_Core",.82,30),"knockback",{footPlant:false,impact:true});
  clip.keyframes=[corePackKey(0,"idle"),corePackKey(.10,"hitReact","R"),corePackKey(.30,"knockback","R",{L:false,R:false},"air"),corePackKey(.58,"crouch", "R",{L:true,R:true},"both"),corePackKey(.82,"idle")];
  clip.impactMarkers=[{id:animationId(),time:.10,type:"hit",strength:1.08,generatedFrom:"core-action-reaction-pack"}];
  Object.assign(clip.impactProfile,{enabled:true,anticipation:.02,compressionTime:.16,recovery:.42,pelvisCompression:.030,kneeCompressionDeg:11,chestRecoilDeg:13,headLagDeg:8,hitStrength:1.12,maxCombined:1.45});addTemplateClip(clip);
}
function createGetUpTemplate(){
  const clip=finalizeCoreReactionClip(makeAnimationClip("Get_Up_Core",1.20,30),"get_up",{footPlant:false});
  clip.keyframes=[corePackKey(0,"downBack","R",{L:false,R:false},"air"),corePackKey(.36,"faint","R",{L:true,R:true},"both"),corePackKey(.72,"crouch","R",{L:true,R:true},"both"),corePackKey(1.0,"jumpTakeoff","R",{L:true,R:true},"both"),corePackKey(1.20,"idle","R",{L:true,R:true},"both")];
  clip.events=[{id:animationId(),time:1.0,type:"state",name:"get_up.ready",socket:"",payload:null}];addTemplateClip(clip);
}
function createDeathTemplate(){
  const clip=finalizeCoreReactionClip(makeAnimationClip("Death_Core",1.05,30),"death",{footPlant:false});
  clip.keyframes=[corePackKey(0,"idle"),corePackKey(.18,"hitReact","R"),corePackKey(.48,"knockback","R",{L:false,R:false},"air"),corePackKey(.80,"downBack","R",{L:false,R:false},"air"),corePackKey(1.05,"downBack","R",{L:false,R:false},"air")];
  clip.events=[{id:animationId(),time:.80,type:"state",name:"death.settled",socket:"",payload:null}];addTemplateClip(clip);
}
function createFaintTemplate(){
  const clip=finalizeCoreReactionClip(makeAnimationClip("Faint_Core",.92,30),"faint",{footPlant:false});
  clip.keyframes=[corePackKey(0,"idle"),corePackKey(.20,"crouch","R",{L:true,R:true},"both"),corePackKey(.54,"faint","R",{L:true,R:true},"both"),corePackKey(.92,"faint","R",{L:true,R:true},"both")];
  clip.events=[{id:animationId(),time:.54,type:"state",name:"faint.settled",socket:"",payload:null}];addTemplateClip(clip);
}
function createInteractTemplate(){
  const clip=finalizeCoreReactionClip(makeAnimationClip("Interact_Core",.86,30),"interact",{footPlant:true});
  clip.keyframes=[corePackKey(0,"idle","R"),corePackKey(.18,"interactReach","R"),corePackKey(.46,"interactReach","R"),corePackKey(.68,"idle","R"),corePackKey(.86,"idle","R")];
  clip.events=[{id:animationId(),time:.46,type:"interact",name:"interact.commit",socket:"hand.R",payload:null}];addTemplateClip(clip);
}
'''+anchor
    rep(anchor,funcs,'core action reaction templates')

    rep('''$("#btnTemplateCrouchWalk").onclick=createCrouchWalkTemplate;\n$("#btnTemplateAttack").onclick=createAttackTemplate;''',
        '''$("#btnTemplateCrouchWalk").onclick=createCrouchWalkTemplate;\n$("#btnTemplateDodgeR").onclick=()=>createDodgeCoreTemplate("R");\n$("#btnTemplateDodgeL").onclick=()=>createDodgeCoreTemplate("L");\n$("#btnTemplateHitReact").onclick=createHitReactTemplate;\n$("#btnTemplateKnockback").onclick=createKnockbackTemplate;\n$("#btnTemplateGetUp").onclick=createGetUpTemplate;\n$("#btnTemplateDeath").onclick=createDeathTemplate;\n$("#btnTemplateFaint").onclick=createFaintTemplate;\n$("#btnTemplateInteract").onclick=createInteractTemplate;\n$("#btnTemplateAttack").onclick=createAttackTemplate;''','core action reaction bindings')

    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.8"','localStorage.setItem("characterPrototypeStudio.v1.8.9"',1)
    html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.8")||',
                      'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.9")||localStorage.getItem("characterPrototypeStudio.v1.8.8")||',1)
    html=html.replace('// Generated by Character Prototype Studio V1.8.8','// Generated by Character Prototype Studio V1.8.9')
    return html

if __name__=='__main__':
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
