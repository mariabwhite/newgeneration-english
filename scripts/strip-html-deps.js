/**
 * Strip data.js and supabase-client.js script tags from cabinet HTML files,
 * bump cabinet.js version to invalidate browser cache.
 *
 * Run from project root:  node scripts/strip-html-deps.js
 */
const fs = require("fs");
const path = require("path");

const CABINET_DIR = path.resolve(__dirname, "..", "site-public-clean", "cabinet");
const HTMLS = ["index.html", "login.html", "parent.html", "student.html", "teacher.html", "me.html", "auth-callback.html"];

const PATTERNS = [
  /\s*<script\s+src="\.\/data\.js[^"]*"><\/script>\s*\n?/g,
  /\s*<script\s+src="\.\/supabase-client\.js[^"]*"><\/script>\s*\n?/g,
];
const CABINET_JS_VERSION_BUMP = /cabinet\.js\?v=\d+/g;

let changedCount = 0;
for (const f of HTMLS) {
  const p = path.join(CABINET_DIR, f);
  if (!fs.existsSync(p)) { console.log("  -- skip (missing):", f); continue; }
  let s = fs.readFileSync(p, "utf8");
  const before = s;
  for (const re of PATTERNS) s = s.replace(re, "\n");
  s = s.replace(CABINET_JS_VERSION_BUMP, "cabinet.js?v=28");
  // Collapse multiple blank lines that may have appeared
  s = s.replace(/\n\n\n+/g, "\n\n");
  if (s !== before) {
    fs.writeFileSync(p, s);
    changedCount++;
    console.log("  ✓", f);
  } else {
    console.log("  -- no changes:", f);
  }
}
console.log("\nChanged", changedCount, "files.");
