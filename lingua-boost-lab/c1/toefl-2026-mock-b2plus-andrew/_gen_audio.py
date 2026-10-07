"""Generate all 19 audio clips for toefl-2026-mock-b2plus-andrew."""
import asyncio
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import edge_tts

HERE = Path(__file__).resolve().parent
OUT = HERE / "audio"
OUT.mkdir(exist_ok=True)

MATTHEW = "en-US-GuyNeural"
JOANNA = "en-US-JennyNeural"

# (filename, voice, rate, text)
CLIPS = [
    # Section 06 · Choose a Response × 5
    ("lstn-06-01.mp3", JOANNA, "+0%",
     "Excuse me, do you know where I can print this document before class?"),
    ("lstn-06-02.mp3", MATTHEW, "+0%",
     "We're having a small barbecue at my place on Saturday afternoon — want to come?"),
    ("lstn-06-03.mp3", JOANNA, "+0%",
     "My laptop keeps freezing every ten minutes or so — any idea what might be wrong?"),
    ("lstn-06-04.mp3", MATTHEW, "+0%",
     "It's almost ten o'clock. Would you like a quick coffee before we head home?"),
    ("lstn-06-05.mp3", JOANNA, "+0%",
     "There are two trains back — one at six twenty and one at nine forty. Which one would you take?"),

    # Section 07 · Conversation · 11 per-turn clips (concat later)
    ("conv-07-01.mp3", JOANNA, "+0%",
     "Hi, sorry to bother you — I was wondering if I could still drop one of my courses, Economics 240?"),
    ("conv-07-02.mp3", MATTHEW, "+0%",
     "Let me check the dates. Hmm — the drop deadline for this semester was October the first. We're almost two weeks past that."),
    ("conv-07-03.mp3", JOANNA, "+0%",
     "I know, I'm really sorry. The workload turned out heavier than I expected, and I'm worried I'll fail it."),
    ("conv-07-04.mp3", MATTHEW, "+0%",
     "I understand, but the deadline exists for a reason. If I let you drop now, I'd have to let everyone else drop too — and the course is already past the midterm."),
    ("conv-07-05.mp3", JOANNA, "+0%",
     "Isn't there any way to make an exception? My other courses are fine, it's just this one."),
    ("conv-07-06.mp3", MATTHEW, "+0%",
     "I can't change the drop status, no. But what I can do is talk to you about an Incomplete."),
    ("conv-07-07.mp3", JOANNA, "+0%",
     "An Incomplete? How does that work?"),
    ("conv-07-08.mp3", MATTHEW, "+0%",
     "You'd get an I on your transcript instead of a grade, and you'd have one semester to finish the missing work. If you finish, the I is replaced with your real grade. If you don't, it turns into an F."),
    ("conv-07-09.mp3", JOANNA, "+0%",
     "So I'd have until the end of the spring semester to catch up?"),
    ("conv-07-10.mp3", MATTHEW, "+0%",
     "Exactly. Your instructor has to agree first — I'd recommend talking to Dr Patel this week. If he signs off, come back here with the form and I'll process it the same day."),
    ("conv-07-11.mp3", JOANNA, "+0%",
     "Okay, that's actually a lot more helpful than I expected. Thank you — I'll go see him tomorrow."),

    # Section 08 · Announcement
    ("ann-08.mp3", MATTHEW, "-5%",
     "Good morning, everyone. This is a brief update from the Main Library ahead of exam week. "
     "From Monday the eleventh through Friday the fifteenth, the library will open at seven a.m. "
     "instead of nine, and close at midnight instead of ten p.m., to give you extra time to prepare. "
     "Please note that during this week the entire third floor will be a silent-study floor — no group "
     "work, no phone calls. Group study rooms on the first floor can still be booked online for "
     "conversation. One more thing: because of complaints last term, only water in sealed bottles is "
     "allowed inside the library during exam week. No coffee, no food, no snacks — please use the café "
     "on the ground floor. Thank you, and good luck with your exams."),

    # Section 09 · Academic Talk
    ("talk-09.mp3", JOANNA, "-5%",
     "Many of us have a strong preference for studying with music in the background. Why is that, and "
     "does it actually help? Research on this is more mixed than people often assume, but there's a "
     "reasonable summary we can offer today. "
     "The usual starting point is a study by a group of psychologists at Glasgow University. They "
     "found that students revising for a maths exam performed slightly better when they had "
     "instrumental music playing at a low, steady volume, compared with students working in complete "
     "silence. The effect was small but consistent. The leading explanation is that gentle, familiar "
     "sound masks random noise from the environment and reduces the mental energy you spend ignoring "
     "distractions. "
     "However — and this is important — the same researchers found no benefit, and sometimes a clear "
     "cost, when the music had lyrics, or when the volume was high enough to grab attention. And for "
     "tasks involving heavy reading or genuinely new material, silence is probably still the safer "
     "default."),

    # Section 13 · Listen-and-Repeat × 7 (rate -8%)
    ("lnr-13-01.mp3", JOANNA, "-8%",
     "I usually have coffee for breakfast."),
    ("lnr-13-02.mp3", MATTHEW, "-8%",
     "My brother works at a small design studio."),
    ("lnr-13-03.mp3", JOANNA, "-8%",
     "We're planning a short trip to the mountains next weekend."),
    ("lnr-13-04.mp3", MATTHEW, "-8%",
     "If the weather is good tomorrow, we'll probably eat lunch outside."),
    ("lnr-13-05.mp3", JOANNA, "-8%",
     "She told me she had already seen that film at least twice before."),
    ("lnr-13-06.mp3", MATTHEW, "-8%",
     "The book I ordered online last week finally arrived, and it looks even better than expected."),
    ("lnr-13-07.mp3", JOANNA, "-8%",
     "Despite feeling tired after the long flight, he unpacked his things and went straight to the office."),

    # Section 14 · Interview × 4
    ("intv-14-01.mp3", JOANNA, "+0%",
     "Describe your typical morning. What do you usually do between waking up and leaving the house?"),
    ("intv-14-02.mp3", MATTHEW, "+0%",
     "Do you prefer spending your free time alone or with other people? Why?"),
    ("intv-14-03.mp3", JOANNA, "+0%",
     "Describe a city you have visited that stayed in your memory. What made it memorable?"),
    ("intv-14-04.mp3", MATTHEW, "+0%",
     "If you could change one thing about the way you learn English, what would it be and why?"),
]


async def synth(fname, voice, rate, text):
    path = OUT / fname
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(str(path))
    size_kb = path.stat().st_size // 1024
    print(f"  OK  {fname}  ({size_kb} KB)")


async def main():
    print(f"generating {len(CLIPS)} clips -> {OUT}")
    for clip in CLIPS:
        try:
            await synth(*clip)
        except Exception as e:
            print(f"  FAIL {clip[0]}: {e}")
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
