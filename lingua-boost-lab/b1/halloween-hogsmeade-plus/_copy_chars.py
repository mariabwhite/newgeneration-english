import shutil, os
DL = os.path.expanduser("~/Downloads")
IMG = os.path.join(os.path.dirname(__file__), "assets", "img")
MAP = {
    "7bdbdc22-4048-4625-b298-7bb1c5dbd511.png": "char-witch-hazel.png",
    "fcd5129b-87e2-4951-9699-1558374525a1.png": "char-cat-kitty.png",
    "52ba5705-6298-41aa-b34f-c483ffe89a7e.png": "char-pumpkin-pip.png",
    "b59e28c7-5bd6-4fc9-9e1f-cffa2bdafba7.png": "char-ghost-boo.png",
    "34f5dce0-183c-4637-9dab-1b2917f30996.png": "char-zombie-zed.png",
    "dd827b23-aaa6-4b2a-8e55-15879e85d08b.png": "char-vampire-vlad.png",
    "e3da6e15-f7ff-44f6-88c9-760ae2bee0ec.png": "char-mummy-mo.png",
    "ff0144e7-375c-4361-bdcc-dee1ed7aeff6.png": "char-monster-furry.png",
    "e9f272cf-d7a8-4e77-a9eb-babf8c4daed3.png": "char-spider-cat-spidey.png",
}
for src, dst in MAP.items():
    s = os.path.join(DL, src)
    d = os.path.join(IMG, dst)
    if os.path.exists(s):
        shutil.copy2(s, d)
        print(f"OK  {dst}  ({os.path.getsize(d):,} b)")
    else:
        print(f"MISS {src}")
