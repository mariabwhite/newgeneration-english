"""
Bake all audio for Lab L3 · The Letter from Aunt Edith
- Narrative sentences (parsed from HTML .r-sent)
- Pre-reading vocab-match (parsed from .pv-row)
- Vocab capsule (parsed from .vcard)
- Speaking exercise model audio (parsed from [data-a] in shadow / minimal-pair / transformation / role-play)
- Listening clips (hard-coded scripts, 30-60s each)
Voices:
  Sonia  - Narrator / Taisiya / Mary (young female British)
  Olivia - Mrs Polk / Rosemary / Edith (older female)
  Ryan   - Terry / Jim / Cafe owner / Station master (male British)
  Thomas - Benjamin the lighthouse keeper (older male)
Retry: 3 attempts on 403 · deletes 0-byte files · concurrency 4.
"""
import asyncio
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import edge_tts

HERE = Path(__file__).parent
HTML = HERE / "index.html"
OUT = HERE / "audio"
OUT.mkdir(exist_ok=True)

V_NARR = "en-GB-SoniaNeural"
V_OLIVIA = "en-GB-OliviaNeural"
V_RYAN = "en-GB-RyanNeural"
V_THOMAS = "en-GB-ThomasNeural"

CONCURRENCY = 4
RETRIES = 3

# ============================================================
# 1. LISTENING CLIPS (hard-coded scripts)
# ============================================================
LISTENING_CLIPS = {
    # Ch 5 · Mary the baker (Sonia)
    "c5-ex4-clip.mp3": (V_NARR,
        "Morning, love. I'm Mary — I've been running this bakery for twelve years now. "
        "Your aunt? Oh, I knew her well. Edith came in every Friday for a saffron bun and a loaf of brown bread. "
        "Never missed a Friday. We'd talk about the weather, about the sea. "
        "She was the first person who told me how to get the bread right in a damp kitchen. "
        "You'll find Rosemary at the library — she knows everyone in this village, knew Edith from childhood. "
        "Tell her Mary sent you."),
    # Ch 6 · Rosemary the librarian (Olivia)
    "c6-ex4-clip.mp3": (V_OLIVIA,
        "Edith came to this library every Tuesday for forty years. "
        "She borrowed a book, returned a book, left a jar of honey on the desk. "
        "That was her ritual. She was... careful. Quiet. Reserved. "
        "She liked history, biography, letters of dead poets. Never novels. "
        "And then, about two years ago, she stopped coming. "
        "I didn't ask. Some things you don't ask. "
        "Go to the harbour. Find Jim. He knows the door."),
    # Ch 7 · Jim the fisherman (Ryan)
    "c7-ex4-clip.mp3": (V_RYAN,
        "Edith's cottage? Been empty two months now. Up that lane, first cottage after the last gate. "
        "Blue door. You can't miss it. The roof's new — she had it done in spring. "
        "The key's under the stone bird in the garden. She always said — if family comes, let them in. "
        "I used to bring her mackerel on Saturday. She paid me in biscuits. "
        "She was a tough one, Edith. Spent her whole life on this coast. "
        "Welcome home, lass."),
    # Ch 8 · Cafe owner (Ryan)
    "c8-ex4-clip.mp3": (V_RYAN,
        "So — the lighthouse. Two ways to get there, love. "
        "The cliff path is beautiful but she's exposed to the wind. "
        "The road is longer, takes about forty minutes, but she's safe. "
        "Today? I'd take the road. Weather's turning. See those clouds? Storm by nightfall. "
        "Tell Benjamin the keeper that I sent you — he'll put the kettle on. "
        "And wouldja mind picking up a loaf of bread from Mary on the way? He runs out."),
    # Ch 9 · Benjamin (Thomas)
    "c9-ex4-clip.mp3": (V_THOMAS,
        "Edith came up here every Saturday. Every single Saturday for fifty years. "
        "Sat in that chair, where you're sitting now, and watched the sea. "
        "Sometimes we talked, sometimes we didn't. We didn't need to. "
        "She's been coming longer than I've been the keeper — I took the job in nineteen eighty-two. "
        "The cat? That's Pumpkim. Edith named him. She said he looked like a pumpkin in October. "
        "You're the first family of hers I've ever met."),
    # Ch 10 · Benjamin reads first letter (Thomas)
    "c10-ex4-clip.mp3": (V_THOMAS,
        "This is the first one. Dated the second of October, nineteen eighty-seven. "
        "Darling. I lost her last spring. My daughter, my only one. "
        "She was six years old. The sea took her. I buried her in the churchyard above Mousehole. "
        "I have not written to your mother. I don't know how. "
        "I kept thinking the words would come. They never did. "
        "If you are reading this, I am sorry. I waited too long."),
    # Ch 11 · Edith on cassette (Olivia)
    "c11-ex4-clip.mp3": (V_OLIVIA,
        "Darling. I have thought about this island every hour since your mother left. "
        "I wrote to her for years. I cried for a week when the first letter came back unopened. "
        "I taught botany at the village school for twenty-eight years. "
        "I kept bees. I grew dahlias. The families of this village became my family. "
        "I do not know who will be listening to this. "
        "But if you are my sister's child, come to Cornwall. Stay a while. I will show you everything."),
    # Ch 12 · Edith records welcome (Olivia)
    "c12-ex4-clip.mp3": (V_OLIVIA,
        "If you are hearing this, you have found the house. "
        "The key is under the stone bird in the garden. "
        "Make yourself at home. The kettle is on the hob. "
        "There is bread in the cupboard and honey on the shelf. "
        "I am not writing a new letter. I am done with letters. "
        "I am in the garden. Come out when you are ready."),
    # Ch 13 · Edith in garden (Olivia)
    "c13-ex4-clip.mp3": (V_OLIVIA,
        "This garden has been mine for forty years. "
        "These roses were planted the year I lost my daughter. "
        "The dahlias came later. The cabbages are new — only three years old. "
        "I keep bees. That hive is twenty years old. I have my own honey. "
        "The birds know me. The bees know me. The sparrows come down for crumbs at breakfast. "
        "And now you are here. There are cups on the kitchen shelf. There is enough cake for both of us."),
    # Ch 14 · Edith tells full story (Olivia)
    "c14-ex4-clip.mp3": (V_OLIVIA,
        "I left home at nineteen, after a fight with my mother. I never went back. "
        "I came to Cornwall because a friend offered me a room. "
        "I taught at the village school. I married a fisherman called Will. "
        "He drowned when I was thirty-seven. We had one daughter. She died at six. "
        "After that I kept writing letters to your mother. She never replied. "
        "When I knew I was dying, I posted the tape. I hoped the sea would bring you. "
        "Stay as long as you like, darling. The guest room has a view of the sea."),
}

