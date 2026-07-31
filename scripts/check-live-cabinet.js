// Скачивает live vault с newgeneration-english.ru, расшифровывает по PIN,
// печатает lessons[] так, как видит cabinet.js.
const https = require("https");
const crypto = require("crypto");

const BASE = "https://newgeneration-english.ru/cabinet/vault";
const PINS = [
  { name: "Маракина",  pin: "1265" },
  { name: "Протасов",  pin: "7186" },
  { name: "Медведева", pin: "3714" },
  { name: "Кузнецова", pin: "3715" },
];

function get(url){
  return new Promise((res, rej) => {
    https.get(url, r => {
      const chunks = [];
      r.on("data", c => chunks.push(c));
      r.on("end", () => res({ status: r.statusCode, body: Buffer.concat(chunks) }));
    }).on("error", rej);
  });
}

function deriveKey(input, saltB64, iter){
  return crypto.pbkdf2Sync(input, Buffer.from(saltB64, "base64"), iter, 32, "sha256");
}
function lookupHash(key){
  return crypto.createHash("sha256").update(key).digest("hex").slice(0, 16);
}
function aesGcmDecrypt(combined, key){
  const iv = combined.slice(0, 12);
  const tag = combined.slice(combined.length - 16);
  const ct = combined.slice(12, combined.length - 16);
  const d = crypto.createDecipheriv("aes-256-gcm", key, iv);
  d.setAuthTag(tag);
  return Buffer.concat([d.update(ct), d.final()]).toString("utf8");
}

(async () => {
  const nc = Date.now();
  const idx = JSON.parse((await get(`${BASE}/index.json?nc=${nc}`)).body.toString());
  console.log("vault generated:", idx.generated);
  for (const { name, pin } of PINS) {
    const key = deriveKey(pin, idx.salt, idx.iter);
    const hash = lookupHash(key);
    const u = idx.users.find(u => u.hash === hash);
    if (!u) { console.log(`\n— ${name} (PIN ${pin}): НЕ НАЙДЕН в live vault`); continue; }
    const blob = (await get(`${BASE}/${u.blob}?nc=${nc}`)).body;
    const plain = aesGcmDecrypt(blob, key);
    const payload = JSON.parse(plain);
    const s = payload.student || payload;
    const lessons = s.lessons || [];
    console.log(`\n=== ${name} (PIN ${pin}) ===`);
    console.log(`name=${s.name}  subscription_month=${s.subscription_month}  in_package=${s.lessons_in_package}  used=${s.lessons_used_this_month}`);
    lessons.forEach((l, i) => {
      const t = (l.topic || "").replace(/\s+/g, " ").slice(0, 80);
      console.log(`  ${(i+1).toString().padStart(2)}. ${l.date}  ${l.status.padEnd(11)}  ${t}`);
    });
  }
})().catch(e => { console.error(e); process.exit(1); });
