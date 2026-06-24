/* lab-ai-feedback.js v3 — Embedded AI tutor.
   Никаких кнопок и внешних вкладок. После «📋 Сдать раздел» и в «📊 Итог урока»
   разбор появляется автоматически прямо на сайте, через бесплатный
   text.pollinations.ai (без ключа, без credits, CORS открыт).
   Кэш: localStorage per (lesson + secId) чтобы не дёргать снова на F5. */
(function(){
  if (window.__labAiLoaded) return;
  window.__labAiLoaded = true;

  // Bесплатный openAI-compatible endpoint, не требует ключа.
  // Запасной — другая модель той же платформы.
  const AI_ENDPOINTS = [
    { url: 'https://text.pollinations.ai/openai', body: 'openai' },
    { url: 'https://text.pollinations.ai/openai', body: 'mistral' }
  ];

  const SYSTEM_PROMPT =
    'Ты тёплый, точный преподаватель английского. Разбираешь раздел онлайн-урока у школьника или взрослого ученика. ' +
    'Пиши на русском, кратко, без воды. Не повторяй задание, говори только по делу. ' +
    'Структура ответа: ' +
    '1) Одна строка — общая оценка с похвалой. ' +
    '2) Раздел «🔍 Ошибки» — каждый пункт «цитата → правильно — короткое пояснение». Максимум 6 пунктов. Если ошибок нет — напиши «Ошибок нет, держи планку». ' +
    '3) Раздел «📚 Что повторить» — 2–3 грамматические темы списком. ' +
    '4) Раздел «✨ Совет» — одна тёплая строка как звучать естественнее. ' +
    'Не упоминай ChatGPT, OpenAI, Anthropic, Pollinations, никаких брендов. Ты — наставник школы.';

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function injectStyle(){
    if (document.getElementById('lab-ai-embed-style')) return;
    const s = document.createElement('style');
    s.id = 'lab-ai-embed-style';
    s.textContent = ''+
      '.lab-ai-embed{margin-top:14px;padding:18px 20px;border-radius:14px;'+
        'background:linear-gradient(135deg,#fbf8ff 0%,#f0e9ff 100%);'+
        'border:1px solid #d4c0f7;border-left:4px solid #7c3aed;'+
        'font:500 .95rem/1.62 "Manrope",sans-serif;color:#1a1f2e;'+
        'box-shadow:0 4px 18px rgba(124,58,237,.08)}'+
      '[data-lab-theme="dark"] .lab-ai-embed{background:linear-gradient(135deg,#1e1a2e 0%,#241c3e 100%);'+
        'border-color:#5b3aa8;color:#f3eee5;box-shadow:0 4px 18px rgba(0,0,0,.32)}'+
      '.lab-ai-embed-h{display:flex;align-items:center;gap:10px;'+
        'font:800 .82rem/1 "JetBrains Mono",monospace;letter-spacing:.16em;'+
        'text-transform:uppercase;color:#7c3aed;margin-bottom:14px}'+
      '[data-lab-theme="dark"] .lab-ai-embed-h{color:#c5a3ff}'+
      '.lab-ai-embed-h .dot{width:8px;height:8px;border-radius:50%;background:#7c3aed;'+
        'animation:laiPulse 1.4s ease-in-out infinite}'+
      '@keyframes laiPulse{0%,100%{opacity:.4;transform:scale(.85)}50%{opacity:1;transform:scale(1.1)}}'+
      '.lab-ai-embed.done .dot{animation:none;background:#22c55e}'+
      '.lab-ai-embed.fail .dot{animation:none;background:#f59e0b}'+
      '.lab-ai-embed-body{white-space:pre-wrap;word-wrap:break-word}'+
      '.lab-ai-embed-body strong{color:#5b21b6;font-weight:800}'+
      '[data-lab-theme="dark"] .lab-ai-embed-body strong{color:#d4b5ff}'+
      '.lab-ai-embed-body h3,.lab-ai-embed-body h4{margin:14px 0 6px;font:800 .95rem/1.3 "Manrope",sans-serif;color:#4a2d8a}'+
      '[data-lab-theme="dark"] .lab-ai-embed-body h3,[data-lab-theme="dark"] .lab-ai-embed-body h4{color:#c5a3ff}'+
      '.lab-ai-embed-body ul,.lab-ai-embed-body ol{margin:6px 0 6px 22px;padding:0}'+
      '.lab-ai-embed-body li{margin:4px 0}'+
      '.lab-ai-embed-body em{color:#7c3aed;font-style:normal;background:#f1e9ff;padding:1px 5px;border-radius:4px}'+
      '[data-lab-theme="dark"] .lab-ai-embed-body em{color:#e9d6ff;background:#3a2a5e}'+
      '.lab-ai-embed-skel{display:flex;gap:8px;align-items:center;color:#6b46c1;font:700 .82rem/1.4 "Manrope",sans-serif}'+
      '[data-lab-theme="dark"] .lab-ai-embed-skel{color:#c5a3ff}';
    document.head.appendChild(s);
  }

  function lessonMeta(){
    const h1 = document.querySelector('.lab-hero h1, .hero h1, h1');
    const sub = document.querySelector('.lab-hero .sub, .hero p, .hero .lead');
    let level = '';
    const path = location.pathname.toLowerCase();
    const m = path.match(/lingua-boost-lab\/([a-z0-9\-]+)\//);
    if (m) level = m[1].toUpperCase().replace(/-/g,' ');
    return {
      title: (h1?.textContent || document.title || 'Lab lesson').trim(),
      sub: (sub?.textContent || '').trim(),
      level: level
    };
  }

  function sectionTitle(section, i){
    return (section.querySelector('h2')?.textContent || ('Section '+(i+1))).trim();
  }

  function collectOpenText(section){
    const out = [];
    section.querySelectorAll('textarea').forEach(t => {
      const v = (t.value || '').trim();
      if (v.length >= 5) out.push({ kind: 'writing', text: v });
    });
    section.querySelectorAll('.mic-row').forEach(row => {
      const tr = row.querySelector('.mic-transcript');
      const txt = ((tr && tr.textContent) || '').replace(/^"|"$/g,'').trim();
      const target = row.dataset.target || '';
      if (txt.length >= 3) out.push({ kind: 'speaking', text: txt, target: target });
    });
    section.querySelectorAll('input[type="text"]').forEach(inp => {
      if (inp.closest('.gap, .gapfill, .wf-row, .builder')) return;
      const v = (inp.value || '').trim();
      if (v.length >= 5) out.push({ kind: 'short-answer', text: v });
    });
    return out;
  }

  function reportTextFromContainer(container){
    const lines = [];
    const stats = container.querySelector('.lp-stats');
    if (stats) lines.push(stats.textContent.trim());
    container.querySelectorAll('.lp-list .lp-item').forEach(li => {
      lines.push('  • ' + li.textContent.replace(/\s+/g,' ').trim());
    });
    return lines.join('\n');
  }

  function buildSectionContext(section, container){
    const meta = lessonMeta();
    const idx = Array.from(document.querySelectorAll('section.section')).indexOf(section);
    const title = sectionTitle(section, idx);
    const reportTxt = reportTextFromContainer(container);
    const openText = collectOpenText(section);

    let p = '# Урок: ' + meta.title + (meta.level ? ' · ' + meta.level : '') + '\n';
    p += '# Раздел: ' + title + '\n';
    if (reportTxt) p += '\n## Автопроверка:\n' + reportTxt + '\n';
    if (openText.length){
      p += '\n## Свободные ответы ученика:\n';
      openText.slice(0, 10).forEach((o, i) => {
        if (o.kind === 'writing') p += '- Письмо ' + (i+1) + ': "' + o.text.slice(0, 700) + '"\n';
        else if (o.kind === 'speaking') p += '- Речь ' + (i+1) + (o.target ? ' (цель: "'+o.target+'")' : '') + ': "' + o.text + '"\n';
        else p += '- Ответ ' + (i+1) + ': "' + o.text + '"\n';
      });
    }
    return p;
  }

  function buildSummaryContext(overlay){
    const meta = lessonMeta();
    const body = overlay.querySelector('.lp-body');
    let p = '# Урок: ' + meta.title + (meta.level ? ' · ' + meta.level : '') + '\n';
    p += '\n## Итог по разделам:\n';
    body.querySelectorAll('.lp-total, .lp-sec-title, .lp-good, .lp-list .lp-item').forEach(el => {
      p += el.textContent.replace(/\s+/g,' ').trim() + '\n';
    });
    const allOpen = [];
    document.querySelectorAll('section.section').forEach(s => {
      collectOpenText(s).forEach(o => allOpen.push(o));
    });
    if (allOpen.length){
      p += '\n## Свободные ответы (по всему уроку):\n';
      allOpen.slice(0, 15).forEach((o, i) => {
        if (o.kind === 'writing') p += '- Письмо ' + (i+1) + ': "' + o.text.slice(0, 500) + '"\n';
        else if (o.kind === 'speaking') p += '- Речь ' + (i+1) + (o.target ? ' (цель: "'+o.target+'")' : '') + ': "' + o.text + '"\n';
        else p += '- Ответ ' + (i+1) + ': "' + o.text + '"\n';
      });
    }
    p += '\nДай итоговый разбор и план на 2-3 дня.';
    return p;
  }

  function cacheKey(scope, secId){
    return 'lai:' + location.pathname + ':' + scope + ':' + (secId || '_');
  }
  function loadCache(key){
    try {
      const raw = localStorage.getItem(key);
      if (!raw) return null;
      const obj = JSON.parse(raw);
      if (Date.now() - obj.ts > 1000*60*60*24*7) return null;
      return obj.text;
    } catch(e) { return null; }
  }
  function saveCache(key, text){
    try { localStorage.setItem(key, JSON.stringify({ ts: Date.now(), text })); } catch(e){}
  }

  async function callAI(userContent, model){
    const body = {
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user',   content: userContent }
      ],
      model: model || 'openai',
      private: true,
      seed: Math.floor(Math.random()*1e6)
    };
    const resp = await fetch('https://text.pollinations.ai/openai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const data = await resp.json().catch(async () => ({ raw: await resp.text() }));
    const text = data?.choices?.[0]?.message?.content
              || data?.raw
              || data?.text
              || (typeof data === 'string' ? data : '');
    if (!text || !text.trim()) throw new Error('empty');
    return text.trim();
  }

  function renderText(node, raw){
    let html = raw
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/"([^"\n]{1,120})"/g, '<em>"$1"</em>');
    html = html.split(/\n\n+/).map(p => {
      if (/^#+\s/.test(p)) return '<h4>' + p.replace(/^#+\s/,'') + '</h4>';
      if (/^\s*[-•]\s/m.test(p)) {
        const items = p.split(/\n/).filter(l => /^\s*[-•]\s/.test(l)).map(l => '<li>'+l.replace(/^\s*[-•]\s/,'')+'</li>').join('');
        return '<ul>' + items + '</ul>';
      }
      if (/^\s*\d+[\.)]\s/m.test(p)) {
        const items = p.split(/\n/).filter(l => /^\s*\d+[\.)]\s/.test(l)).map(l => '<li>'+l.replace(/^\s*\d+[\.)]\s+/,'')+'</li>').join('');
        return '<ol>' + items + '</ol>';
      }
      return '<div>' + p.replace(/\n/g,'<br>') + '</div>';
    }).join('');
    node.innerHTML = html;
  }

  function ensureEmbed(parent){
    let box = parent.querySelector(':scope > .lab-ai-embed');
    if (box) return box;
    box = document.createElement('div');
    box.className = 'lab-ai-embed';
    box.innerHTML =
      '<div class="lab-ai-embed-h"><span class="dot"></span><span>ИИ-наставник · персональный разбор</span></div>'+
      '<div class="lab-ai-embed-skel">Готовлю разбор…</div>';
    parent.appendChild(box);
    return box;
  }

  async function runEmbed(parent, getCtx, key){
    const box = ensureEmbed(parent);
    const cached = loadCache(key);
    if (cached) {
      box.classList.add('done');
      const body = document.createElement('div');
      body.className = 'lab-ai-embed-body';
      renderText(body, cached);
      box.querySelector('.lab-ai-embed-skel')?.remove();
      box.appendChild(body);
      return;
    }
    if (box.__running) return;
    box.__running = true;
    const ctx = getCtx();
    let lastErr = null;
    for (const ep of [{model:'openai'},{model:'mistral'}]) {
      try {
        const text = await callAI(ctx, ep.model);
        saveCache(key, text);
        box.classList.add('done');
        const body = document.createElement('div');
        body.className = 'lab-ai-embed-body';
        renderText(body, text);
        box.querySelector('.lab-ai-embed-skel')?.remove();
        box.appendChild(body);
        box.__running = false;
        return;
      } catch(e) {
        lastErr = e;
      }
    }
    // оба упали — тёплое сообщение, без брендов
    box.classList.add('fail');
    box.querySelector('.lab-ai-embed-skel').textContent =
      'Разбор сейчас недоступен — попробуй ещё раз через минуту или сохрани ответы и попроси наставника лично.';
    box.__running = false;
  }

  function attachToReport(reportEl){
    if (!reportEl.classList.contains('show')) return;
    if (reportEl.__embedAttached) return;
    reportEl.__embedAttached = true;
    const section = reportEl.closest('section.section');
    if (!section) return;
    const key = cacheKey('sec', section.id || section.dataset.id || '');
    runEmbed(reportEl, () => buildSectionContext(section, reportEl), key);
  }

  function attachToOverlay(overlay){
    if (!overlay.classList.contains('show')) return;
    if (overlay.__embedAttached) return;
    overlay.__embedAttached = true;
    const modal = overlay.querySelector('.lp-modal');
    if (!modal) return;
    const key = cacheKey('lesson', 'all');
    runEmbed(modal, () => buildSummaryContext(overlay), key);
  }

  ready(function(){
    injectStyle();
    const mo = new MutationObserver((mutations) => {
      mutations.forEach(m => {
        if (m.type === 'attributes' && m.target.classList) {
          if (m.target.classList.contains('lp-report')) attachToReport(m.target);
          if (m.target.classList.contains('lp-overlay')) attachToOverlay(m.target);
        }
        m.addedNodes.forEach(n => {
          if (!(n instanceof HTMLElement)) return;
          if (n.classList && n.classList.contains('lp-report')) attachToReport(n);
          if (n.classList && n.classList.contains('lp-overlay')) attachToOverlay(n);
          n.querySelectorAll && n.querySelectorAll('.lp-report.show').forEach(attachToReport);
          n.querySelectorAll && n.querySelectorAll('.lp-overlay.show').forEach(attachToOverlay);
        });
      });
    });
    mo.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
    document.querySelectorAll('.lp-report.show').forEach(attachToReport);
    document.querySelectorAll('.lp-overlay.show').forEach(attachToOverlay);
  });
})();
