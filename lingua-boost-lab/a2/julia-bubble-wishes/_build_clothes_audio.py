"""Generate TTS clips for the clothes + UK coins warm-up (sec-00)."""
import asyncio, pathlib
import edge_tts

HERE = pathlib.Path(__file__).parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)

GIRL = "en-GB-LibbyNeural"
SHOP = "en-GB-RyanNeural"

VOCAB = [
    ("jumper", "jumper"),
    ("jeans", "jeans"),
    ("scarf", "scarf"),
    ("cap", "cap"),
    ("coat", "coat"),
    ("gloves", "gloves"),
    ("pyjamas", "pyjamas"),
    ("slippers", "slippers"),
    ("one-penny", "one penny"),
    ("two-pence", "two pence"),
    ("one-pound", "one pound"),
    ("forty-pounds", "forty pounds"),
    ("seven-pounds-twenty-five", "seven pounds twenty-five"),
]

SHOP_LINES = [
    ("shop-coat-q", "How much is the coat?", GIRL),
    ("shop-coat-a", "It's forty pounds.", SHOP),
    ("shop-gloves-q", "How much are the gloves?", GIRL),
    ("shop-gloves-a", "They're seven pounds twenty-five.", SHOP),
    ("shop-cap-q", "How much is the cap?", GIRL),
    ("shop-cap-a", "It's one pound.", SHOP),
]

RATE = "-25%"

async def one(slug, text, voice, tries=3):
    out = AUDIO / f"{slug}.mp3"
    if out.exists() and out.stat().st_size > 1024:
        return "skip"
    for attempt in range(tries):
        try:
            comm = edge_tts.Communicate(text, voice, rate=RATE)
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
    for slug, text in VOCAB:
        r = await one(f"vocab-{slug}", text, GIRL)
        print(f"[{r:5}] vocab-{slug}")
    for slug, text, voice in SHOP_LINES:
        r = await one(slug, text, voice)
        print(f"[{r:5}] {slug}")

if __name__ == "__main__":
    asyncio.run(main())
