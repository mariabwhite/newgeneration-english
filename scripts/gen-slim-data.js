// scripts/gen-slim-data.js
// Берёт site/cabinet/data.js → выкидывает PII → пишет nge-cabinet/data.js
// Что остаётся: ученики (имя, уровень, расписание, PIN), уроки, отчёты, абонементы, реквизиты оплаты
// Что выкидывается: паспорта, телефоны, адреса, email родителей, всё что персонально

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const SRC = path.join(ROOT, "site", "cabinet", "data.js");
const DST = path.join(ROOT, "nge-cabinet", "data.js");

const code = fs.readFileSync(SRC, "utf-8");
const ctx = { window: {} };
vm.createContext(ctx);
vm.runInContext(code, ctx);
const D = ctx.window.NGE_DATA;

// Поля которые ОСТАВЛЯЕМ у студентов
const STUDENT_KEEP = [
  "id", "name", "nickname", "level", "format", "duration", "lessons_per_week",
  "schedule", "stability_note", "goal", "price_per_lesson", "monthly_package",
  "weekly_revenue", "payment_status", "payment_note", "payments", "is_adult",
  "casual_greeting", "greeting_student", "greeting_parent",
  "pin", "lessons_in_package", "subscription_month", "lessons_used_this_month",
  "summer_plan_note", "external_platforms", "materials",
  "lessons", "notion_id", "parent_name",
  // парент_name только ФИО (без паспорта/телефона/адреса) — нужно для приветствия
];

// Поля которые ВЫКИДЫВАЕМ (PII)
const STUDENT_DROP = [
  "parent_passport", "parent_email", "parent_phone", "parent_address", "parent_birthday",
  "contact_passport", "contact_phone", "contact_email", "contact_address",
  "contract_note",
];

function slim(obj, keepList, dropList) {
  const out = {};
  for (const k in obj) {
    if (dropList.indexOf(k) >= 0) continue;
    if (keepList.length && keepList.indexOf(k) < 0) continue;
    out[k] = obj[k];
  }
  return out;
}

// Превращаем относительные ссылки на уроки в абсолютные на публичный сайт
const PUBLIC_BASE = "https://newgeneration-english.ru";
function absolutizeUrl(url) {
  if (!url || typeof url !== "string") return url;
  if (url.startsWith("../lingua-boost-lab/")) return PUBLIC_BASE + "/" + url.slice(3);
  if (url.startsWith("../")) return PUBLIC_BASE + "/" + url.slice(3);
  return url;
}

function fixStudentUrls(s) {
  if (Array.isArray(s.lessons)) {
    s.lessons = s.lessons.map((l) => {
      if (l.homework && l.homework.module_url) {
        l.homework = { ...l.homework, module_url: absolutizeUrl(l.homework.module_url) };
      }
      return l;
    });
  }
  return s;
}

const slimData = {
  version: D.version,
  generated: new Date().toISOString(),
  generated_by: "gen-slim-data.js — без PII (без паспортов/телефонов/адресов)",
  teacher: D.teacher,
  payment: D.payment, // реквизиты ТБанк — публично-показываются в кабинете
  students: D.students.map((s) => fixStudentUrls(slim(s, STUDENT_KEEP, STUDENT_DROP))),
  reports: D.reports,
  labModules: D.labModules.map((m) => ({ ...m, url: absolutizeUrl(m.url) })),
  // contracts — НЕТ. Файлы только через Supabase Storage с signed URL
};

const out = "/* GENERATED — slim version without PII. Source of truth: Supabase. */\n" +
            "window.NGE_DATA = " + JSON.stringify(slimData, null, 2) + ";\n";

fs.writeFileSync(DST, out, "utf-8");
console.log(`Wrote slim data.js: ${DST}`);
console.log(`Size: ${(out.length / 1024).toFixed(1)} КБ (было ~${(code.length / 1024).toFixed(1)} КБ)`);
console.log(`Students: ${slimData.students.length}, Reports: ${slimData.reports.length}, Lab modules: ${slimData.labModules.length}`);
