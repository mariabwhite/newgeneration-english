# 🎨 Image prompts · `julia-big-monday` · A2

**Канал:** Playwright → ChatGPT Марии → DALL-E 3 (бесплатно).
**Паттерн работы:** вставляешь блок STYLE первым сообщением в сессии, потом по одному промпту отдельными сообщениями. Один chat = одна серия (чтобы characters остались consistent).

**Resolutions DALL-E 3:**
- 1024×1024 — characters, mini-stickers, vocab PNGs
- 1792×1024 — scene posters (wide)
- 1024×1792 — для вертикальных композиций (здесь не нужно)

**Transparent fon:** DALL-E нативно не умеет transparent — говорим "pure white background" / "clean white studio background" и потом Марино `remove.bg` или GPT prompt "transparent cutout". Для scene posters фон НУЖЕН (это кадр истории).

---

## 🎨 CANON STYLE (вставить ПЕРВЫМ сообщением в чат ChatGPT)

```
STYLE REFERENCE for every image in this series (reuse exactly):

- Children's picture-book illustration, flat vector style with soft inner shading.
- Warm, cozy, slightly whimsical — Oliver Jeffers meets Lauren Child feel.
- Clean confident black outlines (2-3 px), gentle inner highlights, no gradients inside shapes, no 3D rendering, no photo-realism, no AI-glossy look.
- Palette for THIS lesson:
    sun yellow        #FFB84D
    soft sun glow     #FFE08A
    sky blue          #8ECCF0
    cheek pink        #FF9FB2
    warm cream        #F7EFDC
    deep navy lines   #0E1B36
- Characters: round friendly faces, 2 big dot eyes, small warm smiles, light rosy cheeks.
- Russian features for family: light-to-medium skin, soft hair colors.
- NEVER include text, letters, numbers, logos, speech bubbles, captions, or watermarks in the image.
- Composition: subject centered, generous breathing room, nothing cropped by edges.

I will send one subject per message. Keep the characters CONSISTENT across the whole series — same hair, same clothes, same proportions.
```

---

## 👨‍👩‍👧‍👦 1. CHARACTERS (8 PNG, 1024×1024, pure white bg → cutout)

### 1.1 `char-julia.png`
```
Full-body portrait of Julia, 9-year-old Russian girl. Light brown chin-length wavy hair with straight bangs. Big round green eyes with long lashes. Light rosy cheeks. Small warm smile. Wearing a mustard-yellow knit sweater, dark navy jeans, white sneakers. Holding a sketchbook under her left arm. Slight 3/4 front pose, feet planted, confident but friendly. Pure white background. No text.
```

### 1.2 `char-mum.png`
```
Full-body portrait of Mum Olga, 36-year-old Russian woman, warm and kind. Short brown bob haircut, green eyes, light rosy cheeks, soft smile. Wearing a loose cream knit sweater with sleeves rolled up to the elbows and a dark navy apron with a few colorful paint smudges. Holding a wooden mixing spoon in her right hand. Slight 3/4 pose. Pure white background. No text.
```

### 1.3 `char-dad.png`
```
Full-body portrait of Dad Pavel, 38-year-old Russian man. Thick well-trimmed black beard, round black-framed glasses, dark messy hair, warm half-smile. Wearing a dark navy hoodie and brown corduroy trousers, grey slippers. Holding an acoustic guitar casually by the neck, resting it against his hip. Slight 3/4 pose. Pure white background. No text.
```

### 1.4 `char-max.png`
```
Full-body portrait of Max, 5-year-old little brother. Round face, messy light brown hair sticking up, big round brown eyes, HUGE open-mouth grin showing one missing front tooth. Wearing a bright green t-shirt with a small cartoon-style friendly green T-rex printed on the chest, dark blue shorts, ONE blue sneaker on the right foot and bare left foot (comic touch — "the lost shoe"). Mid-skip pose, one arm raised. Pure white background. No text.
```

