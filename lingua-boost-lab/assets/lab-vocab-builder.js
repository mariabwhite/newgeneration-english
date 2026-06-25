/* lab-vocab-builder.js v1 — Универсальный словарь для Lab-уроков.

   Урок объявляет:
     window.LAB_VOCAB = [
       { word: 'environment', ipa: '/ɪnˈvaɪrənmənt/', ru: 'окружающая среда',
         example: 'We must protect the environment.', audio: 'assets/audio/env.mp3' },
       { word: 'pollution', ipa: '/pəˈluːʃən/', ru: 'загрязнение' },
       ...
     ];

   Модуль:
     • Строит секцию «📖 Vocabulary» с flip-cards (если её нет в HTML).
     • На каждой карточке: front = word + IPA, back = ru + example, 🔊 кнопка
       (audio файл или TTS через speechSynthesis API), ➕ в домашку (lab-homework).
     • Подсвечивает каждое слово в тексте урока (.card, p, li) — мягкое
       подчёркивание, hover → tooltip с IPA + ru + 🔊.
     • УЧИТЕЛЬСКИЙ «+ добавить слово» — Маша выделяет слово в тексте → плавающая
       кнопка «+ в словарь» → mini-modal (word/IPA/ru/example) → добавляется
       в localStorage extras + перерисовывается vocab section.

   Observer mode (URL ?observe=...) — учитель видит структуру, но не добавляет. */
