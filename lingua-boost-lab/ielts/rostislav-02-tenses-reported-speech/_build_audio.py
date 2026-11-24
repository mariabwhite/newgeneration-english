"""Build the three audio tracks for Rostislav L2.

Uses edge-tts CLI. Retries on 403 token rotation issues.
"""
from __future__ import annotations
import os, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)

TRACKS = [
    {
        "file": "s06-reading-full.mp3",
        "voice": "en-US-JennyNeural",
        "rate": "-5%",
        "text": (
            "Why Honeybees Dance. "
            "Honeybees live in large colonies that depend on a steady supply of nectar. "
            "When a worker bee discovers a rich flower patch, she returns to the hive and performs a specialised movement known as the waggle dance. "
            "Other bees gather around her, read the dance, and then fly directly to the food source. "
            "The dance was decoded in the nineteen forties by the Austrian zoologist Karl von Frisch, who received the Nobel Prize in nineteen seventy three for this work. "
            "He showed that the bee runs in a figure of eight while vibrating her abdomen. "
            "Two features of the dance carry information. "
            "The angle of the waggle part relative to the vertical indicates the direction of the flowers in relation to the sun. "
            "The length of the waggle, measured in seconds, tells the other bees how far they must travel. "
            "Researchers today argue that this system meets the standard definition of symbolic communication. "
            "The bee is not simply reacting to a stimulus: she is encoding two independent variables, direction and distance, in a code that her sisters then decode. "
            "Modern studies suggest that the dance also contains a signal about the quality of the find, expressed through the number of repeats."
        ),
    },
    {
        "file": "s07-lecture.mp3",
        "voice": "en-US-GuyNeural",
        "rate": "-4%",
        "text": (
            "Good morning. Today I want to talk about a phenomenon that has shaped every language in the world: language contact. "
            "The linguist Uriel Weinreich said that language contact is as old as language itself, and I think he was right. "
            "Whenever two groups of people meet, they start to borrow words from each other. "
            "English is a famous example. Our everyday vocabulary includes words from more than three hundred and fifty other languages. "
            "Take the word sofa. It looks very English, but it is not. "
            "It came into English from Arabic, where the root suffa means a stone bench, and it travelled through Turkish and French before it reached London. "
            "The same is true of coffee, which came from Arabic qahwa, and of robot, which the Czech writer Karel Capek coined only a hundred years ago. "
            "Some people say that borrowing damages the receiving language. I disagree. "
            "A living language absorbs what it needs and discards what it does not. That is a sign of health, not decline. "
            "Before we finish, let me ask you: can you name one everyday English word that you think is originally English, but which is actually borrowed? "
            "Think about it for homework."
        ),
    },
    {
        "file": "s10-lecture.mp3",
        "voice": "en-US-AriaNeural",
        "rate": "-5%",
        "text": (
            "The reading makes a reasonable case, but it ignores what the research actually shows. "
            "First, the author claims that handwriting is slower than typing. "
            "That may be true, but studies by Mueller and Oppenheimer at Princeton have shown that students who write notes by hand remember the material better than students who type. "
            "The slower speed forces the brain to summarise rather than copy, and summarising is itself the act of learning. "
            "Second, the author says that handwriting has no use outside the classroom. "
            "In fact, memory specialists tell us that handwriting activates motor and visual areas of the brain simultaneously, which is why doctors still write prescriptions by hand in many countries. "
            "Finally, the author argues that we should redirect lesson time to coding. "
            "I would say that this is a false choice: children can learn to code and still practise handwriting, because the two skills use different parts of the brain and do not compete for the same time slot."
        ),
    },
]


def synth(track):
    out = AUDIO / track["file"]
    if out.exists() and out.stat().st_size > 10_000:
        print(f"SKIP {track['file']} (exists, {out.stat().st_size} bytes)")
        return True
    # remove empty 0-byte residues
    if out.exists() and out.stat().st_size < 10_000:
        out.unlink()
    cmd = [
        "edge-tts",
        "--voice", track["voice"],
        f"--rate={track['rate']}",
        "--text", track["text"],
        "--write-media", str(out),
    ]
    for attempt in range(4):
        print(f"SYNTH {track['file']} voice={track['voice']} attempt={attempt+1}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if out.exists() and out.stat().st_size > 10_000:
            print(f"  OK {out.stat().st_size} bytes")
            return True
        # 403 → delete partial, sleep, retry
        print(f"  FAIL rc={r.returncode} stderr={r.stderr[-200:] if r.stderr else ''}")
        if out.exists():
            out.unlink()
        time.sleep(5)
    return False


def main():
    failures = []
    for t in TRACKS:
        if not synth(t):
            failures.append(t["file"])
    if failures:
        print("\nFAILED:", failures)
        sys.exit(1)
    print("\nALL DONE")


if __name__ == "__main__":
    main()
