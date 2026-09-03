#!/usr/bin/env python3
from pathlib import Path

def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)
    html=html.replace('Character Prototype Studio V1.8.7','Character Prototype Studio V1.8.8')
    html=html.replace('V1.8.7 · Foot Plant + Leg Response','V1.8.8 · Core Movement Animation Pack')
    html=html.replace('generatorVersion:"1.8.7"','generatorVersion:"1.8.8"')

    rep('''          <button class="btn" data-librarypose="runContact">Run Contact</button>\n          <button class="btn" data-librarypose="attackWindup">Attack Wind-up</button>''',
        '''          <button class="btn" data-librarypose="runContact">Run Contact</button>\n          <button class="btn" data-librarypose="jumpTakeoff">Jump Takeoff</button>\n          <button class="btn" data-librarypose="jumpAir">Jump Air</button>\n          <button class="btn" data-librarypose="fall">Fall</button>\n          <button class="btn" data-librarypose="land">Land</button>\n          <button class="btn" data-librarypose="crouch">Crouch</button>\n          <button class="btn" data-librarypose="crouchStep">Crouch Step</button>\n          <button class="btn" data-librarypose="attackWindup">Attack Wind-up</button>''','pose library core movement buttons')

    rep('''            <button class="btn" id="btnTemplateTurn">Turn R</button>\n            <button class="btn" id="btnTemplateStrafe">Strafe R</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>''',
        '''            <button class="btn" id="btnTemplateTurn">Turn R</button>\n            <button class="btn" id="btnTemplateTurnL">Turn L</button>\n            <button class="btn" id="btnTemplateStrafe">Strafe R</button>\n            <button class="btn" id="btnTemplateStrafeL">Strafe L</button>\n            <button class="btn" id="btnTemplateJump">Jump</button>\n            <button class="btn" id="btnTemplateFall">Fall Loop</button>\n            <button class="btn" id="btnTemplateLand">Land</button>\n            <button class="btn" id="btnTemplateCrouch">Crouch Idle</button>\n            <button class="btn" id="btnTemplateCrouchWalk">Crouch Walk</button>\n            <button class="btn" id="btnTemplateAttack">Attack 4-Key</button>''','animation library core movement buttons')
    html=html.replace('Library อยู่บนสุดของ Anim tab · V1.8.6 เพิ่ม Sprint / Start / Stop / Turn / Strafe โดยไม่เปลี่ยน Action Library',
                      'Core Movement Pack · Walk / Run / Sprint / Start / Stop / Turn L-R / Strafe L-R / Jump / Fall / Land / Crouch · Weapon ยังไม่เริ่ม',1)

    rep('''    walkContact:"Walk Contact",walkPassing:"Walk Passing",runContact:"Run Contact",\n    attackWindup:"Attack Wind-up",attackImpact:"Attack Impact"\n  };\n  const sided=["walkContact","walkPassing","runContact","attackWindup","attackImpact"].includes(name);''',
        '''    walkContact:"Walk Contact",walkPassing:"Walk Passing",runContact:"Run Contact",\n    jumpTakeoff:"Jump Takeoff",jumpAir:"Jump Air",fall:"Fall",land:"Land",crouch:"Crouch",crouchStep:"Crouch Step",\n    attackWindup:"Attack Wind-up",attackImpact:"Attack Impact"\n  };\n  const sided=["walkContact","walkPassing","runContact","crouchStep","attackWindup","attackImpact"].includes(name);''','pose display map')

    anchor='''  if(name==="attackWindup"){\n    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),other=S("shoulderR","shoulderL");'''
    poses=r'''  if(name==="jumpTakeoff"){
    r("chest",9,0,0);r("pelvis",-4,0,0);
    r("hipL",-34,0,-2);r("hipR",-34,0,2);r("kneeL",72,0,0);r("kneeR",72,0,0);
    r("ankleL",-16,0,0);r("ankleR",-16,0,0);
    r("shoulderL",-30,0,-18);r("shoulderR",-30,0,18);r("elbowL",-28,0,-8);r("elbowR",-28,0,8);
  }
  if(name==="jumpAir"){
    r("chest",-5,0,0);r("pelvis",3,0,0);
    r("hipL",22,0,-3);r("hipR",12,0,3);r("kneeL",56,0,0);r("kneeR",48,0,0);
    r("ankleL",-18,0,0);r("ankleR",-16,0,0);
    r("shoulderL",42,0,-28);r("shoulderR",42,0,28);r("elbowL",-42,0,-10);r("elbowR",-42,0,10);
  }
  if(name==="fall"){
    r("chest",-8,0,0);r("pelvis",2,0,0);
    r("hipL",8,0,-4);r("hipR",8,0,4);r("kneeL",28,0,0);r("kneeR",28,0,0);
    r("ankleL",-8,0,0);r("ankleR",-8,0,0);
    r("shoulderL",18,0,-52);r("shoulderR",18,0,52);r("elbowL",-28,0,-12);r("elbowR",-28,0,12);
  }
  if(name==="land"){
    r("chest",16,0,0);r("pelvis",-5,0,0);
    r("hipL",-38,0,-4);r("hipR",-38,0,4);r("kneeL",92,0,0);r("kneeR",92,0,0);
    r("ankleL",20,0,0);r("ankleR",20,0,0);
    r("shoulderL",-24,0,-22);r("shoulderR",-24,0,22);r("elbowL",-36,0,-8);r("elbowR",-36,0,8);
  }
  if(name==="crouch"){
    r("chest",10,0,0);r("pelvis",-3,0,0);
    r("hipL",-34,0,-2);r("hipR",-34,0,2);r("kneeL",78,0,0);r("kneeR",78,0,0);
    r("ankleL",18,0,0);r("ankleR",18,0,0);
    r("shoulderL",8,0,-14);r("shoulderR",8,0,14);r("elbowL",-20,0,-8);r("elbowR",-20,0,8);
  }
  if(name==="crouchStep"){
    r("chest",10,sgn*2,0);r("pelvis",-3,-sgn*2,0);
    r(S("hipL","hipR"),-45,0,-sgn*2);r(S("hipR","hipL"),-22,0,sgn*2);
    r(S("kneeL","kneeR"),88,0,0);r(S("kneeR","kneeL"),62,0,0);
    r(S("ankleL","ankleR"),20,0,0);r(S("ankleR","ankleL"),12,0,0);
    r(S("shoulderL","shoulderR"),16,0,left?-14:14);r(S("shoulderR","shoulderL"),-8,0,left?14:-14);
    r("elbowL",-24,0,-8);r("elbowR",-24,0,8);
  }
'''+anchor
    rep(anchor,poses,'core movement pose definitions')

    rep('''    if(k.pose==="walkContact"||k.pose==="runContact"){\n      contact=side==="L"?{L:true,R:false}:{L:false,R:true};weight=side;\n    }else if(k.pose==="walkPassing"){\n      const stance=side==="L"?"L":"R";contact=stance==="L"?{L:true,R:false}:{L:false,R:true};weight=stance;\n    }else if(k.pose==="idle"){\n      contact={L:true,R:true};weight="both";\n    }''',
        '''    if(k.pose==="walkContact"||k.pose==="runContact"||k.pose==="crouchStep"){\n      contact=side==="L"?{L:true,R:false}:{L:false,R:true};weight=side;\n    }else if(k.pose==="walkPassing"){\n      const stance=side==="L"?"L":"R";contact=stance==="L"?{L:true,R:false}:{L:false,R:true};weight=stance;\n    }else if(["idle","crouch","jumpTakeoff","land"].includes(k.pose)){\n      contact={L:true,R:true};weight="both";\n    }else if(["jumpAir","fall"].includes(k.pose)){\n      contact={L:false,R:false};weight="air";\n    }''','core movement contact metadata')

    anchor='''function createAttackTemplate(){'''
    funcs=r'''function createTurnLeftTemplate(){
  const clip=createTemplateClip("Turn_L_PoseLibrary",1.0,30,[{time:0,pose:"walkContact",side:"R"},{time:.25,pose:"walkPassing",side:"R"},{time:.5,pose:"walkContact",side:"L"},{time:.75,pose:"walkPassing",side:"L"},{time:1,pose:"walkContact",side:"R"}],true,"smooth");
  clip.runtime.motionClass="walk";clip.runtime.motionSpeed=1.4;clip.locomotionDynamics.mode="turn";clip.locomotionDynamics.direction="L";addTemplateClip(clip);
}
function createStrafeLeftTemplate(){
  const clip=createTemplateClip("Strafe_L_PoseLibrary",.95,30,[{time:0,pose:"walkContact",side:"R"},{time:.24,pose:"walkPassing",side:"R"},{time:.48,pose:"walkContact",side:"L"},{time:.72,pose:"walkPassing",side:"L"},{time:.95,pose:"walkContact",side:"R"}],true,"smooth");
  clip.runtime.motionClass="walk";clip.runtime.motionSpeed=1.6;clip.locomotionDynamics.mode="strafe";clip.locomotionDynamics.direction="L";addTemplateClip(clip);
}
function createJumpTemplate(){
  const clip=createTemplateClip("Jump_Core",1.08,30,[
    {time:0,pose:"idle"},{time:.16,pose:"jumpTakeoff"},{time:.36,pose:"jumpAir"},
    {time:.66,pose:"fall"},{time:.88,pose:"land"},{time:1.08,pose:"idle"}
  ],false,"smooth");
  clip.runtime.motionClass="custom";clip.runtime.state="jump";clip.runtime.motionSpeed=0;
  clip.locomotionDynamics.enabled=false;clip.footPlant.enabled=true;clip.source={kind:"core-movement-pack",studioVersion:"1.8.8"};addTemplateClip(clip);
}
function createFallTemplate(){
  const clip=createTemplateClip("Fall_Loop_Core",1.0,30,[
    {time:0,pose:"fall"},{time:.5,pose:"jumpAir"},{time:1,pose:"fall"}
  ],true,"smooth");
  clip.runtime.motionClass="custom";clip.runtime.state="fall";clip.runtime.motionSpeed=0;
  clip.locomotionDynamics.enabled=false;clip.footPlant.enabled=false;clip.source={kind:"core-movement-pack",studioVersion:"1.8.8"};addTemplateClip(clip);
}
function createLandTemplate(){
  const clip=createTemplateClip("Land_Core",.72,30,[
    {time:0,pose:"fall"},{time:.12,pose:"land"},{time:.38,pose:"crouch"},{time:.72,pose:"idle"}
  ],false,"smooth");
  clip.runtime.motionClass="custom";clip.runtime.state="land";clip.runtime.motionSpeed=0;
  clip.locomotionDynamics.enabled=false;clip.footPlant.enabled=true;clip.source={kind:"core-movement-pack",studioVersion:"1.8.8"};addTemplateClip(clip);
}
function createCrouchTemplate(){
  const a=poseSnapshotFromLibrary("crouch","L"),b=cloneAnimationPose(a);
  if(b.chest)b.chest.rotation[0]+=rad(1.2);if(b.head)b.head.rotation[0]-=rad(.6);
  const clip=makeAnimationClip("Crouch_Idle_Core",1.8,30);clip.loop=true;clip.interpolation="smooth";
  clip.keyframes=[
    {time:0,joints:a,meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}},
    {time:.9,joints:b,meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}},
    {time:1.8,joints:cloneAnimationPose(a),meta:{contact:{L:true,R:true},weight:"both",weightValue:{L:.5,R:.5}}}
  ];
  clip.runtime.motionClass="custom";clip.runtime.state="crouch_idle";clip.locomotionDynamics.enabled=false;clip.footPlant.enabled=true;clip.source={kind:"core-movement-pack",studioVersion:"1.8.8"};addTemplateClip(clip);
}
function createCrouchWalkTemplate(){
  const clip=createTemplateClip("Crouch_Walk_Core",1.15,30,[
    {time:0,pose:"crouchStep",side:"L"},{time:.2875,pose:"crouch",side:"L"},
    {time:.575,pose:"crouchStep",side:"R"},{time:.8625,pose:"crouch",side:"R"},
    {time:1.15,pose:"crouchStep",side:"L"}
  ],true,"smooth");
  clip.runtime.motionClass="custom";clip.runtime.state="crouch_walk";clip.runtime.motionSpeed=.85;
  clip.locomotionDynamics.enabled=false;clip.footPlant.enabled=true;clip.source={kind:"core-movement-pack",studioVersion:"1.8.8"};addTemplateClip(clip);
}
'''+anchor
    rep(anchor,funcs,'core movement template functions')

    rep('''$("#btnTemplateTurn").onclick=createTurnTemplate;\n$("#btnTemplateStrafe").onclick=createStrafeTemplate;\n$("#btnTemplateAttack").onclick=createAttackTemplate;''',
        '''$("#btnTemplateTurn").onclick=createTurnTemplate;\n$("#btnTemplateTurnL").onclick=createTurnLeftTemplate;\n$("#btnTemplateStrafe").onclick=createStrafeTemplate;\n$("#btnTemplateStrafeL").onclick=createStrafeLeftTemplate;\n$("#btnTemplateJump").onclick=createJumpTemplate;\n$("#btnTemplateFall").onclick=createFallTemplate;\n$("#btnTemplateLand").onclick=createLandTemplate;\n$("#btnTemplateCrouch").onclick=createCrouchTemplate;\n$("#btnTemplateCrouchWalk").onclick=createCrouchWalkTemplate;\n$("#btnTemplateAttack").onclick=createAttackTemplate;''','core movement bindings')

    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.7"', 'localStorage.setItem("characterPrototypeStudio.v1.8.8"',1)
    html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.7")||',
                      'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.8")||localStorage.getItem("characterPrototypeStudio.v1.8.7")||',1)
    html=html.replace('// Generated by Character Prototype Studio V1.8.7','// Generated by Character Prototype Studio V1.8.8')
    return html

if __name__=="__main__":
    import sys
    p=Path(sys.argv[1])
    p.write_text(patch(p.read_text(encoding="utf-8")),encoding="utf-8")
