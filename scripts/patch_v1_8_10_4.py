#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    def rep(old, new, label, count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: ' + label)
        html = html.replace(old, new, count)

    html = html.replace('Character Prototype Studio V1.8.10.3', 'Character Prototype Studio V1.8.10.4')
    html = html.replace('V1.8.10.3 · clip Reference Hotfix', 'V1.8.10.4 · Baseball Throw Motion Hotfix')
    html = html.replace('generatorVersion:"1.8.10.3"', 'generatorVersion:"1.8.10.4"')

    rep('''label:"Ball Throw",shape:"attack",twistScale:.82,pelvisMul:1.10,chestMul:1.14,shoulderMul:1.28,armMul:1.48,
    pelvisLeadAdd:.014,chestLagAdd:.004,shoulderLagAdd:.012,armLagAdd:.026,followMul:1.22,
    forwardDrive:.045,lateralDrive:.006,chestLeanMul:1.18,sideLeanMul:.72,
    activeHipPitchDeg:0,supportHipRollDeg:2.8,kickLeg:false''',
        '''label:"Ball Throw",shape:"attack",twistScale:.58,pelvisMul:.94,chestMul:1.04,shoulderMul:1.18,armMul:1.66,
    pelvisLeadAdd:.018,chestLagAdd:.006,shoulderLagAdd:.018,armLagAdd:.038,followMul:1.34,
    forwardDrive:.072,lateralDrive:.002,chestLeanMul:1.36,sideLeanMul:.28,
    activeHipPitchDeg:0,supportHipRollDeg:2.4,kickLeg:false''', 'studio overhand throw profile')

    rep('''throw:{shape:"attack",twistScale:.82,pelvisMul:1.10,chestMul:1.14,shoulderMul:1.28,armMul:1.48,pelvisLeadAdd:.014,chestLagAdd:.004,shoulderLagAdd:.012,armLagAdd:.026,followMul:1.22,forwardDrive:.045,lateralDrive:.006,chestLeanMul:1.18,sideLeanMul:.72,activeHipPitchDeg:0,supportHipRollDeg:2.8,kickLeg:false}''',
        '''throw:{shape:"attack",twistScale:.58,pelvisMul:.94,chestMul:1.04,shoulderMul:1.18,armMul:1.66,pelvisLeadAdd:.018,chestLagAdd:.006,shoulderLagAdd:.018,armLagAdd:.038,followMul:1.34,forwardDrive:.072,lateralDrive:.002,chestLeanMul:1.36,sideLeanMul:.28,activeHipPitchDeg:0,supportHipRollDeg:2.4,kickLeg:false}''', 'runtime overhand throw profile')

    old_pose = '''  if(name==="throwWindup"){
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
  }'''
    new_pose = '''  if(name==="throwWindup"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",2,sgn*22,-sgn*3);r("pelvis",-3,-sgn*9,sgn*2);r(arm,18,0,left?-34:34);r(elbow,-126,0,left?-8:8);r(wrist,18,0,left?-8:8);r(other,-12,0,left?14:-14);
    r(S("hipL","hipR"),-13,0,-sgn*2);r(S("hipR","hipL"),9,0,sgn*2);r(S("kneeL","kneeR"),20,0,0);r(S("kneeR","kneeL"),9,0,0);
  }
  if(name==="throwRelease"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",-15,-sgn*14,sgn*2);r("pelvis",7,sgn*7,-sgn*1);r(arm,-118,0,left?-4:4);r(elbow,-18,0,left?-2:2);r(wrist,-18,0,left?-3:3);r(other,24,0,left?16:-16);
    r(S("hipL","hipR"),15,0,-sgn*1);r(S("hipR","hipL"),-22,0,sgn*1);r(S("kneeL","kneeR"),18,0,0);r(S("kneeR","kneeL"),34,0,0);
  }
  if(name==="throwFollow"){
    const arm=S("shoulderL","shoulderR"),elbow=S("elbowL","elbowR"),wrist=S("wristL","wristR"),other=S("shoulderR","shoulderL");
    r("chest",16,-sgn*18,sgn*4);r("pelvis",6,sgn*9,-sgn*2);r(arm,-76,0,left?30:-30);r(elbow,-34,0,left?6:-6);r(wrist,-12,0,left?10:-10);r(other,18,0,left?14:-14);
    r(S("hipL","hipR"),18,0,-sgn*1);r(S("hipR","hipL"),-12,0,sgn*1);r(S("kneeL","kneeR"),20,0,0);r(S("kneeR","kneeL"),24,0,0);
  }'''
    rep(old_pose, new_pose, 'baseball overhand pose chain')

    rep('''enabled:true,side,style:"horizontal",anticipationEnd:Math.max(.06,settings.windup*.36),windupEnd:settings.windup,
    impactTime:settings.release,impactHold:.025,followThroughEnd:settings.follow,recoveryEnd:settings.duration,
    windupTwistDeg:Math.round(settings.twist*.72),swingTwistDeg:settings.twist,followThroughDeg:Math.round(settings.twist*.56),forwardLeanDeg:settings.lean''',
        '''enabled:true,side,style:"overhead",anticipationEnd:Math.max(.06,settings.windup*.36),windupEnd:settings.windup,
    impactTime:settings.release,impactHold:.025,followThroughEnd:settings.follow,recoveryEnd:settings.duration,
    windupTwistDeg:Math.round(settings.twist*.58),swingTwistDeg:Math.round(settings.twist*.82),followThroughDeg:Math.round(settings.twist*.50),forwardLeanDeg:settings.lean,
    shoulderDriveDeg:30,wristFollowDeg:18''', 'throw attack profile overhead style')

    rep('''Object.assign(clip.bodyDynamics,{enabled:true,actionType:"throw",preset:"natural",intensity:settings.intensity,pelvisShare:.32,chestShare:.62,shoulderShare:.94,armShare:1.12,pelvisLead:.045,chestLag:.014,shoulderLag:.044,armLag:.074,counterRotation:.16,followThrough:.70,headStability:.86,forwardLeanShare:.42,sideLeanShare:.12});''',
        '''Object.assign(clip.bodyDynamics,{enabled:true,actionType:"throw",preset:"natural",intensity:settings.intensity,pelvisShare:.28,chestShare:.56,shoulderShare:.88,armShare:1.20,pelvisLead:.050,chestLag:.016,shoulderLag:.050,armLag:.082,counterRotation:.12,followThrough:.78,headStability:.88,forwardLeanShare:.52,sideLeanShare:.06});''', 'throw kinetic timing')

    rep('''clip.source={kind:"monster-ball-action-pack",studioVersion:"1.8.10",mode,variant};''',
        '''clip.source={kind:"monster-ball-action-pack",studioVersion:"1.8.10.4",mode,variant,throwStyle:"overhand-baseball"};''', 'throw style metadata')

    html = html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.10.3"', 'localStorage.setItem("characterPrototypeStudio.v1.8.10.4"', 1)
    html = html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10.3")||', 'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10.4")||localStorage.getItem("characterPrototypeStudio.v1.8.10.3")||', 1)
    return html


if __name__ == '__main__':
    import sys
    p = Path(sys.argv[1])
    p.write_text(patch(p.read_text(encoding='utf-8')), encoding='utf-8')
