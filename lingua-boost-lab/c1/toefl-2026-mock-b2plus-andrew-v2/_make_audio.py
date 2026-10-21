"""Generate TOEFL mock v2 audio with edge-tts.
Section 06: 5 single-line clips.
Section 07: 10-turn conversation (Jenny + Christopher), concat via ffmpeg.
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
    ("lstn-06-01.mp3", JOANNA,  "Excuse me, do you know where I can top up my travel card? I think mine just ran out."),
    ("lstn-06-02.mp3", MATTHEW, "We're thinking of going for pizza on Thursday evening — would you like to come along?"),
    ("lstn-06-03.mp3", JOANNA,  "My phone keeps dropping the Wi-Fi at home — any idea what might be wrong?"),
    ("lstn-06-04.mp3", MATTHEW, "Would you mind if I opened the window a little? It's getting pretty warm in here."),
    ("lstn-06-05.mp3", JOANNA,  "There are two flights home on Sunday — one at nine in the morning and one at six in the evening. Which would you take?"),
]

# ---------- Section 07: Conversation 10 turns ----------
S07_TURNS = [
    (JOANNA,  "Hi, sorry to bother you. I was hoping to book one of the group-study rooms on the second floor for Friday evening."),
    (MATTHEW, "Sure, let me check. How many of you are there and what time are you thinking?"),
    (JOANNA,  "Six of us, from about seven till ten. We've got a group presentation on Monday and we really need somewhere we can talk without annoying people."),
    (MATTHEW, "Okay, Friday evening is already pretty full. Room B is free from seven to nine, but after nine I only have Room D on the third floor."),
    (JOANNA,  "Oh. Could we start in Room B and then move upstairs at nine?"),
    (MATTHEW, "You could, but honestly, moving a group of six mid-session is a nightmare. I'd suggest just booking Room D for the full three hours — it's a bit smaller, but you'll keep your flow."),
    (JOANNA,  "That's a good point. Let's do Room D then, seven till ten."),
    (MATTHEW, "Done. One thing — Room D doesn't have a whiteboard. If you need one, I can lend you a portable one from the help desk."),
    (JOANNA,  "Yes, please, that would be great. Thank you."),
]

# ---------- Section 08: Announcement ----------
S08_TEXT = ("Attention, all commuting students. From Monday the fifteenth, the campus shuttle bus between the main gate and the north halls of residence will run every twenty minutes instead of every fifteen. The last shuttle of the day will now leave the main gate at eleven thirty, half an hour earlier than before. Students returning from evening events after that time should use the night bus number twenty-two, which stops directly outside the main library. There is no change to the morning schedule. We apologise for any inconvenience; the adjustment is temporary and will be reviewed in January.")

# ---------- Section 09: Academic talk ----------
S09_TEXT = ("Today I want to talk briefly about a surprisingly robust finding in learning research: spacing. The idea is simple. If you have four hours to spend on a topic, you will remember more a month later if you break those hours into four one-hour sessions on four different days than if you do all four hours in one sitting. A classic study by Cepeda and colleagues showed this effect across more than three hundred experiments, with language vocabulary, maths facts, and even motor skills. The size of the benefit was not small — spaced learners sometimes remembered twice as much after a delay. Take a student revising vocabulary for a test. One long cramming session the night before feels productive because recall is high at that moment. But the material drops away quickly over the next week. Short sessions spread over several days feel slower, but the memory sticks. One caveat: for very short-term goals, like an exam tomorrow morning, cramming can still outperform spacing, simply because there is no time for forgetting to happen either way.")


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
        print(f"  {fname} · {os.path.getsize(out)} bytes")

    print("S07: 10-turn conversation")
    parts = []
    for i, (voice, line) in enumerate(S07_TURNS, 1):
        p = os.path.join(TMP, f"conv-07-t{i:02d}.mp3")
        await tts(line, voice, p)
        parts.append(p)
    conv_out = os.path.join(OUT, "conv-07.mp3")
    ffconcat(parts, conv_out, silence_sec=0.35)
    print(f"  conv-07.mp3 · {os.path.getsize(conv_out)} bytes")

    print("S08: announcement")
    out = os.path.join(OUT, "ann-08.mp3")
    await tts(S08_TEXT, MATTHEW, out, rate="-5%")
    print(f"  ann-08.mp3 · {os.path.getsize(out)} bytes")

    print("S09: academic talk")
    out = os.path.join(OUT, "talk-09.mp3")
    await tts(S09_TEXT, JOANNA, out, rate="-5%")
    print(f"  talk-09.mp3 · {os.path.getsize(out)} bytes")

    print("DONE")

if __name__ == "__main__":
    asyncio.run(main())
