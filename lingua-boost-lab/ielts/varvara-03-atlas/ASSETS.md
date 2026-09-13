# varvara-03-atlas · asset list

Всё, что нужно догенерить/нарисовать/найти для визуалки. Урок работает и без картинок (`onerror` прячет битые `<img>`), но с ними — красивее.

## Файлы, которые ждут ассетов

| # | путь | статус | назначение |
|---|------|--------|------------|
| 1 | `assets/img/reading-vantablack.png` | **пусто** — обязательно | hero-картинка в reading passage (шапка «The Blackest Black») |
| 2 | `assets/img/plan-elmswood.png` | **опционально** — сейчас inline SVG | замена SVG-плейсхолдеру карты для L-03 |
| 3 | `assets/img/listening-elmswood.png` | опционально — красотка | фото палм-хауса перед transcript'ом (сейчас нет `<img>` в разметке — нужно будет вставить) |
| 4 | `../varvara-02-tour/assets/img/hero-culture-shapes-us.png` | **уже есть** | hero-фон всей страницы (reuse из L2) |
| 5 | `assets/img/map-granford.jpg` | уже лежит | залоченный запас на будущий map-урок, в текущем не используется |
| 6 | `assets/img/plan-library.jpg` | уже лежит | залоченный запас на будущий plan-урок, в текущем не используется |

## Промпты для ChatGPT / Playwright / DALL-E 3

### 1. `reading-vantablack.png` — MUST HAVE

Формат: **1200×675 (16:9), PNG**

**Prompt:**
> Photorealistic editorial close-up: on the left, a small crumpled aluminium foil ball sitting on a matte grey studio surface — normal, shiny, dimensional. On the right, an identical crumpled foil ball but this one is entirely coated in Vantablack — it looks like a flat two-dimensional black silhouette, absolutely no visible depth or texture, as if a black felt-tip pen has cut a hole through the photograph. Dramatic side lighting from the left. Minimal composition, plenty of negative space. Editorial magazine quality, muted grey background, no text, no logos. 16:9 landscape.

**Alt phrasing (art-world variant):**
> Museum-quality product photograph of Anish Kapoor's installation Descent Into Limbo — a matte black circle painted on a white gallery floor that appears to be a bottomless void. Overhead lighting, minimalist white gallery interior, no visitors visible, 16:9 landscape crop.

---

### 2. `plan-elmswood.png` — OPTIONAL upgrade

Сейчас inline SVG внутри HTML работает и функционален (5 пронумерованных зон + компас + опции). Если хочешь красивее — сгенерь и я подменю `<svg>` на `<img>`.

Формат: **1200×900 (4:3), PNG**

**Prompt:**
> Top-down flat illustration of a botanic garden site plan titled "Elmswood Botanic Gardens". Rectangular boundary with a compass rose in the corner showing North at the top. Main entrance labelled at the south (bottom centre). On the central north-south axis: a large glass palm house labelled "55" (biggest structure). Top-left corner: a small building labelled "52" (herbarium). Top-right corner: a small building labelled "53" (seed bank). Middle-left, west of the palm house: a building labelled "54" (tea room and shop). Middle-right, east of the palm house: a building labelled "56" (education pavilion). Directly behind the palm house: a small pond and a rock garden zone. Between all buildings: green lawn with a few trees. Hand-drawn Wes Anderson symmetrical style, warm off-white paper background, muted mint + terracotta + navy palette, no other text besides the numbers 52-56 and the labels "Main entrance", "Pond", "Rock garden". 4:3 landscape.

---

### 3. `listening-elmswood.png` — OPTIONAL hero for transcript

Если добавляем — надо будет вставить `<img class="hero-img" src="./assets/img/listening-elmswood.png">` в начало `.transcript` блока.

Формат: **1200×675 (16:9), PNG**

**Prompt:**
> Warm midday photograph of a Victorian-era palm house glasshouse in a British botanic garden, seen from three-quarter angle, with tall palms visible through the glass and a small group of tour visitors gathered at the entrance. Soft late-morning light, gravel path in the foreground, no visible text or signage, editorial travel-magazine quality. 16:9 landscape.

---

## Быстрая проверка после генерации

1. Кинуть файл в `assets/img/`
2. Открыть `https://newgeneration-english.ru/lingua-boost-lab/ielts/varvara-03-atlas/` с `?v=2`
3. Vantablack должен появиться в hero passage; если 404 — картинка просто спрячется (не сломает разметку)

## Что уже inline / SVG (не требует ассетов)

- R-10 · Vantablack production flow-chart (SVG inside HTML)
- L-03 · Elmswood garden plan (SVG inside HTML — заменяемо `plan-elmswood.png`)
- Vocab · 14 flip cards (текст + CSS)
- Type badges · CSS + номера
