"""Insert the 15 PNG assets into the right places in index.html.

- scene-00-hero.png → hero bg
- scene-ch1-bottle.png + scene-ch1b-recipe.png → Chapter 1
- scene-ch2-balcony.png → Chapter 2 (first bubble on balcony)
- scene-ch3-barsik.png + scene-ch3b-barsik-paw.png → Chapter 3 (bubble hunter)
- scene-ch4-giant-park.png → Chapter 4 (giant bubble park)
- scene-ch5-sunset.png → Chapter 5 (sunset wishes)
- cast-family.png → wrap-up
"""
import pathlib
HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"
t = HTML.read_text(encoding="utf-8")

# 1) Hero bg - add scene-00-hero as background image under existing gradient
old_hero_bg = """.hero-card{
  border:1px solid rgba(255,255,255,.3);border-radius:var(--radius-l);
  padding:clamp(28px,4vw,46px);
  background:
    linear-gradient(135deg, rgba(242,166,200,.95) 0%, rgba(198,137,224,.9) 35%, rgba(155,107,197,.9) 70%, rgba(74,43,107,.85) 100%),
    linear-gradient(135deg,#C689E0,#4A2B6B);
  position:relative;overflow:hidden;
  box-shadow:0 10px 30px rgba(74,43,107,.3);
  min-height:360px;
  text-align:center;color:#fff;
}"""
new_hero_bg = """.hero-card{
  border:1px solid rgba(255,255,255,.3);border-radius:var(--radius-l);
  padding:clamp(28px,4vw,46px);
  background:
    linear-gradient(180deg, rgba(74,43,107,.4) 0%, rgba(74,43,107,.1) 30%, rgba(74,43,107,.15) 65%, rgba(74,43,107,.85) 100%),
    url('img/scene-00-hero.png') center 25%/cover no-repeat,
    linear-gradient(135deg,#C689E0,#4A2B6B);
  position:relative;overflow:hidden;
  box-shadow:0 10px 30px rgba(74,43,107,.3);
  min-height:460px;
  text-align:center;color:#fff;
  display:flex;flex-direction:column;justify-content:space-between;
}
.hero-card .eyebrow,.hero-card .hero-title{flex:0 0 auto}
.hero-card .hero-lead,.hero-card .hero-tags{flex:0 0 auto;margin-top:auto}"""
assert old_hero_bg in t
t = t.replace(old_hero_bg, new_hero_bg)
print("✓ Hero bg updated")

# 2) Chapter 1 · bottle + recipe
ch1_anchor = """  <div class="reading-body">
    <div class="audio-label">Chapter 1 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch1-bottle.mp3"></audio>"""
ch1_new = """  <img class="scene-img" src="img/scene-ch1-bottle.png" alt="Julia finds the old bubble bottle in the kitchen drawer, Mum and John nearby" style="width:100%;border-radius:14px;margin-bottom:12px;box-shadow:0 8px 20px rgba(74,43,107,.15)">
  <div class="reading-body">
    <div class="audio-label">Chapter 1 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch1-bottle.mp3"></audio>"""
assert ch1_anchor in t
t = t.replace(ch1_anchor, ch1_new)
print("✓ Chapter 1 scene inserted")

# recipe scene — before "Mum's secret bubble recipe"
recipe_anchor = """  <div class="card">
    <span class="ex-sticker">🥣</span>
    <span class="ex-sticker left small">🧪</span>
    <h3><span class="ex-num">2.1</span> Mum's secret bubble recipe</h3>"""
recipe_new = """  <img class="scene-img" src="img/scene-ch1b-recipe.png" alt="The family gathered around a bowl of soap mixture with Barsik and the glycerin bottle" style="width:100%;border-radius:14px;margin:6px 0 14px;box-shadow:0 8px 20px rgba(74,43,107,.15)">
  <div class="card">
    <span class="ex-sticker">🥣</span>
    <span class="ex-sticker left small">🧪</span>
    <h3><span class="ex-num">2.1</span> Mum's secret bubble recipe</h3>"""
assert recipe_anchor in t
t = t.replace(recipe_anchor, recipe_new)
print("✓ Chapter 1 recipe scene inserted")

# 3) Chapter 2 · balcony
ch2_anchor = """  <div class="reading-body">
    <div class="audio-label">Chapter 2 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch2-balcony.mp3"></audio>"""
ch2_new = """  <img class="scene-img" src="img/scene-ch2-balcony.png" alt="Julia and John on the balcony at sunset, blowing bubbles over the city with Barsik watching" style="width:100%;border-radius:14px;margin-bottom:12px;box-shadow:0 8px 20px rgba(74,43,107,.15)">
  <div class="reading-body">
    <div class="audio-label">Chapter 2 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch2-balcony.mp3"></audio>"""
