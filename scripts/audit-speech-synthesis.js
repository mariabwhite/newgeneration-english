const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const roots = ["lingua-boost-lab", "cabinet"];
const exts = new Set([".html", ".js"]);
const rows = [];
function walk(dir) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      if (ent.name === ".git" || ent.name === "node_modules" || ent.name === "_archive") continue;
      walk(full);
    } else if (exts.has(path.extname(ent.name).toLowerCase())) {
      const s = fs.readFileSync(full, "utf8");
      if (s.includes("speechSynthesis")) {
        rows.push({
          file: path.relative(ROOT, full).replace(/\\/g, "/"),
          speak: (s.match(/speechSynthesis\.speak/g) || []).length,
          cancel: (s.match(/speechSynthesis\.cancel/g) || []).length,
          onend: (s.match(/\.onend\s*=/g) || []).length,
          onerror: (s.match(/\.onerror\s*=/g) || []).length,
        });
      }
    }
  }
}
for (const r of roots) walk(path.join(ROOT, r));
rows.sort((a, b) => (b.speak - a.speak) || a.file.localeCompare(b.file));
console.log(JSON.stringify({ files: rows.length, top: rows.slice(0, 40) }, null, 2));