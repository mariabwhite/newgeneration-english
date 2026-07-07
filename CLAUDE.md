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
