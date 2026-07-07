#!/usr/bin/env node
/**
 * Lab Lesson Audit v1 · 2026-07-07
 * Бежит по всем lingua-boost-lab/** урокам, проверяет 45+ пунктов регламента.
 * Выдаёт markdown-таблицу lab-audit-<date>.md
 *
 * Запуск:
 *   node scripts/lab-audit.mjs
 * Опции:
 *   --json     · JSON вместо markdown
 *   --brief    · короткая таблица без деталей
 *   --path X   · путь до сайта, default = ../ (relative to this script)
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const args = process.argv.slice(2);
const outJson = args.includes("--json");
const brief = args.includes("--brief");
const rootIdx = args.indexOf("--path");
const siteRoot = rootIdx >= 0 ? path.resolve(args[rootIdx + 1]) : path.resolve(__dirname, "..");
const labRoot = path.join(siteRoot, "lingua-boost-lab");

// ─────────── FIND LESSONS ───────────
function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      // skip node_modules, .homework, .bak
      if (/^(node_modules|\.homework|_codex|.*\.bak)$/i.test(entry.name)) continue;
      walk(p, out);
    } else if (entry.isFile() && /\.html$/i.test(entry.name) && !/\.bak/i.test(entry.name) && !/\.backup/i.test(entry.name)) {
      out.push(p);
    }
  }
  return out;
}

// Only actual lessons (not premium.html, login.html, index.html, .homework/, etc.)
function isLesson(fp) {
  const rel = path.relative(labRoot, fp).replaceAll("\\", "/");
  const name = path.basename(fp);
  if (["index.html", "premium.html", "login.html"].includes(name) && rel.split("/").length <= 2) return false;
  if (rel.startsWith(".homework/")) return false;
  if (rel.startsWith("assets/")) return false;
  // Workbook / trainer / teaser — не уроки, Маша просила не кошмарить
  if (/workbook|trainer|teaser/i.test(rel)) return false;
  return true;
}

const lessonFiles = walk(labRoot).filter(isLesson);

// ─────────── CHECKS ───────────
// Every check gets a category + label + fn(html, fp) → boolean|string
const checks = [
  // === A · HEAD ===
  { cat: "A · Head",  key: "guard",       label: "premium-lesson-guard.js",           fn: h => /premium-lesson-guard\.js/.test(h) },
  { cat: "A · Head",  key: "viewport",    label: "meta viewport",                     fn: h => /<meta[^>]+name=["']viewport/.test(h) },
  { cat: "A · Head",  key: "description", label: "meta description",                  fn: h => /<meta[^>]+name=["']description["']/.test(h) },
  { cat: "A · Head",  key: "robots",      label: "meta robots=noindex",               fn: h => /<meta[^>]+name=["']robots["'][^>]*noindex/.test(h) },
  { cat: "A · Head",  key: "gfonts",      label: "Google Fonts preconnect",           fn: h => /fonts\.googleapis\.com/.test(h) && /fonts\.gstatic\.com/.test(h) },
  { cat: "A · Head",  key: "canonCss",    label: "canon-L.css?v=15+",                 fn: h => (h.match(/canon-L\.css\?v=(\d+)/) || [])[1] >= 15 },
  { cat: "A · Head",  key: "canonJs",     label: "canon-L.js?v=5+ defer",             fn: h => (h.match(/canon-L\.js\?v=(\d+)[^>]+defer/) || [])[1] >= 5 },
  { cat: "A · Head",  key: "codexCorner", label: "N-mark clip-path corner style",     fn: h => /codex-white-corner-logo/.test(h) },

  // === B · TOPBAR + HERO ===
  { cat: "B · Topbar", key: "labPilotCss", label: "lab-pilot.css?v=7+",               fn: h => (h.match(/lab-pilot\.css\?v=(\d+)/) || [])[1] >= 7 },
  { cat: "B · Topbar", key: "skipLink",    label: "skip-link canon-l-skip-link",      fn: h => /class=["'][^"']*canon-l-skip-link/.test(h) },
  { cat: "B · Topbar", key: "topbar",      label: "canon-l-topbar",                   fn: h => /class=["'][^"']*canon-l-topbar/.test(h) },
  { cat: "B · Topbar", key: "brandMark",   label: "canon-l-mark N-mark",              fn: h => /canon-l-mark/.test(h) },
  { cat: "B · Topbar", key: "topnav",      label: "topnav canon-l-nav",               fn: h => /class=["'][^"']*canon-l-nav/.test(h) },
  { cat: "B · Topbar", key: "toolCatalog", label: "canon-l-pill каталог link",        fn: h => /premium\.html/.test(h) && /canon-l-pill/.test(h) },
  { cat: "B · Topbar", key: "heroImg",     label: "hero <img> (не CSS-градиент)",     fn: h => /class=["'][^"']*hero-bg/.test(h) || /<img[^>]+hero-banner/.test(h) },
  { cat: "B · Topbar", key: "heroOverlay", label: "hero-overlay текст",               fn: h => /class=["'][^"']*hero-overlay/.test(h) },

  // === C · TABS / PROGRESS ===
  { cat: "C · Nav",   key: "tabs",       label: "tabs Урок/Домашка (canon)",          fn: h => /data-tab=["']lesson/.test(h) && /data-tab=["']homework/.test(h) },
  { cat: "C · Nav",   key: "progressDots", label: "progress dots навигация",           fn: h => /class=["']dots/.test(h) || /id=["']dots/.test(h) },

  // === D · SECTIONS + BUTTONS ===
  { cat: "D · Body",  key: "sectionsN",    label: "≥6 section с id block-N",           fn: h => (h.match(/id=["']block-\d+/g) || []).length >= 6 },
  { cat: "D · Body",  key: "sectionHead",  label: "section-head + numbered n",         fn: h => /class=["']section-head/.test(h) && /class=["']n["']/.test(h) },
  { cat: "D · Body",  key: "warmup",       label: "warm-up с data-say TTS",            fn: h => /data-say/.test(h) },

  // === E · VOCAB BUILDER (двусторонний) ===
  { cat: "E · Vocab", key: "vocabCard",    label: "class .vocab-card (не только flip)", fn: h => /class=["'][^"']*vocab-card/.test(h) },
  { cat: "E · Vocab", key: "vocabWord",    label: "class .word внутри карточки",       fn: h => /class=["'][^"']*\bword\b/.test(h) },
  { cat: "E · Vocab", key: "vocabMeaning", label: "class .meaning или .ru",            fn: h => /class=["'][^"']*(?:meaning|\bru\b)/.test(h) },
  { cat: "E · Vocab", key: "vocabEx",      label: "class .ex или .example",            fn: h => /class=["'][^"']*(?:\bex\b|example)/.test(h) },
  { cat: "E · Vocab", key: "vocabBuilder", label: "lab-vocab-builder.js?v=46+",        fn: h => (h.match(/lab-vocab-builder\.js\?v=(\d+)/) || [])[1] >= 46 },

  // === F · HOMEWORK FLOW ===
  { cat: "F · HW",    key: "labTabs",      label: "lab-tabs.js?v=11+ (Урок/Домашка)",  fn: h => (h.match(/lab-tabs\.js\?v=(\d+)/) || [])[1] >= 11 },
  { cat: "F · HW",    key: "labHomework",  label: "lab-homework.js?v=32+",             fn: h => (h.match(/lab-homework\.js\?v=(\d+)/) || [])[1] >= 32 },
  { cat: "F · HW",    key: "hwButtons",    label: "«в домашку» кнопки у секций",       fn: h => /в домашку|home\s*work|lab-hw-add|add.to.homework/i.test(h) || /lab-homework/.test(h) },

  // === G · GRADER (Task 4 · только для speaking) ===
  { cat: "G · Coach", key: "grader",       label: "AI Live Coach (grader div)",        fn: h => /id=["']t4-grader/.test(h) || /class=["'][^"']*grader\b/.test(h) },
  { cat: "G · Coach", key: "graderCriteria", label: "criteria checklist data-cid",     fn: h => /data-cid=/.test(h) },
  { cat: "G · Coach", key: "shareCode",    label: "share-code для teacher mirror",     fn: h => /id=["']share-code/.test(h) || /class=["'][^"']*share-code/.test(h) },
  { cat: "G · Coach", key: "peerjs",       label: "peerjs CDN (для teacher mirror)",    fn: h => /peerjs/.test(h) },
  { cat: "G · Coach", key: "webSpeech",    label: "webkitSpeechRecognition / SR",       fn: h => /webkitSpeechRecognition|SpeechRecognition/.test(h) },

  // === H · SESSION PERSISTENCE ===
  { cat: "H · Persist", key: "localStorage", label: "localStorage.setItem где-то",     fn: h => /localStorage\.setItem|localStorage\.getItem/.test(h) },
  { cat: "H · Persist", key: "labPilotJs",  label: "lab-pilot.js?v=3+ (session state)", fn: h => (h.match(/lab-pilot\.js\?v=(\d+)/) || [])[1] >= 3 },
  { cat: "H · Persist", key: "labSync",     label: "lab-sync.js?v=16+ (Supabase live)", fn: h => (h.match(/lab-sync\.js\?v=(\d+)/) || [])[1] >= 16 },
  { cat: "H · Persist", key: "labMicWpm",   label: "lab-mic-wpm.js (для speaking)",    fn: h => /lab-mic-wpm\.js/.test(h) },
  { cat: "H · Persist", key: "labAiFeed",   label: "lab-ai-feedback.js",               fn: h => /lab-ai-feedback\.js/.test(h) },

  // === I · METADATA + A11Y ===
  { cat: "I · Meta",  key: "title",        label: "<title> непустой",                  fn: h => /<title>[^<]{5,}<\/title>/.test(h) },
  { cat: "I · Meta",  key: "altAll",       label: "все <img> имеют alt",               fn: h => {
      const imgs = h.match(/<img\b[^>]*>/gi) || [];
      if (!imgs.length) return "n/a";
      return imgs.every(img => /alt=["'][^"']+["']/.test(img));
    } },
  { cat: "I · Meta",  key: "lang",         label: "html lang=\"en\" или \"ru\"",       fn: h => /<html[^>]+lang=/.test(h) },

  // === J · MOBILE ===
  { cat: "J · Mobile", key: "labMobileHint", label: "медиа-запросы для мобилки",       fn: h => /@media\s*\([^)]*max-width/.test(h) },

  // === K · EPILOGUE ===
  { cat: "K · Tail",  key: "footer",       label: "<footer> внизу",                    fn: h => /<footer\b/i.test(h) },
];

// ─────────── PREMIUM CATALOG CHECK ───────────
const premiumJson = path.join(labRoot, "premium-lessons.json");
const premiumHtml = path.join(labRoot, "premium.html");
let premiumIds = new Set();
let premiumUrls = new Set();
if (fs.existsSync(premiumJson)) {
  try {
    const data = JSON.parse(fs.readFileSync(premiumJson, "utf8"));
    data.filter(l => l.published).forEach(l => {
      premiumIds.add(l.id);
      premiumUrls.add(l.url);
    });
  } catch (e) { console.warn("cannot read premium-lessons.json:", e.message); }
}
let premiumHtmlContent = fs.existsSync(premiumHtml) ? fs.readFileSync(premiumHtml, "utf8") : "";

function lessonInPremium(fp) {
  const rel = path.relative(labRoot, path.dirname(fp)).replaceAll("\\", "/");
  // check URL match (usually /lingua-boost-lab/b1/xxx/ or /lingua-boost-lab/xxx/)
  const candidates = [
    `/lingua-boost-lab/${rel}/`,
    `./${rel}/`,
    `./lingua-boost-lab/${rel}/`,
    `https://newgeneration-english.ru/lingua-boost-lab/${rel}/`,
  ];
  return candidates.some(c => premiumUrls.has(c));
}
function lessonHasCardHtml(fp) {
  const rel = path.relative(labRoot, path.dirname(fp)).replaceAll("\\", "/");
  const id = path.basename(path.dirname(fp));
  return premiumHtmlContent.includes(`data-id="${id}"`);
}

// ─────────── RUN ───────────
const rows = [];
for (const fp of lessonFiles) {
  const html = fs.readFileSync(fp, "utf8");
  const rel = path.relative(labRoot, fp).replaceAll("\\", "/");
  const row = { file: rel, size: html.length };
  let hits = 0, misses = 0, na = 0;
  for (const c of checks) {
    let res;
    try { res = c.fn(html, fp); } catch (e) { res = false; }
    row[c.key] = res;
    if (res === "n/a") na++;
    else if (res) hits++;
    else misses++;
  }
  row.inPremium = lessonInPremium(fp);
  row.inPremiumCard = lessonHasCardHtml(fp);
  if (row.inPremium) hits++; else misses++;
  if (row.inPremiumCard) hits++; else misses++;
  row.hits = hits;
  row.misses = misses;
  row.na = na;
  row.pct = Math.round((hits / (checks.length + 2)) * 100);
  rows.push(row);
}
rows.sort((a, b) => b.pct - a.pct);

// ─────────── OUTPUT ───────────
if (outJson) {
  console.log(JSON.stringify({ checks: checks.map(c => ({ key: c.key, label: c.label, cat: c.cat })), rows }, null, 2));
  process.exit(0);
}

const now = new Date().toISOString().slice(0, 16).replace("T", " ");
let md = `# 🔬 Lab Lesson Audit · ${now}\n\n`;
md += `Всего уроков: **${rows.length}**\n`;
md += `Проверок на урок: **${checks.length + 2}** (${checks.length} по регламенту + 2 catalog)\n\n`;

md += `## 📊 Ranking · сверху = меньше багов\n\n`;
md += `| # | Урок | Score | Hits / Misses | Fix priority |\n|---|---|---|---|---|\n`;
rows.forEach((r, i) => {
  const prio = r.pct >= 85 ? "🟢" : r.pct >= 65 ? "🟡" : r.pct >= 45 ? "🟠" : "🔴";
  md += `| ${i + 1} | \`${r.file}\` | **${r.pct}%** ${prio} | ${r.hits} / ${r.misses}${r.na ? ` (${r.na} n/a)` : ""} | ${r.pct < 65 ? "**urgent**" : r.pct < 85 ? "medium" : "low"} |\n`;
});

if (!brief) {
  md += `\n## 🔍 Что не хватает по категориям (топ-20 частых мисов)\n\n`;
  const missCount = {};
  for (const c of checks) missCount[c.key] = 0;
  for (const r of rows) {
    for (const c of checks) if (r[c.key] === false) missCount[c.key]++;
  }
  const top = Object.entries(missCount).sort((a, b) => b[1] - a[1]).slice(0, 20);
  md += `| Пункт | Категория | Не хватает в |\n|---|---|---|\n`;
  for (const [key, n] of top) {
    if (n === 0) continue;
    const c = checks.find(x => x.key === key);
    md += `| ${c.label} | ${c.cat} | ${n} уроков |\n`;
  }

  md += `\n## 📋 Детальная карта · урок × 45 пунктов\n\n`;
  md += `Легенда: ✓ = есть, ✗ = нет, • = n/a\n\n`;
  md += `| Урок |`;
  for (const c of checks) md += ` ${c.key} |`;
  md += ` premJson | premHtml |\n`;
  md += `|---|`;
  for (const c of checks) md += `---|`;
  md += `---|---|\n`;
  for (const r of rows) {
    md += `| \`${r.file.replace("/index.html", "")}\` |`;
    for (const c of checks) {
      const v = r[c.key];
      md += v === "n/a" ? " • |" : v ? " ✓ |" : " ✗ |";
    }
    md += (r.inPremium ? " ✓ |" : " ✗ |") + (r.inPremiumCard ? " ✓ |" : " ✗ |") + "\n";
  }

  md += `\n## 🧩 Легенда категорий проверок\n\n`;
  const grouped = {};
  for (const c of checks) {
    if (!grouped[c.cat]) grouped[c.cat] = [];
    grouped[c.cat].push(c);
  }
  for (const [cat, list] of Object.entries(grouped)) {
    md += `**${cat}**\n`;
    for (const c of list) md += `- \`${c.key}\` — ${c.label}\n`;
    md += `\n`;
  }
}

const outPath = path.join(siteRoot, "..", `lab-audit-${now.replace(/[: ]/g, "-")}.md`);
fs.writeFileSync(outPath, md, "utf8");
console.log(`Audited ${rows.length} lessons · ${checks.length + 2} checks each`);
console.log(`Report → ${outPath}`);
console.log(`Top 5:`);
rows.slice(0, 5).forEach(r => console.log(`  ${r.pct}%  ${r.file}`));
console.log(`Bottom 5:`);
rows.slice(-5).forEach(r => console.log(`  ${r.pct}%  ${r.file}`));
