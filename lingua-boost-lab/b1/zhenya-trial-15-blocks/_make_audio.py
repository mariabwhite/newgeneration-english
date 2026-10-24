"""Generate 2 listening audios for Zhenya trial.
listening-A-01.mp3 - 9-turn café order dialogue (Jenny + Christopher ~45s)
listening-B-01.mp3 - Dasha monologue 10 sentences (Aria slower ~70s)
"""
import asyncio, os, subprocess, time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audio")
TMP = os.path.join(OUT, "_tmp")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

JENNY = "en-US-JennyNeural"
RYAN = "en-GB-RyanNeural"
ARIA = "en-US-AriaNeural"

DIALOG_A = [
    (RYAN,  "Hi there, welcome to Rosa's café. What can I get for you?"),
    (JENNY, "Hi! Could I have a medium Margherita pizza, please?"),
    (RYAN,  "Sure. Any extra toppings? We've got mushrooms, olives, pepperoni, extra cheese."),
    (JENNY, "Mmm, could you add mushrooms? But no olives, I don't like them."),
    (RYAN,  "Mushrooms, got it. Anything to drink?"),
    (JENNY, "An orange juice, please. A big one."),
    (RYAN,  "Perfect. And would you like to see our dessert menu? Today we have chocolate cake and apple pie."),
    (JENNY, "Oh yes, please — I'll have the chocolate cake after the pizza."),
    (RYAN,  "Lovely. I'll bring it all over in a few minutes."),
]

MONO_B = (
    "Hi, I'm Dasha. I'm fourteen and I study at home — people call it homeschool. "
    "My favourite subject is biology, because I love animals and I want to be a vet one day. "
    "I'm not so good at maths yet, but I'm trying. "
    "A typical week looks like this: Monday to Thursday I do my lessons online in the morning, from nine to one. "
    "After lunch I'm free. I draw a lot, I walk my dog Boris, and I read. "
    "On Fridays I see my two best friends — we usually meet at a café or go roller-skating in the park. "
    "So, two friends every single week. "
    "On Saturdays we go to my grandma's dacha outside the city. "
    "My parents say homeschool is only possible because I'm quite responsible. "
    "Honestly, I love it. I feel calmer than when I was in a regular school."
)


async def tts(text, voice, out_path, rate="+0%"):
    for attempt in range(3):
        try:
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                return
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(out_path)
            if os.path.getsize(out_path) > 0:
                return
        except Exception as e:
            print(f"  [{attempt+1}] {os.path.basename(out_path)} fail: {e}")
            if os.path.exists(out_path) and os.path.getsize(out_path) == 0:
                os.remove(out_path)
            time.sleep(5)
    raise RuntimeError(f"Failed: {out_path}")


def ffconcat(parts, out_mp3, silence_sec=0.35):
    silence = os.path.join(TMP, "_silence.mp3")
    if not os.path.exists(silence):
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            "anullsrc=channel_layout=mono:sample_rate=24000",
            "-t", str(silence_sec), "-q:a", "9", silence
        ], check=True, capture_output=True)
    lst = os.path.join(TMP, "_list.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for i, p in enumerate(parts):
            f.write(f"file '{p.replace(chr(92), '/')}'\n")
            if i < len(parts) - 1:
                f.write(f"file '{silence.replace(chr(92), '/')}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", lst, "-c", "copy", out_mp3
    ], check=True, capture_output=True)


async def main():
    print("listening-A-01.mp3 (dialogue 9 turns)")
    parts = []
    for i, (voice, line) in enumerate(DIALOG_A, 1):
        p = os.path.join(TMP, f"a-t{i:02d}.mp3")
        await tts(line, voice, p, rate="-5%")
        parts.append(p)
    out = os.path.join(OUT, "listening-A-01.mp3")
    ffconcat(parts, out, silence_sec=0.4)
    print(f"  {os.path.getsize(out)} bytes")

    print("listening-B-01.mp3 (Dasha monologue slower)")
    out = os.path.join(OUT, "listening-B-01.mp3")
    await tts(MONO_B, ARIA, out, rate="-10%")
    print(f"  {os.path.getsize(out)} bytes")

    print("DONE")

if __name__ == "__main__":
    asyncio.run(main())
