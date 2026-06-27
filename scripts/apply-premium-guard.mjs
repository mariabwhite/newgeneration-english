import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const publicRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const labRoot = path.join(publicRoot, "lingua-boost-lab");
const manifestPath = path.join(labRoot, "premium-lessons.json");
const guardTag = '<script src="/lingua-boost-lab/assets/premium-lesson-guard.js"></script>';
const checkOnly = process.argv.includes("--check");

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function localFileForUrl(url) {
  let clean = String(url).split("#")[0].split("?")[0];
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

const lessons = readJson(manifestPath).filter((lesson) => lesson.published !== false);
const missing = [];
const changed = [];

for (const lesson of lessons) {
  const file = localFileForUrl(lesson.url);
  if (!file || !fs.existsSync(file)) {
    missing.push(`${lesson.id}: target missing`);
    continue;
  }

  const html = fs.readFileSync(file, "utf8");
  if (html.includes("premium-lesson-guard.js")) continue;
  if (checkOnly) {
    missing.push(`${lesson.id}: guard missing in ${file}`);
    continue;
  }
  if (!/<head\b[^>]*>/i.test(html)) {
    missing.push(`${lesson.id}: <head> not found in ${file}`);
    continue;
  }

  const updated = html.replace(/<head\b[^>]*>/i, (match) => `${match}\n${guardTag}`);
  fs.writeFileSync(file, updated, "utf8");
  changed.push(lesson.id);
}

if (missing.length) {
  for (const item of missing) console.error(`ERROR: ${item}`);
  process.exit(1);
}

if (checkOnly) {
  console.log(`premium guard check OK: ${lessons.length} lessons`);
} else {
  console.log(`premium guard applied: ${changed.length} files changed`);
}
