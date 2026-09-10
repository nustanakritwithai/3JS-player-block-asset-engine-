#!/usr/bin/env node
/** Offline producer-side projection. Does not advance or modify the world. */
import { readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import { projectWorldSimGround } from './worldsim-ground-adapter.mjs';
export async function exportSnapshot(inputPath, outputPath) {
  const source = JSON.parse(await readFile(inputPath, 'utf8'));
  const frame = projectWorldSimGround(source);
  await writeFile(outputPath, JSON.stringify(frame));
  return frame.dimensions.gridWidth * frame.dimensions.gridHeight;
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [, , input, output] = process.argv;
  if (!input || !output || process.argv.length !== 4) {
    console.error('Usage: node ground/export-worldsim.mjs snapshot.json ground.json');
    process.exitCode = 1;
  } else {
    try { console.log(`Exported ${await exportSnapshot(input, output)} cells (presentation only)`); }
    catch (error) { console.error(error.message); process.exitCode = 1; }
  }
}