assert ch2_anchor in t
t = t.replace(ch2_anchor, ch2_new)
print("✓ Chapter 2 scene inserted")

# 4) Chapter 3 · Barsik the hunter (main + paw)
ch3_anchor = """  <div class="reading-body">
    <div class="audio-label">Chapter 3 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch3-barsik.mp3"></audio>"""
ch3_new = """  <img class="scene-img" src="img/scene-ch3-barsik.png" alt="Barsik flying through the air after bubbles on the balcony, Julia laughing" style="width:100%;border-radius:14px;margin-bottom:12px;box-shadow:0 8px 20px rgba(74,43,107,.15)">
  <div class="reading-body">
    <div class="audio-label">Chapter 3 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch3-barsik.mp3"></audio>"""
assert ch3_anchor in t
t = t.replace(ch3_anchor, ch3_new)
print("✓ Chapter 3 scene inserted")

# second barsik image (paw up) — before mini-theory
ch3b_anchor = """  <div class="card">
    <span class="ex-sticker">🐱</span>
    <span class="ex-sticker left small">💥</span>
    <h3><span class="ex-num">4.1</span> Mini-theory · Past Continuous + Past Simple together</h3>"""
ch3b_new = """  <img class="scene-img" src="img/scene-ch3b-barsik-paw.png" alt="Barsik with his paw up toward a bubble, the family watching and laughing" style="width:100%;border-radius:14px;margin:6px 0 14px;box-shadow:0 8px 20px rgba(74,43,107,.15)">
  <div class="card">
    <span class="ex-sticker">🐱</span>
    <span class="ex-sticker left small">💥</span>
    <h3><span class="ex-num">4.1</span> Mini-theory · Past Continuous + Past Simple together</h3>"""
assert ch3b_anchor in t
t = t.replace(ch3b_anchor, ch3b_new)
print("✓ Chapter 3b scene inserted")

# 5) Chapter 4 · giant park
ch4_anchor = """  <div class="reading-body">
    <div class="audio-label">Chapter 4 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch4-giant.mp3"></audio>"""
ch4_new = """  <img class="scene-img" src="img/scene-ch4-giant-park.png" alt="Julia Emma and John in the park with a giant iridescent soap bubble, sunset over the city" style="width:100%;border-radius:14px;margin-bottom:12px;box-shadow:0 8px 20px rgba(74,43,107,.15)">
  <div class="reading-body">
    <div class="audio-label">Chapter 4 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch4-giant.mp3"></audio>"""
assert ch4_anchor in t
t = t.replace(ch4_anchor, ch4_new)
print("✓ Chapter 4 scene inserted")

# 6) Chapter 5 · sunset
ch5_anchor = """  <div class="reading-body">
    <div class="audio-label">Chapter 5 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch5-sunset.mp3"></audio>"""
ch5_new = """  <img class="scene-img" src="img/scene-ch5-sunset.png" alt="Julia John and Emma on a bench at sunset, Barsik asleep on Julia's lap, giant bubble floating over the city" style="width:100%;border-radius:14px;margin-bottom:12px;box-shadow:0 8px 20px rgba(74,43,107,.15)">
  <div class="reading-body">
    <div class="audio-label">Chapter 5 · audio-first</div>
    <audio controls preload="metadata" src="audio/story-ch5-sunset.mp3"></audio>"""
assert ch5_anchor in t
t = t.replace(ch5_anchor, ch5_new)
print("✓ Chapter 5 scene inserted")

# 7) Wrap-up: cast-family image
wrap_anchor = """<!-- ===== WRAP-UP ===== -->
<section class="wrap-up">
  <h2>🫧 The sky is full of wishes</h2>"""
wrap_new = """<!-- ===== WRAP-UP ===== -->
<section class="wrap-up">
  <img src="img/cast-family.png" alt="Julia Mum John Emma and Barsik all together with floating bubbles" style="width:100%;max-width:420px;margin:0 auto 16px;border-radius:14px;position:relative;z-index:2;display:block">
  <h2>🫧 The sky is full of wishes</h2>"""
assert wrap_anchor in t
t = t.replace(wrap_anchor, wrap_new)
print("✓ Wrap-up cast image inserted")

# 8) Add scene-img CSS if missing
scene_img_css = ".scene-img{display:block;width:100%;max-width:100%;margin:14px 0;border-radius:14px;box-shadow:0 8px 20px rgba(74,43,107,.15)}"
if scene_img_css not in t and ".scene-img{" not in t:
    # insert into style block
    marker = "/* ===== SCENE AUDIO BAR (mini voice drops) ===== */"
    t = t.replace(marker, scene_img_css + "\n\n" + marker)
    print("✓ scene-img CSS added")

HTML.write_text(t, encoding="utf-8")
print(f"\nDone. File size: {len(t)} chars.")