### 1.5 `char-cat-pepper.png`
```
Side view of Pepper, a very fat orange tabby cat. Huge round belly, short legs, long whiskers, two round yellow-green eyes, pink nose. Orange tabby stripes, white chest and paws. Mid-leap pose — all four paws spread, body stretched slightly. A grilled sausage hanging from his mouth. Guilty-smug expression. Exaggerated round comic proportions. Pure white background. No text.
```

### 1.6 `char-dog-biscuit.png`
```
Side view of Biscuit, a small brown dachshund-mix puppy. Long body, short legs, floppy ears, big round shiny black eyes, pink tongue slightly out, short wagging tail. Chocolate-brown fur with cream chest and paws. Sitting pose, head tilted curiously. Sweet, timid, loveable. Pure white background. No text.
```

### 1.7 `char-grandma-lara.png`
```
Full-body portrait of Grandma Lara, 65-year-old Russian babushka. Soft grey hair in a loose bun partly covered by a cream flowery headscarf tied under the chin. Warm wrinkles around smiling green eyes, rosy round cheeks. Wearing a navy cardigan over a cream blouse with embroidered small red flowers, long dark skirt, warm slippers. Holding a glass jar of strawberry jam with a red cloth tied over the lid. Slight 3/4 pose. Pure white background. No text.
```

### 1.8 `char-grandpa-petya.png`
```
Full-body portrait of Grandpa Petya, 68-year-old Russian grandfather. Long bushy grey-white beard reaching his chest. Deep smile wrinkles, kind squinting blue eyes under bushy brows. Wearing a warm brown knit sweater with suede elbow patches, olive-green trousers, sturdy brown boots. Wide-brimmed beekeeper straw hat with mesh veil pushed up on the brim. Holding a hexagonal honey jar in his right hand, wooden honey dipper in his left. Slight 3/4 pose, friendly stance. Pure white background. No text.
```

---

## 🧷 2. MINI-STICKERS (10 PNG, 1024×1024, pure white bg → cutout)

### 2.1 `sticker-clock-730.png`
```
Round yellow retro alarm clock showing 7:30. Two bells on top, two tiny cartoon legs sticking out from the bottom. The clock face has a shy smiling face (two dot eyes, small smile). Hour hand pointing between 7 and 8, minute hand pointing straight down to 6. Soft shadow underneath. Flat kid-book vector style. Pure white background.
```

### 2.2 `sticker-pancake.png`
```
Golden pancake stack of 3 fluffy cakes. A pat of butter melting on top. A drizzle of amber honey running down the sides. Small blueberries scattered around the base. Soft shadow underneath the plate. No plate visible — just the stack floating on pure white background. Flat kid-book vector style.
```

### 2.3 `sticker-cat-wink.png`
```
Pepper the fat orange tabby cat (same character as char-cat-pepper) in a bouncy jumping pose. One eye winking, the other wide open and bright yellow-green. Pink tongue slightly out. All four paws spread, tail flicked up with a curl. Cheeky mischievous look. Pure white background. Flat kid-book vector style.
```

### 2.4 `sticker-milkshake.png`
```
Tall curvy glass with a thick strawberry-pink milkshake. A red-and-white striped straw sticking out. A big dollop of whipped cream on top with a bright red cherry. Three or four beads of condensation on the glass. Soft shadow underneath. Pure white background. Flat kid-book vector style.
```

### 2.5 `sticker-book.png`
```
Open school copybook with pale blue horizontal lines, red margin line on the left. A yellow pencil with a pink eraser laying diagonally across the pages. Slight curl on the bottom-right page corner. Soft shadow underneath. Pure white background. Flat kid-book vector style.
```

### 2.6 `sticker-balloon.png`
```
Three cheerful party balloons tied together with curling ribbons: one yellow, one cheek-pink, one sky-blue. Small highlights on each balloon suggesting shine (no gradient — a tiny white crescent shape). Ribbons curling playfully downward. Pure white background. Flat kid-book vector style.
```

