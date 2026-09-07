"""Generate MP3 for Anya L2 · The Silver Book listening clip."""
import sys, asyncio, pathlib
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

VOICE = "en-GB-SoniaNeural"

CLIPS = {
    "silver-book": (
        "Welcome to the Land of Irregular Verbs. "
        "Here every action has three faces. "
        "You must learn them. You must remember them. And you must never mix them. "
        "Behind each house there are three doors. "
        "Red is the base form. Blue is the past. Gold is the past participle. "
        "If you want to talk about yesterday, always choose the blue door. "
        "Yesterday changes everything. Nothing ends with -ed here. "
        "Go — went — gone. See — saw — seen. Write — wrote — written. "
        "Stand — stood — stood. Give — gave — given. "
        "Remember them, and the land will open to you.",
    ),
}

OUT = pathlib.Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

async def one(name: str, text: str) -> None:
    dest = OUT / f"{name}.mp3"
    if dest.exists() and dest.stat().st_size > 1000:
        print(f"skip  {name}.mp3 ({dest.stat().st_size} B)")
        return
    tts = edge_tts.Communicate(text=text, voice=VOICE, rate="-4%")
    await tts.save(str(dest))
    print(f"ok    {name}.mp3 ({dest.stat().st_size} B)")

async def main() -> None:
    for name, (text,) in CLIPS.items():
        await one(name, text)

if __name__ == "__main__":
    asyncio.run(main())
