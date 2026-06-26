/* lab-homework.js v2 — «Положить в домашку».
   У каждого упражнения появляется маленькая кнопка ➕ — клик добавляет
   задание в личную домашку ученика. FAB «📚 Моя домашка · N» снизу справа
   открывает overlay со списком. Кнопка «📤 Отправить учителю» шлёт batch:
     1. INSERT в Supabase lab_submissions (section_id='homework-batch') ← ОСНОВНОЕ
     2. Broadcast в lab-firehose-v1 (teacher-live.html сразу видит)
     3. Опциональный POST в локальный AI Hub (127.0.0.1:8765) для TG-уведомления
        — silent fail если Hub лежит. Hub НЕ основной канал. */
(function(){
  if (window.__labHwLoaded) return;
  window.__labHwLoaded = true;
  // Observer mode (учитель в iframe) — UI домашки виден, но клики silent
  // (не пишут в БД от имени ученика и не broadcast'ят). Учитель ВИДИТ
  // те же кнопки что и ученик, чтобы понимать что у того на экране.
  var observerView = /[?&]observe=/.test(location.search);

  var SUPABASE_URL  = "https://iqzlphbvmfgoygnozbya.supabase.co";
  var SUPABASE_ANON = "sb_publishable_hYhBk3xS90uouUFd_DZWUw_sOv-6JGO";

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function slugify(s){
    return (s||'').toLowerCase().replace(/[^a-zа-яё0-9]+/gi,'-').replace(/^-+|-+$/g,'').slice(0,30);
  }

  function hwKey(){
    return 'lab-hw:' + location.pathname;
  }
  function loadHw(){
    try { return JSON.parse(localStorage.getItem(hwKey()) || '[]'); }
    catch(e){ return []; }
  }
  function saveHw(arr){
    try { localStorage.setItem(hwKey(), JSON.stringify(arr)); } catch(e){}
  }
  function getName(){
    try { return localStorage.getItem('lab-student-name') || ''; } catch(e){ return ''; }
  }
  function roomFor(name){
    return name ? 'student-' + slugify(name) : (function(){
      try {
        var stored = localStorage.getItem('lab-solo-id');
        if (!stored) { stored = 'solo-' + Math.random().toString(36).slice(2,10); localStorage.setItem('lab-solo-id', stored); }
        return stored;
      } catch(e){ return 'solo-anon'; }
    })();
  }

  function injectStyle(){
    if (document.getElementById('lab-hw-style')) return;
    var s = document.createElement('style');
    s.id = 'lab-hw-style';
    s.textContent = ''+
      '.lab-hw-add{position:absolute;top:4px;right:4px;left:auto;width:26px;height:26px;border-radius:50%;'+
        'background:linear-gradient(135deg,#fff 0%,#fef3c7 100%);'+
        'border:1.5px solid #f59e0b;color:#92400e;cursor:pointer;'+
        'display:inline-flex;align-items:center;justify-content:center;'+
        'font:800 16px/1 system-ui;box-shadow:0 2px 6px rgba(245,158,11,.18);'+
        'opacity:0;transform:scale(.85);transition:all .18s ease-out;z-index:5}'+
      '.lab-hw-host{position:relative}'+
      '.lab-hw-host:hover .lab-hw-add,.lab-hw-add.added{opacity:1;transform:scale(1)}'+
      /* На touch-устройствах нет hover — плюсики всегда видны (mobile/tablet) */
      '@media (hover:none){.lab-hw-add{opacity:1;transform:scale(1)}}'+
      /* В учительском режиме — все плюсики ВСЕГДА видны */
      'body.lab-teacher-on .lab-hw-add{opacity:1;transform:scale(1)}'+
      'body.lab-teacher-on .lab-hw-add:hover{transform:scale(1.12);background:#f59e0b;color:#fff}'+
      '.lab-hw-section-btn{padding:8px 14px;border-radius:50px;border:1.5px solid #f59e0b;'+
        'background:#fff;color:#92400e;cursor:pointer;'+
        'font:800 11px/1 "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;'+
        'display:inline-flex;align-items:center;justify-content:center;gap:6px;transition:all .15s;'+
        'box-sizing:border-box;max-width:100%;white-space:normal;text-align:center;line-height:1.2;margin:14px auto 0}'+
      '.lab-hw-section-btn:hover{background:#f59e0b;color:#fff;transform:translateY(-1px)}'+
      '.lab-hw-add:hover{background:#f59e0b;color:#fff;box-shadow:0 4px 14px rgba(245,158,11,.42);transform:scale(1.08)}'+
      '.lab-hw-add.added{background:linear-gradient(135deg,#fde68a 0%,#fbbf24 100%);color:#78350f}'+
      '.lab-hw-add.added::after{content:""}'+
      '[data-lab-theme="dark"] .lab-hw-add{background:linear-gradient(135deg,#3a2f1a 0%,#4d3d1f 100%);color:#fde68a;border-color:#92400e}'+
      '[data-lab-theme="dark"] .lab-hw-add.added{background:#92400e;color:#fef3c7}'+

      '.lab-hw-fab{position:fixed;right:18px;bottom:150px;z-index:998}'+
      '.lab-hw-fab-btn{padding:11px 18px;border-radius:50px;border:0;cursor:pointer;'+
        'background:linear-gradient(135deg,#f59e0b 0%,#fbbf24 100%);color:#fff;'+
        'font:800 11px/1 "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;'+
        'box-shadow:0 8px 24px rgba(245,158,11,.45);display:flex;align-items:center;gap:8px;'+
        'transition:transform .15s,box-shadow .15s;min-height:42px;box-sizing:border-box}'+
      '.lab-hw-fab-btn:hover{transform:translateY(-2px);box-shadow:0 12px 30px rgba(245,158,11,.55)}'+
      '.lab-hw-fab-btn .n{background:#fff;color:#92400e;padding:2px 10px;border-radius:50px;'+
        'font:900 13px/1 "JetBrains Mono",monospace}'+
      '.lab-hw-fab.empty .lab-hw-fab-btn{background:#475569;opacity:.65;'+
        'box-shadow:0 4px 12px rgba(0,0,0,.18)}'+
      '.lab-hw-fab.empty .n{color:#475569}'+
      '@media (max-width:680px){.lab-hw-fab{right:max(10px,env(safe-area-inset-right));bottom:96px;max-width:calc(100vw - 20px)}'+
        '.lab-hw-fab-btn{max-width:calc(100vw - 20px);min-height:38px;padding:9px 12px;font-size:10px;letter-spacing:.08em;white-space:normal;text-align:center;line-height:1.15;justify-content:center}'+
        '.lab-hw-section-btn{padding:7px 10px;font-size:9.5px;letter-spacing:.06em;max-width:100%}}'+

      '.lab-hw-overlay{position:fixed;inset:0;background:rgba(20,15,40,.62);'+
        'backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);'+
        'z-index:99996;display:none;align-items:center;justify-content:center;padding:20px}'+
      '.lab-hw-overlay.show{display:flex;animation:labHwFade .25s ease-out}'+
      '@keyframes labHwFade{from{opacity:0}to{opacity:1}}'+
      '.lab-hw-modal{background:#fff;border-radius:20px;max-width:640px;width:100%;max-height:86vh;'+
        'display:flex;flex-direction:column;box-shadow:0 24px 60px rgba(0,0,0,.32);'+
        'font-family:"Manrope",sans-serif;color:#1a1f2e}'+
      '[data-lab-theme="dark"] .lab-hw-modal{background:#1b1626;color:#f3eee5}'+
      '.lab-hw-modal-h{padding:22px 26px 12px;border-bottom:1px solid rgba(0,0,0,.08);'+
        'display:flex;justify-content:space-between;align-items:flex-start;gap:12px}'+
      '[data-lab-theme="dark"] .lab-hw-modal-h{border-color:rgba(255,255,255,.08)}'+
      '.lab-hw-modal-h h3{margin:0;font:800 1.4rem/1.2 "Manrope",sans-serif;color:#92400e}'+
      '[data-lab-theme="dark"] .lab-hw-modal-h h3{color:#fbbf24}'+
      '.lab-hw-modal-h .sub{font:500 .85rem/1.4 "Manrope",sans-serif;color:#64748b;margin-top:4px}'+
      '.lab-hw-close{background:transparent;border:0;font-size:28px;cursor:pointer;color:#64748b;'+
        'line-height:1;padding:0;width:34px;height:34px;border-radius:50%}'+
      '.lab-hw-close:hover{background:rgba(0,0,0,.06)}'+
      '[data-lab-theme="dark"] .lab-hw-close{color:#94a3b8}'+
      '.lab-hw-list{flex:1;overflow-y:auto;padding:14px 26px}'+
      '.lab-hw-item{background:linear-gradient(135deg,#fffbeb 0%,#fef3c7 100%);'+
        'border:1px solid #fde68a;border-left:4px solid #f59e0b;border-radius:10px;'+
        'padding:14px 16px;margin-bottom:10px;position:relative}'+
      '[data-lab-theme="dark"] .lab-hw-item{background:linear-gradient(135deg,#2e2419 0%,#3d2f1c 100%);'+
        'border-color:#78350f}'+
      '.lab-hw-item .lab-hw-kind{display:inline-block;font:800 .68rem/1 "JetBrains Mono",monospace;'+
        'letter-spacing:.16em;text-transform:uppercase;color:#92400e;background:#fde68a;'+
        'padding:3px 8px;border-radius:50px;margin-bottom:6px}'+
      '[data-lab-theme="dark"] .lab-hw-item .lab-hw-kind{color:#fbbf24;background:#451a03}'+
      '.lab-hw-item .lab-hw-q{font:700 .96rem/1.45 "Manrope",sans-serif;margin-bottom:4px}'+
      '.lab-hw-item .lab-hw-meta{font:500 .82rem/1.5 "Manrope",sans-serif;color:#78350f}'+
      '[data-lab-theme="dark"] .lab-hw-item .lab-hw-meta{color:#d4a373}'+
      '.lab-hw-item .lab-hw-meta b{color:#1a1f2e}'+
      '[data-lab-theme="dark"] .lab-hw-item .lab-hw-meta b{color:#fef3c7}'+
      '.lab-hw-item .lab-hw-rm{position:absolute;top:8px;right:8px;width:24px;height:24px;'+
        'border-radius:50%;background:transparent;border:0;color:#92400e;cursor:pointer;font-size:18px;line-height:1}'+
      '.lab-hw-item .lab-hw-rm:hover{background:rgba(146,64,14,.12)}'+
      '.lab-hw-empty{text-align:center;padding:40px 20px;color:#64748b;'+
        'font:500 .95rem/1.5 "Manrope",sans-serif}'+
      '.lab-hw-empty .em{font-size:48px;display:block;margin-bottom:12px}'+
      '.lab-hw-modal-f{padding:16px 26px 22px;border-top:1px solid rgba(0,0,0,.08);'+
        'display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end}'+
      '[data-lab-theme="dark"] .lab-hw-modal-f{border-color:rgba(255,255,255,.08)}'+
      '.lab-hw-modal-f button{padding:11px 18px;border-radius:10px;border:0;cursor:pointer;'+
        'font:800 .82rem/1 "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;'+
        'transition:transform .15s,box-shadow .15s}'+
      '.lab-hw-modal-f .lab-hw-send{background:linear-gradient(135deg,#f59e0b 0%,#fbbf24 100%);color:#fff}'+
      '.lab-hw-modal-f .lab-hw-send:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(245,158,11,.42)}'+
      '.lab-hw-modal-f .lab-hw-send:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}'+
      '.lab-hw-modal-f .lab-hw-clear{background:transparent;color:#dc2626;border:1.5px solid #fecaca}'+
      '.lab-hw-modal-f .lab-hw-clear:hover{background:#fef2f2}'+
      '.lab-hw-toast{position:fixed;left:50%;bottom:32px;transform:translateX(-50%);'+
        'background:#92400e;color:#fff;padding:12px 22px;border-radius:50px;'+
        'font:700 .88rem/1.4 "Manrope",sans-serif;z-index:99999;'+
        'box-shadow:0 8px 30px rgba(0,0,0,.32);opacity:0;transition:opacity .2s;pointer-events:none}'+
      '.lab-hw-toast.show{opacity:1}';
    document.head.appendChild(s);
  }

  function toast(msg){
    var t = document.querySelector('.lab-hw-toast');
    if (!t) { t = document.createElement('div'); t.className = 'lab-hw-toast'; document.body.appendChild(t); }
    t.textContent = msg;
    requestAnimationFrame(function(){ t.classList.add('show'); });
    clearTimeout(t.__tt);
    t.__tt = setTimeout(function(){ t.classList.remove('show'); }, 2800);
  }

  function txt(el){ return el ? (el.textContent || '').replace(/\s+/g,' ').trim() : ''; }
  function short(s, n){ s = s||''; return s.length > n ? s.slice(0, n-1) + '…' : s; }

  // Описать упражнение в формате item для домашки
  function describe(host, kind){
    var sec = host.closest('section.section') || host.closest('section');
    var secTitle = (sec && (sec.querySelector('h2')?.textContent || sec.querySelector('h3')?.textContent) || '').trim();
    var item = {
      ts: Date.now(),
      kind: kind,
      section_id: sec ? (sec.id || '') : '',
      section_title: short(secTitle, 100),
      question: '',
      correct: '',
      student_answer: ''
    };
    if (kind === 'mcq') {
      var qEl = host.querySelector('.mcq-q, .mc-q, .stmt, .ctx');
      item.question = short(txt(qEl), 200);
      var right = host.querySelector('.mcq-opts button.correct, .mc-opts button.correct, button.right');
      if (right) item.correct = short(txt(right), 120);
      var clicked = host.querySelector('.mcq-opts button.wrong, .mc-opts button.wrong, button.wrong');
      if (clicked) item.student_answer = short(txt(clicked), 120);
    } else if (kind === 'tfns') {
      item.question = short(txt(host.querySelector('.stmt')), 200);
      var rT = host.querySelector('button.right');
      if (rT) item.correct = short(txt(rT), 80);
      var wT = host.querySelector('button.wrong');
      if (wT) item.student_answer = short(txt(wT), 80);
    } else if (kind === 'gap') {
      var ctx = host.closest('p, li, .gapfill, .cloze, .card');
      item.question = short(txt(ctx), 200);
      item.correct = short(host.dataset.answer || host.dataset.ans || '', 80);
      item.student_answer = short((host.textContent || '').trim(), 80);
    } else if (kind === 'wf') {
      var ctxEl = host.querySelector('.ctx');
      item.question = short(txt(ctxEl), 200);
      var inp = host.querySelector('input');
      if (inp) {
        item.correct = short(inp.dataset.answer || txt(host.querySelector('.hint')), 80);
        item.student_answer = short(inp.value || '', 80);
      }
    } else if (kind === 'match') {
      item.question = short(txt(host), 200);
      item.correct = short(host.dataset.answer || '', 80);
    } else if (kind === 'builder') {
      var prompt = host.querySelector('.target-line, .prompt');
      item.question = short(txt(prompt), 200);
      item.correct = short(host.dataset.answer || '', 200);
    } else if (kind === 'mic') {
      item.question = short(host.dataset.target || txt(host.querySelector('.mic-text')), 200);
      item.correct = short(host.dataset.target || '', 200);
      var tr = host.querySelector('.mic-transcript');
      if (tr) item.student_answer = short((tr.textContent || '').replace(/^"|"$/g,'').trim(), 200);
    } else if (kind === 'writing') {
      var label = host.previousElementSibling;
      item.question = short(txt(label) || 'Open writing', 200);
      item.student_answer = short(host.value || '', 500);
    } else if (kind === 'vocab') {
      var word = host.dataset.word || (host.querySelector('.word, .vocab-front .word')?.textContent || '').trim();
      var meaning = (host.querySelector('.meaning, .vocab-back .meaning')?.textContent || '').trim();
      var example = (host.querySelector('.ex, .vocab-back .ex')?.textContent || '').trim();
      item.question = short('📖 ' + word, 200);
      item.correct = short(meaning, 200);
      item.student_answer = short(example, 200);
    }
    return item;
  }

  function addBtn(host, kind){
    if (host.__hwHost) return;
    host.__hwHost = true;
    host.__hwKind = kind;
    host.classList.add('lab-hw-host');
    if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'lab-hw-add';
    b.textContent = '+';
    b.title = 'Положить в домашку';
    b.addEventListener('mousedown', function(e){ e.preventDefault(); e.stopPropagation(); }, true);
    b.addEventListener('click', function(e){
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
      var item = describe(host, kind);
      var arr = loadHw();
      // защита от дубля — по section_id + question
      var dupIdx = arr.findIndex(function(x){
        return x.section_id === item.section_id && x.question === item.question && x.kind === item.kind;
      });
      if (dupIdx >= 0) {
        arr.splice(dupIdx, 1);
        b.classList.remove('added');
        b.textContent = '+';
        toast('Убрала из домашки');
      } else {
        arr.push(item);
        b.classList.add('added');
        b.textContent = '✓';
        toast('Добавила в домашку · ' + arr.length);
      }
      saveHw(arr);
      refreshFabCount();
    });
    // Если уже в hw — отметить ✓
    var item = describe(host, kind);
    if (loadHw().some(function(x){
      return x.section_id === item.section_id && x.question === item.question && x.kind === item.kind;
    })) {
      b.classList.add('added');
      b.textContent = '✓';
    }
    host.appendChild(b);
  }

  function scanAndDecorate(){
    document.querySelectorAll('.mcq-row, .mc-item, .choice-row, .choice-card, .qcard, .question-card, .q-item').forEach(function(el){ addBtn(el, 'mcq'); });
    document.querySelectorAll('.tfns-row, .tf-row, .tf-item').forEach(function(el){ addBtn(el, 'tfns'); });
    document.querySelectorAll('.gap, .gram-gap, .gapfill, .cloze-gap').forEach(function(el){ addBtn(el, 'gap'); });
    document.querySelectorAll('.wf-row, .wordform-row').forEach(function(el){ addBtn(el, 'wf'); });
    document.querySelectorAll('.match-item, .match-card, .match-row, .pair-row').forEach(function(el){ addBtn(el, 'match'); });
    document.querySelectorAll('.builder, .reorder-row, .order-row').forEach(function(el){ addBtn(el, 'builder'); });
    document.querySelectorAll('.mic-row, .speech-row, .speak-row').forEach(function(el){ addBtn(el, 'mic'); });
    document.querySelectorAll('.write textarea, textarea.writing-area, textarea[data-write], .open-writing textarea, .free-write textarea').forEach(function(el){ addBtn(el, 'writing'); });
    document.querySelectorAll('.vocab-card, .word-card, .vocabulary-item').forEach(function(el){ addBtn(el, 'vocab'); });
    document.querySelectorAll('.cue-card, .post, .prompt-card, .task-card, .speaking-task, .writing-task').forEach(function(el){ addBtn(el, 'builder'); });
    // Modals и подобные — диктант / трансформация / cloze
    document.querySelectorAll('.dict-row, .dictation-row').forEach(function(el){ addBtn(el, 'gap'); });
    document.querySelectorAll('.trans-row, .transform-row, .rewrite-row').forEach(function(el){ addBtn(el, 'builder'); });
    decorateSections();
  }

  // Кнопка «📚 весь блок в домашку» на каждой секции
  function decorateSections(){
    document.querySelectorAll('section.section').forEach(function(sec){
      if (sec.__hwSecBtn) return;
      sec.__hwSecBtn = true;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'lab-hw-section-btn';
      btn.innerHTML = '📚 всю секцию в домашку';
      btn.addEventListener('click', function(e){
        e.preventDefault();
        var items = sec.querySelectorAll('.lab-hw-host');
        if (!items.length) { toast('В этой секции нечего добавить'); return; }
        var arr = loadHw();
        var added = 0;
        items.forEach(function(host){
          var kind = host.__hwKind || '';
          if (!kind) {
            if (host.matches('.mcq-row, .mc-item, .choice-row, .choice-card, .qcard, .question-card, .q-item')) kind='mcq';
            else if (host.matches('.tfns-row, .tf-row, .tf-item')) kind='tfns';
            else if (host.matches('.gap, .gram-gap, .gapfill, .cloze-gap')) kind='gap';
            else if (host.matches('.wf-row, .wordform-row')) kind='wf';
            else if (host.matches('.match-item, .match-card, .match-row, .pair-row')) kind='match';
            else if (host.matches('.builder, .reorder-row, .order-row')) kind='builder';
            else if (host.matches('.mic-row, .speech-row, .speak-row')) kind='mic';
            else if (host.matches('textarea')) kind='writing';
            else if (host.matches('.vocab-card, .word-card, .vocabulary-item')) kind='vocab';
            else kind='other';
          }
          var item = describe(host, kind);
          var dup = arr.some(function(x){ return x.section_id===item.section_id && x.question===item.question && x.kind===item.kind; });
          if (!dup) { arr.push(item); added++; }
        });
        saveHw(arr);
        refreshFabCount();
        items.forEach(function(host){
          var b = host.querySelector('.lab-hw-add');
          if (b) { b.classList.add('added'); b.textContent = '✓'; }
        });
        toast('📚 ' + added + ' заданий из секции — в домашку');
        // BROADCAST ученику — двусторонняя секция
        try {
          var freshItems = [];
          items.forEach(function(host){
            var kind = host.__hwKind || 'other';
            freshItems.push(describe(host, kind));
          });
          if (!window.supabase) return;
          var c = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON);
          var ch = c.channel('lab-firehose-v1', { config:{ broadcast:{ self:false }}});
          ch.subscribe(function(s){
            if (s === 'SUBSCRIBED') {
              ch.send({ type:'broadcast', event:'homework-section-push', payload: {
                lesson_path: location.pathname,
                section_id: sec.id || '',
                items: freshItems, ts: Date.now()
              }});
              setTimeout(function(){ ch.unsubscribe(); }, 700);
            }
          });
        } catch(e){}
      });
      // Размещение: после section-head или в начале секции
      var head = sec.querySelector('.section-head, .section-hdr');
      if (head) {
        head.style.position = head.style.position || 'relative';
        btn.style.cssText = 'margin-top:8px;display:inline-flex';
        head.appendChild(btn);
      } else {
        btn.style.cssText = 'display:inline-flex;margin:10px 0';
        sec.insertBefore(btn, sec.firstChild);
      }
    });
  }

  var fabEl = null, overlayEl = null;

  function refreshFabCount(){
    if (!fabEl) return;
    var n = loadHw().length;
    var btn = fabEl.querySelector('.lab-hw-fab-btn');
    btn.querySelector('.n').textContent = n;
    fabEl.classList.toggle('empty', n === 0);
  }

  function buildFab(){
    fabEl = document.createElement('div');
    fabEl.className = 'lab-hw-fab empty';
    fabEl.innerHTML =
      '<button type="button" class="lab-hw-fab-btn">'+
        '<span>📚 Моя домашка</span><span class="n">0</span>'+
      '</button>';
    document.body.appendChild(fabEl);
    fabEl.querySelector('button').addEventListener('click', openOverlay);
  }

  function kindLabel(k){
    return ({mcq:'Тест',tfns:'True / False / NS',gap:'Пропуск',wf:'Word formation',match:'Match',builder:'Sentence',mic:'Speaking',writing:'Writing',vocab:'Слово'}[k] || k);
  }

  function renderList(){
    var list = overlayEl.querySelector('.lab-hw-list');
    var arr = loadHw();
    var sendBtn = overlayEl.querySelector('.lab-hw-send');
    var clearBtn = overlayEl.querySelector('.lab-hw-clear');
    if (!arr.length) {
      list.innerHTML = '<div class="lab-hw-empty"><span class="em">📭</span>Пока ничего не положили в домашку.<br>Жми кнопку <strong>+</strong> у заданий которые хочешь повторить.</div>';
      sendBtn.disabled = true;
      clearBtn.style.display = 'none';
      return;
    }
    sendBtn.disabled = false;
    clearBtn.style.display = '';
    list.innerHTML = arr.map(function(it, i){
      var lines = [];
      if (it.section_title) lines.push('<div class="lab-hw-meta"><b>Раздел:</b> '+escapeHTML(it.section_title)+'</div>');
      if (it.correct) lines.push('<div class="lab-hw-meta"><b>Правильный ответ:</b> '+escapeHTML(it.correct)+'</div>');
      if (it.student_answer) lines.push('<div class="lab-hw-meta"><b>Мой ответ был:</b> '+escapeHTML(it.student_answer)+'</div>');
      return '<div class="lab-hw-item" data-i="'+i+'">'+
        '<button type="button" class="lab-hw-rm" title="Убрать">×</button>'+
        '<span class="lab-hw-kind">'+escapeHTML(kindLabel(it.kind))+'</span>'+
        '<div class="lab-hw-q">'+escapeHTML(it.question || '(без вопроса)')+'</div>'+
        lines.join('')+
      '</div>';
    }).join('');
    list.querySelectorAll('.lab-hw-rm').forEach(function(b){
      b.addEventListener('click', function(){
        var idx = +b.closest('.lab-hw-item').dataset.i;
        var a = loadHw(); a.splice(idx, 1); saveHw(a);
        refreshFabCount(); renderList();
      });
    });
  }

  function escapeHTML(s){
    return String(s||'').replace(/[&<>"']/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c];
    });
  }

  function buildOverlay(){
    overlayEl = document.createElement('div');
    overlayEl.className = 'lab-hw-overlay';
    overlayEl.innerHTML =
      '<div class="lab-hw-modal">'+
        '<div class="lab-hw-modal-h">'+
          '<div>'+
            '<h3>📚 Моя домашка</h3>'+
            '<div class="sub">Задания которые я положил/а сюда. Учитель увидит этот список.</div>'+
          '</div>'+
          '<button type="button" class="lab-hw-close" aria-label="Закрыть">×</button>'+
        '</div>'+
        '<div class="lab-hw-list"></div>'+
        '<div class="lab-hw-modal-f">'+
          '<button type="button" class="lab-hw-clear">🗑 Очистить</button>'+
          '<button type="button" class="lab-hw-send">📤 Отправить учителю</button>'+
        '</div>'+
      '</div>';
    document.body.appendChild(overlayEl);
    overlayEl.addEventListener('click', function(e){ if (e.target === overlayEl) closeOverlay(); });
    overlayEl.querySelector('.lab-hw-close').addEventListener('click', closeOverlay);
    overlayEl.querySelector('.lab-hw-clear').addEventListener('click', function(){
      if (!confirm('Удалить все задания из домашки?')) return;
      saveHw([]); refreshFabCount(); renderList();
    });
    overlayEl.querySelector('.lab-hw-send').addEventListener('click', sendHomework);
  }

  function openOverlay(){
    if (!overlayEl) buildOverlay();
    renderList();
    overlayEl.classList.add('show');
  }
  function closeOverlay(){
    if (overlayEl) overlayEl.classList.remove('show');
  }

  async function ensureName(){
    var n = getName();
    if (n) return n;
    // Если ученик ещё не вводил имя — спросим коротко прямо здесь
    return new Promise(function(resolve){
      var name = window.prompt('Как тебя зовут? (один раз, чтобы учитель видел домашку)') || '';
      name = name.trim();
      if (name) { try { localStorage.setItem('lab-student-name', name); } catch(e){} }
      resolve(name);
    });
  }

  async function sendHomework(){
    if (observerView) { toast('👁 Observer · просто смотрю как ученик отправит'); return; }
    var arr = loadHw();
    if (!arr.length) return;
    var sendBtn = overlayEl.querySelector('.lab-hw-send');
    sendBtn.disabled = true;
    sendBtn.textContent = '⏳ Отправляю…';
    var name = await ensureName();
    var room = roomFor(name);

    // Lazy SDK
    if (!window.supabase) {
      await new Promise(function(res, rej){
        var sc = document.createElement('script');
        sc.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js';
        sc.onload = res; sc.onerror = rej;
        document.head.appendChild(sc);
      }).catch(function(){});
    }
    var ok = false, err = '';
    try {
      var client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON);
      var title = (document.querySelector('.lab-hero h1, .hero h1, h1')?.textContent || document.title || '').trim();
      var resp = await client.from('lab_submissions').insert({
        room_id: room,
        lesson_path: location.pathname,
        section_id: 'homework-batch',
        section_title: '📚 Homework · ' + arr.length + ' item' + (arr.length>1?'s':'') + ' · ' + short(title, 60),
        student_role: name ? ('homework:' + name) : 'homework:anonymous',
        score: 0,
        total: arr.length,
        misses: arr
      });
      if (resp.error) { err = resp.error.message; } else { ok = true; }
      // Broadcast в firehose — чтобы Маша в teacher-live.html увидела сразу
      try {
        var fh = client.channel('lab-firehose-v1', { config:{ broadcast:{ self:false }}});
        fh.subscribe(function(s){
          if (s === 'SUBSCRIBED') {
            fh.send({ type:'broadcast', event:'homework-batch', payload: {
              room_id: room, name: name||'', lesson_path: location.pathname,
              lesson_title: short(title, 80), count: arr.length, ts: Date.now()
            }});
            setTimeout(function(){ fh.unsubscribe(); }, 800);
          }
        });
      } catch(e){}
      // Опциональный POST в локальный AI Hub (если запущен на этой машине)
      // — silent fail. Hub не основной, основное persist уже сработало выше.
      try {
        var hubMsg = '📚 Новая домашка от ' + (name || 'ученика') +
                     ' · ' + arr.length + ' заданий · ' +
                     short(title, 60);
        fetch('http://127.0.0.1:8765/api/send-telegram', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: hubMsg }),
          mode: 'no-cors'
        }).catch(function(){});
      } catch(e){}
    } catch(e) { err = e.message || String(e); }
    sendBtn.disabled = false;
    sendBtn.textContent = '📤 Отправить учителю';
    if (ok) {
      saveHw([]);
      refreshFabCount();
      renderList();
      toast('Домашка улетела учителю · ' + arr.length + ' заданий');
      setTimeout(closeOverlay, 1200);
    } else {
      toast('Не получилось отправить: ' + (err || 'попробуй ещё'));
    }
  }

  ready(function(){
    injectStyle();
    try {
      if (localStorage.getItem('lab-teacher-mode') === 'on') {
        document.body.classList.add('lab-teacher-on');
      }
    } catch(e){}
    buildFab();
    scanAndDecorate();
    refreshFabCount();
    // Listener — ученик принимает homework-section-push от учителя
    (function hookHwReceive(){
      if (!window.supabase) return setTimeout(hookHwReceive, 400);
      try {
        var c = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON);
        var ch = c.channel('lab-firehose-v1', { config:{ broadcast:{ self:false }}});
        ch.on('broadcast', { event:'homework-section-push' }, function(p){
          var data = p.payload || {};
          if (data.lesson_path !== location.pathname) return;
          if (!Array.isArray(data.items) || !data.items.length) return;
          var arr = loadHw();
          var added = 0;
          data.items.forEach(function(it){
            var dup = arr.some(function(x){ return x.section_id===it.section_id && x.question===it.question && x.kind===it.kind; });
            if (!dup) { arr.push(it); added++; }
          });
          if (added) {
            saveHw(arr);
            refreshFabCount();
            toast('📚 Учитель закинул в домашку: ' + added + ' заданий');
          }
        });
        ch.subscribe();
      } catch(e){}
    })();
    // Если урок дорисовывается динамически — переоблететь
    var mo = new MutationObserver(function(){ scanAndDecorate(); });
    mo.observe(document.body, { childList: true, subtree: true });
  });
})();
