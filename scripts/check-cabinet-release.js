const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const cabinetDir = path.join(ROOT, "cabinet");
const expectedBuild = fs.readFileSync(path.join(cabinetDir, "build.txt"), "utf8").trim();
const htmlFiles = ["index.html", "login.html", "parent.html", "student.html", "teacher.html"];
const errors = [];
function read(rel) { return fs.readFileSync(path.join(ROOT, rel), "utf8"); }
for (const f of htmlFiles) {
  const rel = "cabinet/" + f;
  const s = read(rel);
  if (!s.includes('http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"')) errors.push(rel + ": missing no-cache meta");
  if (!s.includes("var B='" + expectedBuild + "'")) errors.push(rel + ": build.txt marker mismatch");
  if (!/cabinet\.js\?v=\d+/.test(s)) errors.push(rel + ": missing cabinet.js cachebuster");
  if (!/data\.js\?v=\d+/.test(s)) errors.push(rel + ": missing data.js cachebuster");
}
const index = read("cabinet/index.html");
const login = read("cabinet/login.html");
if (index !== login) errors.push("cabinet/index.html and cabinet/login.html diverged; keep them in sync or replace login.html with a deliberate alias");
const vaultIndex = path.join(cabinetDir, "vault", "index.json");
if (!fs.existsSync(vaultIndex)) {
  errors.push("cabinet/vault/index.json missing");
} else {
  const idx = JSON.parse(fs.readFileSync(vaultIndex, "utf8"));
  if (idx.version !== 2 || idx.mode !== "family-data-fallback") errors.push("cabinet/vault/index.json has unexpected contract");
  if (!Array.isArray(idx.users) || idx.users.length === 0) errors.push("cabinet/vault/index.json has no users");
  for (const u of idx.users || []) {
    if (!/^[0-9a-f]{16}$/.test(u.hash || "")) errors.push("cabinet/vault/index.json contains invalid lookup hash");
    if (!u.blob || !fs.existsSync(path.join(cabinetDir, "vault", u.blob))) errors.push("vault blob missing: " + u.blob);
  }
}
if (errors.length) {
  console.error(errors.map(e => "- " + e).join("\n"));
  process.exit(1);
}
console.log("cabinet release check ok: build=" + expectedBuild);