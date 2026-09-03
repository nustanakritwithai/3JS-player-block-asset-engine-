#!/usr/bin/env python3
from pathlib import Path


def patch(html):
    old = '''  "hp","hpcurrent","hpmax","atk","def","spatk","spdef","spd","vitality","combat","blade","ranged","fruitpower","mastery","mana","coins","capture","save","level","exp","experience","damage"'''
    new = '''  "hp","hpcurrent","hpmax","atk","def","spatk","spdef","spd","speed","vitality","combat","blade","ranged","fruitpower","mastery","mana","coins","capture","capturechance","skill","collider","interactionradius","save","savepayload","level","exp","experience","damage"'''
    if old not in html:
        raise RuntimeError('missing V1.9.0 forbidden-key anchor')
    return html.replace(old, new, 1)


if __name__ == '__main__':
    import sys
    p = Path(sys.argv[1])
    p.write_text(patch(p.read_text(encoding='utf-8')), encoding='utf-8')
