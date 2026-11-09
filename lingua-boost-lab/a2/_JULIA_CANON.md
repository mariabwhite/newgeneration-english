# 🔒 JULIA CANON · NO DEVIATION

**Lock date:** 2026-11-09 (replaces previous draft that incorrectly said "Moscow + roubles + no Dad")
**Rule:** любой новый урок Юли читает этот файл ПЕРЕД рендером. Отход от канона — reject, не merge.
**🚨 Источник правды — этот файл, а НЕ старые уроки Юли.** В старых Juля-уроках встречаются ошибки (напр. `julia-big-monday` упоминает «near Moscow» и «roubles» — это НЕ канон, это баг, который надо постепенно вычищать).

---

## 1 · CAST (канон — 6 постоянных + 1 pet-cameo)

| # | name | role | возраст | фикс-факты |
|---|---|---|---|---|
| 1 | **Julia** | main character | **9** | рассказчица, любит бегать, лучшая подруга Emma |
| 2 | **Mum** | мама Julia | — | по воскресеньям печёт **pancakes with honey + raspberry jam**, гуляет в парке с детьми |
| 3 | **Dad** | папа Julia | — | **ЕСТЬ в каноне** — упоминать в семейных сценах |
| 4 | **John** | младший брат Julia | **6** | теряет один ботинок по понедельникам, хочет домашнее животное, «cowboy» на ярмарке |
| 5 | **Emma** | лучшая подруга · одноклассница | **9** | ходит с Julia везде — на ярмарку, в парк, на спорт |
| 6 | **Barsik** | семейный **кот** | **7** | большой серый кот, золотисто-зелёные глаза, «king of the house», НЕ любит котят |
| 7 | **Turbo** | семейная **улитка** (pet-cameo) | — | купили в pet shop, живёт в маленьком террариуме, медленный но любимый |

**🚨 `JULIA_FAMILY` в каноне:** Mum + Dad + Julia + John + Barsik + Turbo. **НЕ забывать Dad.** Если в уроке family-scene — Dad должен быть в кадре или хотя бы в упоминании.

**Эпизодические (можно упоминать):**
- `Mrs. Pilsberry` — cat-breeder, Scottish Folds (экзотика, дорогая порода)
- `Aunt Anya` — тётя, её кот Рыжик (огромный рыжий)
- `Vova` — одноклассник (sleepy Vova)

---

## 2 · LOCATION (locked · FOREIGN FAMILY)

- **Семья живёт в США (America).** Юля — иностранная девочка, НЕ русская.
- **Small town** / suburb — не мегаполис. Есть **большой парк**, **ярмарка каждое лето** (summer fair).
- Школа — **American public school** (grade 3–4), есть PE lesson и sports day.
- **🚨 НЕ Moscow. НЕ Russia. НЕ «near Moscow».** Если в старом уроке есть «Moscow» — это баг. Новые уроки — America.

---

## 3 · CURRENCY (locked · DOLLARS)

- **Доллары (dollars, $).** НЕ roubles, НЕ pounds, НЕ euros.
- Примерные цены для контекста:
  - $500 — purebred Scottish Fold kitten
  - $25 — pair of jeans on sale
  - $5 — pocket money at the fair
  - $12 — one PE kit (sneakers + shorts)
- **🚨 НИКАКИХ рублей.** Если в старом уроке есть «roubles» — баг.

---

## 4 · TIME-ANCHOR

- **Julia · 9 · grade 3–4** (American system)
- **Каникулы в Bodrum** — прошлое лето. Можно упоминать как прошлый опыт (в США семьи часто ездят в Турцию через charter trips).
- **Olympics** — мечта на будущее («One day I'd like to run in the Olympics»).

---

## 5 · WEEKLY RITUALS (стабильные якоря)

| день | ритуал |
|---|---|
| понедельник утро | John теряет один ботинок, Mum несёт pancakes, Barsik смотрит с подоконника, Turbo медленно ползёт в террариуме |
| воскресенье утро | Mum делает **pancakes with honey + raspberry jam** |
| воскресенье день | семья (все четверо + возможно Dad) гуляет в парке |
| лето | summer fair в парке с Emma и John |

---

## 6 · HOMEWORK + NO-GO LIST

**Julia может говорить про:** PE, sports, бег, прыжки, Emma, Dad, Mum, John, Barsik, Turbo, pet shop, ярмарку, парк, Bodrum (прошлое лето), school.

**🚨 Julia НЕ может упоминать:**
- Moscow, Russia, Saint Petersburg (не её дом)
- Roubles (не её валюта)
- «Mother / Father» в школьных реалиях — предпочитать «Mum / Dad» (familiar, British spelling allowed per edge-tts voices, не критично)
- Старшую сестру, бабушку/дедушку — пока нет в каноне

**Если урок вводит нового персонажа** (тренер, новый одноклассник, кузен) — обновить этот файл с именем и возрастом.

---

## 7 · ARCHITECTURE (CANON)

| элемент | канон |
|---|---|
| CSS theme | per-lesson (bubble=purple, PE=green, halloween=orange) |
| Topbar | NG mark + brand-copy + 2 pills (level · 60 min) |
| Hero | gradient + bg image + eyebrow + title + em subtitle + lead + hero-tags |
| **Cast strip** | **6 карточек по порядку: Julia · Mum · Dad · John · Emma · Barsik** (Turbo mention в passage, не в strip) |
| Tabs | 4: 📖 Урок · 🐾 Vocab · 🔀 Grammar · 📝 Рабочая тетрадь (или спец-tabs для speaking-reading) |
| Warm-up | рифма-загадка + spell-the-word |
| Основная часть | 5 chapters ИЛИ speaking + reading блоки |
| Vocab Capsule | **ОБЯЗАТЕЛЬНО В КОНЦЕ · 20 слов · click-to-hear + RU + example + spelling** (`feedback_julia_vocab_capsule_ending`) |
| Workbook | 1-2 коротких home-task |
| Wrap-up | gradient card + «See you next class, Julia» |

---

## 8 · AUDIO + VOICES (edge-tts)

- `en-US-AriaNeural` — Julia narrator (rate -6%, **American English**)
- `en-US-SaraNeural` — Mum (American)
- `en-US-GuyNeural` — Dad (American, warm)
- `en-US-AnaNeural` — John (child voice)
- `en-US-JennyNeural` — Emma
- Barsik + Turbo — narrator voices them, не отдельный голос

**🚨 Все голоса — en-US, НЕ en-GB.** Канон = American family.

---

## 9 · WHEN IN DOUBT

1. Прочитать ЭТОТ файл. Он — источник.
2. НЕ брать канон из старых уроков (они с багами).
3. НЕ придумывать детали — спросить Марию одним вопросом (формат: «Юля · [вопрос] · эталон: X / Y / Z?»).
4. После ответа — обновить этот файл.

---

## 10 · ИЗВЕСТНЫЕ БАГИ СТАРЫХ УРОКОВ (нужна чистка)

- `julia-big-monday/index.html` L437 «one flat in a small town near Moscow» → должно быть «in a small town in America»
- `julia-big-monday/index.html` L514 «Mum gave me 300 roubles» → «300 dollars» / «30 dollars» (пересчитать разумно)
- `julia-big-monday/index.html` L520 «50 000 roubles» → «500 dollars» (Scottish Fold kitten в США примерно столько)
- `julia-big-monday/index.html` L808 «2 500 roubles jeans» → «25 dollars» 
- Cast-strip в старых уроках без Dad — расширить до 6

(Эти правки — отдельная задача, не мешать с новым уроком. Чинить когда Мария скажет «почисти старые».)
