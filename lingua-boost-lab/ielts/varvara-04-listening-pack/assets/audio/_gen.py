"""Generate 5 IELTS listening MP3s for varvara-04-listening-pack via edge-tts.
Run: py -3 _gen.py
"""
import asyncio, sys
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent

# Single-voice tracks
MONO_TRACKS = [
    ("l-02-outreach-programmes.mp3", "en-GB-LibbyNeural",
     "Hello everyone, and welcome to the Ashfield Regional Art Museum. "
     "I'd like to run through the four community outreach programmes we're offering this autumn. "
     "First, the Little Explorers workshop is for children aged five to seven. "
     "Sessions run every Saturday morning and the fee is just three pounds per child, "
     "which includes all art materials. "
     "Our second programme, Junior Curators, is aimed at ten to fourteen year olds. "
     "This one runs on Wednesday evenings, and the cost is eight pounds per session. "
     "Third, we have Sketch and Chat, an informal drawing group for adults, no experience needed. "
     "This meets on the first Sunday of every month and it is completely free of charge. "
     "And finally, our Silver Circle programme for visitors over sixty-five "
     "offers guided tours followed by afternoon tea, every second Tuesday, "
     "for a discounted price of five pounds per person. "
     "Booking is essential for all four programmes."),

    ("l-03-autumn-exhibitions.mp3", "en-GB-MaisieNeural",
     "This week on Gallery Round-up we're looking at five autumn exhibitions across London. "
     "First, Threads of Empire at the Victoria and Albert - a huge textiles show, "
     "and importantly, admission is completely free for everyone. "
     "Next, Faces of Byzantium at the British Museum. "
     "This one is small, only two rooms, but the objects are extraordinary. "
     "Third, the Turner Contemporary showcase at Tate Britain - this one you must book online in advance, "
     "even for members, as timed entry is strictly enforced. "
     "Fourth, Painting Light at Dulwich Picture Gallery - "
     "the standout feature here is the interactive digital wall where visitors compose their own landscapes. "
     "And finally, Small Wonders at the Courtauld Institute. "
     "This is designed with families in mind: activity trails, dressing-up corner, and craft tables in every room."),

    ("l-06-fishbourne-dig.mp3", "en-GB-SoniaNeural",
     "Welcome to Fishbourne Roman Palace, and thank you for signing up to volunteer this season. "
     "Before we head out to the trenches, three quick practical notes. "
     "First, our daily schedule. Work on site starts at seven thirty sharp. "
     "The main gate locks automatically at seven forty-five, so please arrive early; "
     "we cannot buzz anyone in once the safety briefing has begun. "
     "Second, what to bring and what we provide. "
     "You must bring your own sturdy boots, a wide-brimmed sunhat, and a packed lunch. "
     "We provide gloves, trowels and drinking water free of charge — "
     "no need to carry any of those yourselves. "
     "Third, and this is non-negotiable: your signed insurance form. "
     "Without it we are not permitted to allow you anywhere near the trench, no exceptions. "
     "A few last details. Lunch break is at twelve noon and the working day ends at four. "
     "However, the conservation lab stays open for one more hour after that — until five — "
     "and anyone who wants to help wash and label finds is very welcome to stay on. "
     "Finally, if you lose the group during a tour or hear the weather alert siren, "
     "the muster point is the old oak tree beside the ticket office. "
     "Not the car park, not the gift shop — the old oak tree. Any questions before we head out?"),

    ("l-07-hypocaust-lecture.mp3", "en-GB-RyanNeural",
     "Today I'd like to introduce you to one of the most ingenious domestic technologies "
     "the Romans ever developed — the hypocaust, or underfloor heating system. "
     "If you look at the cross-section on your handout, you'll see six numbered components. "
     "Let's work through them from the bottom up. "
     "Number one, at the lower left, is the furnace itself, which the Romans called the praefurnium. "
     "It was tended by a slave standing outside the house, feeding wood into the fire. "
     "Number two is the large empty space directly beneath the floor — the hypocaust chamber. "
     "This is where the hot gases from the furnace were allowed to circulate freely. "
     "The floor was held up above that chamber by short stacks of square tiles, "
     "and these supporting columns were known as pilae — that's number three on the diagram. "
     "Resting on top of the pilae sits the raised floor itself, labelled number four, "
     "typically finished with a decorative mosaic in the main rooms. "
     "Now, the clever part. Hot air didn't just warm the floor; it also rose up through the walls, "
     "using special hollow wall-tiles called tubuli. That system of wall-tiles is number five. "
     "And finally, having passed through the floor and the walls, the smoke and spent gases escaped "
     "through a chimney vent at the roofline — number six on the diagram. "
     "The great advantage of this design is that no smoke whatsoever ever enters the living space; "
     "only the warmth radiates up through the floor and the walls. "
     "A well-maintained Roman hypocaust could keep a dining room at a steady twenty-two degrees Celsius "
     "even on a January day — quite a feat with no boiler, no radiators, and no electricity."),

    ("l-05-caravanserai-lecture.mp3", "en-GB-LibbyNeural",
     "Right, so today I want to talk about recent satellite archaeology along the Silk Road, "
     "and specifically the identification of previously unknown caravanserai. "
     "For those who need a reminder, a caravanserai was a roadside inn "
     "where traders and their animals could rest overnight. "
     "These structures were typically spaced about thirty kilometres apart, "
     "which corresponds to a single day's travel by camel. "
     "In two thousand and seventeen, a joint team from Oxford and Samarkand universities "
     "began systematic analysis of high-resolution satellite imagery covering the Uzbek desert. "
     "Using thermal imaging, they identified the buried outlines of buildings "
     "invisible to the naked eye at ground level. "
     "The most significant find so far has been a large caravanserai near the town of Nurata, "
     "which has been dated to the eleventh century. "
     "Excavation confirmed a central courtyard surrounded by forty individual chambers. "
     "The team also recovered a small collection of coins minted in Baghdad, "
     "providing direct evidence of long-distance trade contact. "
     "Future work will focus on the Kyrgyz section of the route, "
     "where preliminary surveys suggest at least twelve more sites remain to be mapped."),
]

