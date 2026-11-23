"""Generate two listening audios for Julia November Workbook.
1) monday-catchup.mp3  — ~60s follow-up to the Sunday race
2) pet-shop-visit.mp3  — ~45s reading scene for section 3
"""
import asyncio, pathlib, time
import edge_tts

HERE = pathlib.Path(__file__).parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)

NARR_GB = "en-GB-LibbyNeural"
NARR_US = "en-US-AriaNeural"

CLIPS = {
    "monday-catchup": (NARR_GB, "-5%", (
        "Monday morning. Julia walked to school with Emma. "
        "The silver medal was in her backpack. "
        "At break time, everyone wanted to see it. "
        "'Were you nervous before the race?' asked Masha. "
        "'A little,' Julia smiled. 'But Emma said break a leg, and then I ran.' "
        "'And John?' asked Vova. 'He came first. He always does.' "
        "After school, they all walked to the park again. "
        "Barsik the cat was waiting on the bench. "
        "Julia opened her little bubble bottle and blew one slow, round bubble into the air. "
        "'I'm going to run every Sunday now,' she said. 'And one day I will run in a real race in London.' "
        "The bubble floated up and popped. The wish was in the sky."
    )),
    "pet-shop-visit": (NARR_US, "-4%", (
        "Last Saturday Julia and Emma went to the pet shop. "
        "They wanted to see Turbo the snail again. "
        "The shopkeeper, Mr Brown, was feeding a parrot. "
        "'Good morning, girls! How is Turbo?' he asked. "
        "'He's very happy,' said Julia. 'He loves his green leaves.' "
        "Emma pointed at a cage of kittens. "
        "'Look, Julia! Can we have one?' "
        "'Maybe one day,' Julia laughed. 'But first, let's buy more leaves for Turbo.'"
    )),
}

async def gen(name, voice, rate, text):
    out = AUDIO / f"{name}.mp3"
    for attempt in range(1, 4):
        try:
            print(f"[try {attempt}] {out.name} · {voice}")
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(str(out))
            if out.exists() and out.stat().st_size > 1000:
                print(f"  OK · {out.stat().st_size//1024} KB")
                return
            print("  empty file, retry")
            out.unlink(missing_ok=True)
        except Exception as e:
            print(f"  ERR {e}")
            if out.exists() and out.stat().st_size < 1000:
                out.unlink(missing_ok=True)
        time.sleep(5)
    raise RuntimeError(f"failed {name} after 3 tries")

async def main():
    for name, (voice, rate, text) in CLIPS.items():
        await gen(name, voice, rate, text)

asyncio.run(main())
