# -*- coding: utf-8 -*-
"""Per-park narration mp3s for Section 06+ · World's famous parks."""
import asyncio, sys
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).parent
VOICE = "en-GB-SoniaNeural"  # same narrator as world-parks-narration

PARKS = [
    ("park-01-kingda-ka",
     "Kingda Ka is the tallest roller coaster in the world — one hundred and thirty-nine metres tall. "
     "It goes from zero to two hundred and six kilometres per hour in just three-point-five seconds. "
     "Riders wear special safety harnesses. The ride only lasts twenty-eight seconds, "
     "but the queue is often two hours long. It closed in twenty twenty-four — too many breakdowns."),

    ("park-02-formula-rossa",
     "Formula Rossa is the fastest roller coaster in the world — two hundred and forty kilometres per hour. "
     "Faster than a Formula One car at launch. "
     "Riders must wear safety goggles because the wind is so strong. "
     "The launch is like an airplane taking off. Minimum height: one hundred and thirty centimetres."),

    ("park-03-steel-dragon",
     "Steel Dragon Two Thousand is the longest roller coaster in the world — two-and-a-half kilometres. "
     "It has a big drop of ninety-three metres. "
     "In two thousand and three a wheel fell off during a ride — no one was hurt, "
     "but the ride was closed for many months for repairs. Now it is one of the safest in Japan."),

    ("park-04-action-park",
     "Action Park in New Jersey in the nineteen-eighties was famous for the most dangerous water rides in history. "
     "A looping water slide that no one could finish. A wave pool nicknamed The Grave Pool. "
     "More than one hundred accidents. The park closed in nineteen ninety-six. "
     "Now there is a Netflix documentary about it."),

    ("park-05-mckamey",
     "McKamey Manor in Tennessee is called the scariest haunted house in the world. "
     "The tour lasts ten hours — actors chase you, scream, throw water. "
     "The owner offered twenty thousand dollars to anyone who finished the whole tour. "
     "Nobody has ever won. Visitors must sign a forty-page waiver and be over twenty-one. "
     "Not for children."),
]

async def gen_one(key, text):
    fname = OUT / f"{key}.mp3"
    if fname.exists():
        print(f"skip  {fname.name}"); return
    tts = edge_tts.Communicate(text, VOICE, rate="-2%")
    await tts.save(str(fname))
    print(f"done  {fname.name}")

async def main():
    for k, t in PARKS:
        try:
            await gen_one(k, t)
        except Exception as e:
            print(f"FAIL  {k}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
