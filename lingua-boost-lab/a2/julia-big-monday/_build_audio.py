"""Generate TTS clips for julia-big-monday (A2 kid, Julia canon).

Voices:
- Jenny (girl, en-US) — Julia's own lines, bio-julia
- Libby (woman, en-GB) — Mum / Mama lines, Aunt Anya, Mrs. Pilsberry
- Ryan (boy multilingual, en-US) — John's lines
- Aria (narrator, en-US) — reading chapters, Barsik voiceover
- Jenny — Emma lines (same age/class)

Only writes clips that don't exist, with 3 retries on edge-tts 403.
"""
import asyncio
import pathlib
import edge_tts

HERE = pathlib.Path(__file__).parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)

NARR = "en-US-AriaNeural"
GIRL = "en-US-JennyNeural"
BOY = "en-GB-RyanNeural"
MAMA = "en-GB-LibbyNeural"

# ===== STORY CHAPTERS (reading passages — audio-first) =====
STORY_CH1 = (
    "Hi, I'm Julia and this is my family. We live in a nice flat in our city, "
    "not far from the big park where they have the fair every summer. "
    "There are three of us: my mum, my little brother John, and me. "
    "We've also got one very special family member — Barsik, our big grey cat. "
    "Barsik is the king of the flat. Everybody knows it."
)
STORY_CH2 = (
    "My mum works at home. She has got long wavy brown hair and warm eyes. "
    "On school days she always drives John and me to school in our car — "
    "she doesn't like it when we walk alone, because the roads here are busy. "
    "On Sundays Mum makes big pancakes with honey — the best pancakes in the world. "
    "We eat them with tea and raspberry jam. "
    "Then sometimes we all go for a walk in the city park."
)
STORY_CH3 = (
    "John is my little brother. He is six years old and this is his first year at school — first grade. "
    "He loves horses, carousels and ice cream. "
    "Every morning John loses one of his shoes before school, and Mum shouts, Where is your shoe?! "
    "and we all look for it. Usually it is under the sofa. Always. "
    "Last Sunday Mum gave me three hundred roubles and we went to the big fair with Emma. "
    "John rode a white carousel horse and said he was a cowboy. "
    "He put his orange ticket in his pocket and kept it like a treasure."
)
STORY_CH4 = (
    "Barsik is a big grey cat with golden-green eyes and a long serious tail. He is seven years old. "
    "He sleeps a lot, eats a lot, and watches everything that happens in the flat. "
    "Barsik does NOT like small kittens. Last summer at the fair we met Mrs. Pilsberry, a cat breeder. "
    "She had six tiny Scottish Fold kittens, each for about fifty thousand roubles. "
    "John wanted one so much! But I told him: "
    "John, we already have Barsik at home. And Barsik is a king. "
    "He wouldn't like a tiny kitten in his kingdom. "
    "John agreed. Barsik agreed. Mum laughed."
)

# ===== SCENE-ROW story voices (short) =====
SCENE_START = "The weekend is over, the alarm clock rings. It's a bright new day — I love this day!"
SCENE_MORNING = (
    "Hi! I'm Julia and I'm nine years old. Every Monday I always get up at half past seven. "
    "I usually have cereal, but sometimes I have pancakes. "
    "I never walk to school — Mum drives me and John in our car."
)
SCENE_BREAKFAST = (
    "Yesterday I was eating pancakes with honey at Aunt Anya's flat. "
    "Her cat Rizhik was sitting on the floor. "
    "Suddenly he jumped on the table and ate my sausage! Then he ran to the balcony. "
    "Aunt Anya screamed, John laughed, and I dropped my fork. "
    "I forgot my English book on their sofa and we came back for it in the evening!"
)
SCENE_SCHOOL = (
    "It's eleven o'clock. Emma is sitting next to me. She is drawing a flower. "
    "Mrs. Green is writing on the board. Vova is sleeping again! "
    "Three boys are playing with a paper plane. And me? I am looking at the clock — I'm so hungry!"
)
SCENE_CAFE = (
    "After school we are going to meet at the Pink Café. "
    "We are going to order chocolate milkshakes and strawberry pancakes. "
    "Then we are going to buy a present for Mum — her birthday is on Friday, the fifteenth of November!"
)
SCENE_EVENING = (
    "Tomorrow will be Tuesday. We will have English and PE. "
    "I think I will get a good mark — I studied hard! "
    "Mum says it will rain on Friday, but I don't believe her — the sun will shine for her birthday. "
    "And one day, I will travel to London."
)

# ===== BIO ONE-LINERS (cast-strip & family grid) =====
BIO_JULIA = "I'm Julia, I'm nine, I'm in the fourth grade. I love drawing and animals."
BIO_MUM = "I work at home. I take Julia and John to school every morning. On Sundays I make pancakes."
BIO_JOHN = "I'm John! I'm six. I'm in the first grade. I love horses and carousels!"
BIO_BARSIK = "I am Barsik. I am the king of this flat. Serve me cat food, please. Meow."

