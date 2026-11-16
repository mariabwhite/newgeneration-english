"""Generate 11 audio clips for Varvara L13 Mock: Section 13 (lnr × 7) + Section 14 (intv × 4)."""
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
    ("lnr-13-01.mp3", JOANNA,  "-8%", "I'll pick up the tickets tomorrow."),
    ("lnr-13-02.mp3", MATTHEW, "-8%", "The exhibition opens on the first of April."),
    ("lnr-13-03.mp3", JOANNA,  "-8%", "She's been working at the gallery since late September."),
    ("lnr-13-04.mp3", MATTHEW, "-8%", "If we'd left earlier, we would have caught the earlier train."),
    ("lnr-13-05.mp3", JOANNA,  "-8%", "He mentioned that he hadn't been feeling particularly well since last Thursday."),
    ("lnr-13-06.mp3", MATTHEW, "-8%", "The small bookshop on Charlotte Street has become so popular that queues form outside."),
    ("lnr-13-07.mp3", JOANNA,  "-8%", "Although the lecture ran considerably longer than expected, we eventually agreed on a sensible plan for next term."),

    ("intv-14-01.mp3", JOANNA,  "+0%", "Describe how you usually spend a Saturday morning. What do you look forward to most, and why?"),
    ("intv-14-02.mp3", MATTHEW, "+0%", "Would you rather travel in a group or on your own? Give two concrete reasons for your choice."),
    ("intv-14-03.mp3", JOANNA,  "+0%", "Tell me about a place that you remember clearly from your childhood — what it looked like, what you did there, and why it has stayed with you."),
    ("intv-14-04.mp3", MATTHEW, "+0%", "If you had one extra afternoon off each week, how would you most likely spend it, and why?"),
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
