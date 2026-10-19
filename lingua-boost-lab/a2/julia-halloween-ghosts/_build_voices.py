"""Character voice lines + story-scene chunks for julia-halloween-ghosts.

Each clip is one short line in a dedicated kid-friendly voice.
"""
import asyncio, pathlib, edge_tts

HERE = pathlib.Path(__file__).parent / "audio"
HERE.mkdir(exist_ok=True)

# voices
JULIA = "en-US-JennyNeural"       # 10yo girl
JOHN  = "en-US-AnaNeural"         # kid voice (younger)
MAMA  = "en-GB-LibbyNeural"       # mum
PAPA  = "en-US-GuyNeural"         # dad
EMMA  = "en-US-AriaNeural"        # girl friend
GRAN  = "en-GB-SoniaNeural"       # grandma ghost
BOY   = "en-US-AnaNeural"         # ghost boy
WIZ   = "en-US-DavisNeural"       # wizard

CLIPS = {
    # cast strip signatures
    "cast-julia":  (JULIA, "Hi, I'm Julia. I'm a witch tonight!"),
    "cast-john":   (JOHN,  "I'm John, a vampire. Boo!"),
    "cast-mama":   (MAMA,  "I'm Mama, a black cat. Meow."),
    "cast-papa":   (PAPA,  "I'm Papa, a mummy. Help... help!"),
    "cast-emma":   (EMMA,  "Hi, I'm Emma, Julia's best friend. I'm a friendly ghost!"),

    # story scene chunks (short, listen-and-react)
    "scene-start":    (JULIA, "It was Halloween night. The moon was big and orange."),
    "scene-dressup":  (MAMA,  "Let's dress up and go trick-or-treating! All of us together!"),
    "scene-candy":    (JOHN,  "People gave us lots of candy. My bag is full!"),
    "scene-castle":   (JULIA, "At the end of the street, there was an old, old castle. Nobody had lived there for a hundred years."),
    "scene-knock":    (JOHN,  "Knock! Knock! Knock! The door opened by itself..."),
    "scene-grandma":  (GRAN,  "Welcome, children! I am so happy to see you in my old castle."),
    "scene-boy":      (BOY,   "Do you have more candy? I love candy!"),
    "scene-wizard":   (WIZ,   "Come, dance with me under the moon, mummy-man!"),
    "scene-end":      (EMMA,  "Thank you! Come back next Halloween! Bye-bye!"),
}

async def one(slug, voice, text, tries=3):
    out = HERE / f"{slug}.mp3"
    if out.exists() and out.stat().st_size > 1024:
        return "skip"
    for i in range(tries):
        try:
            await edge_tts.Communicate(text, voice, rate="-5%").save(str(out))
            if out.exists() and out.stat().st_size > 1024:
                return "ok"
            out.unlink(missing_ok=True)
        except Exception as e:
            print(f"  retry {i+1}/{tries} {slug}: {e}")
            out.unlink(missing_ok=True)
            await asyncio.sleep(5)
    return "fail"

async def main():
    r = {"ok":0, "skip":0, "fail":0}
    for slug, (voice, text) in CLIPS.items():
        s = await one(slug, voice, text)
        r[s] += 1
        print(f"  {s:<4} {slug}")
    print(r)

if __name__ == "__main__":
    asyncio.run(main())
