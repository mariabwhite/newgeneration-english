# -*- coding: utf-8 -*-
"""
Generate the dinner.mp3 for Sonya's diagnostic (section 17 · Listening).
Two-voice dialogue: mum (en-GB Sonia) + Sonya (en-GB Maisie).
Concatenates 5 turns → single mp3 via ffmpeg-free approach: shell out to
edge-tts for each turn into a temp file, then use `pydub` if available,
else raw MP3 concat (frames compatible when produced by same TTS engine).
"""
import asyncio
import subprocess
import tempfile
import os
from pathlib import Path

OUT = Path(__file__).parent / "dinner.mp3"

# 5 turns; alternate voices
TURNS = [
    ("Mum",   "Sonya, dinner is almost ready. Can you set the table, please?",  "en-GB-SoniaNeural"),
    ("Sonya", "Sure. How many plates? Just us three?",                           "en-GB-MaisieNeural"),
    ("Mum",   "Four — Dad is coming home in ten minutes. And bring the salt, it's on the top shelf.", "en-GB-SoniaNeural"),
    ("Sonya", "Do we have any bread?",                                           "en-GB-MaisieNeural"),
    ("Mum",   "Yes, there's some in the fridge. Take it out. And, Sonya — please don't forget your homework tonight, all right?", "en-GB-SoniaNeural"),
]

async def synth_one(text, voice, out_path):
    import edge_tts
    # Slight pauses via slower rate for L2 listeners
    communicate = edge_tts.Communicate(text, voice, rate="-8%")
    await communicate.save(str(out_path))

async def main():
    tmpdir = Path(tempfile.mkdtemp(prefix="sonya_dinner_"))
    parts = []
    for i, (who, text, voice) in enumerate(TURNS, 1):
        p = tmpdir / f"turn_{i:02d}.mp3"
        print(f"[{i}/{len(TURNS)}] {who} ({voice}) → {p.name}")
        await synth_one(text, voice, p)
        parts.append(p)

    # concat: try ffmpeg first, fall back to raw byte concat
    concat_ok = False
    if not concat_ok:
        # try ffmpeg
        try:
            list_file = tmpdir / "list.txt"
            list_file.write_text("\n".join(f"file '{p.as_posix()}'" for p in parts), encoding="utf-8")
            subprocess.run(
                ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
                 "-c", "copy", str(OUT)],
                check=True, capture_output=True
            )
            concat_ok = True
            print("concat via ffmpeg ✓")
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"ffmpeg unavailable/failed: {e}. Falling back to raw byte concat.")

    if not concat_ok:
        # raw MP3 concat — works when files come from same encoder
        with open(OUT, "wb") as fout:
            for p in parts:
                fout.write(p.read_bytes())
        print("concat via raw bytes ✓")

    size = OUT.stat().st_size
    print(f"\nSAVED: {OUT}\nsize:  {size:,} bytes ({size/1024:.1f} KB)")

    # cleanup
    for p in parts: p.unlink(missing_ok=True)
    (tmpdir / "list.txt").unlink(missing_ok=True)
    tmpdir.rmdir()

if __name__ == "__main__":
    asyncio.run(main())
