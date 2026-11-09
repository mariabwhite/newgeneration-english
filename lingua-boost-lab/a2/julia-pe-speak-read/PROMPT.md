# 🏃 Julia · PE & Sports · Speaking + Reading — PROMPT

**Статус:** черновик промта. Книга-источник A2 ждёт Марию.
**Slug:** `a2/julia-pe-speak-read/`
**Позиция:** после `julia-bubble-wishes` / `julia-big-recap`.

**Главный фокус:** SPEAKING + READING (не грамматика-гринд). Тема — физкультура/спорт. Будущие времена остаются как фоновая грамматика («скажи что будет на спортивном дне», «расскажи план тренировки») — не 10 подсекций теории, а 2–3 коротких speaking-cue + reading passage в будущем.

---

## 1 · Что было до

- `julia-bubble-wishes` — все 10 будущих отрендерены теоретически (toolkit)
- `julia-big-recap` — повтор всех тем
- **Сейчас надо не повторять теорию, а катать её устно + в чтении** на понятной спортивной теме

---

## 2 · Структура — Speaking + Reading canon

```
hero: 🏃 PE Day · talk about it, read about it
cast-strip (Julia + PE teacher + 2 классника + Barsik в костюме мяча)

tabs: 🎙 Speaking · 📖 Reading · 📦 Vocab Capsule · 📝 Workbook

sec-00  Warm-up · 🎙 Picture Talk (3 кадра, 1 мин каждая)
         • flashcard PE lesson · flashcard race · flashcard team game
         • Юля смотрит → «What are they doing? What will happen next?»
         • model answer прячется под кнопкой — открывается после попытки

sec-01  🎙 Speaking Part 1 · «About me & sports»
         • 8 interview-style вопросов (A2 Cambridge-style)
         • каждый с record-button + model answer + 3 sentence stems
         • примеры: What sports do you do at school? · What are you going to do next PE lesson?
           · Which sport do you hope to try one day? · Shall we go running after school? Why?

sec-02  🎙 Speaking Part 2 · «Describe a photo» (long turn 1 min)
         • 1 photo card (школьный спортивный день)
         • prompts: who/where/what doing/what will happen next/how they feel
         • model answer 45–60 sec (audio)

sec-03  🎙 Speaking Part 3 · «Plan the sports day together» (role-play)
         • Julia + partner planning next week's sports day
         • 8 cue-cards: schedule / teams / equipment / snack / weather plan / after-party
         • full dialogue model (Julia ↔ friend) с кнопкой ▶

── bridge ──

sec-04  📖 Reading Part A · Pre-reading (audio-first, red line)
         • Play story (narration + sound FX: whistle · crowd · sneakers)
         • 5 Qs BEFORE reading:
           — Where is the story?
           — Who is the main character?
           — What time of day?
           — What sport?
           — How does it end?
         • Юля угадывает, ответы заморожены до Part B

sec-05  📖 Reading Part B · The text + T/F/NS
         • 180–220 слов, A2+
         • сюжет: Julia готовится к школьному sports day — тренируется всю неделю, в день X бежит эстафету
         • время в тексте: present + future mix (will / going to / be about to / Future Perfect by the race)
         • 8 T/F/NS вопросов + 5 vocab-in-context
         • MCQ options shuffle seed 42

sec-06  📖 Reading Part C · Cloze
         • тот же текст с 10 gap-fill (future forms + sports vocab)
         • drag-drop или type-input
         • auto-check + score

sec-07  📦 Vocab Capsule · 20 слов (click-to-hear + RU + example + spelling) ← ОБЯЗАТЕЛЬНО
         (словарь из §5)

sec-08  📝 Workbook mini · 2 задания из книжки (парафраз, не копия)

wrap-up «See you on the finish line, Julia»
```

**Баланс:** Speaking ~45% · Reading ~35% · Vocab ~15% · Workbook ~5%.

---

## 3 · Speaking механика · что уже умеет Lab

