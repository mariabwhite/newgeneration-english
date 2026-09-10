"""Generate lst1.mp3, lst2.mp3, lst3.mp3 for sofia-pavlova-01-recap via edge-tts + ffmpeg concat.

Speaker voice map is chosen for clarity + variety, not accents pretending to be Russian.
Windows-safe: utf-8 reconfigure + tempdir under this folder (no MAX_PATH surprise with Кириллица).
"""
import sys, os, subprocess, asyncio, tempfile
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

HERE = os.path.abspath(os.path.dirname(__file__))

# ------------------------------------------------------------ LST1 · 6 monologues
LST1 = [
    ("en-US-GuyNeural",    "I've always been drawn to supernatural dramas, but what really keeps me watching is the way they explore moral dilemmas that ordinary shows never touch. When a vampire has to decide between saving one human he loves and dozens of strangers, you feel that weight for days. The costumes and effects are fine, but for me the real magic is the ethical questions — should you forgive someone who betrayed you, does redemption really exist, is loyalty always a virtue? Those conversations continue in my head long after the credits roll."),
    ("en-GB-RyanNeural",   "Honestly, most modern series feel too loud and too fast for me. I grew up watching old black-and-white classics with my grandfather — long slow takes, careful lighting, actors who could say everything with a single glance. Give me a two-hour film from the 1950s and I'll take it over a ten-season streaming saga any day. The new shows recycle the same tricks with better cameras, but the storytelling craft simply isn't there. Old cinema teaches you patience; modern series teach you to keep scrolling."),
    ("en-US-AriaNeural",   "Last Friday I started a new supernatural series just to watch one episode before bed — and I finished all ten by Sunday evening. I barely slept, I skipped breakfast, and by Monday morning my eyes were burning and I couldn't remember basic French vocabulary at school. It was genuinely one of the stupidest weekends of my life, and yet I know I'll probably do it again with the next season. Binge-watching feels great in the moment and awful the next day, and I keep swearing I'll never do it — until the next cliffhanger."),
    ("en-GB-MaisieNeural", "For me, series are basically a free language lab. I switch on English subtitles first, then after a few episodes I turn them off completely, and by the end of the season I can pick up phrases I would never learn from a textbook. My teacher noticed almost immediately — my speaking became more natural, my vocabulary jumped, and I started catching jokes and cultural references. If a teenager wants to improve their English fast, forget grammar apps: watch two seasons of anything with proper native accents."),
    ("en-US-JennyNeural",  "Frankly, I think TV series are a huge waste of time. Twenty hours to finish a season — twenty hours you could have spent reading a proper novel, going for a walk, or actually talking to real human beings. A good book stays with you for a lifetime; a streaming series evaporates from memory in about a week. My friends spend their weekends catching up on episodes, and I spend mine catching up on classic literature. Guess whose university application looks stronger."),
    ("en-GB-SoniaNeural",  "After a long school day, when my head is full of maths formulas and half-finished essays, the last thing I need is more mental effort. I put on something familiar and undemanding — a comedy series I've already seen twice, or a light supernatural drama where I can predict the plot — and I just breathe. No commitment, no thinking, just background comfort. It works better than any wellness app my mother keeps recommending. Sometimes the point of a TV series isn't to move you; it's simply to help you switch off."),
]

# ------------------------------------------------------------ LST2 · Emma & Kate dialogue
EMMA = "en-GB-LibbyNeural"
KATE = "en-GB-SoniaNeural"
LST2 = [
    (EMMA, "Kate, have you heard? They're finally launching the Vampire Diaries reboot in October!"),
    (KATE, "No way! Are you serious? I still remember us crying over the original ending back in secondary school."),
    (EMMA, "Same. I've watched the original series three times already — I'm probably the biggest fan in our class."),
    (KATE, "Have you seen any of the new season yet?"),
    (EMMA, "Not a single episode. Nothing has aired yet. The premiere is on the fourteenth of October — I've counted the days."),
    (KATE, "And what about the cast?"),
    (EMMA, "That's the thing — it's completely new. None of the original actors are returning. New Elena, new Damon, new Stefan. Same town, different faces."),
    (KATE, "Interesting. Where can we watch it?"),
    (EMMA, "Netflix has the streaming rights. So at least it's easy to access."),
    (KATE, "Perfect. We should absolutely watch the first episode together on the fourteenth. My place or yours?"),
    (EMMA, "Yours, obviously — you have the bigger screen. Should we invite anyone else?"),
    (KATE, "Let's decide later. First episode, just the two of us. Deal?"),
    (EMMA, "Deal. I'll bring popcorn. And tissues, because you know I'll cry."),
]

