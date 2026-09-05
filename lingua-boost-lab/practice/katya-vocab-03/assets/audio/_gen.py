# -*- coding: utf-8 -*-
"""katya-vocab-03 · Personality Adjectives · 19 words + 19 examples.
Voice: en-GB-SoniaNeural (British female, ученический темп -6%).
Run:  python _gen.py
Also writes manifest.json  {text: slug.mp3}  next to the mp3s.
"""
import asyncio, json, re, sys
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).parent
VOICE = "en-GB-SoniaNeural"
RATE = "-6%"  # чуть медленнее для A2

WORDS = [
    # Positive
    ("generous",   "My grandma is very generous with sweets."),
    ("mature",     "He's very mature for a 13-year-old."),
    ("honest",     "Please be honest with me."),
    ("determined", "She's determined to become a doctor."),
    ("confident",  "He feels confident before every exam."),
    ("polite",     "Always be polite to teachers."),
    ("modest",     "She's modest about her medals."),
    # Negative
    ("rude",       "Don't be rude to your sister."),
    ("arrogant",   "He is arrogant and never listens."),
    ("mean",       "Why are you so mean to the cat?"),
    ("weak",       "I felt weak after the flu."),
    ("nasty",      "She said something nasty about my hair."),
    ("impatient",  "He's very impatient in the queue."),
    ("dishonest",  "I hate dishonest people."),
    # Temperament
    ("patient",    "My mum is very patient with little kids."),
    ("sensitive",  "She's very sensitive, don't shout at her."),
    ("quiet",      "He's a quiet boy, but very kind."),
    ("shy",        "I was shy on my first day at school."),
    ("talkative",  "My grandma is very talkative."),
]

def slug(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s\-']", "", s)
    s = re.sub(r"[\s']+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s[:40]  # Windows MAX_PATH guard

async def gen_one(text: str) -> str:
    fname = slug(text) + ".mp3"
    fpath = OUT / fname
    if fpath.exists():
        print(f"skip  {fname}")
        return fname
    tts = edge_tts.Communicate(text, VOICE, rate=RATE)
    await tts.save(str(fpath))
    print(f"done  {fname}")
    return fname

async def main():
    manifest = {}
    for w, ex in WORDS:
        try:
            manifest[w] = await gen_one(w)
        except Exception as e:
            print(f"FAIL word  {w}: {e}")
        try:
            manifest[ex] = await gen_one(ex)
        except Exception as e:
            print(f"FAIL phrase  {ex}: {e}")
    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nmanifest.json written ({len(manifest)} entries)")

if __name__ == "__main__":
    asyncio.run(main())
