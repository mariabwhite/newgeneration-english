#!/usr/bin/env node
// Voyager vocab compendium L1+L2 → HTML + Quizlet TSV
// run: node scripts/build-voyager-vocab-compendium.js
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const L1 = path.join(ROOT, 'lingua-boost-lab', 'b2-plus', 'voyager-l1-time-travel', 'index.html');
const L2 = path.join(ROOT, 'lingua-boost-lab', 'b2-plus', 'voyager-l2-are-we-alone', 'index.html');
const OUT_DIR = path.join(process.env.USERPROFILE || '', 'Downloads');

function extractFlipCards(html) {
  const out = [];
  // flip-card block: data-say="EN" ... pos">POS</div> ... ru">RU</div><div>DEF</div>
  const re = /<div class="flip-card"><div class="flip-inner">\s*<div class="flip-front"><div><span class="say-word" data-say="([^"]+)">[^<]+<\/span><\/div><div class="pos">([^<]*)<\/div><\/div>\s*<div class="flip-back"><div class="ru">([^<]+)<\/div><div>([^<]*)<\/div>/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    out.push({ en: m[1].trim(), pos: m[2].trim(), ru: m[3].trim(), def: (m[4] || '').trim() });
  }
  return out;
}

function extractInlineTr(html) {
  // <span class="tr" data-ru="RU">EN</span>
  const out = [];
  const re = /<span class="tr" data-ru="([^"]+)">([^<]+)<\/span>/g;
  const seen = new Set();
  let m;
  while ((m = re.exec(html)) !== null) {
    const en = m[2].trim();
    const ru = m[1].trim();
    const key = en.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({ en, ru, def: '' });
  }
  return out;
}

const html1 = fs.readFileSync(L1, 'utf8');
const html2 = fs.readFileSync(L2, 'utf8');

const l1cards = extractFlipCards(html1);
const l1tr = extractInlineTr(html1);
const l2cards = extractFlipCards(html2);
const l2tr = extractInlineTr(html2);

// Deduplicate inline by EN against card list
function dedupeAgainst(list, refList) {
  const refSet = new Set(refList.map(r => r.en.toLowerCase()));
  return list.filter(x => !refSet.has(x.en.toLowerCase()));
}
const l1trUnique = dedupeAgainst(l1tr, l1cards);
const l2trUnique = dedupeAgainst(l2tr, l2cards);

// HTML compendium
const escapeHtml = s => String(s || '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function renderSection(title, cards, inline) {
  const cardRows = cards.map(c => `
    <tr><td class="en">${escapeHtml(c.en)}</td><td class="pos">${escapeHtml(c.pos)}</td><td class="ru">${escapeHtml(c.ru)}</td><td class="def">${escapeHtml(c.def)}</td></tr>`).join('');
  const trRows = inline.map(c => `
    <tr><td class="en">${escapeHtml(c.en)}</td><td class="pos">—</td><td class="ru">${escapeHtml(c.ru)}</td><td class="def">из текста (in-line)</td></tr>`).join('');
  return `
  <section>
    <h2>${escapeHtml(title)}</h2>
    <h3>Главные карточки <span class="cnt">(${cards.length})</span></h3>
    <table><thead><tr><th>EN</th><th>POS</th><th>RU</th><th>DEF</th></tr></thead><tbody>${cardRows}</tbody></table>
    <h3 style="margin-top:18px">Слова из текста <span class="cnt">(${inline.length})</span></h3>
    <table><thead><tr><th>EN</th><th>POS</th><th>RU</th><th>DEF</th></tr></thead><tbody>${trRows}</tbody></table>
  </section>`;
}

