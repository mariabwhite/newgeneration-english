# TTSMP3 scripts for katya-06-book5-power

Каждый блок — отдельный копипаст на https://ttsmp3.com

**Голоса:** British Amy (женский) и British Brian (мужской).
**Формат:** `[speaker:Amy]` перед каждой строкой.
**Что делать:**
1. Открой https://ttsmp3.com
2. Вставь текст блока
3. Убедись что «Amy (British English)» или «Brian» выбран
4. Нажми «Read» → потом «Download MP3»
5. Сохрани в `assets/audio/` под указанным именем

---

## eng-tts-ex-listen-01.mp3

```
[speaker:Amy]
She told me a beautiful story about her grandmother.
```

---

## eng-tts-ex-listen-02.mp3

```
[speaker:Brian]
Please say hello to your mother from me.
```

---

## eng-tts-ex-listen-03.mp3

```
[speaker:Amy]
Don't tell me lies!
```

---

## eng-tts-ex-listen-04.mp3

```
[speaker:Brian]
Harry said nothing when Snape looked at him.
```

---

## eng-tts-ex-listen-05.mp3

```
[speaker:Amy]
I always tell my friends the truth.
```

---

## eng-tts-ex-listen-06.mp3

```
[speaker:Amy]
My grandmother speaks three languages.
```

---

## eng-reading-da-fireside.mp3

Диалог у камина в гостиной Гриффиндора — Гермиона, Гарри, Рон обсуждают ДА.

```
[speaker:Amy]
That night in the Gryffindor common room, Hermione told Harry that they had to be careful — Umbridge was watching everyone.
[speaker:Brian]
Harry said nothing for a while.
[speaker:Brian]
Then Ron asked him about the D A — was it really worth the risk?
[speaker:Amy]
They talked quietly until midnight.
[speaker:Brian]
In the end, Harry spoke with a calm voice.
"We stay. We fight."
```

---

## Bonus · Modal Verb Cards (6 audio prompts)

Опционально, чтобы можно было слушать modal-карточки:

### eng-modal-01-must-not.mp3
```
[speaker:Brian]
Under Umbridge, students must not gather in groups of three or more. Would you break that rule?
```

### eng-modal-02-have-to.mp3
```
[speaker:Amy]
In your school you have to wear a uniform. Is that a fair rule?
```

### eng-modal-03-should.mp3
```
[speaker:Brian]
Harry should tell Dumbledore about his dreams. Do you agree, or should he keep them secret?
```

### eng-modal-04-can.mp3
```
[speaker:Amy]
In the D A, everyone can cast a full Patronus by the end. Which real skill can you teach a friend in a month?
```

### eng-modal-05-could.mp3
```
[speaker:Brian]
Harry could have stayed at the Dursleys and been safe. Was joining the fight worth it?
```

### eng-modal-06-had-to.mp3
```
[speaker:Amy]
In detention, Harry had to write "I must not tell lies" with a blood-quill. Have you ever had to do something you knew was wrong?
```

---

## Лимиты и советы

- TTSMP3: **3000 знаков в сутки** бесплатно
- Все 13 файлов выше = ~1200 знаков суммарно → влезают в один день
- Если TTSMP3 не хочет — альтернатива: https://ttstool.com (тоже Amy/Brian, тот же движок Polly)
- Amy = British female (мягкий), Brian = British male (низкий) — оба отличные
- «D A» пиши раздельно, иначе Polly читает как «да»

## Что делать после скачивания

1. Все mp3 положи в `assets/audio/` рядом с этой инструкцией
2. В HTML замени `SpeechSynthesisUtterance` на реальные `<audio src="assets/audio/xxx.mp3">` — скажи «переделай на mp3», сделаю за минуту
