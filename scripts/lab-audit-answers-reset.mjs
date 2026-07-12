#!/usr/bin/env node
/**
 * Проходит по всем урокам и ищет секции с автопроверкой,
 * у которых НЕТ кнопок «Show answers» или «Reset».
 * Выдаёт отчёт lab-answers-reset-audit-<date>.md
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const labRoot = path.resolve(__dirname, "..", "lingua-boost-lab");

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (/^(node_modules|\.homework|_codex|.*\.bak)$/i.test(e.name)) continue;
      walk(p, out);
    } else if (e.isFile() && /\.html$/i.test(e.name) && !/\.bak|\.backup/i.test(e.name)) out.push(p);
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

const rows = [];
for (const fp of walk(labRoot).filter(isLesson)) {
  const html = fs.readFileSync(fp, "utf8");
  // Признак что в уроке ЕСТЬ автопроверка
  const hasCheck = /data-answer=|data-correct=|check-btn/.test(html);
  if (!hasCheck) continue;
  const showBtns = (html.match(/(?:Show answers|показать ответ|show[- _]answer|reveal[- _]answer|Показать ключ)/gi) || []).length;
  const resetBtns = (html.match(/(?:🔄 Reset|Reset|Сбросить|Очистить|reset-btn)/g) || []).length;
  const dataAnswer = (html.match(/data-answer=/g) || []).length;
  const dataCorrect = (html.match(/data-correct="true"/g) || []).length;
  const checkBtns = (html.match(/check-btn/g) || []).length;
  rows.push({
    file: path.relative(labRoot, fp).replaceAll("\\","/"),
    hasShow: showBtns > 0,
    hasReset: resetBtns > 0,
    showBtns, resetBtns, dataAnswer, dataCorrect, checkBtns
  });
}
rows.sort((a,b) => (a.hasShow?1:0)*2 + (a.hasReset?1:0) - ((b.hasShow?1:0)*2 + (b.hasReset?1:0)));

const now = new Date().toISOString().slice(0,16).replace('T',' ');
let md = `# Lab · Show answers + Reset audit · ${now}\n\n`;
md += `Уроки где есть автопроверка (\`data-answer\` / \`data-correct\` / \`check-btn\`):\n\n`;
md += `| Урок | Show | Reset | # answers | # check-btns |\n|---|---|---|---|---|\n`;
for (const r of rows) {
  md += `| \`${r.file.replace("/index.html","")}\` | ${r.hasShow ? "✓" : "🔴"} | ${r.hasReset ? "✓" : "🔴"} | ${r.dataAnswer + r.dataCorrect} | ${r.checkBtns} |\n`;
}
md += `\n**Итого:** ${rows.length} уроков с автопроверкой\n`;
md += `**Без Show answers:** ${rows.filter(r => !r.hasShow).length}\n`;
md += `**Без Reset:** ${rows.filter(r => !r.hasReset).length}\n`;

const outPath = path.join(labRoot, "..", "..", `lab-answers-reset-audit-${now.replace(/[: ]/g,'-')}.md`);
fs.writeFileSync(outPath, md, "utf8");
console.log(`Scanned ${rows.length} lessons with auto-check`);
console.log(`Without Show answers: ${rows.filter(r => !r.hasShow).length}`);
console.log(`Without Reset:        ${rows.filter(r => !r.hasReset).length}`);
console.log(`Report → ${outPath}`);
