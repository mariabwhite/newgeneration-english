"""Generate MP3 for 3 city stories · Anna / Sergey / Maya.
Different British voices per character.
Run:  python _gen_stories.py
"""
import asyncio, sys
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).parent

STORIES = [
    ("story-anna.mp3", "en-GB-SoniaNeural",
     "I honestly haven't been inside a supermarket for six months. "
     "On Sunday evening I open the delivery app, tap re-order last week, "
     "and everything comes to my door in an hour. "
     "I buy almost the same list every time: brown bread, milk, three yoghurts, a jar of honey, "
     "a packet of cheese, six apples, one salmon fillet. Boring? Maybe. "
     "But my Saturday morning stays mine — no queue, no heavy bags, no rain. "
     "Yes, I pay a small delivery fee. Yes, sometimes they send tomatoes that look a bit sad. "
     "But if I add up the time I save, it is the best deal of my week."),

    ("story-sergey.mp3", "en-GB-RyanNeural",
     "I never buy food online. I'm 45, I know my food, and I need to touch it. "
     "The tomato in the photo is always the best one — the one in the box is always the saddest. "
     "Every Sunday at eight in the morning I walk to the farmers' market near my flat. "
     "The lady on stall seven remembers me — she saves me the best peaches. "
     "I choose every apple, smell every loaf of bread, ask about the cheese. "
     "It takes an hour and a half. My bag is heavy on the way home. "
     "But I know exactly what I'm eating for the whole week — and that, for me, is worth the time."),

    ("story-maya.mp3", "en-GB-LibbyNeural",
     "I never go to the shop without a list. "
     "Every Sunday morning I plan seven dinners for the whole week, "
     "then I write exactly what I need — nothing more, nothing less. "
     "One trip, one basket, one receipt. Total: about three thousand five hundred roubles a week. "
     "My friends think I'm boring, but my food budget is half of theirs, and I still eat well. "
     "My favourite trick: end-of-day discounts. Bread, yoghurt, fish — after eight in the evening "
     "the shop drops the price by fifty percent. You just need patience — and a good list."),
]

async def gen():
    for fname, voice, text in STORIES:
        target = OUT / fname
        if target.exists():
            print(f"skip  {fname}")
            continue
        tts = edge_tts.Communicate(text, voice, rate="-4%")
        await tts.save(str(target))
        print(f"done  {fname}  ({voice})")

if __name__ == "__main__":
    asyncio.run(gen())
