// scripts/gen-migration-sql.js
// Читает site/cabinet/data.js → пишет supabase-migration.sql
//
// Запуск:  node scripts/gen-migration-sql.js

const fs = require("fs");
const vm = require("vm");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const DATA_PATH = path.join(ROOT, "site", "cabinet", "data.js");
const OUT_PATH = path.join(ROOT, "supabase-migration.sql");

// ----- load data.js into ctx.window.NGE_DATA -----
const code = fs.readFileSync(DATA_PATH, "utf-8");
const ctx = { window: {} };
vm.createContext(ctx);
vm.runInContext(code, ctx);
const D = ctx.window.NGE_DATA;

if (!D) throw new Error("NGE_DATA not loaded");

// ----- helpers -----
const q = (v) => {
  if (v === null || v === undefined || v === "") return "null";
  if (typeof v === "number") return String(v);
  if (typeof v === "boolean") return v ? "true" : "false";
  return "'" + String(v).replace(/'/g, "''").replace(/\\/g, "\\\\") + "'";
};
const arr = (a) => {
  if (!Array.isArray(a) || a.length === 0) return "null";
  return "array[" + a.map(q).join(",") + "]::text[]";
};

const lines = [];
const W = (s) => lines.push(s);

W("-- =============================================================");
W("-- NGE Cabinet — migration from data.js → Supabase");
W("-- Generated: " + new Date().toISOString());
W("-- =============================================================");
W("-- Запускается в SQL Editor. Идемпотентность через DELETE + INSERT.");
W("-- Безопасно перезапускать — все строки удаляются и вставляются заново.");
W("");

// ===== 1. CLEAN existing data (in dependency order) =====
W("-- ---------- Cleanup (для перезапуска) ----------");
W("delete from public.student_lab_assignments;");
W("delete from public.reports;");
W("delete from public.lessons;");
W("delete from public.subscriptions;");
W("delete from public.contracts;");
W("delete from public.student_parent;");
W("delete from public.parents;");
W("delete from public.students;");
W("delete from public.lab_modules;");
W("delete from public.teacher_info;");
W("");

// ===== 2. TEACHER INFO =====
W("-- ---------- 1. TEACHER INFO ----------");
const p = D.payment || {};
W(`insert into public.teacher_info (id, full_name, tinkoff_quick_pay, telegram, phone, contract_number, bank_account, bik, bank, correspondent_account, inn, kpp, payment_purpose) values (1, ${q(D.teacher.name)}, ${q(p.tinkoffQuickPay)}, ${q(p.telegram)}, ${q(p.phone)}, ${q(p.contract)}, ${q(p.account)}, ${q(p.bik)}, ${q(p.bank)}, ${q(p.correspondentAccount)}, ${q(p.inn)}, ${q(p.kpp)}, ${q(p.purpose)});`);
W("");

// ===== 3. LAB MODULES =====
W("-- ---------- 2. LAB MODULES ----------");
(D.labModules || []).forEach((m, i) => {
  const slug = (m.url.split("/").pop() || "").replace(/\.html$/, "");
  W(`insert into public.lab_modules (level, title, slug, url_path, sort_order) values (${q(m.level)}, ${q(m.title)}, ${q(slug || "lab-" + i)}, ${q(m.url)}, ${i});`);
});
W("");

// ===== 4. STUDENTS =====
W("-- ---------- 3. STUDENTS ----------");
const slugToId = {};
(D.students || []).forEach((s) => {
  const sub = `(select id from public.students where slug = ${q(s.id)})`;
  slugToId[s.id] = sub;
  W(`insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values (${q(s.id)}, ${q(s.notion_id)}, ${q(s.name)}, ${q(s.nickname)}, ${q(s.greeting_student)}, ${q(s.greeting_parent)}, ${q(!!s.casual_greeting)}, ${q(s.level)}, ${q(s.format || "индивидуально")}, ${q(s.duration || "90 мин")}, ${q(s.lessons_per_week || 1)}, ${q(s.schedule)}, ${q(s.stability_note)}, ${q(s.goal)}, ${q(s.price_per_lesson)}, ${q(s.monthly_package)}, ${q(!!s.is_adult)});`);
});
W("");

// pair_partner_id update (after all students inserted)
W("-- pair: Катя Медведева ↔ Маша Кузнецова");
W("-- (если в data.js появится отдельная запись пары — раскомментировать)");
W("-- update public.students set pair_partner_id = (select id from public.students where slug='maria-kuznetsova') where slug='ekaterina-medvedeva';");
W("-- update public.students set pair_partner_id = (select id from public.students where slug='ekaterina-medvedeva') where slug='maria-kuznetsova';");
W("");

// ===== 5. PARENTS =====
W("-- ---------- 4. PARENTS + student_parent links ----------");
const parentSeen = {};
(D.students || []).forEach((s) => {
  const pname = s.parent_name && s.parent_name.trim();
  if (!pname) return;
  // dedupe parent by full name
  if (!parentSeen[pname]) {
    parentSeen[pname] = true;
    W(`insert into public.parents (full_name, passport, email, phone, address) values (${q(pname)}, ${q(s.parent_passport || null)}, ${q(s.parent_email || null)}, ${q(s.parent_phone || null)}, ${q(s.parent_address || null)});`);
  }
  // link
  W(`insert into public.student_parent (student_id, parent_id) values (${slugToId[s.id]}, (select id from public.parents where full_name = ${q(pname)} limit 1));`);
});
W("");

// ===== 6. SUBSCRIPTIONS + LESSONS =====
W("-- ---------- 5. SUBSCRIPTIONS ----------");
const subKey = (sid, month) => `${sid}:${month}`;
const subInserted = {};
(D.students || []).forEach((s) => {
  if (!s.subscription_month) return;
  const k = subKey(s.id, s.subscription_month);
  if (subInserted[k]) return;
  subInserted[k] = true;
  W(`insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values (${slugToId[s.id]}, ${q(s.subscription_month)}, ${q(s.lessons_in_package || 0)}, ${q(s.lessons_used_this_month || 0)}, ${q(s.monthly_package || null)}, ${q(s.payment_status === "Оплачено")});`);
});
W("");

W("-- ---------- 6. LESSONS ----------");
(D.students || []).forEach((s) => {
  (s.lessons || []).forEach((l) => {
    const hw = l.homework || {};
    W(`insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values (${slugToId[s.id]}, ${q(l.date)}, ${q(l.num || null)}, ${q(l.status || "planned")}, ${q(l.topic || null)}, ${q(hw.text || null)}, ${q(hw.module_url || null)}, ${q(hw.module_title || null)});`);
  });
});
W("");

// ===== 7. REPORTS =====
W("-- ---------- 7. REPORTS ----------");
(D.reports || []).forEach((r) => {
  const sid = slugToId[r.student_id] || "null";
  const status = (r.status === "ready to send" ? "ready" : r.status === "sent" ? "sent" : r.status === "source imported" ? "draft" : "draft");
  W(`insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values (${sid}, ${q(r.month)}, ${q(r.type === "parent report" ? "parent_report" : r.type === "TOEFL diagnostic" ? "diagnostic" : "parent_report")}, ${q(status)}, ${q(r.title)}, ${q(r.recipient)}, ${q(r.short_message)}, ${q(r.content)}, ${q(r.notion_url)});`);
});
W("");

// ===== 8. CONTRACTS — обрабатываются отдельно через scripts/upload-contracts.js =====
W("-- ---------- 8. CONTRACTS ----------");
W("-- contracts заполняются через scripts/upload-contracts.js (один файл = одна строка)");
W("-- этот скрипт загружает PDF/JPG/PNG в Storage bucket 'contracts' и создаёт записи в БД");
W("");

W("-- =============================================================");
W("-- DONE.");
W("-- =============================================================");

fs.writeFileSync(OUT_PATH, lines.join("\n") + "\n", "utf-8");
console.log(`SQL written: ${OUT_PATH}`);
console.log(`Total lines: ${lines.length}`);
