/* lab-ai-feedback.js — AI разбор open-text (writing + speaking transcript).
   Добавляет кнопку «🤖 AI разбор» рядом с каждым textarea (writing)
   и под mic-transcript (speaking). По клику шлёт текст в Supabase Edge Function
   `lab-ai-review`, которая зовёт Claude/GPT и возвращает разбор по пунктам:
   грамматика · лексика · части речи · времена · порядок слов.

   Активация: подключить + URL ?ai=on (или всегда — снять if-флаг).
   Edge Function deploy: см. supabase/functions/lab-ai-review/index.ts. */
(function(){
  if (window.__labAiLoaded) return;
  window.__labAiLoaded = true;

  var SUPABASE_URL = "https://iqzlphbvmfgoygnozbya.supabase.co";
  var SUPABASE_ANON = "sb_publishable_hYhBk3xS90uouUFd_DZWUw_sOv-6JGO";
  var FN_URL = SUPABASE_URL + "/functions/v1/lab-ai-review";

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function injectStyle(){
    var s = document.createElement('style');
    s.textContent = ''+
      '.lab-ai-btn{margin-top:8px;padding:9px 16px;border-radius:10px;border:1.5px solid #6b46c1;'+
        'background:linear-gradient(135deg,#7c3aed 0%,#a855f7 100%);color:#fff;'+
        'font:800 11px/1 "JetBrains Mono",monospace;letter-spacing:.12em;text-transform:uppercase;cursor:pointer}'+
      '.lab-ai-btn:hover{box-shadow:0 4px 14px rgba(124,58,237,.42)}'+
      '.lab-ai-btn:disabled{opacity:.55;cursor:wait}'+
      '.lab-ai-report{display:none;margin-top:12px;background:#faf7ff;border:1px solid #d4c0f7;'+
        'border-left:4px solid #7c3aed;border-radius:0 12px 12px 0;padding:14px 18px;'+
        'font:600 .92rem/1.55 "Manrope",sans-serif;color:#1a1f2e;white-space:pre-wrap}'+
      '.lab-ai-report.show{display:block}'+
      '.lab-ai-report .ai-h{font:800 .82rem/1 "JetBrains Mono",monospace;letter-spacing:.14em;'+
        'text-transform:uppercase;color:#7c3aed;margin-bottom:10px}'+
      '[data-lab-theme="dark"] .lab-ai-report{background:#1e1a2e;border-color:#5b3aa8;color:#f3eee5}'+
      '[data-lab-theme="dark"] .lab-ai-report .ai-h{color:#c5a3ff}';
    document.head.appendChild(s);
  }

  function makeBtn(label){
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'lab-ai-btn';
    b.textContent = label || '🤖 AI разбор';
    return b;
  }
  function makeReport(){
    var r = document.createElement('div');
    r.className = 'lab-ai-report';
    return r;
  }

  async function callAI(payload){
    try {
      var resp = await fetch(FN_URL, {
        method: 'POST',
        headers: { 'Content-Type':'application/json', 'apikey': SUPABASE_ANON, 'Authorization': 'Bearer '+SUPABASE_ANON },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) {
        var t = await resp.text();
        return { error: 'HTTP '+resp.status+' · '+t.slice(0,200) };
      }
      return await resp.json();
    } catch (e) {
      return { error: e.message };
    }
  }

  function attachWriting(textarea){
    if (textarea.__aiAttached) return;
    textarea.__aiAttached = true;
    var btn = makeBtn('🤖 AI разбор письма');
    var report = makeReport();
    textarea.parentNode.insertBefore(btn, textarea.nextSibling);
    textarea.parentNode.insertBefore(report, btn.nextSibling);

    btn.addEventListener('click', async function(){
      var text = (textarea.value || '').trim();
      if (text.length < 20) {
        report.classList.add('show');
        report.innerHTML = '<div class="ai-h">⚠️ нужен текст</div>Напиши хотя бы 20 символов.';
        return;
      }
      btn.disabled = true;
      btn.textContent = '⏳ разбираю…';
      report.classList.add('show');
      report.innerHTML = '<div class="ai-h">⏳ AI работает…</div>Жди ~10 секунд.';
      var r = await callAI({ mode: 'writing', text: text, lesson: location.pathname });
      btn.disabled = false;
      btn.textContent = '🤖 AI разбор письма';
      if (r.error) {
        report.innerHTML = '<div class="ai-h">⚠️ не удалось</div>'+r.error+
          '<br><br><em>Если ошибка про функцию — учителю нужно задеплоить supabase/functions/lab-ai-review.</em>';
      } else {
        report.innerHTML = '<div class="ai-h">🤖 AI разбор</div>'+(r.review || JSON.stringify(r));
      }
    });
  }

  function attachSpeaking(micRow){
    if (micRow.__aiAttached) return;
    micRow.__aiAttached = true;
    var btn = makeBtn('🤖 AI разбор речи');
    var report = makeReport();
    micRow.appendChild(btn);
    micRow.appendChild(report);

    btn.addEventListener('click', async function(){
      var tr = micRow.querySelector('.mic-transcript');
      var text = ((tr && tr.textContent) || '').replace(/^"|"$/g,'').trim();
      if (text.length < 6) {
        report.classList.add('show');
        report.innerHTML = '<div class="ai-h">⚠️ запиши речь</div>Сначала нажми 🎙 и произнеси предложение.';
        return;
      }
      btn.disabled = true; btn.textContent = '⏳ разбираю…';
      report.classList.add('show');
      report.innerHTML = '<div class="ai-h">⏳ AI работает…</div>';
      var target = micRow.dataset.target || '';
      var wpm = parseInt(micRow.dataset.wpm || '0', 10);
      var r = await callAI({ mode: 'speaking', transcript: text, target: target, wpm: wpm, lesson: location.pathname });
      btn.disabled = false; btn.textContent = '🤖 AI разбор речи';
      if (r.error) {
        report.innerHTML = '<div class="ai-h">⚠️ не удалось</div>'+r.error;
      } else {
        report.innerHTML = '<div class="ai-h">🤖 AI разбор</div>'+(r.review || JSON.stringify(r));
      }
    });
  }

  ready(function(){
    // Feature flag — кнопки рисуются только если явно включено.
    // Edge Function lab-ai-review не задеплоена (требует ANTHROPIC_API_KEY на Anthropic Console).
    // Включить точечно: ?ai=on в URL, или глобально window.LAB_AI_ENABLED=true перед загрузкой.
    var enabled = window.LAB_AI_ENABLED === true || /[?&]ai=on(?:&|$)/.test(location.search);
    if (!enabled) return;
    injectStyle();
    document.querySelectorAll('.write textarea, textarea.writing-area, textarea[data-write]').forEach(attachWriting);
    document.querySelectorAll('.mic-row').forEach(attachSpeaking);
  });
})();
