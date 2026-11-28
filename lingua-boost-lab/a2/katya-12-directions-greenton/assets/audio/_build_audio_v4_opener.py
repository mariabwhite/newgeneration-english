"""
v4 · opener audio for the 4 warm-up micro-sections.

Three folders:
  opener/   hook clue + answer reveal
  lr/       6 left-right body-check commands
  compass/  8 compass-direction single-word clips (N/S/E/W + diagonals)
"""
import asyncio, pathlib
import edge_tts

ROOT = pathlib.Path(__file__).parent
VOICE_F = "en-GB-SoniaNeural"
VOICE_M = "en-GB-RyanNeural"
RATE = "-5%"

# ---- Section 0a HOOK — one treasure-hunt clue + 3 wrong/right reveals ----
OPENER = {
    "hook-clue":
        "Here's the first clue: walk straight ahead, go through the big glass doors, "
        "then take the second right. The surprise is on your left, next to the small fountain.",
    "hook-reveal-right":
        "Correct — it's at the cafe! You went through the doors, took the second right, "
        "and the cafe is on your left by the fountain.",
    "hook-reveal-wrong-park":
        "Not quite — the clue said 'through the glass doors', not 'past them'. The park is outside. Try again.",
    "hook-reveal-wrong-shop":
        "Close — but you took the first right, not the second. The shop is on the first right. Try again.",
}

# ---- Section 0b LEFT vs RIGHT body-check ----
LR = {
    "lr-1": "Touch your left ear.",
    "lr-2": "Raise your right hand.",
    "lr-3": "Point to the left.",
    "lr-4": "Step to the right.",
    "lr-5": "Turn your head to the left.",
    "lr-6": "Wave your right hand.",
}

# ---- Section 0c COMPASS ----
COMPASS = {
    "n":  "North.",
    "s":  "South.",
    "e":  "East.",
    "w":  "West.",
    "ne": "North-east.",
    "nw": "North-west.",
    "se": "South-east.",
    "sw": "South-west.",
}

GROUPS = [("opener", OPENER, VOICE_F), ("lr", LR, VOICE_F), ("compass", COMPASS, VOICE_M)]

async def tts(text, out, voice, rate=RATE):
    if out.exists() and out.stat().st_size > 1500:
        print(f"  [skip] {out.relative_to(ROOT)}")
        return
    for a in range(3):
        try:
            c = edge_tts.Communicate(text, voice, rate=rate)
            await c.save(str(out))
            s = out.stat().st_size if out.exists() else 0
            if s < 1000:
                raise RuntimeError(f"too small {s}")
            print(f"  [ok]   {out.relative_to(ROOT)} ({s} B)")
            return
        except Exception as e:
            print(f"  [retry {a+1}] {out.name}: {e}")
            if out.exists():
                out.unlink()
            await asyncio.sleep(5)
    print(f"  [FAIL] {out.name}")

async def main():
    for folder, mapping, voice in GROUPS:
        d = ROOT / folder
        d.mkdir(exist_ok=True)
        print(f"\n=== {folder} ({len(mapping)}) ===")
        for slug, text in mapping.items():
            await tts(text, d / f"{slug}.mp3", voice)
    print("\nDone.")

if __name__ == "__main__":
    asyncio.run(main())
