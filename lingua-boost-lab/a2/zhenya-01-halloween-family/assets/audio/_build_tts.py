"""
TTS generation for Zhenya L1 · Meet the Monster Family (A1-A2 Halloween).
edge-tts · female voices Aria (narrator/Wendy/Zhenya) + Jenny (Lily).
Reruns are safe: skips existing non-empty files.
"""
import asyncio, pathlib, sys
import edge_tts

OUT = pathlib.Path(__file__).parent
VOICE_N = "en-US-AriaNeural"   # narrator / Wendy / Zhenya / vocab
VOICE_L = "en-US-JennyNeural"  # Lily (contrast)
RATE_SLOW = "-10%"             # A1-A2 pacing
RATE_NORMAL = "+0%"

CLIPS = [
    # WARM-UP · Zhenya's own hello
    ("warm-01", VOICE_N, RATE_SLOW, "Hello! My name is Zhenya."),
    ("warm-02", VOICE_N, RATE_SLOW, "I'm thirteen years old."),
    ("warm-03", VOICE_N, RATE_SLOW, "I live in Moscow."),

    # FAMILY VOCAB · example sentences
    ("fam-01", VOICE_N, RATE_SLOW, "Morticia is Wendy's mother. She is a witch."),
    ("fam-02", VOICE_N, RATE_SLOW, "Dracula is Wendy's father. He is a vampire."),
    ("fam-03", VOICE_N, RATE_SLOW, "Wendy is Freddy's sister. She is a friendly ghost."),
    ("fam-04", VOICE_N, RATE_SLOW, "Freddy is Wendy's little brother. He is a slow zombie."),
    ("fam-05", VOICE_N, RATE_SLOW, "Grandma Mummy is three thousand years old. She wears white bandages."),
    ("fam-06", VOICE_N, RATE_SLOW, "Grandpa Skeleton loves soup. He has no teeth."),
    ("fam-07", VOICE_N, RATE_SLOW, "Aunt Luna is a dark fairy. She lives in the forest."),
    ("fam-08", VOICE_N, RATE_SLOW, "Uncle Wolfy is a werewolf. He howls at the moon."),
    ("fam-09", VOICE_N, RATE_SLOW, "Cousin Troll lives under the bridge. He is funny."),
    ("fam-10", VOICE_N, RATE_SLOW, "The family pet is a bat. His name is Nibbles."),

    # GRAMMAR · possessive 's drill sentences
    ("grm-01", VOICE_N, RATE_SLOW, "Wendy's mother is a witch."),
    ("grm-02", VOICE_N, RATE_SLOW, "Dracula's castle is on Pumpkin Hill."),
    ("grm-03", VOICE_N, RATE_SLOW, "Grandma's bandages are very old."),
    ("grm-04", VOICE_N, RATE_SLOW, "Freddy's pet bat is called Nibbles."),

    # READING · full narration
    ("rd-full", VOICE_N, RATE_SLOW,
     "On top of Pumpkin Hill, in a big dark castle, lives the Boo family. "
     "The father is Dracula. He is a vampire. He sleeps all day and works all night. "
     "The mother is Morticia. She is a witch and she has a big black cat. "
     "Dracula and Morticia have got two children. "
     "Their daughter is Wendy. She is thirteen, like a human girl, but she is a friendly ghost. "
     "Wendy's little brother is Freddy. He is ten and he is a slow, hungry zombie. He loves pizza. "
     "Grandma Mummy and Grandpa Skeleton live in the tower upstairs. "
     "Grandma is three thousand years old and she tells very long stories. "
     "Grandpa has no teeth, so he loves soup. "
     "The family pet is a small bat. His name is Nibbles. He sleeps in Freddy's bedroom and he eats fruit. "
     "Every Halloween the Boo family throws a big party. They are a spooky but very happy family."),

    # LISTENING · dialog "Who is this in the photo?"
    ("lst-01", VOICE_L, RATE_NORMAL, "Wow, Wendy! Who are all these monsters?"),
    ("lst-02", VOICE_N, RATE_SLOW, "Look — this is my family! The vampire is my father, Dracula. The witch is my mother, Morticia."),
    ("lst-03", VOICE_L, RATE_NORMAL, "And this little zombie — is he your brother?"),
    ("lst-04", VOICE_N, RATE_SLOW, "Yes! That's Freddy. He's ten. We've got a pet too — a bat called Nibbles."),
    ("lst-05", VOICE_L, RATE_NORMAL, "Nice! And who are those two old people in the tower?"),
    ("lst-06", VOICE_N, RATE_SLOW, "That's my grandma Mummy — she's three thousand years old — and my grandpa Skeleton. He loves soup."),

    # SPEAKING prompts (teacher voice)
    ("sp-01", VOICE_L, RATE_NORMAL, "How many people are there in your family? Use: there are."),
    ("sp-02", VOICE_L, RATE_NORMAL, "Have you got a brother or a sister? Say the name and age."),
    ("sp-03", VOICE_L, RATE_NORMAL, "Who is your favourite person in your family? Why?"),
    ("sp-04", VOICE_L, RATE_NORMAL, "Have you got a pet? What is its name?"),
    ("sp-05", VOICE_L, RATE_NORMAL, "If your family was a monster family — who would be what monster? My mum would be a..."),

    # WRITING · model sentence
    ("wr-model", VOICE_N, RATE_SLOW, "In my spooky family there are four people."),

    # VOCAB CAPSULE · single words (clear + slow)
    ("cap-01", VOICE_N, RATE_SLOW, "mother"),
    ("cap-02", VOICE_N, RATE_SLOW, "father"),
    ("cap-03", VOICE_N, RATE_SLOW, "sister"),
    ("cap-04", VOICE_N, RATE_SLOW, "brother"),
    ("cap-05", VOICE_N, RATE_SLOW, "grandma"),
    ("cap-06", VOICE_N, RATE_SLOW, "grandpa"),
    ("cap-07", VOICE_N, RATE_SLOW, "aunt"),
    ("cap-08", VOICE_N, RATE_SLOW, "uncle"),
    ("cap-09", VOICE_N, RATE_SLOW, "cousin"),
    ("cap-10", VOICE_N, RATE_SLOW, "pet"),
]

