"""Generate 3 audio clips for Legal English teaching lesson.
audio-04-voicemail.mp3 - Jenny ~45 sec
audio-08-courtroom.mp3 - 11 turns Christopher/Jenny/Aria concat ~60 sec
audio-11-news.mp3 - Christopher news register ~75 sec
"""
import asyncio, os, subprocess, time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audio")
TMP = os.path.join(OUT, "_tmp")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

JENNY = "en-US-JennyNeural"
ARIA = "en-US-AriaNeural"
CHRIS = "en-US-ChristopherNeural"

VOICEMAIL = ("Hi Marta, this is Linh Pires calling you back from Hoang and Pires. "
             "Thanks for the voicemail. I'd like to schedule an initial consultation with you — "
             "thirty minutes, no charge, just to understand what's going on with Golden Crust. "
             "If we take the matter on, we'd ask for a modest retainer up front, and I'll walk you through our rates then. "
             "From what you described, I think you probably have standing and more than one cause of action — "
             "trade-dress infringement plus unfair competition. One important check first: "
             "the statute of limitations in our state is four years from first discovery, so we're well inside the window. "
             "Call me back when you can, any time before six. Thanks, Marta.")

COURTROOM = [
    (JENNY, "Ms Nowak, before the Artisan Harvest Twist appeared, were you the only bakery in the county using that four-turn pattern?"),
    (ARIA,  "Objection, Your Honour, calls for speculation."),
    (CHRIS, "Sustained. Rephrase, counsel."),
    (JENNY, "Of course, Your Honour. Ms Nowak, in your personal experience, had you ever seen that pattern on another bakery's shelf before Golden Crust?"),
    (JENNY, "No. Not in eight years."),
    (ARIA,  "Objection, lack of foundation."),
    (CHRIS, "Overruled. The witness is answering from her own experience."),
    (ARIA,  "Your Honour, may we approach the bench?"),
    (CHRIS, "Approach."),
    (ARIA,  "Your Honour, counsel is also leading. The last question presumed the answer."),
    (CHRIS, "Noted. Strike that last question from the record. Members of the jury, please disregard it. Counsel, please rephrase."),
]

NEWS = ("Good evening. A federal judge in Oakland tonight preliminarily approved a forty-five million dollar "
        "settlement fund in the long-running Pacific Mobile Billing class action. "
        "The lead plaintiff, an Oakland retiree named Eleanor Vasquez, filed suit three years ago, "
        "alleging that Pacific Mobile added undisclosed regulatory recovery fees to roughly eight million customer invoices. "
        "The settlement, if finalised, will refund an average of twenty-two dollars to each class member. "
        "The opt-out deadline for anyone who wants to preserve the right to sue separately is February fifteenth. "
        "In an unusual provision, Judge Patel also approved a cy pres distribution of any unclaimed funds "
        "to three digital-literacy non-profits in the Bay Area. A fairness hearing is set for April. "
        "Pacific Mobile denies all wrongdoing. In other news tonight —")


async def tts(text, voice, out_path, rate="+0%"):
    for attempt in range(3):
        try:
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                return
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(out_path)
            if os.path.getsize(out_path) > 0:
                return
        except Exception as e:
            print(f"  [{attempt+1}] {os.path.basename(out_path)} fail: {e}")
            if os.path.exists(out_path) and os.path.getsize(out_path) == 0:
                os.remove(out_path)
            time.sleep(5)
    raise RuntimeError(f"Failed: {out_path}")


def ffconcat(parts, out_mp3, silence_sec=0.35):
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
    print("audio-04-voicemail.mp3")
    out = os.path.join(OUT, "audio-04-voicemail.mp3")
    await tts(VOICEMAIL, JENNY, out)
    print(f"  {os.path.getsize(out)} bytes")

    print("audio-08-courtroom.mp3 (11 turns)")
    parts = []
    for i, (voice, line) in enumerate(COURTROOM, 1):
        p = os.path.join(TMP, f"court-t{i:02d}.mp3")
        await tts(line, voice, p)
        parts.append(p)
    out = os.path.join(OUT, "audio-08-courtroom.mp3")
    ffconcat(parts, out, silence_sec=0.4)
    print(f"  {os.path.getsize(out)} bytes")

    print("audio-11-news.mp3")
    out = os.path.join(OUT, "audio-11-news.mp3")
    await tts(NEWS, CHRIS, out, rate="-3%")
    print(f"  {os.path.getsize(out)} bytes")

    print("DONE")

if __name__ == "__main__":
    asyncio.run(main())
