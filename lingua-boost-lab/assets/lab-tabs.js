/**
 * lab-tabs.js · v8 · 2026-07-02
 * v8: КРИТИЧНО. Раньше tabs были fixed, а topbar position:relative → при
 *     скролле topbar уезжал, tabs висели в пустоте перекрывая контент.
 *     Теперь ФОРСИМ и topbar (fixed top:0 z:100) и tabs (fixed top:topbarH z:99).
 *     body padding-top = totalPad всегда (не условно). Проверено на Tom Sawyer.
 * v7: inline .lesson-tabs (в 5 уроках) тоже получают dynamic positioning —
 *     раньше skip'ались после querySelector detection.
 * v6: динамическое positionTabs() — измеряем реальную высоту topbar через
 *     getBoundingClientRect и ставим tabs top = topbar.height. Раньше hardcode
 *     top:62px прятался под canon-l-topbar (в A1/A2 topbar ~100px + z-index 100
 *     перекрывал tabs). Также resize/font-load re-position.
 * Auto-injects «📖 Урок / 📚 Моя домашка» tabs after topbar in every Lab lesson.
 * v4: селектор topbar теперь ловит все семейства (canon-l-topbar, friendly-topbar,
 *     lab-topbar, cmdbar) — раньше пропускал A1/A2 уроки с header.canon-l-topbar.
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
    var topbar = document.querySelector('nav.topbar, header.topbar, .topbar, header.canon-l-topbar, nav.canon-l-topbar, .canon-l-topbar, .friendly-topbar, .lab-topbar, .cmdbar');
    if (!topbar) return;
    // Если HTML уже содержит .lesson-tabs (инлайн в 5 уроках) — не инжектим,
    // но ВСЁ РАВНО применяем dynamic positioning чтобы прибить их под topbar.
    var existing = document.querySelector('.lesson-tabs');
    if (existing) {
      function reposExisting(){
        try {
          // Форсируем topbar в sticky/fixed чтобы он не уезжал при скролле
          topbar.style.setProperty('position', 'fixed', 'important');
          topbar.style.setProperty('top', '0', 'important');
          topbar.style.setProperty('left', '0', 'important');
          topbar.style.setProperty('right', '0', 'important');
          topbar.style.setProperty('z-index', '100', 'important');
          var topbarH = topbar.getBoundingClientRect().height || topbar.offsetHeight || 62;
          existing.style.setProperty('position', 'fixed', 'important');
          existing.style.setProperty('top', topbarH + 'px', 'important');
          existing.style.setProperty('left', '0', 'important');
          existing.style.setProperty('right', '0', 'important');
          existing.style.setProperty('z-index', '99', 'important');
          var tabsH = existing.getBoundingClientRect().height || existing.offsetHeight || 46;
          var totalPad = topbarH + tabsH;
          document.body.style.paddingTop = totalPad + 'px';
        } catch(e){}
      }
      reposExisting();
      window.addEventListener('resize', reposExisting);
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(reposExisting).catch(function(){});
      setTimeout(reposExisting, 300);
      setTimeout(reposExisting, 1200);
      return;
    }

    // Style
    var s = document.createElement('style');
    s.id = 'lab-tabs-style';
    s.textContent =
      '.lesson-tabs{position:fixed !important;top:62px !important;left:0 !important;right:0 !important;z-index:99 !important;display:flex !important;gap:8px;justify-content:center;' +
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
    // Динамически позиционируем tabs ПОД реальный topbar (не hardcoded 62px)
    // + body padding компенсирует высоту tabs чтобы hero не нырял под них
    function positionTabs(){
      try {
        // Форсируем topbar в fixed top:0 (не sticky — не сломается overflow-x hidden)
        topbar.style.setProperty('position', 'fixed', 'important');
        topbar.style.setProperty('top', '0', 'important');
        topbar.style.setProperty('left', '0', 'important');
        topbar.style.setProperty('right', '0', 'important');
        topbar.style.setProperty('z-index', '100', 'important');
        var topbarH = topbar.getBoundingClientRect().height || topbar.offsetHeight || 62;
        var tabsH = nav.getBoundingClientRect().height || nav.offsetHeight || 46;
        nav.style.setProperty('top', topbarH + 'px', 'important');
        var totalPad = topbarH + tabsH;
        document.body.style.paddingTop = totalPad + 'px';
      } catch(e){}
    }
    positionTabs();
    // Перепозиционируем при resize + после загрузки шрифтов
    window.addEventListener('resize', positionTabs);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(positionTabs).catch(function(){});
    setTimeout(positionTabs, 300);
    setTimeout(positionTabs, 1200);

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
