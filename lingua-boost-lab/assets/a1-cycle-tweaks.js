/* a1-cycle-tweaks.js v3 · 2026-07-09
   Локальные доводки для A1-цикла (a1-01…a1-08).

   1. Speech Coach (.lab-coach-section) — переставляет секцию из позиции
      после <nav.lesson-foot> в позицию ПЕРЕД <nav.lesson-foot>.
      Мария 2026-07-09: «Speech Coach не должен быть последним, он должен
      стоять перед Previous / Каталог Lab / Следующий».

   2. Кнопка «📚 всю секцию в домашку» на Speech Coach — гарантирует что
      всегда стоит в КОНЦЕ .lab-coach-section (визуально между Speech
      Coach и следующим блоком). Без флага — MO триггерится каждый раз,
      appendChild noop если уже последний ребёнок.

   3. Lesson total (#lab-total-block) — расширяет до общей ширины .block
      (max-width 1280) + карточная оболочка.
*/
(function(){
  if (window.__a1CycleTweaks) return;
  window.__a1CycleTweaks = true;

  function injectStyle(){
    if (document.getElementById('a1-cycle-tweaks-style')) return;
    var s = document.createElement('style');
    s.id = 'a1-cycle-tweaks-style';
    s.textContent =
      '#lab-total-block{max-width:1280px !important;width:calc(100% - 32px) !important;'+
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

  // Speech Coach: (a) в конец должна кнопка «📚 всю секцию», (b) сама секция
  // должна стоять перед <nav.lesson-foot>, а не после.
  function pinCoach(){
    var foot = document.querySelector('nav.lesson-foot, .lesson-foot');
    document.querySelectorAll('.lab-coach-section').forEach(function(sec){
      // (a) кнопка в конце секции
      var btn = sec.querySelector(':scope > .lab-hw-section-btn');
      if (btn && sec.lastElementChild !== btn) {
        btn.style.cssText = 'display:flex;margin:18px auto 4px;align-self:center';
        sec.appendChild(btn);
      }
      // (b) перенести секцию перед lesson-foot
      if (foot && sec.parentNode) {
        // Уже перед foot внутри того же parent?
        if (foot.parentNode === sec.parentNode) {
          var siblings = Array.from(foot.parentNode.children);
          if (siblings.indexOf(sec) > siblings.indexOf(foot)) {
            foot.parentNode.insertBefore(sec, foot);
          }
        } else {
          // Разные родители → перенести в родитель foot
          foot.parentNode.insertBefore(sec, foot);
        }
      }
    });
  }

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  ready(function(){
    injectStyle();
    pinCoach();
    var mo = new MutationObserver(function(){ pinCoach(); });
    mo.observe(document.body, { childList:true, subtree:true });
    // Safety-tail на медленный async speech-tester (fetch criteria)
    [400, 1500, 3500, 7000, 12000].forEach(function(ms){ setTimeout(pinCoach, ms); });
  });
})();