CAST_JULIA = "Hi, I'm Julia! Welcome to my Monday."
CAST_MUM = "Good morning, kids! Breakfast is ready!"
CAST_JOHN = "I lost my shoe AGAIN, Mum!"
CAST_EMMA = "Hi Julia! Pink Café at one o'clock?"
CAST_BARSIK = "Meow. Meow. Meow."

# ===== DIALOGUE TURNS (family 2.4) =====
D_MUM_1 = "Good morning, everybody! The pancakes are ready. John — where is your other shoe?"
D_JOHN_1 = "I don't know, Mum… Maybe Barsik took it!"
D_JULIA_1 = "It's not Barsik. Barsik is sitting on the window sill — he is washing his paw."
D_MUM_2 = "Oh dear. John, come to the table, we have ten minutes before school. Can I have your plate, please?"
D_JULIA_2 = "Mum, I will find the shoe. (looks under the sofa) …Got it! Here, John!"
D_JOHN_2 = "YAY! Thank you, Julia! You are the best big sister!"
D_MUM_3 = "Good team. And this evening we are going to call Grandma — don't forget, OK?"

# ===== VOCAB CAPSULE (20 words from Julia's past lessons + 5 new) =====
VOCAB_WORDS = [
    "shop assistant", "price tag", "shopping bag", "till", "fitting room",
    "receipt", "hanger", "mirror", "cash", "roubles",
    "kitten", "carousel", "ticket", "queue", "breeder",
    "pumpkin", "candy", "costume", "pancakes", "honey",
]

# ===== CLIP TABLE =====
CLIPS = []
# Scene-row story voices (short, Julia narrating)
CLIPS.append(("scene-start", SCENE_START, GIRL))
CLIPS.append(("scene-morning", SCENE_MORNING, GIRL))
CLIPS.append(("scene-breakfast", SCENE_BREAKFAST, GIRL))
CLIPS.append(("scene-school", SCENE_SCHOOL, GIRL))
CLIPS.append(("scene-cafe", SCENE_CAFE, GIRL))
CLIPS.append(("scene-evening", SCENE_EVENING, GIRL))
# Reading chapters (narrator voice for passages)
CLIPS.append(("story-ch1-flat", STORY_CH1, GIRL))
CLIPS.append(("story-ch2-mum", STORY_CH2, NARR))
CLIPS.append(("story-ch3-john", STORY_CH3, NARR))
CLIPS.append(("story-ch4-barsik", STORY_CH4, NARR))
# Bios
CLIPS.append(("bio-julia", BIO_JULIA, GIRL))
CLIPS.append(("bio-mum", BIO_MUM, MAMA))
CLIPS.append(("bio-john", BIO_JOHN, BOY))
CLIPS.append(("bio-barsik", BIO_BARSIK, NARR))
# Cast
CLIPS.append(("cast-julia", CAST_JULIA, GIRL))
CLIPS.append(("cast-mum", CAST_MUM, MAMA))
CLIPS.append(("cast-john", CAST_JOHN, BOY))
CLIPS.append(("cast-emma", CAST_EMMA, GIRL))
CLIPS.append(("cast-barsik", CAST_BARSIK, NARR))
# Dialogue turns
CLIPS.append(("d-mum-1", D_MUM_1, MAMA))
CLIPS.append(("d-john-1", D_JOHN_1, BOY))
CLIPS.append(("d-julia-1", D_JULIA_1, GIRL))
CLIPS.append(("d-mum-2", D_MUM_2, MAMA))
CLIPS.append(("d-julia-2", D_JULIA_2, GIRL))
CLIPS.append(("d-john-2", D_JOHN_2, BOY))
CLIPS.append(("d-mum-3", D_MUM_3, MAMA))
# Vocab capsule words — just the word, slow
for w in VOCAB_WORDS:
    slug = "vocab-" + w.replace("'", "").replace(" ", "-")
    CLIPS.append((slug, w, GIRL))

RATE_SLOW = "-10%"
RATE_VERY_SLOW = "-25%"

async def one(slug, text, voice, tries=3, rate=RATE_SLOW):
    out = AUDIO / f"{slug}.mp3"
    if out.exists() and out.stat().st_size > 1024:
        return "skip"
    for attempt in range(tries):
        try:
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(str(out))
            if out.exists() and out.stat().st_size > 1024:
                return "ok"
        except Exception as e:
            print(f"[{slug}] attempt {attempt+1} fail: {type(e).__name__}: {e}")
            await asyncio.sleep(5)
    # ensure no 0-byte dangling file
    if out.exists() and out.stat().st_size <= 1024:
        try:
            out.unlink()
        except Exception:
            pass
    return "FAIL"

async def main():
    results = {}
    for slug, text, voice in CLIPS:
        # vocab words — slower pace for spelling drill
        rate = RATE_VERY_SLOW if slug.startswith("vocab-") else RATE_SLOW
        r = await one(slug, text, voice, rate=rate)
        print(f"[{r:5}] {slug}")
        results[slug] = r
    print()
    ok = sum(1 for v in results.values() if v == "ok")
    skip = sum(1 for v in results.values() if v == "skip")
    fail = sum(1 for v in results.values() if v == "FAIL")
    print(f"TOTAL  ok={ok}  skip={skip}  fail={fail}")

if __name__ == "__main__":
    asyncio.run(main())
