"""
v6 · rewrite 6 L/R drill clips with REAL direction sentences, not body-part baby stuff.
Each sentence embeds a clear L or R so Katya has to listen for the actual direction word.
"""
import asyncio, pathlib
import edge_tts

ROOT = pathlib.Path(__file__).parent
LR_DIR = ROOT / "lr"
LR_DIR.mkdir(exist_ok=True)

VOICE = "en-GB-SoniaNeural"
RATE = "-5%"

LR = {
    "lr-1": "Turn left at the corner, then keep going straight.",
    "lr-2": "Take the second right after the bridge.",
    "lr-3": "Walk along the left-hand side of the park.",
    "lr-4": "The cafe is on your right, next to the little bakery.",
    "lr-5": "Cross the road and keep to the left.",
    "lr-6": "Go straight on, then turn right at the traffic lights.",
}

async def tts(text, out):
    if out.exists():
        out.unlink()
    for a in range(3):
        try:
            c = edge_tts.Communicate(text, VOICE, rate=RATE)
            await c.save(str(out))
            s = out.stat().st_size
            if s < 2000:
                raise RuntimeError(f"too small {s}")
            print(f"[ok] {out.name} ({s} B)")
            return
        except Exception as e:
            print(f"[retry {a+1}] {e}")
            if out.exists(): out.unlink()
            await asyncio.sleep(5)
    print(f"[FAIL] {out.name}")

async def main():
    print(f"=== 6 new L/R direction sentences -> {LR_DIR} ===")
    for slug, text in LR.items():
        await tts(text, LR_DIR / f"{slug}.mp3")
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
