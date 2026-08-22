"""Generate MP3 audio for denis-shopping-recap via edge-tts.
Windows fix: sys.stdout.reconfigure utf-8; slug cap 40.
Voice: en-GB-SoniaNeural (British female, natural).
Run:  python _gen.py
"""
import asyncio, sys, re
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VOICE = "en-GB-SoniaNeural"
OUT = Path(__file__).parent

def slug(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s[:40] or "audio"

LINES = [
    # 7.5A · Listen & tick (5)
    ("t1a", "I'd like a large cappuccino to go, please. No sugar, just a little milk."),
    ("t1b", "Excuse me, have you got this jacket in a bigger size? This one is a little tight around the shoulders."),
    ("t1c", "Good afternoon, Grand View Hotel. I'd like to book a double room for two nights, arriving on Friday. Have you got Wi-Fi and free breakfast?"),
    ("t1d", "Look at those clouds — it's going to rain in a minute. Let's take a taxi instead of walking."),
    ("t1e", "No, thanks. I'm just browsing. If I need help, I'll come and find you."),
    # 7.5B · Listen & respond (5)
    ("r2a", "I only buy things on sale. I never pay full price for clothes."),
    ("r2b", "Online shopping is a waste of time. You never really know what you're buying."),
    ("r2c", "I go to the same café every morning. The barista knows my order."),
    ("r2d", "I've packed three jackets for a two-day trip. Better to be ready for any weather."),
    ("r2e", "I never take a receipt. Too much paper. Everything is in the bank app anyway."),
    # 7.5C · Dictation (5)
    ("d3a", "I'll take this one, please."),
    ("d3b", "Have you got this in a bigger size?"),
    ("d3c", "The fitting room is on your left."),
    ("d3d", "Would you like a receipt with that?"),
    ("d3e", "I'm going to buy a warm coat before winter."),
]

async def gen_one(key, text):
    fname = OUT / f"{key}-{slug(text)}.mp3"
    if fname.exists():
        print(f"skip  {fname.name}"); return
    tts = edge_tts.Communicate(text, VOICE, rate="-6%")
    await tts.save(str(fname))
    print(f"done  {fname.name}")

async def main():
    for key, text in LINES:
        try:
            await gen_one(key, text)
        except Exception as e:
            print(f"FAIL  {key}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