async def gen_one(name, voice, rate, text):
    out = OUT / f"{name}.mp3"
    if out.exists() and out.stat().st_size > 1000:
        return f"skip {name}"
    try:
        comm = edge_tts.Communicate(text, voice, rate=rate)
        await comm.save(str(out))
        if out.exists() and out.stat().st_size > 1000:
            return f"OK   {name}  {out.stat().st_size} B"
        return f"EMPTY {name}"
    except Exception as e:
        return f"ERR  {name}  {e}"

async def main():
    results = []
    # Process in small batches to avoid rate limit 403
    batch = 4
    for i in range(0, len(CLIPS), batch):
        chunk = CLIPS[i:i+batch]
        tasks = [gen_one(n, v, r, t) for (n, v, r, t) in chunk]
        rs = await asyncio.gather(*tasks)
        for r in rs:
            print(r)
            results.append(r)
        await asyncio.sleep(0.4)
    # retry empties / 403
    retry = [c for c in CLIPS if not (OUT / f"{c[0]}.mp3").exists() or (OUT / f"{c[0]}.mp3").stat().st_size < 1000]
    if retry:
        print(f"\n--- RETRY {len(retry)} clips after 5s pause ---")
        await asyncio.sleep(5)
        for n, v, r, t in retry:
            print(await gen_one(n, v, r, t))
    missing = [c[0] for c in CLIPS if not (OUT / f"{c[0]}.mp3").exists() or (OUT / f"{c[0]}.mp3").stat().st_size < 1000]
    if missing:
        print(f"\n!!! STILL MISSING: {missing}")
        sys.exit(1)
    print(f"\nAll {len(CLIPS)} clips OK.")

if __name__ == "__main__":
    asyncio.run(main())
