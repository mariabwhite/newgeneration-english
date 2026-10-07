"""Resize + save Kruglov mock PNGs to assets/img/ as optimised JPEGs."""
import os
from PIL import Image

SRC = r"C:\Users\Whitenois\Downloads"
DST = r"C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\01_Сайт New Generation — сайт, Lab, кабинет\site-public-clean\lingua-boost-lab\c1\toefl-2026-mock-b2plus-andrew\assets\img"
os.makedirs(DST, exist_ok=True)

mapping = [
    # Primary picks (embedded in HTML)
    ("f707763c-c3f7-4438-8c3e-9ae3b3e50bf9.png", "hero.jpg",         1400),
    ("91720567-d76d-4415-9085-5c82d888be70.png", "img-s04.jpg",       900),
    ("7f5f13a3-759d-4bab-8a27-1d672625cb89.png", "img-s05.jpg",       900),
    ("3af0573b-a7fd-43fd-b859-d4d3ea97c52a.png", "img-s09.jpg",       900),
    ("645e613f-0a3e-4129-b08b-61bfa0a1cf44.png", "img-s11.jpg",       900),
    ("3720063e-2948-449a-8816-910e25a79f2e.png", "img-s15.jpg",       600),
    # Alternates (not embedded, kept for easy swap)
    ("cd92fc4a-9ce1-432d-92de-45ff2fd4da96.png", "hero-alt.jpg",     1400),
    ("76090780-82c6-4deb-aaf9-f040cf88cac8.png", "img-s04-alt.jpg",   900),
]

for src_name, dst_name, max_w in mapping:
    src = os.path.join(SRC, src_name)
    dst = os.path.join(DST, dst_name)
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        if w > max_w:
            im = im.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
        im.save(dst, "JPEG", quality=86, optimize=True)
    print(f"OK  {dst_name:20s} {im.size[0]}x{im.size[1]}  {os.path.getsize(dst)//1024} KB")
