#!/usr/bin/env node
/**
 * Batch A · Auto-inject <script src="…/lab-tabs.js?v=11" defer></script>
 * Before closing </body> or right after other lab-* scripts.
 * Skips lessons that already have any lab-tabs.js.
 *
 * Usage:  node scripts/lab-fix-batch-a-tabs.mjs [--dry]
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
    } else if (e.isFile() && /\.html$/i.test(e.name) && !/\.bak|\.backup/i.test(e.name)) {
      out.push(p);
    }
  }
  return out;
}
function isLesson(fp) {
  const rel = path.relative(labRoot, fp).replaceAll("\\", "/");
  const name = path.basename(fp);
  if (["index.html", "premium.html", "login.html"].includes(name) && rel.split("/").length <= 2) return false;
  if (rel.startsWith(".homework/")) return false;
  if (rel.startsWith("assets/")) return false;
  // Не трогаем воркбуки, тренажёры и обрезки — они не полноценные уроки (по правилу Маши)
  if (/workbook|trainer|teaser/i.test(rel)) return false;
  return true;
}
// pick right relative path to assets/lab-tabs.js from lesson file
function relToAssets(lessonFile) {
  const lessonDir = path.dirname(lessonFile);
  const assetsDir = path.join(labRoot, "assets");
  let rel = path.relative(lessonDir, assetsDir).replaceAll("\\", "/");
  if (!rel.startsWith(".")) rel = "./" + rel;
  return rel;
}

const files = walk(labRoot).filter(isLesson);
let added = 0, skipped = 0, errors = 0;
const errList = [];

for (const fp of files) {
  try {
    const html = fs.readFileSync(fp, "utf8");
    if (/lab-tabs\.js/.test(html)) { skipped++; continue; }
    // Find anchor: prefer right after lab-homework OR right before </body>
    const rel = relToAssets(fp);
    const tag = `<script src="${rel}/lab-tabs.js?v=11" defer></script>`;
    let updated;
    if (/<script[^>]+lab-homework\.js/.test(html)) {
      updated = html.replace(/(<script[^>]+lab-homework\.js[^>]+>\s*<\/script>)/, `<script src="${rel}/lab-tabs.js?v=11" defer></script>\n$1`);
    } else if (/<\/body>/i.test(html)) {
      updated = html.replace(/<\/body>/i, `${tag}\n</body>`);
    } else {
      errors++; errList.push(fp + " · no <body> or lab-homework anchor");
      continue;
    }
    if (updated === html) { errors++; errList.push(fp + " · replace failed"); continue; }
    if (!dry) fs.writeFileSync(fp, updated, "utf8");
    added++;
    console.log(`  + ${path.relative(labRoot, fp).replaceAll("\\","/")}`);
  } catch (e) {
    errors++; errList.push(fp + " · " + e.message);
  }
}
console.log(`\nBatch A summary${dry ? " (DRY-RUN)" : ""}:`);
console.log(`  added:   ${added}`);
console.log(`  skipped (already had lab-tabs.js): ${skipped}`);
console.log(`  errors:  ${errors}`);
if (errList.length) errList.forEach(e => console.log("    ! " + e));
