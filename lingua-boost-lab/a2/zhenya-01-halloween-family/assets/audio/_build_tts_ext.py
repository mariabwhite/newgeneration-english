"""Extra TTS for Section 2 · Part B (extended family vocab + tree reading)."""
import asyncio, pathlib
import edge_tts

OUT = pathlib.Path(__file__).parent
VOICE = "en-US-AriaNeural"
RATE = "-10%"

CLIPS = [
    ("ext-01", "Dracula and Morticia are Wendy's parents."),
    ("ext-02", "Vlad and Elvira are Wendy's grandparents. They live in Romania."),
    ("ext-03", "Dracula is Morticia's husband. They got married five hundred years ago."),
    ("ext-04", "Morticia is Dracula's wife. She wears black at every party."),
    ("ext-05", "Freddy is Dracula's son. He is ten years old."),
    ("ext-06", "Wendy is Morticia's daughter. She is thirteen."),
    ("ext-07", "Rick and Ricky are twin skeleton cousins. They look exactly the same."),
    ("ext-08", "Peony is a baby ghost. She is the new sister in the family."),
    ("ext-09", "Dracula and Morticia have got three children now."),
    ("ext-10", "Here is the Boo family tree. Four generations of monsters."),
    ("ext-tree-full",
     "The Boo family is big. Dracula and Morticia are husband and wife. "
     "They are Wendy's parents. "
     "Dracula's mum and dad live in Romania. "
     "They are Vlad and Elvira — Wendy's grandparents. "
     "Morticia has got a sister called Luna. Luna is Wendy's aunt. "
     "Luna is married to Uncle Wolfy. "
     "Together they have got twin boys — Rick and Ricky. They are Wendy's cousins. "
     "Last Halloween the family had a new baby — a little ghost called Peony. "
     "Now Dracula and Morticia have got three children: Wendy, Freddy and baby Peony. "
     "One big spooky family tree!"),
]

async def gen_one(name, text):
    out = OUT / f"{name}.mp3"
    if out.exists() and out.stat().st_size > 1000:
        return f"skip {name}"
    try:
        comm = edge_tts.Communicate(text, VOICE, rate=RATE)
        await comm.save(str(out))
        if out.exists() and out.stat().st_size > 1000:
            return f"OK   {name}  {out.stat().st_size} B"
        return f"EMPTY {name}"
    except Exception as e:
        return f"ERR  {name}  {e}"

async def main():
    for i in range(0, len(CLIPS), 4):
        chunk = CLIPS[i:i+4]
        tasks = [gen_one(n, t) for (n, t) in chunk]
        rs = await asyncio.gather(*tasks)
        for r in rs: print(r)
        await asyncio.sleep(0.4)
    retry = [c for c in CLIPS if not (OUT / f"{c[0]}.mp3").exists() or (OUT / f"{c[0]}.mp3").stat().st_size < 1000]
    if retry:
        print(f"\n--- RETRY {len(retry)} ---")
        await asyncio.sleep(5)
        for n, t in retry:
            print(await gen_one(n, t))

if __name__ == "__main__":
    asyncio.run(main())
