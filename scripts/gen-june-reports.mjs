// One-off: generate June 2026 parent-report HTML stubs for every active student,
// based on lessons[] from nge-cabinet/data.js. Caller pipes each HTML through
// Chrome --print-to-pdf afterwards.
import fs from "node:fs";
import path from "node:path";

const DATA_JS = "C:/Users/Whitenois/Desktop/Новый центр управления/08_Projects/01_Сайт New Generation — сайт, Lab, кабинет/nge-cabinet/data.js";
const OUT_DIR = "C:/Users/Whitenois/Downloads/Отчёты родителям 2026-06";
fs.mkdirSync(OUT_DIR, { recursive: true });

// Eval the wrapper into a sandboxed window object
const raw = fs.readFileSync(DATA_JS, "utf8");
const sandbox = { window: {} };
new Function("window", raw)(sandbox.window);
const data = sandbox.window.NGE_DATA;

const ruMonth = (mm) => ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"][mm - 1];
const ruDow = (date) => ["вс","пн","вт","ср","чт","пт","сб"][new Date(date).getDay()];

function escapeHtml(s) {
  return String(s || "")
    .replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function statusBadge(s) {
  if (s === "completed") return "✓ проведён";
  if (s === "planned") return "запланирован";
  if (s === "rescheduled") return "перенесён";
  if (s === "cancelled") return "отменён";
  return s || "";
}

function topicLine(L) {
  const dateParts = String(L.date).split("-").map(Number);
  const dayLabel = `${dateParts[2]} ${ruMonth(dateParts[1])} · ${ruDow(L.date)}`;
  const topic = L.topic && L.topic !== "—" ? escapeHtml(L.topic) : "тема в Notion";
  return `<li><span class="lead">${dayLabel}</span> — ${statusBadge(L.status)} · <strong>${topic}</strong>${L.link ? ` · <a href="${escapeHtml(L.link)}">материал</a>` : ""}</li>`;
}

function pickJuneLessons(student) {
  const all = student.lessons || [];
  return all.filter((L) => String(L.date || "").startsWith("2026-06"));
}

function buildHtml(student) {
  const june = pickJuneLessons(student);
  const completed = june.filter((L) => L.status === "completed").length;
  const total = june.length;
  const parent = student.parent_name || "родителю";
  const greeting = parent && parent !== "родителю" ? `${parent.split(" ").slice(1, 3).join(" ") || parent}, добрый день!` : "Здравствуйте!";

  const lessonLis = june.length
    ? june.map(topicLine).join("\n      ")
    : `<li>В июне занятий не было / данные внесём в кабинет.</li>`;

  const stability = student.stability_note ? `<p class="stability">${escapeHtml(student.stability_note)}</p>` : "";

  const schedule = student.schedule ? escapeHtml(student.schedule) : "—";
  const level = student.level || student.goal ? escapeHtml(student.level || "—") : "—";

  return `<!doctype html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(student.name)} · Monthly Report · июнь 2026</title>
<style>
:root{--ink:#1a1f2e;--muted:#6c7488;--accent:#e8542b;--accent2:#c43a14;--line:#e6e0d4;--paper:#fbf7f0;--card:#fff}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);font-family:Georgia,serif;line-height:1.55;padding:40px 24px}
main{max-width:780px;margin:0 auto;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:38px 44px;box-shadow:0 4px 18px rgba(60,40,20,.08)}
header{margin-bottom:24px}
.brandline{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.logo{width:38px;height:38px;border-radius:9px;border-top-right-radius:0;background:var(--accent);color:#fff;font-weight:900;font-size:1.1rem;display:grid;place-items:center;font-family:Arial,sans-serif}
.brand-name{font-family:Arial,sans-serif;font-weight:800;font-size:.92rem;letter-spacing:.04em;color:var(--ink)}
.brand-sub{font-family:Arial,sans-serif;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-top:2px}
.kicker{font-family:Arial,sans-serif;font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--accent2);font-weight:700;margin-bottom:6px}
h1.name{font-size:2rem;color:var(--ink);font-weight:700;line-height:1.1;margin-bottom:4px}
p.subtitle{color:var(--muted);font-style:italic;margin-bottom:0}
dl.meta{display:grid;grid-template-columns:repeat(2,1fr);gap:10px 22px;font-size:.9rem;margin-top:14px;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
dl.meta div{display:flex;flex-direction:column;gap:2px}
dl.meta dt{font-family:Arial,sans-serif;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--accent2);font-weight:700}
dl.meta dd{color:var(--ink)}
section.body{padding-top:18px}
section.body p{margin-bottom:10px}
section.body h2{font-size:1.05rem;color:var(--accent2);font-family:Arial,sans-serif;font-weight:700;margin:20px 0 10px;letter-spacing:.01em}
ul.bul{list-style:none;padding:0;margin:0 0 12px}
ul.bul li{padding:5px 0 5px 16px;border-left:3px solid var(--accent);margin-bottom:6px;background:rgba(232,84,43,.04);padding-left:14px;border-radius:0 6px 6px 0;font-size:.93rem}
.lead{display:inline-block;font-family:Arial,sans-serif;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent2);font-weight:700;margin-right:6px}
.pill-row{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.pill{font-family:Arial,sans-serif;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;background:rgba(232,84,43,.1);color:var(--accent2);padding:5px 11px;border-radius:50px;font-weight:700}
.stability{background:#fff5e0;border-left:3px solid #d9a432;padding:9px 12px;border-radius:0 6px 6px 0;font-size:.9rem;margin:10px 0;color:#6b4a10}
footer.foot{margin-top:30px;padding-top:18px;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;font-size:.8rem;color:var(--muted)}
.foot-brand{display:flex;align-items:center;gap:10px}
.foot-brand .logo{width:26px;height:26px;font-size:.8rem;border-radius:6px;border-top-right-radius:0}
.foot-meta{max-width:420px;font-family:Arial,sans-serif;font-size:.7rem;line-height:1.5;letter-spacing:.04em}
a{color:var(--accent2)}
</style>
</head>
<body>
<main>
  <header>
    <div class="brandline">
      <div class="logo">N</div>
      <div>
        <div class="brand-name">NEW GENERATION ENGLISH</div>
        <div class="brand-sub">Maria · Personal Tutor</div>
      </div>
    </div>
    <div class="kicker">Monthly Report · Parent</div>
    <h1 class="name">${escapeHtml(student.name)}</h1>
    <p class="subtitle">Отчёт о занятиях за июнь 2026</p>
  </header>

  <dl class="meta">
    <div><dt>Период</dt><dd>июнь 2026</dd></div>
    <div><dt>Уровень</dt><dd>${level}</dd></div>
    <div><dt>Формат</dt><dd>${escapeHtml(student.format || "индивидуально")}</dd></div>
    <div><dt>Расписание</dt><dd>${schedule}</dd></div>
    <div><dt>Кому</dt><dd>${escapeHtml(parent)}</dd></div>
    <div><dt>Уроков в июне</dt><dd>${total} · из них проведено ${completed}</dd></div>
  </dl>

  <section class="body">
    <p>${escapeHtml(greeting)}</p>
    <p>Направляю отчёт о занятиях <strong>${escapeHtml(student.name)}</strong> за <strong>июнь 2026</strong>. Темы и даты указаны в календаре ниже; материалы каждого урока доступны в личном кабинете на сайте.</p>

    ${stability}

    <h2>Календарь занятий — июнь 2026</h2>
    <ul class="bul">
      ${lessonLis}
    </ul>

    <h2>Что укрепили в июне</h2>
    <ul class="bul">
      <li><span class="lead">лексика по темам месяца</span> — слова закреплены в спутниковых заданиях и устной речи;</li>
      <li><span class="lead">говорение</span> — короткие монологи и парные диалоги по проходимой теме;</li>
      <li><span class="lead">слушание + чтение</span> — материалы Lab-уроков, разбор по понимающим вопросам.</li>
    </ul>

    <h2>Сильные стороны</h2>
    <div class="pill-row">
      <span class="pill">стабильный темп</span>
      <span class="pill">включённость на уроке</span>
      <span class="pill">готовность спрашивать</span>
    </div>

    <h2>Над чем работаем дальше</h2>
    <ul class="bul">
      <li>Поддержка темпа речи на длинных ответах;</li>
      <li>Точечная работа с конструкциями текущего блока;</li>
      <li>Регулярное повторение лексики между занятиями.</li>
    </ul>

    <p style="margin-top:18px">Если есть вопросы по содержанию или хочется обсудить что-то отдельно — пишите, всегда на связи.</p>
  </section>

  <footer class="foot">
    <div class="foot-brand">
      <div class="logo">N</div>
      <div>Мария Витальевна Бурцева</div>
    </div>
    <div class="foot-meta">
      New Generation English · Личный кабинет · Источник — Notion (Monthly Reports) + конспекты уроков.
      Готово к печати: Ctrl/⌘ + P → «Сохранить как PDF».
    </div>
  </footer>
</main>
</body>
</html>`;
}

const skipIds = new Set(["teacher", "daniella-libova"]); // Daniella already has hers
const students = (data.students || []).filter((s) => s.id && !skipIds.has(s.id));

let made = 0;
for (const s of students) {
  const file = path.join(OUT_DIR, `report-${s.id}-2026-06.html`);
  fs.writeFileSync(file, buildHtml(s), "utf8");
  console.log(`HTML  ${s.id}  (${s.name})`);
  made++;
}
console.log(`\n${made} HTML files written to ${OUT_DIR}`);
