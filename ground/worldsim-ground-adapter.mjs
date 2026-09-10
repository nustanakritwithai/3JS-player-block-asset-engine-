/** Read-only projection of Living World Physics Simulator 20.9.4 snapshots.
 * Source: src/world/WorldSnapshot.ts, soil/SoilSnapshot.ts,
 * vegetation/VegetationSnapshot.ts, fire/FireSnapshot.ts, biomes/BiomeSnapshot.ts.
 * No biome classification, hydrology integration, clocks, or world writes here.
 */
export const GROUND_SCHEMA = 'worldsim-ground/1';
export const SOURCE_VERSION = '20.9.4';
export const BIOMES = Object.freeze(['forest','grassland','wetland','beach','rock','mountain','lake','river','dryland','burned','ocean']);
export const MATERIALS = Object.freeze(['grass','forest-floor','mud','sand','rock','dry-soil','burned']);
const TERRAIN = ['deepWater','shallowWater','sand','grass','forest','rock'];
const SOIL = ['none','sand','loam','clay','peat','rocky','wetland','coastal'];
const PROFILE = Object.freeze({forest:1,grassland:0,wetland:2,beach:3,rock:4,mountain:4,lake:2,river:2,dryland:5,burned:6,ocean:3});
export const CHANNELS = Object.freeze(['elevation','waterHeight','waterDepth','wetness','vegetation','burn','biome','material','ocean','flooded']);
const unit = value => Math.max(0, Math.min(1, value));
function finite(value, name, minimum = -Infinity) {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < minimum) throw new TypeError(`Invalid ${name}`);
  return value;
}
function integer(value, name, minimum = 0) {
  finite(value, name, minimum);
  if (!Number.isSafeInteger(value)) throw new TypeError(`Invalid ${name}`);
  return value;
}
function boolean(value, name) {
  if (typeof value !== 'boolean') throw new TypeError(`Invalid ${name}`);
  return value;
}
function enumValue(value, values, name) {
  if (!values.includes(value)) throw new TypeError(`Unsupported ${name}: ${String(value)}`);
  return value;
}
function dimensions(world) {
  const width = integer(world.gridWidth, 'gridWidth', 1);
  const height = integer(world.gridHeight, 'gridHeight', 1);
  if (width * height > 65536) throw new RangeError('Ground preview is limited to 65536 cells');
  const cw = finite(world.cellWidth, 'cellWidth', Number.MIN_VALUE);
  const ch = finite(world.cellHeight, 'cellHeight', Number.MIN_VALUE);
  const ww = finite(world.worldWidth, 'worldWidth', Number.MIN_VALUE);
  const wh = finite(world.worldHeight, 'worldHeight', Number.MIN_VALUE);
  if (Math.abs(width*cw-ww) > Math.max(1,ww)*1e-8 || Math.abs(height*ch-wh) > Math.max(1,wh)*1e-8) throw new TypeError('Inconsistent world dimensions');
  return {gridWidth:width, gridHeight:height, cellWidth:cw, cellHeight:ch, worldWidth:ww, worldHeight:wh};
}
function cellsOf(section, count, label) {
  const cells = section?.cells;
  if (!Array.isArray(cells) || cells.length !== count) throw new TypeError(`Missing or incomplete ${label}.cells; a full snapshot is required`);
  for (let i=0;i<count;i++) if (!cells[i] || cells[i].index !== i) throw new TypeError(`${label}.cells must have canonical row-major indices (at ${i})`);
  return cells;
}
function seal(frame) {
  for (const name of CHANNELS) Object.freeze(frame.channels[name]);
  Object.freeze(frame.channels); Object.freeze(frame.source.versions); Object.freeze(frame.source);
  Object.freeze(frame.dimensions);
  return Object.freeze(frame);
}
/** Accept RenderSnapshot or RenderWorldSnapshot. Optional surfaceBiome must be
 * the producer's existing WorldSurfacePresentation.worldSurfaceBiome function,
 * not a new consumer classifier. The default uses primaryBiome verbatim.
 */
