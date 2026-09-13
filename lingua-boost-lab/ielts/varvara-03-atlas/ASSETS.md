# varvara-03-atlas · asset list

Урок работает целиком: 11 reading текстов + 6 listening треков (аудио уже вшито, MP3 сгенерены через edge-tts). Всё, что ниже — украшательства.

## Уже готово

| # | путь | статус | назначение |
|---|------|--------|------------|
| 1 | `assets/audio/l-01-concert.mp3` … `l-06-tour.mp3` | **готово** — 6 файлов ~1.4 MB суммарно | listening треки, вшиты `<audio>` в карточки L-01…L-06 |
| 2 | `assets/audio/_gen.py` | готово | скрипт edge-tts, чтобы пересгенерить любой трек (`py -3 _gen.py`) |
| 3 | inline SVG · L-03 map (Elmswood plan) | готово | 5 пронумерованных зон + компас в HTML |
| 4 | inline SVG · R-10 flow-chart (chocolate) | готово | процесс обработки какао в HTML |
| 5 | `../varvara-02-tour/assets/img/hero-culture-shapes-us.png` | reuse | hero-фон всей страницы |

## Голоса edge-tts (по трекам)

| track | voice | тема | длительность |
|---|---|---|---|
| L-01 | en-GB-SoniaNeural | community concert venue change | ~40 с |
| L-02 | en-GB-RyanNeural | tutor · 4 university modules | ~45 с |
| L-03 | en-GB-LibbyNeural | Elmswood Botanic Gardens tour | ~55 с |
| L-04 | en-GB-SoniaNeural | Camden language course booking | ~55 с |
| L-05 | en-GB-LibbyNeural | Céide Fields Neolithic lecture | ~55 с |
| L-06 | en-GB-MaisieNeural | Sunday walking tour phone enquiry | ~35 с |

Пересгенерить трек: правь текст в `_gen.py`, запусти `py -3 _gen.py`, все 6 файлов перезапишутся.

## Опциональные картинки (для украшения)

Не обязательные — урок без них полноценный.

### 1. Hero-иллюстрации к 11 reading текстам

Формат: **1200×675 (16:9), PNG**. Стилистика — минимализм, тёмный фон #0F151A, teal + gold акценты.

| card | topic | prompt (короткий) |
|---|---|---|
| R-01 | Octopus cognition | "Underwater dramatic photo of an octopus with two arms rotating the lid of a glass screw-top jar containing a live crab, deep blue background, editorial macro" |
| R-02 | Ottoman Selimiye Mosque | "Interior wide-angle photo of Selimiye Mosque in Edirne, Turkey, dome with 999 windows, warm golden light beams" |
| R-03 | Sarajevo reconstruction | "Editorial photo of a Sarajevo façade showing wartime shrapnel scars framed and preserved as memorial, muted colours" |
| R-04 | Medici patronage | "Detail of Verrocchio's terracotta bust of Cosimo de' Medici on plain grey museum background" |
| R-05 | Coffee & sleep | "Overhead flat lay of a coffee cup with an EEG sleep-line graph rising from steam, dark moody kitchen surface" |
| R-06 | Nordic film composers | "Split-screen editorial portrait of three film composers at work — a Lithuanian power plant control room, a mixing desk, a full orchestra recording session" |
| R-07 | Iceberg calving | "Aerial drone photo of a large iceberg mid-rotation in Arctic water, blue-green ice, dramatic light, small tsunami wave visible" |
| R-08 | Silk Road caravanserai | "Wide-angle photo of a Central Asian caravanserai courtyard at dusk, camels resting, warm orange lighting from arched cells" |
| R-09 | Solar sail LightSail 2 | "Space photograph of a Mylar solar sail unfolded in low Earth orbit, sunlight bouncing off, dark space background, small shoebox spacecraft visible" |
| R-10 | Chocolate processing | "Overhead photo of split cacao pods with wet white beans and pulp on wooden fermenting box, tropical plantation background" |
| R-11 | Blue whale acoustics | "Underwater side-view of blue whale with subtle overlay of sonar hydrophone waveforms in accent teal, deep ocean" |

Куда класть → `assets/img/r-01.png` … `r-11.png`. Затем добавляй `<img class="hero-img">` в начало каждого `.passage` (если хочешь).

### 2. Иллюстрации к listening (по желанию)

| track | prompt |
|---|---|
| L-01 | "Photo of a Victorian British village hall with 'concert tonight' sandwich board" |
| L-02 | "Overhead photo of a university tutor's desk with four coloured module folders labelled" |
| L-03 | "Aerial photo of a Victorian palm house glasshouse in a botanic garden" |
| L-04 | "Photo of language school reception desk with course brochures" |
| L-05 | "Aerial photo of Céide Fields Neolithic stone walls under peat, Irish Atlantic coast" |
| L-06 | "Photo of Trafalgar Square north lion at 10 a.m. with a small tour group gathered" |

### 3. Замена L-03 SVG-плана на нарисованную карту

Если хочешь красивее — сгенерь **plan-elmswood.png** (1200×900) под Wes-Anderson-style top-down site plan (детальный prompt был в предыдущей версии этого файла).

## Регенерация аудио

```powershell
cd "C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\01_Сайт New Generation — сайт, Lab, кабинет\site-public-clean\lingua-boost-lab\ielts\varvara-03-atlas\assets\audio"
py -3 _gen.py
```

Все 6 треков перезапишутся за ~30-40 сек. Затем `git add . && git commit && git push`.
