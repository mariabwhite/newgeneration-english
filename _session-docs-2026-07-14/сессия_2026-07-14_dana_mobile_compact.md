# Сессия · 2026-07-14 · Мобильная компактификация · Дана — Russian History Exam

**Урок:** `lingua-boost-lab/b1/dana-russia-history-exam/`
**Домен:** newgeneration-english.ru
**Ассистент:** Синтия (Claude Opus 4.7)

## Что сделано

### Итоговый набор мобильных правок (`@media(max-width:640px)`)

1. **Топбар (белый):**
   - Логотип `N LinguaBoost Lab` уменьшен, «EXAM · ЕГЭ 2026» скрыт
   - Категории Listening/Reading/Grammar/Writing/Speaking/Score → свёрнуты в **бургер ☰**
     - Тап на ☰ → выпадающий вертикальный drawer со ссылками
   - Пилюли Catalog / B1+ — маленькие

2. **Кнопки Урок / Домашка (`.ltab`):**
   - Возвращены pill-стиль (не квадратики)
   - Латиница: `📖 L` / `📚 H` (Lesson / Homework)
   - Счётчик домашки — жёлтый бабл справа

3. **Жёлтая teacher-полоса (`.lab-teacher-banner`):**
   - Осталась `position:fixed` вверху (по просьбе Марии — красивая)
   - `min-height:60px`, 2 строки, wrapped
   - Содержимое: `🎓 Teacher · путь урока` + input «+ слово в корзиночку» + `➕ ENTER`
   - Скрыто: 3-я строка «click слово в тексте → в корзинку» и кнопка «выкл»
   - **body padding-top: 150px** — hero виден с первого экрана без наложения фиксированных полос

4. **Hero и секции:**
   - `.hero-card` min-height 220→160, шрифты и padding'и ужаты
   - Все `.section-head` плотнее (цифра 26px, h2 0.85rem, ege-tag 0.55rem)
   - `.card` радиусы и padding'и меньше

5. **Speaking-bottom-dock (Вокабуляр / Результаты):**
   - Из широких пилюль `VOCABULARY` / `RESULTS` → 2 маленьких круга **V** / **R** (30px)
   - Прижаты **вплотную к правому краю** (`right:0`)
   - Вертикальный столбик, `bottom:12px`

6. **Лифт (`.lp-toc` — колонка номеров блоков 01–18 слева):**
   - Скрыт по умолчанию
   - Вместо него — своя круглая кнопка `☰` 38×38 (тёмно-синяя) фикс `left:8, bottom:96`
   - Тап → раскрывает `.lp-toc` в fixed drawer (`left:6, bottom:80, max-height:60vh`)
   - Кнопка меняет иконку на `✕`
   - Тап по номеру → прыгает + автоматически сворачивает
   - Тап вне лифта → сворачивает
   - Реализовано через inline `<script>` в самом уроке — shared JS не тронут

### Все коммиты + пуши

**Репо site-public-clean (main → newgeneration-english.ru):**
- `4bf66916` — mobile declutter (<640px + <400px)
- `17332fc2` — mobile compact-v2 (topbar + hero + pills)
- `ca26c793` — mobile burger menu (лифт → ☰) + ltab до буквы У/Д
- `fbc7fdaf` — L/H pills + teacher banner cleanup + V/R dock + collapsible лифт
- `e7888d6b` — лифт видимый ☰ + V/R прижаты
- `d6e134f5` — teacher banner unfix + z-index (эта итерация была отменена в следующей)
- `d740e1cb` — вернуть жёлтую полосу fixed + body padding-top:150 + видимая кнопка-лифт

**Репо site (mirror → mariabwhite.github.io):**
- Синхронно каждый коммит, пуш через `git push origin deploy-gh-pages:gh-pages` (ветки различаются!)

**Backups на диске:**
- `index.backup-2026-07-14.html` (v1, до всех правок сегодня)
- `index.backup-2026-07-14-v2.html` (перед compact-v2)
- `index.backup-2026-07-14-v3.html` (перед burger)
- `index.backup-2026-07-14-v4.html` (перед teacher cleanup)

## Косяки, которые разобрали по ходу

1. **Push не долетал до GitHub Pages в site.** Локальная ветка `deploy-gh-pages`, remote — `gh-pages`. Простой `git push origin deploy-gh-pages` создавал бы новую remote-ветку. Правильно: **`git push origin deploy-gh-pages:gh-pages`**. Записано в `reference_cabinet_deploy_protocol.md`.

2. **Дубль memory-файла.** Записала правило про `deploy-gh-pages:gh-pages` в новый feedback-файл, хотя оно уже было в существующем reference. Мария справедливо ругнула, дубль удалён, правило усилено в existing entry.

3. **Открепление teacher-banner на mobile.** Пыталась освободить место, убрав fixed позицию. Мария: «уродски, было намного лучше с жёлтой полосой». Возвращено fixed + body padding-top.

4. **Лифт `.lp-toc` не рендерился как я задумала.** Первая попытка через `::before` + `overflow:hidden` + `max-height` — не работала (или элемент был не виден на её девайсе). Переделано: собственный `<button>` inject'ится через inline JS, `.lp-toc` полностью скрыт по умолчанию, показывается по toggle.

## Инфраструктура сессии

- **AI Hub** запущен: порт 8765 LISTENING (PID из процесса). Скрин от Марии из Telegram упал в `AI_Chat_Hub/telegram_media/20260714-183820-file_480.jpg`
- **Chrome DevTools MCP** использован для DOM inspection (`.lab-teacher-banner`, `.speaking-bottom-dock`, `.lp-toc`)
- Пуши проверялись через `curl -s ... | grep -c 'signature'` пока GitHub Pages не пересобрал (~1–4 минуты)

## Что осталось / возможное продолжение

- Проверить как выглядит **student view** (без `?teacher=on`) — сейчас все правки заточены на присутствие teacher banner и лифта одновременно. Без teacher panel body-padding 150px даст лишний зазор.
- Аккордеон 18 секций (свернуть весь урок в details/summary) — Мария не заказывала явно, отложено
- Другие уроки в lab/b1/, lab/practice/ — если ей понравится, эти же правила можно применить как shared mobile.css
