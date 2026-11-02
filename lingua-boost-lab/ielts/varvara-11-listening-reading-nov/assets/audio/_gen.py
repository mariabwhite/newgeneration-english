"""Generate 3 IELTS listening MP3s for L11 Variety Pack via edge-tts.
Topics: furniture rental call (S1 dialog), career counseling (S3 dialog), sleep psychology (S4 lecture).
Run: py -3 _gen.py
"""
import asyncio, os, sys, subprocess, tempfile
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent
ONLY = os.environ.get("ONLY", "").strip()

MONO_TRACKS = [
    ("l11-s2-festival-map.mp3", "en-GB-SoniaNeural",
     "Hello everyone, and welcome to Riverside Music Festival. "
     "I'm Chloe, one of the stewards, and I'll run through the site layout before you head in. "
     "If you look at your site map, you'll see the main entrance at the bottom — that's where you just came through. "
     "The box office is immediately on your right as you enter, that's position A, just inside the gate — "
     "collect any pre-booked wristbands and lost tickets there. "
     "Now, follow the central path straight ahead, past the big oak tree. "
     "At the end of that path, in the top-left corner of the site, you'll find the main stage. "
     "That's position B. The headline acts play there from six o'clock each evening. "
     "The second stage is much smaller — acoustic sets and local bands only — and it's in the top-right corner, position C. "
     "If you want to grab a bite, the food court is in the middle of the site, right next to the oak tree — position D. "
     "We've got around twenty food trucks there, hot food served until midnight. "
     "The toilets — a note of warning — the toilets are not where you might expect. "
     "They're not next to the food court. They are tucked away on the left-hand side of the site, "
     "roughly halfway between the entrance and the main stage, position E. "
     "There's also a second bank of toilets closer to the camping area, but position E is the big one. "
     "First aid — very important — is clearly signposted. "
     "It's on the right-hand side of the site, directly between the box office and the second stage, position F. "
     "If you need any medical help at all, head straight there. "
     "And finally, if you're camping with us this weekend, the campsite entrance is a separate gate — "
     "it's at the very far end of the site, past the main stage, in the bottom-left corner, position G. "
     "Overnight guests only; wristbands required to enter. "
     "Right, that's it from me. Enjoy the music, drink lots of water, and if you get lost, just find a steward in a yellow vest. "
     "Have a brilliant weekend."),

    ("l11-s4-sleep-psychology.mp3", "en-GB-LibbyNeural",
     "Right, this morning's lecture is on the psychology of sleep, "
     "and specifically the role that sleep plays in long-term memory consolidation. "
     "For roughly a century, researchers assumed that memory was essentially a passive residue — "
     "that experiences left faint traces in the brain, and that over time these traces simply faded. "
     "The modern view, developed since the nineteen nineties, is almost the opposite. "
     "Memory is now understood as an active, overnight process. "
     "During the deepest stage of sleep, known as slow-wave sleep, "
     "the brain selectively replays the day's experiences at roughly twenty times normal speed. "
     "A key study by the German researcher Jan Born in two thousand and four demonstrated this very neatly. "
     "Volunteers who learned a motor task in the afternoon showed a thirty percent improvement the following morning — "
     "but only if they were allowed to sleep normally. "
     "Volunteers kept awake for the same duration showed almost no improvement at all. "
     "A separate line of research, led by Matthew Walker at Berkeley, "
     "has focused on the role of rapid-eye-movement sleep, "
     "or REM, in emotional regulation. "
     "Walker's team found that REM sleep selectively strips emotional charge from stressful memories, "
     "leaving the factual content intact. "
     "This explains the common experience that a problem seems less overwhelming after a night's rest. "
     "The practical implications are considerable. "
     "Chronic sleep deprivation — now estimated to affect roughly a third of adults in industrialised countries — "
     "has been linked not only to poor memory performance, "
     "but also to a measurably higher risk of anxiety and depression. "
     "The World Health Organization in twenty eighteen officially classified night-shift work "
     "as a probable carcinogen, "
     "largely because of the way it disrupts the body's circadian clock. "
     "Looking forward, researchers at University College London are now trialling a technique "
     "known as targeted memory reactivation. "
     "Specific sounds associated with learning tasks are quietly played back to volunteers during slow-wave sleep, "
     "and this appears to boost recall even further. "
     "Early results, published last year in the journal Nature, suggest improvements of around fifteen percent "
     "compared with sleep alone. "
     "The authors caution that it is far too early to recommend any of this for home use."),
]

