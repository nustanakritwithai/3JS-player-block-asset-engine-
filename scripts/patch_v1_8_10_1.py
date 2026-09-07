from pathlib import Path

def patch(html):
    def rep(old,new,label,count=1):
        nonlocal html
        if old not in html:
            raise RuntimeError('missing anchor: '+label)
        html=html.replace(old,new,count)

    html=html.replace('Character Prototype Studio V1.8.10','Character Prototype Studio V1.8.10.1')
    html=html.replace('V1.8.10 · Monster Ball Action Pack','V1.8.10.1 · Character Boot Recovery Hotfix')
    html=html.replace('generatorVersion:"1.8.10"','generatorVersion:"1.8.10.1"')

    imports="""import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';
"""
    loader=r'''const THREE_RUNTIME_SOURCES=[
  {
    name:"jsDelivr",
    three:"https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js",
    orbit:"https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/controls/OrbitControls.js",
    transform:"https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/controls/TransformControls.js"
  },
  {
    name:"esm.sh",
    three:"https://esm.sh/three@0.169.0?target=es2020",
    orbit:"https://esm.sh/three@0.169.0/examples/jsm/controls/OrbitControls.js?target=es2020",
    transform:"https://esm.sh/three@0.169.0/examples/jsm/controls/TransformControls.js?target=es2020"
  }
];
function earlyBootOverlay(title,detail){
  let el=document.getElementById("studioBootError");
  if(!el){
    el=document.createElement("div");el.id="studioBootError";
    Object.assign(el.style,{position:"fixed",zIndex:"99999",left:"12px",right:"12px",top:"70px",padding:"14px",background:"rgba(80,12,18,.96)",border:"1px solid #ff6376",borderRadius:"12px",color:"#fff",fontFamily:"system-ui,sans-serif",boxShadow:"0 12px 40px #0009"});
    document.body.appendChild(el);
  }
  el.innerHTML=`<b>${title}</b><div style="margin-top:6px;font-size:12px;opacity:.9;word-break:break-word">${String(detail||"")}</div><button id="studioBootRetry" style="margin-top:10px;padding:8px 12px;border:0;border-radius:8px">Reload Studio</button>`;
  document.getElementById("studioBootRetry")?.addEventListener("click",()=>location.reload());
}
function moduleTimeout(promise,ms,label){
  return Promise.race([promise,new Promise((_,reject)=>setTimeout(()=>reject(new Error(label+" timeout")),ms))]);
}
async function loadThreeRuntime(){
  const failures=[];
  for(const src of THREE_RUNTIME_SOURCES){
    try{
      const three=await moduleTimeout(import(src.three),8000,src.name+" three");
      const [orbit,transform]=await Promise.all([
        moduleTimeout(import(src.orbit),8000,src.name+" OrbitControls"),
        moduleTimeout(import(src.transform),8000,src.name+" TransformControls")
      ]);
      if(!three?.WebGLRenderer||!orbit?.OrbitControls||!transform?.TransformControls)throw new Error("incomplete Three.js module set");
      window.__CPS_3D_SOURCE__=src.name;
      return {THREE:three,OrbitControls:orbit.OrbitControls,TransformControls:transform.TransformControls};
    }catch(err){failures.push(src.name+": "+(err?.message||err));console.warn("3D source failed",src.name,err)}
  }
  const detail=failures.join(" | ");earlyBootOverlay("3D engine failed to load",detail);throw new Error(detail);
}
const __threeRuntime=await loadThreeRuntime();
const THREE=__threeRuntime.THREE;
const OrbitControls=__threeRuntime.OrbitControls;
const TransformControls=__threeRuntime.TransformControls;
'''
    rep(imports,loader,'dynamic Three runtime fallback')

    startup='''loadLocal();const purgedLegacyTwistDemos=purgeLegacyTwistDemoClips();initUI();buildCharacter(false);applyCapturedPose(spec.pose.joints);$("#poseLabel").textContent=spec.pose.name||"Custom";updateHistoryButtons();if(purgedLegacyTwistDemos)autoSave();onResize();animate(performance.now());'''
    recovery=r'''function bootCharacterStudio(){
  let purgedLegacyTwistDemos=0;
  try{
    loadLocal();purgedLegacyTwistDemos=purgeLegacyTwistDemoClips();initUI();buildCharacter(false);applyCapturedPose(spec.pose.joints);$("#poseLabel").textContent=spec.pose.name||"Custom";updateHistoryButtons();if(purgedLegacyTwistDemos)autoSave();onResize();
    window.__CPS_BOOT_OK__=true;window.__CPS_BOOT_RECOVERED__=false;animate(performance.now());
    console.info("Character Studio boot OK via",window.__CPS_3D_SOURCE__||"unknown");
    return;
  }catch(primaryError){
    console.error("Character Studio primary boot failed",primaryError);
    try{
      const bad=localStorage.getItem("characterPrototypeStudio.v1.8.10")||localStorage.getItem("characterPrototypeStudio.v1.8.9");
      if(bad)localStorage.setItem("characterPrototypeStudio.v1.8.10.1.recoveryBackup",bad);
    }catch(_){}
    try{
      spec=structuredClone(DEFAULT);historyStack=[];redoStack=[];
      initUI();buildCharacter(false);applyPose("idle");$("#poseLabel").textContent="Idle · Recovered";updateHistoryButtons();onResize();
      window.__CPS_BOOT_OK__=true;window.__CPS_BOOT_RECOVERED__=true;animate(performance.now());
      setTimeout(()=>toast("Recovered default character · previous state backed up"),0);
      console.warn("Character Studio recovered from saved-state boot failure",primaryError);
      return;
    }catch(recoveryError){
      window.__CPS_BOOT_OK__=false;
      earlyBootOverlay("Character renderer failed to start",(primaryError?.message||primaryError)+" | recovery: "+(recoveryError?.message||recoveryError));
      throw recoveryError;
    }
  }
}
bootCharacterStudio();'''
    rep(startup,recovery,'safe character boot')

    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.10"', 'localStorage.setItem("characterPrototypeStudio.v1.8.10.1"',1)
    html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10")||', 'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10.1")||localStorage.getItem("characterPrototypeStudio.v1.8.10")||',1)
    return html

if __name__=='__main__':
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
