"""Generate TTS clips for julia-bubble-wishes (A2→B1, Julia canon)."""
import asyncio, pathlib, shutil
import edge_tts

HERE = pathlib.Path(__file__).parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)

# Reuse cast voices from julia-big-monday (same characters)
SOURCE = HERE.parent / "julia-big-monday" / "audio"
for cast in ["cast-julia", "cast-mum", "cast-john", "cast-emma", "cast-barsik"]:
    src = SOURCE / f"{cast}.mp3"
    dst = AUDIO / f"{cast}.mp3"
    if src.exists() and not dst.exists():
        shutil.copy(src, dst)
        print(f"[copy] {cast}")

NARR = "en-US-AriaNeural"
GIRL = "en-US-JennyNeural"
BOY = "en-GB-RyanNeural"
MAMA = "en-GB-LibbyNeural"

SCENE_START = "After school. The kitchen window is open. Sunlight on the floor. And in the drawer — something I had forgotten about since last summer."

STORY_CH1 = (
    "Julia opened the kitchen drawer and smiled. There it was — the old bubble bottle from last summer in Bodrum. "
    "Only one tiny drop left inside. "
    "Mum, can we make more? Please, please! shouted John from the sofa, suddenly very awake. "
    "Mum laughed. Of course. I know the perfect recipe. Bring me a bowl. "
    "She wrote on a piece of paper. "
    "Take a big bowl. Pour one cup of water into the bowl. Add two spoons of dish soap. "
    "Mix gently with a spoon — don't shake! Add one small spoon of glycerin — the magic ingredient. "
    "Wait ten minutes. Then take your wand and blow!"
)

STORY_CH2 = (
    "Ten minutes later, Julia stood on the balcony with the wand. The afternoon sun was warm. "
    "She breathed in deeply and blew. "
    "A perfect, shiny bubble floated out of the ring — a rainbow on its skin. "
    "I will travel to London one day, Julia whispered. That's my wish. "
    "The bubble floated higher, higher, higher… and then — pop. "
    "There, she smiled. The wish is in the sky now. It will come true."
)

STORY_CH3 = (
    "Julia was blowing her tenth bubble when Barsik suddenly jumped onto the balcony table. "
    "He was running after a shiny pink bubble. POP! "
    "The bubble burst on his nose. He stopped. He looked at his wet paw. He sneezed. "
    "Julia was laughing so hard she dropped the wand. "
    "BARSIK! That was my wish! she said. Now I will have to blow another one. "
    "Barsik wasn't listening. He was already waiting for the next bubble, "
    "his tail moving left and right like a conductor's baton."
)

STORY_CH4 = (
    "Ten minutes later, Emma rang the doorbell. In her hands was a huge wire ring, big as a plate. "
    "Look what I brought! Mum helped me make it. We are going to blow a bubble bigger than John! "
    "They poured the mixture into a big bowl and took everything to the city park. "
    "The grass was warm. A soft wind was blowing. "
    "If I blow very slowly, the bubble will be giant, Emma said. "
    "And if it bursts, we will just mix some more! Julia laughed. "
    "They were going to make a Guinness-record bubble, but Barsik — well, you already know Barsik."
)

STORY_CH5 = (
    "The sun was turning orange. Julia, John and Emma sat on the warm grass. "
    "The last bubble of the day floated slowly above the trees — bigger than any before. "
    "Maybe one day I might be a scientist, said John quietly, and I will invent a bubble that never pops. "
    "Maybe one day I could have my own art studio with a huge window, said Julia. "
    "Maybe one day we might open a bubble shop together, said Emma, and only sell wishes. "
    "Barsik was already asleep in Julia's lap, dreaming his own bubble dreams. "
    "Julia smiled. Maybe one day… but today was a very good day too."
)

VOCAB = [
    ("bubble","bubble"),("soap","soap"),("blow","to blow"),("pop","to pop"),("burst","to burst"),
    ("wand","wand"),("ring","ring"),("recipe","recipe"),("mixture","mixture"),("ingredient","ingredient"),
    ("rainbow","rainbow"),("shiny","shiny"),("float","to float"),("wet","wet"),
    ("wish","wish"),("hope","to hope"),("dream","dream"),("promise","promise"),
    ("one-day","one day"),("come-true","come true"),
]

CLIPS = []
CLIPS.append(("scene-start", SCENE_START, GIRL))
CLIPS.append(("story-ch1-bottle", STORY_CH1, GIRL))
CLIPS.append(("story-ch2-balcony", STORY_CH2, GIRL))
CLIPS.append(("story-ch3-barsik", STORY_CH3, NARR))
CLIPS.append(("story-ch4-giant", STORY_CH4, NARR))
CLIPS.append(("story-ch5-sunset", STORY_CH5, NARR))
for slug, text in VOCAB:
    CLIPS.append((f"vocab-{slug}", text, GIRL))

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
    if out.exists() and out.stat().st_size <= 1024:
        try: out.unlink()
        except: pass
    return "FAIL"

async def main():
    results = {}
    for slug, text, voice in CLIPS:
        rate = RATE_VERY_SLOW if slug.startswith("vocab-") else RATE_SLOW
        r = await one(slug, text, voice, rate=rate)
        print(f"[{r:5}] {slug}")
        results[slug] = r
    ok = sum(1 for v in results.values() if v == "ok")
    skip = sum(1 for v in results.values() if v == "skip")
    fail = sum(1 for v in results.values() if v == "FAIL")
    print(f"\nTOTAL ok={ok} skip={skip} fail={fail}")

if __name__ == "__main__":
    asyncio.run(main())
