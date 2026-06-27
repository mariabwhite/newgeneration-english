import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const publicRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const labRoot = path.join(publicRoot, "lingua-boost-lab");
const premiumPath = path.join(labRoot, "premium.html");
const manifestPath = path.join(labRoot, "premium-lessons.json");
const pin = process.env.PREMIUM_PIN;
const checkOnly = process.argv.includes("--check");
const syncCards = !process.argv.includes("--no-sync-cards");

if (!pin) {
  console.error("Set PREMIUM_PIN before running this script.");
  console.error("PowerShell: $env:PREMIUM_PIN='...'; node scripts/build-premium-vault.mjs --check");
  process.exit(1);
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function htmlEscape(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function extract(html, name) {
  const match = html.match(new RegExp(`${name}:\\s*"([^"]+)"`));
  if (!match) throw new Error(`Cannot find VAULT.${name}`);
  return match[1];
}

function getIter(html) {
  const match = html.match(/iter:\s*(\d+)/);
  if (!match) throw new Error("Cannot find VAULT.iter");
  return Number(match[1]);
}

function decryptVault(html) {
  const salt = Buffer.from(extract(html, "salt"), "base64");
  const iv = Buffer.from(extract(html, "iv"), "base64");
  const ct = Buffer.from(extract(html, "ct"), "base64");
  const iter = getIter(html);
  const key = crypto.pbkdf2Sync(pin, salt, iter, 32, "sha256");
  const data = ct.subarray(0, ct.length - 16);
  const tag = ct.subarray(ct.length - 16);
  const decipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(tag);
  const plain = Buffer.concat([decipher.update(data), decipher.final()]);
  return JSON.parse(plain.toString("utf8"));
}

function encryptVault(lessons, iter) {
  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);
  const key = crypto.pbkdf2Sync(pin, salt, iter, 32, "sha256");
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const data = Buffer.concat([
    cipher.update(JSON.stringify(lessons), "utf8"),
    cipher.final(),
  ]);
  return {
    salt: salt.toString("base64"),
    iv: iv.toString("base64"),
    ct: Buffer.concat([data, cipher.getAuthTag()]).toString("base64"),
  };
}

function localFileForUrl(url) {
  let clean = String(url).split("#")[0].split("?")[0];
  clean = clean.replace(/^https:\/\/newgeneration-english\.ru\//, "/");
  if (clean.startsWith("/")) {
    clean = clean.slice(1);
    return path.join(publicRoot, clean.endsWith("/") ? clean + "index.html" : clean);
  }
  if (clean.startsWith("./")) {
    clean = clean.slice(2);
    return path.join(labRoot, clean.endsWith("/") ? clean + "index.html" : clean);
  }
  return null;
}

function getCardIds(html) {
  return [...html.matchAll(/<article\b[^>]*\bclass="[^"]*\bcard\b[^"]*"[^>]*\bdata-id="([^"]+)"/g)]
    .map((match) => match[1]);
}

function getCardSections(html) {
  const sections = new Map();
  const sectionMatches = [...html.matchAll(/<section\b[^>]*\bdata-series="([^"]+)"[^>]*>/g)];
  for (let index = 0; index < sectionMatches.length; index += 1) {
    const section = sectionMatches[index][1];
    const start = sectionMatches[index].index;
    const end = index + 1 < sectionMatches.length ? sectionMatches[index + 1].index : html.length;
    const sectionHtml = html.slice(start, end);
    for (const card of sectionHtml.matchAll(/<article\b[^>]*\bclass="[^"]*\bcard\b[^"]*"[^>]*\bdata-id="([^"]+)"/g)) {
      sections.set(card[1], section);
    }
  }
  return sections;
}

function renderCard(lesson) {
  const skills = (lesson.skills || []).map(htmlEscape).join(' <span class="dot">·</span> ');
  const coverStyle = lesson.cover
    ? ` style="background-image:url('${htmlEscape(lesson.cover)}');background-size:cover;background-position:center;"`
    : "";
  return `

        <article class="card" data-id="${htmlEscape(lesson.id)}">
          <div class="card-cover"${coverStyle} aria-hidden="true">
            <span class="card-num">${htmlEscape(lesson.number || "")}</span>
            <span class="card-tag">${htmlEscape(lesson.level || "")}</span>
          </div>
          <div class="card-body">
            <h3 class="card-title">${htmlEscape(lesson.title)}</h3>
            <div class="card-skills">${skills}</div>
            <a class="card-open" href="#" rel="noopener"><span>Открыть модуль</span><span class="arrow">→</span></a>
          </div>
        </article>`;
}

function insertMissingCards(html, missingLessons) {
  let next = html;
  for (const lesson of missingLessons) {
    const targetSection = lesson.section || lesson.series;
    const sectionStart = next.search(new RegExp(`<section[^>]+data-series="${targetSection}"`));
    if (sectionStart < 0) {
      throw new Error(`Cannot insert card ${lesson.id}: section ${targetSection} not found in premium.html`);
    }
    const divStart = next.indexOf('<div class="cards"', sectionStart);
    if (divStart < 0) throw new Error(`Cannot insert card ${lesson.id}: cards grid not found`);
    const close = next.indexOf("</div>", divStart);
    if (close < 0) throw new Error(`Cannot insert card ${lesson.id}: cards grid close not found`);
    next = next.slice(0, close) + renderCard(lesson) + "\n" + next.slice(close);
  }
  return next;
}

function fail(errors) {
  for (const error of errors) console.error(`ERROR: ${error}`);
  process.exit(errors.length ? 1 : 0);
}

let html = fs.readFileSync(premiumPath, "utf8");
const manifest = readJson(manifestPath);
const lessons = manifest.filter((lesson) => lesson.published !== false);
const errors = [];

const ids = new Set();
for (const lesson of lessons) {
  if (!lesson.id) errors.push("Lesson without id");
  if (ids.has(lesson.id)) errors.push(`Duplicate lesson id: ${lesson.id}`);
  ids.add(lesson.id);
  if (!lesson.url) errors.push(`Lesson ${lesson.id} has no url`);
  if (!lesson.series) errors.push(`Lesson ${lesson.id} has no series`);
  if (!lesson.section) lesson.section = lesson.series;
  const localFile = localFileForUrl(lesson.url);
  if (localFile && !fs.existsSync(localFile)) {
    errors.push(`Lesson ${lesson.id} URL target missing: ${localFile}`);
  }
}

let cardIds = getCardIds(html);
const cardSections = getCardSections(html);
const cardSet = new Set(cardIds);
const missingCards = lessons.filter((lesson) => !cardSet.has(lesson.id));
const extraCards = cardIds.filter((id) => !ids.has(id));
const wrongSections = lessons.filter((lesson) => {
  const actual = cardSections.get(lesson.id);
  return actual && actual !== lesson.section;
});

if (extraCards.length) {
  errors.push(`Cards without manifest entries: ${extraCards.join(", ")}`);
}

if (wrongSections.length) {
  errors.push(`Cards in wrong sections: ${wrongSections.map((lesson) => {
    return `${lesson.id} manifest=${lesson.section} html=${cardSections.get(lesson.id)}`;
  }).join("; ")}`);
}

if (missingCards.length && checkOnly) {
  errors.push(`Manifest lessons without cards: ${missingCards.map((lesson) => lesson.id).join(", ")}`);
}

let vaultLessons = [];
try {
  vaultLessons = decryptVault(html);
} catch (error) {
  errors.push(`Cannot decrypt current Vault: ${error.message}`);
}

if (vaultLessons.length) {
  const vaultById = new Map(vaultLessons.map((lesson) => [lesson.id, lesson]));
  const missingInVault = lessons.filter((lesson) => !vaultById.has(lesson.id));
  const extraInVault = vaultLessons.filter((lesson) => !ids.has(lesson.id));
  const urlMismatches = lessons.filter((lesson) => {
    const vaultLesson = vaultById.get(lesson.id);
    return vaultLesson && vaultLesson.url !== lesson.url;
  });
  if (checkOnly && missingInVault.length) {
    errors.push(`Manifest lessons missing in current Vault: ${missingInVault.map((lesson) => lesson.id).join(", ")}`);
  }
  if (checkOnly && urlMismatches.length) {
    errors.push(`Vault URL mismatches: ${urlMismatches.map((lesson) => {
      const vaultLesson = vaultById.get(lesson.id);
      return `${lesson.id} manifest=${lesson.url} vault=${vaultLesson.url}`;
    }).join("; ")}`);
  }
  if (extraInVault.length) {
    errors.push(`Vault entries without manifest entries: ${extraInVault.map((lesson) => lesson.id).join(", ")}`);
  }
}

if (checkOnly) {
  if (!errors.length) {
    console.log(`premium check OK: ${lessons.length} published lessons, ${cardIds.length} cards`);
  }
  fail(errors);
}

if (errors.length) fail(errors);

if (syncCards && missingCards.length) {
  html = insertMissingCards(html, missingCards);
  cardIds = getCardIds(html);
}

const iter = getIter(html);
const vaultPayload = lessons.map((lesson) => ({
  id: lesson.id,
  url: lesson.url,
  title: lesson.title,
  level: lesson.level,
  series: lesson.series,
}));
const next = encryptVault(vaultPayload, iter);
const version = `v${new Date().toISOString().slice(0, 10).replaceAll("-", "")}-${lessons.length}-premium-lessons`;

html = html
  .replace(/salt:\s*"[^"]+"/, `salt: "${next.salt}"`)
  .replace(/iv:\s*"[^"]+"/, `iv:   "${next.iv}"`)
  .replace(/ct:\s*"[^"]+"/, `ct:   "${next.ct}"`)
  .replace(/<meta name="vault-version" content="[^"]+">/, `<meta name="vault-version" content="${version}">`);

fs.writeFileSync(premiumPath, html, "utf8");
console.log(`premium vault built: ${lessons.length} lessons`);
console.log(`cards inserted: ${missingCards.length}`);
console.log(`version: ${version}`);
