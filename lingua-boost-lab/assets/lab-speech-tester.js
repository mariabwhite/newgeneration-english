/* lab-speech-tester.js v1 — универсальный AI Speech Coach.

   Что делает:
   • Внизу любого Lab-урока появляется свёрнутая полоса «🎙 Speech Coach».
     Click → разворачивается полноценный тренажёр.
   • Pollinations один раз генерит 5-7 speaking-criteria по материалам урока
     (заголовок + первый осмысленный текст), кэширует на 7 дней.
   • Кнопка «🎙 Начать запись» — Web Speech Recognition, live transcript,
     словарь-метрик: words / WPM / linkers / longest pause / B2+ words.
   • Каждое criterion подсвечивается ✓ как только в речи упомянуто ключевое
     слово/паттерн.
   • На остановке — Pollinations разбирает запись по criteria + общая оценка.
   • Transcript сохраняется (lab-coach-persist подхватывает).
   Без credits, без бэкенда. */
(function(){
  if (window.__labSpeechTesterLoaded) return;
  window.__labSpeechTesterLoaded = true;

  // Observer mode и teacher mode — coach строится, но запись пусть учитель не
  // дёргает (его клики не должны транслироваться). По факту его click handlers
  // безопасны для observer — Web Speech Recognition требует mic permission, в
  // iframe она не разрешена, тренажёр просто покажет «mic недоступен».
  var observeMode = /[?&]observe=/.test(location.search);

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function injectStyle(){
    if (document.getElementById('lab-coach-style')) return;
    var s = document.createElement('style');
    s.id = 'lab-coach-style';
    s.textContent = ''+
      '.lab-coach-section{margin:24px auto !important;padding:20px 24px !important;border-radius:16px !important;'+
        'background:var(--card, var(--surface, #1b232d)) !important;'+
        'border:1px solid var(--line, color-mix(in srgb, var(--accent, #fbbf24) 35%, transparent)) !important;'+
        'color:var(--text, #f3eee5) !important;font-family:"Manrope",sans-serif !important;'+
        'max-width:1180px !important;width:calc(100% - 24px) !important;display:block !important;box-sizing:border-box;'+
        'box-shadow:0 8px 28px rgba(0,0,0,.18)}'+
      '@media(max-width:600px){.lab-coach-section{margin:14px 8px !important;padding:14px !important}}'+
      '.lc-grid{display:grid;grid-template-columns:1fr 1.2fr;gap:18px;align-items:start}'+
      '@media(max-width:780px){.lc-grid{grid-template-columns:1fr}}'+
      '.lc-crit-h{font:800 .78rem/1 "JetBrains Mono",monospace;letter-spacing:.16em;text-transform:uppercase;color:#fbbf24;margin-bottom:10px;opacity:.85}'+
      '.lc-left,.lc-right{min-width:0}'+
      '.lab-coach-toggle{cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:10px}'+
      '.lab-coach-toggle h2{margin:0;font:800 1rem/1.2 "Manrope",sans-serif;color:var(--accent, #fbbf24)}'+
      '.lab-coach-toggle .meta{font:600 .8rem/1 "JetBrains Mono",monospace;color:color-mix(in srgb, var(--accent, #fbbf24) 60%, transparent);letter-spacing:.06em}'+
      '.lab-coach-body{display:none;margin-top:14px}'+
      '.lab-coach-section.expanded .lab-coach-body{display:block}'+

      '.lc-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:10px}'+
      '.lc-btn{padding:10px 18px;border-radius:50px;border:0;cursor:pointer;'+
        'font:800 .82rem/1 "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;'+
        'background:linear-gradient(135deg,#22c55e 0%,#16a34a 100%);color:#fff;'+
        'box-shadow:0 4px 14px rgba(34,197,94,.32);display:inline-flex;align-items:center;gap:6px}'+
      '.lc-btn:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(34,197,94,.42)}'+
      '.lc-btn.recording{background:linear-gradient(135deg,#ef4444 0%,#dc2626 100%);'+
        'animation:lcPulse 1.4s ease-in-out infinite}'+
      '@keyframes lcPulse{50%{box-shadow:0 0 0 6px rgba(239,68,68,.18)}}'+
      '.lc-btn.lc-stop{background:linear-gradient(135deg,#475569 0%,#334155 100%)}'+
      '.lc-btn.lc-analyze{background:linear-gradient(135deg,#7c3aed 0%,#a855f7 100%)}'+
      '.lc-btn:disabled{opacity:.55;cursor:wait;transform:none}'+

      '.lc-stats{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin:10px 0}'+
      '@media(max-width:780px){.lc-stats{grid-template-columns:repeat(auto-fit,minmax(80px,1fr))}}'+
      '.lc-stat{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:8px 12px}'+
      '.lc-stat .lc-lbl{font:700 .68rem/1 "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:rgba(251,191,36,.6);margin-bottom:3px}'+
      '.lc-stat .lc-val{font:800 1.1rem/1 "Manrope",sans-serif;color:#fbbf24}'+

      '.lc-transcript{background:#000;color:#E8F5E9;border:1px solid rgba(255,255,255,.14);border-radius:10px;'+
        'padding:12px 14px;min-height:110px;max-height:240px;overflow-y:auto;font:500 .92rem/1.55 "Manrope",sans-serif;'+
        'margin:10px 0}'+
      '.lc-transcript:empty::before{content:"Live transcript появится здесь когда ты начнёшь говорить…";color:rgba(251,191,36,.6);font-style:italic}'+
      '.lc-transcript .interim{opacity:.55;font-style:italic}'+

      '.lc-criteria{display:flex;flex-direction:column;gap:6px;margin:10px 0}'+
      '.lc-crit{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:8px;'+
        'background:rgba(255,255,255,.05);border-left:3px solid #475569;transition:all .2s}'+
      '.lc-crit.hit{border-left-color:#22c55e;background:#0f1f15}'+
      '.lc-crit .lc-tick{width:22px;height:22px;border-radius:50%;background:#334155;color:#fff;'+
        'display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;font-weight:800}'+
      '.lc-crit.hit .lc-tick{background:#22c55e}'+
      '.lc-crit .lc-crit-text{flex:1;font:600 .9rem/1.45 "Manrope",sans-serif;color:#E8F5E9}'+
      '.lc-crit .lc-crit-hint{font:500 .76rem/1.3 "Manrope",sans-serif;color:rgba(251,191,36,.6);font-style:italic;margin-top:2px}'+

      '.lc-loading{color:rgba(251,191,36,.6);font:600 .82rem/1.4 "Manrope",sans-serif;text-align:center;padding:14px}'+
      '.lc-loading::before{content:"⏳ ";margin-right:6px}'+
      '.lc-analysis{background:linear-gradient(135deg,#1e1a2e 0%,#241c3e 100%);border:1px solid #5b3aa8;'+
        'border-left:4px solid #7c3aed;border-radius:10px;padding:14px 16px;margin-top:10px;'+
        'font:500 .92rem/1.6 "Manrope",sans-serif;color:#f3eee5;white-space:pre-wrap}'+
      '.lc-analysis strong{color:#c5a3ff;font-weight:800}'+
      '.lc-analysis em{color:#fbbf24;background:rgba(251,191,36,.12);padding:1px 6px;border-radius:4px;font-style:normal}';
    document.head.appendChild(s);
  }

  function esc(s){
    return String(s||'').replace(/[&<>"']/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c];
    });
  }

  function lessonContext(){
    var h1 = document.querySelector('.lab-hero h1, .hero h1, h1');
    var sub = document.querySelector('.lab-hero .sub, .hero p, .hero .lead, .lab-hero p');
    var firstPara = document.querySelector('.card p, .reading p, .story p, .passage p, p.lead');
    return {
      title: (h1?.textContent || document.title || '').trim().slice(0, 200),
      sub: (sub?.textContent || '').trim().slice(0, 300),
      excerpt: (firstPara?.textContent || '').trim().slice(0, 600),
      level: (location.pathname.match(/lingua-boost-lab\/([a-z0-9\-]+)\//) || [,''])[1].toUpperCase()
    };
  }

  function criteriaKey(){ return 'lab-coach-criteria:' + location.pathname; }
  function loadCachedCriteria(){
    try {
      var raw = localStorage.getItem(criteriaKey());
      if (!raw) return null;
      var obj = JSON.parse(raw);
      if (Date.now() - obj.ts > 1000*60*60*24*7) return null;
      return obj.criteria;
    } catch(e){ return null; }
  }
  function saveCachedCriteria(criteria){
    try { localStorage.setItem(criteriaKey(), JSON.stringify({ ts: Date.now(), criteria })); } catch(e){}
  }

  async function generateCriteria(ctx){
    var prompt = 'Lab-урок английского. Уровень: ' + (ctx.level || 'B1') + '.\n' +
      'Заголовок: ' + ctx.title + '\n' +
      (ctx.sub ? 'Подзаголовок: ' + ctx.sub + '\n' : '') +
      (ctx.excerpt ? 'Кусок текста урока: ' + ctx.excerpt + '\n' : '') +
      '\nПридумай для ученика speaking-задание на 2-3 минуты по этой теме (one short sentence). ' +
      'Затем дай 5-7 criteria что он должен сказать. Для каждого criterion укажи ключевые слова/паттерны на английском которые система ищет в его речи.\n' +
      'Отвечай СТРОГО JSON БЕЗ markdown:\n' +
      '{"task":"<задание на английском, одна строка>","criteria":[' +
      '{"label":"<критерий, на русском, короткий>","hint":"<подсказка на английском что сказать>","keywords":["word1","phrase 2","..."]},' +
      '...]}';
    var resp = await fetch('https://text.pollinations.ai/openai', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        messages: [
          { role:'system', content: 'Ты опытный преподаватель английского. Делаешь criteria для speaking-тренажёра. Отвечаешь чистым JSON без пояснений.' },
          { role:'user', content: prompt }
        ],
        model:'openai', private:true, seed: Math.floor(Math.random()*1e6)
      })
    });
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    var data = await resp.json().catch(async ()=>({raw: await resp.text()}));
    var text = data?.choices?.[0]?.message?.content || data?.raw || '';
    var m = text.match(/\{[\s\S]*\}/);
    if (!m) throw new Error('AI не дал JSON');
    var obj = JSON.parse(m[0]);
    if (!obj.task || !Array.isArray(obj.criteria)) throw new Error('JSON неполный');
    return obj;
  }

  var state = {
    rec: null, recording: false, started: 0,
    finalText: '', interimText: '',
    criteria: null, task: '',
    longestPauseMs: 0, lastWordAt: 0
  };

  var LINKERS = ['however','whereas','in contrast','unlike','moreover','furthermore','in addition',
    'because','since','as a result','therefore','thus','so','then','first','then','finally','to conclude',
    'in summary','overall','on the other hand','for example','for instance','such as'];
  var B2_VOCAB = ['nevertheless','despite','consequently','arguably','undoubtedly','encompass','enhance',
    'establish','implement','perceive','sustain','crucial','significant','remarkable','prominent','viable',
    'accommodate','derive','illustrate','notion','perspective','undertake'];

  function countMatches(text, list){
    var t = (' ' + text.toLowerCase() + ' ').replace(/[^a-z\s]/g,' ').replace(/\s+/g,' ');
    var n = 0;
    list.forEach(function(p){ if (t.indexOf(' '+p+' ') >= 0) n++; });
    return n;
  }

  function updateStats(box){
    var full = (state.finalText + ' ' + state.interimText).replace(/\s+/g,' ').trim();
    var words = full ? (full.match(/\S+/g) || []).length : 0;
    var dur = state.started ? Math.max(1, (Date.now() - state.started)/1000) : 0;
    var wpm = dur ? Math.round(words / dur * 60) : 0;
    var linkers = countMatches(full, LINKERS);
    var b2 = countMatches(full, B2_VOCAB);
    var s = box.querySelectorAll('.lc-stat .lc-val');
    if (s[0]) s[0].textContent = words;
    if (s[1]) s[1].textContent = wpm || '—';
    if (s[2]) s[2].textContent = linkers;
    if (s[3]) s[3].textContent = b2;
    if (s[4]) s[4].textContent = (state.longestPauseMs/1000).toFixed(1) + 's';
    // criteria check
    var lc = box.querySelectorAll('.lc-crit');
    state.criteria.forEach(function(c, i){
      var hit = (c.keywords || []).some(function(k){
        return full.toLowerCase().indexOf(String(k).toLowerCase()) >= 0;
      });
      if (lc[i]) lc[i].classList.toggle('hit', hit);
    });
  }

  function startRecognition(box){
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { alert('Web Speech не поддерживается. Открой Chrome или Edge на десктопе.'); return; }
    state.rec = new SR();
    state.rec.continuous = true;
    state.rec.interimResults = true;
    state.rec.lang = 'en-US';
    state.finalText = ''; state.interimText = '';
    state.longestPauseMs = 0; state.lastWordAt = Date.now();
    state.started = Date.now();
    var transcript = box.querySelector('.lc-transcript');
    transcript.innerHTML = '';

    state.rec.onresult = function(e){
      var interim = '', final = '';
      for (var i = e.resultIndex; i < e.results.length; i++) {
        var r = e.results[i];
        if (r.isFinal) final += r[0].transcript + ' ';
        else interim += r[0].transcript + ' ';
      }
      if (final) {
        state.finalText += final;
        var now = Date.now();
        var pause = now - state.lastWordAt;
        if (pause > state.longestPauseMs) state.longestPauseMs = pause;
        state.lastWordAt = now;
      }
      state.interimText = interim;
      transcript.innerHTML = esc(state.finalText) + (interim ? ' <span class="interim">'+esc(interim)+'</span>' : '');
      transcript.scrollTop = transcript.scrollHeight;
      updateStats(box);
    };
    state.rec.onerror = function(){};
    state.rec.onend = function(){
      if (state.recording) {
        try { state.rec.start(); } catch(_){}
      }
    };
    state.rec.start();
    state.recording = true;
    var btn = box.querySelector('.lc-record');
    btn.classList.add('recording');
    btn.textContent = '⏹ Stop';
    box.querySelector('.lc-analyze').disabled = true;
  }

  function stopRecognition(box){
    state.recording = false;
    if (state.rec) { try { state.rec.stop(); } catch(_){} }
    var btn = box.querySelector('.lc-record');
    btn.classList.remove('recording');
    btn.textContent = '🎙 Record';
    box.querySelector('.lc-analyze').disabled = false;
    // Force persist через CustomEvent для lab-coach-persist
    setTimeout(function(){
      var t = box.querySelector('.lc-transcript');
      if (t) {
        // dispatch mutation чтобы persist подхватил
        var e = document.createEvent('Event'); e.initEvent('DOMNodeInserted', true, true);
        t.dispatchEvent(e);
      }
    }, 100);
  }

  async function analyze(box){
    var full = state.finalText.replace(/\s+/g,' ').trim();
    if (full.length < 10) { alert('Сначала наговори хотя бы пару предложений.'); return; }
    var btn = box.querySelector('.lc-analyze');
    btn.disabled = true;
    btn.textContent = '⏳ AI разбирает…';
    var prompt = 'Ученик английского ' + (state.level || 'B1') + '. Задание: "' + state.task + '"\n' +
      'Critеria: ' + state.criteria.map(function(c){ return c.label; }).join(' / ') + '\n' +
      'Распознанная речь: "' + full + '"\n' +
      'Стат: words ' + (full.match(/\S+/g)||[]).length + ', WPM ' + Math.round((full.match(/\S+/g)||[]).length / Math.max(1,(Date.now()-state.started)/60000)) + '.\n' +
      'Дай тёплый разбор по-русски на 6-8 строк: что получилось, 3-5 конкретных ошибок (цитата → правильно), какие criteria покрыл, какие — нет, и один тёплый совет.';
    try {
      var resp = await fetch('https://text.pollinations.ai/openai', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({
          messages:[
            { role:'system', content:'Ты тёплый и точный наставник английского. Без брендов, без markdown заголовков, кратко.' },
            { role:'user', content: prompt }
          ],
          model:'openai', private:true, seed: Math.floor(Math.random()*1e6)
        })
      });
      var data = await resp.json().catch(async ()=>({raw: await resp.text()}));
      var text = data?.choices?.[0]?.message?.content || data?.raw || '(пусто)';
      var analysis = box.querySelector('.lc-analysis');
      if (!analysis) {
        analysis = document.createElement('div');
        analysis.className = 'lc-analysis';
        box.querySelector('.lab-coach-body').appendChild(analysis);
      }
      analysis.innerHTML = String(text).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>').replace(/"([^"\n]{1,80})"/g,'<em>"$1"</em>').replace(/\n/g,'<br>');
    } catch(e) {
      alert('AI разбор не получилось: ' + e.message);
    }
    btn.disabled = false;
    btn.textContent = '🤖 AI review';
  }

  function buildUI(criteriaObj){
    state.criteria = criteriaObj.criteria;
    state.task = criteriaObj.task;
    var section = document.createElement('section');
    section.className = 'section lab-coach-section';
    section.id = 'lab-speech-coach';
    // Inline style — единая ширина 1240 по body как у lab-total и vocab
    section.style.cssText = 'max-width:1240px;margin:24px auto;padding:20px clamp(16px,3vw,28px);box-sizing:border-box';
    section.innerHTML =
      '<div class="lab-coach-toggle">'+
        '<h2>🎙 Speech Coach · record yourself and get instant feedback</h2>'+
        '<span class="meta">click to collapse</span>'+
      '</div>'+
      '<div class="lab-coach-body">'+
        '<div style="background:color-mix(in srgb, var(--accent, #fbbf24) 14%, transparent);border:1px solid color-mix(in srgb, var(--accent, #fbbf24) 45%, transparent);border-radius:10px;padding:13px 16px;margin-bottom:14px;color:#fff;font:700 1rem/1.55 Manrope;text-shadow:0 1px 2px rgba(0,0,0,.4)"><strong style="color:var(--accent, #fbbf24);font-size:.85rem;letter-spacing:.14em;display:block;margin-bottom:6px;text-transform:uppercase">📋 Task</strong>'+esc(state.task)+'</div>'+
        '<div class="lc-grid">'+
          '<div class="lc-left">'+
            '<div class="lc-crit-h">Criteria · real time</div>'+
            '<div class="lc-criteria">'+
              state.criteria.map(function(c){
                return '<div class="lc-crit"><div class="lc-tick">✓</div><div style="flex:1"><div class="lc-crit-text">'+esc(c.label)+'</div>'+
                  (c.hint ? '<div class="lc-crit-hint">'+esc(c.hint)+'</div>' : '')+
                  '</div></div>';
              }).join('')+
            '</div>'+
          '</div>'+
          '<div class="lc-right">'+
            '<div class="lc-row">'+
              '<button type="button" class="lc-btn lc-record">🎙 Start recording</button>'+
              '<button type="button" class="lc-btn lc-analyze" disabled>🤖 AI review</button>'+
            '</div>'+
            '<div class="lc-transcript grader-transcript" data-transcript></div>'+
            '<div class="lc-stats">'+
              '<div class="lc-stat"><div class="lc-lbl">Words</div><div class="lc-val">0</div></div>'+
              '<div class="lc-stat"><div class="lc-lbl">Pace · WPM</div><div class="lc-val">—</div></div>'+
              '<div class="lc-stat"><div class="lc-lbl">Linkers</div><div class="lc-val">0</div></div>'+
              '<div class="lc-stat"><div class="lc-lbl">B2+ vocab</div><div class="lc-val">0</div></div>'+
              '<div class="lc-stat"><div class="lc-lbl">Pause</div><div class="lc-val">0.0s</div></div>'+
            '</div>'+
          '</div>'+
        '</div>'+
      '</div>';

    // Toggle
    section.querySelector('.lab-coach-toggle').addEventListener('click', function(){
      section.classList.toggle('expanded');
      section.querySelector('.meta').textContent = section.classList.contains('expanded') ? 'click чтобы свернуть' : 'click чтобы развернуть';
    });
    // Auto-expand on first visit
    section.classList.add('expanded');
    section.querySelector('.meta').textContent = 'click чтобы свернуть';

    // Record button
    section.querySelector('.lc-record').addEventListener('click', function(){
      if (state.recording) stopRecognition(section);
      else startRecognition(section);
    });
    section.querySelector('.lc-analyze').addEventListener('click', function(){ analyze(section); });

    // Insert: перед последней section или в конце container
    // ЕДИНАЯ стратегия с lab-total и lab-vocab-builder — вставка перед <footer>.
    var anchor = document.querySelector('footer') || document.body.lastElementChild;
    if (anchor && anchor.parentNode) {
      anchor.parentNode.insertBefore(section, anchor);
    } else {
      document.body.appendChild(section);
    }
  }

  function loadInlineConfig(){
    // Урок может задать coach через <script type="application/json" id="lab-coach-config">
    var el = document.getElementById('lab-coach-config');
    if (!el) return null;
    try {
      var cfg = JSON.parse(el.textContent || '{}');
      if (cfg.task && Array.isArray(cfg.criteria)) return cfg;
    } catch(e){}
    return null;
  }

  function buildUIAt(anchor, cfg){
    // Аналог buildUI, но рендерит coach в указанном anchor вместо в конец.
    state.criteria = cfg.criteria;
    state.task = cfg.task;
    var section = document.createElement('section');
    section.className = 'section lab-coach-section';
    section.style.cssText = 'max-width:1240px;margin:24px auto;padding:20px clamp(16px,3vw,28px);box-sizing:border-box';
    section.innerHTML = '';
    document.body.insertBefore(section, document.body.firstChild); // tmp position
    // Reuse buildUI rendering by calling it; but it inserts at end. Workaround:
    var tmpFirst = document.querySelectorAll('section.section')[0];
    if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(section, anchor.nextSibling);
    // Build inner content via buildUI shell
    buildUIInner(section, cfg);
  }

  function buildUIInner(section, cfg){
    state.criteria = cfg.criteria;
    state.task = cfg.task;
    section.innerHTML =
      '<div class="lab-coach-toggle">'+
        '<h2>🎙 Speech Coach · record yourself and get instant feedback</h2>'+
        '<span class="meta">click to collapse</span>'+
      '</div>'+
      '<div class="lab-coach-body">'+
        '<div style="background:color-mix(in srgb, var(--accent, #fbbf24) 14%, transparent);border:1px solid color-mix(in srgb, var(--accent, #fbbf24) 45%, transparent);border-radius:10px;padding:13px 16px;margin-bottom:14px;color:var(--text,#fff);font:700 1rem/1.55 Manrope"><strong style="color:var(--accent, #fbbf24);font-size:.85rem;letter-spacing:.14em;display:block;margin-bottom:6px;text-transform:uppercase">📋 Task</strong>'+esc(cfg.task)+'</div>'+
        '<div class="lc-grid">'+
          '<div class="lc-left">'+
            '<div class="lc-crit-h">Criteria · real time</div>'+
            '<div class="lc-criteria">'+
              cfg.criteria.map(function(c){
                return '<div class="lc-crit"><div class="lc-tick">✓</div><div style="flex:1"><div class="lc-crit-text">'+esc(c.label)+'</div>'+
                  (c.hint ? '<div class="lc-crit-hint">'+esc(c.hint)+'</div>' : '')+
                  '</div></div>';
              }).join('')+
            '</div>'+
          '</div>'+
          '<div class="lc-right">'+
            '<div class="lc-row">'+
              '<button type="button" class="lc-btn lc-record">🎙 Start recording</button>'+
              '<button type="button" class="lc-btn lc-analyze" disabled>🤖 AI review</button>'+
            '</div>'+
            '<div class="lc-transcript grader-transcript" data-transcript></div>'+
            '<div class="lc-stats">'+
              '<div class="lc-stat"><div class="lc-lbl">Words</div><div class="lc-val">0</div></div>'+
              '<div class="lc-stat"><div class="lc-lbl">Pace · WPM</div><div class="lc-val">—</div></div>'+
              '<div class="lc-stat"><div class="lc-lbl">Linkers</div><div class="lc-val">0</div></div>'+
              '<div class="lc-stat"><div class="lc-lbl">B2+ vocab</div><div class="lc-val">0</div></div>'+
              '<div class="lc-stat"><div class="lc-lbl">Pause</div><div class="lc-val">0.0s</div></div>'+
            '</div>'+
          '</div>'+
        '</div>'+
      '</div>';
    section.querySelector('.lab-coach-toggle').addEventListener('click', function(){
      section.classList.toggle('expanded');
    });
    section.classList.add('expanded');
    section.querySelector('.lc-record').addEventListener('click', function(){
      if (state.recording) stopRecognition(section);
      else { state.criteria = cfg.criteria; state.task = cfg.task; startRecognition(section); }
    });
    section.querySelector('.lc-analyze').addEventListener('click', function(){
      state.criteria = cfg.criteria; state.task = cfg.task; analyze(section);
    });
  }

  async function init(){
    injectStyle();
    state.level = (location.pathname.match(/lingua-boost-lab\/([a-z0-9\-]+)\//) || [,''])[1].toUpperCase();

    // MULTI: inline <div data-coach-config="{...}"> или <script data-coach-config>...</script>
    var multi = document.querySelectorAll('[data-coach-config]');
    if (multi && multi.length) {
      multi.forEach(function(el){
        var raw = el.getAttribute('data-coach-config') || el.textContent || '';
        try {
          var cfg = JSON.parse(raw);
          if (cfg.task && Array.isArray(cfg.criteria)) buildUIInner(el, cfg);
        } catch(e){}
      });
      return;
    }

    // 1. Inline config (приоритет — Maria's hand-crafted criteria)
    var inline = loadInlineConfig();
    if (inline) { buildUI(inline); return; }

    // 2. Cached авто-config из прошлой сессии
    var cached = loadCachedCriteria();
    if (cached && cached.task && Array.isArray(cached.criteria)) {
      buildUI(cached);
      return;
    }

    // 3. Авто-генерация через Pollinations
    var ctx = lessonContext();
    if (!ctx.title) return;
    var loader = document.createElement('section');
    loader.className = 'section lab-coach-section';
    loader.innerHTML = '<div class="lab-coach-toggle"><h2>🎙 Speech Coach</h2><span class="meta">preparing…</span></div><div class="lc-loading">⏳ generating criteria for this lesson…</div>';
    var sections = document.querySelectorAll('section.section');
    if (sections.length) {
      var last = sections[sections.length - 1];
      last.parentNode.insertBefore(loader, last.nextSibling);
    } else {
      document.body.appendChild(loader);
    }
    try {
      var obj = await generateCriteria(ctx);
      saveCachedCriteria(obj);
      loader.remove();
      buildUI(obj);
    } catch(e) {
      loader.querySelector('.lc-loading').textContent = '⚠ Speech Coach unavailable right now. Refresh in a minute.';
    }
  }

  ready(function(){
    if (observeMode) return; // в iframe-зеркале coach не строим
    init();
  });
})();
