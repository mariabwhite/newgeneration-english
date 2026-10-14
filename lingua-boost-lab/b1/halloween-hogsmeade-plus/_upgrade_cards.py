import os
p = os.path.join(os.path.dirname(__file__), 'index.html')
with open(p, 'r', encoding='utf-8') as f: s = f.read()

# Each: (unique original front div, replacement front div with image)
PAIRS = [
    # Card 1 — crosses path
    ('<div class="face front"><div class="ico">🐈‍⬛</div><div class="label">If · 1 · England</div><div class="if">a <strong>black cat crosses</strong> your path…</div></div>',
     '<div class="face front with-img"><img src="assets/img/card-cat-crosses-path.png" alt="Black cat crossing a cobbled street"><div class="label">If · 1 · England</div><div class="if">a <strong>black cat crosses</strong> your path…</div></div>'),
    # Card 2 — doorstep Scotland
    ('<div class="face front"><div class="ico">🏠</div><div class="label">If · 2 · Scotland</div><div class="if">a black cat <strong>appears on your doorstep</strong>…</div></div>',
     '<div class="face front with-img"><img src="assets/img/card-cat-doorstep-gold.png" alt="Black cat on a doorstep with gold coins"><div class="label">If · 2 · Scotland</div><div class="if">a black cat <strong>appears on your doorstep</strong>…</div></div>'),
    # Card 4 — mirror / ghost
    ('<div class="face front"><div class="ico">🪞</div><div class="label">If · 4</div><div class="if">your cat <strong>refuses the mirror</strong> on October 31…</div></div>',
     '<div class="face front with-img"><img src="assets/img/card-cat-mirror-ghost.png" alt="Black cat looking away from a mirror with a ghost reflection"><div class="label">If · 4</div><div class="if">your cat <strong>refuses the mirror</strong> on October 31…</div></div>'),
    # Card 5 — cream saucer
    ('<div class="face front"><div class="ico">🥛</div><div class="label">If · 5</div><div class="if">you <strong>leave a saucer of cream</strong> on the step…</div></div>',
     '<div class="face front with-img"><img src="assets/img/card-cat-cream-saucer.png" alt="Black cat on a doorstep with a saucer of cream"><div class="label">If · 5</div><div class="if">you <strong>leave a saucer of cream</strong> on the step…</div></div>'),
    # Card 6 — whistle midnight
    ('<div class="face front"><div class="ico">🎵</div><div class="label">If · 6</div><div class="if">you <strong>whistle indoors</strong> after midnight…</div></div>',
     '<div class="face front with-img"><img src="assets/img/card-cat-whistle-ghosts.png" alt="Girl at the door with ghosts floating around and a cat leaving"><div class="label">If · 6</div><div class="if">you <strong>whistle indoors</strong> after midnight…</div></div>'),
    # Card 7 — bed / dreams
    ('<div class="face front"><div class="ico">🛏</div><div class="label">If · 7</div><div class="if">a black cat <strong>sits on your bed</strong>…</div></div>',
     '<div class="face front with-img"><img src="assets/img/card-cat-bed-dream.png" alt="Black cat on the bed of a sleeping child with magical dream clouds"><div class="label">If · 7</div><div class="if">a black cat <strong>sits on your bed</strong>…</div></div>'),
    # Card 8 — shooting star / one-eyed
    ('<div class="face front"><div class="ico">👁</div><div class="label">If · 8</div><div class="if">you see a <strong>one-eyed cat</strong> on Halloween night…</div></div>',
     '<div class="face front with-img"><img src="assets/img/card-cat-shooting-star.png" alt="Black cat looking up at a shooting star on Halloween night"><div class="label">If · 8</div><div class="if">you see a <strong>one-eyed cat</strong> on Halloween night…</div></div>'),
    # Card 9 — yawns at stranger
    ('<div class="face front"><div class="ico">😾</div><div class="label">If · 9</div><div class="if">a cat <strong>yawns at a stranger</strong>…</div></div>',
     '<div class="face front with-img"><img src="assets/img/card-cat-grumpy-stranger.png" alt="Grumpy black cat standing with pumpkins and autumn leaves"><div class="label">If · 9</div><div class="if">a cat <strong>yawns at a stranger</strong>…</div></div>'),
]

count = 0
for old, new in PAIRS:
    if old in s:
        s = s.replace(old, new)
        count += 1
    else:
        print(f"MISS: {old[:60]}...")

with open(p, 'w', encoding='utf-8') as f: f.write(s)
print(f"cards upgraded: {count}/8")
