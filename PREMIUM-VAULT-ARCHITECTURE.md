# Premium Vault architecture

Дата: 2026-06-27

## Что сломалось

Симптом старой архитектуры: новая карточка урока видна в `premium.html`, но кнопка не открывает модуль, потому что у карточки нет авторизованного URL из Vault.

Причина: HTML-карточка и физическая папка урока были добавлены, но зашифрованный `VAULT` внутри `premium.html` не содержал запись с тем же `id`.

Конкретный случай:

- карточка: `data-id="travel-talk-2"`;
- урок: `site-public-clean/lingua-boost-lab/b1/travel-talk-light-and-bright-2/index.html`;
- нужная запись Vault: `{ "id": "travel-talk-2", "url": "./b1/travel-talk-light-and-bright-2/" }`;
- исправление: Vault пересобран, версия поднята до `v18-2026-06-27-add-travel-talk-2`.

## Как работает Premium Vault

`site-public-clean/lingua-boost-lab/premium.html` содержит:

1. Видимые карточки уроков:
   - `article.card`
   - `data-id="..."`
   - изначально ссылка `href="#"`
   - визуально карточка всегда остается нормальной и читаемой.

2. Зашифрованный объект `VAULT`:
   - `salt`
   - `iv`
   - `ct`
   - `iter`.

3. JS-разблокировку:
   - пользователь вводит PIN;
   - `decryptUrls(pin)` расшифровывает Vault;
   - строится словарь `byId`;
   - для каждой карточки берется `card.dataset.id`;
   - если такой `id` есть в Vault, карточка получает реальный `href`;
   - если `id` нет, карточка остается видимой, но кнопка не открывает урок и просит ввести PIN.

## Правило

Для каждого premium-урока должны совпадать 3 вещи:

1. Физическая папка урока:

   `site-public-clean/lingua-boost-lab/<level>/<lesson-slug>/index.html`

2. Карточка в `premium.html`:

   `data-id="<lesson-id>"`

3. Запись в зашифрованном Vault:

   `{ "id": "<lesson-id>", "url": "./<level>/<lesson-slug>/" }`

Если хотя бы одно звено пропущено, урок будет "существовать", но пользователь его не откроет.

## Как добавлять новый premium-урок

Новая целевая схема уже заведена:

`premium-lessons.json -> build-premium-vault.mjs -> premium.html cards + encrypted Vault + vault-version`

Источник правды:

`site-public-clean/lingua-boost-lab/premium-lessons.json`

В manifest:

- `series` — смысловая серия/семейство урока;
- `section` — фактическая HTML-секция `premium.html` (`data-series`), куда должна попасть карточка;
- если `section` не задан, сборщик использует `series`.

Сборщик:

`scripts/build-premium-vault.mjs`

1. Создать папку урока:

   `site-public-clean/lingua-boost-lab/<level>/<lesson-slug>/index.html`

2. Проверить, что урок открывается напрямую локально.

3. Добавить урок в `premium-lessons.json`.

4. Запустить сборку. Если карточки с таким `id` еще нет, сборщик вставит ее в секцию по `section`, а если `section` не задан — по `series`.

5. Запустить пересборку:

   ```powershell
   $env:PREMIUM_PIN='...'
   node scripts/build-premium-vault.mjs
   Remove-Item Env:\PREMIUM_PIN
   ```

6. Проверить Vault без перезаписи:

   ```powershell
   $env:PREMIUM_PIN='...'
   node scripts/build-premium-vault.mjs --check
   Remove-Item Env:\PREMIUM_PIN
   ```

7. Проверить ссылки уроков:

   ```powershell
   node scripts/audit-premium-links.mjs
   ```

   И, если нужен live-аудит домена:

   ```powershell
   node scripts/audit-premium-links.mjs --live
   ```

8. Проверить `premium.html` в браузере:

   - ввести PIN заново;
   - если браузер держал старый кэш, открыть `premium.html#lock`, затем снова ввести PIN;
   - новый урок должен получить активную кнопку с реальным URL.

9. Закоммитить и запушить `site-public-clean`.

## Почему нужен `vault-version`

В `premium.html` есть:

```html
<meta name="vault-version" content="...">
```

Браузер хранит расшифрованный список в `localStorage`:

- `nge-vault-cache`
- `nge-vault-cache-v`
- `nge-vault-pin`

Если `vault-version` не поднять, браузер может использовать старый список и новый урок не получит реальный URL даже после деплоя. Поэтому при каждом изменении Vault нужно менять `vault-version`.

## Важное UX-правило

Карточки premium-уроков никогда не должны быть визуально скрыты, размыты или выключены.

Правильная модель:

- каталог всегда виден;
- картинки, названия и skills всегда читаются;
- без PIN кнопка не открывает урок, а просит ввести код;
- после PIN кнопки получают реальные URL;
- после сброса доступа реальные URL удаляются, но карточки остаются видимыми.

## Guard на прямые ссылки уроков

Важно: GitHub Pages отдает HTML-файлы публично, поэтому это не серверная защита контента. Это клиентский guard от обычного обхода через прямую ссылку.

Каждый premium-урок должен подключать:

```html
<script src="/lingua-boost-lab/assets/premium-lesson-guard.js"></script>
```

Guard проверяет `localStorage.nge-vault-cache`. Если текущий URL урока не найден в расшифрованном списке разрешенных уроков, страница перенаправляет пользователя на:

`/lingua-boost-lab/premium.html?next=<lesson-url>#login`

После успешного PIN `premium.html` сохраняет доступ и возвращает пользователя в исходный урок из `next`.

Проверка guard:

```powershell
node scripts/apply-premium-guard.mjs --check
```

Применение guard ко всем published premium-урокам:

```powershell
node scripts/apply-premium-guard.mjs
```

Для настоящей защиты от технического обхода нужен backend/Auth/Cloudflare Access или другой серверный слой, который решает, отдавать HTML урока или нет.

## Быстрая диагностика

Если урок не открывается:

1. Есть ли физическая папка урока?
2. Есть ли карточка в `premium.html`?
3. Совпадает ли `data-id` с `id` в Vault?
4. Есть ли URL в Vault?
5. Поднята ли `vault-version`?
6. Очищен ли старый кэш через `#lock`?
7. Запушен ли обновленный `premium.html`?
8. Проходит ли `node scripts/audit-premium-links.mjs --live`?
9. Проходит ли `node scripts/apply-premium-guard.mjs --check`?

## Текущее исправление

Исправлено:

- `site-public-clean/lingua-boost-lab/premium.html`
- добавлена запись Vault для `travel-talk-2`;
- добавлен `premium-lessons.json`;
- добавлен `scripts/build-premium-vault.mjs`;
- добавлен `scripts/audit-premium-links.mjs`;
- добавлен `scripts/apply-premium-guard.mjs`;
- добавлен `lingua-boost-lab/assets/premium-lesson-guard.js`;
- Vault пересобран из manifest;
- версия Vault: `v20260627-24-premium-lessons`;
- проверка: `premium check OK: 24 published lessons, 24 cards`;
- проверка ссылок: `premium link audit OK: 24 lessons, 0 warnings, live checked`;
- проверка guard: `premium guard check OK: 24 lessons`;
- добавлена полная делогинизация: кнопка `Сбросить доступ` и `premium.html#lock` чистят `nge-vault-cache`, `nge-vault-cache-v`, `nge-vault-pin` и удаляют реальные URL с кнопок, не скрывая карточки.
