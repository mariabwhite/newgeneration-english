#!/usr/bin/env node
/**
 * Batch B · Inject <script src=".../lab-vocab-retrofit.js?v=1"> в уроки
 * которые НЕ имеют класса .vocab-card на своих карточках.
 * Ставим ПЕРЕД lab-vocab-builder.js (обязательно раньше).
 * Skip: уроки где retrofit УЖЕ подключён.
 *
 * Usage:  node scripts/lab-fix-batch-b-vocab.mjs [--dry]
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
  if (/workbook|trainer|teaser/i.test(rel)) return false;
  return true;
}
function relToAssets(lessonFile) {
  const lessonDir = path.dirname(lessonFile);
  const assetsDir = path.join(labRoot, "assets");
  let rel = path.relative(lessonDir, assetsDir).replaceAll("\\", "/");
  if (!rel.startsWith(".")) rel = "./" + rel;
  return rel;
}

const files = walk(labRoot).filter(isLesson);
let added = 0, skippedHasClass = 0, skippedAlready = 0, errors = 0;
const errList = [];

for (const fp of files) {
  try {
    const html = fs.readFileSync(fp, "utf8");

    // 1. Уже подключён — пропускаем
    if (/lab-vocab-retrofit\.js/.test(html)) { skippedAlready++; continue; }

    // 2. Урок уже нормальный (имеет .vocab-card на карточках) — пропускаем
    if (/class\s*=\s*["'][^"']*\bvocab-card\b/.test(html)) { skippedHasClass++; continue; }

    // 3. У урока вообще нет vocab-карточек в HTML — retrofit ему не нужен, пропускаем
    //    (проверяем базовые паттерны)
    const hasVocabPattern = /class\s*=\s*["'][^"']*(flip-card|voc-item|vocab-item|voyager-vocab-item)/.test(html)
      || /id\s*=\s*["'](vocab-grid|vocab-box|vocab)["']/.test(html)
      || /data-en\s*=\s*["'][^"']+["'][^>]*data-ru/.test(html);
    if (!hasVocabPattern) {
      // Нет vocab на странице — retrofit бесполезен, не подключаем
      continue;
    }

    const rel = relToAssets(fp);
    const tag = `<script src="${rel}/lab-vocab-retrofit.js?v=1" defer></script>`;
    let updated;
    if (/<script[^>]+lab-vocab-builder\.js/.test(html)) {
      // Перед lab-vocab-builder
      updated = html.replace(
        /(<script[^>]+lab-vocab-builder\.js[^>]+>\s*<\/script>)/,
        `${tag}\n$1`
      );
    } else if (/<\/body>/i.test(html)) {
      updated = html.replace(/<\/body>/i, `${tag}\n</body>`);
    } else {
      errors++; errList.push(fp + " · no anchor");
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
console.log(`\nBatch B summary${dry ? " (DRY-RUN)" : ""}:`);
console.log(`  added retrofit script:      ${added}`);
console.log(`  already had retrofit:       ${skippedAlready}`);
console.log(`  already had .vocab-card:    ${skippedHasClass}`);
console.log(`  no vocab pattern (skipped): ${files.length - added - skippedAlready - skippedHasClass - errors}`);
console.log(`  errors:                     ${errors}`);
if (errList.length) errList.forEach(e => console.log("    ! " + e));