DIALOGUES = [
    ("l11-s1-furniture-rental.mp3", [
        ("en-GB-RyanNeural",   "Good afternoon, City Furniture Hire, how can I help?"),
        ("en-GB-LibbyNeural",  "Hi, I'd like to rent some furniture for a flat I'm moving into next week."),
        ("en-GB-RyanNeural",   "Of course. Can I take your name, please?"),
        ("en-GB-LibbyNeural",  "Marta Dvorak — D-V-O-R-A-K."),
        ("en-GB-RyanNeural",   "Thank you. And the delivery address?"),
        ("en-GB-LibbyNeural",  "It's flat 7B, Elmwood Court, that's E-L-M-W-O-O-D."),
        ("en-GB-RyanNeural",   "And the postcode?"),
        ("en-GB-LibbyNeural",  "SE19 4RT."),
        ("en-GB-RyanNeural",   "Lovely. What date would suit for delivery?"),
        ("en-GB-LibbyNeural",  "Could we do Saturday the twenty-second?"),
        ("en-GB-RyanNeural",   "Saturday the twenty-second, noted. We have two slots left — morning, eight to twelve, or afternoon, one to five."),
        ("en-GB-LibbyNeural",  "Afternoon, please."),
        ("en-GB-RyanNeural",   "Right. Now, which items would you like?"),
        ("en-GB-LibbyNeural",  "A double bed, a sofa, and a desk."),
        ("en-GB-RyanNeural",   "A double bed is forty pounds a month, the sofa is sixty, and a standard writing desk is twenty-five. That's a hundred and twenty-five a month, plus a one-off delivery charge of thirty."),
        ("en-GB-LibbyNeural",  "Could you deliver the mattress too? I forgot about that."),
        ("en-GB-RyanNeural",   "No extra charge — the mattress always comes bundled with the bed."),
        ("en-GB-LibbyNeural",  "Perfect. And how long is the minimum rental?"),
        ("en-GB-RyanNeural",   "Three months. After that it's rolling, cancellable with two weeks' notice."),
        ("en-GB-LibbyNeural",  "And payment?"),
        ("en-GB-RyanNeural",   "Direct debit, taken on the first of each month. Your reference will be F H nine two one four."),
    ]),
    ("l11-s3-career-counseling.mp3", [
        ("en-GB-RyanNeural",   "Hi, Mia, come in. So you wanted to talk through your options for after graduation. Where are you leaning?"),
        ("en-GB-LibbyNeural",  "Honestly, I'm torn. I've got a conditional offer from a graduate scheme in London, but I'm also tempted to apply for a one-year research assistantship at the Max Planck Institute in Berlin."),
        ("en-GB-RyanNeural",   "Right. And what's drawing you to the research assistantship?"),
        ("en-GB-LibbyNeural",  "I think it would actually test whether I want to go on to a PhD. The graduate scheme pays much better immediately, but it's a corporate role — I'd be unlikely to publish anything."),
        ("en-GB-RyanNeural",   "That's a fair reading. One thing worth bearing in mind: the research assistantship pays very little, but Max Planck covers your health insurance and your accommodation stipend separately — so the headline salary understates what you'd actually have in hand."),
        ("en-GB-LibbyNeural",  "I didn't know that. That changes things."),
        ("en-GB-RyanNeural",   "Does your supervisor know you're considering both?"),
        ("en-GB-LibbyNeural",  "Not yet. I was planning to tell her next week."),
        ("en-GB-RyanNeural",   "A word of advice — tell her now. If you leave it, and the graduate scheme asks for a decision first, you'll feel rushed, and she won't have time to write you a strong supporting reference."),
        ("en-GB-LibbyNeural",  "That's a good point."),
        ("en-GB-RyanNeural",   "And one more thing. If you go with the research route, make sure you negotiate a clear deliverable up front — ideally a draft paper or chapter you can take with you. Otherwise a year disappears quickly, and you'll leave Berlin with experience but nothing on paper."),
        ("en-GB-LibbyNeural",  "I'll build that into any conversation with the Berlin team. Thanks."),
        ("en-GB-RyanNeural",   "One last thing — regardless of which you choose, apply for the Rhodes Trust travel grant next spring. It's small money, two thousand five hundred pounds, but it looks very good on an application. Deadline is the first of March."),
    ]),
]


