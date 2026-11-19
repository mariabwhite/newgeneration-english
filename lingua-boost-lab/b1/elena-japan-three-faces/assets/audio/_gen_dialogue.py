"""Generate dialogue-yuki-sakura.mp3 — 6 alternating lines, 2 UK female voices, 0.6s silence between.

Needs ffmpeg on PATH (comes with Shotcut on Maria's machine).
"""
import asyncio, os, subprocess, tempfile, shutil, edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dialogue-yuki-sakura.mp3")

LINES = [
    ("yuki",   "en-GB-LibbyNeural", "Honestly, Tokyo really gets on my nerves these days. During rush hour there is nowhere to sit and nobody is smiling."),
    ("sakura", "en-GB-SoniaNeural", "I see your point, but I don't completely agree. Everything in Tokyo is so convenient — trains, food, technology. Everyone complains, but everyone stays."),
    ("yuki",   "en-GB-LibbyNeural", "Maybe. But in Kyoto I feel something different. Somebody always has time for you. Nobody is in a hurry."),
    ("sakura", "en-GB-SoniaNeural", "That's a fair point. My grandmother lives in Okinawa, and she says exactly the same thing — nothing is urgent there, and everybody knows everybody."),
    ("yuki",   "en-GB-LibbyNeural", "Would you ever move to Okinawa, then?"),
    ("sakura", "en-GB-SoniaNeural", "Not now. I love the pressure of Tokyo. But someday, yes — when I'm tired of everything."),
]

async def gen_line(path, text, voice, attempt=1):
    try:
        comm = edge_tts.Communicate(text, voice, rate="-4%")
        await comm.save(path)
        if os.path.getsize(path) < 2000:
            raise RuntimeError("tiny file")
    except Exception as e:
        print(f"[err {attempt}] {os.path.basename(path)}: {e}")
        if attempt < 4:
            await asyncio.sleep(5)
            if os.path.exists(path):
                os.remove(path)
            await gen_line(path, text, voice, attempt + 1)
        else:
            raise

async def main():
    if os.path.exists(OUT) and os.path.getsize(OUT) > 2000:
        print(f"[skip] {os.path.basename(OUT)} exists")
        return
    tmp = tempfile.mkdtemp(prefix="dlg_")
    try:
        parts = []
        for i, (speaker, voice, text) in enumerate(LINES):
            p = os.path.join(tmp, f"{i:02d}_{speaker}.mp3")
            await gen_line(p, text, voice)
            parts.append(p)
            print(f"[ok] {speaker}: {len(text)} chars")

        silence = os.path.join(tmp, "silence.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
            "-t", "0.6", "-q:a", "9", "-acodec", "libmp3lame", silence
        ], check=True, capture_output=True)

        listfile = os.path.join(tmp, "list.txt")
        with open(listfile, "w", encoding="utf-8") as f:
            for i, p in enumerate(parts):
                f.write(f"file '{p.replace(chr(92), '/')}'\n")
                if i < len(parts) - 1:
                    f.write(f"file '{silence.replace(chr(92), '/')}'\n")

        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", listfile, "-c:a", "libmp3lame", "-b:a", "96k", OUT
        ], check=True, capture_output=True)

        print(f"[done] {os.path.basename(OUT)} ({os.path.getsize(OUT) // 1024} KB)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    asyncio.run(main())
