"""
Bake all edge-tts mp3 files for the pronunciation-launchpad lesson.
Voices: en-GB-SoniaNeural (default female), en-GB-RyanNeural (male, for waiter).
Rate: -8% (per protocol_lab_lesson_audio.md).
Windows: sys.stdout reconfigure utf-8 (per reference_lab_gen_py_windows_fix.md).
"""
import sys, os, re, json, hashlib, asyncio, html
from pathlib import Path

# --- Windows utf-8 hardening
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    import edge_tts
except ImportError:
    print("edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

HERE = Path(__file__).parent
LESSON_HTML = HERE.parent / "index.html"
OUT_DIR = HERE
OUT_DIR.mkdir(exist_ok=True)

VOICE_FEMALE = "en-GB-SoniaNeural"
VOICE_MALE   = "en-GB-RyanNeural"
RATE         = "-8%"

# --- Enumerate phrases from the HTML
def enum_phrases(html_text):
    """Return list of unique (text, voice_key) pairs.
    voice_key: 'f' (Sonia) or 'm' (Ryan). Slow versions get same mp3, JS handles rate."""
    phrases = {}   # text -> voice_key
    # 1) All data-say="..." attributes
    for m in re.finditer(r'data-say="([^"]+)"', html_text):
        text = html.unescape(m.group(1))
        text = text.strip()
        if text and text not in phrases:
            phrases[text] = "f"
    # 2) All data-c="..." (listening options that we speak on click)
    for m in re.finditer(r'data-c="([^"]+)"', html_text):
        text = html.unescape(m.group(1))
        text = text.strip()
        if text and text not in phrases:
            phrases[text] = "f"
    # 3) Dialogue lines are stored in HTML too but the JS array has canonical text.
    # We'll bake those here explicitly (waiter = male).
    dialogue = [
        ("Good afternoon! What can I get you?", "m"),
        ("Hi! Can I have a hot chocolate and a piece of chocolate cake, please?", "f"),
        ("Of course! Would you like whipped cream on top?", "m"),
        ("Yes, please. And do you have any strawberries?", "f"),
        ("We have fresh strawberries with the cake. Anything else?", "m"),
        ("No, that's all. How much is it?", "f"),
        ("That will be seven pounds fifty, please.", "m"),
    ]
    for text, v in dialogue:
        phrases[text] = v  # override to male where relevant
    return phrases

# --- Filename hash
def slug_for(text, voice_key):
    h = hashlib.md5((voice_key + "|" + text).encode("utf-8")).hexdigest()[:12]
    return f"{voice_key}_{h}.mp3"

async def bake_one(text, voice, out_path):
    c = edge_tts.Communicate(text, voice, rate=RATE)
    await c.save(str(out_path))

async def main():
    html_text = LESSON_HTML.read_text(encoding="utf-8")
    phrases = enum_phrases(html_text)
    manifest = {}
    total = len(phrases)
    print(f"[gen] Total unique phrases: {total}")

    made, skipped, failed = 0, 0, 0
    for i, (text, vkey) in enumerate(phrases.items(), 1):
        voice = VOICE_MALE if vkey == "m" else VOICE_FEMALE
        fname = slug_for(text, vkey)
        fpath = OUT_DIR / fname
        manifest[text] = fname
        if fpath.exists() and fpath.stat().st_size > 0:
            skipped += 1
            continue
        try:
            await bake_one(text, voice, fpath)
            made += 1
            if i % 20 == 0 or i == total:
                print(f"[gen] {i}/{total} done ({made} new, {skipped} skip)")
        except Exception as e:
            failed += 1
            print(f"[gen] FAIL '{text[:40]}...': {e}")

    # Write manifest
    manifest_path = OUT_DIR / "_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"[gen] Manifest: {manifest_path.name} ({len(manifest)} entries)")
    print(f"[gen] Summary: {made} new, {skipped} skipped, {failed} failed")

if __name__ == "__main__":
    asyncio.run(main())
