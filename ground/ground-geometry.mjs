import { MATERIALS } from './worldsim-ground-adapter.mjs';
/** Visual geometry only. Source horizontal coordinates and normalized elevations
 * are NOT metres. Consumers must select their own explicit coordinate transform.
 * Collision/navigation must continue to sample the authoritative WorldSim grid. */
export function validateGroundTransform({horizontalScale,elevationScale,textureWorldSize=4}={}) {
  for (const [key,value] of Object.entries({horizontalScale,elevationScale,textureWorldSize})) {
    if (!Number.isFinite(value)||value<=0) throw new RangeError(`${key} must be a positive finite number`);
  }
  return Object.freeze({horizontalScale,elevationScale,textureWorldSize});
}
export function buildGroundGeometry(frame, transform) {
  const {horizontalScale,elevationScale,textureWorldSize}=validateGroundTransform(transform);
  const d=frame.dimensions, c=frame.channels, w=d.gridWidth, h=d.gridHeight;
  const dx=d.cellWidth*horizontalScale, dz=d.cellHeight*horizontalScale;
  const vertices=(w+1)*(h+1), heights=new Float64Array(vertices), wet=new Float64Array(vertices), burn=new Float64Array(vertices);
  const normals=new Float64Array(vertices*3);
  for (let z=0;z<=h;z++) for (let x=0;x<=w;x++) {
    const j=z*(w+1)+x; let n=0;
    for (let oz=-1;oz<=0;oz++) for (let ox=-1;ox<=0;ox++) {
      const cx=x+ox, cz=z+oz;
      if (cx<0||cz<0||cx>=w||cz>=h) continue;
      const i=cz*w+cx; heights[j]+=c.elevation[i]*elevationScale; wet[j]+=c.wetness[i];burn[j]+=c.burn[i];n++;
    }
    heights[j]/=n;wet[j]/=n;burn[j]/=n;
  }
  for (let z=0;z<=h;z++) for (let x=0;x<=w;x++) {
    const l=Math.max(0,x-1),r=Math.min(w,x+1),t=Math.max(0,z-1),b=Math.min(h,z+1),j=z*(w+1)+x;
    const nx=(heights[z*(w+1)+l]-heights[z*(w+1)+r])/((r-l)*dx);
    const nz=(heights[t*(w+1)+x]-heights[b*(w+1)+x])/((b-t)*dz);
    const length=Math.hypot(nx,1,nz); normals.set([nx/length,1/length,nz/length],j*3);
  }
  const batch=()=>({position:[],normal:[],uv:[],surface:[]});
  const terrain=Array.from({length:MATERIALS.length},batch),water=batch();
  const order=[[0,0],[0,1],[1,0],[1,0],[0,1],[1,1]];
  for (let z=0;z<h;z++) for (let x=0;x<w;x++) {
    const i=z*w+x, dest=terrain[c.material[i]];
    for (const [ox,oz] of order) {
      const vx=x+ox,vz=z+oz,j=vz*(w+1)+vx;
      const px=vx*dx-w*dx/2,pz=vz*dz-h*dz/2;
      dest.position.push(px,heights[j],pz);dest.normal.push(...normals.subarray(j*3,j*3+3));
      // UVs are globally anchored, not reset at material/chunk boundaries.
      dest.uv.push(px/textureWorldSize,pz/textureWorldSize);dest.surface.push(wet[j],burn[j]);
      if (c.waterDepth[i]>0) {
        water.position.push(px,c.waterHeight[i]*elevationScale,pz);
        water.normal.push(0,1,0);water.uv.push(px/textureWorldSize,pz/textureWorldSize);water.surface.push(0,0);
      }
    }
  }
  const typed=b=>Object.fromEntries(Object.entries(b).map(([k,v])=>[k,new Float32Array(v)]));
  return {terrain:terrain.map(typed),water:typed(water),bounds:{width:w*dx,depth:h*dz},cellCount:w*h};
}
