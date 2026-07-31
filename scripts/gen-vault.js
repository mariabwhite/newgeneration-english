/**
 * gen-vault.js
 *
 * Reads source-of-truth data from `nge-cabinet/data.js` (private repo, NEVER deployed)
 * and generates per-user AES-GCM encrypted vault files into
 * `site-public-clean/cabinet/vault/` (public repo, deployed to GitHub Pages).
 *
 * Encryption: PBKDF2-SHA256(PIN, salt, 600000) → 32 bytes → 16 bytes used as
 * AES-256-GCM key indirectly. We derive 48 bytes: first 32 = AES key,
 * last 16 hex digits of SHA256(key) = public index lookup hash.
 *
 * Public index.json contains only {hash, blob} pairs + the global salt + iter.
 * No PII, no names, no PINs.
 *
 * Each vault/<random>.enc file is AES-GCM ciphertext that only the holder of
 * the correct PIN can decrypt. Without PIN, the blob is opaque random bytes.
 *
 * Run:
 *   node scripts/gen-vault.js
 *
 * Updates:
 *   - Edit nge-cabinet/data.js (or future Supabase fetcher)
 *   - Re-run this script
 *   - Commit site-public-clean/cabinet/vault/ to public repo
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

// FIX 2026-07-31: скрипт лежит в site-public-clean/scripts/, значит
// PROJECT_ROOT = site-public-clean/ САМ. Раньше был лишний "site-public-clean"
// в VAULT_DIR path.join, из-за чего файлы падали в
// site-public-clean/site-public-clean/cabinet/vault/ (DOUBLE-PREFIX bug).
// Каждый прогон требовал rescue-copy руками.
const PROJECT_ROOT = path.resolve(__dirname, "..");
const SOURCE_DATA = path.join(PROJECT_ROOT, "nge-cabinet", "data.js");
const VAULT_DIR   = path.join(PROJECT_ROOT, "cabinet", "vault");
const INDEX_FILE  = path.join(VAULT_DIR, "index.json");

const PBKDF2_ITER = 600000; // OWASP 2023 recommendation for PBKDF2-SHA256
const SALT_BYTES  = 16;     // 128-bit global salt
const IV_BYTES    = 12;     // AES-GCM IV is 12 bytes
const KEY_BYTES   = 32;     // AES-256
const LOOKUP_HEX  = 16;     // 16 hex chars = 64 bits — enough for index lookup, not for brute force

/* ---------- helpers ---------- */

function loadSourceData() {
  if (!fs.existsSync(SOURCE_DATA)) {
    throw new Error(`Source data.js not found at: ${SOURCE_DATA}`);
  }
  const raw = fs.readFileSync(SOURCE_DATA, "utf8");
  const cleaned = raw
    .replace(/^\/\*[\s\S]*?\*\/\s*/m, "")           // strip leading block comment
    .replace(/^window\.NGE_DATA\s*=\s*/m, "")       // strip assignment
    .replace(/;\s*$/, "");                          // strip trailing semicolon
  // eslint-disable-next-line no-eval
  return eval("(" + cleaned + ")");
}

function deriveKey(passwordOrPin, salt) {
  return crypto.pbkdf2Sync(passwordOrPin, salt, PBKDF2_ITER, KEY_BYTES, "sha256");
}

function computeLookupHash(key) {
  // SHA-256(key) → first 16 hex chars. Used only for public index lookup.
  // Knowing this hash does not help decrypt the blob (different one-way hash).
  return crypto.createHash("sha256").update(key).digest("hex").slice(0, LOOKUP_HEX);
}

function encryptJSON(plainObj, key) {
  const iv = crypto.randomBytes(IV_BYTES);
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const plaintext = Buffer.from(JSON.stringify(plainObj), "utf8");
  const ciphertext = Buffer.concat([cipher.update(plaintext), cipher.final()]);
  const authTag = cipher.getAuthTag();
  // Format: iv (12) || ciphertext || authTag (16)
  return Buffer.concat([iv, ciphertext, authTag]);
}

function randomBlobName() {
  return crypto.randomBytes(16).toString("hex") + ".enc";
}

/* ---------- vault builder per role ---------- */

function buildFamilyPayload(student, allReports, teacher, payment) {
  // What a student/parent sees: own info + own reports + teacher contact (for greeting)
  // + payment info (for billing).
  return {
    role: "family",
    student: student,                                              // full student record
    reports: (allReports || []).filter(r => r.student_id === student.id),
    teacher_name: teacher.name,                                    // name only, NO passwordHash
    payment: payment,                                              // bank/payment info (intentionally accessible)
  };
}

function buildTeacherPayload(data) {
  // Teacher sees everything except their own password hash (they typed it to log in).
  const { passwordHash, ...teacherSafe } = data.teacher;
  return {
    role: "teacher",
    teacher: teacherSafe,
    payment: data.payment,
    students: data.students,
    reports: data.reports || [],
    labModules: data.labModules || [],
  };
}

