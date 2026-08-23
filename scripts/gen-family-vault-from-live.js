const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "..");
const CABINET_JS = path.join(ROOT, "cabinet", "cabinet.js");
const OUT_DIR = path.join(ROOT, "cabinet", "vault");
const SB_URL = "https://iqzlphbvmfgoygnozbya.supabase.co";
const PBKDF2_ITER = 600000;
const SALT_BYTES = 16;
const IV_BYTES = 12;
const KEY_BYTES = 32;
const LOOKUP_HEX = 16;

function getAnon() {
  const js = fs.readFileSync(CABINET_JS, "utf8");
  const m = js.match(/const _SB_ANON = "([^"]+)"/);
  if (!m) throw new Error("Cannot find _SB_ANON in cabinet.js");
  return m[1];
}
function deriveKey(pin, salt) {
  return crypto.pbkdf2Sync(String(pin), salt, PBKDF2_ITER, KEY_BYTES, "sha256");
}
function lookupHash(key) {
  return crypto.createHash("sha256").update(key).digest("hex").slice(0, LOOKUP_HEX);
}
function encryptJSON(obj, key) {
  const iv = crypto.randomBytes(IV_BYTES);
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const plaintext = Buffer.from(JSON.stringify(obj), "utf8");
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, ciphertext, tag]);
}
function blobName() { return crypto.randomBytes(16).toString("hex") + ".enc"; }

async function main() {
  const pins = (process.env.CABINET_PIN_LIST || "")
    .split(/[,;\s]+/)
    .map(s => s.trim())
    .filter(Boolean);
  if (!pins.length) throw new Error("Set CABINET_PIN_LIST=<comma-separated-active-pins>");
  if (new Set(pins).size !== pins.length) throw new Error("Duplicate PIN in CABINET_PIN_LIST");
  const anon = getAnon();
  fs.mkdirSync(OUT_DIR, { recursive: true });
  for (const f of fs.readdirSync(OUT_DIR)) fs.unlinkSync(path.join(OUT_DIR, f));
  const salt = crypto.randomBytes(SALT_BYTES);
  const users = [];
  for (const pin of pins) {
    const res = await fetch(`${SB_URL}/functions/v1/family-data`, {
      method: "POST",
      headers: { Authorization: `Bearer ${anon}`, "Content-Type": "application/json" },
      body: JSON.stringify({ pin }),
    });
    if (!res.ok) throw new Error(`family-data ${pin} HTTP ${res.status}: ${await res.text()}`);
    const data = await res.json();
    if (!data.students || !data.students.length) throw new Error(`family-data ${pin}: empty students`);
    const key = deriveKey(pin, salt);
    const hash = lookupHash(key);
    if (users.some(u => u.hash === hash)) throw new Error("lookup collision");
    const blob = blobName();
    fs.writeFileSync(path.join(OUT_DIR, blob), encryptJSON(data, key));
    users.push({ hash, blob });
    console.log(`${pin} -> ${data.students[0].id} -> ${blob}`);
  }
  for (let i = users.length - 1; i > 0; i--) {
    const j = crypto.randomInt(i + 1);
    [users[i], users[j]] = [users[j], users[i]];
  }
  fs.writeFileSync(path.join(OUT_DIR, "index.json"), JSON.stringify({
    version: 2,
    mode: "family-data-fallback",
    generated: new Date().toISOString(),
    salt: salt.toString("base64"),
    iter: PBKDF2_ITER,
    users,
  }, null, 2));
  console.log(`Wrote ${users.length} family vault entries to ${OUT_DIR}`);
}
main().catch(e => { console.error(e); process.exit(1); });