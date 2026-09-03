def patch(html):
    old='''function previewDynamicsAutoTune(){\n  const clip=selectedAnimationClip(),p=dynamicsAutoTunerState.proposal;if(!clip||!p||p.clipId!==clip.id||!p.changes.length)return;\n  if(dynamicsAutoTunerState.preview)cancelDynamicsAutoTunePreview(false);'''
    new='''function previewDynamicsAutoTune(){\n  const clip=selectedAnimationClip(),p=dynamicsAutoTunerState.proposal;if(!clip||!p||p.clipId!==clip.id||!p.changes.length)return;\n  if(p.sourceFingerprint!==actionDynamicsFingerprint(clip)){dynamicsAutoTunerState.proposal=null;renderDynamicsAutoTuner();toast("Auto-Tuner proposal stale · Analyze again");return}\n  if(dynamicsAutoTunerState.preview)cancelDynamicsAutoTunePreview(false);'''
    if old not in html:
        raise RuntimeError('missing preview stale guard anchor')
    html=html.replace(old,new,1)

    old='''function applyDynamicsAutoTune(){\n  const clip=selectedAnimationClip(),p=dynamicsAutoTunerState.proposal;if(!clip||!p||p.clipId!==clip.id||!p.changes.length)return;\n  const authoredBefore=JSON.stringify(clip.keyframes);'''
    new='''function applyDynamicsAutoTune(){\n  const clip=selectedAnimationClip(),p=dynamicsAutoTunerState.proposal;if(!clip||!p||p.clipId!==clip.id||!p.changes.length)return;\n  if(!dynamicsAutoTunerState.preview&&p.sourceFingerprint!==actionDynamicsFingerprint(clip)){dynamicsAutoTunerState.proposal=null;renderDynamicsAutoTuner();toast("Auto-Tuner proposal stale · Analyze again");return}\n  const authoredBefore=JSON.stringify(clip.keyframes);'''
    if old not in html:
        raise RuntimeError('missing apply stale guard anchor')
    return html.replace(old,new,1)
