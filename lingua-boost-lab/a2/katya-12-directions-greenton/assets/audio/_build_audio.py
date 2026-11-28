"""
Build all audio for Katya L12 directions trainer.

- 1-30-directions.mp3    : book-echo gap-fill dialogue (track 1.30)
- ielts-riverside-park.mp3 : IELTS Section 2 tour guide monologue (~90 s)
- vocab/*.mp3            : 25 single-word/short-phrase clips for the capsule

Usage: python _build_audio.py
Requires: edge-tts (installed via `pip install edge-tts`)
"""
import asyncio, os, pathlib, sys, time
import edge_tts

ROOT = pathlib.Path(__file__).parent
VOCAB_DIR = ROOT / "vocab"
VOCAB_DIR.mkdir(exist_ok=True)

# Two British voices for variety
VOICE_F = "en-GB-SoniaNeural"   # female, clear BBC-style
VOICE_M = "en-GB-RyanNeural"    # male, neutral British
RATE = "-8%"                    # slower, A2-friendly

# --- 1.30 book-echo listening (gap-fill) ---
TRACK_130 = (
    "OK, so you want to get to the village centre. "
    "Go along this lane, straight ahead. "
    "You'll pass a small pond on your left. Just go past the pond, don't stop. "
    "A little further on, you'll see a wooden gate on your left. "
    "Go through the gate on your left and you'll come to a big open field. "
    "Go across the field — just follow the footpath, you can't miss it. "
    "On the other side of the field, there's a small country lane. "
    "Turn right onto the lane. Then go straight on for about two minutes. "
    "Take the first right, and walk to the end of the road. "
    "That's where the village centre is. It's about ten minutes in total. "
    "Would you like me to repeat that?"
)

# --- IELTS Section 2 map-labelling (Riverside Park) ---
# Answers set in the HTML: A=Café, B=Information centre, C=Children's playground,
# D=Boat jetty, E=Picnic area, F=Bike hire, G=Birdwatching hide
TRACK_IELTS = (
    "Good morning, everyone, and welcome to our brand-new Riverside Park. "
    "I'd like to spend a few minutes pointing out the main facilities, so please look at the map in your brochure. "
    "You'll see we're standing right at the main entrance, at the bottom of the map. "
    "Now, straight ahead of you, just inside the entrance on the left, is our café — that's marked with the letter A. "
    "It serves hot drinks and light snacks all day. "
    "Opposite the café, on the right of the main path, you'll find the information centre — that's B. "
    "If you have any questions during your visit, do pop in. "
    "A short walk further up the main path, you come to a crossroads. "
    "On your left, right beside the lake, is the children's playground — that's letter C. "
    "Now, from the crossroads, if you follow the path along the lake, you'll come to the boat jetty — that's D. "
    "You can hire a rowing boat there for a very reasonable price. "
    "Carrying on past the jetty, over the little wooden bridge, "
    "you'll find the picnic area — that's letter E, on your right, under the trees. "
    "It's a lovely spot for lunch. "
    "Now, back to the main path. If instead of turning towards the lake you carry straight on, past the children's playground, "
    "you'll come to the bike hire shed — that's F, next to the big oak tree. "
    "And finally, in the far corner of the park, right beside the river, we have the birdwatching hide — that's G. "
    "It's a short walk through the woodland, but well worth it. "
    "Right, that's the quick tour. Any questions before we start?"
)

# --- vocab capsule (25 short clips) ---
VOCAB = {
    "go": "Go.",
    "walk": "Walk.",
    "turn": "Turn.",
    "take": "Take.",
    "follow": "Follow.",
    "cross": "Cross.",
    "along": "Along. Go along this lane.",
    "across": "Across. Walk across the bridge.",
    "past": "Past. Go past the pond.",
    "through": "Through. Go through the gate.",
    "into": "Into. Go into the café.",
    "onto": "Onto. Turn right onto the lane.",
    "towards": "Towards. Walk towards the church.",
    "up-to": "Up to. Walk up to the gate.",
    "lane": "Lane.",
    "road": "Road.",
    "path": "Path.",
    "footpath": "Footpath. Follow the footpath.",
    "gate": "Gate.",
    "field": "Field.",
    "bridge": "Bridge.",
    "pond": "Pond.",
    "corner": "Corner.",
    "end-of-the-road": "The end of the road. Walk to the end of the road.",
    "straight-on": "Straight on. Go straight on.",
    "take-the-first-right": "Take the first right.",
    "turn-left-right": "Turn left. Turn right.",
    "on-your-left": "On your left. The gate is on your left.",
}

async def tts(text, out_path, voice=VOICE_F, rate=RATE):
    if out_path.exists() and out_path.stat().st_size > 1000:
        print(f"  [skip] {out_path.name} ({out_path.stat().st_size} B)")
        return
    for attempt in range(3):
        try:
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(str(out_path))
            size = out_path.stat().st_size if out_path.exists() else 0
            if size < 500:
                raise RuntimeError(f"too small: {size} B")
            print(f"  [ok]   {out_path.name} ({size} B, voice {voice})")
            return
        except Exception as e:
            print(f"  [retry {attempt+1}] {out_path.name}: {e}")
            if out_path.exists():
                out_path.unlink()
            await asyncio.sleep(5)
    print(f"  [FAIL] {out_path.name}")

async def main():
    print("=== Long tracks ===")
    await tts(TRACK_130, ROOT / "1-30-directions.mp3", voice=VOICE_F, rate="-10%")
    await tts(TRACK_IELTS, ROOT / "ielts-riverside-park.mp3", voice=VOICE_M, rate="-4%")

    print("\n=== Vocab capsule ===")
    for slug, phrase in VOCAB.items():
        out = VOCAB_DIR / f"{slug}.mp3"
        await tts(phrase, out, voice=VOICE_F, rate="-5%")

    print("\nDone.")

if __name__ == "__main__":
    asyncio.run(main())
