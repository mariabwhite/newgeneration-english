"""Extra TTS: 5 character mini-bios + 1 dialogue + 5 riddles + 4 listen&tick sentences."""
import asyncio, pathlib, edge_tts

HERE = pathlib.Path(__file__).parent / "audio"
HERE.mkdir(exist_ok=True)

NARR  = "en-US-AriaNeural"
GIRL  = "en-US-JennyNeural"      # Julia
EMMA  = "en-US-MichelleNeural"   # Emma (different girl voice)
BOY   = "en-US-AnaNeural"
MAN   = "en-US-GuyNeural"
GB    = "en-GB-SoniaNeural"
GB2   = "en-GB-LibbyNeural"

CLIPS = {
    # 5 character mini-bios (A2, 2-3 short sentences)
    "bio-vampire": (MAN, "Hello! I am a vampire. My name is Vlad. I don't like the sun. I sleep in the day and I fly at night. I love bats. I don't eat garlic!"),
    "bio-witch":   (GB2, "Hi! I am a witch. My name is Hazel. I have a tall black hat and a long broomstick. I live in a dark forest. I cook magic potions in my big cauldron."),
    "bio-mummy":   (MAN, "Good night. I am a mummy. My name is Mo. I am very, very old — three thousand years old! I am from Egypt. I like to walk slowly and say... help."),
    "bio-skeleton":(NARR, "Boo! I am a skeleton. I have no skin, no muscles, no blood — only bones! I live in old graveyards. I can dance all night long. I love Halloween!"),
    "bio-zombie":  (BOY, "Hi, friends. I am a zombie. My name is Zed. I walk slowly. I love brains... just kidding! I love pizza. I live in the old shopping mall. See you tonight!"),

    # dialogue · Julia and Emma at the first house (role-play audio)
    "dlg-julia-1": (GIRL, "Look at this house, Emma! There are three jack-o'-lanterns on the porch!"),
    "dlg-emma-1":  (EMMA, "Wow! They are beautiful. Shall we knock on the door?"),
    "dlg-julia-2": (GIRL, "Yes! Ready? One, two, three. Trick or treat!"),
    "dlg-emma-2":  (EMMA, "The grandma is giving us candy! Thank you, grandma!"),
    "dlg-julia-3": (GIRL, "My bag is almost full. Let's try one more house, Emma!"),
    "dlg-emma-3":  (EMMA, "OK! Oh look — there is a big old castle at the end of the street..."),

    # 5 "What am I?" riddles
    "rid-1": (NARR, "I am tall and black. I have a broomstick and a big hat. I cook potions in a cauldron. What am I?"),
    "rid-2": (NARR, "I am white and transparent. I live in old houses and castles. I say Boo. What am I?"),
    "rid-3": (NARR, "I am orange. I have a scary face and a candle inside me. People put me on windows. What am I?"),
    "rid-4": (NARR, "I have no skin and no blood. Only bones. I can dance in the graveyard. What am I?"),
    "rid-5": (NARR, "I have black wings. I fly only at night. I sleep in dark caves and old attics. What am I?"),

    # 4 "listen and tick" sentences (A2 kid)
    "tick-1": (GIRL, "The witch is sitting on a big pumpkin."),
    "tick-2": (GIRL, "The ghost is flying over the castle."),
    "tick-3": (GIRL, "The black cat is on the roof under the moon."),
    "tick-4": (GIRL, "Three bats are flying out of the attic."),
}

async def one(slug, voice, text, tries=3, rate="-5%"):
    out = HERE / f"{slug}.mp3"
    if out.exists() and out.stat().st_size > 1024:
        return "skip"
    for i in range(tries):
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(str(out))
            if out.exists() and out.stat().st_size > 1024:
                return "ok"
            out.unlink(missing_ok=True)
        except Exception as e:
            print(f"  retry {i+1}/{tries} {slug}: {e}")
            out.unlink(missing_ok=True)
            await asyncio.sleep(5)
    return "fail"

async def main():
    r = {"ok":0,"skip":0,"fail":0}
    for slug,(voice,text) in CLIPS.items():
        s = await one(slug, voice, text)
        r[s] += 1
        print(f"  {s:<4} {slug}")
    print(r)

if __name__ == "__main__":
    asyncio.run(main())
