// Entry for make.fun's "Sum up 26 November's world news in one image".
//
// The picture itself is entry.png beside this file: a one-page broadsheet
// composed by draw.py (kept in this repository) from the day's reporting,
// with AI-generated front-page art (hero.png). The grader runs this
// program with no network, so all it does is copy that image to the
// output path.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1_048_576; // the gate's 1 MiB cap
const MAX_SIDE = 1024;       // the gate's 1024-by-1024 cap

// Fail loudly rather than copy an image the gate would refuse: it must be
// a whole PNG or JPEG (told apart by its first bytes), within the size
// caps. A PNG's IHDR names its dimensions; a JPEG is trusted to the gate.
function checkImage(bytes: Buffer): void {
  if (bytes.length > MAX_BYTES) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
  }
  const isPng = bytes.subarray(0, 8).equals(
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
  const isJpeg = bytes[0] === 0xff && bytes[1] === 0xd8;
  if (isPng) {
    const width = bytes.readUInt32BE(16);
    const height = bytes.readUInt32BE(20);
    if (width > MAX_SIDE || height > MAX_SIDE) {
      throw new Error(`entry.png is ${width}x${height}, over the 1024 cap`);
    }
    // A whole PNG ends with its IEND chunk; a truncated file is refused.
    const iend = bytes.subarray(bytes.length - 12);
    if (!iend.subarray(4, 8).equals(Buffer.from('IEND'))) {
      throw new Error('entry.png is truncated: no IEND chunk at the end');
    }
  } else if (!isJpeg) {
    throw new Error('entry.png is neither a PNG nor a JPEG');
  }
}

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);
checkImage(bytes);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(source, join(outDir, 'entry.png'));
console.log(`copied entry.png (${bytes.length} bytes) to ${join(outDir, 'entry.png')}`);
