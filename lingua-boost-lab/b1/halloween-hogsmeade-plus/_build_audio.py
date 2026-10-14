"""Halloween-hogsmeade-plus audio build.

Шаг 1: edge-tts batch (5 клипов: Джек-ру, chant-en, chant-child-en, witch, deep-laugh).
Шаг 2: ffmpeg эффекты (reverb/echo/volume) + генерация ambient-loop.
Шаг 3: финальный mix: ambient-loop + overlay chants как single Halloween track.
"""
import asyncio
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "assets", "audio")
os.makedirs(AUDIO, exist_ok=True)

# -------- 1. edge-tts clips --------
# (filename, text, voice, rate, pitch, volume)
CLIPS = [
    (
        "jack-intro-ru.mp3",
        "Привет, детишки! Я... Джек. Хи-хи-хи, ха-ха-ха-ха. "
        "Сегодня я проведу этот урок. "
        "Готовьтесь — Hogsmeade ждёт! Поехали, детишки.",
        "ru-RU-DmitryNeural", "-18%", "-8Hz",
    ),
    (
        "chant-boys-girls.mp3",
        "Boys and girls, boys and girls of every age! "
        "Welcome, welcome to our Halloween stage! "
        "Pumpkins glowing, witches riding — "
        "This is Hogsmeade, Hallo-weeeeen!",
        "en-GB-RyanNeural", "-8%", "-6Hz",
    ),
    (
        "chant-trick-treat.mp3",
        "Trick or treat! Trick or treat! "
        "Give us something nice to eat! "
        "Pumpkins, candies, chocolate frogs — "
        "Honeydukes has got them all!",
        "en-US-AnaNeural", "+3%", "+8Hz",
    ),
    (
        "witch-cackle.mp3",
        "Hee hee hee! Haa haa haa haa haaa! Oh, come inside, come inside, dear...",
        "en-GB-SoniaNeural", "-4%", "+6Hz",
    ),
    (
        "deep-laugh.mp3",
        "Ho ho ho ho! Ha ha ha ha haaaaa!",
        "en-US-GuyNeural", "-22%", "-18Hz",
    ),
]


async def tts_batch():
    import edge_tts
    for fn, text, voice, rate, pitch in CLIPS:
        path = os.path.join(AUDIO, fn)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            print(f"[skip] {fn} ({os.path.getsize(path)}b)")
            continue
        print(f"[tts]  {fn}  ({voice}, rate={rate}, pitch={pitch})")
        try:
            tts = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            await tts.save(path)
            if os.path.getsize(path) == 0:
                raise RuntimeError("empty file")
            print(f"       {os.path.getsize(path)} bytes OK")
        except Exception as e:
            print(f"       ERROR: {e}")
            # retry once after short sleep
            import time
            if os.path.exists(path):
                os.remove(path)
            time.sleep(5)
            print(f"[tts]  retry {fn}")
            tts = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            await tts.save(path)
            print(f"       {os.path.getsize(path)} bytes OK (retry)")


def run(cmd, cwd=None):
    print(f"$ {cmd}")
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print("STDOUT:", r.stdout)
        print("STDERR:", r.stderr)
        raise RuntimeError(f"ffmpeg failed ({r.returncode})")


def ffmpeg_fx():
    """Apply spooky reverb/echo to each clip (overwrite _fx version)."""
    recipes = {
        # Jack: big cathedral reverb, slight volume boost
        "jack-intro-ru.mp3":   "aecho=0.8:0.9:60|180:0.45|0.3,volume=1.4",
        "chant-boys-girls.mp3": "aecho=0.85:0.85:80|160|240:0.4|0.3|0.2,volume=1.3",
        "chant-trick-treat.mp3": "aecho=0.8:0.7:40|100:0.35|0.22,volume=1.25",
        "witch-cackle.mp3":    "aecho=0.9:0.85:50|140|280:0.5|0.35|0.25,volume=1.35",
        "deep-laugh.mp3":      "aecho=0.9:0.9:100|220|360:0.5|0.4|0.3,volume=1.5",
    }
    for fn, flt in recipes.items():
        inp = os.path.join(AUDIO, fn)
        out = os.path.join(AUDIO, fn.replace(".mp3", "-fx.mp3"))
        if not os.path.exists(inp):
            print(f"[fx]   SKIP {fn} (source missing)")
            continue
        if os.path.exists(out) and os.path.getsize(out) > 0:
            print(f"[fx]   skip {out} already exists")
            continue
        cmd = f'ffmpeg -y -i "{inp}" -af "{flt}" -c:a libmp3lame -b:a 128k "{out}"'
        run(cmd)


