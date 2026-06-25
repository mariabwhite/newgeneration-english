/* lab-quick-speak.js v1 — после каждой обычной section.section добавляет
   collapsible блок «🎙 Quick speak» с 3 questions по теме секции.
   Questions генерятся через Pollinations один раз на section и кэшируются. */
(function(){
  if (window.__labQuickSpeakLoaded) return;
  window.__labQuickSpeakLoaded = true;

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function esc(s){
    return String(s||'').replace(/[&<>"']/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c];
    });
  }

  function injectStyle(){
    if (document.getElementById('lab-qs-style')) return;
    var s = document.createElement('style');
    s.id = 'lab-qs-style';
    s.textContent =
      '.lab-qs{margin:14px 0 6px;padding:12px 16px;border-radius:10px;'+
        'background:color-mix(in srgb, var(--accent, #fbbf24) 8%, var(--surface, rgba(15,20,30,.82)));'+
        'border:1px solid color-mix(in srgb, var(--accent, #fbbf24) 25%, transparent);'+
        'color:var(--text, #f3eee5);font-family:"Manrope",sans-serif}'+
      '.lab-qs-h{display:flex;justify-content:space-between;align-items:center;cursor:pointer;gap:8px;flex-wrap:wrap}'+
      '.lab-qs-h .ttl{font:800 .82rem/1 "JetBrains Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent, #fbbf24);display:flex;align-items:center;gap:8px}'+
      '.lab-qs-h .meta{font:600 .72rem/1 "JetBrains Mono",monospace;opacity:.6}'+
      '.lab-qs-body{display:none;margin-top:10px}'+
      '.lab-qs.open .lab-qs-body{display:block}'+
      '.lab-qs ul{margin:8px 0 4px 18px;padding:0}'+
      '.lab-qs li{margin:4px 0;font:600 .92rem/1.55 "Manrope",sans-serif}'+
      '.lab-qs .hint{margin-top:6px;font:500 .78rem/1.5 "Manrope",sans-serif;opacity:.65;font-style:italic}'+
      '.lab-qs-loading{font:500 .82rem/1.4 "Manrope",sans-serif;opacity:.7}';
    document.head.appendChild(s);
  }

  function key(secId){ return 'lab-qs:' + location.pathname + ':' + secId; }
  function loadCached(k){
    try {
      var raw = localStorage.getItem(k);
      if (!raw) return null;
      var obj = JSON.parse(raw);
      if (Date.now() - obj.ts > 1000*60*60*24*14) return null;
      return obj.questions;
    } catch(e){ return null; }
  }
  function saveCached(k, qs){
    try { localStorage.setItem(k, JSON.stringify({ ts: Date.now(), questions: qs })); } catch(e){}
  }

  async function generateQuestions(secTitle, secExcerpt, lessonTitle, level){
    var prompt = 'Lab-урок: "' + lessonTitle + '" (' + level + '). Section: "' + secTitle + '"' +
      (secExcerpt ? '. Section start: "' + secExcerpt + '"' : '') +
      '\nGive 3 short speaking questions (5-12 words each) on THIS section topic. Output STRICT JSON array of strings: ["Q1?","Q2?","Q3?"]';
    var resp = await fetch('https://text.pollinations.ai/openai', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        messages: [
          { role:'system', content:'You are an English teacher creating speaking prompts. Output ONLY valid JSON array of 3 strings, nothing else.' },
          { role:'user', content: prompt }
        ],
        model:'openai', private:true, seed: Math.floor(Math.random()*1e6)
      })
    });
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    var data = await resp.json().catch(async ()=>({raw: await resp.text()}));
    var text = data?.choices?.[0]?.message?.content || data?.raw || '';
    var m = text.match(/\[[\s\S]*\]/);
    if (!m) throw new Error('no JSON');
    var arr = JSON.parse(m[0]);
    if (!Array.isArray(arr)) throw new Error('not array');
    return arr.slice(0, 3).map(function(q){ return String(q).trim(); }).filter(Boolean);
  }

  function render(sec, questions, opts){
    var box = document.createElement('div');
    box.className = 'lab-qs';
    box.innerHTML =
      '<div class="lab-qs-h">'+
        '<span class="ttl">🎙 Quick speak</span>'+
        '<span class="meta">'+(opts.cached?'cached':'')+' · click</span>'+
      '</div>'+
      '<div class="lab-qs-body">'+
        '<ul>' + questions.map(function(q){ return '<li>'+esc(q)+'</li>'; }).join('') + '</ul>'+
        '<div class="hint">Read each one aloud. Don\'t plan — speak in full sentences for 30 seconds each.</div>'+
      '</div>';
    box.querySelector('.lab-qs-h').addEventListener('click', function(){ box.classList.toggle('open'); });
    // Insert at the end of the section
    var card = sec.querySelector('.card') || sec;
    card.appendChild(box);
  }

  function shouldSkip(sec){
    // Не дублируем для speaking-секций которые уже есть
    var h2 = sec.querySelector('h2');
    if (!h2) return true;
    var t = (h2.textContent || '').toLowerCase();
    if (/speak|oral|interview|monologue|dialogue|conversation|task 1|task 2|task 3|task 4/i.test(t)) return true;
    if (sec.id === 'auto-vocab') return true;
    if (sec.id === 'lab-speech-coach') return true;
    return false;
  }

  function lessonMeta(){
    var h1 = document.querySelector('.lab-hero h1, .hero h1, h1');
    var level = (location.pathname.match(/lingua-boost-lab\/([a-z0-9\-]+)\//) || [,''])[1].toUpperCase();
    return {
      title: (h1?.textContent || document.title || '').trim().slice(0,150),
      level: level
    };
  }

  async function processOne(sec, meta){
    if (sec.__qsProcessed) return;
    sec.__qsProcessed = true;
    if (shouldSkip(sec)) return;
    var h2 = sec.querySelector('h2');
    var title = (h2?.textContent || '').trim();
    if (!title) return;
    var p = sec.querySelector('p, li, .section-sub, .stmt');
    var excerpt = ((p?.textContent) || '').replace(/\s+/g,' ').trim().slice(0, 200);
    var k = key(sec.id || title.slice(0,40));
    var cached = loadCached(k);
    if (cached && cached.length) {
      render(sec, cached, { cached: true });
      return;
    }
    // Loading placeholder
    var loader = document.createElement('div');
    loader.className = 'lab-qs';
    loader.innerHTML = '<div class="lab-qs-h"><span class="ttl">🎙 Quick speak</span><span class="meta">preparing…</span></div><div class="lab-qs-loading">⏳ generating speaking questions…</div>';
    var card = sec.querySelector('.card') || sec;
    card.appendChild(loader);
    try {
      var qs = await generateQuestions(title, excerpt, meta.title, meta.level);
      if (qs && qs.length) {
        saveCached(k, qs);
        loader.remove();
        render(sec, qs, { cached: false });
      } else {
        loader.querySelector('.lab-qs-loading').textContent = '—';
      }
    } catch(e) {
      loader.querySelector('.lab-qs-loading').textContent = '⚠ unable to generate · refresh later';
    }
  }

  ready(function(){
    injectStyle();
    var meta = lessonMeta();
    var sections = document.querySelectorAll('section.section');
    // Stagger requests чтобы Pollinations не задушило (1 sec между)
    var i = 0;
    sections.forEach(function(sec){
      setTimeout(function(){ processOne(sec, meta); }, i * 1000);
      i++;
    });
  });
})();
