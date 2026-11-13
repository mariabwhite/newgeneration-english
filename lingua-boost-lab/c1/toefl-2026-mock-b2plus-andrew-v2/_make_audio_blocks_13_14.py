"""Generate the 11 missing audio clips for v2 Mock: Section 13 (lnr × 7) + Section 14 (intv × 4)."""
import asyncio, os, sys, time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import edge_tts

HERE = Path(__file__).resolve().parent
OUT = HERE / "audio"
OUT.mkdir(exist_ok=True)

JOANNA = "en-US-JennyNeural"
MATTHEW = "en-US-GuyNeural"

CLIPS = [
    ("lnr-13-01.mp3", JOANNA,  "-8%", "My train arrives at ten past six."),
    ("lnr-13-02.mp3", MATTHEW, "-8%", "The parcel should arrive sometime on Wednesday afternoon."),
    ("lnr-13-03.mp3", JOANNA,  "-8%", "She's been teaching at the same school for almost twenty years."),
    ("lnr-13-04.mp3", MATTHEW, "-8%", "If I'd known you were coming, I'd have made a proper dinner."),
    ("lnr-13-05.mp3", JOANNA,  "-8%", "He mentioned that he hadn't been feeling well since Monday morning, actually."),
    ("lnr-13-06.mp3", MATTHEW, "-8%", "The new café on the corner has become so popular that you often have to queue."),
    ("lnr-13-07.mp3", JOANNA,  "-8%", "Although the meeting ran much longer than expected, we eventually agreed on a reasonable plan for next quarter."),

    ("intv-14-01.mp3", JOANNA,  "+0%", "Describe how you usually spend a Sunday. What makes it different from the rest of the week for you?"),
    ("intv-14-02.mp3", MATTHEW, "+0%", "Would you rather live in a big city or a small town? Give two concrete reasons."),
    ("intv-14-03.mp3", JOANNA,  "+0%", "Tell me about a meal that you remember clearly — what it was, where you had it, and why it stayed with you."),
    ("intv-14-04.mp3", MATTHEW, "+0%", "If you had one extra free day a week, how would you most likely spend it, and why?"),
]


async def tts(fname, voice, rate, text):
    path = OUT / fname
    for attempt in range(1, 4):
        try:
            if path.exists() and path.stat().st_size > 0:
                print(f"  SKIP {fname}  ({path.stat().st_size // 1024} KB — exists)")
                return
            comm = edge_tts.Communicate(text=text, voice=voice, rate=rate)
            await comm.save(str(path))
            if path.exists() and path.stat().st_size > 0:
                print(f"  OK   {fname}  ({path.stat().st_size // 1024} KB)")
                return
        except Exception as e:
            print(f"  [{attempt}] {fname} failed: {e}")
            if path.exists() and path.stat().st_size == 0:
                path.unlink()
            time.sleep(5)
    print(f"  FAIL {fname} after 3 attempts")


async def main():
    print(f"generating {len(CLIPS)} clips -> {OUT}")
    for clip in CLIPS:
        await tts(*clip)
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
