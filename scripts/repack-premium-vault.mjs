import fs from "node:fs";
import crypto from "node:crypto";

const projectRoot = new URL("../", import.meta.url);
const premiumPath = new URL("site-public-clean/lingua-boost-lab/premium.html", projectRoot);
const pin = process.env.PREMIUM_PIN;
if (!pin) {
  console.error("Set PREMIUM_PIN before running this script.");
  console.error("PowerShell: $env:PREMIUM_PIN='...'; node scripts/repack-premium-vault.mjs --check");
  process.exit(1);
}

const additions = [
  {
    id: "travel-talk-2",
    url: "./b1/travel-talk-light-and-bright-2/",
  },
];

const version = "v18-2026-06-27-add-travel-talk-2";
const checkOnly = process.argv.includes("--check");
const dumpOnly = process.argv.includes("--dump");

function extract(html, name) {
  const match = html.match(new RegExp(`${name}:\\s*"([^"]+)"`));
  if (!match) throw new Error(`Cannot find VAULT.${name}`);
  return match[1];
}

function decryptVault(html) {
  const salt = Buffer.from(extract(html, "salt"), "base64");
  const iv = Buffer.from(extract(html, "iv"), "base64");
  const ct = Buffer.from(extract(html, "ct"), "base64");
  const iterMatch = html.match(/iter:\s*(\d+)/);
  if (!iterMatch) throw new Error("Cannot find VAULT.iter");
  const iter = Number(iterMatch[1]);
  const key = crypto.pbkdf2Sync(pin, salt, iter, 32, "sha256");
  const data = ct.subarray(0, ct.length - 16);
  const tag = ct.subarray(ct.length - 16);
  const decipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
  decipher.setAuthTag(tag);
  const plain = Buffer.concat([decipher.update(data), decipher.final()]);
  return { lessons: JSON.parse(plain.toString("utf8")), iter, key };
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

const html = fs.readFileSync(premiumPath, "utf8");
const { lessons, iter } = decryptVault(html);
const byId = new Map(lessons.map((lesson) => [lesson.id, lesson]));

if (dumpOnly) {
  console.log(JSON.stringify(lessons, null, 2));
  process.exit(0);
}

if (checkOnly) {
  console.log(`premium vault decrypted: ${lessons.length}`);
  for (const addition of additions) {
    const lesson = byId.get(addition.id);
    console.log(`${addition.id}: ${lesson ? lesson.url : "MISSING"}`);
  }
  process.exit(0);
}

for (const addition of additions) {
  byId.set(addition.id, addition);
}

const nextLessons = lessons.filter((lesson) => !additions.some((addition) => addition.id === lesson.id));
nextLessons.push(...additions);

const next = encryptVault(nextLessons, iter);
let updated = html
  .replace(/salt:\s*"[^"]+"/, `salt: "${next.salt}"`)
  .replace(/iv:\s*"[^"]+"/, `iv:   "${next.iv}"`)
  .replace(/ct:\s*"[^"]+"/, `ct:   "${next.ct}"`)
  .replace(/<meta name="vault-version" content="[^"]+">/, `<meta name="vault-version" content="${version}">`);

fs.writeFileSync(premiumPath, updated, "utf8");

console.log(`premium vault repacked: ${lessons.length} -> ${nextLessons.length}`);
console.log(`version: ${version}`);
console.log(`added/updated: ${additions.map((addition) => addition.id).join(", ")}`);
