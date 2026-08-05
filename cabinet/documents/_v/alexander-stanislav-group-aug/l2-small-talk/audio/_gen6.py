import asyncio, os, hashlib, re, json
import edge_tts

VOICE = "en-GB-SoniaNeural"
OUT = os.path.dirname(os.path.abspath(__file__))

PHRASES = [
    # primary dialogue · knock-out clichés
    "My name is Alex.",
    "I'm Stan.",
    "Nice to meet you too.",
    "I'm fine, thanks. And you?",
    "I'm good, thanks.",
    # 10 Present Simple questions about the daily routine
    "What time do you get up?",
    "What do you have for breakfast?",
    "How do you get to work?",
    "What time do you start work?",
    "Where do you have lunch?",
    "When do you finish work?",
    "What do you do after work?",
    "How often do you go to the gym?",
    "Do you watch TV in the evening?",
    "What time do you go to bed?",
    # Model для блока рутины
    "I get up at seven. I have coffee for breakfast. I go to work by metro.",
]

def slugify(text):
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    s = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:40]
    return f"{s}-{h}.mp3"

async def gen(phrase):
    fname = slugify(phrase)
    fpath = os.path.join(OUT, fname)
    if os.path.exists(fpath):
        return fname, phrase
    comm = edge_tts.Communicate(phrase, VOICE, rate="-5%")
    await comm.save(fpath)
    return fname, phrase

async def main():
    manifest_path = os.path.join(OUT, "_manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    for p in PHRASES:
        fname, phrase = await gen(p)
        manifest[phrase] = fname
        print(f"  {fname}  <-  {phrase.encode('ascii', 'ignore').decode()}")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"done. {len(PHRASES)} phrases · manifest = {len(manifest)} entries")

asyncio.run(main())