### 2.7 `sticker-moon.png`
```
Crescent moon with a sleepy closed-eye face and small smile. Three small 4-point stars floating around it. Soft night-blue glow halo. Flat kid-book vector style. Pure white background.
```

### 2.8 `sticker-crystal-ball.png`
```
Purple fortune-teller crystal ball sitting on a small gold stand. Inside the ball: swirling galaxy pattern with tiny stars. Three sparkle marks ("✦") around the ball. Mystical glow around it. Flat kid-book vector style. Pure white background.
```

### 2.9 `sticker-star.png`
```
One warm sun-yellow 5-point star with a happy winking face (one eye wink, small smile). Three tiny sparkle lines radiating out from it. Soft shadow underneath. Flat kid-book vector style. Pure white background.
```

### 2.10 `sticker-airplane.png`
```
A playful cream-colored paper airplane with a tiny London skyline cutout visible through its wing: Big Ben, a red double-decker bus silhouette, London Eye. Three curved motion lines behind the airplane. Flat kid-book vector style. Pure white background.
```

---

## 🖼 3. SCENE POSTERS (9 PNG, 1792×1024 wide, with background)

### 3.1 `scene-00-hero.png`
```
Wide cinematic morning view of a small Russian town. Soft orange-and-pink sunrise sky between two low 5-story Soviet-era apartment buildings with pitched roofs. In the right foreground on a 5th-floor balcony: Julia (9-year-old girl, mustard sweater, light brown hair) seen from behind, one hand on the railing, looking at the sunrise. A sliver of the balcony's potted plants on the left. Peaceful, quiet, warm morning light. Flat kid-book illustration, no text.
```

### 3.2 `scene-01-morning.png`
```
Interior of Julia's bedroom at 7:30 am. Julia sitting up in bed with messy hair and a sleepy half-closed-eyes expression, cream blanket pulled up. Biscuit the small brown dog curled asleep on her pillow next to her. Night-stand with a yellow retro alarm clock showing 7:30 (bells on top). Soft morning light streaming diagonally through a window with sheer curtains. Posters on wall (abstract shapes — no text). Cozy slightly whimsical kid-book style. Wide composition.
```

### 3.3 `scene-02-breakfast.png`
```
Family kitchen scene at breakfast. Round wooden table with a pancake stack, a honey jar, a plate of grilled sausages, cups of tea. Around the table: Mum Olga serving pancakes with her wooden spoon, Dad Pavel with a coffee cup, Max in green dinosaur pyjamas with ONE sneaker on his right foot and a bare left foot, and Julia eating pancakes with a fork. Warm morning sunlight through the kitchen window. Pot plants on the windowsill. Flat kid-book style. No text. Wide composition.
```

### 3.4 `scene-03-cat-sausage.png`
```
Comic chaos moment, frozen in time. Breakfast table from side angle. Pepper the fat orange tabby cat caught MID-LEAP onto the table — paws spread wide, body stretched, mouth clamped on a sausage that is lifting off the plate. Mum (left) mouth open in a surprised scream. Julia (right) has dropped her fork mid-air (fork drawn in motion, slightly blurred). Dad (back) is laughing with his hand on his belly. Max (far right) wide-eyed, pointing. Three or four comic motion lines around the cat. Flat kid-book style, no text. Wide composition.
```

### 3.5 `scene-04-school.png`
```
Classroom at 11:00 am. Julia and Emma (red-haired girl in a mint-green hoodie) sitting next to each other at a shared wooden desk, both facing camera. Emma drawing a big curly flower in her open copybook. Julia glancing at the big round wall clock (showing 11:00) with a hungry expression, hand on her stomach. In the back row: Vova (dark-haired boy in a navy sweater) asleep with his head on his folded arms. In the middle row: three boys quietly throwing a white paper airplane. In the front: Mrs. Green (teacher, grey hair in a soft bun, round glasses, cream blouse) writing abstract squiggles on a green chalkboard. Flat kid-book style. No readable text. Wide composition.
```