(function(){
  if (window.__labVocabLoaded) return;
  window.__labVocabLoaded = true;

  var observeMode = /[?&]observe=/.test(location.search);
  var teacherMode = !observeMode && (/[?&](teacher|t)=1/.test(location.search) || /[?&]role=teacher/.test(location.search));

  function injectStyle(){
    if (document.getElementById('lab-vb-style')) return;
    var s = document.createElement('style');
    s.id = 'lab-vb-style';
    s.textContent = ''+
      '.lab-vocab-section{margin:32px 0;padding:26px;border-radius:16px;'+
        'background:linear-gradient(135deg,#fbf8ff 0%,#f1ebff 100%);'+
        'border:1px solid #d4c0f7;font-family:"Manrope",sans-serif}'+
      '[data-lab-theme="dark"] .lab-vocab-section{background:linear-gradient(135deg,#1e1a2e 0%,#241c3e 100%);'+
        'border-color:#5b3aa8;color:#f3eee5}'+
      '.lab-vocab-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;flex-wrap:wrap;gap:12px}'+
      '.lab-vocab-h h2{margin:0;font:800 1.25rem/1.2 "Manrope",sans-serif;color:#4a2d8a;display:flex;align-items:center;gap:10px}'+
      '[data-lab-theme="dark"] .lab-vocab-h h2{color:#e9d6ff}'+
      '.lab-vocab-h .meta{font:600 .82rem/1.4 "JetBrains Mono",monospace;letter-spacing:.08em;color:#6b46c1}'+
      '[data-lab-theme="dark"] .lab-vocab-h .meta{color:#c5a3ff}'+
      '.lab-vocab-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}'+
      '.vocab-card{position:relative;background:#fff;border:1.5px solid #d4c0f7;border-radius:12px;'+
        'padding:14px 16px;cursor:pointer;transition:transform .15s,box-shadow .15s;perspective:600px;min-height:100px}'+
      '[data-lab-theme="dark"] .vocab-card{background:#15102a;border-color:#5b3aa8}'+
      '.vocab-card:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(124,58,237,.18)}'+
      '.vocab-card .face{display:block}'+
      '.vocab-card.flipped .front{display:none}'+
      '.vocab-card:not(.flipped) .back{display:none}'+
      '.vocab-card .word{font:800 1.05rem/1.2 "Manrope",sans-serif;color:#1a1f2e;margin-bottom:4px}'+
      '[data-lab-theme="dark"] .vocab-card .word{color:#f3eee5}'+
      '.vocab-card .ipa{font:500 .88rem/1.4 "JetBrains Mono",monospace;color:#7c3aed;margin-bottom:6px}'+
      '[data-lab-theme="dark"] .vocab-card .ipa{color:#c5a3ff}'+
      '.vocab-card .ru{font:700 .94rem/1.4 "Manrope",sans-serif;color:#4a2d8a;margin-bottom:4px}'+
      '[data-lab-theme="dark"] .vocab-card .ru{color:#e9d6ff}'+
      '.vocab-card .ex{font:500 .82rem/1.5 "Manrope",sans-serif;color:#64748b;font-style:italic}'+
      '[data-lab-theme="dark"] .vocab-card .ex{color:#9aa0ab}'+
      '.vocab-card .speak{position:absolute;top:8px;right:8px;width:28px;height:28px;border-radius:50%;'+
        'border:0;background:#7c3aed;color:#fff;cursor:pointer;font-size:14px;'+
        'box-shadow:0 2px 6px rgba(124,58,237,.32);display:flex;align-items:center;justify-content:center}'+
      '.vocab-card .speak:hover{background:#a855f7;transform:scale(1.08)}'+
      '.vocab-card .extra-mark{position:absolute;top:8px;right:42px;font:800 .68rem/1 "JetBrains Mono",monospace;'+
        'letter-spacing:.14em;color:#f59e0b;background:#fef3c7;padding:3px 7px;border-radius:50px}'+
      '[data-lab-theme="dark"] .vocab-card .extra-mark{background:#451a03;color:#fbbf24}'+

      '.lab-vocab-add-btn{padding:9px 16px;border-radius:10px;border:1.5px dashed #7c3aed;'+
        'background:transparent;color:#7c3aed;cursor:pointer;'+
        'font:700 .82rem/1 "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase}'+
      '.lab-vocab-add-btn:hover{background:#7c3aed;color:#fff;border-style:solid}'+
      '[data-lab-theme="dark"] .lab-vocab-add-btn{color:#c5a3ff;border-color:#7c5ad6}'+

      '.vocab-hl{cursor:help;border-bottom:1.5px dotted #7c3aed;color:inherit;text-decoration:none;'+
        'background:rgba(124,58,237,.08);padding:1px 3px;border-radius:3px;transition:background .15s}'+
      '.vocab-hl:hover{background:rgba(124,58,237,.20)}'+
      '[data-lab-theme="dark"] .vocab-hl{border-color:#c5a3ff;background:rgba(197,163,255,.12)}'+

      '.vocab-tip{position:fixed;z-index:99997;max-width:260px;background:#1a1a2e;color:#fff;'+
        'border-radius:10px;padding:10px 14px;font:600 .85rem/1.45 "Manrope",sans-serif;'+
        'box-shadow:0 10px 30px rgba(0,0,0,.35);pointer-events:auto;opacity:0;transition:opacity .15s}'+
      '.vocab-tip.show{opacity:1}'+
      '.vocab-tip .word{font:800 .98rem/1.2 "Manrope",sans-serif;color:#fbbf24;margin-bottom:3px}'+
      '.vocab-tip .ipa{font:500 .82rem/1.3 "JetBrains Mono",monospace;color:#c5a3ff;margin-bottom:6px}'+
      '.vocab-tip .ru{font:700 .9rem/1.3 "Manrope",sans-serif;color:#fff;margin-bottom:4px}'+
      '.vocab-tip .ex{font:500 .8rem/1.4 "Manrope",sans-serif;color:#9aa0ab;font-style:italic;margin-bottom:6px}'+
      '.vocab-tip .speak{background:#7c3aed;color:#fff;border:0;padding:5px 12px;border-radius:50px;cursor:pointer;'+
        'font:700 .76rem/1 "JetBrains Mono",monospace;letter-spacing:.1em}'+

      '.teacher-add-float{position:fixed;z-index:99996;padding:10px 16px;border-radius:50px;'+
        'background:linear-gradient(135deg,#f59e0b 0%,#fbbf24 100%);color:#1a1a2e;'+
        'border:0;cursor:pointer;font:800 .82rem/1 "Manrope",sans-serif;'+
        'box-shadow:0 8px 22px rgba(245,158,11,.42);transform:scale(.85);opacity:0;'+
        'transition:transform .15s,opacity .15s}'+
      '.teacher-add-float.show{transform:scale(1);opacity:1}'+

      '.vocab-add-overlay{position:fixed;inset:0;background:rgba(20,15,40,.55);'+
        'backdrop-filter:blur(8px);z-index:99998;display:none;align-items:center;justify-content:center;padding:20px}'+
      '.vocab-add-overlay.show{display:flex;animation:vbFade .25s ease-out}'+
      '@keyframes vbFade{from{opacity:0}to{opacity:1}}'+
      '.vocab-add-modal{background:#fff;border-radius:16px;padding:24px 28px;max-width:440px;width:100%;'+
        'box-shadow:0 24px 60px rgba(0,0,0,.32);font-family:"Manrope",sans-serif;color:#1a1f2e}'+
      '[data-lab-theme="dark"] .vocab-add-modal{background:#1b1626;color:#f3eee5}'+
      '.vocab-add-modal h3{margin:0 0 6px;font:800 1.2rem/1.2 "Manrope",sans-serif;color:#7c3aed}'+
      '.vocab-add-modal p{margin:0 0 14px;font:500 .85rem/1.5 "Manrope",sans-serif;color:#64748b}'+
      '.vocab-add-modal label{display:block;font:800 .72rem/1 "JetBrains Mono",monospace;letter-spacing:.16em;text-transform:uppercase;color:#7c3aed;margin:10px 0 6px}'+
      '.vocab-add-modal input,.vocab-add-modal textarea{width:100%;box-sizing:border-box;padding:10px 12px;border-radius:8px;'+
        'border:1.5px solid #d4c0f7;background:#fff;font:600 .92rem/1.4 "Manrope",sans-serif;color:#1a1f2e;outline:none}'+
      '[data-lab-theme="dark"] .vocab-add-modal input,[data-lab-theme="dark"] .vocab-add-modal textarea{background:#15102a;border-color:#5b3aa8;color:#f3eee5}'+
      '.vocab-add-modal input:focus,.vocab-add-modal textarea:focus{border-color:#7c3aed;box-shadow:0 0 0 4px rgba(124,58,237,.12)}'+
      '.vocab-add-modal textarea{resize:vertical;min-height:60px;font-family:"Manrope",sans-serif}'+
      '.vocab-add-actions{display:flex;gap:10px;margin-top:18px;justify-content:flex-end}'+
      '.vocab-add-actions button{padding:10px 16px;border-radius:9px;border:0;cursor:pointer;'+
        'font:700 .82rem/1 "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase}'+
      '.vocab-add-actions .cancel{background:transparent;color:#7c3aed;border:1.5px solid #d4c0f7}'+
      '.vocab-add-actions .ok{background:linear-gradient(135deg,#7c3aed 0%,#a855f7 100%);color:#fff}';
    document.head.appendChild(s);
  }

  function ttsSay(text){
    try {
      if (!('speechSynthesis' in window)) return;
      var u = new SpeechSynthesisUtterance(text);
      u.lang = 'en-GB';
      u.rate = 0.9;
      speechSynthesis.cancel();
      speechSynthesis.speak(u);
    } catch(e){}
  }

  function esc(s){
    return String(s||'').replace(/[&<>"']/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c];
    });
  }

  function extraKey(){ return 'lab-vocab-extra:' + location.pathname; }
  function loadExtras(){
    try { return JSON.parse(localStorage.getItem(extraKey()) || '[]'); }
    catch(e){ return []; }
  }
  function saveExtras(arr){
    try { localStorage.setItem(extraKey(), JSON.stringify(arr)); } catch(e){}
  }

  function getVocab(){
    var fromPage = Array.isArray(window.LAB_VOCAB) ? window.LAB_VOCAB.slice() : [];
    var extras = loadExtras();
    extras.forEach(function(e){ e.__extra = true; });
    return fromPage.concat(extras);
  }

  function buildCard(item){
    var card = document.createElement('div');
    card.className = 'vocab-card';
    card.dataset.word = item.word || '';
    card.innerHTML =
      (item.__extra ? '<div class="extra-mark">⭐ teacher</div>' : '') +
      '<button class="speak" type="button" title="Прослушать">🔊</button>' +
      '<div class="face front">'+
        '<div class="word">'+esc(item.word)+'</div>'+
        (item.ipa ? '<div class="ipa">'+esc(item.ipa)+'</div>' : '') +
      '</div>' +
      '<div class="face back">'+
        '<div class="ru">'+esc(item.ru || '')+'</div>' +
        (item.example ? '<div class="ex">'+esc(item.example)+'</div>' : '') +
      '</div>';
    card.addEventListener('click', function(e){
      if (e.target.closest('.speak')) return;
      card.classList.toggle('flipped');
    });
    card.querySelector('.speak').addEventListener('click', function(e){
      e.stopPropagation();
      if (item.audio) {
        try { new Audio(item.audio).play(); return; } catch(_){}
      }
      ttsSay(item.word);
    });
    return card;
  }

  function findOrBuildSection(){
    // Если в уроке уже есть статичный vocab section — используем его
    var existing = document.querySelector('section.vocabulary, .vocab-section, section[id*="vocab"]');
    if (existing) return null; // не дублируем — статичная секция важнее
    var sec = document.createElement('section');
    sec.className = 'section lab-vocab-section';
    sec.id = 'auto-vocab';
    sec.innerHTML =
      '<div class="lab-vocab-h">'+
        '<h2>📖 Vocabulary</h2>'+
        '<div class="meta"><span id="vocabCount">0</span> слов · кликни карточку, чтобы перевернуть</div>'+
      '</div>'+
      '<div class="lab-vocab-grid" id="vocabGrid"></div>'+
      (teacherMode ? '<div style="margin-top:18px"><button class="lab-vocab-add-btn" id="vocabAddBtn">+ добавить своё слово</button></div>' : '');
    // Вставка: после hero, до первой содержательной секции
    var hero = document.querySelector('.lab-hero, .hero, section.section');
    if (hero) {
      hero.parentNode.insertBefore(sec, hero.nextSibling);
    } else {
      document.body.insertBefore(sec, document.body.firstChild);
    }
    return sec;
  }

  function renderVocab(){
    var vocab = getVocab();
    if (!vocab.length) return;
    var section = findOrBuildSection();
    if (!section) return; // статичная — модуль её не трогает
    var grid = section.querySelector('#vocabGrid');
    var counter = section.querySelector('#vocabCount');
    grid.innerHTML = '';
    vocab.forEach(function(it){ grid.appendChild(buildCard(it)); });
    if (counter) counter.textContent = vocab.length;
    if (teacherMode) {
      var addBtn = section.querySelector('#vocabAddBtn');
      if (addBtn) addBtn.addEventListener('click', function(){ openAddModal(); });
    }
  }

  function highlightInText(){
    var vocab = getVocab();
    if (!vocab.length) return;
    var hosts = document.querySelectorAll('.card p, .card li, .reading p, .story p, .passage p, .lp-bridge p, p.lead');
    var map = {};
    vocab.forEach(function(v){ if (v.word) map[v.word.toLowerCase()] = v; });
    var words = Object.keys(map).sort(function(a,b){ return b.length - a.length; });
    if (!words.length) return;
    var re = new RegExp('\\b(' + words.map(function(w){ return w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }).join('|') + ')\\b', 'gi');
    hosts.forEach(function(host){
      if (host.__vbHighlighted) return;
      host.__vbHighlighted = true;
      walkAndReplace(host, re, map);
    });
  }
  function walkAndReplace(node, re, map){
    if (node.nodeType === 3) {
      var txt = node.nodeValue;
      if (!re.test(txt)) return;
      re.lastIndex = 0;
      var frag = document.createDocumentFragment();
      var last = 0, m;
      while ((m = re.exec(txt)) !== null) {
        if (m.index > last) frag.appendChild(document.createTextNode(txt.slice(last, m.index)));
        var item = map[m[0].toLowerCase()];
        var span = document.createElement('span');
        span.className = 'vocab-hl';
        span.dataset.word = item.word;
        span.textContent = m[0];
        attachTooltip(span, item);
        frag.appendChild(span);
        last = m.index + m[0].length;
      }
      if (last < txt.length) frag.appendChild(document.createTextNode(txt.slice(last)));
      node.parentNode.replaceChild(frag, node);
      return;
    }
    if (node.nodeType !== 1) return;
    if (/^(SCRIPT|STYLE|SPAN)$/.test(node.tagName)) return;
    if (node.classList && node.classList.contains('vocab-hl')) return;
    Array.from(node.childNodes).forEach(function(c){ walkAndReplace(c, re, map); });
  }

  var tipEl = null;
  function tip(){
    if (tipEl) return tipEl;
    tipEl = document.createElement('div');
    tipEl.className = 'vocab-tip';
    document.body.appendChild(tipEl);
    return tipEl;
  }
  function showTip(span, item){
    var t = tip();
    t.innerHTML =
      '<div class="word">'+esc(item.word)+'</div>'+
      (item.ipa ? '<div class="ipa">'+esc(item.ipa)+'</div>' : '') +
      '<div class="ru">'+esc(item.ru||'')+'</div>'+
      (item.example ? '<div class="ex">'+esc(item.example)+'</div>' : '') +
      '<button class="speak" type="button">🔊 listen</button>';
    var r = span.getBoundingClientRect();
    t.style.left = Math.min(window.innerWidth - 280, r.left) + 'px';
    t.style.top  = (r.bottom + 6) + 'px';
    t.classList.add('show');
    t.querySelector('.speak').onclick = function(){
      if (item.audio) { try { new Audio(item.audio).play(); return; } catch(_){} }
      ttsSay(item.word);
    };
  }
  function hideTip(){
    if (tipEl) tipEl.classList.remove('show');
  }
  function attachTooltip(span, item){
    span.addEventListener('mouseenter', function(){ showTip(span, item); });
    span.addEventListener('mouseleave', function(){ setTimeout(function(){
      if (tipEl && !tipEl.matches(':hover')) hideTip();
    }, 200); });
  }

  // ==== TEACHER MODE — добавление слов через selection ====
  var floatBtn = null;
  function ensureFloat(){
    if (floatBtn) return floatBtn;
    floatBtn = document.createElement('button');
    floatBtn.className = 'teacher-add-float';
    floatBtn.textContent = '+ в словарь';
    document.body.appendChild(floatBtn);
    return floatBtn;
  }
  function hookSelection(){
    if (!teacherMode) return;
    ensureFloat();
    document.addEventListener('mouseup', function(){
      setTimeout(function(){
        var sel = window.getSelection();
        var text = (sel ? sel.toString() : '').trim();
        if (!text || text.length < 2 || text.length > 40 || /\s{2,}/.test(text)) {
          floatBtn.classList.remove('show');
          return;
        }
        var range = sel.getRangeAt(0);
        var r = range.getBoundingClientRect();
        floatBtn.style.left = Math.min(window.innerWidth - 160, r.right + 8) + 'px';
        floatBtn.style.top  = (r.top + window.scrollY - 8) + 'px';
        floatBtn.style.position = 'absolute';
        floatBtn.classList.add('show');
        floatBtn.onclick = function(){
          openAddModal({ word: text });
          floatBtn.classList.remove('show');
        };
      }, 80);
    });
  }

  function openAddModal(prefill){
    var overlay = document.querySelector('.vocab-add-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'vocab-add-overlay';
      overlay.innerHTML =
        '<div class="vocab-add-modal">'+
          '<h3>Новое слово в словарь</h3>'+
          '<p>Это слово сохранится для этого устройства и появится в Vocabulary секции этого урока (помечено ⭐ teacher).</p>'+
          '<label>Слово (EN)</label><input type="text" id="vbWord" maxlength="40">'+
          '<label>Транскрипция (IPA)</label><input type="text" id="vbIpa" placeholder="/ˈmɔːr.fiːm/">'+
          '<label>Перевод (RU)</label><input type="text" id="vbRu">'+
          '<label>Пример (необязательно)</label><textarea id="vbEx"></textarea>'+
          '<div class="vocab-add-actions">'+
            '<button class="cancel" type="button">Отмена</button>'+
            '<button class="ok" type="button">Добавить</button>'+
          '</div>'+
        '</div>';
      document.body.appendChild(overlay);
      overlay.addEventListener('click', function(e){ if (e.target === overlay) overlay.classList.remove('show'); });
      overlay.querySelector('.cancel').addEventListener('click', function(){ overlay.classList.remove('show'); });
      overlay.querySelector('.ok').addEventListener('click', function(){
        var word = (overlay.querySelector('#vbWord').value || '').trim();
        if (word.length < 2) { alert('Введи слово'); return; }
        var item = {
          word: word,
          ipa: (overlay.querySelector('#vbIpa').value || '').trim(),
          ru:  (overlay.querySelector('#vbRu').value  || '').trim(),
          example: (overlay.querySelector('#vbEx').value || '').trim()
        };
        var extras = loadExtras();
        extras.push(item);
        saveExtras(extras);
        overlay.classList.remove('show');
        // Re-render
        var existing = document.getElementById('auto-vocab');
        if (existing) existing.remove();
        renderVocab();
        document.querySelectorAll('p, li').forEach(function(el){ el.__vbHighlighted = false; });
        highlightInText();
      });
    }
    overlay.querySelector('#vbWord').value = (prefill && prefill.word) || '';
    overlay.querySelector('#vbIpa').value = '';
    overlay.querySelector('#vbRu').value = '';
    overlay.querySelector('#vbEx').value = '';
    overlay.classList.add('show');
    setTimeout(function(){
      var f = overlay.querySelector(prefill && prefill.word ? '#vbIpa' : '#vbWord');
      if (f) f.focus();
    }, 50);
  }

  function init(){
    if (observeMode) return; // observer не трогаем
    injectStyle();
    renderVocab();
    highlightInText();
    if (teacherMode) hookSelection();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