const html = `<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Voyager L1 + L2 · vocab compendium · NG English</title>
<style>
:root{--bg:#0b1c33;--surface:#fff;--text:#0b1c33;--muted:#4b5b75;--accent:#2563eb;--border:#dce7f3}
*{box-sizing:border-box;margin:0;padding:0}
body{background:linear-gradient(135deg,#0b1c33 0%,#1e3a8a 100%);font:14px/1.55 -apple-system,Segoe UI,system-ui,sans-serif;color:var(--text);min-height:100vh;padding:24px}
.wrap{max-width:1100px;margin:0 auto;background:var(--surface);border-radius:16px;padding:32px 36px;box-shadow:0 18px 60px rgba(0,0,0,.28)}
h1{font-size:1.85rem;margin-bottom:6px;color:var(--bg);letter-spacing:-.01em}
.lede{color:var(--muted);font-size:.96rem;margin-bottom:22px;line-height:1.55}
section{margin-top:30px;border-top:1px solid var(--border);padding-top:22px}
section:first-of-type{border-top:none;padding-top:0;margin-top:18px}
h2{font-size:1.18rem;color:var(--accent);letter-spacing:-.005em;margin-bottom:10px}
h3{font-size:.92rem;text-transform:uppercase;letter-spacing:.14em;color:var(--muted);margin:14px 0 8px}
.cnt{color:var(--muted);font-weight:400;letter-spacing:0}
table{width:100%;border-collapse:collapse;margin-bottom:6px;background:#fff;border:1px solid var(--border);border-radius:10px;overflow:hidden}
th,td{padding:9px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--border);font-size:.92rem}
th{background:#f3f7fc;font-weight:700;color:var(--bg);font-size:.78rem;text-transform:uppercase;letter-spacing:.10em}
td.en{font-weight:700;color:#0a3a8a;width:24%}
td.pos{font-family:Consolas,monospace;font-size:.78rem;color:var(--muted);width:7%;text-transform:uppercase}
td.ru{color:#1b1b22;width:34%}
td.def{color:var(--muted);font-size:.86rem;width:35%}
tr:last-child td{border-bottom:none}
.footer{margin-top:30px;padding-top:18px;border-top:1px solid var(--border);font-size:.82rem;color:var(--muted);text-align:center}
@media print{
  body{background:#fff;padding:0}
  .wrap{box-shadow:none;border-radius:0;max-width:none;padding:24px}
}
</style>
</head>
<body>
<div class="wrap">
  <h1>📒 Voyager · vocab compendium · L1 + L2</h1>
  <p class="lede">Полный словарь двух пройденных эпизодов: <strong>Voyager L1 — The Watchmaker</strong> + <strong>Voyager L2 — Are we alone?</strong>. Сначала — главные карточки урока, ниже — все слова, подсвеченные внутри текста (in-line). Для печати: Ctrl/Cmd+P → Сохранить как PDF.</p>
  ${renderSection('Voyager L1 · The Watchmaker · Time travel + neutrinos', l1cards, l1trUnique)}
  ${renderSection('Voyager L2 · Are we alone? · Mia\'s signal', l2cards, l2trUnique)}
  <div class="footer">
    NG English · LinguaBoost Lab · Voyager series · vocab compendium · ${new Date().toISOString().slice(0,10)}<br>
    Total: ${l1cards.length + l1trUnique.length + l2cards.length + l2trUnique.length} word/phrase pairs.
  </div>
</div>
</body>
</html>`;

// Quizlet TSV: EN<TAB>RU (one per line)
const all = [...l1cards, ...l1trUnique, ...l2cards, ...l2trUnique];
// Dedupe by EN across both lessons (keep first definition)
const seen = new Map();
all.forEach(c => {
  const k = c.en.toLowerCase();
  if (!seen.has(k)) seen.set(k, c);
});
const tsvLines = [...seen.values()].map(c => `${c.en}\t${c.ru}`);
const tsv = tsvLines.join('\n');

const stamp = new Date().toISOString().slice(0,10);
const htmlOut = path.join(OUT_DIR, `Voyager_L1_L2_vocab_compendium_${stamp}.html`);
const tsvOut = path.join(OUT_DIR, `Voyager_L1_L2_vocab_quizlet_${stamp}.txt`);
fs.writeFileSync(htmlOut, html, 'utf8');
fs.writeFileSync(tsvOut, tsv, 'utf8');

console.log('=== Voyager L1+L2 vocab compendium ===');
console.log('L1 main cards:', l1cards.length);
console.log('L1 in-line vocab:', l1trUnique.length);
console.log('L2 main cards:', l2cards.length);
console.log('L2 in-line vocab:', l2trUnique.length);
console.log('Total unique pairs:', tsvLines.length);
console.log('HTML →', htmlOut);
console.log('TSV  →', tsvOut);
