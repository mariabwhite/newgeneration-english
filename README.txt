NEW GENERATION ENGLISH — собранный сайт
=========================================

Что внутри
----------
Главные страницы:
  index.html, about-project.html, programs.html, cases.html,
  conditions.html, blog.html, travel.html, diagnostic-test.html

Кабинеты:        cabinet/index.html, login.html, parent.html, teacher.html, student.html
Лаборатория:     lingua-boost-lab/index.html

Где это на сайте
----------------
Этот каталог — production-сайт для домена:
  newgeneration-english.ru

GitHub remote:
  https://github.com/mariabwhite/newgeneration-english.git

Кабинет на основном сайте:
  /cabinet/

Локально кабинет лежит здесь:
  site-public-clean/cabinet/

Зашифрованные данные кабинета лежат здесь:
  site-public-clean/cabinet/vault/

Источник правды для данных учеников НЕ здесь, а в соседнем репозитории:
  ../nge-cabinet/data.js

Кабинетный pipeline
-------------------
1. Править ученика в ../nge-cabinet/data.js.
2. В ../nge-cabinet bump data.js?v=... во всех 5 HTML:
   index.html, login.html, parent.html, student.html, teacher.html.
3. Из корня проекта запустить:
   node scripts/gen-vault.js
4. Скрипт пересоберёт cabinet/vault/*.enc и cabinet/vault/index.json здесь,
   в site-public-clean.
5. Push нужен в оба репозитория:
   ../nge-cabinet
   site-public-clean

Последняя кабинетная серия 2026-06-28:
  nge-cabinet 49aba1d — Денис: урок 28.06 completed + домашка.
  site-public-clean 38b9a7c — Vault rebuild после Дениса.
  Daniella: новый интенсив 10 x 2500 = 25 000, все 10 уроков показаны через
  summer_plan_note.
  Тимофей: Workbook 02 Past Tenses привязан к фактически completed уроку 25.06.

Premium Lab — последняя правка login/logout
-------------------------------------------
Рабочий файл:
  lingua-boost-lab/premium.html

Server-side functions:
  functions/api/premium-login.js
  functions/api/premium-lessons.js
  functions/api/premium-logout.js
  functions/_shared/premium-auth.js

Последняя незакоммиченная правка в premium.html:
  вместо двух ссылок "Сбросить доступ" и "Войти" сделана одна кнопка
  "Войти" / "Выйти" в topbar и footer.

Логика:
  - без доступа кнопка ведёт на /lingua-boost-lab/login.html;
  - после успешной авторизации текст меняется на "Выйти";
  - при выходе чистятся localStorage/sessionStorage ключи vault-cache:
    nge-vault-cache, nge-vault-cache-v, nge-vault-pin;
  - затем вызывается /api/premium-logout и пользователь возвращается на
    /lingua-boost-lab/login.html;
  - premium.html также выставляет состояние кнопки через setPremiumAuthState().

Общие файлы:
  system.css       — дизайн-токены, базовые компоненты
  site.js          — переключение языка (RU/EN) + лёгкая обёртка темы
  theme-cycle.js   — переключение темы (light/dark), синхронизация ссылок,
                     запись в localStorage И в URL (?theme=...&lang=...)

Как работает цепочка темы/языка
-------------------------------
1. На любой странице нажмите DARK/LITE — тема + ключ "lesson-palette" пишется
   в localStorage, и одновременно в URL текущей страницы добавляется
   ?theme=light-lab|black-lab&lang=ru|en
2. Все теги <a> на странице автоматически обновляются — на ссылке тоже стоит
   ?theme=...&lang=...
3. При переходе на следующую страницу она читает либо localStorage
   (если браузер делит один origin для всех файлов — Chrome это умеет),
   либо URL-параметры (на случай file:// + Firefox/Safari, где localStorage
   изолирован пофайлово).
4. То же самое для языка (RU/EN).

4 комбинации (рус-светл, рус-тёмн, англ-светл, англ-тёмн) живут на любой странице
и наследуются по цепочке. Default — RU + DARK.

Как открыть локально
--------------------
Если у вас Chrome или новый Edge — можно просто открыть index.html двойным
кликом, всё будет работать.

Если Firefox/Safari иногда изолируют localStorage между файлами, всё равно
будет работать благодаря URL-параметрам — главное переходить по ссылкам
внутри сайта (а не открывать страницы напрямую без параметров).

Что НЕ скопировано
------------------
- assets/video/kids-lesson-01.mp4 и kids-lesson-02.mp4 — слишком большие файлы,
  не прошли через копировщик. Их можно вручную скопировать из вашей
  локальной папки "САМАЯ УДАЧНАЯ КОПИЯ - ЭТАЛОН!/assets/video/" в site/assets/video/

Известные нюансы (стоит знать)
------------------------------
- diagnostic-test.html использует свою систему локализации
  (data-ru-text/data-en-text + html[data-lang]), а не общую (data-ru/data-en).
  Она подхватывает язык из общего localStorage, но может не реагировать на
  кнопку #langBtn от site.js. У неё есть собственная кнопка "RU / EN".

- Lab (lingua-boost-lab/index.html) использует собственный lab-theme-sync.js
  с расширенной палитрой (peach/green/rose/cyan и т.д.), но базовая
  пара dark/light синхронизирована с основным сайтом через те же
  ключи localStorage (nge-theme, lesson-palette).
