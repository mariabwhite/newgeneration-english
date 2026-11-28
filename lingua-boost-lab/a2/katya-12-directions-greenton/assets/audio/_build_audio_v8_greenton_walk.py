"""
v8 · 3 Greenton-map walk narrations for §03.
Each one starts at bus stop B and ends at a different numbered place.
Katya has to identify the final place from the 13 options on the map.
"""
import asyncio, pathlib
import edge_tts

ROOT = pathlib.Path(__file__).parent
G_DIR = ROOT / "greenton"
G_DIR.mkdir(exist_ok=True)

VOICE_F = "en-GB-SoniaNeural"
VOICE_M = "en-GB-RyanNeural"
RATE = "-6%"

# answer: 21 church
WALK_1 = (
    "You're standing at the bus stop, point B. "
    "Walk straight ahead along the main lane. "
    "You'll pass the orange farmhouse on your left — that's number sixteen. "
    "Keep going, cross the small stream by the wooden bridge. "
    "Now turn right and walk up the hill past the yellow house on your right. "
    "At the top of the hill you'll see a big village with a tall spire. "
    "Stop in front of the main building. Where are you now?"
)

# answer: 15 small blue cottage
WALK_2 = (
    "Start at the bus stop. Walk down the lane with the field on your right. "
    "Go past the big barn — that's the building with a curved grey roof. "
    "Keep going along the fence, past the orange farmhouse. "
    "You'll see a tiny thatched cottage painted pale blue, right by the wooden fence. "
    "Stop there. Where are you?"
)

# answer: 20 pond
WALK_3 = (
    "From the bus stop, walk ahead past the barn on your right. "
    "Then turn left and follow the small footpath across the grass. "
    "Go down the hill, past the fence. "
    "You'll come to a flat, open area with water lilies on the surface. "
    "The red tractor is parked just beyond it. Where are you standing?"
)

WALKS = [
    ("greenton-walk-1", WALK_1, VOICE_F),
    ("greenton-walk-2", WALK_2, VOICE_M),
    ("greenton-walk-3", WALK_3, VOICE_F),
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
    print(f"=== 3 Greenton walks -> {G_DIR} ===")
    for slug, text, voice in WALKS:
        await tts(text, G_DIR / f"{slug}.mp3", voice)
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
