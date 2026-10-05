"""
Generate story.mp3 for julia-animal-exhibition (A1 Lab lesson).
Jenny neural reads 6 paragraphs with small pauses between them.
"""
import asyncio, os, subprocess, shutil, uuid, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
TMP  = os.path.join(HERE, "_tmp")
os.makedirs(TMP, exist_ok=True)

FFMPEG = shutil.which("ffmpeg") or r"C:\Users\Whitenois\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build\bin\ffmpeg.exe"

VOICE = "en-US-JennyNeural"

PARAS = [
    "Last Sunday was a sunny day. Julia, her best friend Masha and her little brother Vova went to a big animal exhibition in the city park. Mum gave them money for ice cream and said, Have a wonderful day!",
    "The first tent was full of rabbits. There were white rabbits, brown rabbits and even one very small grey rabbit. Masha touched a soft brown rabbit. It feels like a cloud, she said. Vova wanted to touch the grey one, but it hopped away.",
    "In the second tent they saw a big green parrot. The parrot could say hello and good morning. Vova stood in front of the cage and said hello ten times. The parrot answered every time. Julia laughed so much her stomach hurt.",
    "Then they walked to the pony area. A kind woman asked, Would you like to ride? Vova wanted to try, but he was a little afraid. Julia said, Don't worry, Vova. I will sit behind you. They climbed on the brown pony together. The pony walked slowly around the ring. Vova laughed and shouted, I am a cowboy!",
    "Masha's favourite animal was a small white cat with blue eyes. The cat sat on her lap for ten minutes and did not want to leave. Julia liked the parrot the most. Vova said, I love the pony! Mum, can we come here every Sunday?",
    "At the end of the day, they bought three big ice creams — strawberry for Julia, chocolate for Masha and vanilla for Vova. They sat on a bench, watched the people and the animals, and talked about which animal was the best. It was a perfect Sunday.",
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

async def main():
    sil_file = os.path.join(TMP, "sil_1.0.mp3")
    if not os.path.exists(sil_file):
        make_silence(1.0, sil_file)
    pieces = []
    for i, p in enumerate(PARAS):
        f = os.path.join(TMP, f"p{i+1:02d}.mp3")
        print(f"[{i+1}/{len(PARAS)}] TTS ... {p[:40]}...")
        await tts(p, VOICE, f)
        pieces.append(f)
        if i < len(PARAS) - 1:
            pieces.append(sil_file)
        await asyncio.sleep(0.3)
    out = os.path.join(HERE, "story.mp3")
    concat(pieces, out)
    for p in pieces:
        if p == sil_file: continue
        try: os.remove(p)
        except OSError: pass
    size = os.path.getsize(out)
    print(f"OK -> story.mp3 ({size/1024:.1f} KB)")

if __name__ == "__main__":
    asyncio.run(main())
