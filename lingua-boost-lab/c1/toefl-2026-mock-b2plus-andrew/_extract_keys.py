"""Extract correct MCQ answers + builder targets + CTW answers to KEYS.md."""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
html = (HERE / "index.html").read_text(encoding="utf-8")

# Split by section ids
sec_pat = re.compile(r'<section class="section" id="(s\d+)">', re.DOTALL)
positions = [(m.start(), m.group(1)) for m in sec_pat.finditer(html)]
positions.append((len(html), None))
sections = {}
for i in range(len(positions) - 1):
    start, sid = positions[i]
    if not sid:
        continue
    end = positions[i + 1][0]
    sections[sid] = html[start:end]

def strip(t):
    return re.sub(r"<[^>]+>", "", t).strip()

def extract_mcq(chunk):
    pat = re.compile(
        r'<div class="mcq-row" data-answer="([A-E])">\s*'
        r'<div class="mcq-q">(.*?)</div>\s*'
        r'<div class="mcq-opts">(.*?)</div>',
        re.DOTALL,
    )
    out = []
    for m in pat.finditer(chunk):
        letter = m.group(1)
        q = strip(m.group(2))
        btn_pat = re.compile(r'<button data-v="([A-E])">(.*?)</button>', re.DOTALL)
        ct = None
        for bm in btn_pat.finditer(m.group(3)):
            if bm.group(1) == letter:
                ct = strip(bm.group(2))
                break
        out.append((q, letter, ct))
    return out

def extract_ctw(chunk):
    pat = re.compile(
        r'<span class="ctw" data-ans="([^"]+)"><span class="s">([^<]+)</span>'
        r'<input[^>]*><span class="t">([^<]+)</span></span>',
        re.DOTALL,
    )
    return [(m.group(2), m.group(1), m.group(3)) for m in pat.finditer(chunk)]

def extract_builders(chunk):
    pat = re.compile(r'<div class="builder" data-answer="([^"]+)">', re.DOTALL)
    return [m.group(1) for m in pat.finditer(chunk)]

# Build KEYS.md
lines = []
lines.append("# Diagnostic Mock · Keys · Andrew Kruglov · TOEFL iBT 2026 (B2+ ceiling)")
lines.append("")
lines.append("All auto-scored answers below. Note: MCQ **letters shuffle on each page load**, so match by TEXT, not by letter.")
lines.append("")

# Section 03 CTW
lines.append("## Section 03 · Complete the Words × 20 (type-in)")
lines.append("")
ctw = extract_ctw(sections.get("s03", ""))
# Split into two paragraphs of 10 each by order
lines.append("Format shown as `stem[middle]tail`. Type only the middle part. Case-insensitive.")
lines.append("")
lines.append("**P1 · Screens before bed and sleep**")
for i, (s, mid, t) in enumerate(ctw[:10], 1):
    lines.append(f"{i:2d}. `{s}[{mid}]{t}`  (word: **{s}{mid}{t}**)")
lines.append("")
lines.append("**P2 · Working from home**")
for i, (s, mid, t) in enumerate(ctw[10:], 1):
    lines.append(f"{i:2d}. `{s}[{mid}]{t}`  (word: **{s}{mid}{t}**)")
lines.append("")

# Sections 04-09 MCQ
section_labels = {
    "s04": "Section 04 · Reading · Daily Life × 8 MCQ",
    "s05": "Section 05 · Reading · Academic Passage × 6 MCQ",
    "s06": "Section 06 · Listening · Choose a Response × 5",
    "s07": "Section 07 · Listening · Conversation × 3 MCQ",
    "s08": "Section 08 · Listening · Announcement × 2 MCQ",
    "s09": "Section 09 · Listening · Academic Talk × 4 MCQ",
}
for sid, label in section_labels.items():
    rows = extract_mcq(sections.get(sid, ""))
    lines.append(f"## {label}")
    lines.append("")
    for i, (q, letter, ct) in enumerate(rows, 1):
        q_short = q[:140]
        lines.append(f"**Q{i}.** {q_short}")
        lines.append(f"  → **{ct}**")
    lines.append("")

# Section 10 Build-a-Sentence
builders = extract_builders(sections.get("s10", ""))
lines.append("## Section 10 · Build-a-Sentence × 10 (target sentences)")
lines.append("")
for i, b in enumerate(builders, 1):
    lines.append(f"{i:2d}. {b}")
lines.append("")

# Section 11-14 self-score reminders
lines.append("## Section 11 · Email · self-score 1–6")
lines.append("")
lines.append("Rubric (visible band 1–6 selector in the page): task completion · tone/register · grammar · vocab · coherence. Compare against the C1 model inside the lesson toggle. Target length: 80–150 words.")
lines.append("")
lines.append("## Section 12 · Academic Discussion · self-score 1–6")
lines.append("")
lines.append("Rubric: clear position · engagement with one classmate · one specific reason · C1 register. Target length: 100–130 words. C1 model inside the lesson toggle.")
lines.append("")
lines.append("## Section 13 · Listen-and-Repeat × 7 · self-rate hit/miss")
lines.append("")
lines.append("Target sentences (in audio_scripts.md):")
lines.append("")
l13 = [
    "I usually have coffee for breakfast.",
    "My brother works at a small design studio.",
    "We're planning a short trip to the mountains next weekend.",
    "If the weather is good tomorrow, we'll probably eat lunch outside.",
    "She told me she had already seen that film at least twice before.",
    "The book I ordered online last week finally arrived, and it looks even better than expected.",
    "Despite feeling tired after the long flight, he unpacked his things and went straight to the office.",
]
for i, s in enumerate(l13, 1):
    lines.append(f"{i:2d}. {s}")
lines.append("")

lines.append("## Section 14 · Interview × 4 · self-score 1–6 each")
lines.append("")
lines.append("No single correct answer. Rubric per answer: fully fills 45 sec · grammatically clean · at least one B2+ structure · at least one specific detail · clear final sentence. Interviewer questions:")
lines.append("")
intv = [
    "Describe your typical morning. What do you usually do between waking up and leaving the house?",
    "Do you prefer spending your free time alone or with other people? Why?",
    "Describe a city you have visited that stayed in your memory. What made it memorable?",
    "If you could change one thing about the way you learn English, what would it be and why?",
]
for i, s in enumerate(intv, 1):
    lines.append(f"{i}. {s}")
lines.append("")

lines.append("## Section 15 · Band mapping")
lines.append("")
lines.append("- **Reading** (34 items): 30-34 → 6 · 24-29 → 5 · 18-23 → 4 · 12-17 → 3 · 6-11 → 2 · 0-5 → 1")
lines.append("- **Listening** (14 items): 12-14 → 6 · 9-11 → 5 · 6-8 → 4 · 4-5 → 3 · 2-3 → 2 · 0-1 → 1")
lines.append("- **Writing**: average of (Build-a-Sentence/10 scaled to 6) + Email band + Discussion band, rounded to half-band")
lines.append("- **Speaking**: average of (LnR hits/7 scaled to 6) + mean of 4 Interview bands, rounded to half-band")
lines.append("- **Overall**: average of four section bands, rounded to half-band")

out = HERE / "KEYS.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out} ({len(lines)} lines)")
