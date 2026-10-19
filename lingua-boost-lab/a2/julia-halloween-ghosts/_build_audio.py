"""Generate TTS clips for julia-halloween-ghosts (A2 kid, Halloween).

Girl voice (Jenny) for Julia's own lines + pre-reading questions.
Woman narrator (Aria) for the story main body.
Boy voice (Ryan) for John's lines where needed.

Only writes clips that don't exist, with 3 retries on edge-tts 403.
"""
import asyncio, os, pathlib, time
import edge_tts

HERE = pathlib.Path(__file__).parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)

NARR  = "en-US-AriaNeural"
GIRL  = "en-US-JennyNeural"
BOY   = "en-US-RyanMultilingualNeural"
MAMA  = "en-GB-LibbyNeural"

STORY_MAIN = """
It was Halloween night. The moon was big and orange. Julia and her family lived on Garden Street in Rostov. This year, Mama had a great idea.
"Let's dress up and go trick-or-treating — all of us together!"
Julia put on a long black dress and a tall witch hat. Her brother John was a vampire with white skin and red eyes. Papa was a mummy — Mama used ten metres of toilet paper on him. Mama was a black cat with little ears. And Julia's best friend Emma was a funny ghost in a big white sheet with pink slippers.
The five of them went from door to door. People gave them a lot of candy. Julia's bag was full. Emma was laughing all the time.
At the end of the street, there was an old, old castle. It had two tall towers, broken shutters, and a dead garden. The iron gate was half-open. Nobody had lived in the castle for one hundred years.
"Let's try the castle!" said John. He was not afraid at all.
"The castle?" said Mama. "I don't know..."
"Please, Mama!" said Julia and Emma together.
But the children were already at the big wooden door. John knocked three times. Knock. Knock. Knock.
The door opened by itself.
Inside the castle, it was dark and cold. Then — a soft lavender light. On the grand staircase, there was a woman. She was white and transparent. She was a real ghost!
"Welcome!" said the grandma ghost. "I am so happy to see children in my old castle!"
Emma hid behind Julia for one second. Then she saw the ghost's kind eyes and smiled. Julia was not scared either.
In the castle kitchen, there was a boy ghost. He was eating a cookie. He saw John and smiled.
"Do you have more candy?" he asked. "I love candy."
John gave him two chocolate bars. The boy ghost was so happy.
In the attic, there was an old dog ghost. He was wagging his tail. He jumped on Emma and licked her face through the sheet. Emma laughed and laughed.
In the castle garden, a tall wizard ghost was walking under the moon. He had a magic wand with little stars.
Julia, John and Emma played with the ghost boy. Papa danced a funny mummy-dance with the wizard. Mama talked to the grandma ghost about old recipes.
At midnight, the big castle clock said "Bong, bong, bong".
"It's time," said the grandma ghost quietly. "Thank you for a magic night. Come back next Halloween!"
Julia, Emma and John ran home. Their bags were full of candy. Their hearts were full of magic. It was the best Halloween ever.
""".strip()

STORY_PRE = """
Before you read, think about three questions. One. Do you believe in ghosts? Two. What costume do you like for Halloween? Three. If a ghost is kind, is it scary or fun?
Now press play and listen to the story. You can read along with the text.
""".strip()

TRADITIONS = """
Listen and fill in the words. On Halloween, people put jack-o-lanterns outside the house. The orange colour means the harvest season. People buy spooky costumes. Students like having Halloween parties. In Rome, people played a game with apples.
""".strip()

VOCAB_WORDS = [
    "ghost", "witch", "vampire", "mummy", "pumpkin", "jack-o-lantern",
    "haunted house", "candy", "trick or treat", "costume",
    "broomstick", "bat", "skeleton", "cauldron", "spooky", "scary",
    "moon", "attic", "midnight", "knock",
]

CLIPS = []
CLIPS.append(("story-pre",       STORY_PRE,  GIRL))
CLIPS.append(("story-main",      STORY_MAIN, NARR))
CLIPS.append(("tradition-audio", TRADITIONS, NARR))
for w in VOCAB_WORDS:
    slug = w.replace("'", "").replace(" ", "-")
    CLIPS.append((slug, w, GIRL))

RATE_SLOW = "-10%"

async def one(slug, text, voice, tries=3):
    out = AUDIO / f"{slug}.mp3"
    if out.exists() and out.stat().st_size > 1024:
        return "skip"
    for attempt in range(tries):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=RATE_SLOW)
            await communicate.save(str(out))
            if out.exists() and out.stat().st_size > 1024:
                return "ok"
            else:
                if out.exists(): out.unlink()
        except Exception as e:
            print(f"  attempt {attempt+1}/{tries} failed for {slug}: {e}")
            if out.exists(): out.unlink()
            await asyncio.sleep(5)
    return "fail"

async def main():
    print(f"Target dir: {AUDIO}")
    print(f"Clips: {len(CLIPS)}")
    results = {"ok": 0, "skip": 0, "fail": 0}
    for slug, text, voice in CLIPS:
        r = await one(slug, text, voice)
        results[r] += 1
        print(f"  {r:<4} {slug}")
    print(f"\nDone: {results}")

if __name__ == "__main__":
    asyncio.run(main())
