# LinguaBoost Lab — Архитектура урока (canonical)

Один файл, где живут все правила и все ссылки на кирпичи. Открывать перед каждым новым уроком.

## 1. Один урок = одна HTML-страница

```
lingua-boost-lab/<level>/<slug>/index.html   ← для полноценных уроков со своими ассетами
lingua-boost-lab/<level>/<slug>.html         ← для одностраничных уроков без ассетов
```

Уровни: `pre-a1`, `a1`, `a2`, `b1`, `b2-plus`, `c1`, `practice`, `trial-academic-abroad`.

## 2. Обязательные скрипты в `<head>` / перед `</body>`

Порядок важен: сначала supabase-realtime (для sync/firehose), потом lab-* в порядке ниже.

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>

<script src="../assets/lab-manifest.js?v=..." defer></script>
<script src="../assets/lab-pilot.js?v=..." defer></script>
<script src="../assets/lab-mic-wpm.js?v=..." defer></script>
<script src="../assets/lab-ai-feedback.js?v=..." defer></script>
<script src="../assets/lab-sync.js?v=16" defer></script>
<script src="../assets/lab-tabs.js?v=12" defer></script>
<script src="../assets/lab-homework.js?v=38" defer></script>
<script src="../assets/lab-vocab-builder.js?v=48" defer></script>
<script src="../assets/lab-coach-persist.js?v=1" defer></script>
<script src="../assets/lab-speech-tester.js?v=11" defer></script>
<script src="../assets/lab-quick-speak.js?v=4" defer></script>
```

Пути в `<level>/<slug>/index.html` — `../../assets/…`; в `<level>/<slug>.html` — `../assets/…`.
Cache-buster `?v=N` **обязателен**. Когда меняется shared asset — bump везде.

Скрипты, что делают что:

| script                       | зачем                                                                              |
| ---------------------------- | ---------------------------------------------------------------------------------- |
| `lab-manifest.js`            | манифест урока, регистрация в total.                                              |
| `lab-pilot.js`               | UI пилота: топбар, темы, hero, TOC, кнопка «в домашку».                            |
| `lab-mic-wpm.js`             | speaking WPM/mic-drill.                                                            |
| `lab-ai-feedback.js`         | AI-фидбек по ответам в домашке.                                                    |
| `lab-sync.js`                | teacher/observer mirror через Supabase Realtime.                                   |
| `lab-tabs.js`                | вкладки «Урок / Моя домашка» под topbar.                                          |
| `lab-homework.js`            | плюсы `+` рядом с упражнениями, клон в raw-block, доставка в `.homework/`.        |
| `lab-vocab-builder.js`       | секция «📖 Vocabulary», подсветка слов, teacher `+ в словарь`, click-to-vocab.    |
| `lab-coach-persist.js`       | сохранение прогресса ученика.                                                      |
| `lab-speech-tester.js`       | speaking-задания с распознаванием.                                                 |
| `lab-quick-speak.js`         | inline «say it» на строках.                                                        |

## 3. Vocabulary — как это работает

Урок объявляет:

```html
<script>
  window.LAB_VOCAB = [
    { word: 'environment', ipa: '/ɪnˈvaɪrənmənt/', ru: 'окружающая среда',
      example: 'We must protect the environment.', audio: 'assets/audio/env.mp3' },
    { word: 'pollution', ipa: '/pəˈluːʃən/', ru: 'загрязнение' },
    ...
  ];
