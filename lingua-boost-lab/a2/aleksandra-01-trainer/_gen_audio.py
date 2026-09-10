"""Generate edge-tts MP3 for the Aleksandra L2 mini-trainer.
Voice: en-GB SoniaNeural (British female, matches Katya-vocab pattern).
Windows-safe stdout.
Run: python _gen_audio.py
"""
import sys, asyncio, pathlib, re
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

VOICE = "en-GB-SoniaNeural"
RATE = "-6%"

def slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s[:60] or "clip"

VOCAB = [
    ("tired",          "I am tired today."),
    ("horrible",       "The weather is horrible."),
    ("hungry",         "I am hungry, let's eat."),
    ("angry",          "Don't be angry with me."),
    ("afraid",         "I am afraid of the dark."),
    ("stressed",       "She is stressed about the exam."),
    ("free medicine",  "The clinic gives free medicine to pensioners."),
    ("team",           "Our team works well together."),
    ("research",       "She does research on climate."),
    ("business trip",  "I had a business trip last week."),
    ("tour",           "We took a tour of the museum."),
    ("be going to",    "I am going to call my mother."),
    ("be allergic to", "I am allergic to the sun."),
    ("because of",     "Because of this situation, I am stressed."),
]

PHRASES = [
    "I am tired today.",
    "The weather is horrible.",
    "I am hungry, let's eat.",
    "Don't be angry with me.",
    "I am afraid of the dark.",
    "She is stressed about the exam.",
    "You look tired.",
    "Our team works well together.",
    "She does research on climate.",
    "I had a business trip last week.",
    "We took a tour of the museum.",
    "The doctor gave me free medicine.",
    "I am going to call my mother.",
    "She is going to travel next week.",
    "I am allergic to the sun.",
    "He is allergic to nuts.",
    "Because of this situation, I am afraid.",
    "I am tired because of the trip.",
]

# Deduplicate all texts to voice.
TEXTS = set()
for w, ex in VOCAB:
    TEXTS.add(w)
    TEXTS.add(ex)
for p in PHRASES:
    TEXTS.add(p)

async def gen_one(text: str, out_dir: pathlib.Path):
    fname = slug(text) + ".mp3"
    dest = out_dir / fname
    if dest.exists() and dest.stat().st_size > 500:
        return fname, "skip"
    tts = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
    await tts.save(str(dest))
    return fname, "ok"

async def main():
    out_dir = pathlib.Path(__file__).parent / "assets" / "audio"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"-> {out_dir}")
    print(f"-> {len(TEXTS)} unique clips")
    manifest = {}
    for i, text in enumerate(sorted(TEXTS), 1):
        try:
            fname, status = await gen_one(text, out_dir)
            manifest[text] = fname
            print(f"  [{i:>3}/{len(TEXTS)}] {status:4}  {fname}")
        except Exception as e:
            print(f"  ERR  {text!r}: {e}")
    # Emit JS manifest snippet
    print("\n--- window.AUDIO_MANIFEST = ---")
    import json
    print(json.dumps(manifest, ensure_ascii=False))
    print("--- end ---\n")
    print("done.")

if __name__ == "__main__":
    asyncio.run(main())