### 3.6 `scene-05-cafe.png`
```
Interior of a bright "Pink Café" at 1:30 pm. Julia and Emma seated at a small round marble table by a tall window, both laughing. Two tall glasses of strawberry-pink milkshakes with whipped cream and cherries. A plate of pink pancakes between them. Pink velvet booth seat behind them. Potted monstera plant on the left. Soft late-afternoon light streaming through the window — a slice of street visible outside with cars and a bakery across the road. Flat kid-book style. No text. Wide composition.
```

### 3.7 `scene-06-shopping.png`
```
Interior of a gift shop, warm indoor lighting. Shelves full of wrapped presents in pastel colors. Julia reaching up to the middle shelf, lifting a cream gift box with a bright yellow bow. Emma next to her holding a bouquet of pink peonies wrapped in brown paper. Both looking excited. Shop window on the right shows a soft late-afternoon street outside with a lamp just turning on. Flat kid-book style. No text. Wide composition.
```

### 3.8 `scene-07-evening-homework.png`
```
Julia's bedroom at 8:00 pm. Julia sitting at a small white desk with her English textbook open, a half-full glass of milk, a yellow pencil in her hand, concentrating. Biscuit the brown dog curled asleep at her feet. Window above the desk shows a dark deep-blue night sky with a bright crescent moon and a few stars. Warm yellow light from a desk lamp spilling across the pages. Cozy, calm. Flat kid-book style. Wide composition.
```

### 3.9 `scene-08-dream-london.png`
```
Dream sequence, soft dreamy haze. Julia (slightly older — maybe 15, same light brown hair, mustard sweater) standing confidently in front of Big Ben and a red London double-decker bus on Westminster Bridge. She is holding a large art portfolio under her arm. London Eye visible in the distance. A few fluffy clouds in the sky — one has a tiny pink heart inside, another has a tiny yellow star. Soft pastel palette (not harsh). Flat kid-book style. No text. Wide composition.
```

---

## 📊 4. THEORY VISUALS (2 PNG, 1024×1024)

### 4.1 `theory-tense-timeline.png`
```
Horizontal timeline arrow going left to right, drawn as a thick cream band with navy outline. 3 equal sections, each marked with a small pictogram ABOVE the band (no text — the HTML will add captions):
- LEFT section: a crescent moon with sleep-Zzz
- CENTER section: a bright sun directly overhead
- RIGHT section: a sunrise with 3 sparkle stars
Below the band, a small arrow curving back to the LEFT labelled with pictogram of a book bookmark (= past), a yellow clock in the CENTER (= now), and a tiny crystal ball on the RIGHT (= future). Soft palette, flat kid-book style. Pure white background. NO TEXT.
```

### 4.2 `theory-will-vs-going-to.png`
```
Split card, 1024×1024, vertical dividing line down the middle.
LEFT HALF (sun-yellow background tint): a thought bubble with a glowing lightbulb inside and 3 sparkle stars around it.
RIGHT HALF (sky-blue background tint): a clipboard with a to-do list of 3 ticked items (just checkmarks, no words), and a small calendar page in the corner with one date circled in red.
Thin cream dividing line between halves. NO TEXT. Flat kid-book style. HTML will add the "WILL" / "GOING TO" labels on top.
```

---

## 📦 5. VOCAB CAPSULE PNGs (15 PNG, 512×512 or 1024×1024, pure white bg)

Короткий промт на каждое — все в одном стиле (см. CANON STYLE), флат, pure white bg, no text:

