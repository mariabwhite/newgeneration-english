"""Generate MP3 files for Anya's Recap Test lesson.
Windows-safe (utf-8, short slugs, no crashes on em-dash).
Run: python _gen_audio.py
"""
import sys, asyncio, pathlib
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

VOICE_F = "en-GB-SoniaNeural"   # Anya + narrator, calm BrE
VOICE_M = "en-GB-RyanNeural"    # reporter, teacher voice, adult BrE

# id -> (text, voice_key)
CLIPS = {
    # ─── Section 11 · Listening · Riverside Local News (single file) ───
    "listen-news": (
        "Good morning, this is Riverside Local News. "
        "The city has been experiencing an unusual heatwave since Monday, "
        "and temperatures have not dropped below thirty degrees for four days. "
        "Builders have been working on the new pedestrian bridge over the river for two weeks. "
        "The mayor, who has visited the site twice this month, "
        "said the project is running on time and on budget. "
        "Look up at the sky — it is going to rain later today. "
        "Please carry an umbrella, especially in the market area, "
        "where the streets are crowded on Saturdays. "
        "That is all for this morning. Have a lovely weekend.",
        "m",
    ),
}

VOICE_MAP = {"f": VOICE_F, "m": VOICE_M}

OUT = pathlib.Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

async def one(name: str, text: str, voice: str) -> None:
    dest = OUT / f"{name}.mp3"
    if dest.exists() and dest.stat().st_size > 1000:
        print(f"skip  {name}.mp3 ({dest.stat().st_size} B)")
        return
    tts = edge_tts.Communicate(text=text, voice=voice, rate="-2%")
    await tts.save(str(dest))
    print(f"ok    {name}.mp3 ({dest.stat().st_size} B)")

async def main() -> None:
    for name, (text, vkey) in CLIPS.items():
        await one(name, text, VOICE_MAP[vkey])

if __name__ == "__main__":
    asyncio.run(main())
