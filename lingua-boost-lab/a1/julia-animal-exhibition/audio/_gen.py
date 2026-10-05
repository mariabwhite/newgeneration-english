"""
Generate text1.mp3, text2.mp3, text3.mp3 for julia-animal-exhibition.
Multi-voice: Narrator, Julia, Emma, John, Mrs. Pilsberry, extras.
"""
import asyncio, os, subprocess, shutil, uuid, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
TMP  = os.path.join(HERE, "_tmp")
os.makedirs(TMP, exist_ok=True)

FFMPEG = shutil.which("ffmpeg") or r"C:\Users\Whitenois\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"

# Voices
N  = "en-US-AriaNeural"            # Narrator (neutral, clear)
JU = "en-US-JennyNeural"           # Julia (teen girl, warm)
EM = "en-GB-SoniaNeural"           # Emma (British, teen)
JO = "en-US-AnaNeural"             # John (child voice)
MP = "en-GB-LibbyNeural"           # Mrs. Pilsberry (older, kind, British)
CM = "en-US-GuyNeural"             # Carousel man

# Each item: (voice, text) — pause 0.5s after each line
TEXT1 = [
    (N,  "Text one. Sunday morning at the gate."),
    (N,  "Last Sunday was a beautiful warm day. Julia, her friend Emma and her little brother John went to the big city park. There was a fair with carousels, a Ferris wheel, food stalls and a special animal exhibition. John was six years old, and he was very excited. He had never been to a fair before."),
    (N,  "At the gate, there was a long queue for tickets. Mum gave Julia some money and said:"),
    (N,  "Buy three tickets. Keep John close. Have fun! The children stood in the queue for ten minutes. John wanted everything at once — the carousels, the ice cream, the animals."),
    (JO, "I want to ride the horses now!"),
    (JU, "Wait a minute, John. First we buy the tickets."),
    (EM, "And then we have a plan. Animals first, then carousels, then ice cream."),
    (JO, "But I'm hungry!"),
    (JU, "It's only ten o'clock. You can wait one hour, John."),
    (JO, "One hour is a long time!"),
    (EM, "One hour is sixty minutes, John. We can do a lot in one hour."),
    (N,  "Finally, it was their turn. Julia bought three tickets — one for her, one for Emma and one for John. The tickets were orange and had a little picture of a horse on them. John put his ticket in his pocket very carefully."),
    (JO, "I won't lose it."),
]

TEXT2 = [
    (N,  "Text two. The animal exhibition and Mrs. Pilsberry."),
    (N,  "They walked into the big white pavilion. Inside, there were tables and cages with animals. Julia saw rabbits, two parrots, a small aquarium with goldfish, and even a wise brown owl sitting on a wooden perch. In the corner, there was a quiet lady with grey hair, a long green dress and a kind smile. On her table there were six fluffy grey kittens with big round eyes and tiny folded ears."),
    (MP, "These are Scottish Folds. I am a cat breeder. My name is Mrs. Pilsberry."),
    (N,  "John opened his mouth and whispered:"),
    (JO, "They look like little clouds."),
    (N,  "The lady laughed."),
    (MP, "You can stroke them very gently. One finger. Like this."),
    (JO, "Can I touch one? Please?"),
    (MP, "Yes, you can. But very gently, John."),
    (JO, "Oh! It's so soft!"),
    (EM, "Mrs. Pilsberry, how old are the kittens?"),
    (MP, "They are nine weeks old. They are ready for a new home."),
    (JU, "Are they expensive?"),
    (MP, "They are purebred, so yes — one kitten costs about fifty thousand roubles. But I only sell to good families."),
    (JO, "Julia, can we have one? Please, please!"),
    (JU, "John, we already have Barsik at home. And Barsik is a king. He wouldn't like a tiny kitten in his kingdom."),
    (N,  "Mrs. Pilsberry gave each child a small photo of her favourite kitten."),
    (MP, "Her name is Pearl. She is my first and best cat."),
    (N,  "John put the photo next to his ticket in his pocket."),
    (JO, "I will show it to Barsik."),
    (N,  "The children said thank you and walked to the next pavilion."),
]

