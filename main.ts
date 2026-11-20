import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here: string = path.dirname(fileURLToPath(import.meta.url));
const srcPath: string = path.join(here, "entry.png");

const envDir: string = (process.env.MAKEFUN_OUTPUT_DIR ?? "").trim();
const outDir: string = envDir.length > 0 ? envDir : path.join(process.cwd(), "output");
const dstPath: string = path.join(outDir, "entry.png");

fs.mkdirSync(outDir, { recursive: true });
fs.copyFileSync(srcPath, dstPath);

const srcBytes: Buffer = fs.readFileSync(srcPath);
const dstBytes: Buffer = fs.readFileSync(dstPath);

if (Buffer.compare(srcBytes, dstBytes) !== 0) {
  console.error(`Error: copied file ${dstPath} differs byte-for-byte from ${srcPath}`);
  process.exit(1);
}

console.log(`Verified ${dstPath} matches ${srcPath} (${srcBytes.length} bytes).`);
