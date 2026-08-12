/* NG English · Premium Lab · vault-flag guard  (v2 · 2026-08-12)
 *
 * Model:
 *   1. Fast path — if `nge-lab-unlocked === "yes"` in localStorage → no-op.
 *   2. Otherwise, fetch premium-lessons.json and check whether the CURRENT
 *      pathname belongs to the premium catalogue. If yes → redirect to
 *      /lingua-boost-lab/login.html?next=<current>. If no → let the page
 *      render (it is a personal / student lesson, not premium content).
 *   3. Fail-open on any error (network, JSON parse, timeout) — we would
 *      rather show a premium page unlocked than trap a legitimate student
 *      in a PIN loop on a page they own.
 *
 * Why v2 exists (incident 2026-08-12):
 *   Katya Zhizhina's parent reported that clicking through from the cabinet
 *   to her lesson (katya-02-azkaban-library) opened the login screen and
 *   never let her in. Root cause: v1 gated EVERY page that included
 *   this script, but the script had been mass-attached to 79 lesson files
 *   including personal / persona-lock lessons that were never meant to be
 *   behind the premium password. Parents of ordinary students do not know
 *   the premium password (watchmaker2026q3) — they only know their child's
 *   cabinet PIN — so the login screen was an inescapable dead end.
 *
 *   Also: /lingua-boost-lab/.homework/ was gated by the same script, which
 *   caused a cross-origin loop between cabinet.newgeneration-english.ru
 *   (Cloudflare Pages) and newgeneration-english.ru (GH Pages) because the
 *   unlock flag lives in localStorage per-origin and doesn't cross domains.
 *
 * Fix philosophy:
 *   Keep the whitelist in one place — premium-lessons.json — so adding a
 *   new premium lesson stays a one-file edit (Codex bumps the catalogue,
 *   guard.js auto-picks it up on next load). No more mass-touching lesson
 *   files. Persona-lock lessons carry the <script> tag but the guard
 *   simply ignores them.
 */
(function () {
  "use strict";

  var UNLOCK_KEY = "nge-lab-unlocked";
  var LOGIN_URL  = "/lingua-boost-lab/login.html";
  var CATALOG    = "/lingua-boost-lab/premium-lessons.json";
  var FETCH_TIMEOUT_MS = 3000;

  // Fast path: already unlocked. Do nothing.
  try {
    if (localStorage.getItem(UNLOCK_KEY) === "yes") return;
  } catch (_) { /* localStorage blocked (private mode) — fall through */ }

  function normalizePath(u) {
    try {
      var url = new URL(u, location.origin);
      var p = url.pathname;
      // Trailing slash normalisation: "/foo" and "/foo/" collapse to "/foo/"
      // ONLY if the URL clearly points at a directory index. Keep .html paths
      // as-is (some premium lessons are flat .html files, not folders).
      if (!/\.[a-z0-9]+$/i.test(p) && !p.endsWith("/")) p = p + "/";
      return p;
    } catch (_) { return u; }
  }

  var currentPath = normalizePath(location.pathname);
  // Never gate the login page itself — that IS the loop we are killing.
  if (currentPath === normalizePath(LOGIN_URL)) return;
  // Never gate the shared .homework surface — it is a per-student clone
  // page and its own contract is that any student can open it.
  if (currentPath.indexOf("/lingua-boost-lab/.homework/") === 0) return;

  // Hide the page visually until we know whether it is premium — otherwise
  // a legitimate premium lesson would flash its content before redirecting.
  // If the fetch takes too long or fails, we un-hide (fail-open).
  var html = document.documentElement;
  var prevVisibility = html.style.visibility;
  html.style.visibility = "hidden";

  function showPage() { html.style.visibility = prevVisibility || ""; }
  function redirectToLogin() {
    var next = location.pathname + location.search + location.hash;
    location.replace(LOGIN_URL + "?next=" + encodeURIComponent(next));
  }

  var settled = false;
  var timer = setTimeout(function () {
    if (settled) return;
    settled = true;
    // Catalogue took too long — do not trap the student. Show the page.
    showPage();
  }, FETCH_TIMEOUT_MS);

  fetch(CATALOG, { credentials: "same-origin", cache: "no-cache" })
    .then(function (r) {
      if (!r.ok) throw new Error("catalog " + r.status);
      return r.json();
    })
    .then(function (list) {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      var isPremium = false;
      if (Array.isArray(list)) {
        for (var i = 0; i < list.length; i++) {
          var entry = list[i];
          if (!entry || !entry.url) continue;
          if (normalizePath(entry.url) === currentPath) { isPremium = true; break; }
        }
      }
      if (isPremium) redirectToLogin();
      else showPage();
    })
    .catch(function () {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      // Network/parse failure — fail open. A rare premium page will briefly
      // be reachable without the password, but this is better than trapping
      // a real student on a broken lookup.
      showPage();
    });
})();
