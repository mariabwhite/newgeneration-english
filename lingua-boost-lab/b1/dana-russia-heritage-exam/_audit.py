"""Audit: audio presence, keys, shuffle for dana-russia-heritage-exam."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
html = open('index.html', encoding='utf-8').read()
print(f'=== FILE: {len(html):,} chars, {html.count(chr(10)):,} lines')

# ---- AUDIO AUDIT ----
direct = set(re.findall(r'["\'][.]{0,2}/?assets/audio/([a-zA-Z0-9_\-./]+\.mp3)["\']', html))
direct |= set(re.findall(r'["\']audio/([a-zA-Z0-9_\-./]+\.mp3)["\']', html))
says = set(re.findall(r'data-say="([^"]+)"', html))
has_mf = 'AUDIO_MANIFEST' in html

audio_dir = 'assets/audio' if os.path.isdir('assets/audio') else 'audio'
present = set()
if os.path.isdir(audio_dir):
    for root, _, files in os.walk(audio_dir):
        for f in files:
            if f.endswith('.mp3'):
                rel = os.path.relpath(os.path.join(root, f), audio_dir)
                rel = rel.replace(os.sep, '/')
                present.add(rel)

print(f'\n=== AUDIO ===  dir: {audio_dir}')
print(f'  direct audio refs: {len(direct)}  sample: {list(direct)[:3]}')
print(f'  data-say phrases: {len(says)}')
print(f'  AUDIO_MANIFEST in code: {has_mf}')
print(f'  mp3 on disk: {len(present)}  sample: {list(present)[:3]}')

missing = sorted(direct - present)
print(f'  MISSING (direct refs not on disk): {len(missing)}')
for m in missing[:10]:
    print(f'    - {m}')
small = []
for f in sorted(present):
    sz = os.path.getsize(os.path.join(audio_dir, f))
    if sz < 500:
        small.append((f, sz))
print(f'  SMALL mp3 (<500b, likely bad/empty): {len(small)}')
for s in small[:10]:
    print(f'    - {s[0]}  {s[1]}b')

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') + '.mp3'
if says:
    expected = {slug(s) for s in says}
    miss_slug = sorted(expected - present)
    print(f'  if slug-based: {len(miss_slug)} slug-mp3 missing of {len(expected)}')
    for m in miss_slug[:10]:
        print(f'    - {m}')

# ---- EXERCISE KEYS ----
print(f'\n=== EXERCISE KEYS ===')
checks = [
    ('.mcq items (data-correct)', 'mcq', 'data-correct'),
    ('.tfns-item (data-correct)', 'tfns-item', 'data-correct'),
    ('.tf-item2 (data-a)', 'tf-item2', 'data-a'),
    ('.mp-item (data-a + data-b)', 'mp-item', None),
    ('.tp-row (data-answer)', 'tp-row', 'data-answer'),
    ('.mc-item (data-a)', 'mc-item', 'data-a'),
    ('.sort-token (data-col)', 'sort-token', 'data-col'),
    ('.sl-row (data-silent)', 'sl-row', 'data-silent'),
    ('.fi-row + .fi-inp (data-answer)', 'fi-inp', 'data-answer'),
    ('.cloze-inp (data-answer)', 'cloze-inp', 'data-answer'),
    ('.lst-q (data-answer)', 'lst-q', 'data-answer'),
    ('.ws-pair (data-answer)', 'ws-pair', 'data-answer'),
]
for label, cls, attr in checks:
    pat = rf'(?:<[a-z]+[^>]*class="[^"]*\b{re.escape(cls)}\b[^"]*"[^>]*>)'
    all_matches = re.findall(pat, html)
    if attr:
        with_key = sum(1 for m in all_matches if f'{attr}=' in m)
    else:
        with_key = sum(1 for m in all_matches if 'data-a=' in m and 'data-b=' in m)
    total = len(all_matches)
    if total == 0:
        continue
    status = 'OK' if with_key == total else 'MISS'
    print(f'  [{status}] {label}: {with_key}/{total}')
    # list missing
    if with_key < total:
        for m in all_matches:
            if attr and f'{attr}=' not in m:
                print(f'    - no {attr} in: {m[:120]}')
            elif not attr and not ('data-a=' in m and 'data-b=' in m):
                print(f'    - no data-a/b in: {m[:120]}')

# ---- SHUFFLE ----
print(f'\n=== SHUFFLE ===')
has_shuffle = bool(re.search(r'(Math\.random|Fisher.?Yates)', html))
print(f'  Math.random / Fisher-Yates in code: {has_shuffle}')
calls = len(re.findall(r'Math\.random\s*\(', html))
print(f'  Math.random() calls: {calls}')
if 'shuffle' in html.lower():
    sh_funcs = re.findall(r'function\s+(\w*[Ss]huffle\w*)', html)
    print(f'  shuffle functions: {sh_funcs}')
# does MCQ init shuffle options?
init_shuffle = bool(re.search(r'mcq[\s\S]{0,500}Math\.random', html))
print(f'  MCQ init looks like it shuffles options: {init_shuffle}')
