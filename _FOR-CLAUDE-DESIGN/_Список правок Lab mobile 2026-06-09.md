# 🎯 Список правок Lab mobile — 2026-06-09 (ФИНАЛ сессии)

> 🎨 **Открыть красиво:** ярлык «Открыть MD-файл» на десктопе → перетащи `.md`.

---

## 🟢 Текущее состояние

- **HEAD:** `f6485cf` на `main` (`mariabwhite/newgeneration-english`)
- **Домен:** newgeneration-english.ru
- **Источник правды баннеров:** `lingua-boost-lab/assets/lab-banner-unified.css?v=20260610b`
- **Коммитов за день:** 38

---

## ✅ Что сделано (по группам)

### A. Унификация баннеров (главное)
1. Создан `lab-banner-unified.css` — single source of truth
2. Подключён последним в `<head>` всех 22 уроков
3. Геометрия: width calc(100% - 28px), height 420px, border-radius 22px, padding 0
4. Background image: opacity 1, object-fit cover, position по уроку
5. Soft gradient overlay снизу для контраста pills
6. Title: 28px, белый, text-shadow x3 (читается на любой иллюстрации)
7. Lead скрыт на mobile
8. Pills: grid 2×2, белые soft-square 10px
9. Cap-at-4 — 5-я+ скрыты

### B. Per-lesson object-position (картинка по уроку)
10. Easter → `100% 70%` (inline на img)
11. Hello → `100% center` (limited ассетом)
12. Body & Grammar → `100% center` ✅ работает
13. English Booster → `100% center` ✅ работает
14. Prepositions World → `100% center` (limited ассетом)
15. Word Forge → `right 30%` ✅ работает

### C. Pills цвет
16. Whispering Library: убраны is-violet / is-emerald модификаторы из HTML — все 6 pills один оранжевый

### D. Mojibake вычищен (11 файлов)
17. Premium, English Booster, Core Trainer, Restaurant Menu, Space Explorers, Word Forge, Grammar Arcade, Stars, Articles, Ancient China Explorer, a1-01
18. data-ru `???` атрибуты заменены по словарю по data-en (Catalog → Каталог, Workshop → Воркшоп и т.д.)

### E. Прочее
19. Jerusalem cover (Premium) — заменён на твой закат с куполами
20. Stars цепь шагов: scroll + fade-индикатор справа
21. Topbar pills CAB/THEME/RU — мягкий квадрат, выровнены
22. Catalog level chips — мягкий квадрат 10px

---

## ❌ Открытые TODO (на следующую сессию)

| # | Урок | Что |
|---|---|---|
| 1 | **Grammar Arcade** | Title `Gramma\nr Arcade` режется. 6 inline-JS lock-loops перебивают всё. Нужен deep refactor (удалить блоки 2274-2440 в HTML) |
| 2 | **Menu Architect** | «Build & Present» полупрозрачный watermark, шеф режет «Architect», дубль RUBRIC (один section pill + одна кнопка) |
| 3 | **Hello / Easter / Prepositions** | Иллюстрации с центральным персонажем — нужны новые ассеты через Sora с персонажем сбоку, чтобы заголовок слева был полностью свободен |

---

## 🔍 Спека баннера

Полная спека на `_ИДЕАЛЬНЫЙ дизайн баннера — спека по Китаю.md` — там 89 пунктов. Файл `lab-banner-unified.css` написан по этой спеке.

---

## 📅 Хронология последних 10 коммитов

| SHA | Что |
|---|---|
| `d6a1c4e` | Stars rail scroll-indicator |
| `49f7fe2` | Mojibake `???` в nav почищен |
| `7e11e0d` | Whisper pills убраны цветные модификаторы |
| `c9576f6` | End-of-style override Whisper/Restaurant/Booster |
| `ef13b0b` | Booster lead hide, Whisper pills color |
| `595600e` | Iter aa selectors |
| `9443f55` | Iter z fixes |
| `d06c1f7` | **🆕 lab-banner-unified.css — single source of truth** |
| `24595b7` | tune: object-position 100%, text-shadow stronger |
| `f6485cf` | inline `style` на canon-l-hero-bg для 6 уроков |

---

## 🟢 Что МОЖЕШЬ открывать на iPhone

В приватной Safari или с `?cb=99`:

- newgeneration-english.ru — главная (с «Места на лето 2026»)
- newgeneration-english.ru/lingua-boost-lab/ — каталог
- newgeneration-english.ru/lingua-boost-lab/premium.html
- newgeneration-english.ru/lingua-boost-lab/b1/ancient-china-cultural-studies.html (эталон)
- newgeneration-english.ru/lingua-boost-lab/pre-a1/body-and-grammar-pink.html
- newgeneration-english.ru/lingua-boost-lab/b1/whispering-library-quest.html

---

> Откат всего изменения дня (на случай если что-то полетит): `git revert d06c1f7..HEAD` — возвращает на состояние до unified.css
