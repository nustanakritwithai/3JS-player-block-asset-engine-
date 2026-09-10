/** Run against the separately supplied, authorized WorldSim source.
 * Compile original code (from its root) with:
 * tsc --target es2020 --module commonjs --moduleResolution node --rootDir src \
 *   --outDir /absolute/path/worldsim-compiled --skipLibCheck --esModuleInterop \
 *   --strict src/simulation/Simulation.ts src/rendering/WorldSurfacePresentation.ts
 * Then: node tests/ground-worldsim-integration.mjs /absolute/path/worldsim-compiled
 */
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { resolve, join } from 'node:path';
import { writeFile } from 'node:fs/promises';
import { projectWorldSimGround, readGroundFrame } from '../ground/worldsim-ground-adapter.mjs';
import { buildGroundGeometry } from '../ground/ground-geometry.mjs';
const root=process.argv[2];
if(!root){console.error('Usage: node tests/ground-worldsim-integration.mjs /path/to/worldsim-compiled [output-example.json]');process.exitCode=1;}
else {
 const require=createRequire(import.meta.url);
 const {Simulation}=require(join(resolve(root),'simulation/Simulation.js'));
 const {worldSurfaceBiome}=require(join(resolve(root),'rendering/WorldSurfacePresentation.js'));
 for(const size of [16,64]){
  const sim=new Simulation({initializeWorld:false,config:{seed:29051,initialDynamicBodyCount:0},worldGenerationConfig:{gridWidth:size,gridHeight:size}});
  const snapshot=sim.getSnapshot(),before=JSON.stringify(snapshot),frame=projectWorldSimGround(snapshot);
  assert.deepEqual(readGroundFrame(JSON.parse(JSON.stringify(frame))),frame);
  const visual=projectWorldSimGround(snapshot,{surfaceBiome:worldSurfaceBiome});
  assert.equal(visual.source.surfacePolicy,'producer-worldSurfaceBiome');
  assert.equal(JSON.stringify(snapshot),before,'input snapshot changed');
  // getSnapshot itself can consume dirty-index bookkeeping; compare projected
  // cell truth and the clock, not unrelated inspector/metrics bookkeeping.
  const again=sim.getSnapshot();assert.equal(again.tick,snapshot.tick);
  assert.deepEqual(projectWorldSimGround(again),frame);
  const geometry=buildGroundGeometry(frame,{horizontalScale:.04,elevationScale:15,textureWorldSize:4});
  assert.equal(geometry.terrain.reduce((n,g)=>n+g.position.length/3,0),size*size*6);
  assert.ok(geometry.terrain.every(g=>g.position.every(Number.isFinite)));
  sim.advanceFrame(1/30);assert.equal(projectWorldSimGround(sim.getSnapshot()).source.tick,1);
  if(size===16&&process.argv[3])await writeFile(process.argv[3],JSON.stringify(visual));
  console.log(`PASS real WorldSim 20.9.4 ${size}x${size}; immutable projection, roundtrip, geometry, producer selector, tick 0 -> 1`);
 }
}