# ============================================================
# 2. Character voice mapping for role-play / speaking audio
# ============================================================
CHAR_VOICE = {
    "edith": V_OLIVIA, "polk": V_OLIVIA, "rose": V_OLIVIA, "rosemary": V_OLIVIA,
    "mary": V_NARR,
    "terry": V_RYAN, "jim": V_RYAN, "owner": V_RYAN, "master": V_RYAN, "t1": V_RYAN, "t2": V_RYAN,
    "ben": V_THOMAS, "benjamin": V_THOMAS,
    "model": V_NARR,
}


def voice_for_path(path: str) -> str:
    """Pick voice based on filename suffix."""
    name = Path(path).stem.lower()
    # Explicit character suffix after last dash (e.g. c3-ex3-t1)
    for key, v in CHAR_VOICE.items():
        if name.endswith("-" + key):
            return v
    return V_NARR


# ============================================================
# 3. Parse HTML for all audio paths + extract text
# ============================================================
def extract_manifest():
    soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    manifest = {}  # path -> (voice, text)

    # --- Narrative sentences ---
    for sent in soup.select(".r-sent[data-audio]"):
        path = sent["data-audio"]
        txt_el = sent.select_one(".r-txt")
        if txt_el:
            text = txt_el.get_text(" ", strip=True)
            manifest[path] = (V_NARR, text)

    # --- Pre-reading vocab-match (.pv-row) ---
    for row in soup.select(".pv-row"):
        wd = row.select_one(".pv-word")
        if not wd:
            continue
        say_btn = wd.select_one("button[data-a]")
        if not say_btn:
            continue
        path = say_btn.get("data-a")
        # Word text = pv-word text WITHOUT the button text
        word_text = wd.get_text(" ", strip=True)
        if path and word_text:
            manifest[path] = (V_NARR, word_text)

    # --- Vocab capsule (.vcard) ---
    for card in soup.select(".vcard"):
        say_btn = card.select_one("button.say[data-a]")
        w_el = card.select_one(".w")
        if not say_btn or not w_el:
            continue
        path = say_btn.get("data-a")
        word = w_el.get_text(" ", strip=True)
        if path and word:
            manifest[path] = (V_NARR, word)

    # --- Shadow exercise rows (.sh-row with .sh-say[data-a] + .sh-text) ---
    for row in soup.select(".sh-row"):
        say_btn = row.select_one(".sh-say[data-a]")
        txt_el = row.select_one(".sh-text")
        if not say_btn or not txt_el:
            continue
        path = say_btn.get("data-a")
        text = txt_el.get_text(" ", strip=True)
        if path and text:
            manifest[path] = (V_NARR, text)

    # --- Minimal-pair / MCQ-style with .mp-say[data-a] + .mp-pair ---
    for item in soup.select(".mp-item"):
        say_btn = item.select_one(".mp-say[data-a]")
        pair_el = item.select_one(".mp-pair")
        if not say_btn or not pair_el:
            continue
        path = say_btn.get("data-a")
        # Replace slashes / vs for TTS clarity
        text = pair_el.get_text(" ", strip=True).replace("/", " or ").replace("vs", " or ")
        if path and text:
            manifest[path] = (V_NARR, text)

    # --- Transformation (.tr-row with .tr-say + .tr-src) ---
    for row in soup.select(".tr-row"):
        say_btn = row.select_one(".tr-say[data-a]")
        src_el = row.select_one(".tr-src")
        if not say_btn or not src_el:
            continue
        path = say_btn.get("data-a")
        text = src_el.get_text(" ", strip=True)
        if path and text:
            manifest[path] = (V_NARR, text)

    # --- Role-play (.rp div with .rp-play[data-a] + .rp-line text) ---
    for rp in soup.select(".rp"):
        for turn in rp.select(".rp-turn"):
            play_btn = turn.select_one(".rp-play[data-a]")
            line_el = turn.select_one(".rp-line")
            if not play_btn or not line_el:
                continue
            path = play_btn.get("data-a")
            # Get only direct text, exclude the .rp-play button text
            for sub in line_el.select(".rp-play, .rp-stem"):
                sub.extract()
            text = line_el.get_text(" ", strip=True)
            if path and text:
                manifest[path] = (voice_for_path(path), text)

    # --- Listening narr-btn clips (play-all / slow) · handled manually ---
    for path, (voice, text) in LISTENING_CLIPS.items():
        manifest[path] = (voice, text)

    # Also build slow versions (rate -30%)
    slow_manifest = {}
    for path, (voice, text) in LISTENING_CLIPS.items():
        slow_path = path.replace(".mp3", "-slow.mp3")
        slow_manifest[slow_path] = (voice, text, "-30%")

    return manifest, slow_manifest