</script>
```

`lab-vocab-builder.js` v48+ автоматически:
1. Строит секцию `📖 Vocabulary` (flip-cards) в конце главной колонки.
2. Подсвечивает каждое слово из `LAB_VOCAB` в тексте `.card, p, li`.
3. Кнопка `🔊` — если задан `audio`, играет файл; иначе TTS через `speechSynthesis`.
4. Кнопка `➕` — кладёт слово в домашку через `lab-homework`.
5. Teacher `+ в словарь` — выделяю слово в тексте → плавающая кнопка → mini-modal (word/IPA/ru/example) → добавляется в localStorage `extras` и в vocab section.
6. **Click-to-vocab (v48)** — учитель, ученик или observer кликают ЛКМ на слово в тексте `.card / .reading / .story / .passage / .lab-bridge` → слово добавляется в vocab section. Guards исключают клики в `.homework`, `.lab-hw-*`, `.lab-vocab-section` и по интерактивам упражнений (mc-opt / tf-btn / choice / bank-word / word-chip / drag-item / drop-* / match-* / wo-pill / ord-*).

## 4. Homework — как это работает

`lab-homework.js` v38+:

- Добавляет `+` кнопки к каждому упражнению по селекторам архетипов (MCQ / TF / gap / match / ord / vocab / prompt / builder / card).
- При клике `+` клонирует «хост» упражнения через `cleanRawClone(node)`:
  - убирает `lab-hw-*`, `script`, `style`, `link[rel=stylesheet]`, `details.teacher`, `.answer-key`, `.reveal`, `.solution`, `.correct-answer`, `.listen-script`, `.transcript`;
  - подчищает inline `background`/`color` в `[style]` (родные цвета урока прячутся, палитра `.homework` берёт своё);
  - `src`/`href` относительные → абсолютные.
- Каждому клону присваивается уникальный `section_id = ${sectionId}:${kind}:${nodeFingerprint(host)}`. Это фиксит julia-vampire, где 10 vocab-карточек имели одинаковый question и взаимно toggle-удалялись.
- Item попадает в `localStorage['lab-hw:' + lessonPath]` как `{ kind: 'raw-block', question, html, section_id, ts }`. Для vocab-карточек `kind: 'vocab'` с полями `en/ipa/ru/ex`.
- Прямая ссылка на домашку: `.homework/?lesson=<encoded lessonPath>`.

## 5. `.homework/index.html` — как рендерит raw

`.homework` — независимая страница, живёт в `lingua-boost-lab/.homework/index.html`. Топбар, вкладка «Моя домашка» рядом с уроком, палитра синхронизирована через `lab-theme-sync.js`.

Rendering item:

1. `head` — номер + kind-chip + question.
2. `body` — для `raw-block` = `<div class="raw">${item.html}</div>`; для `vocab` = собственная vocab-card.
3. `answer` — textarea для ученика (учитель видит readonly или empty).
4. Крест `×` удаления справа сверху.
5. `hydrateRawAnswers(article)` — сбрасывает наследованные из HTML урока классы `correct / wrong / selected / is-correct / filled / used / revealed / [data-state]` и накатывает сохранённое состояние ученика. Это фиксит эффект «Voyager всё зелёное на входе».

CSS-правила для `.raw` (только внутри `.homework`, уроки не трогаются):

- `.raw` — border, radius, padding, `max-height: min(720px, 60vh); overflow-y: auto` на desktop; mobile — без cap.
- `.raw img / picture img / figure img / [class*=img] img` — `max-height: 380px !important; object-fit: contain !important`.
- Structural flatten для containers: `section / .section / .card / .story-block / .round-card / .game-card / .info-card / .error-card / .prompt-card / .now-item / .tile / .output-box / .match-wrap` — transparent bg, no shadow, no border, no padding.
- UI-мусор из уроков (nav / header / footer / hero / lab-hero / hero-banner / lesson-hero / topbar / snake-overlay / lb-overlay / img-story-overlay / tracker / progress-bar) — `display: none !important`.
- Interactive классы `.raw button / .mc-opt / .tf-btn / .btn-tf / .choice / .choice-btn / .bank-word / .word-chip / .drop-slot / .drop-gap / .drop-zone / .match-place / .match-drop / .match-slot / .wo-pill / .ord-card / .ord-chip / .predict-btn` — визуально показываются как «пилюли», реагируют на клик через общий handler.

Общий JS-handler в `.homework` понимает:

- MCQ / TF / выбор одного ответа — рассматривается по ближайшей группе `rawChoiceGroupSelector`. Правильный ответ ищется по `data-correct / data-answer / data-expected / data-ans / data-a / value / text`.
- Bank → drop-gap / drop-slot / drop-zone — pick word, place, verify, save.
- Match — pick left → click right.
- Ordering / word-order — pill в bank ↔ slot, check по `data-words / data-answer`.
- Flip-cards — `.flipped` toggle.
- TTS кнопки с `data-say` / `.play` — озвучиваются через `speechSynthesis` (`handleRawPlayButton`).

## 6. Teacher / observer / ученик — режимы

URL-флаги:

| режим     | URL                                | доступ                                                                   |
| --------- | ---------------------------------- | ------------------------------------------------------------------------ |
| ученик    | без флагов                         | UI урока + подсветка + click-to-vocab + `+` в домашку.                    |
| учитель   | `?teacher=on` (canonical)          | + teacher-баннер, teacher-mirror, `+ в словарь` через selection.          |
| observer  | `?observe=<roomId>`                | смотрит зеркало ученика, click-to-vocab транслируется в firehose ученику. |

Sticky флаг учителя: `localStorage['lab-teacher-mode'] = 'on'`.

Проверять для каждого изменения teacher UI:
- `?teacher=on`, `?teacher=1`, `?role=teacher`, `?observe=<room>&role=teacher`, `?v=v7&theme=light-lab&lang=ru&teacher=on`.

## 7. Realtime backbone (Supabase)

- URL: `https://iqzlphbvmfgoygnozbya.supabase.co`.
- Anon key: `sb_publishable_hYhBk3xS90uouUFd_DZWUw_sOv-6JGO`.
- Каналы:
  - `lab-firehose-v1` — vocab push / vocab remove (observer → ученик).
  - `student-<slug>` — teacher-mirror ответов, live typing.

