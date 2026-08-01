# Claude Code Memory

## 2026-07-02: Teacher vocab bar regression in Lab lessons

Сегодня после правок архитектуры уроков появилась регрессия: домашка стала доступна, но желтая teacher-строка добавления слов пропала в части реальных teacher-сценариев.

Причина была не одна:

- `lab-sync.js` и отдельные уроки по-разному понимали teacher mode.
- Часть кода включала teacher UI только через `?teacher=on` / `?teacher=1`.
- Кабинет и live-зеркало могут открывать урок как `?role=teacher` или `?observe=<room>&role=teacher`.
- Проверка только на A1-уроке была недостаточной: реальный кейс был Voyager `b2-plus/voyager-l1-time-travel`.
- Вручную открытая ссылка без teacher-флага, например `?v=v7&theme=light-lab&lang=ru`, не должна показывать teacher-панель. Для teacher-доступа нужен `teacher=on` или эквивалентный teacher-флаг.

Правило на будущее:

- При любых изменениях teacher UI, vocab builder, homework, sync/observe логики проверять минимум:
  - `?teacher=on`
  - `?teacher=1`
  - `?role=teacher`
  - `?observe=<room>&role=teacher`
  - уже существующие query-параметры урока, например `?v=v7&theme=light-lab&lang=ru&teacher=on`
- Проверять не только A1-уроки, но и premium/Voyager-уроки с PIN guard.
- Если меняется `lab-sync.js`, обязательно bump cache-buster во всех уроках: `lab-sync.js?v=<next>`.
- Не считать raw GitHub достаточной проверкой: отдельно проверить live HTML и live screenshot/DOM.
- Для teacher-ссылок руками самый надежный флаг: `teacher=on`.

Связанные фиксы:

- `lab-sync.js`: teacher banner должен работать и в `observe + role=teacher`.
- `b2-plus/voyager-l1-time-travel/index.html`: локальный teacher-mode должен понимать `teacher=on`, `teacher=1`, `role=teacher`, `#teacher`.

## 2026-08-01: Lab fragility, homework smoke, BeeSeeker analogy

Контекст сессии: Мария сравнивала свой LinguaBoost Lab с BeeSeeker/Jeffrey, чтобы понять, почему сайт Jeffrey выглядит более надежным, а Lab ощущается хрупким.

Ключевой вывод:

- BeeSeeker по сути web app с понятной доменной моделью: производители, профили, продукты, карта/каталог, заявки/контакты, админка.
- LinguaBoost Lab сейчас богаче по механикам, но хрупче технически: уроки являются HTML/DOM-страницами, а shared-механики угадывают структуру по классам, `data-*`, DOM-порядку и inline JS.
- Цель ремонта Lab: не “перерисовать уроки”, а постепенно перевести механику на явные объекты: Lesson Data -> Homework Object -> Student Answer -> Teacher Review -> Supabase Storage.

Файлы-источники по этой теме:

- `lingua-boost-lab/_internal/stability-audit/CABINET_AND_LAB_FRAGILITY_AUDIT.md`
- `lingua-boost-lab/_internal/lesson-data-v2/LESSON_DATA_CONTRACT_V2.md`
- `C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\06_Переезд + отдых\BeeSeeker\00_BeeSeeker_полное_досье.md`

Что было сделано в Lab:

- `assets/lab-sync.js`: добавлены `findContextSection(el)` и `getSectionId(sec)`, чтобы teacher/live sync находил `section_id` не только в `section.section`, но и в `.block`, `.canon-l-section`, `.lesson-section`, `section[id^="block-"]`, `section[data-section]`, `section[data-section-id]`. Важно: не возвращать широкий bare `[id^="block-"]`, только `section[id^="block-"]`.
- `.homework/index.html`: добавлен `scheduleRender()` с `requestAnimationFrame`, чтобы быстрые async `render()` склеивались в один кадр.
- После ручного smoke Мария сказала, что `.homework` “лаганула”. Это не считать green. Найдена вероятная причина: авто-`prompt('Как тебя зовут?')` через 400 мс после открытия `.homework`. Минимальный фикс: не спрашивать имя при загрузке, спрашивать только при `submitHomework()`.

Текущие риски:

- `scheduleRender()` уменьшает render storm, но не лечит полностью тяжелый `render()` и reset/hydrate race.
- `.homework` нужно повторно проверить после отключения авто-prompt.
- `lab-sync.js` cache-buster не должен оставаться частичным: перед deploy сверять живые HTML, а не backup-файлы.
- В рабочем дереве на момент обсуждения были несвязанные изменения по Fedor audio и `nge-cabinet`; не пушить их вместе с Lab-fix случайно.

Рабочий принцип:

- Маленькие P0-правки допустимы только после syntax check и smoke.
- Не трогать уроки массово без inventory.
- Для следующего архитектурного шага использовать `LESSON_DATA_CONTRACT_V2.md`, а не продолжать расширять OR-цепи и DOM-клоны.