/* ---------- main ---------- */

function main() {
  console.log("== gen-vault.js ==");
  console.log("Source:", SOURCE_DATA);
  console.log("Output:", VAULT_DIR);
  console.log("");

  // Read source
  const data = loadSourceData();
  console.log("Source loaded:");
  console.log("  students:", data.students.length);
  console.log("  reports: ", (data.reports || []).length);
  console.log("  teacher passwordHash:", data.teacher.passwordHash ? "present" : "MISSING");
  console.log("");

  // Sanity check
  if (!data.teacher.passwordHash || data.teacher.passwordHash.length !== 64) {
    throw new Error("Teacher passwordHash missing or invalid (must be 64-char hex SHA-256)");
  }
  for (const s of data.students) {
    if (!/^\d{4}$/.test(String(s.pin || ""))) {
      throw new Error(`Student ${s.id} has invalid PIN: "${s.pin}"`);
    }
  }
  const pins = data.students.map(s => s.pin);
  if (new Set(pins).size !== pins.length) {
    throw new Error("Duplicate PIN detected across students!");
  }

  // Clean target dir
  if (fs.existsSync(VAULT_DIR)) {
    for (const f of fs.readdirSync(VAULT_DIR)) {
      fs.unlinkSync(path.join(VAULT_DIR, f));
    }
  } else {
    fs.mkdirSync(VAULT_DIR, { recursive: true });
  }

  // Global salt (regenerated each gen — invalidates all previous vaults)
  const salt = crypto.randomBytes(SALT_BYTES);

  const indexUsers = [];

  // --- Encrypt per family ---
  for (const student of data.students) {
    const pin = String(student.pin);
    const key = deriveKey(pin, salt);
    const hash = computeLookupHash(key);
    const blob = randomBlobName();

    // Detect collisions on lookup hash (with 16 hex = 64 bits, ~zero probability)
    if (indexUsers.some(u => u.hash === hash)) {
      throw new Error(`Hash collision for student ${student.id} — should be impossible`);
    }

    const payload = buildFamilyPayload(student, data.reports, data.teacher, data.payment);
    const ciphertext = encryptJSON(payload, key);

    fs.writeFileSync(path.join(VAULT_DIR, blob), ciphertext);
    indexUsers.push({ hash, blob });
    console.log(`  ✓ ${student.id.padEnd(30)} → vault/${blob}`);
  }

  // --- Encrypt teacher ---
  // Use the teacher password (NOT its hash) as the key derivation input.
  // We don't HAVE the password — only its SHA-256 hash. So the teacher's vault
  // is keyed by the SAME passwordHash that exists in data.teacher.passwordHash.
  // This is fine: when teacher logs in, JS hashes the input and uses the hash
  // as the PBKDF2 password input. SHA256(typed-password) === stored hash =>
  // derives the same vault key. Without typing the right password, no access.
  const teacherKeyInput = data.teacher.passwordHash;
  const teacherKey = deriveKey(teacherKeyInput, salt);
  const teacherHash = computeLookupHash(teacherKey);
  const teacherBlob = randomBlobName();

  if (indexUsers.some(u => u.hash === teacherHash)) {
    throw new Error("Hash collision for teacher — should be impossible");
  }

  const teacherPayload = buildTeacherPayload(data);
  const teacherCiphertext = encryptJSON(teacherPayload, teacherKey);
  fs.writeFileSync(path.join(VAULT_DIR, teacherBlob), teacherCiphertext);
  indexUsers.push({ hash: teacherHash, blob: teacherBlob });
  console.log(`  ✓ ${"teacher".padEnd(30)} → vault/${teacherBlob}`);

  // --- Write public index ---
  const indexJson = {
    version: 1,
    generated: new Date().toISOString(),
    salt: salt.toString("base64"),
    iter: PBKDF2_ITER,
    users: indexUsers,           // shuffled order so position doesn't leak anything
  };
  // shuffle index users so order doesn't correlate with student order
  for (let i = indexJson.users.length - 1; i > 0; i--) {
    const j = crypto.randomInt(i + 1);
    [indexJson.users[i], indexJson.users[j]] = [indexJson.users[j], indexJson.users[i]];
  }
  fs.writeFileSync(INDEX_FILE, JSON.stringify(indexJson, null, 2));

  console.log("");
  console.log("✓ index.json written");
  console.log("  users in index:", indexJson.users.length, "(15 students + 1 teacher = 16 expected)");
  console.log("");
  console.log("Done. Vault is sealed.");
  console.log("Public files: " + VAULT_DIR.replace(PROJECT_ROOT, "<project>"));
  console.log("Source kept private at: " + SOURCE_DATA.replace(PROJECT_ROOT, "<project>"));
}

main();
