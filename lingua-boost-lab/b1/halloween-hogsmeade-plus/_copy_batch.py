import shutil, os
DL = os.path.expanduser("~/Downloads")
IMG = os.path.join(os.path.dirname(__file__), "assets", "img")
MAP = {
    "1236fc41-bff8-4a33-a0b3-ae515571ca21.png": "card-cat-crosses-path.png",
    "7e529ee3-7ecf-4f88-83d5-5e44b6f10342.png": "card-cat-doorstep-gold.png",
    "e697d827-bfc7-4704-b07d-23fcb3d6f545.png": "card-cat-mirror-ghost.png",
    "1f4bb976-d49d-4064-b8d2-ea4ff3b13190.png": "card-cat-cream-saucer.png",
    "5317e7bb-3847-4b58-98f5-ff91206ca8d4.png": "card-cat-whistle-ghosts.png",
    "215cc859-f3d4-4c9a-82df-b02809265777.png": "card-cat-bed-dream.png",
    "25869aac-050d-42aa-801f-7f4967c30212.png": "card-cat-shooting-star.png",
    "d0c611c1-168f-4058-b621-c4c780779020.png": "card-cat-grumpy-stranger.png",
    "3b96a4c5-67e8-4140-91ff-86b12be6c514.png": "scene-jack-lantern.png",
    "4fad80b1-70c9-4ea6-bec4-41a5e2f8d658.png": "scene-witch-cauldron.png",
    "bf7448ef-0b3e-403c-a236-2c13043d7942.png": "scene-cat-moonlit-wall.png",
    "99674b94-b8c6-4d70-8dde-0fa17d61feab.png": "scene-potion-happy.png",
    "636842e8-d23a-4cb9-9f09-29008e6534e7.png": "scene-halloween-world.png",
}
for src_name, dst_name in MAP.items():
    s = os.path.join(DL, src_name)
    d = os.path.join(IMG, dst_name)
    if os.path.exists(s):
        shutil.copy2(s, d)
        print(f"OK  {dst_name}  ({os.path.getsize(d):,} b)")
    else:
        print(f"MISS {src_name}")
