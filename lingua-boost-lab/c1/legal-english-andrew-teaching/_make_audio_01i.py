"""Generate 3 dialog audios for section 01i.
Each: 6 turns Jenny + Christopher, concatenated with 0.35s silence.
"""
import asyncio, os, subprocess, time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audio")
TMP = os.path.join(OUT, "_tmp01i")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

J = "en-US-JennyNeural"
C = "en-US-ChristopherNeural"

D1 = [
    (J, "My neighbour's dog bit me yesterday. The owner says it's my fault."),
    (C, "Did you take photos?"),
    (J, "Yeah, and I went to a doctor."),
    (C, "Then you can take him to small claims court. Keep the medical bills — that's your damages."),
    (J, "Should I warn him first?"),
    (C, "Send a short demand letter. If he ignores it, file."),
]

D2 = [
    (J, "They changed my job description without asking me. Is that legal?"),
    (C, "Depends on your contract. Did you sign anything that allows reasonable changes?"),
    (J, "I think so."),
    (C, "Then unfortunately they can."),
    (J, "So I can't do anything?"),
    (C, "If you want to bring an action, you'd need to show the change is a material breach — and that's a steep hill. Try HR first."),
]

D3 = [
    (C, "They want me to sign a non-compete. Two years, worldwide."),
    (J, "That's aggressive."),
    (C, "Really?"),
    (J, "Push back — most courts won't enforce a non-compete that broad."),
    (C, "What if they refuse to narrow it?"),
    (J, "Then you walk. Or sign and know it probably wouldn't hold up if they ever tried to sue over it."),
]


async def tts(text, voice, out_path):
    for attempt in range(3):
        try:
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                return
            comm = edge_tts.Communicate(text, voice)
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


async def build(dialog, name):
    print(f"{name}")
    parts = []
    for i, (voice, line) in enumerate(dialog, 1):
        p = os.path.join(TMP, f"{name}-t{i:02d}.mp3")
        await tts(line, voice, p)
        parts.append(p)
    out = os.path.join(OUT, f"{name}.mp3")
    ffconcat(parts, out, silence_sec=0.35)
    print(f"  {os.path.getsize(out)} bytes")


async def main():
    await build(D1, "audio-01i-01")
    await build(D2, "audio-01i-02")
    await build(D3, "audio-01i-03")
    print("DONE")

if __name__ == "__main__":
    asyncio.run(main())
