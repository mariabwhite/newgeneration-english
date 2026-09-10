"""Generate MP3 for every clickable word in Julia's Flags & Countries lesson.
Run: python _gen_audio.py
"""
import sys, asyncio, pathlib
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

VF = "en-GB-SoniaNeural"   # calm BrE female
VM = "en-GB-RyanNeural"    # BrE male (used for some greetings for variety)

# id → (text, voice)
CLIPS = {
    # ─── 20 country names (English pronunciation) ─────────────
    "uk":                ("the United Kingdom", "f"),
    "usa":               ("the United States",  "f"),
    "canada":            ("Canada",              "f"),
    "australia":         ("Australia",           "f"),
    "france":            ("France",              "f"),
    "italy":             ("Italy",               "f"),
    "spain":             ("Spain",               "f"),
    "germany":           ("Germany",             "f"),
    "portugal":          ("Portugal",            "f"),
    "netherlands":       ("the Netherlands",     "f"),
    "greece":            ("Greece",              "f"),
    "sweden":            ("Sweden",              "f"),
    "russia":            ("Russia",              "f"),
    "poland":            ("Poland",              "f"),
    "turkey":            ("Turkey",              "f"),
    "china":             ("China",               "f"),
    "japan":             ("Japan",               "f"),
    "korea":             ("South Korea",         "f"),
    "india":             ("India",               "f"),
    "egypt":             ("Egypt",               "f"),
    "brazil":            ("Brazil",              "f"),
    "argentina":         ("Argentina",           "f"),
    "mexico":            ("Mexico",              "f"),
    "peru":              ("Peru",                "f"),
    "belgium":           ("Belgium",             "f"),
    "morocco":           ("Morocco",             "f"),
    "israel":            ("Israel",              "f"),

    # ─── 20 nationality adjectives / person nouns ─────────────
    "british":           ("British",             "f"),
    "american":          ("American",            "f"),
    "canadian":          ("Canadian",            "f"),
    "australian":        ("Australian",          "f"),
    "french":            ("French",              "f"),
    "italian":           ("Italian",             "f"),
    "spanish":           ("Spanish",             "f"),
    "german":            ("German",              "f"),
    "portuguese":        ("Portuguese",          "f"),
    "dutch":             ("Dutch",               "f"),
    "greek":             ("Greek",               "f"),
    "swedish":           ("Swedish",             "f"),
    "russian":           ("Russian",             "f"),
    "polish":            ("Polish",              "f"),
    "turkish":           ("Turkish",             "f"),
    "chinese":           ("Chinese",             "f"),
    "japanese":          ("Japanese",            "f"),
    "korean":            ("Korean",              "f"),
    "indian":            ("Indian",              "f"),
    "egyptian":          ("Egyptian",            "f"),
    "brazilian":         ("Brazilian",           "f"),
    "mexican":           ("Mexican",             "f"),
    "peruvian":          ("Peruvian",            "f"),

    # ─── 8 special person nouns (Pattern C from Afanasyeva 8) ─
    "englishman":        ("an Englishman",       "f"),
    "frenchman":         ("a Frenchman",         "f"),
    "dutchman":          ("a Dutchman",          "f"),
    "spaniard":          ("a Spaniard",          "f"),
    "pole":              ("a Pole",              "f"),
    "turk":              ("a Turk",              "f"),
    "swede":             ("a Swede",             "f"),
    "briton":            ("a Briton",            "f"),

    # ─── 12 greetings (native pronunciations approximated by BrE voice) ─
    "hello_bonjour":     ("Bonjour",             "f"),
    "hello_hola":        ("Hola",                "f"),
    "hello_ciao":        ("Ciao",                "f"),
    "hello_hallo":       ("Hallo",               "f"),
    "hello_konnichiwa":  ("Konnichiwa",          "f"),
    "hello_nihao":       ("Ni hao",              "f"),
    "hello_privet":      ("Privet",              "f"),
    "hello_merhaba":     ("Merhaba",             "f"),
    "hello_kalimera":    ("Kalimera",            "f"),
    "hello_ola":         ("Olá",                 "f"),
    "hello_namaste":     ("Namaste",             "f"),
    "hello_salam":       ("As-salamu alaykum",   "f"),
}

VMAP = {"f": VF, "m": VM}
OUT = pathlib.Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

async def one(name: str, text: str, voice: str) -> None:
    dest = OUT / f"{name}.mp3"
    if dest.exists() and dest.stat().st_size > 500:
        print(f"skip  {name}.mp3 ({dest.stat().st_size} B)")
        return
    tts = edge_tts.Communicate(text=text, voice=voice, rate="-8%")
    await tts.save(str(dest))
    print(f"ok    {name}.mp3 ({dest.stat().st_size} B)")

async def main() -> None:
    for name, (text, vkey) in CLIPS.items():
        await one(name, text, VMAP[vkey])
    print(f"\nDone. {len(CLIPS)} clips in {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
