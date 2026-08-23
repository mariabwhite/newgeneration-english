# -*- coding: utf-8 -*-
"""Generate MP3 lines for Listening 02 · Alex & Jamie dine out.
Voices: Waiter=Brian (en-GB male), Alex=Russell (en-AU male), Jamie=Amy (en-GB female).
edge-tts equivalents: en-GB-RyanNeural / en-AU-WilliamNeural / en-GB-SoniaNeural.
Run: python _gen.py
"""
import asyncio, sys
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).parent

WAITER = "en-GB-RyanNeural"
ALEX   = "en-AU-WilliamNeural"
JAMIE  = "en-GB-SoniaNeural"

LINES = [
    ("01-waiter", WAITER, "Good evening! Can I start you off with something to drink?"),
    ("02-alex",   ALEX,   "Hi! We'll have a bottle of house red wine, please."),
    ("03-jamie",  JAMIE,  "And some sparkling water for the table."),
    ("04-waiter", WAITER, "Great choice! Have you looked at the menu?"),
    ("05-alex",   ALEX,   "Not yet. What do you recommend?"),
    ("06-waiter", WAITER, "The bruschetta is popular, and the seafood pasta is a favorite."),
    ("07-jamie",  JAMIE,  "Let's get the bruschetta to start."),
    ("08-waiter", WAITER, "Excellent! Are you ready for your main courses?"),
    ("09-alex",   ALEX,   "I'll have the grilled salmon."),
    ("10-jamie",  JAMIE,  "And I'll take the chicken marsala."),
    ("11-waiter", WAITER, "Perfect! Would you like any sides?"),
    ("12-jamie",  JAMIE,  "Yes, let's add garlic mashed potatoes."),
    ("13-waiter", WAITER, "How was everything?"),
    ("14-jamie",  JAMIE,  "Everything was wonderful!"),
    ("15-alex",   ALEX,   "Yes, we loved it. Can we see the dessert menu?"),
    ("16-waiter", WAITER, "Of course! I recommend the chocolate lava cake."),
    ("17-jamie",  JAMIE,  "That sounds perfect. We'll have one of those!"),
    ("18-alex",   ALEX,   "Thank you for the delicious meal."),
    ("19-waiter", WAITER, "My pleasure! Would you like the bill?"),
    ("20-jamie",  JAMIE,  "Yes, please!"),
]

async def gen_one(key, voice, text):
    fname = OUT / f"{key}.mp3"
    if fname.exists():
        print(f"skip  {fname.name}"); return
    tts = edge_tts.Communicate(text, voice, rate="-4%")
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
