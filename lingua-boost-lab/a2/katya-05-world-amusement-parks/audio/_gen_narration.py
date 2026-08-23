# -*- coding: utf-8 -*-
"""60-sec narration about world amusement parks for the video overlay."""
import asyncio, sys
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).parent
VOICE = "en-GB-SoniaNeural"  # Katya's voice for consistency

TEXT = (
"Welcome to the wildest amusement parks on Earth. "
"In New Jersey stands Kingda Ka — one hundred and thirty-nine metres tall, "
"faster than a car chase, from zero to two hundred and six kilometres per hour in just three-point-five seconds. "
"In the desert of Abu Dhabi, Formula Rossa launches you at two hundred and forty kilometres per hour — "
"faster than a Formula One car at start. Riders wear special goggles to protect their eyes from the wind. "
"In Japan, Steel Dragon Two Thousand is two-and-a-half kilometres long, with a ninety-three metre drop. "
"Some parks are famous for the wrong reasons. "
"Action Park in the nineteen-eighties had a looping water slide no one could finish. Over one hundred accidents. Closed in nineteen-ninety-six. "
"And the scariest one? McKamey Manor in Tennessee — a ten-hour haunted house tour. Twenty thousand dollars for anyone who can finish. "
"Nobody ever has. Ready for the ride?"
)

async def main():
    target = OUT / "world-parks-narration.mp3"
    if target.exists():
        print(f"skip  {target.name}"); return
    tts = edge_tts.Communicate(TEXT, VOICE, rate="+2%")
    await tts.save(str(target))
    print(f"done  {target.name}  ({VOICE})")

if __name__ == "__main__":
    asyncio.run(main())
