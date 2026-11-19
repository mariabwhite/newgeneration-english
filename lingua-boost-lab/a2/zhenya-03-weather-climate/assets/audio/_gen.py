"""Generate MP3s for zhenya-03-weather-climate via edge-tts.
Run: py -3 _gen.py
"""
import asyncio, sys, subprocess
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent

MONO = [
    # Katie letter (reading audio-first)
    ("katie-scotland.mp3", "en-GB-SoniaNeural",
     "Dear Zhenya, I think it is always very hot in summer in Moscow. But in Scotland the summer is not hot. "
     "Today, for example, it is only sixteen degrees and quite windy. "
     "I'm wearing a sweater and a jacket, and I still feel a bit cold. "
     "Last August I went to London and the weather there was much warmer — about twenty-six degrees every day, bright sunshine, no rain. "
     "I was really happy. I walked a lot and I visited six museums. "
     "Have you ever been to London in summer? I hope one day you will come. "
     "The autumn in Scotland is beautiful too, but it rains a lot. "
     "Yesterday morning it was cold and foggy, and in the afternoon the sun came out for about an hour. "
     "Then the wind started blowing and it began to rain again. That is a typical Scottish day. "
     "What is the weather like in Moscow now? Write back soon. Love, Katie."),
    # BBC weather forecast (listening gap-fill)
    ("bbc-weather-forecast.mp3", "en-GB-RyanNeural",
     "Good morning, this is the BBC weather forecast for Thursday. "
     "In London, the day will start cloudy with light rain in the morning. "
     "By midday the rain will stop and the sun will come out for a few hours. "
     "The temperature will reach seventeen degrees in the afternoon. "
     "In the north of Scotland, expect strong wind and heavy showers all day, with temperatures around eight degrees. "
     "In Wales, the morning will be foggy, but the afternoon will be bright and dry. "
     "Tonight, the temperature in most of the country will drop to about six degrees, and a thick frost is possible in the countryside. "
     "Tomorrow, Friday, the weather will be much better everywhere — mostly sunny, dry, and warmer, with temperatures up to twenty degrees in the south. "
     "That is all from the weather centre."),
    # Dialogue weather today (en-GB female pair)
    ("moscow-weather-chat.mp3", None,  # dialogue — handled below
     ""),
]

DIALOGUES = [
    ("moscow-weather-chat.mp3", [
        ("en-GB-SoniaNeural", "Hi Zhenya! How is the weather in Moscow today?"),
        ("en-GB-MaisieNeural", "Hi Katie! It's really cold today. The temperature is minus five, and it's snowing hard."),
        ("en-GB-SoniaNeural", "Minus five? Wow. Is it windy as well?"),
        ("en-GB-MaisieNeural", "A little. The wind is blowing from the north, but not very strong. What about Scotland?"),
        ("en-GB-SoniaNeural", "Here it's plus seven and raining. It has rained every day this week!"),
        ("en-GB-MaisieNeural", "Oh no. Have you been outside today?"),
        ("en-GB-SoniaNeural", "Yes, I have. I walked my dog this morning. I got completely wet."),
        ("en-GB-MaisieNeural", "In Moscow I love winter because the snow is so bright. The streets look like a fairy tale."),
        ("en-GB-SoniaNeural", "That sounds beautiful. Send me a photo!"),
        ("en-GB-MaisieNeural", "OK, I will. Have a warm evening, Katie!"),
    ]),
]

async def gen_mono(fname, voice, text):
    if not voice: return
    out = HERE / fname
    comm = edge_tts.Communicate(text, voice=voice, rate="-10%")
    await comm.save(str(out))
    print(f"  wrote {fname}")

async def gen_dialogue(fname, turns):
    tmp_files = []
    silence = HERE / "__silence.mp3"
    if not silence.exists():
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
            "-t", "0.4", "-q:a", "9", "-acodec", "libmp3lame", str(silence)
        ], check=True, capture_output=True)
    for i, (voice, text) in enumerate(turns):
        tmp = HERE / f"__tmp_{i:02d}.mp3"
        comm = edge_tts.Communicate(text, voice=voice, rate="-10%")
        await comm.save(str(tmp))
        tmp_files.append(tmp)
    listf = HERE / "__concat.txt"
    with listf.open("w", encoding="utf-8") as f:
        for i, tmp in enumerate(tmp_files):
            f.write(f"file '{tmp.name}'\n")
            if i < len(tmp_files) - 1:
                f.write(f"file '{silence.name}'\n")
    out = HERE / fname
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
        "-c", "copy", str(out)
    ], check=True, capture_output=True, cwd=str(HERE))
    listf.unlink()
    for tmp in tmp_files:
        tmp.unlink()
    print(f"  wrote {fname} ({len(turns)} turns)")

async def main():
    print("zhenya-03-weather-climate · edge-tts")
    import os
    only = set(os.environ.get("ONLY","").split(",")) if os.environ.get("ONLY") else None
    for fname, voice, text in MONO:
        if only and fname not in only: continue
        await gen_mono(fname, voice, text)
    for fname, turns in DIALOGUES:
        if only and fname not in only: continue
        await gen_dialogue(fname, turns)
    sil = HERE / "__silence.mp3"
    if sil.exists(): sil.unlink()
    print("done.")

if __name__ == "__main__":
    asyncio.run(main())
