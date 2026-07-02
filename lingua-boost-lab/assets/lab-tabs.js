/**
 * lab-tabs.js · v3 · 2026-07-02
 * Auto-injects «📖 Урок / 📚 Моя домашка» tabs after .topbar in every Lab lesson.
 * v3: position:sticky → position:fixed (body{overflow-x:hidden} ломает sticky
 *     во всех Lab-уроках, tabs «ездили» посреди страницы). getHwKey теперь
 *     'lab-hw:' (унифицировано с lab-homework.js v=29+).
 * Canon: reference_lab_lesson_tabs_canon.md
 * — Палитра берётся через CSS vars из урока (--accent / --line / --card / --bg).
 * — Click on «Моя домашка» → opens the dedicated homework page.
 * — Esc / backdrop / .lab-hw-close → возврат на Lesson.
 */
(function(){
  if (window.__labTabsLoaded) return;
  window.__labTabsLoaded = true;

  function inject(){
    // Если HTML уже содержит .lesson-tabs (инлайн в файле) — не дублируем
    if (document.querySelector('.lesson-tabs')) return;
    var topbar = document.querySelector('nav.topbar, header.topbar, .topbar');
    if (!topbar) return;

    // Style
    var s = document.createElement('style');
    s.id = 'lab-tabs-style';
    s.textContent =
      '.lesson-tabs{position:fixed;top:62px;left:0;right:0;z-index:99;display:flex;gap:8px;justify-content:center;' +
        'background:color-mix(in srgb,var(--bg,#fff) 94%,transparent);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);' +
        'border-bottom:1px solid var(--line,rgba(0,0,0,.08));padding:10px 12px;' +
        'transition:top .26s cubic-bezier(.4,0,.2,1)}' +
      '.topbar.tb-hidden + .lesson-tabs,.topbar.is-hidden + .lesson-tabs{top:0}' +
      '.ltab{padding:9px 18px;border-radius:50px;border:1.5px solid var(--line-2,rgba(0,0,0,.14));background:var(--card,#fff);' +
        'color:var(--muted,#64748b);font:800 11px/1 "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;' +
        'cursor:pointer;transition:.18s;display:inline-flex;align-items:center;gap:8px}' +
      '.ltab:hover{border-color:var(--accent,#7c3aed);color:var(--accent,#7c3aed)}' +
      '.ltab.is-active{background:var(--accent,#7c3aed);color:var(--accent-on,#fff);border-color:var(--accent,#7c3aed);' +
        'box-shadow:0 4px 12px color-mix(in srgb,var(--accent,#7c3aed) 40%,transparent)}' +
      '.ltab .ltab-count{background:rgba(255,255,255,.18);padding:2px 8px;border-radius:50px;font-size:10px;min-width:20px;text-align:center}' +
      '.ltab.is-active .ltab-count{background:rgba(0,0,0,.18);color:inherit}' +
      '@media(max-width:680px){.lesson-tabs{padding:6px 6px;gap:6px;top:54px}' +
        '.ltab{padding:7px 12px;font-size:9.5px;letter-spacing:.08em}}';
    document.head.appendChild(s);

    // HTML
    var nav = document.createElement('nav');
    nav.className = 'lesson-tabs';
    nav.setAttribute('role','tablist');
    nav.setAttribute('aria-label','Lesson / Homework');
    nav.innerHTML =
      '<button class="ltab is-active" data-tab="lesson" type="button">📖 Урок</button>' +
      '<button class="ltab" data-tab="homework" type="button">📚 Моя домашка <span class="ltab-count" id="ltab-hw-count">0</span></button>';
    // Вставить сразу после topbar
    if (topbar.nextSibling) topbar.parentNode.insertBefore(nav, topbar.nextSibling);
    else topbar.parentNode.appendChild(nav);
    // Компенсируем высоту fixed-табов чтобы hero не нырял под них
    try {
      var isMobile = window.matchMedia && window.matchMedia('(max-width:680px)').matches;
      var pad = isMobile ? 46 : 52;
      var cur = parseFloat(getComputedStyle(document.body).paddingTop) || 0;
      if (cur < pad) document.body.style.paddingTop = pad + 'px';
    } catch(e){}

    // JS логика — переключение / привязка к FAB домашке
    var tabs = nav.querySelectorAll('.ltab');
    var hwCount = nav.querySelector('#ltab-hw-count');
    function setActive(name){ tabs.forEach(function(t){ t.classList.toggle('is-active', t.dataset.tab === name); }); }
    function getHwKey(){ return 'lab-hw:' + location.pathname; }
    function refreshCount(){
      try { var arr = JSON.parse(localStorage.getItem(getHwKey()) || '[]'); if (hwCount) hwCount.textContent = arr.length; }
      catch(e){}
    }
    tabs.forEach(function(t){
      t.addEventListener('click', function(){
        var name = t.dataset.tab;
        setActive(name);
        if (name === 'homework') {
          window.location.href = '/lingua-boost-lab/.homework/?lesson=' + encodeURIComponent(location.pathname);
        } else {
          document.querySelectorAll('.lab-hw-overlay.show').forEach(function(o){ o.classList.remove('show'); });
        }
      });
    });
    refreshCount();
    setInterval(refreshCount, 1500);
    document.addEventListener('click', function(e){
      if (e.target.classList && e.target.classList.contains('lab-hw-overlay')) setActive('lesson');
      if (e.target.closest && e.target.closest('.lab-hw-close, .lab-hw-modal-close, [data-lab-hw-close]')) setActive('lesson');
    });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') setActive('lesson'); });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject);
  else inject();
})();
