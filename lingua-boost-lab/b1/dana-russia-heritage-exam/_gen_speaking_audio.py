"""Generate mp3 for the 8 speaking data-say phrases + write _manifest.js."""
import re, hashlib, json, os, sys, asyncio
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print('pip install edge-tts first', file=sys.stderr); sys.exit(1)

HERE = Path(__file__).parent
HTML = HERE / 'index.html'
AUDIO_DIR = HERE / 'assets' / 'audio' / 'speaking'
MANIFEST = HERE / 'assets' / 'audio' / '_manifest.js'
VOICE = 'en-GB-SoniaNeural'
RATE = '-5%'


def slug(text: str) -> str:
    base = re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')[:30]
    h = hashlib.md5(text.encode()).hexdigest()[:6]
    return f'{base}-{h}.mp3'


async def tts(text: str, out: Path, attempts: int = 3) -> bool:
    for i in range(attempts):
        try:
            await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(out))
            if out.exists() and out.stat().st_size > 500:
                return True
            if out.exists(): out.unlink()
            await asyncio.sleep(5)
        except Exception as e:
            print(f'  retry {i+1}: {e}')
            if out.exists():
                try: out.unlink()
                except: pass
            await asyncio.sleep(5)
    return False


async def main():
    html = HTML.read_text(encoding='utf-8')
    phrases = sorted(set(re.findall(r'data-say="([^"]+)"', html)))
    print(f'Found {len(phrases)} unique speaking phrases')
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {}
    missing = []
    for i, text in enumerate(phrases, 1):
        fname = slug(text)
        rel = f'speaking/{fname}'
        out = AUDIO_DIR / fname
        manifest[text] = rel
        if out.exists() and out.stat().st_size > 500:
            print(f'  [{i}/{len(phrases)}] skip {fname}')
            continue
        ok = await tts(text, out)
        print(f'  [{i}/{len(phrases)}] {"OK" if ok else "MISS"} {fname}')
        if not ok: missing.append(text)

    MANIFEST.write_text('window.AUDIO_MANIFEST = ' +
                        json.dumps(manifest, ensure_ascii=False, indent=1) + ';\n',
                        encoding='utf-8')
    print(f'\nManifest: {MANIFEST} ({len(manifest)} entries)')
    if missing: sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