TEXT3 = [
    (N,  "Text three. Carousels, horses and ice cream."),
    (N,  "After the exhibition, the children ran to the carousels. The music was loud, the lights were bright and the air smelled of popcorn and sugar. There were three carousels — the small one with painted horses, the big one with golden swans, and a tiny one for little children with cars and planes."),
    (N,  "John wanted the painted horses."),
    (JO, "Please, please, please!"),
    (N,  "He pulled Julia's hand. Emma laughed."),
    (EM, "I think he already decided."),
    (N,  "They gave the man their orange tickets. John chose a white horse with a pink saddle. Julia chose the one next to him — a brown horse with blue eyes. Emma didn't want a horse; she wanted the Ferris wheel."),
    (JO, "Julia, look at me! I'm a cowboy!"),
    (JU, "You look wonderful, John. Hold on tight!"),
    (CM, "Hold the bar, little man! Here we go!"),
    (JO, "I'm not scared! I'm not scared!"),
    (JU, "Are you excited?"),
    (JO, "I'm super excited! Can we do it again?"),
    (JU, "One more time, and then ice cream, okay?"),
    (JO, "Okay! But the ice cream must be very big!"),
    (N,  "Emma was already in the queue for the Ferris wheel. From the top, she said later, she could see the whole park — the tents, the carousels, the queue for ice cream and even their mum walking back from the shops."),
    (EM, "I waved at everyone, but of course nobody saw me."),
    (N,  "At the end of the day, they bought three enormous ice creams. Strawberry for Julia, chocolate with sprinkles for Emma and — of course — a double vanilla for John, because he deserved a very, very big one. They sat on a bench near the fountain and talked about the day."),
    (JO, "This was the best Sunday of my life."),
    (N,  "Julia and Emma looked at each other and smiled."),
]

async def tts(text, voice, out):
    for attempt in range(6):
        try:
            await edge_tts.Communicate(text, voice).save(out)
            if os.path.getsize(out) > 500:
                return
            raise RuntimeError("empty")
        except Exception as e:
            last = e
            await asyncio.sleep(1.5 + attempt)
    raise last

def make_silence(sec, out):
    subprocess.run([FFMPEG, "-y", "-f", "lavfi", "-i",
                    f"anullsrc=r=24000:cl=mono", "-t", str(sec),
                    "-q:a", "9", "-acodec", "libmp3lame", out],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def concat(files, out):
    lf = os.path.join(TMP, f"list_{uuid.uuid4().hex}.txt")
    with open(lf, "w", encoding="utf-8") as f:
        for p in files:
            safe = p.replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{safe}'\n")
    subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0",
                    "-i", lf, "-c", "copy", out],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(lf)

async def build_text(name, lines):
    sil = os.path.join(TMP, "sil_0.6.mp3")
    if not os.path.exists(sil):
        make_silence(0.6, sil)
    pieces = []
    for i, (voice, text) in enumerate(lines):
        f = os.path.join(TMP, f"{name}_{i:02d}.mp3")
        print(f"  [{i+1}/{len(lines)}] {voice[:14]}... {text[:50]}")
        await tts(text, voice, f)
        pieces.append(f)
        if i < len(lines) - 1:
            pieces.append(sil)
        await asyncio.sleep(0.25)
    out = os.path.join(HERE, f"{name}.mp3")
    concat(pieces, out)
    for p in pieces:
        if p == sil: continue
        try: os.remove(p)
        except OSError: pass
    size = os.path.getsize(out)
    print(f"  OK -> {name}.mp3 ({size/1024:.1f} KB)")

async def main():
    # cleanup old story.mp3 if present
    old = os.path.join(HERE, "story.mp3")
    if os.path.exists(old):
        os.remove(old)
        print("Removed old story.mp3")
    print("Text 1 ...")
    await build_text("text1", TEXT1)
    print("Text 2 ...")
    await build_text("text2", TEXT2)
    print("Text 3 ...")
    await build_text("text3", TEXT3)
    print("ALL DONE")

if __name__ == "__main__":
    asyncio.run(main())
