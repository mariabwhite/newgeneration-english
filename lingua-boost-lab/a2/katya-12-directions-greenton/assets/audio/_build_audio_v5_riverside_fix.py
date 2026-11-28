"""
v5 · regenerate ONLY ielts-riverside-park.mp3 to match Maria's actual map layout.

Map layout (image i (24).webp):
  - Main entrance at the BOTTOM.
  - Bottom row (near entrance): E (left, small rectangle), F (centre, circle), G (right, rectangle).
  - Middle row south of river: C (oval, left), D (rectangle, right).
  - River across the middle with a footbridge in the centre.
  - Top row across river: A (top-left), B (top-right).

Answer key (entirely original, matches the drawn map):
  A = Boat jetty          B = Birdwatching hide
  C = Children's playground   D = Picnic area
  E = Cafe               F = Information centre   G = Bike hire
"""
import asyncio, pathlib
import edge_tts

ROOT = pathlib.Path(__file__).parent
VOICE = "en-GB-RyanNeural"
RATE = "-4%"

SCRIPT = (
    "Good morning, everyone, and welcome to our brand-new Riverside Park. "
    "I'd like to spend a few minutes pointing out the main facilities, so please look at the map in your brochure. "
    "You'll see we're standing right at the main entrance, at the bottom of the map. "
    "Just inside the entrance, there are three facilities. "
    "On your left, that small building is our cafe — letter E. It serves hot drinks and light snacks all day. "
    "Right in the centre, straight ahead of you, that round building is the information centre, F. "
    "If you have any questions during your visit, do pop in. "
    "And on your right by the entrance, you'll find bike hire — that's G. "
    "You can rent a bike for two pounds an hour. "
    "Now, walking straight up the main path past the entrance, you come to two bigger areas. "
    "On your left, that oval area is the children's playground, letter C — lots of swings and slides. "
    "Directly opposite, on your right, is the picnic area, D — a lovely grassy spot with wooden tables. "
    "Now, to reach the last two facilities, you'll need to cross the river by the footbridge in the centre. "
    "Once you're over the bridge, on your LEFT you'll find the boat jetty — that's letter A. "
    "You can hire a rowing boat there. "
    "And finally, in the top-right corner, right by the river, is the birdwatching hide — that's B. "
    "It's a short walk along the river bank, well worth it. "
    "Right, that's the quick tour. Any questions before we start?"
)

OUT = ROOT / "ielts-riverside-park.mp3"

async def main():
    # delete old so we can rebuild
    if OUT.exists():
        OUT.unlink()
    for a in range(3):
        try:
            c = edge_tts.Communicate(SCRIPT, VOICE, rate=RATE)
            await c.save(str(OUT))
            s = OUT.stat().st_size
            if s < 50_000:
                raise RuntimeError(f"too small {s}")
            print(f"[ok] {OUT.name} ({s} B, {VOICE})")
            return
        except Exception as e:
            print(f"[retry {a+1}] {e}")
            if OUT.exists():
                OUT.unlink()
            await asyncio.sleep(5)
    print("[FAIL]")

if __name__ == "__main__":
    asyncio.run(main())
