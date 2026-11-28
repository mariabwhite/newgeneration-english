"""
v7 · 3 city-navigation clue clips for §0a.
Katya listens to each clue and matches it to one of 12 urban places.
Real B1+ direction collocations: 'pedestrian crossing', 'roundabout',
'take the second exit', 'just past the ...', 'between the X and the Y'.
"""
import asyncio, pathlib
import edge_tts

ROOT = pathlib.Path(__file__).parent
HUNT_DIR = ROOT / "hunt"
HUNT_DIR.mkdir(exist_ok=True)

VOICE_F = "en-GB-SoniaNeural"
VOICE_M = "en-GB-RyanNeural"
RATE = "-4%"

# answer: post office
CLUE_1 = (
    "Go straight along the main street until you reach the bank on the corner. "
    "Turn left there, and it's the second building on your right, "
    "between the florist and the dry cleaner's. "
    "You'll spot the big red post box outside — you can't miss it."
)

# answer: bakery
CLUE_2 = (
    "Cross the pedestrian crossing and turn right. "
    "Walk past the bus stop and keep going for about fifty metres. "
    "It's on your left, just before the bookshop. "
    "You'll smell the fresh bread before you see it."
)

# answer: cash machine (ATM)
CLUE_3 = (
    "Go round the roundabout and take the second exit. "
    "Walk past the pharmacy on your right, then cross the road at the lights. "
    "It's right there, just outside the main bank next to the entrance. "
    "The green sign says ATM."
)

CLUES = [
    ("hunt-clue-1", CLUE_1, VOICE_F),
    ("hunt-clue-2", CLUE_2, VOICE_M),
    ("hunt-clue-3", CLUE_3, VOICE_F),
]

async def tts(text, out, voice):
    if out.exists():
        out.unlink()
    for a in range(3):
        try:
            c = edge_tts.Communicate(text, voice, rate=RATE)
            await c.save(str(out))
            s = out.stat().st_size
            if s < 5000:
                raise RuntimeError(f"too small {s}")
            print(f"[ok] {out.name} ({s} B, {voice})")
            return
        except Exception as e:
            print(f"[retry {a+1}] {e}")
            if out.exists(): out.unlink()
            await asyncio.sleep(5)
    print(f"[FAIL] {out.name}")

async def main():
    print(f"=== 3 city-hunt clues -> {HUNT_DIR} ===")
    for slug, text, voice in CLUES:
        await tts(text, HUNT_DIR / f"{slug}.mp3", voice)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
