# Проект: Сайт New Generation

## Суть
Главный публичный сайт, LinguaBoost Lab, кабинет, уроки и визуальная система New Generation English.

## Рабочая зона кода на 2026-06-28
Корень проекта:
`C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\01_Сайт New Generation — сайт, Lab, кабинет`

Три каталога внутри корня:
- `nge-cabinet/` — источник правды для кабинета: `data.js`, `cabinet.js`, 5 HTML UI (`index.html`, `login.html`, `parent.html`, `student.html`, `teacher.html`), Supabase-клиент и кабинетные модули.
- `site-public-clean/` — production-сайт и production-зеркало кабинета на основном домене, включая `cabinet/vault/*.enc` и `cabinet/vault/index.json`.
- `site/` — legacy gh-pages. Не трогать без отдельного согласования.

## Кабинетный pipeline
1. Править ученика только в `nge-cabinet/data.js`.
2. После правки bump `data.js?v=...` во всех 5 HTML кабинета: `index.html`, `login.html`, `parent.html`, `student.html`, `teacher.html`.
3. Из корня проекта запускать `node scripts/gen-vault.js`; скрипт читает `nge-cabinet/data.js` и пересобирает encrypted vault в `site-public-clean/cabinet/vault/`.
4. Коммитить и push'ить оба репо: сначала `nge-cabinet`, затем `site-public-clean` с vault rebuild.

Последняя подтверждённая кабинетная серия 2026-06-28:
- `nge-cabinet` `49aba1d` — Денис: урок 28.06 completed, домашка «весь конец урока», bump версии кабинета.
- `site-public-clean` `38b9a7c` — vault rebuild после Дениса: пересобран `cabinet/vault/index.json` и encrypted blobs.
- Перед этим в `nge-cabinet`: `e6a5c2d` и `a2c2c8c` по Даниэлле — новый интенсив 10 × 2500 = 25 000 ₽, показ всех 10 уроков через `summer_plan_note`, темы Russia/ЕГЭ; `88d04c4` и `df1160b` по Тимофею Workbook 02.

## Где лежат материалы в Центре управления
- `C:\Users\Whitenois\Desktop\Новый центр управления\02_Work\New Gen`
- `...\HTML-материалы и интерактивы\06 - все версии сайтов` — архив версий и Reels-материал про создание сайта.
- `...\Визуальные материалы - комиксы, картинки, видео` — визуалы для сайта и контента.

## Кто отвечает
- Claude: код сайта, Lab, кабинет, методика, HTML/CSS/JS.
- Codex: README, архивы, карты, preview, Git push по handoff.
- Маша: что считать рабочим, что публиковать, что оставить как память/контент.

## Правило безопасности
Пока Claude кодит, Codex не правит рабочие файлы сайта. Здесь только карта проекта и ссылки на склады.
