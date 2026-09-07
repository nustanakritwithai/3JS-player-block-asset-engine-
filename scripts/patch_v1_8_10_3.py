#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    def rep(old, new, label, count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: ' + label)
        html = html.replace(old, new, count)

    html = html.replace('Character Prototype Studio V1.8.10.2', 'Character Prototype Studio V1.8.10.3')
    html = html.replace('V1.8.10.2 · Core-First Character Boot Hotfix', 'V1.8.10.3 · clip Reference Hotfix')
    html = html.replace('generatorVersion:"1.8.10.2"', 'generatorVersion:"1.8.10.3"')

    old = '''function renderContactAnalysis(){\n  const r=contactAnalysisState.last;\n  $("#authoredSlideL").textContent=(r?.maxL||0).toFixed(2);\n  $("#authoredSlideR").textContent=(r?.maxR||0).toFixed(2);\n  $("#authoredContactPct").textContent=Math.round((r?.contactPct||0)*100)+"%";\n  const state=contactStateAtTime(selectedAnimationClip(),animationState.time);\n  $("#authoredWeightState").textContent=state.weight.toUpperCase();\n  if($("#authoredFootPlantToggle"))$("#authoredFootPlantToggle").checked=clip.footPlant?.enabled!==false;'''
    new = '''function renderContactAnalysis(){\n  const clip=selectedAnimationClip();\n  const r=contactAnalysisState.last;\n  $("#authoredSlideL").textContent=(r?.maxL||0).toFixed(2);\n  $("#authoredSlideR").textContent=(r?.maxR||0).toFixed(2);\n  $("#authoredContactPct").textContent=Math.round((r?.contactPct||0)*100)+"%";\n  const state=contactStateAtTime(clip,animationState.time);\n  $("#authoredWeightState").textContent=state.weight.toUpperCase();\n  if($("#authoredFootPlantToggle"))$("#authoredFootPlantToggle").checked=clip?.footPlant?.enabled!==false;'''
    rep(old, new, 'renderContactAnalysis clip scope fix')

    html = html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.10.2"', 'localStorage.setItem("characterPrototypeStudio.v1.8.10.3"', 1)
    html = html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10.2")||', 'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10.3")||localStorage.getItem("characterPrototypeStudio.v1.8.10.2")||', 1)
    return html


if __name__ == '__main__':
    import sys
    p = Path(sys.argv[1])
    p.write_text(patch(p.read_text(encoding='utf-8')), encoding='utf-8')
