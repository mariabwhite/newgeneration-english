/* NG English · Premium Lab · vault-flag guard
 * Simple model: one password for the whole premium group.
 * localStorage.getItem('nge-lab-unlocked') === 'yes' → all premium lessons open.
 * No per-lesson PIN, no per-lesson URL list, no /api probe → no redirect loops.
 *
 * If the flag is missing, redirect to /lingua-boost-lab/login.html?next=<current>.
 * If the flag is present, do nothing (page renders as usual).
 */
(function () {
  "use strict";
  var UNLOCK_KEY = "nge-lab-unlocked";
  var LOGIN_URL = "/lingua-boost-lab/login.html";

  function isUnlocked() {
    try { return localStorage.getItem(UNLOCK_KEY) === "yes"; }
    catch (_) { return false; }
  }

  if (isUnlocked()) return;

  var next = window.location.pathname + window.location.search + window.location.hash;
  window.location.replace(LOGIN_URL + "?next=" + encodeURIComponent(next));
})();