## 8. Premium урок

- URL остаётся публичным, но контент прячется за AES-GCM vault.
- PIN хранится в `localStorage['lab-premium-pin']` после ввода.
- Vault repack — Node-скрипт с текущим PIN. Ключи из git log site-public-clean.
- **Правило:** PIN никогда не зашивать в публичные ссылки/кнопки. Открывается только вводом PIN руками.

## 9. Cache-buster протокол

Когда меняешь shared asset — bumps во ВСЕХ уроках, которые его подключают. Bulk-replace через PowerShell:

```powershell
Get-ChildItem -Recurse -File -Filter '*.html' | ForEach-Object {
  $c = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
  if ($c -match 'lab-<asset>\.js\?v=<old>') {
    Set-Content -LiteralPath $_.FullName -Value ($c -replace 'lab-<asset>\.js\?v=<old>', 'lab-<asset>.js?v=<new>') -Encoding UTF8 -NoNewline
  }
}
```

Проверять что diff трогает только строку `<script src="..." >` — а не содержимое урока.

## 10. Мандат «уроки не трогать»

Правки только в `assets/*.js`, `.homework/index.html`, `assets/*.css` (если появится), `ARCHITECTURE.md`. Уроки — источник правды. Bump `?v=` в HTML уроков — единственное разрешённое исключение.

## 11. Аудитный тулинг

- `_scan_reports/sweep_homework_audit.mjs` — прогон по всем 61 урокам: enumerates `+`, кликает, проверяет localStorage, открывает `.homework`, снимает признаки `oversized / imgTooBig / greenInitial / emptyRaw / audioTts`.
- `_scan_reports/batch_smoke.mjs` — batch на 10 уроков разного архетипа: скриншоты lesson + homework, click-to-vocab check.
- `_scan_reports/click_vocab_test.mjs` — real mouse click проверка click-to-vocab.
- Отчёты — `_scan_reports/sweep_summary.json`, `_scan_reports/batch_smoke.json`, скрины — `_scan_reports/screenshots/`.

Запускать перед каждым push, если менялись shared assets или `.homework`.

## 12. Как рождается новый урок — короткий чек-лист

1. Скопировать структуру ближайшего эталона того же архетипа.
2. `<title>`, `<h1>`, `hero-card` — свои.
3. `window.LAB_VOCAB` — минимум 10-16 слов, всё в объектах `{word, ipa, ru, example, audio?}`.
4. Упражнения — из канонических классов (см. секцию 5). НЕ придумывать новые имена без нужды.
5. Speaking prompts — минимум 8-10 предложений на задание (см. `feedback_speaking_task_length.md`).
6. MCQ правильные ответы — вперемежку между заданиями. Не подряд A/A/A/A.
7. Все обязательные `<script src="../assets/lab-*.js?v=...">` — с актуальными версиями.
8. Прогнать `sweep_homework_audit.mjs`, посмотреть свой урок в отчёте: `addButtons` > 0, `stored == added`, `greenInitial: 0`, `oversized: 0`.
9. Открыть `.homework/?lesson=/lingua-boost-lab/<path>/` глазами, кликнуть 5-6 добавлений, проверить каждое.
10. Push, дождаться Pages deploy, live-verify.

---

*Последнее обновление: 2026-07-08 (Синтия).*
