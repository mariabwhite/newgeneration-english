/*!
 * NGE Cookie Consent + Conditional Yandex.Metrika loader
 * 152-ФЗ compliant (active consent, re-prompt on denial, localStorage log).
 * Yandex.Metrika tag.js is loaded ONLY after the user clicks "Принять все".
 * Version 1.0 — 2026-06-27
 */
(function () {
  if (window.__ngeCookieConsentLoaded) return;
  window.__ngeCookieConsentLoaded = true;

  var STORAGE_KEY = 'nge-cookie-consent';
  var POLICY_VERSION = '1.1';
  var METRIKA_ID = 110204496;
  var PRIVACY_URL = '/assets/documents/privacy-policy.html';

  /* ───── 1. Read stored consent ───── */
  function readConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (data.version !== POLICY_VERSION) return null; // re-prompt on policy change
      return data;
    } catch (e) { return null; }
  }

  function writeConsent(granted) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        granted: !!granted,
        ts: new Date().toISOString(),
        version: POLICY_VERSION,
        url: location.href.split('?')[0].split('#')[0]
      }));
    } catch (e) {}
  }

  /* ───── 2. Load Yandex.Metrika (called only after consent) ───── */
  function loadMetrika() {
    if (window.__ngeMetrikaLoaded) return;
    window.__ngeMetrikaLoaded = true;

    (function (m, e, t, r, i, k, a) {
      m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
      m[i].l = 1 * new Date();
      for (var j = 0; j < document.scripts.length; j++) {
        if (document.scripts[j].src === r) { return; }
      }
      k = e.createElement(t); a = e.getElementsByTagName(t)[0];
      k.async = 1; k.src = r;
      a.parentNode.insertBefore(k, a);
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=' + METRIKA_ID, 'ym');

    window.ym(METRIKA_ID, 'init', {
      ssr: true,
      webvisor: true,
      clickmap: true,
      ecommerce: 'dataLayer',
      referrer: document.referrer,
      url: location.href,
      accurateTrackBounce: true,
      trackLinks: true
    });
  }

  /* ───── 3. Banner styles ───── */
  function injectStyles() {
    if (document.getElementById('nge-cookie-banner-style')) return;
    var css =
      '#nge-cookie-banner{position:fixed;left:12px;right:12px;bottom:12px;z-index:99999;' +
      'background:#1B2F4E;color:#F5EFE0;border:1px solid rgba(255,255,255,.10);border-radius:10px;' +
      'box-shadow:0 8px 24px rgba(0,0,0,.30);' +
      'padding:10px 14px;max-width:560px;margin:0 auto;font:400 12.5px/1.45 "Manrope",system-ui,sans-serif;' +
      'transform:translateY(14px);opacity:0;transition:opacity .25s ease, transform .25s ease}' +
      '#nge-cookie-banner.show{transform:translateY(0);opacity:1}' +
      '#nge-cookie-banner .nge-cb-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}' +
      '#nge-cookie-banner .nge-cb-text{flex:1;min-width:220px}' +
      '#nge-cookie-banner .nge-cb-text a{color:#D9A55E;text-decoration:underline}' +
      '#nge-cookie-banner .nge-cb-text a:hover{color:#F4C77A}' +
      '#nge-cookie-banner .nge-cb-actions{display:flex;gap:6px;align-items:center;flex-shrink:0}' +
      '#nge-cookie-banner button{font:700 11.5px/1 "Manrope",system-ui,sans-serif;border-radius:6px;cursor:pointer;padding:7px 12px;border:1px solid transparent;transition:filter .15s, transform .1s;white-space:nowrap}' +
      '#nge-cookie-banner button:active{transform:translateY(1px)}' +
      '#nge-cookie-banner .nge-cb-accept{background:#FF5A1F;color:#fff;border-color:#FF5A1F}' +
      '#nge-cookie-banner .nge-cb-accept:hover{filter:brightness(1.08)}' +
      '#nge-cookie-banner .nge-cb-deny{background:transparent;color:rgba(245,239,224,.75);border-color:rgba(245,239,224,.35)}' +
      '#nge-cookie-banner .nge-cb-deny:hover{background:rgba(245,239,224,.08);color:#F5EFE0;border-color:rgba(245,239,224,.6)}' +
      '@media(max-width:540px){#nge-cookie-banner{left:8px;right:8px;bottom:8px;padding:10px 12px;font-size:12px}#nge-cookie-banner .nge-cb-actions{width:100%}#nge-cookie-banner .nge-cb-actions button{flex:1}}';
    var s = document.createElement('style');
    s.id = 'nge-cookie-banner-style';
    s.textContent = css;
    document.head.appendChild(s);
  }

  /* ───── 4. Render banner ───── */
  function renderBanner() {
    if (document.getElementById('nge-cookie-banner')) return;
    injectStyles();

    var banner = document.createElement('div');
    banner.id = 'nge-cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-labelledby', 'nge-cb-title');
    banner.innerHTML =
      '<div class="nge-cb-row">' +
        '<div class="nge-cb-text" id="nge-cb-title">' +
          '🍪 Используем cookies и Яндекс.Метрику (статистика, серверы в РФ). ' +
          '<a href="' + PRIVACY_URL + '" target="_blank" rel="noopener">Политика</a>' +
        '</div>' +
        '<div class="nge-cb-actions">' +
          '<button type="button" class="nge-cb-deny" data-nge-cb="deny">Только нужные</button>' +
          '<button type="button" class="nge-cb-accept" data-nge-cb="accept">Принять</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(banner);
    requestAnimationFrame(function () { banner.classList.add('show'); });

    banner.addEventListener('click', function (e) {
      var t = e.target;
      if (!t || !t.dataset || !t.dataset.ngeCb) return;
      var choice = t.dataset.ngeCb;
      writeConsent(choice === 'accept');
      banner.classList.remove('show');
      setTimeout(function () { banner.remove(); }, 350);
      if (choice === 'accept') loadMetrika();
    });
  }

  /* ───── 5. Boot ───── */
  function boot() {
    var consent = readConsent();
    if (consent && consent.granted) {
      loadMetrika();
      return;
    }
    if (consent && consent.granted === false) {
      // Denied previously: re-prompt on next visit (banner re-appears)
      renderBanner();
      return;
    }
    renderBanner();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  /* ───── 6. Expose API for footer-link re-prompt ───── */
  window.ngeCookieConsent = {
    show: function () {
      try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
      window.__ngeMetrikaLoaded = false;
      renderBanner();
    },
    status: readConsent
  };
})();
