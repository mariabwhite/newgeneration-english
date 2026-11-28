"""
v2 · build all direction-PHRASE audio for Katya L12.

Three folders:
  dir/       13 phrase clips, one per mini-schema in the showcase section
  ex2/        6 clips — the completed jumbled sentences from Section 4
  roleplay/   5 clips — the example tourist-helper lines in Section 7
  ielts/      6 clips — the signpost phrases in Section 8

Everything else (1.30, IELTS guide, vocab/*) is already built — not touched.
"""
import asyncio, pathlib
import edge_tts

ROOT = pathlib.Path(__file__).parent
VOICE = "en-GB-SoniaNeural"
RATE = "-6%"   # a bit slower than natural, child-friendly, still fluent

# ---- 13 direction-phrase cards ----
DIR = {
    "dir-go-along":          "Go along this lane.",
    "dir-go-across":         "Go across the field.",
    "dir-go-past":           "Go past the pond.",
    "dir-go-through":        "Go through the gate.",
    "dir-go-into":           "Go into the bakery.",
    "dir-turn-right-onto":   "Turn right onto the lane.",
    "dir-go-straight-on":    "Go straight on.",
    "dir-take-first-right":  "Take the first right.",
    "dir-turn-left-corner":  "Turn left at the corner.",
    "dir-follow-footpath":   "Just follow the footpath.",
    "dir-walk-to-end":       "Walk to the end of the road.",
    "dir-on-your-left":      "It's on your left.",
    "dir-cross-road":        "Cross the road at the lights.",
}

# ---- ex.2 completed sentences ----
EX2 = {
    "ex2-1": "Go straight on.",
    "ex2-2": "Walk to the end of the lane.",
    "ex2-3": "Turn right into the lane.",
    "ex2-4": "Go along this road.",
    "ex2-5": "Take the first right.",
    "ex2-6": "Go through the gate on your left.",
}

# ---- role-play example steps (§7) ----
RP = {
    "rp-1": "No, it's only a few minutes' walk.",
    "rp-2": "Go along the lane towards the pond.",
    "rp-3": "Then go past the pond and across the small bridge.",
    "rp-4": "Go through the gate on your right.",
    "rp-5": "The church is on your left — you can't miss it.",
}

# ---- IELTS signpost phrases (§8 tip card) ----
SIG = {
    "sig-straight-ahead": "Straight ahead of you.",
    "sig-just-past":      "Just past the cafe.",
    "sig-opposite":       "Opposite the entrance.",
    "sig-far-corner":     "In the far corner.",
    "sig-next-to":        "Next to the big tree.",
    "sig-short-walk":     "A short walk down the path.",
}

GROUPS = [("dir", DIR), ("ex2", EX2), ("roleplay", RP), ("ielts", SIG)]

async def tts(text, out, voice=VOICE, rate=RATE):
    if out.exists() and out.stat().st_size > 1500:
        print(f"  [skip] {out.relative_to(ROOT)} ({out.stat().st_size} B)")
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
    for folder, mapping in GROUPS:
        d = ROOT / folder
        d.mkdir(exist_ok=True)
        print(f"\n=== {folder} ({len(mapping)}) ===")
        for slug, phrase in mapping.items():
            await tts(phrase, d / f"{slug}.mp3")
    print("\nDone.")

if __name__ == "__main__":
    asyncio.run(main())
