"""
v3 · 4 additional IELTS Section-2 style map-labelling clips
(Task 1 — Riverside Park — is already in the audio folder from v1.)

Standard IELTS Listening Section 2 FORMAT:
  - A single speaker (tour guide / community leader) addresses a group.
  - Pace: slower-than-natural B2/B1 British English, clear intonation.
  - Signpost phrases: "as you come in…", "straight ahead of you…",
    "just past…", "opposite…", "in the far corner…", "next to…".

All five scenarios and scripts here are ORIGINAL (names, layouts, content).
They follow the publicly-documented IELTS task format only.
"""
import asyncio, pathlib
import edge_tts

ROOT = pathlib.Path(__file__).parent
IELTS_DIR = ROOT / "ielts_tasks"
IELTS_DIR.mkdir(exist_ok=True)

VOICE_F = "en-GB-SoniaNeural"
VOICE_M = "en-GB-RyanNeural"
RATE = "-4%"

# ---------- TASK 2 · Westhaven Community Garden ----------
# A=tool shed, B=herb garden, C=polytunnel, D=compost area,
# E=children's garden, F=pond, G=apple orchard
T2 = (
    "Welcome, everyone, to Westhaven Community Garden. "
    "Please gather round the big map by the gate — I'll quickly show you where everything is so you don't get lost. "
    "Right beside me, on the right as you come in, is the tool shed. That's letter A. "
    "Please return all tools there at the end of your visit. "
    "If you look straight ahead of you, down the main path, you'll see the herb garden — that's B — with rosemary, mint and basil growing in neat rows. "
    "Over on the far left of the garden, next to the brick wall, we have our polytunnel, where the tomatoes grow. That's C. "
    "Now, if you follow the path right to the back corner on the right, you'll find the compost area, which is D. It's a little bit tucked away. "
    "Halfway back on the right, next to the big wooden picnic bench, is the children's garden — that's letter E, full of sunflowers. "
    "If you keep walking all the way to the top of the garden, by the willow trees, there's our little pond, F. "
    "And finally, beyond the pond, on the right, is the apple orchard. That's G. "
    "We'll finish the tour there in about an hour. Enjoy!"
)

# ---------- TASK 3 · Summerfield Farmers' Market ----------
# A=info tent (entrance), B=bread stall (first row left), C=cheese counter (first row right),
# D=vegetable stalls (centre), E=flower corner (far left past bread), F=coffee van (centre back),
# G=children's workshop (far right)
T3 = (
    "Good morning and welcome to the Summerfield Farmers' Market. "
    "Before you go exploring, let me point out the main stalls on your map. "
    "The information tent is right here at the entrance, where we're standing. That's letter A. "
    "As you walk straight in, the first row of stalls has two main points. "
    "On your left, you'll spot the bread and pastry stall — that's B. "
    "Directly opposite, on your right, is the cheese counter. That's C. "
    "Keep walking down the central path and you'll come to the vegetable stalls, D. "
    "They stretch across the middle of the market. "
    "If you'd like flowers, head to the far left corner, past the bread stall. That's our flower corner, letter E. "
    "In the centre at the very back of the market, you'll find the coffee van, F, with its bright red umbrella — hard to miss. "
    "And finally, over on the far right, right beside the small children's playground, is our children's workshop tent, G. "
    "That's where kids can make jam and decorate pots this morning. Enjoy!"
)

# ---------- TASK 4 · Oak Hill University Library ----------
# A=reception, B=self-checkout machines, C=silent study room (upstairs left),
# D=group study room (upstairs right), E=computer lab (ground floor back),
# F=coffee bar (courtyard), G=garden reading area (courtyard far corner)
T4 = (
    "Welcome, everyone, to Oak Hill University Library. Let me give you a quick overview. "
    "You've just come through the main doors, and straight in front of you is the reception desk. That's A. "
    "You can ask any question there. "
    "Just past reception, still on the ground floor, you'll see our self-checkout machines. That's letter B. "
    "Now, if you take the stairs up to the first floor, the room immediately on your left is the silent study room, C. "
    "Please — absolutely no talking in there. "
    "Opposite the silent room, on your right, is the group study room, D, where you can work in teams. "
    "Back down on the ground floor, right at the back, behind the main bookshelves, is our computer lab — that's letter E. "
    "Now let's step outside through the side door. We have a lovely little courtyard. "
    "Straight ahead of you there's our coffee bar, F. "
    "And past the coffee bar, in the far corner under the big oak tree, is the garden reading area — letter G. "
    "A beautiful spot to read on a sunny day. Any questions before we start the proper tour?"
)

# ---------- TASK 5 · Blackwater Zoo education trail ----------
# A=ticket office (entrance), B=penguin pool (first left), C=monkey island (straight ahead past penguins),
# D=reptile house (small building right of monkeys), E=butterfly garden (far right in trees),
# F=elephant enclosure (far left past penguins), G=education centre (centre back)
T5 = (
    "Hello and welcome to Blackwater Zoo. Before our tour begins, let me run through the map with you. "
    "As you came in, you passed the ticket office on your left — that's letter A. "
    "Now, following the main path, the first animal area on your left is the penguin pool, B. "
    "You can watch the penguins being fed at eleven o'clock. "
    "If you continue straight ahead, past the penguins, you'll come to Monkey Island, which is C. "
    "It's a small island in the middle of a little lake. "
    "Just to the right of Monkey Island is a small white building. That's the reptile house, letter D. "
    "Now, over on the far right of the zoo, hidden among the trees, we have our butterfly garden — that's E. Do take your time there. "
    "On the far left of the zoo, past the penguin pool, is the elephant enclosure. That's letter F. "
    "The elephants are usually outside on warm days. "
    "And finally, right in the middle at the back of the zoo, is the education centre, G. "
    "That's where the children's workshops take place this afternoon. Enjoy your visit!"
)

TASKS = {
    "task2-westhaven-garden":   (T2, VOICE_F),
    "task3-summerfield-market": (T3, VOICE_M),
    "task4-oakhill-library":    (T4, VOICE_F),
    "task5-blackwater-zoo":     (T5, VOICE_M),
}

async def tts(text, out, voice):
    if out.exists() and out.stat().st_size > 10_000:
        print(f"  [skip] {out.name} ({out.stat().st_size} B)")
        return
    for a in range(3):
        try:
            c = edge_tts.Communicate(text, voice, rate=RATE)
            await c.save(str(out))
            s = out.stat().st_size if out.exists() else 0
            if s < 5000:
                raise RuntimeError(f"too small {s}")
            print(f"  [ok]   {out.name} ({s} B, {voice})")
            return
        except Exception as e:
            print(f"  [retry {a+1}] {out.name}: {e}")
            if out.exists():
                out.unlink()
            await asyncio.sleep(5)
    print(f"  [FAIL] {out.name}")

async def main():
    print(f"=== 4 new IELTS Section-2 tasks -> {IELTS_DIR} ===")
    for slug, (text, voice) in TASKS.items():
        await tts(text, IELTS_DIR / f"{slug}.mp3", voice)
    print("\nDone.")

if __name__ == "__main__":
    asyncio.run(main())