async def gen_single(out_name, voice, text, retries=3):
    out = HERE / out_name
    for i in range(retries):
        try:
            comm = edge_tts.Communicate(text, voice=voice, rate="-5%")
            await comm.save(str(out))
            if out.exists() and out.stat().st_size > 0:
                print(f"[ok] {out_name}  ({out.stat().st_size//1024} KB)  voice={voice}")
                return
            raise RuntimeError("zero-byte output")
        except Exception as e:
            print(f"[retry {i+1}/{retries}] {out_name}  err={e}")
            await asyncio.sleep(3 + i * 2)
    print(f"[FAIL] {out_name}")


async def gen_dialogue(out_name, turns):
    out = HERE / out_name
    tmpdir = Path(tempfile.mkdtemp(prefix="l11_"))
    parts = []
    for i, (voice, line) in enumerate(turns):
        part = tmpdir / f"t{i:02d}.mp3"
        for attempt in range(3):
            try:
                comm = edge_tts.Communicate(line, voice=voice, rate="-5%")
                await comm.save(str(part))
                if part.exists() and part.stat().st_size > 0:
                    break
            except Exception as e:
                print(f"  [turn {i} retry {attempt+1}] err={e}")
                await asyncio.sleep(3)
        if not part.exists() or part.stat().st_size == 0:
            print(f"  [FAIL turn {i}]")
            return
        parts.append(part)
    silence = tmpdir / "sil.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i",
                    "anullsrc=r=24000:cl=mono", "-t", "0.35",
                    "-q:a", "9", "-acodec", "libmp3lame", str(silence)],
                   check=False, capture_output=True)
    listfile = tmpdir / "list.txt"
    with open(listfile, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p.as_posix()}'\n")
            f.write(f"file '{silence.as_posix()}'\n")
    r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                        "-i", str(listfile), "-c", "copy", str(out)],
                       capture_output=True)
    if r.returncode == 0 and out.exists() and out.stat().st_size > 0:
        print(f"[ok] {out_name}  ({out.stat().st_size//1024} KB)  turns={len(parts)}")
    else:
        print(f"[FAIL] {out_name}  stderr={r.stderr.decode(errors='ignore')[-400:]}")


async def main():
    tasks = []
    for name, voice, text in MONO_TRACKS:
        if ONLY and ONLY != name: continue
        if (HERE / name).exists() and (HERE / name).stat().st_size > 0 and not ONLY:
            print(f"[skip existing] {name}")
            continue
        tasks.append(gen_single(name, voice, text))
    for name, turns in DIALOGUES:
        if ONLY and ONLY != name: continue
        if (HERE / name).exists() and (HERE / name).stat().st_size > 0 and not ONLY:
            print(f"[skip existing] {name}")
            continue
        tasks.append(gen_dialogue(name, turns))
    await asyncio.gather(*tasks)
    print("done.")


if __name__ == "__main__":
    asyncio.run(main())