| # | file | prompt (short) |
|---|---|---|
| 1 | `vocab/alarm-clock.png` | Yellow retro alarm clock showing 7:30, two bells on top, no face. Flat kid-book style. |
| 2 | `vocab/half-past.png` | Clock face showing 7:30, the lower half highlighted in soft sun-yellow with a thin arc. Simple, iconographic. |
| 3 | `vocab/cereal.png` | Cream bowl of corn-flake cereal with milk, a silver spoon sticking out of the bowl. Flat kid-book style. |
| 4 | `vocab/pancake.png` | Stack of 3 golden pancakes with butter melting on top and a drizzle of honey. Flat kid-book style. |
| 5 | `vocab/sausage.png` | One grilled brown sausage with grill marks on a small cream plate. Flat kid-book style. |
| 6 | `vocab/fork.png` | Single silver dinner fork, isolated. Flat kid-book style. |
| 7 | `vocab/board.png` | Green classroom chalkboard with a wooden frame and a chalk shelf at the bottom. Blank surface. Flat kid-book style. |
| 8 | `vocab/copybook.png` | Open school copybook with pale blue lines and a red margin line on the left page. Blank. Flat kid-book style. |
| 9 | `vocab/milkshake.png` | Tall glass of pink strawberry milkshake with striped straw, whipped cream and a cherry. Flat kid-book style. |
| 10 | `vocab/present.png` | Cream gift box with a bright pink ribbon and a big bow on top. Flat kid-book style. |
| 11 | `vocab/mark.png` | A blank sheet of school paper with a bright red "5" (just the digit) written in the top-right corner in handwritten style. Flat kid-book style. |
| 12 | `vocab/promise.png` | Two pinky fingers hooked together (pinky promise), light skin, slightly cartoon proportions. Soft shadow. Flat kid-book style. |
| 13 | `vocab/plan.png` | A clipboard with a to-do list of 3 ticked items (just checkmarks, no words), a yellow pencil clipped to the top. Flat kid-book style. |
| 14 | `vocab/dream.png` | A fluffy white cloud with three "Zzz" letters and a tiny galaxy with stars inside the cloud. Flat kid-book style. |
| 15 | `vocab/tomorrow.png` | A single calendar page with the next-day square circled in red marker (the current day square has a small cross on it). No words, just the square grid. Flat kid-book style. |

---

## 🧪 6. SMOKE / QA (после каждых 8-10 рендеров)

1. **Characters consistency check**: открыть все 8 char-*.png рядом → не должно быть "Julia стала старше / Mum с другим цветом волос / Dad без очков в одном варианте".
2. **Palette drift check**: случайный scene + случайный sticker → цвета сан/sky/pink не разъехались в сторону оранжевого/бирюзового.
3. **Outline weight check**: все persons одинаковой толщины outline (2-3px, не 1px как иконки, не 5px как detail).
4. **"NO TEXT" check**: ни одна картинка не должна иметь букв/цифр/надписей/логотипов.

Если персонаж "уехал" — regen с добавлением reference: "Use the same Julia / Mum / Dad / Max / Pepper / Biscuit from the previous image in this chat. Same hair, same clothes, same proportions."

---

## 📂 Файловая структура после рендера

```
julia-big-monday/
  index.html           ← уже готов
  10_image_prompts.md  ← этот файл
  img/
    char-julia.png
    char-mum.png
    char-dad.png
    char-max.png
    char-cat-pepper.png
    char-dog-biscuit.png
    char-grandma-lara.png
    char-grandpa-petya.png
    sticker-clock-730.png
    sticker-pancake.png
    sticker-cat-wink.png
    sticker-milkshake.png
    sticker-book.png
    sticker-balloon.png
    sticker-moon.png
    sticker-crystal-ball.png
    sticker-star.png
    sticker-airplane.png
    scene-00-hero.png
    scene-01-morning.png
    scene-02-breakfast.png
    scene-03-cat-sausage.png
    scene-04-school.png
    scene-05-cafe.png
    scene-06-shopping.png
    scene-07-evening-homework.png
    scene-08-dream-london.png
    theory-tense-timeline.png
    theory-will-vs-going-to.png
    vocab/
      alarm-clock.png
      half-past.png
      cereal.png
      pancake.png
      sausage.png
      fork.png
      board.png
      copybook.png
      milkshake.png
      present.png
      mark.png
      promise.png
      plan.png
      dream.png
      tomorrow.png
```

**Итого:** 8 characters + 10 stickers + 9 scenes + 2 theory + 15 vocab = **44 PNG**.