def ffmpeg_ambient():
    """Generate 45-sec Halloween ambient: pink noise wind + sub-bass drone + reverb."""
    out = os.path.join(AUDIO, "ambient-halloween.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"[amb]  skip (exists)")
        return
    # 45 seconds total; pink noise + two sine basses + bell-like high sine, mix, reverb
    cmd = (
        'ffmpeg -y '
        '-f lavfi -i "anoisesrc=color=pink:duration=45:amplitude=0.07" '
        '-f lavfi -i "sine=frequency=55:duration=45" '
        '-f lavfi -i "sine=frequency=82.5:duration=45" '
        '-f lavfi -i "sine=frequency=440:duration=45" '
        '-filter_complex '
        '"[1:a]volume=0.14[sub1];'
        '[2:a]volume=0.08[sub2];'
        '[3:a]volume=0.015,tremolo=f=0.3:d=0.6[bell];'
        '[0:a][sub1][sub2][bell]amix=inputs=4:normalize=0,'
        'aecho=0.6:0.9:220|450|700:0.35|0.22|0.12,'
        'lowpass=f=900,'
        'volume=0.9" '
        '-c:a libmp3lame -b:a 128k '
        f'"{out}"'
    )
    run(cmd)


def ffmpeg_final_mix():
    """Compose a 25-sec 'opening overture': ambient + chant layers + sinister laugh end."""
    out = os.path.join(AUDIO, "halloween-opener.mp3")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"[mix]  skip (exists)")
        return
    amb = os.path.join(AUDIO, "ambient-halloween.mp3")
    c1 = os.path.join(AUDIO, "chant-boys-girls-fx.mp3")
    c2 = os.path.join(AUDIO, "chant-trick-treat-fx.mp3")
    witch = os.path.join(AUDIO, "witch-cackle-fx.mp3")
    deep = os.path.join(AUDIO, "deep-laugh-fx.mp3")
    # Timings (seconds): c1 at 1.5s, c2 at 10s overlapped, witch at 18s, deep at 22s
    cmd = (
        f'ffmpeg -y '
        f'-i "{amb}" -i "{c1}" -i "{c2}" -i "{witch}" -i "{deep}" '
        f'-filter_complex '
        f'"[1:a]adelay=1500|1500,volume=1.0[a1];'
        f'[2:a]adelay=10000|10000,volume=0.9[a2];'
        f'[3:a]adelay=18000|18000,volume=1.1[a3];'
        f'[4:a]adelay=22500|22500,volume=1.2[a4];'
        f'[0:a]volume=0.75[amb];'
        f'[amb][a1][a2][a3][a4]amix=inputs=5:normalize=0:duration=longest,'
        f'volume=1.1" '
        f'-t 28 '
        f'-c:a libmp3lame -b:a 160k '
        f'"{out}"'
    )
    run(cmd)


if __name__ == "__main__":
    print("=== STEP 1 · edge-tts batch ===")
    asyncio.run(tts_batch())
    print("\n=== STEP 2 · ffmpeg fx per clip ===")
    ffmpeg_fx()
    print("\n=== STEP 3 · ffmpeg ambient loop ===")
    ffmpeg_ambient()
    print("\n=== STEP 4 · ffmpeg final mix (halloween-opener) ===")
    ffmpeg_final_mix()
    print("\n=== DONE ===")
    print("Final files in:", AUDIO)
    for f in sorted(os.listdir(AUDIO)):
        p = os.path.join(AUDIO, f)
        print(f"  {f}  ({os.path.getsize(p):,} bytes)")
