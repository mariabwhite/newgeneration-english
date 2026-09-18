# varvara-04-listening-pack · asset list

Урок работает целиком: 5 listening треков (все en-GB, edge-tts) + 2 writing блока с inline SVG pie-chart и Band 7.5–8 model answers.

## Аудио

| # | путь | голос(а) | тема | task type | длит. |
|---|------|----------|------|-----------|-------|
| L-01 | `assets/audio/l-01-museum-booking.mp3` | en-GB-Sonia + en-GB-Ryan (dialogue) | British Museum · private tour booking | Note / Form completion (10 gaps) | ~1:15 |
| L-02 | `assets/audio/l-02-outreach-programmes.mp3` | en-GB-Libby | Ashfield Regional Art Museum · 4 outreach programmes | Table completion (7 gaps) | ~0:55 |
| L-03 | `assets/audio/l-03-autumn-exhibitions.mp3` | en-GB-Maisie | Gallery Round-up · 5 autumn exhibitions | Matching (5 items → A–E) | ~1:00 |
| L-04 | `assets/audio/l-04-tutorial-medici.mp3` | en-GB-Ryan + en-GB-Sonia (dialogue) | Dissertation tutorial · Medici patronage | MCQ 3-option (6 questions) | ~1:20 |
| L-05 | `assets/audio/l-05-caravanserai-lecture.mp3` | en-GB-Libby | Silk Road satellite archaeology · caravanserai | Sentence completion (10 gaps) | ~1:25 |

## Изображения

Hero-фон карточки берётся из `../varvara-02-tour/assets/img/museum-interior.png` (reuse, никаких новых картинок). Inline SVG для двух pie-chart сгенерены прямо в HTML — файлов не нужно.

## Регенерация аудио

```powershell
cd "C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\01_Сайт New Generation — сайт, Lab, кабинет\site-public-clean\lingua-boost-lab\ielts\varvara-04-listening-pack\assets\audio"
py -3 _gen.py
```

Пересгенерить один трек: `ONLY=l-01-museum-booking.mp3 py -3 _gen.py`.

Диалоги (L-01, L-04) собираются через ffmpeg concat из per-turn edge-tts файлов + 0.35 с тишины между репликами. ffmpeg должен быть в PATH (у Марии установлен: `C:\Users\Whitenois\bin\ffmpeg.exe`).

## Модельные ответы (обязательные)

- Writing Task 1 · Pie chart · ~205 слов · Band 7.5–8 · Details `📖 Show Band 7.5–8 model answer` в секции `#sec-w1`.
- Writing Task 2 · Discuss+opinion · ~305 слов · Band 7.5–8 · Details в секции `#sec-w2`. Позиция — hybrid (residents free, tourists pay).

Оба модели раскрываются только после того, как Варя напишет свой draft — в textarea со счётчиком слов и красной подсветкой если <150 / <250.

## Что открыто на потом

- 6-й трек с short-answer (Section 4 alternative) — если добавим 05-й lesson.
- Bar-chart / line / process-diagram Task 1 — отдельный урок.
- Speaking pack (Part 1/2/3 с cue cards) — отдельный урок.
