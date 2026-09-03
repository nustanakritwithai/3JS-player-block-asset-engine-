#!/usr/bin/env python3


def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)

    html=html.replace('Character Prototype Studio V1.8.5.2','Character Prototype Studio V1.8.5.3')
    html=html.replace('V1.8.5.2 · Twist Isolation + Animation Library Restore',
                      'V1.8.5.3 · Walk Pelvis Translation Hotfix')
    html=html.replace('generatorVersion:"1.8.5.2"','generatorVersion:"1.8.5.3"')

    rep('''    clip:"walk",speed:1.0,hipSwing:34,kneeLift:52,armSwing:38,\n    pelvisShift:.028,pelvisBob:.040,pelvisTwist:3.5,chestTwist:5.5,\n    compression:.020,headStabilization:true,showContacts:true,\n    tuningVersion:"1.8.1"''','''    clip:"walk",speed:1.0,hipSwing:34,kneeLift:52,armSwing:38,\n    pelvisShift:.014,pelvisBob:.040,pelvisTwist:3.5,chestTwist:5.5,\n    compression:.020,headStabilization:true,showContacts:true,\n    tuningVersion:"1.8.5.3"''','default natural walk lateral translation')

    rep('''      lateralInfluence:.32,maxShift:.075,hipDropDeg:2.5,twistDeg:4,\n      compression:.020,comGain:.26,comMaxCorrection:.05,smoothing:.78,\n      lateralResponse:.55,dominanceDeadZone:.08,responsePower:1.25,\n      tuningVersion:"1.8.1"''','''      lateralInfluence:.32,maxShift:.075,walkVisualShiftCap:.016,hipDropDeg:2.5,twistDeg:4,\n      compression:.020,comGain:.26,comMaxCorrection:.05,smoothing:.78,\n      lateralResponse:.55,dominanceDeadZone:.08,responsePower:1.25,\n      tuningVersion:"1.8.5.3"''','default walk visual cap')

    rep('''    const lateralWave=-s;\n    const lateralEase=lateralWave*Math.pow(Math.abs(lateralWave),.18);\n    joints.pelvis.position.x=pelvisBase.pos[0]+lateralEase*c.pelvisShift;''','''    const lateralWave=-s;\n    const lateralEase=lateralWave*Math.pow(Math.abs(lateralWave),.18);\n    // V1.8.5.3: keep gait weight/phase truth, but decouple it from excessive visible hip translation.\n    // Walk gets a visual-only cap; Run remains untouched for the dedicated V1.8.6 locomotion pass.\n    const walkVisualCap=spec.weight?.pelvisSolver?.walkVisualShiftCap??.016;\n    const visualPelvisShift=c.clip==="walk"?Math.min(Math.max(0,Number(c.pelvisShift)||0),walkVisualCap):Math.max(0,Number(c.pelvisShift)||0);\n    joints.pelvis.position.x=pelvisBase.pos[0]+lateralEase*visualPelvisShift;''','procedural walk visual translation cap')

    rep('''    maxShift:clamp(Number(s.maxShift)||0,0,.5),\n    hipDropDeg:clamp(Number(s.hipDropDeg)||0,0,20),''','''    maxShift:clamp(Number(s.maxShift)||0,0,.5),\n    walkVisualShiftCap:clamp(Number(s.walkVisualShiftCap??.016),0,.08),\n    hipDropDeg:clamp(Number(s.hipDropDeg)||0,0,20),''','pelvis solver config walk cap')

    rep('''  const maxShift=s.maxShift??.075;\n  const coupling=s.lateralResponse??.55;\n  const visualDominance=dominance*coupling;\n  p.position.x+=clamp(visualDominance*maxShift*(s.lateralInfluence??.32),-maxShift,maxShift);''','''  const maxShift=s.maxShift??.075;\n  const coupling=s.lateralResponse??.55;\n  const visualDominance=dominance*coupling;\n  const visualShiftLimit=clip.runtime?.motionClass==="walk"?Math.min(maxShift,s.walkVisualShiftCap??.016):maxShift;\n  p.position.x+=clamp(visualDominance*maxShift*(s.lateralInfluence??.32),-visualShiftLimit,visualShiftLimit);''','game runtime walk visual cap')

    rep('''  let comCorrection=clamp(comErrorX*cfg.comGain*feedbackScale,-cfg.comMaxCorrection,cfg.comMaxCorrection);\n  let shiftX=clamp(targetDeltaX+comCorrection,-cfg.maxShift,cfg.maxShift);''','''  let comCorrection=clamp(comErrorX*cfg.comGain*feedbackScale,-cfg.comMaxCorrection,cfg.comMaxCorrection);\n  // COM correction remains fully computed for balance truth/QA. Only the rendered Walk pelvis translation is capped.\n  const visualShiftLimit=clip.runtime?.motionClass==="walk"?Math.min(cfg.maxShift,cfg.walkVisualShiftCap):cfg.maxShift;\n  let shiftX=clamp(targetDeltaX+comCorrection,-visualShiftLimit,visualShiftLimit);''','authored walk solver visual cap')

    rep('''    dominance=THREE.MathUtils.lerp(dominance,pelvisSolverState.last.visualDominance??dominance,retain);\n  }\n  return {shiftX,hipDrop,twist,compression,comCorrection,weight,visualWeight,visualDominance:dominance,targetX:target.x,comX:com.x};''','''    dominance=THREE.MathUtils.lerp(dominance,pelvisSolverState.last.visualDominance??dominance,retain);\n  }\n  // Prevent smoothing/history from reintroducing a larger lateral offset when switching into Walk.\n  if(clip.runtime?.motionClass==="walk")shiftX=clamp(shiftX,-visualShiftLimit,visualShiftLimit);\n  return {shiftX,hipDrop,twist,compression,comCorrection,weight,visualWeight,visualDominance:dominance,targetX:target.x,comX:com.x};''','walk cap after smoothing')

    migrate_anchor='''}\nconst WALK_TUNING_PRESETS={'''
    migrate_new='''}\nfunction migrateWalkPelvisTranslationHotfix(){\n  spec.motionPreview=spec.motionPreview||structuredClone(DEFAULT.motionPreview);\n  const m=spec.motionPreview;\n  // Preserve custom tuning. Only migrate the V1.8.1 Natural default that users already have saved.\n  if(Math.abs((Number(m.pelvisShift)||0)-.028)<.00001)m.pelvisShift=.014;\n  m.tuningVersion="1.8.5.3";\n  const p=ensureWeightSpec().pelvisSolver;\n  if(!Number.isFinite(Number(p.walkVisualShiftCap)))p.walkVisualShiftCap=.016;\n  p.tuningVersion="1.8.5.3";\n}\nconst WALK_TUNING_PRESETS={'''
    rep(migrate_anchor,migrate_new,'walk translation migration')

    rep('''  natural:{\n    motion:{pelvisShift:.028,pelvisBob:.040,pelvisTwist:3.5,chestTwist:5.5,compression:.020},\n    pelvis:{lateralInfluence:.32,lateralResponse:.55,maxShift:.075,hipDropDeg:2.5,twistDeg:4,comGain:.26,comMaxCorrection:.05,smoothing:.78,dominanceDeadZone:.08,responsePower:1.25}\n  },\n  subtle:{\n    motion:{pelvisShift:.018,pelvisBob:.034,pelvisTwist:2.5,chestTwist:4.5,compression:.017},\n    pelvis:{lateralInfluence:.24,lateralResponse:.42,maxShift:.055,hipDropDeg:1.7,twistDeg:3,comGain:.20,comMaxCorrection:.035,smoothing:.84,dominanceDeadZone:.10,responsePower:1.35}\n  },\n  stylized:{\n    motion:{pelvisShift:.040,pelvisBob:.052,pelvisTwist:4.5,chestTwist:7,compression:.024},\n    pelvis:{lateralInfluence:.42,lateralResponse:.68,maxShift:.095,hipDropDeg:3.5,twistDeg:5,comGain:.32,comMaxCorrection:.065,smoothing:.70,dominanceDeadZone:.06,responsePower:1.15}\n  }''','''  natural:{\n    motion:{pelvisShift:.014,pelvisBob:.040,pelvisTwist:3.5,chestTwist:5.5,compression:.020},\n    pelvis:{lateralInfluence:.32,lateralResponse:.55,maxShift:.075,walkVisualShiftCap:.016,hipDropDeg:2.5,twistDeg:4,comGain:.26,comMaxCorrection:.05,smoothing:.78,dominanceDeadZone:.08,responsePower:1.25}\n  },\n  subtle:{\n    motion:{pelvisShift:.010,pelvisBob:.034,pelvisTwist:2.5,chestTwist:4.5,compression:.017},\n    pelvis:{lateralInfluence:.24,lateralResponse:.42,maxShift:.055,walkVisualShiftCap:.012,hipDropDeg:1.7,twistDeg:3,comGain:.20,comMaxCorrection:.035,smoothing:.84,dominanceDeadZone:.10,responsePower:1.35}\n  },\n  stylized:{\n    motion:{pelvisShift:.020,pelvisBob:.052,pelvisTwist:4.5,chestTwist:7,compression:.024},\n    pelvis:{lateralInfluence:.42,lateralResponse:.68,maxShift:.095,walkVisualShiftCap:.024,hipDropDeg:3.5,twistDeg:5,comGain:.32,comMaxCorrection:.065,smoothing:.70,dominanceDeadZone:.06,responsePower:1.15}\n  }''','walk tuning presets lateral reduction')

    html=html.replace('Object.assign(spec.motionPreview,preset.motion,{tuningVersion:"1.8.1"});',
                      'Object.assign(spec.motionPreview,preset.motion,{tuningVersion:"1.8.5.3"});',1)
    html=html.replace('Object.assign(ensureWeightSpec().pelvisSolver,preset.pelvis,{tuningVersion:"1.8.1"});',
                      'Object.assign(ensureWeightSpec().pelvisSolver,preset.pelvis,{tuningVersion:"1.8.5.3"});',1)

    rep('''ensureRuntimeSettings();ensureWeightSpec();ensureSkinSystem();migrateNaturalWalkTuning();''','''ensureRuntimeSettings();ensureWeightSpec();ensureSkinSystem();migrateNaturalWalkTuning();migrateWalkPelvisTranslationHotfix();''','walk hotfix migration call')

    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.5.2"',
                      'localStorage.setItem("characterPrototypeStudio.v1.8.5.3"',1)
    html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.5.2")||',
                      'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.5.3")||localStorage.getItem("characterPrototypeStudio.v1.8.5.2")||',1)
    return html

if __name__=='__main__':
    from pathlib import Path
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
