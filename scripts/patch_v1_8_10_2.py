from pathlib import Path
import re

def patch(html):
    html=html.replace('Character Prototype Studio V1.8.10.1','Character Prototype Studio V1.8.10.2')
    html=html.replace('V1.8.10.1 · Character Boot Recovery Hotfix','V1.8.10.2 · Core-First Character Boot Hotfix')

    pattern=re.compile(r'''const THREE_RUNTIME_SOURCES=\[.*?const TransformControls=__threeRuntime\.TransformControls;\n''',re.S)
    replacement=r'''const THREE_CORE_SOURCES=[
  {name:"jsDelivr",url:"https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js"},
  {name:"esm.sh",url:"https://esm.sh/three@0.169.0?target=es2020"},
  {name:"unpkg",url:"https://unpkg.com/three@0.169.0/build/three.module.js"}
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
async function loadThreeCore(){
  const failures=[];
  for(const src of THREE_CORE_SOURCES){
    try{
      const three=await moduleTimeout(import(src.url),7000,src.name+" three");
      if(!three?.WebGLRenderer||!three?.Scene||!three?.Object3D)throw new Error("incomplete Three.js core");
      window.__CPS_3D_SOURCE__=src.name;
      return three;
    }catch(err){failures.push(src.name+": "+(err?.message||err));console.warn("Three core source failed",src.name,err)}
  }
  const detail=failures.join(" | ");earlyBootOverlay("3D engine core failed to load",detail);throw new Error(detail);
}
function makeFallbackOrbitControls(THREE){
  return class FallbackOrbitControls{
    constructor(camera,domElement){this.object=camera;this.domElement=domElement;this.enabled=true;this.enableDamping=false;this.target=new THREE.Vector3();this.minDistance=0;this.maxDistance=Infinity;this.maxPolarAngle=Math.PI}
    update(){return false}
    dispose(){}
  };
}
function makeFallbackTransformControls(THREE){
  return class FallbackTransformControls extends THREE.EventDispatcher{
    constructor(camera,domElement){super();this.camera=camera;this.domElement=domElement;this.object=null;this.enabled=false;this._mode="rotate";this._space="local";this._helper=new THREE.Group();this._helper.name="TransformControlsFallback"}
    setMode(v){this._mode=v;return this}
    getMode(){return this._mode}
    setSpace(v){this._space=v;return this}
    setSize(){return this}
    attach(obj){this.object=obj;return this}
    detach(){this.object=null;return this}
    getHelper(){return this._helper}
    dispose(){}
  };
}
async function loadEditorControls(THREE){
  if(window.__CPS_3D_SOURCE__==="jsDelivr"){
    try{
      const [orbit,transform]=await Promise.all([
        moduleTimeout(import("https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/controls/OrbitControls.js"),5000,"jsDelivr OrbitControls"),
        moduleTimeout(import("https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/controls/TransformControls.js"),5000,"jsDelivr TransformControls")
      ]);
      if(orbit?.OrbitControls&&transform?.TransformControls){
        window.__CPS_CONTROLS_FALLBACK__=false;
        return {OrbitControls:orbit.OrbitControls,TransformControls:transform.TransformControls};
      }
    }catch(err){console.warn("Editor controls unavailable; rendering with fallback controls",err)}
  }
  window.__CPS_CONTROLS_FALLBACK__=true;
  return {OrbitControls:makeFallbackOrbitControls(THREE),TransformControls:makeFallbackTransformControls(THREE)};
}
const THREE=await loadThreeCore();
const __editorControls=await loadEditorControls(THREE);
const OrbitControls=__editorControls.OrbitControls;
const TransformControls=__editorControls.TransformControls;
'''
    html,n=pattern.subn(replacement,html,1)
    if n!=1:
        raise RuntimeError('missing V1.8.10.1 runtime loader anchor')

    html=html.replace('localStorage.setItem("characterPrototypeStudio.v1.8.10.1"', 'localStorage.setItem("characterPrototypeStudio.v1.8.10.2"',1)
    html=html.replace('const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10.1")||', 'const raw=localStorage.getItem("characterPrototypeStudio.v1.8.10.2")||localStorage.getItem("characterPrototypeStudio.v1.8.10.1")||',1)
    html=html.replace('characterPrototypeStudio.v1.8.10.1.recoveryBackup','characterPrototypeStudio.v1.8.10.2.recoveryBackup')
    return html

if __name__=='__main__':
    import sys
    p=Path(sys.argv[1]);p.write_text(patch(p.read_text(encoding='utf-8')),encoding='utf-8')