# ------------------------------------------------------------ LST3 · Host & Elena interview
HOST  = "en-GB-RyanNeural"
ELENA = "en-US-AriaNeural"
LST3 = [
    (HOST,  "Elena, welcome. You are only 26, but you have just released a supernatural drama series that everyone is talking about. Where does that imagination come from?"),
    (ELENA, "Thank you. Well, I grew up in Kazan, a city with two cultures constantly living side by side. That gave me a taste for stories where different worlds collide. But my earliest inspiration was much simpler — I spent my childhood reading fantasy novels under the blanket with a torch. Tolkien, Le Guin, all the Russian folk tales — that was my true film school before I ever picked up a camera."),
    (HOST,  "And your formal education?"),
    (ELENA, "I started with journalism at Kazan Federal University because my parents insisted on a real profession. I finished my degree, worked for a newspaper for six months, hated every day of it, and then applied to a screenwriting course in Moscow. That was the moment my life actually began."),
    (HOST,  "Have you worked abroad?"),
    (ELENA, "Yes, twice. I did a three-month writers' residency in Prague, and then a longer project in Berlin working on a European co-production. Both cities were inspiring, but Berlin especially taught me discipline — German producers do not tolerate excuses."),
    (HOST,  "What has been your biggest professional challenge?"),
    (ELENA, "Rejection, without question. Before this series was picked up, I collected around forty rejections from studios. Some were polite, some were brutal. For two years I genuinely thought I would never sell a script."),
    (HOST,  "How do you keep going through years like that?"),
    (ELENA, "Habit. I write every single morning before nine, no exceptions — weekends, holidays, sick days, doesn't matter. Two thousand words before breakfast. Ninety percent of it is rubbish, but that habit is the only thing that saved my career."),
    (HOST,  "Finally, what would you tell a teenager who dreams of writing?"),
    (ELENA, "Write badly first. That is the whole secret. Every young writer wants their first draft to be brilliant, and then they freeze. Give yourself permission to write terrible pages — you can only edit words that already exist on the screen."),
]

async def synth(voice, text, out_path, rate="-5%"):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate)
    await communicate.save(out_path)

def concat_mp3(parts, final_path):
    listfile = os.path.join(HERE, "_concat.txt")
    with open(listfile, "w", encoding="utf-8") as f:
        for p in parts:
            f.write("file '" + p.replace("\\", "/") + "'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
         "-c:a", "libmp3lame", "-b:a", "128k", final_path],
        check=True, capture_output=True
    )
    os.remove(listfile)

async def build(segments, out_name):
    with tempfile.TemporaryDirectory(dir=HERE, prefix="_tts_") as td:
        parts = []
        for i, (voice, text) in enumerate(segments):
            part = os.path.join(td, f"p{i:02d}.mp3")
            await synth(voice, text, part)
            parts.append(part)
            print(f"  · {i+1}/{len(segments)}  {voice}  {text[:60]}...")
        final = os.path.join(HERE, out_name)
        concat_mp3(parts, final)
        size = os.path.getsize(final) / 1024
        print(f"  ✓ {out_name}  ({size:.1f} KB)")

async def main():
    print("LST1 · 6 monologues");                    await build(LST1, "lst1.mp3")
    print("LST2 · Emma & Kate dialogue (14 turns)"); await build(LST2, "lst2.mp3")
    print("LST3 · Host & Elena interview (12 turns)"); await build(LST3, "lst3.mp3")
    print("\nDone.")

if __name__ == "__main__":
    asyncio.run(main())
