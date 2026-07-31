# Prompt for Claude: Premium Vault automation and logout architecture

Задача: исправить архитектуру Premium Vault в LinguaBoost Lab так, чтобы добавление нового урока больше не ломало доступ.

## Контекст

Сейчас premium-урок может быть физически создан и даже показан карточкой в `premium.html`, но оставаться размытым/locked, потому что его `id` не попал в зашифрованный Vault.

Пример поломки:

- карточка есть: `data-id="travel-talk-2"`;
- урок есть: `site-public-clean/lingua-boost-lab/b1/travel-talk-light-and-bright-2/index.html`;
- но в Vault не было записи `{ id: "travel-talk-2", url: "./b1/travel-talk-light-and-bright-2/" }`;
- в результате PIN вводится, часть уроков открывается, новый урок не открывается.

Так больше быть не должно.

## Целевое поведение

1. Добавляется новый premium-урок.
2. Урок автоматически попадает в Premium Vault.
3. Я вижу урок в библиотеке.
4. Я ввожу PIN.
5. Все доступные по Vault уроки раскрываются.
6. Если PIN/пароль сброшен, происходит полная делогинизация:
   - уроки снова закрыты;
   - локальный кэш доступа очищен;
   - сохраненный PIN удален;
   - повторный доступ требует нового ввода PIN.

## Главное требование

Нужен один источник правды для premium-уроков.

Запрещено поддерживать вручную несколько несинхронных мест:

- HTML-карточку отдельно;
- папку урока отдельно;
- Vault-запись отдельно;
- счетчик/каталог отдельно.

Добавление урока должно происходить через один реестр/манифест, а все производные файлы должны собираться автоматически.

## Предлагаемая архитектура

Создать явный manifest premium-уроков, например:

`site-public-clean/lingua-boost-lab/premium-lessons.json`

Формат:

```json
[
  {
    "id": "travel-talk-2",
    "title": "Travel Talk · Light & Bright 2",
    "series": "travel-light",
    "level": "B1",
    "number": "02",
    "url": "./b1/travel-talk-light-and-bright-2/",
    "cover": "./b1/travel-talk-light-and-bright-2/assets/img/hero.jpg",
    "skills": ["Airports", "Hotel check-in", "Lost luggage", "Emergencies"],
    "premium": true,
    "published": true
  }
]
```

После этого сборка должна:

1. Прочитать manifest.
2. Проверить, что каждый `url` ведет к существующему `index.html`.
3. Сгенерировать карточки или проверить, что карточки в `premium.html` совпадают с manifest.
4. Сгенерировать Vault из всех `published: true` premium-уроков.
5. Поднять `vault-version`.
6. Выдать ошибку сборки, если:
   - есть карточка без Vault-записи;
   - есть Vault-запись без физического урока;
   - есть дубли `id`;
   - URL не существует;
   - `data-id` в HTML не совпадает с manifest.

## Нужные команды

Сделать команды:

```powershell
$env:PREMIUM_PIN='...'
node scripts/build-premium-vault.mjs
Remove-Item Env:\PREMIUM_PIN
```

и проверку без перезаписи:

```powershell
$env:PREMIUM_PIN='...'
node scripts/build-premium-vault.mjs --check
Remove-Item Env:\PREMIUM_PIN
```

`--check` должен:

- расшифровать текущий Vault;
- сравнить Vault с manifest;
- проверить физические файлы;
- проверить `premium.html`;
- вывести список проблем;
- завершиться с non-zero exit code, если есть рассинхрон.

## PIN / login / logout behavior

Сейчас `premium.html` хранит доступ в `localStorage`:

- `nge-vault-cache`
- `nge-vault-cache-v`
- `nge-vault-pin`

Нужно сделать явную функцию полной делогинизации:

```js
function logoutPremiumVault() {
  localStorage.removeItem('nge-vault-cache');
  localStorage.removeItem('nge-vault-cache-v');
  localStorage.removeItem('nge-vault-pin');
  sessionStorage.removeItem('nge-vault-cache');
  document.querySelectorAll('.card').forEach(card => {
    card.classList.add('locked');
    const link = card.querySelector('.card-open');
    if (link) link.href = '#';
  });
}
```

Добавить UI/сценарии:

1. `premium.html#lock` должен вызывать полный logout.
2. Кнопка "Сбросить доступ" должна делать то же самое.
3. Если `vault-version` изменился и silent re-decrypt не удался, старый кэш нельзя использовать как полноценный доступ к новым урокам.
4. После сброса PIN/пароля пользователь должен снова вводить PIN.

## Acceptance criteria

Готово считается только если:

1. Новый урок добавляется в manifest один раз.
2. После запуска сборки он автоматически попадает в Vault.
3. После ввода PIN карточка нового урока раскрывается.
4. Если урок есть в HTML, но нет в Vault, `--check` падает с ошибкой.
5. Если урок есть в Vault, но нет физического `index.html`, `--check` падает с ошибкой.
6. Если `data-id` не совпадает с manifest, `--check` падает с ошибкой.
7. `#lock` полностью очищает доступ.
8. Кнопка сброса полностью очищает доступ.
9. После logout все карточки снова locked.
10. После повторного ввода PIN все доступные уроки снова раскрываются.

## Важное ограничение

Не хранить PIN в коде.

PIN должен передаваться только через:

- переменную окружения `PREMIUM_PIN`;
- ручной ввод в браузере;
- временный bootstrap hash, если он уже используется.

Не коммитить PIN, пароли, расшифрованный Vault и приватные списки доступа.

## Файлы, которые нужно смотреть

- `site-public-clean/lingua-boost-lab/premium.html`
- `scripts/repack-premium-vault.mjs`
- `PREMIUM-VAULT-ARCHITECTURE.md`
- `site-public-clean/lingua-boost-lab/b1/travel-talk-light-and-bright-2/index.html`

## Желаемый результат

Архитектура должна стать такой:

`premium-lessons.json -> build script -> premium.html cards + encrypted Vault + vault-version`

А не такой:

`урок отдельно -> карточка отдельно -> Vault вручную -> кэш браузера случайно мешает`
