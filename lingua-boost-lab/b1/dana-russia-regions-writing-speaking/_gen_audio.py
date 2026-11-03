#!/usr/bin/env python3
# Generate 4 audio tracks for dana-russia-regions-writing-speaking lesson.
# Uses edge-tts for every clip, concatenates via raw mp3 byte-join (works with MP3).

import asyncio
import os
import subprocess
import time
from pathlib import Path

import edge_tts

HERE = Path(__file__).parent
OUT = HERE / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

# ====== 6-SPEAKER OGE MATCHING ======
SPEAKERS = [
    ("en-GB-SoniaNeural", "Speaker A. I grew up in Suzdal, and until I moved to Moscow for university I honestly thought every Russian town had fifty wooden churches and smelt of cucumbers in July. Only here, in the capital, I realised how unusual my hometown is -- and now I visit it every single holiday."),
    ("en-GB-ThomasNeural", "Speaker B. People always ask me, which Russian craft is the hardest to learn? I'd say Palekh miniatures. You spend five years at the school before anyone lets you touch a real box. Compare that to Khokhloma -- a talented student can start painting after one year."),
    ("en-GB-RyanNeural", "Speaker C. Last February I finally crossed Baikal on ice. We drove from Listvyanka to Olkhon Island on an official ice road. The ice was so transparent that you could see fish swimming eighty centimetres below your wheels -- and that was the most frightening and beautiful thing I've ever experienced."),
    ("en-GB-LibbyNeural", "Speaker D. My grandmother spoke Chuvash at home and taught me to count in it. Nowadays I live in Moscow and only use Russian, but every time I visit my relatives in Cheboksary I switch back. It's a kind of memory stored in your mouth, not your head."),
    ("en-GB-MaisieNeural", "Speaker E. We eat so many pancakes during Maslenitsa week that by Sunday I honestly cannot look at butter. But I still love the whole thing -- especially burning the straw doll of winter on the last evening. It really does feel like saying goodbye to the cold."),
    ("en-US-GuyNeural", "Speaker F. I'm not a religious person, but I love visiting old Russian monasteries. The silence inside those white-stone walls has nothing to do with faith -- it's about centuries of people whispering in the same place. You walk out calmer than you went in."),
]

# ====== LISTENING 1 · MASLENITSA MONOLOGUE ======
L1_VOICE = "en-GB-SoniaNeural"
L1_TEXT = (
    "Hello and welcome to Russia in Season. I'm Olga Petrova, and today we're talking about Maslenitsa -- Pancake Week -- one of the oldest and most beloved traditions in Russia. "
    "Maslenitsa is actually a pre-Christian festival that marks the end of winter and the arrival of spring. It takes place during the last week before the Orthodox Lent, which means the date changes every year -- usually late February or early March. "
    "Each of the seven days has its own name. Monday is called Vstrecha, the welcoming day. Tuesday is Zaigrysh -- the day of games, when young people meet. Wednesday is Lakomka, the sweet-tooth day, when a son-in-law visits his mother-in-law for pancakes. The real highlight comes on Sunday, called Forgiveness Sunday -- people apologise to one another and the straw doll of winter is burnt on a huge bonfire. "
    "And of course -- the pancakes. The round golden blini are not just a food, they are a symbol of the sun. A good Russian family eats dozens over the week: with butter and sour cream, with red caviar, with condensed milk, with honey, with jam. Even today, when fewer people go to church, almost everyone bakes blini for Maslenitsa. "
    "In Suzdal and Yaroslavl the festival has turned into a huge open-air event with troika sleigh rides, folk choirs and pancake-eating competitions. If you ever visit Russia in late winter, don't miss it."
)

# ====== LISTENING 2 · BAIKAL DIALOGUE ======
L2_V_CUST = "en-GB-RyanNeural"
L2_V_AGENT = "en-GB-LibbyNeural"
L2_LINES = [
    (L2_V_CUST, "Hello, I'd like some information about a trip to Lake Baikal."),
    (L2_V_AGENT, "Of course! When are you planning to go?"),
    (L2_V_CUST, "Probably February. Is it a good time?"),
    (L2_V_AGENT, "Yes, actually February is the magic season. The lake is completely frozen -- the ice can be up to a metre and a half thick. Visitors can walk on it, drive across it, even cycle."),
    (L2_V_CUST, "Really? How thick does it have to be before cars can drive?"),
    (L2_V_AGENT, "Around seventy centimetres is the safety minimum, but by mid-February it's usually much more. There are official ice roads from Listvyanka to Olkhon Island."),
    (L2_V_CUST, "Olkhon -- is that the biggest island?"),
    (L2_V_AGENT, "Yes, it's the fourth-largest lake island in the world. The main village is Khuzhir, where you'll find homestays, small restaurants and the famous Shaman Rock. The local Buryat people see it as a sacred place."),
    (L2_V_CUST, "Interesting. And what about activities?"),
    (L2_V_AGENT, "Hovercraft tours across the ice, visits to the ice caves on Olkhon's north coast, dog-sled rides, hot banya after a day outside. If you're lucky, you can even see methane bubbles frozen inside the ice."),
    (L2_V_CUST, "Sounds amazing. How do we get there from Moscow?"),
    (L2_V_AGENT, "Fly to Irkutsk -- six hours -- then it's a four-hour drive to Listvyanka or six hours to Olkhon."),
    (L2_V_CUST, "Can you organise the whole package?"),
    (L2_V_AGENT, "Of course. Four days with transfers, meals and two excursions costs around sixty-five thousand roubles per person."),
    (L2_V_CUST, "Perfect, I'll check my dates and get back to you tomorrow."),
]

