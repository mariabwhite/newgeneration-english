# -*- coding: utf-8 -*-
"""Katya + Mia at Disneyland Paris · 20 lines · MP3s for Listening 02.
Voices: Katya=Sonia (en-GB female), Mia=Libby (en-GB female alt), Guide=Ryan.
Run:  python _gen.py
"""
import asyncio, sys
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).parent

KATYA = "en-GB-SoniaNeural"
MIA   = "en-GB-LibbyNeural"

LINES = [
    ("01-katya", KATYA, "Look at that huge roller coaster! It's amazing!"),
    ("02-mia",   MIA,   "I know! It's called Space Mountain. Do you want to ride it first?"),
    ("03-katya", KATYA, "Yes, but the queue is so long, nearly an hour!"),
    ("04-mia",   MIA,   "Let's buy a fast pass. It saves lots of time."),
    ("05-katya", KATYA, "Great idea. How much is it?"),
    ("06-mia",   MIA,   "About twenty euros extra, but it's worth it."),
    ("07-katya", KATYA, "Look, there's a carousel over there. Should we ride it first?"),
    ("08-mia",   MIA,   "Sure, it's a classic. My little sister loves carousels."),
    ("09-katya", KATYA, "After that, let's go on the ferris wheel. The view is incredible."),
    ("10-mia",   MIA,   "Perfect. And later, bumper cars?"),
    ("11-katya", KATYA, "Of course! I'm going to win this time!"),
    ("12-mia",   MIA,   "We'll see about that."),
    ("13-katya", KATYA, "I'm getting hungry. Where's the food court?"),
    ("14-mia",   MIA,   "Right past the haunted house. They have great pizza."),
    ("15-katya", KATYA, "Let's grab a slice and eat by the lake."),
    ("16-mia",   MIA,   "Look, the parade is starting! Mickey Mouse the mascot is waving!"),
    ("17-katya", KATYA, "Wait, I want a souvenir first. Where's the shop?"),
    ("18-mia",   MIA,   "Near the exit. Let's go there after the parade."),
    ("19-katya", KATYA, "Best day ever! Thank you for bringing me here!"),
    ("20-mia",   MIA,   "My pleasure! Same time next summer?"),
]

async def gen_one(key, voice, text):
    fname = OUT / f"{key}.mp3"
    if fname.exists():
        print(f"skip  {fname.name}"); return
    tts = edge_tts.Communicate(text, voice, rate="-2%")
    await tts.save(str(fname))
    print(f"done  {fname.name}  ({voice})")

async def main():
    for k, v, t in LINES:
        try:
            await gen_one(k, v, t)
        except Exception as e:
            print(f"FAIL  {k}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
