"""Generate 5 audio clips for Andrew logistics L1 via edge-tts.
Run: python _make_audio.py
Requires: pip install edge-tts
"""
import asyncio, os, time
from pathlib import Path
import edge_tts

OUT = Path(__file__).parent / "audio"
OUT.mkdir(exist_ok=True)

# voices
M1 = "en-GB-RyanNeural"      # male UK — Mikael / Manager
M2 = "en-US-GuyNeural"       # male US — Driver / Broker
F1 = "en-GB-SoniaNeural"     # female UK — Lena / Customer
F2 = "en-US-JennyNeural"     # female US — Warehouse manager Ingrid
ANC = "en-GB-RyanNeural"     # news anchor

CLIPS = [
    # audio-01g-01 · warehouse manager -> driver
    ("audio-01g-01.mp3", [
        (F2, "Morning, Peter. We've got eight pallets of coffee going to Novosibirsk today."),
        (M2, "Alright. Which bay?"),
        (F2, "Bay four. They've already been pulled and labelled. You'll need to secure them with straps — they're a bit top-heavy."),
        (M2, "No problem. When do you need me on the road?"),
        (F2, "By ten at the latest. You should hit the border tomorrow morning."),
    ]),
    # audio-01g-02 · forwarder -> customer
    ("audio-01g-02.mp3", [
        (M1, "Hello, Lena. I'm calling to confirm your booking for the Nordic Coffee shipment."),
        (F1, "Great, thanks. What are the details?"),
        (M1, "Container MSKU seven seven two one one eight four, forty-foot high-cube. Dispatched from Hamburg Monday evening, ETA Novosibirsk twenty-eighth."),
        (F1, "And the paperwork?"),
        (M1, "The Bill of Lading will be issued once the vessel sails. I'll forward it along with the invoice and packing list by Wednesday."),
        (F1, "Perfect. Any customs concerns I should know about?"),
        (M1, "None at this stage. Our broker will handle clearance when the container lands."),
    ]),
    # audio-01g-03 · customer -> carrier
    ("audio-01g-03.mp3", [
        (F1, "Hi, I'm calling about shipment reference N C dash four four two one. It should have arrived three days ago and I've had no update."),
        (M1, "Let me pull up the file. One moment please. Right, I can see the container has been held up at customs since Monday."),
        (F1, "What's the issue?"),
        (M1, "They've requested additional paperwork — specifically the certificate of origin. Our broker is sorting it out now."),
        (F1, "Why wasn't I notified?"),
        (M1, "You should have received an automatic alert. I'll look into why it didn't reach you. I apologise for the inconvenience."),
        (F1, "When can I expect the shipment now?"),
        (M1, "If the paperwork clears today, the container should be released by Thursday morning and delivered Friday."),
    ]),
    # audio-04-voicemail · Ingrid voicemail
    ("audio-04-voicemail.mp3", [
        (F2, "Hi Mikael, it's Ingrid from the warehouse. I'm calling about the Nordic Coffee shipment to Novosibirsk. We've loaded all eight pallets into the container — MSKU seven seven two one one eight four — this morning. Everything went smoothly. The container was sealed with seal number four four eight seven two one and handed over to the trucker at nine o'clock. He's taking it straight to the port, so it should be at the Hamburg terminal by around two this afternoon. One small thing — the driver mentioned that the port is reporting some congestion today, so there might be a short wait before the gate-in is processed. Nothing to worry about; it just means the container may not actually reach the stack until early evening. I'll send the signed loading note over by email in the next hour. Let me know if you need anything else. Bye."),
    ]),
    # audio-08-customs · broker call to Mikael
    ("audio-08-customs.mp3", [
        (M1, "Mikael Jensen speaking."),
        (M2, "Hello Mikael, this is Dmitry from the Novosibirsk broker office. I'm calling about container MSKU seven seven two one one eight four."),
        (M1, "Yes, is there a problem?"),
        (M2, "Unfortunately, yes. Customs have placed a hold on the shipment. The certificate of origin you provided is a standard EUR dot one, but for this import we need the Eurasian Economic Union form instead."),
        (M1, "I see. How long will this take to sort out?"),
        (M2, "Two options. Either you re-issue the certificate — that's three to five working days — or we pay the full duty now and claim a refund later. Your client has asked us to go with option one."),
        (M1, "Understood. What about demurrage?"),
        (M2, "The container is racking up charges at around one hundred euros per day. The sooner we clear this, the better."),
        (M1, "Right. I'll contact our documentation team immediately and push to have the corrected certificate with you by Thursday morning."),
        (M2, "Perfect. Please send it directly to my inbox and I'll present it to customs the same day."),
    ]),
    # audio-11-news · industry news radio
    ("audio-11-news.mp3", [
        (ANC, "Good morning. In today's logistics briefing: port congestion continues to disrupt European supply chains. The port of Hamburg reported dwell times of over seven days last week — well above the three-day average seen earlier this year. Industry analysts link the slowdown to a combination of reduced labour availability, continued vessel bunching from Asia, and knock-on effects from the extended Cape of Good Hope routing, which remains the primary alternative to the Suez Canal."),
        (ANC, "Spot freight rates on the Asia-to-Europe lane edged up another four per cent last week, according to the Freightos Baltic Index. Carriers announced a general rate increase to take effect from the first of December. Shippers are advised to confirm bookings before the end of November to lock in current contract rates."),
        (ANC, "In warehousing news, demand for cold-chain capacity in northern Europe has risen sharply ahead of the holiday season, pushing utilisation above ninety per cent across all major hubs. Operators are reporting waiting lists for new storage contracts."),
    ]),
]

async def gen_line(voice, text, path):
    com = edge_tts.Communicate(text, voice, rate="-5%")
    await com.save(str(path))

async def main():
    tmp = OUT / "_tmp"
    tmp.mkdir(exist_ok=True)
    for filename, lines in CLIPS:
        print(f"-> {filename} ({len(lines)} line(s))")
        parts = []
        for i,(voice,text) in enumerate(lines):
            p = tmp / f"{filename[:-4]}_{i:02}.mp3"
            retries = 0
            while retries < 3:
                try:
                    await gen_line(voice, text, p)
                    break
                except Exception as e:
                    retries += 1
                    print(f"  ! retry {retries}: {e}")
                    time.sleep(3)
            parts.append(str(p))
        # concat via ffmpeg
        list_file = tmp / f"{filename}.list"
        list_file.write_text("\n".join(f"file '{p.replace(chr(92),'/')}' " for p in parts), encoding="utf-8")
        out = OUT / filename
        import subprocess
        subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(list_file),"-c","copy",str(out)],
                       check=True, capture_output=True)
        print(f"  OK {out.name}  ({out.stat().st_size//1024} KB)")
    # cleanup tmp
    for f in tmp.iterdir(): f.unlink()
    tmp.rmdir()

if __name__ == "__main__":
    asyncio.run(main())
