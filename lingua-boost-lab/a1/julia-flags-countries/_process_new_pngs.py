"""Process the 7 fresh Downloads PNGs — background already transparent,
just resize to max 900px + save WebP into assets/img/.
Falls back to black-pixel-to-transparent removal if image is fully opaque.
"""
import sys, os, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

SRC = pathlib.Path(r"C:\Users\Whitenois\Downloads")
DST = pathlib.Path(__file__).parent / "assets" / "img"
DST.mkdir(parents=True, exist_ok=True)

MAP = {
    "aef7607a-53c8-43f9-978e-f34d321d183c.png": "s1-flag-stickers.webp",     # 9 Julia flags stickers → sec-1 warm-up opener
    "34773291-af8d-48c7-bac1-4bf847a11875.png": "s2-signpost.webp",          # signpost countries/languages/people → sec-2 theory opener
    "f6f4fb8c-1c56-49bd-b976-ae821de5a69b.png": "s7-hello-bubbles.webp",     # speech bubbles Bonjour/Hola/Ciao → sec-7 hello
    "5901bce9-d1a3-4d8b-98d1-c124f1773472.png": "s8-food-blackboard.webp",   # FOOD AROUND THE WORLD → sec-8
    "28cdf828-b273-4269-bf9a-bdb4cb337538.png": "s9-money-jar.webp",         # money coins → sec-9 currencies
    "e934fc12-6681-4716-8979-4a331fe3ec20.png": "s12-postcards-envelope.webp",  # envelope with question cards → sec-12 postcards
    "30ed33e8-4366-4b6e-aacb-beff29ff7ce5.png": "s16-world-notes-book.webp", # my world notes book → sec-16 vocab bank
}

MAX_W = 900
BLACK_THRESHOLD = 32  # r+g+b sum below → treat as background

for src_name, dst_name in MAP.items():
    src = SRC / src_name
    if not src.exists():
        print(f"MISS  {src_name}")
        continue
    im = Image.open(src).convert("RGBA")
    r, g, b, a = im.split()
    amin, amax = a.getextrema()
    if amin == 255:
        # fully opaque — remove dark background
        px = im.load()
        w, h = im.size
        for y in range(h):
            for x in range(w):
                pr, pg, pb, pa = px[x, y]
                if pr + pg + pb < BLACK_THRESHOLD:
                    px[x, y] = (pr, pg, pb, 0)
        print(f"      {dst_name} — removed black bg")
    else:
        print(f"      {dst_name} — alpha already present (min={amin})")
    w, h = im.size
    if w > MAX_W:
        nh = int(h * MAX_W / w)
        im = im.resize((MAX_W, nh), Image.LANCZOS)
    dst = DST / dst_name
    im.save(dst, "WEBP", quality=88, method=6)
    kb = os.path.getsize(dst) // 1024
    print(f"OK    {dst_name:36s} {im.size[0]}x{im.size[1]} = {kb} KB")
