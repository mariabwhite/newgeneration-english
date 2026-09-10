import sys, os
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

SRC = r"C:\Users\Whitenois\Downloads"
DST = os.path.join(os.path.dirname(__file__), "assets", "img")
os.makedirs(DST, exist_ok=True)

MAP = {
    "891492c2-de66-4146-8a39-28e4af058ca2.png": "hero-around-world.webp",
    "0808a7a0-dbd6-48f7-964e-148fdbabcd84.png": "theory-3-sisters.webp",
    "5d7037b7-0905-423b-9ac7-872fbe475e2f.png": "theory-3-patterns-overview.webp",
    "86d75fa9-98c4-4647-9fee-6a286184a40d.png": "theory-pattern-a.webp",
    "e501cce7-f51b-4b1e-b2fc-5330c4870d6b.png": "theory-pattern-b.webp",
    "aab7138f-c730-49e5-a68a-9387c41e0af3.png": "theory-pattern-c.webp",
    "9bbcdadc-89aa-4226-a7bf-12f7255dd2ed.png": "decor-flag-medallions.webp",
}

MAX_W = 1400
for src_name, dst_name in MAP.items():
    src = os.path.join(SRC, src_name)
    dst = os.path.join(DST, dst_name)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w > MAX_W:
        nh = int(h * MAX_W / w)
        im = im.resize((MAX_W, nh), Image.LANCZOS)
    im.save(dst, "WEBP", quality=82, method=6)
    kb = os.path.getsize(dst) // 1024
    print(f"{dst_name:40s} {im.size[0]}x{im.size[1]} = {kb} KB")
