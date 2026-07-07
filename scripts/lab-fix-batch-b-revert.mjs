#!/usr/bin/env node
/**
 * Batch B ROLLBACK · удаляет тег <script src=".../lab-vocab-retrofit.js…"> из всех уроков.
 * Ничего кроме этой строки не трогает.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const dry = process.argv.includes("--dry");
const labRoot = path.resolve(__dirname, "..", "lingua-boost-lab");

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (/^(node_modules|\.homework|_codex|.*\.bak)$/i.test(e.name)) continue;
      walk(p, out);
    } else if (e.isFile() && /\.html$/i.test(e.name)) out.push(p);
  }
  return out;
}

let removed = 0;
for (const fp of walk(labRoot)) {
  const html = fs.readFileSync(fp, "utf8");
  if (!/lab-vocab-retrofit/.test(html)) continue;
  const cleaned = html
    .replace(/<script[^>]+lab-vocab-retrofit[^>]+><\/script>\s*\n?/g, "")
    .replace(/\n\s*\n\s*\n/g, "\n\n");
  if (cleaned === html) continue;
  if (!dry) fs.writeFileSync(fp, cleaned, "utf8");
  removed++;
  console.log("  - " + path.relative(labRoot, fp).replaceAll("\\", "/"));
}
console.log(`\nRollback ${dry ? "(DRY)" : ""}: removed retrofit from ${removed} files`);
