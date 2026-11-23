"""
Generate audio for extended speaking section (14g-14j).
15 files total. Uses edge-tts; concatenates multi-voice turns via ffmpeg.
Skips files that already exist.
"""
import asyncio, os, subprocess, tempfile, sys
import edge_tts

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
os.makedirs(OUT, exist_ok=True)

# Voices
V_ARIA = "en-US-AriaNeural"           # female student / narrator
V_GUY = "en-US-GuyNeural"             # male student
V_CHRIS = "en-US-ChristopherNeural"   # professor (Task 3)
V_ROGER = "en-US-RogerNeural"         # professor (Task 4)
V_JENNY = "en-US-JennyNeural"         # pronunciation demos

def ffmpeg_concat(parts, out_path):
    """Concat mp3 parts into one using ffmpeg concat demuxer."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p.replace(os.sep, '/')}'\n")
        list_file = f.name
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
         "-c:v", "copy", "-c:a", "copy", out_path],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    os.unlink(list_file)

async def tts_to_file(text, voice, path, rate="-4%"):
    """Simple edge-tts generation with retry on 403."""
    for attempt in range(4):
        try:
            comm = edge_tts.Communicate(text, voice=voice, rate=rate)
            await comm.save(path)
            if os.path.exists(path) and os.path.getsize(path) > 0:
                return
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}")
            await asyncio.sleep(5)
    raise RuntimeError(f"edge-tts failed for {path}")

async def make_single(voice, text, out_name, rate="-4%"):
    out_path = os.path.join(OUT, out_name)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"SKIP {out_name} (exists)")
        return
    print(f"GEN  {out_name} · {voice} · {len(text)} chars")
    await tts_to_file(text, voice, out_path, rate=rate)

async def make_multi(turns, out_name, rate="-4%"):
    """turns = [(voice, text), ...] — concat into single file."""
    out_path = os.path.join(OUT, out_name)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        print(f"SKIP {out_name} (exists)")
        return
    print(f"GEN  {out_name} · {len(turns)} turns")
    with tempfile.TemporaryDirectory() as td:
        parts = []
        for i, (voice, text) in enumerate(turns):
            pp = os.path.join(td, f"p{i:02d}.mp3")
            await tts_to_file(text, voice, pp, rate=rate)
            parts.append(pp)
        ffmpeg_concat(parts, out_path)

# ============================================================
# TASK 2 · Campus conversation + prompt
# ============================================================
TASK2_CONV_TURNS = [
    (V_ARIA, "So, did you read the new admissions notice for the Art History MA?"),
    (V_GUY, "Yeah, the one about the studio-art prerequisite. Honestly, I'm not sure what to think about it."),
    (V_ARIA, "Really? I actually think it's going to help us. I've been in studio classes, and the moment you try to glaze an oil layer yourself, or carve a small piece of limewood, you start reading other paintings completely differently. You notice the direction of brushstrokes, you feel how heavy the material is — things you just can't get from a slide in a lecture hall."),
    (V_GUY, "OK, but what about students coming from more theoretical backgrounds? Philosophy, literature — they haven't touched a canvas since school."),
    (V_ARIA, "That's actually my second reason for liking it. The bridge course is built specifically for them. It's one semester, on campus, and it covers the three main techniques they'd miss. So no one is shut out — they just get an extra on-ramp. I think it's fair."),
    (V_GUY, "Hmm. When you put it like that, it does sound reasonable."),
]

TASK2_PROMPT = (
    "The woman expresses her opinion of the new admissions policy. "
    "State her opinion, and explain the reasons she gives for holding it. "
    "You have thirty seconds to prepare, and sixty seconds to speak."
)

# ============================================================
# TASK 3 · Reading-based lecture + prompt
# ============================================================
TASK3_LECTURE = (
    "So, when Panofsky distinguishes iconography from iconology, he's really asking two different questions. "
    "Iconography asks: what is depicted? It identifies the subjects — a woman holding a lily is the Virgin Annunciate, a man with keys is Peter. "
    "Iconology goes one layer deeper. It asks: what cultural, philosophical, political worldview made this particular combination of symbols meaningful at this moment in history? "
    "Take Botticelli's Primavera. An iconographic reading tells you: on the right, Zephyr pursues Chloris, who transforms into Flora; in the centre, Venus presides; on the left, the three Graces dance, and Mercury disperses the clouds. That's identification. "
    "An iconological reading goes further. It asks why the Medici, who commissioned the panel, wanted a Neoplatonic allegory of spiritual love refining into civic virtue, painted for a wedding chamber in 1480s Florence. "
    "The individual figures are iconography. The reason an educated Florentine humanist would read the whole garden as a programme of philosophical ascent — that's iconology."
)

TASK3_PROMPT = (
    "Using the example of Botticelli's Primavera from the professor's lecture, "
    "explain the difference between iconography and iconology. "
    "You have thirty seconds to prepare, and sixty seconds to speak."
)

# ============================================================
# TASK 4 · Lecture-only + prompt
# ============================================================
TASK4_LECTURE = (
    "Today I want to show you how Baroque painters weaponised light. "
    "The technique is called chiaroscuro — literally light-dark — a dramatic contrast where a single, often unseen, source of light carves subjects out of near-total darkness. "
    "The darkness isn't passive background. It's an active compositional tool: it decides what you see, in what order, and how urgently. "
    "Consider Caravaggio's Calling of Saint Matthew, 1600. A hard shaft of light cuts diagonally across the canvas from the upper right. It lands on Matthew's face and on the coins on the table. The rest of the room — the walls, the floor, half of the figures — is swallowed by shadow. "
    "The light is doing theological work: it is the moment of grace arriving, selecting Matthew, and nothing else in the scene exists until that selection happens. "
    "Now compare Georges de La Tour's Repentant Magdalene, around 1640. Here the only light source is a single candle flame, reflected in a mirror beside the Magdalene's hand. Everything softens. The shadows breathe. "
    "Chiaroscuro has shifted from Caravaggio's confrontation to a slow, meditative stillness — but it's still the same principle: subtract all light but one, and the remaining light becomes a protagonist."
)

TASK4_PROMPT = (
    "Using the two paintings described by the professor, "
    "explain how chiaroscuro functions as a compositional technique in Baroque painting. "
    "You have twenty seconds to prepare, and sixty seconds to speak."
)

# ============================================================
# PRONUNCIATION × 12
# ============================================================
PRON = [
    ("pron-01.mp3", V_JENNY, "The OBject of the study was clear, but two reviewers obJECTed to the method."),
    ("pron-02.mp3", V_GUY,   "She kept a careful REcord of every session while the archive reCORded her lectures."),
    ("pron-03.mp3", V_JENNY, "Her research PROject depends on slides that proJECT cleanly in the gallery."),
    ("pron-04.mp3", V_GUY,   "The CONtrast is striking when you conTRAST Caravaggio with La Tour."),
    ("pron-05.mp3", V_ARIA,  "Not the Baroque — the Rococo."),
    ("pron-06.mp3", V_CHRIS, "Vermeer painted it. ... Vermeer painted it."),
    ("pron-07.mp3", V_JENNY, "She finished the dissertation first. ... She finished the dissertation first."),
    ("pron-08.mp3", V_GUY,   "Caravaggio uses light to select a figure; La Tour uses light to calm one."),
    ("pron-09.mp3", V_ARIA,  "An idea of it. An idea of it. An idea of it."),
    ("pron-10.mp3", V_GUY,   "I want to write about it. I wanna write about it."),
    ("pron-11.mp3", V_JENNY, "Last year. Last year. Old man. Old man."),
    ("pron-12.mp3", V_ARIA,  "She has been working on it. She's been working on it."),
]

# ============================================================
# 14k · TOEFL 2026 INTERVIEW · Nov sliv × 2 threads × 4 Qs
# ============================================================
INTERVIEW_K = [
    # Thread A · Environment (Nov 10 2026 reported set)
    ("intv-k-A1.mp3", V_ARIA,
     "Thank you for speaking with me today. First, could you tell me what you do in your daily life to help protect the environment? For example, do you recycle, save energy at home, or use public transportation?"),
    ("intv-k-A2.mp3", V_ARIA,
     "OK. When you shop for things like clothes or electronics, do you usually choose the cheapest option, or are you willing to pay more for products that are better for the environment? Please explain your choice."),
    ("intv-k-A3.mp3", V_ARIA,
     "Thanks. Now, I'm curious about your opinion. Many cities are now building more space for electric scooters and bicycles. Do you think that in the future most people in cities will stop using cars? Why or why not?"),
    ("intv-k-A4.mp3", V_ARIA,
     "That's a helpful answer. Here's my last question. Some people think protecting the environment is mainly the job of governments and large companies, while others believe ordinary people should take the most responsibility. Which view do you agree with and why?"),
    # Thread B · AI & technology
    ("intv-k-B1.mp3", V_ARIA,
     "Thanks for joining me. First, how often do you use AI tools like chatbots, translators, or image generators in your daily life? Tell me about one recent example."),
    ("intv-k-B2.mp3", V_ARIA,
     "OK. When you need information quickly, do you prefer asking an AI assistant, or searching with a traditional search engine? Why?"),
    ("intv-k-B3.mp3", V_ARIA,
     "Now, I'd like your opinion. Some people say AI tools are making students lazier; others say they are making studying more efficient. What is your view?"),
    ("intv-k-B4.mp3", V_ARIA,
     "Last question. Should universities ban the use of AI for coursework, allow it only with full disclosure, or integrate it as a normal study tool? Which position would you support, and why?"),
]

async def main():
    # Prompts (short narrator cues)
    await make_single(V_ARIA, TASK2_PROMPT, "task2-prompt.mp3", rate="-6%")
    await make_single(V_ARIA, TASK3_PROMPT, "task3-prompt.mp3", rate="-6%")
    await make_single(V_ARIA, TASK4_PROMPT, "task4-prompt.mp3", rate="-6%")

    # Multi-voice conversation (Task 2)
    await make_multi(TASK2_CONV_TURNS, "task2-conv.mp3", rate="-4%")

    # Lectures (Tasks 3 and 4) — single voice
    await make_single(V_CHRIS, TASK3_LECTURE, "task3-lecture.mp3", rate="-6%")
    await make_single(V_ROGER, TASK4_LECTURE, "task4-lecture.mp3", rate="-6%")

    # Pronunciation
    for fname, voice, text in PRON:
        await make_single(voice, text, fname, rate="-8%")

    # TOEFL 2026 Interview (14k)
    for fname, voice, text in INTERVIEW_K:
        await make_single(voice, text, fname, rate="-4%")

    print("\nDONE.")

if __name__ == "__main__":
    asyncio.run(main())