# Two-speaker dialogues (concatenated with a short pause)
DIALOGUES = [
    ("l-01-museum-booking.mp3", [
        ("en-GB-SoniaNeural", "Good morning, I'd like to book a private guided tour of the Egyptian galleries."),
        ("en-GB-RyanNeural", "Certainly. Could I take your name, please?"),
        ("en-GB-SoniaNeural", "Yes, it's Varvara Sules, spelt S-U-L-E-S."),
        ("en-GB-RyanNeural", "Thank you. And which date were you thinking of?"),
        ("en-GB-SoniaNeural", "The twenty-second of October, if possible, in the afternoon."),
        ("en-GB-RyanNeural", "The twenty-second, afternoon. Our afternoon slot on that day starts at half past two."),
        ("en-GB-SoniaNeural", "Half past two works perfectly. And I'd like the group to be six people in total."),
        ("en-GB-RyanNeural", "Six people, noted. And are you all adults?"),
        ("en-GB-SoniaNeural", "Five adults and one student, actually."),
        ("en-GB-RyanNeural", "Right. For a group of that size we recommend the extended tour, which lasts ninety minutes and costs twelve pounds per adult, and six pounds for the student. That comes to sixty-six pounds in total."),
        ("en-GB-SoniaNeural", "Perfect. Can I pay by card now over the phone?"),
        ("en-GB-RyanNeural", "Of course. And could you tell me who your guide should be? We have Dr Farouk who specialises in the New Kingdom period."),
        ("en-GB-SoniaNeural", "Dr Farouk sounds ideal."),
        ("en-GB-RyanNeural", "Booked. Your reference number is E as in echo, three, seven, nine, two. Please quote that at reception."),
    ]),
    ("l-04-tutorial-medici.mp3", [
        ("en-GB-RyanNeural", "So, Varvara, you'd like to discuss your dissertation proposal on the patronage system in Quattrocento Florence."),
        ("en-GB-SoniaNeural", "Yes. I was originally planning to focus on Cosimo the Elder, but I'm now leaning towards Lorenzo the Magnificent instead."),
        ("en-GB-RyanNeural", "I'd actually strongly recommend you narrow it further. Rather than the whole of Lorenzo's patronage, why not concentrate specifically on his commissions to Verrocchio's workshop?"),
        ("en-GB-SoniaNeural", "That's more manageable, yes. Should I use a comparative framework, contrasting it with earlier Medici commissions?"),
        ("en-GB-RyanNeural", "Comparative work is tempting, but at Master's level I'd suggest a single-case deep study is stronger. Save the comparison for a chapter in the discussion."),
        ("en-GB-SoniaNeural", "Understood. And on methodology, I was thinking of iconographic analysis as the main approach."),
        ("en-GB-RyanNeural", "For this topic, archival evidence should really be your primary method. Iconographic analysis works well as a supporting tool, but the argument needs documents."),
        ("en-GB-SoniaNeural", "So the account books at the State Archive in Florence?"),
        ("en-GB-RyanNeural", "Exactly. Those, and Verrocchio's own catasto tax returns. Both are digitised now, which saves you a trip."),
        ("en-GB-SoniaNeural", "That's a relief. What about secondary sources? Should I start with Rubinstein?"),
        ("en-GB-RyanNeural", "Kent, actually. Dale Kent's monograph on the Medici is the current standard reference. Rubinstein is useful but a bit dated."),
        ("en-GB-SoniaNeural", "Kent, noted. And in terms of length, are you expecting the standard fifteen thousand words?"),
        ("en-GB-RyanNeural", "For the proposal itself, three thousand words is the maximum. The full dissertation is fifteen thousand, submitted in June."),
    ]),
]


