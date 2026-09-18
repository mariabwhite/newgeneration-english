"""Generate the family-trip reading audio for julia-pet-shop-snail.
Multi-voice narration via edge-tts, glued via ffmpeg concat.
Run: py -3 _gen.py
"""
import asyncio, sys, subprocess
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent

NARR = "en-GB-LibbyNeural"
DAD  = "en-GB-RyanNeural"
MUM  = "en-GB-SoniaNeural"
JOHN = "en-GB-ThomasNeural"
JULIA = "en-GB-MaisieNeural"

# Each turn: (voice, text, rate)
TURNS = [
    (NARR, "A Sunday at Whiskers and Wings. A story for Julia.", "-6%"),
    (NARR, "Last Sunday morning, Julia's family had a big argument. It started at breakfast.", "-6%"),
    (NARR, "Julia's dad said:", "-6%"),
    (DAD,  "We should get a dog. A dog is a real pet.", "-8%"),
    (NARR, "Julia's mum shook her head.", "-6%"),
    (MUM,  "A dog is too much work. Let's get a small bird — a beautiful yellow canary. Birds are quiet.", "-8%"),
    (NARR, "John, Julia's little brother, banged the table.", "-6%"),
    (JOHN, "No! I want a lizard! Lizards are cool! My friend Toby has a green one.", "-4%"),
    (NARR, "Julia listened to everyone. Then she said calmly:", "-6%"),
    (JULIA, "I want a snail.", "-4%"),
    (NARR, "Everybody laughed.", "-6%"),
    (JOHN, "A snail is not a pet, Julia!", "-4%"),
    (NARR, "But Julia's mum smiled.", "-6%"),
    (MUM,  "OK. Let's all go to the pet shop and decide together.", "-8%"),
    (NARR, "They all put on their jackets and walked to Whiskers and Wings, the small pet shop on the corner.", "-6%"),
    (NARR, "When they came in, Julia's dad went straight to the puppies. He looked at a golden brown one and said:", "-6%"),
    (DAD,  "This dog is perfect!", "-8%"),
    (NARR, "Julia's mum was already talking to a yellow canary in a big cage.", "-6%"),
    (MUM,  "Hello, beautiful bird!", "-8%"),
    (NARR, "John was sitting on the floor, watching two little lizards behind the glass.", "-6%"),
    (NARR, "Julia walked slowly to the back of the shop. There, on a wooden shelf, she saw a small glass tank with one tiny snail inside. The snail was moving very, very slowly across a green leaf. Julia smiled.", "-6%"),
    (JULIA, "Perfect.", "-4%"),
    (NARR, "They came back together at the cash desk. Dad said:", "-6%"),
    (DAD,  "The dog costs four hundred pounds.", "-8%"),
    (NARR, "Mum said:", "-6%"),
    (MUM,  "The canary is seventy-five pounds.", "-8%"),
    (NARR, "John said:", "-6%"),
    (JOHN, "The lizard is one hundred and twenty pounds!", "-4%"),
    (NARR, "Julia opened her small hand. Inside was one pound coin.", "-6%"),
    (JULIA, "The snail is one pound.", "-4%"),
    (NARR, "For a moment, everyone was quiet. Then Dad laughed.", "-6%"),
    (DAD,  "Well, Julia wins. Let's take the snail home.", "-8%"),
    (NARR, "Julia named the snail Turbo. Barsik, their old grey cat, was not sure at first. But by the evening, he was sitting next to the tank and watching Turbo very carefully. Turbo did not move. Barsik did not move. The house was quiet, for the first time all Sunday.", "-6%"),
]


async def gen_turn(idx, voice, text, rate):
    tmp = HERE / f"__t{idx:03d}.mp3"
    # try preferred voice, fall back to Ryan/Sonia
    try:
        comm = edge_tts.Communicate(text, voice=voice, rate=rate)
        await comm.save(str(tmp))
    except Exception as e:
        fallback = "en-GB-RyanNeural" if voice.endswith("ThomasNeural") else "en-GB-SoniaNeural"
        print(f"  voice {voice} failed → {fallback} · {e}")
        comm = edge_tts.Communicate(text, voice=fallback, rate=rate)
        await comm.save(str(tmp))
    return tmp


async def main():
    print("julia-pet-shop-snail · family story · edge-tts")
    silence = HERE / "__silence.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", "0.4", "-q:a", "9", "-acodec", "libmp3lame", str(silence)
    ], check=True, capture_output=True)

    tmp_files = []
    for i, (voice, text, rate) in enumerate(TURNS):
        tmp = await gen_turn(i, voice, text, rate)
        tmp_files.append(tmp)
        print(f"  turn {i:02d} · {voice.split('-')[-1][:6]} · {text[:60]}…")

    listf = HERE / "__concat.txt"
    with listf.open("w", encoding="utf-8") as f:
        for i, t in enumerate(tmp_files):
            f.write(f"file '{t.name}'\n")
            if i < len(tmp_files) - 1:
                f.write(f"file '{silence.name}'\n")

    out = HERE / "story-family-trip.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
        "-c", "copy", str(out)
    ], check=True, capture_output=True, cwd=str(HERE))

    listf.unlink()
    silence.unlink()
    for t in tmp_files:
        t.unlink()
    print(f"wrote {out.name}")


if __name__ == "__main__":
    asyncio.run(main())
