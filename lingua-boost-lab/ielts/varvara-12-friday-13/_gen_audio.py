"""
Audio generator for varvara-12-friday-13 lesson.
- passage-curse-of-thirteen.mp3  (reading, single voice, ~3:40)
- interview-harrison-triskaidekaphobia.mp3  (2-voice dialog, ~2:30, ffmpeg concat)
- idiom-XX-*.mp3  (12 clips, one short contextual sentence each)

Usage: python _gen_audio.py
Deps: edge-tts, ffmpeg in PATH
Retry on 403: Microsoft token rotation — 1-2 clips may fail, we retry individually.
"""
import asyncio
import os
import subprocess
import tempfile
import time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(HERE, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE_NARRATOR = "en-GB-SoniaNeural"
VOICE_HOST = "en-GB-RyanNeural"
VOICE_HARRISON = "en-GB-LibbyNeural"
RATE = "-5%"

# =========== PASSAGE (§1) ===========
PASSAGE = """The Curse of Thirteen. Three Origins of a Modern Fear.

The dread of the number thirteen is one of the most enduring and widely observed superstitions in Western culture. The clinical term for it, friggatriskaidekaphobia, is almost comically technical, but the behaviour it describes is not rare: a 2019 Gallup poll found that nearly one in four Americans would refuse to stay on the thirteenth floor of a hotel, and the airline industries of Britain, France and the United States still routinely omit row 13 from the cabin layouts of newly built aircraft. The puzzling question is not whether the superstition exists — it plainly does — but where, exactly, it comes from.

Folklorists usually point to three independent origin stories, each surfacing from a different corner of the medieval and pre-medieval imagination. The first, and probably the oldest in continuous circulation, is the Christian tradition surrounding the Last Supper. According to the Gospels, thirteen men gathered at the table on the evening before the Crucifixion, with Judas Iscariot, the betrayer, counted among them. Within a few centuries, the association had hardened into a domestic taboo: a dinner of thirteen was said to guarantee that one of the guests would die within the year. Mark Twain, invited to just such a dinner in 1883, is reported to have remarked drily that the crowd was so numerous that the thirteenth guest was unnecessary.

The second origin story is colder and more northern. In Norse mythology, the god Loki is sometimes described as an uninvited thirteenth guest at a banquet in Valhalla, where his arrival precipitates the death of the beloved god Balder. Scholars dispute how old this version is — some of the surviving texts are relatively late — but the shape of the story is familiar: an interloper, a thirteenth place, a catastrophe. Whatever its true date, by the nineteenth century the Norse tale was widely cited alongside the Last Supper as a parallel explanation, and the two have become entangled in popular retellings ever since.

The third origin is historical rather than mythic. On the morning of Friday, 13 October 1307, King Philip IV of France, deeply in debt to the Knights Templar and keen to seize their fortune, ordered the arrest of every Templar in the kingdom. Scores were tortured and burned at the stake; the order itself was dissolved by papal bull five years later. The date has often been cited, particularly since the twentieth century, as the moment at which Friday and the number thirteen fused into a single, especially unlucky, combination. Historians today are more cautious: there is little evidence that medieval contemporaries themselves made this connection, and the pairing of Friday plus thirteen appears to be a nineteenth-century retrospective construction. Still, as an origin myth about an origin myth, the Templar story has the right dark gravity.

What unites all three traditions — and perhaps explains the superstition's stubborn survival — is less the specific narrative than the mathematical and visual uneasiness of the number itself. Twelve is a completing number: twelve apostles, twelve months, twelve hours on a clock face. Thirteen stands just beyond that closure, a fractional step into the unknown. It is, as the French structuralist Claude Lévi-Strauss once observed of similar numerical taboos, a small irregularity in an otherwise orderly world — and that is precisely why the mind catches on it."""

# =========== INTERVIEW (§3) ===========
# list of (voice, text) tuples; ffmpeg will concat with 400ms silence between
INTERVIEW_TURNS = [
    (VOICE_HOST,     "Doctor Harrison, we've all grown up with the fear of Friday the thirteenth — but is any of it actually medieval?"),
    (VOICE_HARRISON, "Not quite. The Last Supper association, yes, that's genuinely old — probably by the ninth century it was folk knowledge that a dinner of thirteen meant a death within the year. What is NOT medieval is the specific combination of Friday and the number thirteen. That pairing really only appears in nineteenth-century sources. The Templar arrest on the thirteenth of October thirteen-oh-seven was a Friday, that part is true, but no medieval chronicle links the two as a superstition."),
    (VOICE_HOST,     "So the Templar version is almost a… retrospective construction?"),
    (VOICE_HARRISON, "Exactly. A nineteenth-century origin myth about a medieval event. Which is quite common in folklore — people dislike superstitions that feel arbitrary, so they reach back and anchor them to a date, a story, a name."),
    (VOICE_HOST,     "And the Norse story? The Loki-at-Valhalla one?"),
    (VOICE_HARRISON, "I'd be cautious there. The surviving texts are late enough that the thirteenth-guest framing could easily be a later folkloric overlay. I don't dismiss it entirely, but I wouldn't rank it as independent evidence."),
    (VOICE_HOST,     "Airlines still skip row thirteen. Are they reinforcing a fear they could simply ignore?"),
    (VOICE_HARRISON, "I'd defend the airlines, actually. They respond rationally to a small but measurable passenger preference. It's cheaper to renumber than to argue with twenty-two percent of your customers."),
    (VOICE_HOST,     "You've called friggatriskaidekaphobia 'a splinter'. Why?"),
    (VOICE_HARRISON, "Because it's a splinter of medieval mental furniture lodged in a secular modern brain. We don't believe the cosmology any more, but the pattern stayed. It's tiny. It's harmless, mostly. And it's weirdly beautiful — a small piece of the Middle Ages, still working."),
]

# =========== IDIOMS (§10 · 12 clips) ===========
IDIOMS = [
    ("01-touch-wood",        "Marta hasn't had an accident in twenty years — touch wood."),
    ("02-fingers-crossed",   "I'll be waiting for the results on Monday — fingers crossed!"),
    ("03-tempt-fate",        "Don't say the project is finished before it's live — you're tempting fate."),
    ("04-against-all-odds",  "Against all odds, the small bakery won the trade-dress case."),
    ("05-stroke-of-luck",    "It was a real stroke of luck that we found the subpoena file in the archive."),
    ("06-down-on-luck",      "He's been down on his luck ever since the business closed."),
    ("07-walk-on-eggshells", "After the argument, we were walking on eggshells around him for weeks."),
    ("08-writing-on-wall",   "When the CEO stopped answering emails, the writing was on the wall."),
    ("09-speak-of-devil",    "Speak of the devil — I was just telling Elena about you yesterday."),
    ("10-creeps",            "That abandoned theatre on Fifth Avenue really gives me the creeps."),
    ("11-blood-cold",        "When I heard his voice on the phone, my blood ran cold."),
    ("12-leap-of-faith",     "Starting your own law firm is always a bit of a leap of faith."),
]


async def tts_one(text: str, voice: str, out_path: str, rate: str = RATE, max_tries: int = 4):
    """Generate one MP3 with retries on 403 (Microsoft token rotation)."""
    for attempt in range(1, max_tries + 1):
        try:
            if os.path.exists(out_path) and os.path.getsize(out_path) > 500:
                print(f"  SKIP (exists): {os.path.basename(out_path)}")
                return
            communicate = edge_tts.Communicate(text, voice, rate=rate)
            await communicate.save(out_path)
            size = os.path.getsize(out_path)
            if size < 500:
                raise RuntimeError(f"too small ({size} B)")
            print(f"  OK: {os.path.basename(out_path)} ({size // 1024} KB)")
            return
        except Exception as e:
            print(f"  attempt {attempt} failed: {e!r}; wait 5s & retry")
            if os.path.exists(out_path):
                try:
                    os.remove(out_path)
                except OSError:
                    pass
            time.sleep(5)
    raise RuntimeError(f"edge-tts failed after {max_tries} tries: {out_path}")


async def main():
    print("== PASSAGE ==")
    passage_out = os.path.join(AUDIO_DIR, "passage-curse-of-thirteen.mp3")
    await tts_one(PASSAGE, VOICE_NARRATOR, passage_out)

    print("== INTERVIEW (dialog, will concat) ==")
    tmp_dir = tempfile.mkdtemp(prefix="interview_")
    turn_files = []
    silence = os.path.join(tmp_dir, "silence.mp3")
    # 0.4s silence
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", "0.4", "-q:a", "9", "-acodec", "libmp3lame", silence],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for i, (voice, text) in enumerate(INTERVIEW_TURNS, 1):
        clip = os.path.join(tmp_dir, f"turn-{i:02d}.mp3")
        print(f"  turn {i:02d} · {voice}")
        await tts_one(text, voice, clip)
        turn_files.append(clip)

    concat_list = os.path.join(tmp_dir, "concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for i, turn in enumerate(turn_files):
            f.write(f"file '{turn.replace(os.sep, '/')}'\n")
            if i < len(turn_files) - 1:
                f.write(f"file '{silence.replace(os.sep, '/')}'\n")

    interview_out = os.path.join(AUDIO_DIR, "interview-harrison-triskaidekaphobia.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", interview_out],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"  OK: {os.path.basename(interview_out)} ({os.path.getsize(interview_out) // 1024} KB)")

    print("== IDIOMS (12 clips) ==")
    for slug, text in IDIOMS:
        out = os.path.join(AUDIO_DIR, f"idiom-{slug}.mp3")
        await tts_one(text, VOICE_NARRATOR, out)

    print("\nALL DONE. Audio written to:", AUDIO_DIR)


if __name__ == "__main__":
    asyncio.run(main())