async def gen_mono(fname, voice, text):
    out = HERE / fname
    comm = edge_tts.Communicate(text, voice=voice, rate="-6%")
    await comm.save(str(out))
    print(f"  wrote {fname}")


async def gen_dialogue(fname, turns):
    """Save each turn as tmp mp3, glue via ffmpeg concat with 0.35s silence."""
    import subprocess
    tmp_files = []
    silence = HERE / "__silence.mp3"
    if not silence.exists():
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
            "-t", "0.35", "-q:a", "9", "-acodec", "libmp3lame", str(silence)
        ], check=True, capture_output=True)
    for i, (voice, text) in enumerate(turns):
        tmp = HERE / f"__tmp_{i:02d}.mp3"
        comm = edge_tts.Communicate(text, voice=voice, rate="-6%")
        await comm.save(str(tmp))
        tmp_files.append(tmp)
    # write ffmpeg concat list
    listf = HERE / "__concat.txt"
    with listf.open("w", encoding="utf-8") as f:
        for i, tmp in enumerate(tmp_files):
            f.write(f"file '{tmp.name}'\n")
            if i < len(tmp_files) - 1:
                f.write(f"file '{silence.name}'\n")
    out = HERE / fname
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listf),
        "-c", "copy", str(out)
    ], check=True, capture_output=True, cwd=str(HERE))
    listf.unlink()
    for tmp in tmp_files:
        tmp.unlink()
    print(f"  wrote {fname} ({len(turns)} turns)")


async def main():
    print("varvara-04-listening-pack · edge-tts")
    import os
    only = set(os.environ.get("ONLY", "").split(",")) if os.environ.get("ONLY") else None
    for fname, voice, text in MONO_TRACKS:
        if only and fname not in only:
            continue
        await gen_mono(fname, voice, text)
    for fname, turns in DIALOGUES:
        if only and fname not in only:
            continue
        await gen_dialogue(fname, turns)
    # cleanup silence
    sil = HERE / "__silence.mp3"
    if sil.exists():
        sil.unlink()
    print("done.")


if __name__ == "__main__":
    asyncio.run(main())
