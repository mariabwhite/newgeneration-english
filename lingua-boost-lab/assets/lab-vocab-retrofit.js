/**
 * lab-vocab-retrofit.js · v1 · 2026-07-07
 * Проходит по DOM урока и добавляет CSS-классы, которые ждёт lab-vocab-builder.js:
 *   .vocab-card, .word, .meaning, .example
 * Работает поверх ЛЮБОЙ структуры vocab-карточек — только ДОБАВЛЯЕТ классы,
 * ничего не переписывает. Полностью idempotent: если классы уже есть, no-op.
 *
 * После добавления классов lab-vocab-builder.js подхватывает карточки
 * и рисует жёлтую полосу «+ добавить слово» под ?teacher=on.
 *
 * Подключение: <script src=".../lab-vocab-retrofit.js?v=1" defer></script>
 * ДОЛЖЕН стоять ПЕРЕД lab-vocab-builder.js в footer scripts.
 */
(function () {
  if (window.__labVocabRetrofitLoaded) return;
  window.__labVocabRetrofitLoaded = true;

  function retrofit() {
    // 1. Common flip-card pattern (Dana, Timofey, Stage-vs-Screen...)
    document.querySelectorAll('.flip-card:not(.vocab-card)').forEach(function (card) {
      var front = card.querySelector('.flip-front');
      var back = card.querySelector('.flip-back');
      if (!front || !back) return;
      var w = front.querySelector('.w, .word');
      var m = back.querySelector('.def, .meaning, .ru');
      // Считаем это vocab-карточкой только если внутри есть слово + перевод
      if (!w || !m) return;
      card.classList.add('vocab-card');
      w.classList.add('word');
      m.classList.add('meaning');
      var ex = back.querySelector('.ex, .example');
      if (ex) ex.classList.add('example');
    });

    // 2. Voyager-style: .voc-item / .voyager-vocab-item
    document.querySelectorAll('.voc-item:not(.vocab-card), .voyager-vocab-item:not(.vocab-card)').forEach(function (card) {
      var w = card.querySelector('.voc-word, .word, strong, b');
      var m = card.querySelector('.voc-def, .voc-ru, .meaning, .ru, em, i');
      if (!w || !m) return;
      card.classList.add('vocab-card');
      w.classList.add('word');
      m.classList.add('meaning');
    });

    // 3. Julia/kids · picture-card style with data-en / data-ru attributes
    document.querySelectorAll('[data-en][data-ru]:not(.vocab-card)').forEach(function (card) {
      // Пропускаем маленькие inline-элементы — только card-подобные
      if (!card.matches('div, section, article, li, figure, span.picture-card')) return;
      if (!(card.offsetWidth > 80 || card.dataset.forceVocab === '1')) return;
      // Не портим селекторы уроков-квизов — только явные vocab-контексты
      var container = card.closest('[data-vocab], .vocab-list, .vocab-grid, .vocab-box, .vocab-flow, #vocab, #vocab-grid, #vocab-box');
      if (!container) return;
      card.classList.add('vocab-card');
      var en = card.dataset.en;
      var ru = card.dataset.ru;
      // Не создаём новых DOM — только помечаем классы у существующих
      var wordEl = card.querySelector('.en, .word, [data-en-text]');
      var meanEl = card.querySelector('.ru, .meaning, [data-ru-text]');
      if (wordEl) wordEl.classList.add('word');
      if (meanEl) meanEl.classList.add('meaning');
    });

    // 4. Timofey / Interview generic pattern .vocab-item
    document.querySelectorAll('.vocab-item:not(.vocab-card)').forEach(function (card) {
      card.classList.add('vocab-card');
      var w = card.querySelector('.vocab-item-word, .word, strong');
      var m = card.querySelector('.vocab-item-ru, .vocab-item-meaning, .meaning, em, i');
      if (w) w.classList.add('word');
      if (m) m.classList.add('meaning');
    });
  }

  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  ready(function () {
    retrofit();
    // Урок может создавать карточки динамически (Dana, Voyager) — ждём + повторяем
    setTimeout(retrofit, 150);
    setTimeout(retrofit, 600);
    setTimeout(retrofit, 1500);

    // MutationObserver — на случай ленивой генерации после кликов
    try {
      var mo = new MutationObserver(function () {
        clearTimeout(window.__labVocabRetroDebounce);
        window.__labVocabRetroDebounce = setTimeout(retrofit, 250);
      });
      mo.observe(document.body, { childList: true, subtree: true });
      // Не наблюдаем вечно — иначе лишний CPU
      setTimeout(function () { mo.disconnect(); }, 15000);
    } catch (_) { /* ignore */ }
  });
})();
