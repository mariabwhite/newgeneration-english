"""Generate MP3 audio for Anya L4 · Lighthouse at Midnight.
Uses same slug algorithm as the inline JS so files are found automatically.
Run: py _gen_audio.py
"""
import sys, asyncio, pathlib, re
sys.stdout.reconfigure(encoding='utf-8')
import edge_tts

VOICE_SASHA = "en-GB-SoniaNeural"   # Anya / narrator (female British)
VOICE_GRANDMA = "en-GB-LibbyNeural"  # grandma voice (slightly different female)
VOICE_CAT = "en-US-JennyNeural"      # ghost cat (lighter female)
VOICE_CRYSTAL = "en-GB-RyanNeural"   # crystal ball (male British, mysterious)

def slug(src: str) -> str:
    s = src.lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s[:30]

# Main audio clips: each matches a data-say attribute in HTML
CLIPS = [
    (
        "Anya lives in a small village by the sea. Every autumn, when the wind gets cold, people tell the same story: the old lighthouse on the cliff is empty — but at midnight, a warm light appears in every window. Tonight is 31 October. Anya is standing at the bottom of the lighthouse. The wind is blowing, waves are hitting the rocks, and green seaweed is dancing around her boots. A friendly ghost cat is sitting on the step, licking its paw. Last year, Anya said to the cat, my grandmother climbed this lighthouse. She saw a wonderful light at the top. She came home with a secret book, and never opened it. While Anya was speaking, the cat was listening. The moon was rising. Suddenly a bell was ringing somewhere inside, not loud, but clear. I will climb, Anya whispered. I will reach the top. I will not be scared. Tomorrow I will tell grandma what I saw. The cat meowed. I am going to help you, it seemed to say. We are going to climb all six floors together. And on the top, we are going to find the real secret of the lighthouse. Anya takes a deep breath. The door opens with a soft creak. The quest begins.",
        VOICE_SASHA,
    ),
    (
        "On Halloween night, Anya walked to the old lighthouse on the cliff. The wind was blowing and green seaweed was dancing on the rocks. A friendly ghost cat was sitting on the step. Anya opened the door and started to climb. On every floor she met a different time. On the first floor the Present Simple ghost taught her facts. On the second floor the Present Continuous spirit showed her the storm outside. On the third floor she saw old photographs of her grandmother. On the fourth floor she heard a bell that was ringing when grandma was young. On the fifth floor a crystal ball showed her the future. On the sixth floor she wrote a plan: tomorrow she will visit grandma and tell her everything. At the top, Anya found grandma's old book — and finally opened it.",
        VOICE_SASHA,
    ),
    (
        "When I was young, I climbed the lighthouse for the first time. The night was dark and the wind was blowing hard. On every floor I met a strange thing. On the top I found a book — the same book you have now, Anya. Please take care of it.",
        VOICE_GRANDMA,
    ),
    (
        "Meow. I am the lighthouse cat. I live here every night. Right now I am sitting on the step, waiting for a brave visitor. Every autumn I meet one — but most of them run away. You are different, Anya. You are smiling, not screaming. Follow me.",
        VOICE_CAT,
    ),
    (
        "I see your future, child. Tomorrow you will tell grandma what you saw. Next week you are going to visit her again. In one month you will finish reading the whole book. In one year you will come back to this lighthouse — not as a visitor, but as the keeper.",
        VOICE_CRYSTAL,
    ),
]

async def gen_one(text: str, voice: str, out_dir: pathlib.Path):
    sl = slug(text)
    dest = out_dir / f"{sl}.mp3"
    if dest.exists() and dest.stat().st_size > 500:
        print(f"  skip  {sl[:50]}  (exists)")
        return
    tts = edge_tts.Communicate(text=text, voice=voice, rate="-6%")
    await tts.save(str(dest))
    print(f"  ok    {sl[:50]:50}  {voice}")

async def main():
    out = pathlib.Path(__file__).parent / "assets" / "audio"
    out.mkdir(parents=True, exist_ok=True)
    print(f"→ {out}")
    print(f"→ {len(CLIPS)} clips")
    for text, voice in CLIPS:
        try:
            await gen_one(text, voice, out)
        except Exception as e:
            print(f"  ERR  {slug(text)[:50]}  {e}")
    print("done.")

if __name__ == "__main__":
    asyncio.run(main())
