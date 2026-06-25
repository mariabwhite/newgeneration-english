/* lab-coach-persist.js v1 — сохраняет recorded transcript из любого
   AI Live Coach / mic-drill в localStorage. После F5 (или новой сессии)
   transcript восстанавливается в том же блоке, чтобы ученик и учитель
   могли его перечитать.
   Селекторы: .grader-transcript, .mic-transcript, [data-transcript].
   Ключ: lab-script:<pathname>:<idx>. */
(function(){
  if (window.__labCoachPersistLoaded) return;
  window.__labCoachPersistLoaded = true;

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function k(idx){ return 'lab-script:' + location.pathname + ':' + idx; }

  function plainText(el){
    // Берём чистый текст без interim-span курсивов
    var clone = el.cloneNode(true);
    clone.querySelectorAll('.interim').forEach(function(n){ n.remove(); });
    return (clone.textContent || '').replace(/\s+/g,' ').trim();
  }

  function injectPersistedBlock(host, text){
    if (!text) return;
    var existing = host.parentNode.querySelector('.lab-script-persisted');
    if (existing) { existing.querySelector('.lsp-body').textContent = text; return; }
    var box = document.createElement('div');
    box.className = 'lab-script-persisted';
    box.innerHTML =
      '<div class="lsp-head">💾 Последний записанный ответ <span class="lsp-meta">сохранён локально</span></div>' +
      '<div class="lsp-body"></div>' +
      '<div class="lsp-actions"><button type="button" class="lsp-clear">очистить</button></div>';
    box.querySelector('.lsp-body').textContent = text;
    host.parentNode.insertBefore(box, host.nextSibling);
  }

  function injectStyle(){
    if (document.getElementById('lab-script-persist-style')) return;
    var s = document.createElement('style');
    s.id = 'lab-script-persist-style';
    s.textContent = ''+
      '.lab-script-persisted{margin:10px 0;padding:12px 14px;border-radius:10px;'+
        'background:linear-gradient(135deg,#0E1A11 0%,#162820 100%);border:1px solid #244029;'+
        'color:#E8F5E9;font:500 .9rem/1.55 "Manrope",sans-serif}'+
      '.lab-script-persisted .lsp-head{display:flex;justify-content:space-between;align-items:center;'+
        'font:800 .76rem/1 "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;'+
        'color:#7bd9a7;margin-bottom:8px;flex-wrap:wrap;gap:6px}'+
      '.lab-script-persisted .lsp-meta{font-weight:600;color:#6E8A72;text-transform:none;letter-spacing:.04em;font-size:.7rem}'+
      '.lab-script-persisted .lsp-body{white-space:pre-wrap;word-wrap:break-word}'+
      '.lab-script-persisted .lsp-actions{margin-top:10px;display:flex;justify-content:flex-end}'+
      '.lab-script-persisted .lsp-clear{background:transparent;border:1px solid #244029;color:#7bd9a7;'+
        'padding:4px 10px;border-radius:6px;cursor:pointer;'+
        'font:700 .72rem/1 "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase}'+
      '.lab-script-persisted .lsp-clear:hover{background:#244029;color:#fff}';
    document.head.appendChild(s);
  }

  function attach(el, idx){
    if (el.__lspBound) return;
    el.__lspBound = true;

    // 1. Восстанавливаем при загрузке
    try {
      var saved = localStorage.getItem(k(idx));
      if (saved) injectPersistedBlock(el, saved);
    } catch(e){}

    // 2. Слушаем mutations — текст appendится → сохраняем
    var mo = new MutationObserver(function(){
      var txt = plainText(el);
      if (txt.length < 3) return;
      try { localStorage.setItem(k(idx), txt); } catch(e){}
      injectPersistedBlock(el, txt);
    });
    mo.observe(el, { childList:true, characterData:true, subtree:true });

    // 3. Очистка
    if (el.parentNode) {
      el.parentNode.addEventListener('click', function(e){
        if (!e.target.classList.contains('lsp-clear')) return;
        try { localStorage.removeItem(k(idx)); } catch(_){}
        var box = e.target.closest('.lab-script-persisted');
        if (box) box.remove();
      });
    }
  }

  ready(function(){
    injectStyle();
    var idx = 0;
    document.querySelectorAll('.grader-transcript, .mic-transcript, [data-transcript]').forEach(function(el){
      attach(el, idx++);
    });
    // Динамически добавленные — observer на body
    var bodyObs = new MutationObserver(function(){
      document.querySelectorAll('.grader-transcript, .mic-transcript, [data-transcript]').forEach(function(el){
        if (!el.__lspBound) attach(el, idx++);
      });
    });
    bodyObs.observe(document.body, { childList:true, subtree:true });
  });
})();
