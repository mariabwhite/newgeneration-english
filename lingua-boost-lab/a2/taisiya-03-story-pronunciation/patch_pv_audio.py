"""Add 🔊 say-buttons to every .pv-word in Ch 2-14 that doesn't have one."""
import re
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "index.html"
text = HTML.read_text(encoding="utf-8")

# Find the current chapter while walking
chapter = None
output = []
i = 0
BTN_STYLE = 'background:var(--accent);color:#fff;border:none;border-radius:50%;width:24px;height:24px;font-size:.7rem;cursor:pointer;margin-right:6px;vertical-align:middle'


def slugify(word_html: str) -> str:
    # Strip tags, pick first plain word, lowercase, alpha-numeric
    plain = re.sub(r'<[^>]+>', '', word_html).strip()
    # Take substring before parens or spaces
    first = re.split(r'[\s(]', plain, 1)[0]
    s = re.sub(r'[^a-zA-Z0-9]', '', first).lower()
    return s or 'word'


# Simple linear replace while tracking chapter
pattern_chapter = re.compile(r'<section class="section" id="c(\d+)">')
pattern_pv = re.compile(r'<div class="pv-word">(.*?)</div>', re.DOTALL)

# Walk through and build new text
pos = 0
chunks = []
current_ch = None
# Combined iterator over both patterns
events = []
for m in pattern_chapter.finditer(text):
    events.append((m.start(), 'ch', m))
for m in pattern_pv.finditer(text):
    events.append((m.start(), 'pv', m))
events.sort(key=lambda e: e[0])

last = 0
pv_count_per_ch = {}
for ev_pos, kind, m in events:
    chunks.append(text[last:m.start()])
    if kind == 'ch':
        current_ch = int(m.group(1))
        chunks.append(m.group(0))
    else:  # pv
        inner = m.group(1)
        if '<button' in inner:
            # Already has button — keep as-is
            chunks.append(m.group(0))
        else:
            pv_count_per_ch[current_ch] = pv_count_per_ch.get(current_ch, 0) + 1
            slug = slugify(inner)
            # Avoid dup slugs within chapter by appending index if needed
            path = f'audio/pv-c{current_ch}-{slug}.mp3'
            btn = f'<button class="say" data-a="{path}" style="{BTN_STYLE}">🔊</button>'
            new = f'<div class="pv-word">{btn}{inner.strip()}</div>'
            chunks.append(new)
    last = m.end()
chunks.append(text[last:])

new_text = ''.join(chunks)
if new_text != text:
    HTML.write_text(new_text, encoding="utf-8")
    added = sum(pv_count_per_ch.values())
    print(f"Added {added} 🔊 buttons across chapters: {sorted(pv_count_per_ch.items())}")
else:
    print("No changes needed.")
