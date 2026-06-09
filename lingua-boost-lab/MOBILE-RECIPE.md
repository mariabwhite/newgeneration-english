# Lab Mobile Banner Recipe (2026-06-09)

Документация по мобильному дизайну Lab. Лежит рядом с кодом, чтобы будущие сессии не догадывались с нуля.

## Эталон
**Ancient China Cultural Studies** (`b1/ancient-china-cultural-studies.html`) — не трогаем.
**Whispering Library** + **Stars and Stellar** — отдельные стилизации, тоже не трогаем.

## Главный файл
- `assets/lab-banner-canon.css` — single source of truth для mobile-баннеров
- Подключается **последним** в `<head>` каждого урока:
  ```html
  <link rel="stylesheet" href="../assets/lab-banner-canon.css?v=20260610b" data-tag="lab-banner-canon">
  ```

## Применён на 11 уроках
- pre-a1/hello-classroom-fun
- pre-a1/body-and-grammar-pink
- a1/easter-english-lesson
- a1/prepositions-world
- a1/school-words-and-pronouns
- a2/english-booster-a2-b1
- a2/ancient-china-explorer
- b1/grammar-arcade-pc-pp
- b1/space-explorers-english
- b1/word-building-prefixes-and-suffixes
- b2-plus/articles-with-geographical-names

## Recipe (cream side-veil от Claude Design)

**Идея:** иллюстрация **яркая** (opacity 1), но слева ложится полупрозрачная "вуаль" цвета урока. Текст слева на solid-cream, иллюстрация целиком справа.

```css
@media (max-width: 820px) {
  html body .canon-l-hero.canon-l-hero.canon-l-hero {
    min-height: 340px !important;
    max-height: 380px !important;
    border-radius: 22px !important;
    /* ... */
  }
  html body .canon-l-hero.canon-l-hero.canon-l-hero::after {
    background: linear-gradient(90deg,
      color-mix(in srgb, var(--lb-bg) 94%, transparent) 0%,
      color-mix(in srgb, var(--lb-bg) 74%, transparent) 40%,
      color-mix(in srgb, var(--lb-bg) 22%, transparent) 62%,
      transparent 80%) !important;
  }
  html body .canon-l-hero.canon-l-hero.canon-l-hero .canon-l-hero-pill {
    background: #fff !important;
    border-radius: 10px !important;
    /* ... */
  }
}
```

Тройное повторение класса `.canon-l-hero.canon-l-hero.canon-l-hero` — для увеличения specificity до 0,0,3,X, чтобы побеждать !important rules в lesson inline styles.

## Per-lesson object-position

Иллюстрации с центральным персонажем сдвигаются через **inline `style`** на `<img class="canon-l-hero-bg">`:

```html
<img class="canon-l-hero-bg" style="object-position:75% center !important" src="...">
```

Это побеждает любой CSS и JS lock-loops.

| Урок | object-position |
|---|---|
| Body & Grammar | `75% center` |
| Easter English | `75% 70%` |
| English Booster | `30% center` |
| Prepositions World | `80% center` |
| Word Forge | `left center` |

## Lesson-level fixes

### Restaurant Menu Lab
В конце `<head>` файла:
```html
<style id="claude-restaurant-mobile-canon-...">
@media (max-width: 820px) {
  html body .hero-visual { display: none !important; }
  html body section.hero {
    background-image: linear-gradient(135deg, #fff5e8 0%, #fde9d0 100%) !important;
    /* ... */
  }
}
</style>
```
Шеф скрыт на mobile, текст на cream gradient.

### Grammar Arcade
Inline `style="..."` прямо на h1 + JS перезаписать (`fixMobile` функция в lesson — заменили `max-width:210px` → `max-width:100%`).

### Whispering Library
Убраны `is-violet` / `is-emerald` модификаторы из HTML — pills все одного оранжевого.

## Cache-bust
При любом изменении `lab-banner-canon.css` → bump `?v=` во всех HTML:
```bash
find lingua-boost-lab -name "*.html" -exec sed -i 's|lab-banner-canon.css?v=20260610b|lab-banner-canon.css?v=20260610c|g' {} \;
```

## Не покрыты canon-ом
- **Core Trainer** — `.hero-mini` другая архитектура
- **Past Simple Adventure** — нет `canon-l-hero` структуры
- **Menu Architect** — `.hero` legacy, имеет свой inline-fix
- **Restaurant Menu Lab** — `.hero` legacy, свой inline-fix

## Открытое (TODO)

1. **English Booster** — pills `.canon-l-hero-pills` absolute-позиционированы поверх заголовка. Fix через `position:absolute; bottom:14px` запушен `076a22e`, ждёт визуальной проверки на iPhone
2. **Whispering Library** — бургер 3-чёрточки в topbar тёмный, не виден на фиолетовом
3. **Watermark «Whispering»** на тексте лида — opacity ниже не дошёл
4. **Index / Premium landscape** на iPhone (~844px viewport) — кнопки CAB/THEME/RU накладываются на длинное nav-меню
5. **Past Simple Adventure** / **Core Trainer** — нужен отдельный подход (другая архитектура hero)

## Backup из bundle для Claude Design

В `_FOR-CLAUDE-DESIGN/` на десктопе у Маши лежит bundle из 15 HTML + `ЗАДАЧА.md` — для повторного использования Claude Design.

## Финальный коммит дня
`076a22e` (Booster pills sticky bottom) → newgeneration-english.ru
