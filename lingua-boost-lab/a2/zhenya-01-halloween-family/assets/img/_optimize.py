"""Resize + optimize PNG → WebP for faster loading in Lab."""
from PIL import Image
import pathlib

IMG_DIR = pathlib.Path(__file__).parent
# Target widths: hero 1600, scenes 1200
widths = {
    "hero-boo-family-castle": 1600,
    "scene-family-couch": 1400,
    "scene-wendy-school": 1200,
    "scene-freddy-pizza-bat": 1200,
    "scene-luna-wolfy-twins-peony": 1400,
    "vocab-4-panel": 1200,
}

for png in IMG_DIR.glob("*.png"):
    stem = png.stem
    target_w = widths.get(stem, 1200)
    img = Image.open(png)
    w, h = img.size
    if w > target_w:
        new_h = int(h * target_w / w)
        img = img.resize((target_w, new_h), Image.LANCZOS)
    # Save WebP (quality 86 – good balance)
    out = IMG_DIR / f"{stem}.webp"
    img.save(out, "WEBP", quality=86, method=6)
    print(f"{stem}  {w}x{h} -> {img.size[0]}x{img.size[1]}  "
          f"{png.stat().st_size//1024}KB -> {out.stat().st_size//1024}KB")
