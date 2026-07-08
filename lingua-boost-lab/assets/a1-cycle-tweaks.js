/* a1-cycle-tweaks.js v1 · 2026-07-09
   Локальные доводки для A1-цикла (a1-01…a1-08).

   1. Speech Coach (.lab-coach-section) — переносит кнопку «📚 всю секцию
      в домашку» из начала блока в конец. Визуально она встаёт между
      Speech Coach и следующей секцией (Final Task).

   2. Lesson total (#lab-total-block, инжектится lab-total.js) —
      расширяет до общей ширины .block и даёт ту же карточную оболочку
      (border, background, radius, padding), чтобы совпадал по ширине
      с остальными блоками урока.
*/
(function(){
  if (window.__a1CycleTweaks) return;
  window.__a1CycleTweaks = true;

  function injectStyle(){
    if (document.getElementById('a1-cycle-tweaks-style')) return;
    var s = document.createElement('style');
    s.id = 'a1-cycle-tweaks-style';
    s.textContent =
      // Lesson total block: расширяем и оформляем как обычный .block
      '#lab-total-block{max-width:1240px !important;width:calc(100% - 32px) !important;'+
        'margin:32px auto !important;padding:28px clamp(20px,3vw,32px) !important;'+
        'border:1px solid var(--line,rgba(255,255,255,.14)) !important;'+
        'background:color-mix(in srgb, var(--surface,#fff) 94%, transparent) !important;'+
        'border-radius:20px !important;box-sizing:border-box !important;'+
        'box-shadow:0 18px 46px color-mix(in srgb,var(--brand,#7c3aed) 8%,transparent) !important}'+
      '#lab-total-block > div:first-child{background:transparent !important;border:0 !important;padding:0 0 12px !important}'+
      '#lab-total-block > div:last-child{gap:16px !important}'+
      '#lab-total-block > div:last-child > div{border-radius:14px !important;padding:16px 20px !important}'+
      '@media(max-width:600px){#lab-total-block{padding:20px 16px !important;width:calc(100% - 20px) !important}'+
        '#lab-total-block > div:last-child{grid-template-columns:1fr !important}}';
    document.head.appendChild(s);
  }

  // Speech Coach: переносим кнопку «📚 всю секцию в домашку» в конец
  function relocateCoachHwBtn(){
    document.querySelectorAll('.lab-coach-section').forEach(function(sec){
      if (sec.__a1HwRelocated) return;
      var btn = sec.querySelector(':scope > .lab-hw-section-btn');
      if (!btn) return;
      // Ставим в конец секции, чтобы визуально между Speech Coach и Final Task
      btn.style.cssText = 'display:flex;margin:18px auto 4px;align-self:center';
      sec.appendChild(btn);
      sec.__a1HwRelocated = true;
    });
  }

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  ready(function(){
    injectStyle();
    // Пробуем сразу
    relocateCoachHwBtn();
    // lab-homework.js добавляет кнопку через MutationObserver — ждём
    var mo = new MutationObserver(function(){ relocateCoachHwBtn(); });
    mo.observe(document.body, { childList:true, subtree:true });
    // Safety: несколько отсроченных проходов на случай медленного inject Speech Coach
    setTimeout(relocateCoachHwBtn, 600);
    setTimeout(relocateCoachHwBtn, 1800);
    setTimeout(relocateCoachHwBtn, 3500);
  });
})();