# ====== LISTENING 3 · PALEKH INTERVIEW ======
L3_V_JOURN = "en-GB-SoniaNeural"
L3_V_MASTER = "en-GB-ThomasNeural"
L3_LINES = [
    (L3_V_JOURN, "Alexander, you've been painting Palekh miniatures for twenty-two years. How did you start?"),
    (L3_V_MASTER, "I was born in Palekh village, so I literally grew up in a workshop. My father was an icon-painter before the revolution, and after 1924 he joined the first Palekh artel. I went to the Palekh Art School at sixteen -- it's still the only school in the world that teaches this exact technique."),
    (L3_V_JOURN, "How long does one box take?"),
    (L3_V_MASTER, "A small round pin maybe two weeks. A large casket with a battle scene can take four months. Everything is painted with squirrel-hair brushes made of a few hairs each, and we grind our own tempera from egg yolk and natural pigments."),
    (L3_V_JOURN, "And the themes -- are they always folk tales?"),
    (L3_V_MASTER, "Mostly, yes. Pushkin's fairy tales, bylinas, Russian winter scenes, Troika. The black background is non-negotiable; it's what makes the gold stand out."),
    (L3_V_JOURN, "Are there many young painters today?"),
    (L3_V_MASTER, "Not enough. In the 1980s Palekh had about four hundred artists; now we're down to seventy. Young people don't want to spend five years learning before they can earn a living."),
    (L3_V_JOURN, "What would you say to a teenager considering it?"),
    (L3_V_MASTER, "Come, try it, paint one small box. If your hand loves it, it will stay with you. Palekh is not a job -- it's a way of looking at the world."),
]


async def _tts_to(voice: str, text: str, path: Path, retries: int = 3) -> None:
    """Synthesise one clip. 403 -> sleep+retry."""
    for attempt in range(1, retries + 1):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(path))
            if path.stat().st_size > 500:
                return
        except Exception as e:
            print(f"  attempt {attempt} failed: {e}")
        time.sleep(5)
    raise RuntimeError(f"failed to synth {path.name}")


def _concat_mp3(parts: list[Path], out: Path) -> None:
    """Join mp3 files by raw byte concat (works for same-codec edge-tts output)."""
    with open(out, "wb") as f_out:
        for p in parts:
            with open(p, "rb") as f_in:
                f_out.write(f_in.read())


async def build_matching() -> None:
    print("[1/4] 6-speaker OGE matching …")
    parts: list[Path] = []
    tmpdir = OUT / "_tmp_matching"
    tmpdir.mkdir(exist_ok=True)
    for i, (voice, text) in enumerate(SPEAKERS, 1):
        p = tmpdir / f"s{i}.mp3"
        print(f"  speaker {i} · {voice}")
        await _tts_to(voice, text, p)
        parts.append(p)
    final = OUT / "l0-matching-6speakers.mp3"
    _concat_mp3(parts, final)
    print(f"  -> {final} · {final.stat().st_size//1024} KB")


async def build_l1() -> None:
    print("[2/4] L1 Maslenitsa monologue …")
    final = OUT / "l1-maslenitsa.mp3"
    await _tts_to(L1_VOICE, L1_TEXT, final)
    print(f"  -> {final} · {final.stat().st_size//1024} KB")


async def build_dialogue(name: str, lines: list[tuple[str, str]], out_name: str) -> None:
    print(f"[{name}] dialogue · {len(lines)} turns …")
    tmpdir = OUT / f"_tmp_{out_name.replace('.mp3','')}"
    tmpdir.mkdir(exist_ok=True)
    parts: list[Path] = []
    for i, (voice, text) in enumerate(lines, 1):
        p = tmpdir / f"ln{i:02d}.mp3"
        await _tts_to(voice, text, p)
        parts.append(p)
    final = OUT / out_name
    _concat_mp3(parts, final)
    print(f"  -> {final} · {final.stat().st_size//1024} KB")


async def main() -> None:
    await build_matching()
    await build_l1()
    await build_dialogue("3/4", L2_LINES, "l2-baikal.mp3")
    await build_dialogue("4/4", L3_LINES, "l3-palekh.mp3")
    print("\nAll 4 audio files generated.")


if __name__ == "__main__":
    asyncio.run(main())