Проверить в `julia-*`:
- record-button + play-back (Media Recorder API) — если есть, использовать; если нет, кнопка «answered aloud ✓» + сравнить с model
- model answer под «show model» кнопкой (не сразу открыт)
- sentence stems (3 × каркас): "In our school, we usually…" / "Next week, I'm going to…" / "I'd love to try…"
- live-sync teacher/student сцепка через `lab-sync.js` (teacher видит нажатия student'а)

Если record-button не канон — делаем click-to-hear model + чек-лист самопроверки. Не изобретать.

---

## 4 · Reading passage · черновой сюжет

**Title:** Julia's First Sports Day

**Длина:** 180–220 слов, Flesch A2.

**Mini-sketch:**
> It is Monday morning. Julia is at school. Next Friday is the big sports day. Julia is going to run the 60 metres and jump into the long jump pit. Every day this week she is practising with her PE teacher, Mr Brown. By Friday morning she will have run twenty short sprints.
> "Shall we practise one more time?" asks her friend Lily. "Yes, let's," says Julia.
> On Friday, the sun shines. The whistle is about to blow. Julia's heart is beating fast. "I think I'll win!" she whispers. She is going to try her best.
> When the whistle blows, Julia runs. The wind is in her hair. She doesn't win the gold medal — Lily does. But Julia gets the silver medal. "I'm so happy!" she says. "Next year I will run even faster. One day I'd like to run in the Olympics."

→ 8 T/F/NS · 5 vocab-in-context · 10 cloze. Будущие времена как естественный фон.

---

## 5 · Vocab Capsule · 20 простых A2-слов (из §4 + warm-ups)

| EN | RU | example |
|---|---|---|
| to run | бегать | She will run the 60 metres on Friday. |
| to jump | прыгать | Julia is going to jump in the long jump. |
| to race | бежать на скорость | Shall we race to the gate? |
| to practise | тренироваться | Every day this week she is practising. |
| to throw | бросать | Throw the ball to Lily! |
| to catch | ловить | I hope I will catch it. |
| to kick | пинать | He's about to kick the ball. |
| to win | выиграть | I think our team will win. |
| to lose | проиграть | Nobody likes to lose. |
| ball | мяч | The red ball is in the net. |
| team | команда | Our team is going to play on Saturday. |
| game | игра | The game starts at 3. |
| match | матч | The match is about to begin. |
| score | счёт | What's the score, 2–1? |
| goal | гол | She scored a goal! |
| whistle | свисток | The teacher is about to blow the whistle. |
| coach | тренер | Our coach says we're training at 4. |
| PE lesson | урок физкультуры | Our next PE lesson is on Wednesday. |
| sports day | спортивный праздник | On sports day I will run the 60 metres. |
| medal | медаль | I hope I will win a medal one day. |

---

## 6 · Audio / image pipeline

**Voices (edge-tts):**
- `en-US-AriaNeural` — Julia narrator (rate -6%)
- `en-GB-SoniaNeural` — Mr Brown / teacher
- `en-US-GuyNeural` — Lily (child alt)
- Model-answer voices чётко отделены от narrative

**Sound FX для Reading Play story:** whistle, crowd cheer, sneaker squeak, stopwatch click. Найти бесплатно (Freesound CC0).

**Soundtrack track** (`feedback_lesson_track_real_song_not_ambient`):
`yt-dlp "ytsearch1:school sports day song kids upbeat clean" -x --audio-format mp3`
Dev-fallback: "Eye of the Tiger" (instrumental), "Happy" (Pharrell), "Can't Hold Us".

**Images** (`reference_image_generation_capabilities`):
- hero + cast → Playwright → ChatGPT Марии (DALL-E 3)
- 3 flashcards для Picture Talk + 1 photo card для Speaking Part 2
- Ex-sticker PNG канон (121/79/176 px, абсолют, dual drop-shadow glow)

**Retry 403** (`reference_edge_tts_403_retry`): удалить 0-byte, sleep 5, retry skip existing. Slug cap 30 (`julia-pe-speak-read` = 20 ✓).

---

## 7 · Red lines сводкой

- [ ] Vocab Capsule в конце (click-to-hear + RU + example + spelling type-input)
- [ ] MCQ options shuffle seed 42
- [ ] Reading audio-first (3 части: pre-Q → text+T/F/NS → cloze)
- [ ] Real song soundtrack (не ffmpeg-ambient)
- [ ] Ex-sticker PNG канон
- [ ] edge-tts retry 403
- [ ] Topic в кабинете ≤ 40 символов
- [ ] 1 карточка/урок в кабинете
- [ ] Teacher-mode флаги: `teacher=on` / `teacher=1` / `role=teacher`
- [ ] Модель-answer под кнопкой «show model», не раскрыт сразу — иначе Юля читает вместо говорит
- [ ] Текст passage — парафраз из учебника, не копия

---

## 8 · Открытые вопросы к Марии

1. Какая книжка — A2 unit sports/PE? (Spotlight 5/6 · Family and Friends 4 · Prepare 1/2 · Project 3/4 · что-то другое?)
2. Юля в каком классе / какой спорт у неё в школе (бег, прыжки, футбол, плавание)?
3. Есть ли у неё фаворит-спортсмен или команда — упомянуть в tasks?
4. Record-button для speaking в Lab уже канон, или делаем click-to-hear model + самопроверка?
5. Premium gate или сразу публичный?
6. Soundtrack trackname?

---

## 9 · Кабинет — короткий topic/homework

```
topic:                 🏃 PE Day · speaking + reading
interactive_title:     🏃 Открыть · PE Day
homework_module_title: 🏃 Повторить · reading + 20 слов
```
