// Entry point for the news-image-20261126 entry.
//
// The front page is drawn by draw.py and stored in this repository as
// entry.png. This program only verifies that image against the
// competition's gate (file type by magic bytes, at most 1 MiB, at most
// 1024 pixels a side, whole file with its proper trailer) and copies it
// to the output directory as entry.png. Node standard library only.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const JPEG_MAGIC = Buffer.from([0xff, 0xd8, 0xff]);
const IEND_TRAILER = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);

function fail(message: string): never {
  console.error("gate check failed: " + message);
  process.exit(1);
}

// Read the width and height out of a PNG's IHDR chunk.
function pngDimensions(bytes: Buffer): [number, number] {
  if (bytes.length < 33) fail("PNG too short for an IHDR chunk");
  if (bytes.toString("ascii", 12, 16) !== "IHDR") {
    fail("first PNG chunk is not IHDR");
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  return [width, height];
}

// Read the width and height out of a JPEG's first SOF marker.
function jpegDimensions(bytes: Buffer): [number, number] {
  let offset = 2;
  while (offset + 9 < bytes.length) {
    if (bytes[offset] !== 0xff) fail("bad JPEG marker at offset " + offset);
    const marker = bytes[offset + 1];
    const segmentLength = bytes.readUInt16BE(offset + 2);
    if (segmentLength < 2) fail("bad JPEG segment length");
    // SOF0..SOF3, SOF5..SOF7, SOF9..SOF11, SOF13..SOF15 carry dimensions.
    const isSof =
      marker >= 0xc0 &&
      marker <= 0xcf &&
      marker !== 0xc4 &&
      marker !== 0xc8 &&
      marker !== 0xcc;
    if (isSof) {
      const height = bytes.readUInt16BE(offset + 5);
      const width = bytes.readUInt16BE(offset + 7);
      return [width, height];
    }
    offset += 2 + segmentLength;
  }
  fail("no SOF marker found in JPEG");
}

function main(): void {
  const here = new URL(".", import.meta.url).pathname;
  const source = join(here, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, "entry.png");

  const bytes = readFileSync(source);
  const size = statSync(source).size;
  if (size !== bytes.length) fail("could not read the whole entry file");
  if (size > MAX_BYTES) {
    fail(`entry is ${size} bytes, over the 1 MiB cap`);
  }

  let width: number;
  let height: number;
  if (bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    [width, height] = pngDimensions(bytes);
    if (!bytes.subarray(bytes.length - IEND_TRAILER.length).equals(IEND_TRAILER)) {
      fail("PNG does not end with a whole IEND chunk");
    }
  } else if (bytes.subarray(0, 3).equals(JPEG_MAGIC)) {
    [width, height] = jpegDimensions(bytes);
    if (bytes[bytes.length - 2] !== 0xff || bytes[bytes.length - 1] !== 0xd9) {
      fail("JPEG does not end with its EOI marker");
    }
  } else {
    fail("entry is neither a PNG nor a JPEG by its first bytes");
  }

  if (width > MAX_SIDE || height > MAX_SIDE) {
    fail(`entry is ${width}x${height}, over the 1024 pixel cap`);
  }
  if (width === 0 || height === 0) fail("entry has a zero dimension");

  copyFileSync(source, target);
  console.log(
    `gate passed: ${width}x${height}, ${size} bytes, copied to ${target}`,
  );
}

main();
