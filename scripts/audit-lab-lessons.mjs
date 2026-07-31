#!/usr/bin/env node
/*
 * scripts/audit-lab-lessons.mjs
 *
 * Быстрая проверка каждого Lab-урока на соответствие эталонному набору скриптов.
 * Раскатывать после каждой волны новых уроков + автоматически перед push.
 *
 * Usage:
 *   node scripts/audit-lab-lessons.mjs              # audit all lessons
 *   node scripts/audit-lab-lessons.mjs --new-only   # only lessons created last 24h (git)
 *   node scripts/audit-lab-lessons.mjs --strict     # fail if any lesson missing critical scripts
 *
 * Эталонный набор (актуален на 2026-07-13):
 *  Critical (обязательны на КАЖДОМ premium-lesson):
 *    - premium-lesson-guard.js
 *  Standard Lab lesson (для full-feature уроков):
 *    - lab-persist.js?v=3
 *    - lab-homework.js?v=42
 *    - lab-send-pill.js?v=3
 *    - lab-tabs.js?v=12
 *    - lab-sync.js?v=17
 *    - lab-total.js?v=4
 *    - lab-pilot.js?v=3
 *    - lab-mic-wpm.js?v=1
 *    - lab-ai-feedback.js?v=6
 *    - lab-telemost.js?v=1
 *    - lab-coach-persist.js?v=1
 *    - lab-clean-bottom-dock.js?v=1
 *  Optional (по типу урока):
 *    - lab-vocab-builder.js?v=53   (если есть Vocabulary секция)
 *    - lab-vocab-saver.js?v=2      (если есть .tr[data-ru] hover-translations)
 *
 * Workbook / practice / mini-lesson может подключать сокращённый набор:
 *    persist + send-pill + total + homework + tabs + clean-bottom-dock
 *    + premium-lesson-guard если урок в premium-lessons.json
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const publicRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const labRoot = path.join(publicRoot, "site-public-clean", "lingua-boost-lab");
const manifestPath = path.join(labRoot, "premium-lessons.json");

const REQUIRED_STANDARD = {
  "premium-lesson-guard.js": null,          // no ?v= needed
  "lab-persist.js":          "v=3",
  "lab-homework.js":         "v=42",
  "lab-send-pill.js":        "v=3",
  "lab-tabs.js":             "v=12",
  "lab-sync.js":             "v=17",
  "lab-total.js":            "v=4",
  "lab-pilot.js":            "v=3",
  "lab-mic-wpm.js":          "v=1",
  "lab-ai-feedback.js":      "v=6",
  "lab-telemost.js":         "v=1",
  "lab-coach-persist.js":    "v=1",
  "lab-clean-bottom-dock.js":"v=1",
};

const REQUIRED_WORKBOOK = {
  "lab-persist.js":          "v=3",
  "lab-homework.js":         "v=42",
  "lab-send-pill.js":        "v=3",
  "lab-tabs.js":             "v=12",
  "lab-total.js":            "v=4",
  "lab-clean-bottom-dock.js":"v=1",
};

const args = new Set(process.argv.slice(2));
const strict = args.has("--strict");
const newOnly = args.has("--new-only");

// Catalogue / landing / entry files that are NOT premium lessons — skip in audit
const NON_LESSON = new Set([
  "index.html", "premium.html", "login.html", "find-and-say-teaser.html",
  "_boot-eating.html",
]);

function walkHtml(root) {
  const out = [];
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const p = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === "assets" || entry.name.startsWith("_")) continue;
        walk(p);
      } else if (entry.name.endsWith(".html")) {
        // Skip .homework/index.html stubs — the real homework runner lives in /lingua-boost-lab/.homework/
        if (dir.endsWith(".homework") || dir.endsWith(".homework" + path.sep)) continue;
        // Skip root catalog/landing pages
        const rel = path.relative(root, p).replaceAll(path.sep, "/");
        if (!rel.includes("/") && NON_LESSON.has(entry.name)) continue;
        if (entry.name === "index.html" || (entry.name.endsWith(".html") && dir === root)) {
          out.push(p);
        }
      }
    }
  }
  walk(root);
  return out;
}

function checkLesson(filePath) {
  const text = fs.readFileSync(filePath, "utf-8");
  const rel = path.relative(labRoot, filePath).replaceAll(path.sep, "/");
  const isWorkbook = /^practice\//.test(rel) || rel.includes("-workbook-");
  const spec = isWorkbook ? REQUIRED_WORKBOOK : REQUIRED_STANDARD;

  const missing = [];
  const stale = [];
  for (const [script, needVer] of Object.entries(spec)) {
    const m = text.match(new RegExp(script.replace(/\./g, "\\.") + "\\?v=(\\d+)"));
    const mNoVer = text.match(new RegExp(script.replace(/\./g, "\\.") + "(?![\\w?])"));
    if (!m && !mNoVer) {
      missing.push(script);
    } else if (needVer && m && `v=${m[1]}` !== needVer) {
      stale.push(`${script} → v=${m[1]} (want ${needVer})`);
    } else if (needVer && !m && mNoVer) {
      stale.push(`${script} → no ?v= (want ${needVer})`);
    }
  }
  return { rel, isWorkbook, missing, stale };
}

let lessons = walkHtml(labRoot);
if (newOnly) {
  try {
    const gitOut = execSync(
      `git log --since="24 hours ago" --diff-filter=A --name-only --pretty=format: -- 'lingua-boost-lab/**/*.html'`,
      { cwd: path.join(publicRoot, "site-public-clean"), encoding: "utf-8" }
    );
    const newSet = new Set(gitOut.split("\n").filter(Boolean).map((s) => s.trim()));
    lessons = lessons.filter((p) => newSet.has(path.relative(publicRoot + path.sep + "site-public-clean", p).replaceAll(path.sep, "/")));
  } catch (e) {
    console.error("git log failed, showing all lessons");
  }
}

let hasError = false;
let totalOk = 0;
let totalWarn = 0;
let totalFail = 0;
console.log(`\n📚 Audit ${lessons.length} lesson files`);
console.log("=".repeat(90));

for (const p of lessons) {
  const { rel, isWorkbook, missing, stale } = checkLesson(p);
  const tag = isWorkbook ? "WB" : "LB";
  if (!missing.length && !stale.length) {
    totalOk++;
    // uncomment for verbose ok
    // console.log(`✅ [${tag}] ${rel}`);
    continue;
  }
  if (missing.length > 0 || stale.length > 0) {
    console.log(`\n⚠  [${tag}] ${rel}`);
    if (missing.length) {
      console.log(`   MISSING: ${missing.join(", ")}`);
      if (missing.includes("premium-lesson-guard.js")) hasError = true;
      totalFail += missing.length;
    }
    if (stale.length) {
      console.log(`   STALE: ${stale.join(", ")}`);
      totalWarn += stale.length;
    }
  }
}

console.log("\n" + "=".repeat(90));
console.log(`Summary · OK: ${totalOk} · Stale: ${totalWarn} · Missing: ${totalFail}`);

if (strict && hasError) {
  console.error("\n❌ Strict mode: critical scripts missing (premium-lesson-guard)");
  process.exit(1);
}
