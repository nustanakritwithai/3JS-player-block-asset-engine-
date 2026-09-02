#!/usr/bin/env python3
from pathlib import Path
import argparse, json, math
import numpy as np
from PIL import Image


def save_webp(arr,path,quality=94):
    arr=np.clip(arr,0,255).astype(np.uint8)
    Image.fromarray(arr,'RGB').save(path,'WEBP',quality=quality,method=6)

def save_gray(arr,path,quality=94):
    arr=np.clip(arr,0,255).astype(np.uint8)
    Image.fromarray(np.stack([arr]*3,-1),'RGB').save(path,'WEBP',quality=quality,method=6)

def normal_from_height(height,strength=2.5):
    h=height.astype(np.float32)
    gy,gx=np.gradient(h)
    nx=-gx*strength; ny=-gy*strength; nz=np.ones_like(h)
    length=np.sqrt(nx*nx+ny*ny+nz*nz)+1e-8
    return np.clip(np.stack([(nx/length*.5+.5),(ny/length*.5+.5),(nz/length*.5+.5)],-1)*255,0,255).astype(np.uint8)

def build(out: Path, N: int):
    out.mkdir(parents=True,exist_ok=True)
    Y,X=np.mgrid[0:N,0:N]
    def smooth_noise(scale,seed):
        rr=np.random.default_rng(seed)
        small=max(4,N//scale)
        a=(rr.random((small,small))*255).astype(np.uint8)
        return np.asarray(Image.fromarray(a,'L').resize((N,N),Image.Resampling.BICUBIC),dtype=np.float32)/255
    n1=smooth_noise(128,1); n2=smooth_noise(48,2); n3=smooth_noise(18,3)
    materials={}

    pores=(np.sin(X*.31)+np.sin(Y*.27)+np.sin((X+Y)*.17))*.5
    skin_h=.55*n2+.25*n3+.02*pores
    skin=np.empty((N,N,3),float); skin[:]=[211,157,119]
    skin*=.90+.16*n1[...,None]; skin+=((n3-.5)*9)[...,None]; skin[...,0]+=(n2-.5)*8; skin[...,2]-=(n2-.5)*5
    save_webp(skin,out/'skin_warm_basecolor.webp'); Image.fromarray(normal_from_height(skin_h,1.1),'RGB').save(out/'skin_warm_normal.png')
    save_gray(175+(n2-.5)*35,out/'skin_warm_roughness.webp'); save_gray(235-n1*20,out/'skin_warm_ao.webp')
    materials['skin_warm']={'baseColor':'skin_warm_basecolor.webp','normal':'skin_warm_normal.png','roughness':'skin_warm_roughness.webp','ao':'skin_warm_ao.webp'}

    warp=np.sin(X*math.pi/5.5)*.5+.5; weft=np.sin(Y*math.pi/6.2)*.5+.5; cloth_h=.22*warp+.22*weft+.35*n3+.18*n2
    navy=np.empty((N,N,3),float); navy[:]=[38,70,116]; navy*=.82+.26*n2[...,None]; navy+=((warp*weft)*16)[...,None]
    save_webp(navy,out/'cloth_navy_basecolor.webp'); Image.fromarray(normal_from_height(cloth_h,2.6),'RGB').save(out/'cloth_weave_normal.png')
    save_gray(205+(n2-.5)*25,out/'cloth_roughness.webp'); save_gray(220-n1*30,out/'cloth_ao.webp')
    materials['cloth_navy']={'baseColor':'cloth_navy_basecolor.webp','normal':'cloth_weave_normal.png','roughness':'cloth_roughness.webp','ao':'cloth_ao.webp'}
    red=np.empty((N,N,3),float); red[:]=[139,39,48]; red*=.80+.28*n2[...,None]; red+=((warp*weft)*12)[...,None]
    save_webp(red,out/'cloth_red_basecolor.webp')
    materials['cloth_red']={'baseColor':'cloth_red_basecolor.webp','normal':'cloth_weave_normal.png','roughness':'cloth_roughness.webp','ao':'cloth_ao.webp'}

    leather_h=.55*n2+.28*n3+.05*np.sin(X*.08+n1*8)+.04*np.sin(Y*.11+n2*7)
    leather=np.empty((N,N,3),float); leather[:]=[92,49,27]; leather*=.74+.42*n1[...,None]; leather[...,0]+=n3*12
    save_webp(leather,out/'leather_brown_basecolor.webp'); Image.fromarray(normal_from_height(leather_h,2),'RGB').save(out/'leather_brown_normal.png')
    save_gray(165+(n2-.5)*45,out/'leather_brown_roughness.webp'); save_gray(205-n1*42,out/'leather_brown_ao.webp')
    materials['leather_brown']={'baseColor':'leather_brown_basecolor.webp','normal':'leather_brown_normal.png','roughness':'leather_brown_roughness.webp','ao':'leather_brown_ao.webp'}

    scratch=np.sin(Y*.45+np.sin(X*.01)*5); metal_h=.18*n3+.05*scratch
    steel=np.empty((N,N,3),float); steel[:]=[150,158,166]; steel*=.78+.34*n1[...,None]; steel+=(scratch*9)[...,None]
    save_webp(steel,out/'steel_basecolor.webp'); Image.fromarray(normal_from_height(metal_h,1.3),'RGB').save(out/'steel_normal.png')
    save_gray(98+(n2-.5)*35,out/'steel_roughness.webp'); save_gray(np.full((N,N),245),out/'steel_metalness.webp'); save_gray(228-n1*20,out/'steel_ao.webp')
    materials['steel']={'baseColor':'steel_basecolor.webp','normal':'steel_normal.png','roughness':'steel_roughness.webp','metalness':'steel_metalness.webp','ao':'steel_ao.webp'}
    gold=np.empty((N,N,3),float); gold[:]=[190,134,34]; gold*=.80+.30*n1[...,None]; gold[...,0]+=n3*14
    save_webp(gold,out/'gold_basecolor.webp'); Image.fromarray(normal_from_height(metal_h,1),'RGB').save(out/'gold_normal.png')
    save_gray(82+(n2-.5)*28,out/'gold_roughness.webp'); save_gray(np.full((N,N),250),out/'gold_metalness.webp'); save_gray(232-n1*18,out/'gold_ao.webp')
    materials['gold']={'baseColor':'gold_basecolor.webp','normal':'gold_normal.png','roughness':'gold_roughness.webp','metalness':'gold_metalness.webp','ao':'gold_ao.webp'}

    strands=np.sin(X*.16+np.sin(Y*.012)*8)+.55*np.sin(X*.29+Y*.018); hair_h=.5*n2+.16*strands
    hair=np.empty((N,N,3),float); hair[:]=[23,26,31]; hair+=((strands+1.5)/2.5*25)[...,None]; hair*=.82+.22*n1[...,None]
    save_webp(hair,out/'hair_dark_basecolor.webp'); Image.fromarray(normal_from_height(hair_h,2.1),'RGB').save(out/'hair_dark_normal.png')
    save_gray(135+(n2-.5)*30,out/'hair_dark_roughness.webp'); save_gray(220-n1*28,out/'hair_dark_ao.webp')
    materials['hair_dark']={'baseColor':'hair_dark_basecolor.webp','normal':'hair_dark_normal.png','roughness':'hair_dark_roughness.webp','ao':'hair_dark_ao.webp'}

    cell=max(18,N//46); cy=Y//cell; fx=((X+(cy%2)*(cell//2))%cell)/cell-.5; fy=(Y%cell)/cell-.5
    radius=np.sqrt((fx/.52)**2+(fy/.42)**2); rel=np.clip(1-radius,0,1); scale_h=.55*rel+.22*n2+.12*n3
    scales=np.empty((N,N,3),float); scales[:]=[53,110,64]; scales*=.70+.40*n1[...,None]; scales[...,1]+=rel*35; scales[...,0]+=rel*8
    save_webp(scales,out/'monster_green_basecolor.webp'); Image.fromarray(normal_from_height(scale_h,3.5),'RGB').save(out/'monster_green_normal.png')
    save_gray(185+(n2-.5)*32,out/'monster_green_roughness.webp'); save_gray(190+rel*45-n1*22,out/'monster_green_ao.webp')
    materials['monster_green']={'baseColor':'monster_green_basecolor.webp','normal':'monster_green_normal.png','roughness':'monster_green_roughness.webp','ao':'monster_green_ao.webp'}

    radial=(np.sin(X*.035)+np.sin(Y*.041)+np.sin((X+Y)*.018))*.33; glow=np.clip((radial+1)/2,0,1)**3
    em=np.empty((N,N,3),float); em[:]=[4,18,25]; em[...,0]+=glow*10; em[...,1]+=glow*150; em[...,2]+=glow*220
    save_webp(em,out/'emissive_cyan_basecolor.webp'); save_webp(em*1.15,out/'emissive_cyan_emissive.webp'); save_gray(105+(n2-.5)*25,out/'emissive_cyan_roughness.webp')
    materials['emissive_cyan']={'baseColor':'emissive_cyan_basecolor.webp','emissive':'emissive_cyan_emissive.webp','roughness':'emissive_cyan_roughness.webp'}

    manifest={'schemaVersion':'1','masterResolution':N,'generatedNativelyAtResolution':True,'pixelArt':False,'note':f'Starter material pack generated natively at {N}x{N}; not upscaled from low-resolution sources.','materials':materials}
    (out/'texture_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='assets/textures');ap.add_argument('--resolution',type=int,default=2048);args=ap.parse_args()
    if args.resolution<2048: raise SystemExit('High-quality master generation requires resolution >= 2048')
    build(Path(args.output),args.resolution)