export function projectWorldSimGround(input, {sourceVersion=SOURCE_VERSION, surfaceBiome}={}) {
  if (sourceVersion !== SOURCE_VERSION) throw new TypeError('Unverified producer version; add an audited adapter first');
  if (surfaceBiome !== undefined && typeof surfaceBiome !== 'function') throw new TypeError('surfaceBiome must be a producer function');
  const world = input?.world ?? input;
  if (!world || typeof world !== 'object') throw new TypeError('World snapshot required');
  const dims = dimensions(world), count = dims.gridWidth*dims.gridHeight;
  const terrain = cellsOf(world,count,'world');
  const soil = cellsOf(world.soil,count,'soil');
  const vegetation = cellsOf(world.vegetation,count,'vegetation');
  const biomes = cellsOf(world.biomes,count,'biomes');
  const fire = cellsOf(world.fire,count,'fire');
  const channels = Object.fromEntries(CHANNELS.map(key => [key,new Array(count)]));
  const versions = {};
  for (const key of ['hydrology','soil','vegetation','biomes','fire']) {
    versions[key] = integer(world[key]?.version,`${key}.version`);
  }
  for (let i=0;i<count;i++) {
    const c=terrain[i], s=soil[i], v=vegetation[i], f=fire[i];
    if (c.column!==i%dims.gridWidth || c.row!==Math.floor(i/dims.gridWidth)) throw new TypeError(`Cell coordinate/index mismatch at ${i}`);
    enumValue(c.terrainType,TERRAIN,'terrainType'); enumValue(s.soilType,SOIL,'soilType');
    const biome=enumValue(biomes[i].primaryBiome,BIOMES,'primaryBiome');
    const surface=surfaceBiome ? enumValue(surfaceBiome(world,i),BIOMES,'producer surfaceBiome') : biome;
    const water=finite(s.waterContent,`soil[${i}].waterContent`,0);
    const capacity=finite(s.saturationCapacity,`soil[${i}].saturationCapacity`,0);
    const active=boolean(s.active,`soil[${i}].active`);
    const coverage=finite(v.coverage,`vegetation[${i}].coverage`,0);
    channels.elevation[i]=finite(c.elevation,`cells[${i}].elevation`);
    // totalWaterHeight already contains the elevation datum; never add it twice.
    channels.waterHeight[i]=finite(c.totalWaterHeight,`cells[${i}].totalWaterHeight`);
    channels.waterDepth[i]=finite(c.surfaceWater,`cells[${i}].surfaceWater`,0);
    channels.wetness[i]=active && capacity>0 ? unit(water/capacity) : 0;
    channels.vegetation[i]=boolean(v.active,`vegetation[${i}].active`) ? unit(coverage) : 0;
    channels.burn[i]=unit(finite(f.burnSeverity,`fire[${i}].burnSeverity`,0));
    channels.biome[i]=BIOMES.indexOf(biome);
    channels.material[i]=PROFILE[surface];
    channels.ocean[i]=Number(boolean(c.isOceanCell,`cells[${i}].isOceanCell`));
    channels.flooded[i]=Number(boolean(c.isFlooded,`cells[${i}].isFlooded`));
  }
  return seal({schema:GROUND_SCHEMA,presentationOnly:true,source:{version:SOURCE_VERSION,seed:integer(world.seed,'seed',-Number.MAX_SAFE_INTEGER),tick:input?.world ? integer(input.tick,'tick') : null,surfacePolicy:surfaceBiome?'producer-worldSurfaceBiome':'primaryBiome',versions},dimensions:dims,channels});
}
/** Validate imported presentation packets; copy arrays so callers cannot mutate
 * data held by the renderer. This packet is not authoritative gameplay input. */
export function readGroundFrame(value) {
  if (value?.schema!==GROUND_SCHEMA || value.presentationOnly!==true || value.source?.version!==SOURCE_VERSION) throw new TypeError('Unsupported ground frame');
  const dims=dimensions(value.dimensions), count=dims.gridWidth*dims.gridHeight;
  const channels={};
  for (const key of CHANNELS) {
    const arr=value.channels?.[key];
    if (!Array.isArray(arr)||arr.length!==count) throw new TypeError(`Invalid ground channel ${key}`);
    channels[key]=arr.map((n,i)=>finite(n,`${key}[${i}]`));
    if (['wetness','vegetation','burn','ocean','flooded'].includes(key) && arr.some(n=>n<0||n>1)) throw new RangeError(`Invalid normalized channel ${key}`);
    if (['ocean','flooded'].includes(key) && arr.some(n=>n!==0&&n!==1)) throw new RangeError(`Invalid flag channel ${key}`);
    if (key==='waterDepth' && arr.some(n=>n<0)) throw new RangeError('Negative water depth');
    const max=key==='biome'?BIOMES.length:key==='material'?MATERIALS.length:null;
    if (max!==null && arr.some(n=>!Number.isInteger(n)||n<0||n>=max)) throw new RangeError(`Invalid enum channel ${key}`);
  }
  const source=value.source, versions={};
  for (const key of ['hydrology','soil','vegetation','biomes','fire']) versions[key]=integer(source.versions?.[key],`${key}.version`);
  if (!['primaryBiome','producer-worldSurfaceBiome'].includes(source.surfacePolicy)) throw new TypeError('Unknown surface policy');
  return seal({schema:GROUND_SCHEMA,presentationOnly:true,source:{version:SOURCE_VERSION,seed:integer(source.seed,'seed',-Number.MAX_SAFE_INTEGER),tick:source.tick===null?null:integer(source.tick,'tick'),surfacePolicy:source.surfacePolicy,versions},dimensions:dims,channels});
}
