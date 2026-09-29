#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chocolat · Three Winds · Cinema Speaking Lab
3 listening tracks · 4 unique voices · en-GB
File 1: dialogue (Marie=Sonia, Jeanne=Libby) - concat via ffmpeg
File 2: monologue Vianne (Maisie)
File 3: monologue Père Henri (Ryan)
"""
import sys, asyncio, os, subprocess
sys.stdout.reconfigure(encoding="utf-8")

import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))

# ─── File 1 · Two-voice dialogue ──────────────────────────
DIALOGUE_1 = [
    ("Marie",  "en-GB-SoniaNeural", "-12%", "Did you see her? Walking straight past the church, that woman in the red cloak."),
    ("Jeanne", "en-GB-LibbyNeural", "-12%", "During Lent, no less. And with a small child. What kind of mother —"),
    ("Marie",  "en-GB-SoniaNeural", "-12%", "Armande gave her the key. Just like that. To the old shop across the square."),
    ("Jeanne", "en-GB-LibbyNeural", "-12%", "The Comte was furious, I could see his face. She wants to sell chocolate. Chocolate. During the Great Fast."),
    ("Marie",  "en-GB-SoniaNeural", "-12%", "Well. The north wind brought her. Maybe the north wind will take her away again."),
]

# ─── File 2 · Vianne monologue ─────────────────────────────
VIANNE_TEXT = (
    "Come in, madame. It's cold outside, and you've been standing at that window for a long time. "
    "No, no — you don't have to buy anything. Just one small taste. On the house. "
    "Now — let me look at you. Hmm. You are a woman who likes strong tea. "
    "Who reads the same book every winter. Who sits closer to the fire than to the window. "
    "Try this one. Bitter chocolate — with a little chilli. Trust me. "
    "Everyone has a favourite, madame. They just don't always know it yet."
)

# ─── File 3 · Père Henri homily ────────────────────────────
HENRI_TEXT = (
    "I'm not sure what the theme of my homily today ought to be. "
    "Do I want to speak of the miracle of Our Lord's divine transformation? "
    "Not really, no. I don't want to talk about His divinity. I'd rather talk about His humanity. "
    "I mean, you know, how He lived His life, here on Earth. His kindness, His tolerance. "
    "Listen, here's what I think. I think that we can't go around measuring our goodness "
    "by what we don't do — by what we deny ourselves, what we resist, and who we exclude. "
    "I think we've got to measure goodness by what we embrace, what we create, and who we include."
)


async def synth(text, voice, rate, out_path):
    comm = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await comm.save(out_path)


def make_silence(out_path, seconds=0.45):
    """Pre-baked silence for concat between dialogue turns."""
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"anullsrc=r=24000:cl=mono",
        "-t", str(seconds), "-c:a", "libmp3lame", "-b:a", "48k",
        out_path
    ], check=True, capture_output=True)


def concat(inputs, out_path):
    """FFmpeg concat with file list."""
    list_path = out_path + ".list.txt"
    with open(list_path, "w", encoding="utf-8") as f:
        for p in inputs:
            f.write(f"file '{p.replace(chr(92), '/')}'" + "\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_path, "-c", "copy", out_path
    ], check=True, capture_output=True)
    os.remove(list_path)


async def main():
    # ─── FILE 1: dialogue Marie + Jeanne ─────────────
    print("[+] listen-1-gossip · SoniaNeural + LibbyNeural (dialogue concat)", flush=True)
    turns_dir = os.path.join(HERE, "_tmp_turns")
    os.makedirs(turns_dir, exist_ok=True)
    silence = os.path.join(turns_dir, "silence.mp3")
    make_silence(silence, 0.45)
    turn_paths = []
    for i, (speaker, voice, rate, text) in enumerate(DIALOGUE_1):
        turn_path = os.path.join(turns_dir, f"turn_{i:02d}_{speaker}.mp3")
        await synth(text, voice, rate, turn_path)
        turn_paths.append(turn_path)
        if i < len(DIALOGUE_1) - 1:
            turn_paths.append(silence)
    out1 = os.path.join(HERE, "listen-1-gossip.mp3")
    concat(turn_paths, out1)
    print(f"    -> {out1}  ({os.path.getsize(out1):,} bytes)", flush=True)

    # ─── FILE 2: Vianne monologue (Maisie) ───────────
    print("[+] listen-2-shop · MaisieNeural (warm monologue)", flush=True)
    out2 = os.path.join(HERE, "listen-2-shop.mp3")
    await synth(VIANNE_TEXT, "en-GB-MaisieNeural", "-8%", out2)
    print(f"    -> {out2}  ({os.path.getsize(out2):,} bytes)", flush=True)

    # ─── FILE 3: Père Henri homily (Ryan) ────────────
    print("[+] listen-3-homily · RyanNeural (male soft)", flush=True)
    out3 = os.path.join(HERE, "listen-3-homily.mp3")
    await synth(HENRI_TEXT, "en-GB-RyanNeural", "-10%", out3)
    print(f"    -> {out3}  ({os.path.getsize(out3):,} bytes)", flush=True)

    # cleanup
    for p in os.listdir(turns_dir):
        os.remove(os.path.join(turns_dir, p))
    os.rmdir(turns_dir)
    print("[done] 3 tracks · 4 unique voices (Sonia + Libby + Maisie + Ryan)")


if __name__ == "__main__":
    asyncio.run(main())
