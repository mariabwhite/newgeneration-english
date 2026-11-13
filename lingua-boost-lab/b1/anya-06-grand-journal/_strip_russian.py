"""Strip Russian from anya-06 index.html — English-only lesson.
- Remove every <span class="ru">...</span> block
- Shrink vcap-item CSS grid from 3 cols to 2 cols
- Replace a dictionary of common RU phrases → EN
"""
import re, os, io

HERE = os.path.dirname(__file__)
TARGET = os.path.join(HERE, "index.html")

with io.open(TARGET, "r", encoding="utf-8") as f:
    html = f.read()

orig_len = len(html)

# 1. Remove every <span class="ru">...</span>
html = re.sub(r'<span class="ru">[^<]*</span>', '', html)

# 2. Shrink vcap-item CSS grid to 2 cols (icon + en)
html = html.replace(
    '.vcap-item{display:grid;grid-template-columns:36px 1fr 1fr;gap:8px;align-items:center;background:rgba(6,24,51,.4);border:1px solid var(--card-border);border-radius:10px;padding:8px 10px}',
    '.vcap-item{display:grid;grid-template-columns:36px 1fr;gap:8px;align-items:center;background:rgba(6,24,51,.4);border:1px solid var(--card-border);border-radius:10px;padding:8px 10px}'
)
html = html.replace(
    '.vcap-item{grid-template-columns:28px 1fr 1fr}',
    '.vcap-item{grid-template-columns:28px 1fr}'
)