# ============================================================
# 4. Baker
# ============================================================
async def bake_one(path_rel: str, voice: str, text: str, rate: str = "+0%"):
    out = OUT / Path(path_rel).name  # strip "audio/" prefix
    if out.exists() and out.stat().st_size > 1000:
        return (path_rel, "skip")
    for attempt in range(1, RETRIES + 1):
        try:
            # Clean zero-byte if exists
            if out.exists() and out.stat().st_size < 500:
                out.unlink()
            tts = edge_tts.Communicate(text, voice, rate=rate)
            await tts.save(str(out))
            if out.exists() and out.stat().st_size > 1000:
                return (path_rel, f"ok ({out.stat().st_size // 1024}KB)")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"  retry {attempt}/{RETRIES} {path_rel}: {type(e).__name__}: {e}", flush=True)
            await asyncio.sleep(5)
    return (path_rel, "FAIL")


async def main():
    manifest, slow_manifest = extract_manifest()

    all_jobs = []
    for path, (voice, text) in manifest.items():
        all_jobs.append((path, voice, text, "+0%"))
    for path, (voice, text, rate) in slow_manifest.items():
        all_jobs.append((path, voice, text, rate))

    # De-dupe by output filename
    seen = set()
    jobs = []
    for job in all_jobs:
        name = Path(job[0]).name
        if name in seen:
            continue
        seen.add(name)
        jobs.append(job)

    total = len(jobs)
    print(f"Manifest: {total} clips to bake into {OUT}", flush=True)

    # Count skipped
    already = sum(1 for j in jobs if (OUT / Path(j[0]).name).exists()
                  and (OUT / Path(j[0]).name).stat().st_size > 1000)
    print(f"Already baked: {already} · to go: {total - already}", flush=True)

    sem = asyncio.Semaphore(CONCURRENCY)
    done = {"n": 0, "ok": 0, "skip": 0, "fail": 0}

    async def worker(job):
        async with sem:
            path, voice, text, rate = job
            result = await bake_one(path, voice, text, rate)
            done["n"] += 1
            if result[1].startswith("ok"):
                done["ok"] += 1
            elif result[1] == "skip":
                done["skip"] += 1
            elif result[1] == "FAIL":
                done["fail"] += 1
                print(f"[{done['n']}/{total}] FAIL {result[0]}", flush=True)
            # Progress every 20
            if done["n"] % 20 == 0 or done["n"] == total:
                print(f"  progress {done['n']}/{total} · ok={done['ok']} skip={done['skip']} fail={done['fail']}", flush=True)

    await asyncio.gather(*(worker(j) for j in jobs))

    print(f"\nDONE · ok={done['ok']} skip={done['skip']} fail={done['fail']} total={total}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
