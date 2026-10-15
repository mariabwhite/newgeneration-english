"""Copy 10 jobs/hobbies DALL-E images into assets/img/ with semantic names,
wire them into the HTML (replace shopping img src), unhide images in CSS."""
import os, shutil, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.expanduser('~/Downloads')
IMG = os.path.join(HERE, 'assets', 'img')
os.makedirs(IMG, exist_ok=True)

COPY = {
    'e4885e3a-fbe1-4e4f-83cb-4ea993167bff.png': 'scene-hero.png',                       # British high street workers
    'd405adc8-60c6-4a5a-82b7-74abb593940a.png': 'scene-vocab-objects.png',              # 20 flat-lay job objects
    '72b02cc4-5798-4ef5-acea-631776db49b1.png': 'scene-features-dream-job.png',         # 10 features cards
    '838ebf1f-14fa-4620-9fcf-abaf3bad3229.png': 'scene-bodyguard-two-sides.png',        # PROS/CONS ENGLISH
    '2951f406-966b-426a-ba0e-ecc372e112d8.png': 'scene-bodyguard-reading.png',          # President + bodyguards
    'ffde6764-aa19-402d-98fa-7236ab88e2f4.png': 'scene-passive-infographic.png',        # Passive 8 tenses
    '419fc7e9-866a-440f-8bef-4ac2befd001f.png': 'scene-hobbies-by-age.png',             # Hobbies by age chart
    '395e8fc5-05ae-449d-b420-4f9d7ca28514.png': 'scene-why-jobs-pay-more.png',          # Why jobs pay more chart
    'db4cf5c4-4717-4837-b1ca-ac10b5ac78c3.png': 'scene-conditionals-strip.png',         # Conditionals IF→RESULT
    '31620625-da33-4bfe-bd60-8998e3cb46c8.png': 'scene-interview-room.png',             # Interview editorial
    '993ec0dc-4540-4fa3-80cc-7afb21fc2a45.png': 'scene-hero-alt.png',                   # alt hero
}

for src, dst in COPY.items():
    s = os.path.join(DL, src)
    d = os.path.join(IMG, dst)
    if os.path.exists(s):
        shutil.copy2(s, d)
        print(f'OK {dst} ({os.path.getsize(d):,} b)')
    else:
        print(f'MISS {src}')

# ─── wire into HTML ───
p = os.path.join(HERE, 'index.html')
with open(p, 'r', encoding='utf-8') as f: s = f.read()

# 1. remove the display:none for images
s = s.replace('img[src^="assets/img"]{display:none !important}', '/* images now live again */')

# 2. restore hero.png in hero-card background (desktop + mobile)
s = s.replace(
    'linear-gradient(100deg, rgba(255,244,236,.98) 0%, rgba(255,232,214,.82) 42%, rgba(247,127,58,.28) 72%, rgba(232,93,31,.18) 100%);',
    'linear-gradient(100deg, rgba(255,244,236,.95) 0%, rgba(255,232,214,.80) 32%, rgba(247,127,58,.22) 65%, rgba(232,93,31,.14) 100%), url("assets/img/scene-hero.png") right center / cover no-repeat;'
)
s = s.replace(
    '@media(max-width:720px){.hero-card{background:linear-gradient(135deg,rgba(255,244,236,.98) 0%,rgba(255,232,214,.72) 100%)}}',
    '@media(max-width:720px){.hero-card{background:linear-gradient(135deg,rgba(255,244,236,.95) 0%,rgba(255,232,214,.72) 100%),url("assets/img/scene-hero.png") center/cover no-repeat}}'
)

# 3. swap img src values pointing to shopping files → new scene files
img_swaps = {
    'assets/img/section0b-teen-haul.png':  'assets/img/scene-features-dream-job.png',  # section 0+ hero banner
    'assets/img/vocab-objects.png':        'assets/img/scene-vocab-objects.png',
    'assets/img/section1-arcade.png':      'assets/img/scene-features-dream-job.png',  # features of a job
    'assets/img/section2-shop-assistant.png': 'assets/img/scene-bodyguard-two-sides.png',
    'assets/img/section3-verger.png':      'assets/img/scene-bodyguard-reading.png',
    'assets/img/section5-modals.png':      'assets/img/scene-passive-infographic.png',
    'assets/img/section6-britain.png':     'assets/img/scene-hobbies-by-age.png',
    'assets/img/section7-money-timeline.png': 'assets/img/scene-why-jobs-pay-more.png',
    'assets/img/section10-shopeng.png':    'assets/img/scene-interview-room.png',
}
cnt = 0
for old, new in img_swaps.items():
    if old in s:
        s = s.replace(old, new)
        cnt += 1
print(f'img swaps: {cnt}')

with open(p, 'w', encoding='utf-8') as f: f.write(s)
print(f'wire done.')
