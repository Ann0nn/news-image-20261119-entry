// news-image-20261119 entry driver (Node 22, standard library only).
// The entry image is the entry.png beside this file: a one-page newspaper
// summary of the world news of Thursday 19 November 2026, drawn by
// src/render.py from headlines researched that day. The program copies it
// to /output/entry.png. A plain copy is deterministic: every run writes
// the same bytes, as the competition requires.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoDir = dirname(fileURLToPath(import.meta.url));
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const target = join(outputDir, 'entry.png');
copyFileSync(join(repoDir, 'entry.png'), target);

// Confirm the copy landed: a missing or empty output would fail the gate.
const { size } = statSync(target);
if (size === 0) throw new Error('entry.png copied but empty');
console.log(`wrote ${target} (${size} bytes)`);
