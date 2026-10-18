"""Generate mp3 files for taisiya-01-spelling-rules via edge-tts.
   Parses all data-say="..." from index.html, dedupes, outputs audio/<slug>.mp3,
   writes audio/_manifest.js (text -> filename). Retries on 403.
"""
import re
import asyncio
import hashlib
import json
import os
import sys
import time
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print('ERROR: pip install edge-tts', file=sys.stderr)
    sys.exit(1)

HERE = Path(__file__).parent
HTML = HERE / 'index.html'
AUDIO_DIR = HERE / 'audio'
MANIFEST = AUDIO_DIR / '_manifest.js'

VOICE = 'en-GB-SoniaNeural'
RATE = '-5%'

SAY_RE = re.compile(r'data-say="([^"]+)"')


def slugify(text: str) -> str:
    """Short filename-safe slug + stable hash suffix for uniqueness."""
    base = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')[:30]
    if not base:
        base = 'phr'
    h = hashlib.md5(text.encode('utf-8')).hexdigest()[:6]
    return f'{base}-{h}.mp3'


async def tts_one(text: str, out: Path, attempts: int = 3):
    for i in range(attempts):
        try:
            comm = edge_tts.Communicate(text, VOICE, rate=RATE)
            await comm.save(str(out))
            if out.exists() and out.stat().st_size > 500:
                return True
            if out.exists():
                out.unlink()
            await asyncio.sleep(5)
        except Exception as e:
            print(f'  retry {i+1}: {text!r} ({e})')
            if out.exists():
                try:
                    out.unlink()
                except Exception:
                    pass
            await asyncio.sleep(5)
    return False


async def main():
    html = HTML.read_text(encoding='utf-8')
    phrases = []
    seen = set()
    for m in SAY_RE.finditer(html):
        t = m.group(1).strip()
        if not t or t in seen:
            continue
        seen.add(t)
        phrases.append(t)

    print(f'Found {len(phrases)} unique phrases')
    AUDIO_DIR.mkdir(exist_ok=True)

    manifest = {}
    missing = []
    for i, text in enumerate(phrases, 1):
        fname = slugify(text)
        out = AUDIO_DIR / fname
        manifest[text] = fname
        if out.exists() and out.stat().st_size > 500:
            print(f'  [{i:3d}/{len(phrases)}] skip {fname}  ({text!r})')
            continue
        ok = await tts_one(text, out)
        if ok:
            print(f'  [{i:3d}/{len(phrases)}] OK   {fname}  ({text!r})')
        else:
            missing.append(text)
            print(f'  [{i:3d}/{len(phrases)}] MISS {fname}  ({text!r})')

    # Write manifest
    manifest_js = 'window.AUDIO_MANIFEST = ' + json.dumps(manifest, ensure_ascii=False, indent=1) + ';\n'
    MANIFEST.write_text(manifest_js, encoding='utf-8')
    print(f'\nManifest: {MANIFEST} ({len(manifest)} entries)')
    if missing:
        print(f'\n⚠️  MISSING ({len(missing)}):')
        for t in missing:
            print(f'    - {t!r}')
        sys.exit(1)

    print('\nAll audio ready')


if __name__ == '__main__':
    asyncio.run(main())
