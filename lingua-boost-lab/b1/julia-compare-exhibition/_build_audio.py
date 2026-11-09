#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Julia compare-exhibition · audio build (Julia canon: American family, en-US).
Voices:
  Julia narrator → en-US-AriaNeural (rate=-6%)
  John           → en-US-AnaNeural   (child)
  Emma           → en-US-JennyNeural
  Mum            → en-US-SaraNeural
"""
import asyncio, os, time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audio")
os.makedirs(OUT, exist_ok=True)

V_JULIA = "en-US-AriaNeural"   # narrator & Julia
V_JOHN  = "en-US-AnaNeural"    # 6yo brother
V_EMMA  = "en-US-JennyNeural"
V_MUM   = "en-US-SaraNeural"

RATE = "-6%"

CLIPS = [
    # ---------- READING: 4 scenes ----------
    ("r1-scene-gate", V_JULIA,
     "It is Saturday. Julia, John and Emma are at the big summer Exhibition in the park. "
     "There are elephants, giraffes, peacocks and even a carousel. "
     "John runs to the first cage. Wow, Julia, look at the elephant, he says. It is much bigger than the lion. "
     "Yes, it is, answers Julia. And look up — the giraffe is the tallest animal in the whole zoo. "
     "I can't see its head, says John. That's because it's taller than two Dads together, laughs Julia."),

    ("r2-scene-peacock", V_JULIA,
     "They walk past the birds. Oh, look, Julia, says Emma, a peacock! It is more beautiful than any bird I know. "
     "But John doesn't care about birds. He pulls Emma's hand. Come on, come on, he shouts. "
     "The carousel is the most interesting thing at the whole fair!"),

    ("r3-scene-lunch", V_JULIA,
     "At twelve o'clock Mum comes with a basket. Hungry, kids, she asks. "
     "I made pancakes with honey and raspberry jam. Emma takes a bite. "
     "Mmm, Mum, your pancakes are better than the shop ones. "
     "John laughs. And they are not as expensive as the shop pancakes! Everyone smiles."),

    ("r4-scene-home", V_JULIA,
     "On the way home the sky gets darker and darker. "
     "When they open the door, Barsik is on the sofa, warm and lazy. "
     "Hi, Barsik, says Julia, did you miss us? "
     "Barsik yawns and purrs. He really thinks he is the best cat in the whole world."),

    # ---------- LISTENING dialogue (Julia + Emma planning) ----------
    ("l1-julia", V_JULIA,
     "Emma, tomorrow we're going to the summer exhibition. Are you coming?"),
    ("l2-emma", V_EMMA,
     "Of course! What's the most interesting part?"),
    ("l3-julia", V_JULIA,
     "John says the carousel. But I think the giraffes are more interesting."),
    ("l4-emma", V_EMMA,
     "And the peacocks? Mum says they are the most beautiful birds at the zoo."),
    ("l5-julia", V_JULIA,
     "Yes! They are more beautiful than any bird I know. See you at ten, Emma!"),

    # ---------- Full-passage single file (for Part B full read) ----------
    ("r0-full-passage", V_JULIA,
     "Julia's day at the exhibition. "
     "It is Saturday. Julia, John and Emma are at the big summer Exhibition in the park. "
     "There are elephants, giraffes, peacocks and even a carousel. "
     "John runs to the first cage. Wow, look at the elephant! It is much bigger than the lion. "
     "Yes, it is, answers Julia. And look up — the giraffe is the tallest animal in the whole zoo. "
     "They walk past the birds. Oh, look, says Emma, a peacock! It is more beautiful than any bird I know. "
     "But John doesn't care about birds. The carousel is the most interesting thing at the whole fair, he shouts. "
     "At twelve o'clock Mum comes with a basket of pancakes with honey and raspberry jam. "
     "Mmm, Mum, your pancakes are better than the shop ones, says Emma. "
     "On the way home the sky gets darker and darker. "
     "When they open the door, Barsik is on the sofa, warm and lazy. "
     "He yawns and purrs. He really thinks he is the best cat in the whole world."),
]

async def one(slug, voice, text, retries=3):
    path = os.path.join(OUT, f"{slug}.mp3")
    if os.path.exists(path) and os.path.getsize(path) > 500:
        print(f"  skip {slug}")
        return True
    for attempt in range(retries):
        try:
            comm = edge_tts.Communicate(text, voice, rate=RATE)
            await comm.save(path)
            size = os.path.getsize(path) if os.path.exists(path) else 0
            if size < 500:
                if os.path.exists(path):
                    os.remove(path)
                raise RuntimeError(f"tiny file {size}b")
            print(f"  ok   {slug}  ({size // 1024} KB)")
            return True
        except Exception as e:
            print(f"  err  {slug} attempt {attempt+1}: {e}")
            if os.path.exists(path) and os.path.getsize(path) < 500:
                os.remove(path)
            await asyncio.sleep(5)
    print(f"  FAIL {slug}")
    return False

async def main():
    print(f"Writing audio to: {OUT}")
    print(f"Total clips: {len(CLIPS)}")
    print()
    results = []
    for slug, voice, text in CLIPS:
        ok = await one(slug, voice, text)
        results.append((slug, ok))
    print()
    print("Summary:")
    for s, ok in results:
        print(f"  {'OK ' if ok else 'XXX'} {s}")

if __name__ == "__main__":
    asyncio.run(main())
