// news-image-20261119: entry driver, Node 22 standard library only.
//
// The entry is the newspaper front page in entry.png beside this file: it
// sums up the world news of Thursday 19 November 2026 and was drawn by
// src/render.py from headlines researched that day. This program reads the
// image and writes it out to /output/entry.png. Reading a file and writing
// it back byte for byte is deterministic, so repeated runs produce
// identical output, exactly as the competition requires.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

if (!existsSync(source)) {
  throw new Error(`entry image missing: ${source}`);
}
mkdirSync(outDir, { recursive: true });

const bytes = readFileSync(source);
writeFileSync(dest, bytes);

if (bytes.length === 0) {
  throw new Error('entry.png is empty, refusing to submit a blank image');
}
console.log(`wrote ${dest} (${bytes.length} bytes)`);
