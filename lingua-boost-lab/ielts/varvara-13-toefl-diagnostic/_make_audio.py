"""Generate TOEFL mock L13 audio for Varvara Sules (arts/museum theme) with edge-tts.
Section 06: 5 single-line clips (Choose a Response).
Section 07: 9-turn conversation (student + archivist), concat via ffmpeg.
Section 08: single announcement, Christopher rate -5%.
Section 09: single academic talk, Jenny rate -5%.
"""
import asyncio, os, subprocess, time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audio")
TMP = os.path.join(HERE, "audio", "_tmp")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

JOANNA = "en-US-JennyNeural"
MATTHEW = "en-US-ChristopherNeural"

# ---------- Section 06: Choose a Response x 5 ----------
S06 = [
    ("lstn-06-01.mp3", JOANNA,  "Excuse me, do you know if the museum café is still open? I was hoping to grab something before it closes."),
    ("lstn-06-02.mp3", MATTHEW, "A few of us are going to the National Gallery on Saturday afternoon — would you like to come along?"),
    ("lstn-06-03.mp3", JOANNA,  "This printer has been giving me trouble all morning. Any idea how to get it working again?"),
    ("lstn-06-04.mp3", MATTHEW, "Would you mind swapping seats so my friend and I can sit together for the film?"),
    ("lstn-06-05.mp3", JOANNA,  "There are two tours of the exhibition on Sunday — one at eleven in the morning and one at four in the afternoon. Which would you take?"),
]

# ---------- Section 07: Conversation (student + archivist, 9 turns) ----------
S07_TURNS = [
    (JOANNA,  "Hi, sorry to interrupt. I'm working on my dissertation, and I was hoping to look at some nineteenth-century exhibition catalogues that you keep in the special collections."),
    (MATTHEW, "Of course. Have you registered as a reader with us yet, or is this your first visit to the archive?"),
    (JOANNA,  "It's my first time — I've brought my university ID and a short letter from my supervisor, if that's useful."),
    (MATTHEW, "Perfect. You'll need to fill out a brief reader's form first, and then I can set up an account for you. One thing to keep in mind — the nineteenth-century material is particularly fragile, so items have to be requested at least a day in advance."),
    (JOANNA,  "Oh, I was really hoping to get started today. Is there anything I could look at right now while I wait for tomorrow?"),
    (MATTHEW, "Most of our printed catalogues from the eighteen-eighties onwards have already been digitised. If you tell me a bit about your topic, I can point you to the online finding aid, and you can work on that until your physical items arrive."),
    (JOANNA,  "That would be great. I'm looking at how smaller galleries presented themselves differently from the big royal exhibitions in the same period."),
    (MATTHEW, "In that case, I'd particularly recommend the Grosvenor Gallery files — they're well-documented and they fit your angle quite neatly. Would you like me to email you the shelfmarks?"),
    (JOANNA,  "Yes, please. Thank you — this has been much more helpful than I was expecting."),
]

# ---------- Section 08: Announcement ----------
S08_TEXT = ("Attention, readers in the main reading room. From Monday the twelfth, the collection reading room will close thirty minutes earlier than usual — at half past six, instead of seven. This change is in response to building-maintenance work that has been scheduled for every evening next month. Readers who need access to special collections material should place their requests before four in the afternoon, as items cannot be retrieved from the store after that time. There is no change to the Saturday schedule, and the online catalogue remains fully available at all hours. We apologise for any inconvenience; the arrangement is temporary and will be reviewed in early January.")

# ---------- Section 09: Academic talk (sleep & creative problem-solving) ----------
S09_TEXT = ("Today I want to talk briefly about a well-established finding in sleep research: the role of REM sleep in creative problem-solving. The idea is simple. If you are stuck on a difficult problem, a single night of sleep that includes enough rapid-eye-movement, or REM, sleep will often help you see solutions that were invisible to you the day before. A series of studies by Walker and colleagues at Berkeley showed this effect across hundreds of participants, with word puzzles, logical riddles, and even design tasks. The size of the benefit was striking — people who had slept were roughly twice as likely to find a creative solution as those who had simply worked through the problem awake. Consider a student struggling with an essay structure. One long, late-night session may feel productive because the effort is intense. But the structural insight often comes only after the brain has had time to rearrange information during sleep. Short bursts of focused work followed by rest feel slower, but the breakthroughs stick. One caveat: for very mechanical tasks, like memorising dates, the benefit is much smaller, because creativity isn't really what's being measured.")


async def tts(text, voice, out_path, rate="+0%"):
    """Generate one clip with edge-tts, retry on 403."""
    for attempt in range(3):
        try:
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                return
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(out_path)
            if os.path.getsize(out_path) > 0:
                return
        except Exception as e:
            print(f"  [{attempt+1}] {os.path.basename(out_path)} failed: {e}")
            if os.path.exists(out_path) and os.path.getsize(out_path) == 0:
                os.remove(out_path)
            time.sleep(5)
    raise RuntimeError(f"Failed to generate {out_path}")


def ffconcat(parts, out_mp3, silence_sec=0.4):
    """Concat mp3s with short silence gaps using ffmpeg concat filter."""
    silence = os.path.join(TMP, "_silence.mp3")
    if not os.path.exists(silence):
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"anullsrc=channel_layout=mono:sample_rate=24000",
            "-t", str(silence_sec), "-q:a", "9", silence
        ], check=True, capture_output=True)
    lst = os.path.join(TMP, "_list.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for i, p in enumerate(parts):
            f.write(f"file '{p.replace(chr(92), '/')}'\n")
            if i < len(parts) - 1:
                f.write(f"file '{silence.replace(chr(92), '/')}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", lst, "-c", "copy", out_mp3
    ], check=True, capture_output=True)


async def main():
    print("S06: 5 clips")
    for fname, voice, text in S06:
        out = os.path.join(OUT, fname)
        await tts(text, voice, out)
        print(f"  {fname} . {os.path.getsize(out)} bytes")

    print("S07: 9-turn conversation")
    parts = []
    for i, (voice, line) in enumerate(S07_TURNS, 1):
        p = os.path.join(TMP, f"conv-07-t{i:02d}.mp3")
        await tts(line, voice, p)
        parts.append(p)
    conv_out = os.path.join(OUT, "conv-07.mp3")
    ffconcat(parts, conv_out, silence_sec=0.35)
    print(f"  conv-07.mp3 . {os.path.getsize(conv_out)} bytes")

    print("S08: announcement")
    out = os.path.join(OUT, "ann-08.mp3")
    await tts(S08_TEXT, MATTHEW, out, rate="-5%")
    print(f"  ann-08.mp3 . {os.path.getsize(out)} bytes")

    print("S09: academic talk")
    out = os.path.join(OUT, "talk-09.mp3")
    await tts(S09_TEXT, JOANNA, out, rate="-5%")
    print(f"  talk-09.mp3 . {os.path.getsize(out)} bytes")

    print("DONE")

if __name__ == "__main__":
    asyncio.run(main())
