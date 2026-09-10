#!/usr/bin/env python3


def patch(html: str) -> str:
    if 'Character Prototype Studio V1.8.10.6' not in html:
        raise RuntimeError('missing V1.8.10.6 base for cuff hierarchy hotfix')
    if 'blueExplorerBindCuffsToElbows' in html:
        raise RuntimeError('Blue Explorer cuff hierarchy hotfix already applied')

    helper_anchor = 'function buildBlueExplorerPrimaryCharacter(preserve=true){'
    if helper_anchor not in html:
        raise RuntimeError('missing Blue Explorer primary builder')

    helper = r'''const BLUE_EXPLORER_CUFF_MESH=/^(?:rolled-cuff|cuff-lower-edge|cuff-button-shadow|cuff-button)_/;
function blueExplorerBindCuffsToElbows(r){
  for(const [shoulder,elbow] of [[r.shoulder_left,r.elbow_left],[r.shoulder_right,r.elbow_right]]){
    if(!shoulder||!elbow)continue;
    shoulder.updateWorldMatrix?.(true,true);elbow.updateWorldMatrix?.(true,true);
    const pieces=[...shoulder.children].filter(node=>node?.isMesh&&BLUE_EXPLORER_CUFF_MESH.test(String(node.name||"")));
    for(const piece of pieces){
      elbow.attach(piece);
      piece.userData??={};piece.userData.cuffOwner="elbow";
    }
    elbow.userData??={};elbow.userData.cuffPieceCount=pieces.length;
  }
}
'''
    html = html.replace(helper_anchor, helper + helper_anchor, 1)

    hierarchy_anchor = '    r.pelvis.attach(r.hip_left);r.pelvis.attach(r.hip_right);\n    if(model.parts?.pouch)r.pelvis.attach(model.parts.pouch);'
    hierarchy_replacement = hierarchy_anchor + '\n    model.root.updateMatrixWorld?.(true);\n    blueExplorerBindCuffsToElbows(r);'
    if hierarchy_anchor not in html:
        raise RuntimeError('missing Blue Explorer hierarchy anchor')
    html = html.replace(hierarchy_anchor, hierarchy_replacement, 1)

    html = html.replace('Character Prototype Studio V1.8.10.6', 'Character Prototype Studio V1.8.10.7')
    html = html.replace('V1.8.10.6 · Shared Solver Runtime', 'V1.8.10.7 · Cuff Hierarchy Hotfix')
    html = html.replace('studioVersion:"1.8.10.6"', 'studioVersion:"1.8.10.7"')
    return html
