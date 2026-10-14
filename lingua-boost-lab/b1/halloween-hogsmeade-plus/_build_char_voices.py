"""9 character voice clips for halloween-hogsmeade-plus match-task."""
import asyncio, os, subprocess, sys, time
ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "assets", "audio")
os.makedirs(AUDIO, exist_ok=True)

# (slug, text, voice, rate, pitch, ffmpeg_fx)
CHARS = [
    ("hazel",  "Come in, dearie… come in. The cauldron is just waiting for you. Don't be shy, hee hee hee. Step inside.",
     "en-GB-SoniaNeural", "-16%", "-6Hz",
     "aecho=0.85:0.9:70|180|300:0.4|0.3|0.2,volume=1.3"),
    ("kitty",  "Mrrrow! Hello, I'm Kitty. I'm a witch's kitten. I like socks, and I like naps. Will you scratch my ear?",
     "en-US-AnaNeural", "+2%", "+14Hz",
     "aecho=0.5:0.6:30:0.2,volume=1.25"),
    ("pip",    "Ha ha ha! I am Pip the Pumpkin Elf! Do you like my hat? It's bigger than my head! Let's go trick-or-treating!",
     "en-US-AndrewNeural", "+6%", "+8Hz",
     "aecho=0.6:0.7:40:0.2,volume=1.25"),
    ("boo",    "Boooo… I'm Boo. I'm a very little ghost. Would you like to hold my pumpkin? It's heavy for me, you know.",
     "en-US-JennyNeural", "-18%", "+8Hz",
     "aecho=0.9:0.9:100|250|400:0.5|0.35|0.25,volume=1.35"),
    ("zed",    "Uhhh… hi there… I'm… Zed. I'm a zombie. I lost my… uhhh… what was I saying? Oh yes. Brains. I like brains.",
     "en-US-GuyNeural", "-32%", "-18Hz",
     "aecho=0.85:0.85:80|200:0.4|0.3,volume=1.4"),
    ("vlad",   "Good evening. I am Vlad, a vampire. I promise I don't bite… very hard. Would you join me for one small drink?",
     "en-GB-ThomasNeural", "-6%", "-5Hz",
     "aecho=0.8:0.85:60|160:0.4|0.3,volume=1.3"),
    ("mo",     "Mmmfff… hello… I am Mo, the mummy. My scarf keeps my neck warm. Which is useful, because… I don't really have one.",
     "en-US-RogerNeural", "-22%", "-12Hz",
     "aecho=0.9:0.9:90|240:0.45|0.3,lowpass=f=2800,volume=1.4"),
    ("furry",  "Hi hi hi! I am Furry! I know I look a bit scary, but really I just want a big big hug! Will you give me one?",
     "en-US-ChristopherNeural", "+8%", "+6Hz",
     "aecho=0.6:0.7:40:0.22,volume=1.25"),
    ("spidey", "Pssst… over here. I'm Spidey. Half cat. Half spider. All witch's hat. Eight legs for climbing bookshelves nobody else can reach. Follow me…",
     "en-GB-RyanNeural", "-12%", "-3Hz",
     "aecho=0.85:0.85:60|180|300:0.42|0.28|0.18,volume=1.3"),
]

async def tts_batch():
    import edge_tts
    for slug, text, voice, rate, pitch, _fx in CHARS:
        raw = os.path.join(AUDIO, f"char-{slug}.mp3")
        if os.path.exists(raw) and os.path.getsize(raw) > 0:
            print(f"[skip-tts] {raw}")
            continue
        print(f"[tts] {slug} ({voice}, {rate}, {pitch})")
        for attempt in range(3):
            try:
                await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(raw)
                if os.path.getsize(raw) == 0: raise RuntimeError("empty")
                print(f"       {os.path.getsize(raw)}b OK (try{attempt+1})")
                break
            except Exception as e:
                print(f"       try{attempt+1} ERR {str(e)[:80]}")
                try: os.remove(raw)
                except: pass
                if attempt < 2: time.sleep(4)
                else: print(f"       GIVE UP on {slug}")

def ffmpeg_fx():
    for slug, _t, _v, _r, _p, flt in CHARS:
        inp = os.path.join(AUDIO, f"char-{slug}.mp3")
        out = os.path.join(AUDIO, f"char-{slug}-fx.mp3")
        if not os.path.exists(inp): continue
        if os.path.exists(out) and os.path.getsize(out) > 0:
            print(f"[skip-fx] {out}")
            continue
        cmd = f'ffmpeg -y -i "{inp}" -af "{flt}" -c:a libmp3lame -b:a 128k "{out}"'
        print(f"$ {cmd[:100]}...")
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"       ERR\n{r.stderr[-400:]}")
        else:
            print(f"       {os.path.getsize(out)}b OK")

if __name__ == "__main__":
    print("=== TTS ===")
    asyncio.run(tts_batch())
    print("\n=== FX ===")
    ffmpeg_fx()
    print("\nDONE")
    for s, *_ in CHARS:
        p = os.path.join(AUDIO, f"char-{s}-fx.mp3")
        if os.path.exists(p):
            print(f"  {s}-fx: {os.path.getsize(p):,}b")
