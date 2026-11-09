# 🖼 Julia · PE Day · Image Prompts

**Генератор:** Playwright → ChatGPT Марии (DALL-E 3), бесплатно.
**Стиль по всем:** same illustrative style как `julia-big-monday` и `julia-bubble-wishes` — warm, children's-book, soft-shaded, slight paper texture, bright but not neon, happy faces. American school vibe.
**Канон героев:** Julia (9, girl, brown hair ponytail) · Mum (American mom) · Dad (American dad, athletic, holds silver stopwatch) · John (6, little boy, missing one sneaker joke) · Emma (9, Julia's best friend, different look so they distinct) · Barsik (grey cat, golden-green eyes).
**Format:** 1024×1024 PNG для hero/cast, 1024×768 для photo cards, 512×384 для pic-grid cards.

---

## 1 · `img/scene-00-hero.png` — HERO BACKGROUND

**Prompt:**
> Wide cinematic school sports day scene, American elementary school field, early morning sunshine, running track with coloured finish-line tape, four 8–10 year old kids in sports kit sprinting toward camera, a coach on the right side blowing a whistle, a cheering crowd on the left with parents clapping and holding signs, small American flags along the fence, warm green grass, soft shadows, children's book illustration style, warm palette, no text, 16:9 wide composition, centre of composition slightly lower so title fits top.

---

## 2 · `img/cast-sports-day.png` — WRAP-UP FAMILY PORTRAIT

**Prompt:**
> Group portrait at the end of a school sports day: Julia (9, brown ponytail, wearing a silver medal around her neck, happy smile), her Mum (warm American mom in casual clothes holding a lunch box), her Dad (athletic American dad with old silver stopwatch in one hand), little brother John (6, holding a crooked GO JULIA sign with a backwards letter I), best friend Emma (9, gold medal around her neck, hugging Julia), and a grey cat Barsik sitting in a small carrier with a tiny team t-shirt. In the lower left corner, a small snail (Turbo) in a tiny hat on the grass. Golden-hour light, finish-line tape in the background, children's book illustration style, warm palette, happy faces, no text on image.

---

## 3 · `img/pic-pe-rope.png` — PICTURE TALK · "In the gym"

**Prompt:**
> American school gym interior, two 8–10 year old kids climbing a thick rope up to the ceiling, one halfway up and smiling, the other near the floor looking up, their PE teacher (American coach, clipboard + stopwatch) standing below. Wooden gym floor, American flags on the walls, sports ropes and climbing frames. Bright gym lights. Children's book illustration style, 4:3 composition, no text.

---

## 4 · `img/pic-race.png` — PICTURE TALK · "The 60-metre race"

**Prompt:**
> Four American schoolkids (ages 8–10, mixed gender, sports kit, race numbers pinned to shirts) running the 60-metre sprint on a school field, finish-line tape with red-white-blue colours just a few metres away, the girl in a yellow shirt in front leading, concentrated faces. Coach on the right side with a stopwatch and whistle. Grass field, bright sunny morning, warm palette. Children's book illustration, 4:3, no text.

---

## 5 · `img/pic-ball.png` — PICTURE TALK · "The team game"

**Prompt:**
> Mixed-gender team of American schoolkids (ages 8–10) playing soccer in a schoolyard. One child is mid-motion, about to kick the ball, which hovers just above the grass. Other kids run toward the ball, some clapping their hands in anticipation. Coach on the side clapping encouragement. School building visible in the background. Bright sunny day, children's book illustration style, 4:3, no text.

---

## 6 · `img/photo-sports-day.png` — PHOTO CARD · Race moment

**Prompt:**
> Wider horizontal composition of a school sports day, the 60-metre sprint. On the track, four kids running toward camera. The girl in a yellow shirt (Julia, 9, brown ponytail) is in front — she is about to cross the finish-line tape, arms spread, face determined but smiling. On the right side, the coach holds a whistle to her mouth and glances at a stopwatch. On the left side of the composition, in the crowd: Julia's Mum clapping energetically, Dad filming with his phone, little brother John (6) holding up a big sign reading "GO JULIA" (the letter I in JULIA is backwards). A grey cat (Barsik) sits on a wooden bench in a tiny white team t-shirt, looking wary. Soft golden morning light, American school field setting, warm palette, children's book illustration style, 4:3 (1024×768), no text other than the visible GO JULIA sign.

---

## 7 · `img/photo-long-jump.png` — PHOTO CARD · Long jump moment

**Prompt:**
> Mid-action long jump shot, horizontal composition. A 9-year-old girl (Julia, brown ponytail, sports kit, race number 7) is frozen in the air mid-flight over a long-jump pit, arms thrown forward, legs tucked under. Grains of sand already lifting below her. Concentrated, slightly worried expression — mouth closed, focused eyes. On the right side of the pit, the coach stands with a measuring tape ready. In the soft-focus background, two other kids stretching before their turn. American school athletics field, bright afternoon light, warm tones. Children's book illustration style, 4:3 (1024×768), no text on image.

---

## 8 · CAST-CARD portraits (optional bonus — only if Мария хочет)

Если нужны отдельные portrait-chips для cast-strip:
- `img/cast-julia-portrait.png` · Julia (9, brown ponytail, sports kit, friendly smile)
- `img/cast-mum-portrait.png` · Mum (warm face, apron over a casual American shirt, holding a plate of pancakes)
- `img/cast-dad-portrait.png` · Dad (athletic, hair slightly grey at the temples, holding silver stopwatch)
- `img/cast-john-portrait.png` · John (6, little boy, holding one sneaker in his hand, laughing)
- `img/cast-emma-portrait.png` · Emma (9, blonde or red hair — different from Julia — sports kit, big smile)
- `img/cast-barsik-portrait.png` · Barsik grey cat in a tiny team t-shirt, serious face

Пока в HTML они НЕ используются (cast-strip сейчас текстовый). Если понадобятся — добавлю `<img>` внутрь .cast-card.

---

## 9 · Sticker PNGs — НЕ ТРЕБУЮТСЯ

Все стикеры в теме урока — unicode emoji (🏃 📸 🎧 📖 🧩 📣 ⏳ etc.). PNG-стикеры не нужны.

---

## 10 · Пайплайн

1. Сгенерить 1–7 через DALL-E (Playwright Chat).
2. Переместить в `img/` этой папки.
3. Проверить что имена точно такие как в `index.html` (grep "img/" для списка).
4. Запушить вместе с index.html.

Файлы которые ссылаются в HTML (точная проверка):
- `img/scene-00-hero.png`
- `img/cast-sports-day.png`
- `img/pic-pe-rope.png`
- `img/pic-race.png`
- `img/pic-ball.png`
- `img/photo-sports-day.png`
- `img/photo-long-jump.png`
