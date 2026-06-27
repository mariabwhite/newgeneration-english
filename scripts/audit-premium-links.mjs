import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const publicRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const labRoot = path.join(publicRoot, "lingua-boost-lab");
const manifestPath = path.join(labRoot, "premium-lessons.json");
const live = process.argv.includes("--live");
const siteOrigin = "https://newgeneration-english.ru";

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function cleanUrl(url) {
  return String(url || "").split("#")[0].split("?")[0];
}

function localFileForUrl(url) {
  let clean = cleanUrl(url);
  clean = clean.replace(/^https:\/\/newgeneration-english\.ru\//, "/");
  if (clean.startsWith("/")) {
    clean = clean.slice(1);
    return path.join(publicRoot, clean.endsWith("/") ? `${clean}index.html` : clean);
  }
  if (clean.startsWith("./")) {
    clean = clean.slice(2);
    return path.join(labRoot, clean.endsWith("/") ? `${clean}index.html` : clean);
  }
  return null;
}

function publicUrlForLesson(url) {
  const value = String(url || "");
  if (value.startsWith("https://newgeneration-english.ru/")) return value;
  if (value.startsWith("/")) return `${siteOrigin}${value}`;
  if (value.startsWith("./")) return `${siteOrigin}/lingua-boost-lab/${value.slice(2)}`;
  return null;
}

function lessonLabel(lesson) {
  return `${lesson.id} (${lesson.title || "untitled"})`;
}

async function checkLive(url) {
  const response = await fetch(url, { method: "GET", redirect: "follow" });
  return {
    status: response.status,
    ok: response.status >= 200 && response.status < 400,
    finalUrl: response.url,
  };
}

const lessons = readJson(manifestPath).filter((lesson) => lesson.published !== false);
const errors = [];
const warnings = [];
const rows = [];

for (const lesson of lessons) {
  const localFile = localFileForUrl(lesson.url);
  const publicUrl = publicUrlForLesson(lesson.url);

  if (!publicUrl) {
    errors.push(`${lessonLabel(lesson)} has unsupported URL: ${lesson.url}`);
  }

  if (!localFile) {
    warnings.push(`${lessonLabel(lesson)} has no local file mapping: ${lesson.url}`);
  } else if (!fs.existsSync(localFile)) {
    errors.push(`${lessonLabel(lesson)} local target missing: ${localFile}`);
  }

  rows.push({ lesson, localFile, publicUrl });
}

if (live) {
  for (const row of rows) {
    if (!row.publicUrl) continue;
    try {
      const result = await checkLive(row.publicUrl);
      if (!result.ok) {
        errors.push(`${lessonLabel(row.lesson)} live URL returned ${result.status}: ${row.publicUrl}`);
      }
    } catch (error) {
      errors.push(`${lessonLabel(row.lesson)} live URL failed: ${row.publicUrl} (${error.message})`);
    }
  }
}

for (const warning of warnings) console.warn(`WARN: ${warning}`);
for (const error of errors) console.error(`ERROR: ${error}`);

if (errors.length) {
  console.error(`premium link audit failed: ${errors.length} errors, ${warnings.length} warnings`);
  process.exit(1);
}

console.log(`premium link audit OK: ${lessons.length} lessons, ${warnings.length} warnings${live ? ", live checked" : ""}`);
