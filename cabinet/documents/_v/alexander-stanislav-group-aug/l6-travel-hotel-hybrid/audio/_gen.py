"""
L6 · Hotel Arrival & Travel Talk · edge-tts mp3 generator
Voice: en-GB-SoniaNeural (British female).
Scans index.html for all `data-say="..."` attributes AND all `w:` / `right:` / `examples:`
strings inside JS data blocks. Generates one mp3 per unique text and writes _manifest.js.

Usage:
    cd cabinet/documents/_v/alexander-stanislav-group-aug/l6-travel-hotel-hybrid/audio
    python _gen.py

Requires:
    pip install edge-tts
"""
import asyncio, hashlib, json, os, re, sys
from pathlib import Path
import edge_tts

# Windows cp1251 stdout blows up on em-dash etc — force utf-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).parent
ROOT = HERE.parent
HTML = ROOT / "index.html"
VOICE = "en-GB-SoniaNeural"
RATE = "-4%"   # slight slow-down for A2 clarity

def slug(text: str) -> str:
    """Short filesystem-safe file name (short cap avoids Windows MAX_PATH)."""
    base = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    base = re.sub(r"[\s_-]+", "-", base)
    if len(base) > 40:
        # keep first 32 chars + short hash suffix for uniqueness
        h = hashlib.md5(text.encode("utf-8")).hexdigest()[:8]
        base = base[:32].rstrip("-") + "-" + h
    return base + ".mp3"

def extract_texts(html: str) -> list[str]:
    texts: list[str] = []
    # 1) HTML data-say="..."
    for m in re.finditer(r'data-say="([^"]+)"', html):
        texts.append(m.group(1))
    # 2) JS array items {w:'...',...}   → both '' and "" strings
    for m in re.finditer(r"\bw:\s*(['\"])(.+?)\1(?=\s*,)", html):
        texts.append(m.group(2))
    # 3) JS M7 items — {right:'...'}
    for m in re.finditer(r"\bright:\s*(['\"])(.+?)\1(?=\s*,)", html):
        texts.append(m.group(2))
    # 4) JS PATTERNS examples arrays — everything inside examples:[ ... ]
    for arr in re.finditer(r"examples:\s*\[(.*?)\]", html, re.S):
        for s in re.finditer(r'"([^"]+)"', arr.group(1)):
            texts.append(s.group(1))
    # decode HTML entities
    out = []
    for t in texts:
        t = t.replace("&quot;", '"').replace("&amp;", "&").replace("&#39;", "'").replace("&apos;", "'").strip()
        if t and t not in out:
            out.append(t)
    return out

async def gen_one(text: str, fname: str) -> None:
    out = HERE / fname
    if out.exists() and out.stat().st_size > 500:
        print(f"  skip  {fname}  (already exists)")
        return
    comm = edge_tts.Communicate(text, VOICE, rate=RATE)
    await comm.save(str(out))
    print(f"  ok    {fname}   <- {text[:60]}")

async def main():
    html = HTML.read_text(encoding="utf-8")
    texts = extract_texts(html)
    manifest: dict[str, str] = {}
    print(f"Found {len(texts)} unique lines to voice.\n")
    for i, t in enumerate(texts, 1):
        fname = slug(t)
        manifest[t] = fname
        print(f"[{i:3}/{len(texts)}] ", end="")
        try:
            await gen_one(t, fname)
        except Exception as e:
            print(f"  FAIL  {fname}: {e}")
    # Write manifest.js
    mjs = "window.AUDIO_MANIFEST = " + json.dumps(manifest, ensure_ascii=False, indent=2) + ";\n"
    (HERE / "_manifest.js").write_text(mjs, encoding="utf-8")
    print(f"\nWrote _manifest.js with {len(manifest)} entries.")

if __name__ == "__main__":
    asyncio.run(main())