# 3. Dictionary of common RU phrases → EN
PAIRS = [
    # Overview / meta
    ('60-80 минут · 11 sections · 8 станций + overview + big vocab + finale',
     '60-80 min · 11 sections · 8 stations + overview + big vocab + finale'),
    ('read first', 'read first'),
    ('0 · правила путешествия + легенда цветов + предметы в рюкзак',
     '0 · travel rules + color legend + items for your backpack'),
    ('(факты, привычки)', '(facts, habits)'),
    ('(прямо сейчас, arrangement)', '(right now, arrangement)'),
    ('(while / when)', '(while / when)'),
    ('(prediction / promise)', '(prediction / promise)'),
    ('(plan + evidence)', '(plan + evidence)'),
    ('(+ for / since)', '(+ for / since)'),
    ('(past habit NOT now)', '(past habit NOT now)'),

    # Game bars
    ('❤️ HP · health', '❤️ HP · health'),
    ('⚡ XP · experience', '⚡ XP · experience'),
    ('старт 100 · −10 за ошибку · +20 за артефакт',
     'start 100 · −10 per mistake · +20 per artifact'),
    ('+5 за правильный ответ · до финала 400 XP',
     '+5 per correct answer · final goal 400 XP'),
    ('🎁 8 артефактов · собирай по пути', '🎁 8 artifacts · collect them on the way'),
    ('🎨 6 colors · 8 tenses in the journal', '🎨 6 colors · 8 tenses in the journal'),

    # TOC (keep EN labels)

    # Station headers · sub lines
    ('1 · Anya садится в поезд · первая остановка у гавани · brass seller',
     '1 · Anya boards the train · first stop at the harbour · brass seller'),
    ('2 · поезд останавливается у рынка · grandma waiting with the basket',
     '2 · the train stops at the market · grandma waiting with the basket'),
    ('3 · поезд останавливается у утёса · ghost cat is waiting',
     '3 · the train stops at the cliff · ghost cat is waiting'),
    ('4 · поезд останавливается в долине храмов · the guide is waiting',
     '4 · the train stops in the temple valley · the guide is waiting'),
    ('5 · поезд останавливается у старой почты · postman has your letters',
     '5 · the train stops at the old depot · postman has your letters'),
    ('6 · поезд въезжает в её родной город · Masha встречает с кофе',
     '6 · the train enters her hometown · Masha is waiting with coffee'),
    ('7 · поезд останавливается в Hollow · Jack-o\'-lantern светится на платформе',
     '7 · the train stops in Hollow · a Jack-o\'-lantern glows on the platform'),
    ('8 · поезд возвращается на станцию старта · круг замкнулся · 5 телескопов на закате',
     '8 · the train returns to the start · full circle · 5 telescopes at sunset'),
    ('9 · весь vocab года в одном месте · 20 type-in + финальная песня',
     '9 · all year vocab in one place · 20 type-in + song finale'),
    ('10 · положи 8 артефактов перед собой · на каждый — одна карта',
     '10 · put all 8 artifacts in front of you · one cue card each'),

    # Section tags
    ('audio-first · 4 forms', 'audio-first · 4 forms'),

    # Audio captions
    ('~140 слов · прослушай 2 раза ДО чтения · закрой текст рукой',
     '~140 words · listen 2 times BEFORE reading · cover the text with your hand'),
    ('~160 слов · 20+ irregular verbs in context',
     '~160 words · 20+ irregular verbs in context'),
    ('~150 слов · Past Continuous + Past Simple',
     '~150 words · Past Continuous + Past Simple'),
    ('~160 слов · 12+ Present Perfect forms',
     '~160 words · 12+ Present Perfect forms'),
    ('~110 слов · used to · habit then vs now',
     '~110 words · used to · habit then vs now'),
    ('~130 слов · Present Simple + Present Continuous',
     '~130 words · Present Simple + Present Continuous'),
    ('~100 слов · Past Simple + Past Continuous · seasonal',
     '~100 words · Past Simple + Past Continuous · seasonal'),
    ('~170 слов · все 5 будущих форм + time clauses',
     '~170 words · all 5 future forms + time clauses'),

    # Section chips / headers
    ('🚂 Train arrives 06:12 · brass seller is waiting',
     '🚂 Train arrives 06:12 · brass seller is waiting'),
    ('🚂 Train arrives 07:40 · grandma + basket', '🚂 Train arrives 07:40 · grandma + basket'),
    ('🚂 Train arrives 09:00 · ghost cat on the step',
     '🚂 Train arrives 09:00 · ghost cat on the step'),
    ('🚂 Train arrives 10:30 · guide with old map',
     '🚂 Train arrives 10:30 · guide with old map'),
    ('🚂 Train arrives 12:00 · old postman smiling',
     '🚂 Train arrives 12:00 · old postman smiling'),
    ('🚂 Train arrives 14:00 · Masha at Central Station',
     '🚂 Train arrives 14:00 · Masha at Central Station'),
    ('🚂 Train arrives 17:00 · Halloween · witch on broom',
     '🚂 Train arrives 17:00 · Halloween · witch on broom'),
    ('🚂 Train returns 19:30 · sunset · 5 telescopes',
     '🚂 Train returns 19:30 · sunset · 5 telescopes'),

    # Audio-first parts
    ('🎧 PART A · Listen first (audio-first)', '🎧 PART A · Listen first (audio-first)'),
    ('🎧 PART A · Listen first', '🎧 PART A · Listen first'),
    ('👂 Pre-reading listening · 5 Qs (по звуку)', '👂 Pre-reading listening · 5 Qs (by ear only)'),
    ('👂 Pre-reading · 5 Qs', '👂 Pre-reading · 5 Qs'),
    ('👂 Pre-reading · 4 Qs', '👂 Pre-reading · 4 Qs'),
    ('📖 PART B · Read the story', '📖 PART B · Read the story'),
    ('⌨️ PART C · Cloze · put the verb in the right form',
     '⌨️ PART C · Cloze · put the verb in the right form'),
    ('⌨️ PART C · Cloze · 10 irregular verbs', '⌨️ PART C · Cloze · 10 irregular verbs'),
    ('⌨️ PART C · Cloze · while / when', '⌨️ PART C · Cloze · while / when'),
    ('⌨️ PART C · Cloze · Present Perfect', '⌨️ PART C · Cloze · Present Perfect'),
    ('⌨️ PART C · Cloze · used to', '⌨️ PART C · Cloze · used to'),
    ('⌨️ PART C · Cloze · Pres S vs Pres C', '⌨️ PART C · Cloze · Pres S vs Pres C'),
    ('⌨️ PART C · Cloze · mixed past', '⌨️ PART C · Cloze · mixed past'),
    ('⌨️ PART C · Cloze · 5 futures', '⌨️ PART C · Cloze · 5 futures'),

    # Theory boxes
    ('🧭 Theory · was / were + Past Simple regular',
     '🧭 Theory · was / were + Past Simple regular'),
    ('Past of «to be»', 'Past of "to be"'),
    ('finished action in the past', 'finished action in the past'),
    ('3 sounds of -ed', '3 sounds of -ed'),
    ('3 звука окончания:', '3 endings:'),
    ('/t/ after p,k,f,s,sh,ch — ', '/t/ after p,k,f,s,sh,ch — '),
    (' · /d/ after voiced — ', ' · /d/ after voiced — '),
    (' · /ɪд/ after t,d — ', ' · /ɪd/ after t,d — '),
    ('🧩 The 8 families of irregular verbs', '🧩 The 8 families of irregular verbs'),
    ('🧭 Theory · Past Continuous vs Past Simple',
     '🧭 Theory · Past Continuous vs Past Simple'),
    ('процесс в прошлом · длительное действие', 'process in the past · ongoing action'),
    ('точка в прошлом · finished moment', 'point in the past · finished moment'),
    ('оба процесса одновременно', 'both processes at the same time'),
    ('процесс + точка', 'process + interrupting point'),
    ('🧭 Theory · Present Perfect', '🧭 Theory · Present Perfect'),
    ('связь прошлого и настоящего', 'link between past and present'),
    ('(когда-либо до сих пор)', '(any time up to now)'),
    ('+ период:', '+ period:'),
    ('+ точка:', '+ point in time:'),
    ('🧭 Theory · used to', '🧭 Theory · used to'),
    ('привычка в прошлом, которой больше НЕТ',
     'past habit that is NO longer true'),
    ('⚠️ ТОЛЬКО для длинной привычки · не для одного момента',
     '⚠️ ONLY for long habits · not for one single moment'),
    ('🧭 5 future forms side-by-side', '🧭 5 future forms side-by-side'),
    ('⏳ Final Rule · Time clauses · NO «will» after when / if / as soon as / until / the moment / by the time',
     '⏳ Final Rule · Time clauses · NO "will" after when / if / as soon as / until / the moment / by the time'),

    # Drill headers
    ('🎯 Drill · was or were · 8', '🎯 Drill · was or were · 8'),
    ('⌨️ Spelling · V+ed (Past Simple regular) · 10',
     '⌨️ Spelling · V+ed (Past Simple regular) · 10'),
    ('⌨️ Spelling Arena · type the Past Simple · 30',
     '⌨️ Spelling Arena · type the Past Simple · 30'),
    ('🔍 Error Hunt · 8 · type the correct form', '🔍 Error Hunt · 8 · type the correct form'),
    ('🔍 Error Hunt · 6 time clauses', '🔍 Error Hunt · 6 time clauses'),
    ('🎯 Drill · 10 pick-the-tense', '🎯 Drill · 10 pick-the-tense'),
    ('🎯 Drill · signal words · 8', '🎯 Drill · signal words · 8'),
    ('⚡ for or since? · 10 taps', '⚡ for or since? · 10 taps'),
    ('⌨️ Transform · 10', '⌨️ Transform · 10'),
    ('🎯 Functions match · place → function · 10', '🎯 Functions match · place → function · 10'),
    ('🎯 Drill · 10 MCQ · 5 futures', '🎯 Drill · 10 MCQ · 5 futures'),
    ('⌨️ Drill · time clauses · 8 gap-fill', '⌨️ Drill · time clauses · 8 gap-fill'),
    ('⌨️ Vocab test RU→EN · 8', '⌨️ Vocab test · type EN word · 8'),
    ('⌨️ Type RU → EN · 20 mixed', '⌨️ Vocab test · type EN word · 20 mixed'),

    # Vocab sub-headers
    ('📦 Harbour vocab · 8', '📦 Harbour vocab · 8'),
    ('📦 Market vocab · 10', '📦 Market vocab · 10'),
    ('📦 Lighthouse vocab · 10', '📦 Lighthouse vocab · 10'),
    ('📦 Temples vocab · 8', '📦 Temples vocab · 8'),
    ('📦 Postcards vocab · 8', '📦 Postcards vocab · 8'),
    ('📦 City vocab · 15 places (май)', '📦 City vocab · 15 places (from May)'),
    ('📦 Halloween vocab · 10', '📦 Halloween vocab · 10'),
    ('📦 Observatory + future markers · 15', '📦 Observatory + future markers · 15'),

    # Speaking · 3 задания
    ('🎤 Speaking · 3 задания', '🎤 Speaking · 3 tasks'),
    ('<b>Warm-up (20 sec):</b>', '<b>Warm-up (20 sec):</b>'),
    ('<b>Main (60 sec):</b>', '<b>Main (60 sec):</b>'),
    ('<b>Vocab in sentence (30 sec):</b>', '<b>Vocab in sentence (30 sec):</b>'),

    # Prize captions
    ('🎁 Артефакт собран · Brass Compass', '🎁 Artifact unlocked · Brass Compass'),
    ('🎁 Артефакт собран · Wicker Basket', '🎁 Artifact unlocked · Wicker Basket'),
    ('🎁 Артефакт собран · Bronze Bell (lantern inside)',
     '🎁 Artifact unlocked · Bronze Bell (lantern inside)'),
    ('🎁 Артефакт собран · Ancient Map', '🎁 Artifact unlocked · Ancient Map'),
    ('🎁 Артефакт собран · The August Postcard', '🎁 Artifact unlocked · The August Postcard'),
    ('🎁 Артефакт собран · Shiny Fountain Coin', '🎁 Artifact unlocked · Shiny Fountain Coin'),
    ('🎁 Артефакт собран · Little Jack-o\'-lantern',
     '🎁 Artifact unlocked · Little Jack-o\'-lantern'),
    ('🎁 Артефакт собран · Brass Telescope', '🎁 Artifact unlocked · Brass Telescope'),

    # Prize plus (bottom text)
    ('+5 XP × 23 правильных · HP 100/100 · поезд уходит в 06:30',
     '+5 XP × 23 correct · HP 100/100 · train leaves at 06:30'),
    ('бабушка кладёт в неё 10 яблок и хлеб · +25 XP',
     'grandma puts 10 apples and bread inside · +25 XP'),
    ('привязываешь на компас · звенит на ветру · +30 XP',
     'tie it to the compass · it rings in the wind · +30 XP'),
    ('гид передаёт свою карту, что ездила с ней 10 лет · +40 XP',
     'the guide gives you her map of 10 years · +40 XP'),
    ('её рука из прошлого — напоминание, кто она была · +45 XP',
     'her own handwriting from the past · a reminder of who she was · +45 XP'),
    ('загадала желание на год вперёд · +50 XP',
     'she made a wish for the year ahead · +50 XP'),
    ('маленький фонарик-тыква для вагона · +55 XP',
     'a tiny pumpkin lantern for the carriage · +55 XP'),
    ('маленький латунный телескоп · +60 XP · квест ЗАВЕРШЁН · 8/8 артефактов!',
     'a small brass telescope · +60 XP · QUEST COMPLETE · 8/8 artifacts!'),

    # Speak prompts fallback (Russian description text)
    ('60 seconds · tell the brass seller about ',
     '60 seconds · tell the brass seller about '),
    ('90 seconds · tell grandma about your ',
     '90 seconds · tell grandma about your '),
    ('60 seconds · describe ',
     '60 seconds · describe '),
    ('90 seconds · tell the guide about your year. ',
     '90 seconds · tell the guide about your year. '),
    ('60 seconds · tell the postman ',
     '60 seconds · tell the postman '),
    ('90 seconds · give Masha a tour of your city. ',
     '90 seconds · give Masha a tour of your city. '),
    ('60 seconds · describe <em>your best Halloween costume ever</em>. What <b>were you doing</b> while you were wearing it? What <b>happened</b>? Use Past Simple + Past Continuous.',
     '60 seconds · describe <em>your best Halloween costume ever</em>. What <b>were you doing</b> while you were wearing it? What <b>happened</b>? Use Past Simple + Past Continuous.'),

    # Big Vocab Capsule section
    ('📦 Big Vocab Capsule · 80 words recap',
     '📦 Big Vocab Capsule · 80 words recap'),
    ('🎃 Halloween (10) + 🔭 Observatory & future markers (15) — см. в станциях 7 и 8',
     '🎃 Halloween (10) + 🔭 Observatory &amp; future markers (15) — see them in stations 7 and 8'),
    ('знакомая песня из Dawn Observatory · подпой will-строчки',
     'familiar song from Dawn Observatory · sing along with the will-lines'),

    # Finale section
    ('🎤 Grand Finale · 8 artifacts · 8 cue cards',
     '🎤 Grand Finale · 8 artifacts · 8 cue cards'),
    ('quest complete · stand up and speak', 'quest complete · stand up and speak'),
    ('📋 Как это работает', '📋 How it works'),
    ('Положи 8 предметов (или их список) перед собой. На каждой карте ты берёшь один артефакт в руку и говоришь. 1-2 минуты на карту. Запиши голосовым или живьём.',
     'Put the 8 objects (or a list of them) in front of you. On each card, pick up one artifact and start talking. 1-2 minutes per card. Record a voice memo or speak live.'),
    ('Must use: ', 'Must use: '),

    # Homework
    ('Homework · к следующему уроку', 'Homework · for the next lesson'),
    ('5 задач · 45 минут', '5 tasks · 45 minutes'),
    ('🎤 Voice memo · 4 минуты', '🎤 Voice memo · 4 minutes'),
    ('— выбери 4 артефакта из Grand Finale (глава 10) и запиши рассказ голосовым в TG. На каждый артефакт — минимум 1 минута. Не прыгай между карточками хаотично.',
     ' — pick 4 artifacts from the Grand Finale (section 10) and record a voice memo in TG. Minimum 1 minute per artifact. Don\'t jump between cards chaotically.'),
    ('⌨️ Spelling Arena 30 глаголов', '⌨️ Spelling Arena 30 verbs'),
    ('(станция 2) — пройти ВСЕ 30 без единой ошибки. Если промахнулась — переделать до идеала. Скриншот финального счёта в TG.',
     ' (station 2) — complete ALL 30 with zero mistakes. If you miss any, redo until perfect. Screenshot of the final score in TG.'),
    ('⌨️ Big Vocab Capsule · 20 type-in RU→EN',
     '⌨️ Big Vocab Capsule · 20 type-in'),
    ('(глава 9) — все 20 без ошибок. Скриншот.',
     ' (section 9) — all 20 without mistakes. Screenshot.'),
    ('📝 6 time-clause предложений', '📝 6 time-clause sentences'),
    ('(станция 8) — переписать в тетрадь, подчеркнуть зелёным Present Simple и синим — will/going to/Future Perfect. Фото тетради в TG.',
     ' (station 8) — copy into your notebook, underline Present Simple in green and will/going to/Future Perfect in blue. Photo of the notebook in TG.'),
    ('📖 Reading вслух', '📖 Reading out loud'),
    ('— прочитать историю со <em>станции 2 (Market)</em> три раза, засечь время каждого раза. Цель: убрать паузы на irregular verbs.',
     ' — read the story from <em>station 2 (Market)</em> three times, time each read. Goal: no pauses on irregular verbs.'),
    ('🎵 Бонус:', '🎵 Bonus:'),
    ('спеть припев', 'sing the chorus of'),
    ('голосовым в TG. +1 звезда ⭐', 'as a voice memo in TG. +1 star ⭐'),

    # Overview headings
    ('Duration', 'Duration'),
    ('Skills', 'Skills'),
    ('Grammar focus', 'Grammar focus'),
    ('Story arc', 'Story arc'),
    ('Format', 'Format'),
    ('Previous lessons', 'Previous lessons'),
    # Overview body texts
    ('Reading (×8) · Listening (×8) · Vocabulary · Speaking (×9) · Grammar drills',
     'Reading (×8) · Listening (×8) · Vocabulary · Speaking (×9) · Grammar drills'),
    ('Present S/C + timetable · was/were · Past S regular + <em>60 irregular</em> · Past C · Present Perfect + for/since · <em>used to</em> · 5 futures · time clauses',
     'Present S/C + timetable · was/were · Past S regular + <em>60 irregular</em> · Past C · Present Perfect + for/since · <em>used to</em> · 5 futures · time clauses'),
    ('Аня садится на ночной поезд на рассвете у обсерватории. Поезд едет через её год: 8 станций — Harbour → Market → Lighthouse → Temples → Postcards → City → Hogsmeade → Observatory. На каждой станции она встречает знакомых и <em>забирает артефакт</em>. В финале — 8 артефактов и прощальная речь.',
     'Anya boards the Night Train at dawn by the observatory. The train travels through her whole year: 8 stations — Harbour → Market → Lighthouse → Temples → Postcards → City → Hogsmeade → Observatory. At every stop she meets familiar people and <em>collects one artifact</em>. In the finale: 8 artifacts and her farewell speech.'),
    ('Audio-first reading · colored tense verbs · cloze · theory boxes · drills · vocab grid · artifact pickup · speak prompt',
     'Audio-first reading · color-coded tense verbs · cloze · theory boxes · drills · vocab grid · artifact pickup · speak prompt'),
    ('L5 · Dawn Observatory (5 futures) · L4 · Lighthouse at Midnight (6 tenses) · L3 · Clock Tower · L2 · Irregular Verbs · L1 · Recap Test',
     'L5 · Dawn Observatory (5 futures) · L4 · Lighthouse at Midnight (6 tenses) · L3 · Clock Tower · L2 · Irregular Verbs · L1 · Recap Test'),

    # TOC labels (keep)
    # Nav brand sub (keep)
]

for ru, en in PAIRS:
    html = html.replace(ru, en)

# 4. Remove misc pure-RU little bits that commonly appear
# "LinguaBoost Lab · Anya · B1 · Night Train Quest · L6" — keep
# Transform cue EN examples sometimes have RU — keep EN if present

new_len = len(html)
diff = orig_len - new_len
print(f"Original: {orig_len:,} chars")
print(f"New:      {new_len:,} chars")
print(f"Diff:     {diff:+,} chars (negative = Russian stripped)")

# Count remaining Cyrillic chars for sanity
cyrillic_count = sum(1 for c in html if 'Ѐ' <= c <= 'ӿ')
print(f"Remaining Cyrillic characters: {cyrillic_count:,}")

# Write back
with io.open(TARGET, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Written to {TARGET}")
