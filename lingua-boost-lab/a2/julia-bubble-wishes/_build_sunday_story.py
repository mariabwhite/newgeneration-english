"""Generate Sunday-race consolidation story MP3 for julia-bubble-wishes 7+."""
import asyncio, pathlib, time
import edge_tts

HERE = pathlib.Path(__file__).parent
AUDIO = HERE / "audio"
AUDIO.mkdir(exist_ok=True)

NARR = "en-US-AriaNeural"

STORY = (
    "Chapter 1. Sunday morning. Emma knocked on Julia's door before breakfast. "
    "We are going to the park in half an hour! she said, her trainers already laced. "
    "A real mini-race on the running track. Coach Mike is going to use his stopwatch, "
    "and he will hand out tiny medals. "
    "I'm nervous, Julia said. She was still in her pyjamas. What if I'm last? "
    "Break a leg! Emma laughed. That means good luck. And I've got my fingers crossed for you. "

    "Chapter 2. By ten o'clock they were walking down the street. "
    "The sun was about to pop out from behind a tall cloud. "
    "Julia had packed a bottle of water, her blue sneakers, and a tiny bubble bottle for after the race. "
    "If I win, Julia said quietly, I will blow one giant bubble at the finish line. Just one. For luck. "
    "Knock on wood, Emma whispered, and tapped a wooden bench as they walked past. "

    "Chapter 3. At the track, Coach Mike was already blowing his whistle. "
    "Six other kids were doing warm-up jumps. Lane three is yours, Julia, he said. Emma, lane four. "
    "Julia looked at her lane and took a deep breath. She hadn't raced in a month. "
    "This might be beginner's luck, Emma said, because you haven't practised much. But sometimes that's a good thing. "
    "I'm not sure I will be first, Julia said. I might be third. Or fourth. We will see. "

    "Chapter 4. The race started. Coach Mike raised his hand. On your marks, get set — and the whistle blew. "
    "Julia sprinted. She could feel her heart in her ears. "
    "She wasn't going to win on pure speed — John was faster — but she was going to try. "
    "As luck would have it, she thought, the wind is behind me today. "
    "She passed one runner at the middle lane. Then another. The finish line was close. "
    "She couldn't hear anything except her sneakers hitting the track. "

    "Chapter 5. Julia crossed the line second. Emma was third. "
    "John, the fastest boy in the group, was first — of course. "
    "Better luck next time! John shouted, smiling. He wasn't being mean. He was offering a hand. "
    "I'm not out of luck, Julia laughed, catching her breath. Silver is my colour. "
    "Coach Mike pressed his stopwatch and showed Julia the time. "
    "By next Sunday you will have beaten this by two seconds, I'm telling you. Just keep going. "

    "Chapter 6. Later, as the sun was setting, Julia pulled out the tiny bubble bottle at the finish line. "
    "She blew one slow, round bubble into the orange sky. "
    "Make a wish, Emma said. I will, said Julia. I'm going to wish for one more Sunday like this one. "
    "Shall we do it again next week? Emma asked. "
    "Yes — the arrangement is already in the diary. Sunday, ten o'clock, same track. "
    "Coach Mike said he will be bringing new stopwatches. Julia's lucky break had turned into a plan."
)

async def main():
    out = AUDIO / "sunday-story.mp3"
    for attempt in range(1, 4):
        try:
            print(f"[try {attempt}] {out.name}")
            comm = edge_tts.Communicate(STORY, NARR, rate="-6%")
            await comm.save(str(out))
            if out.exists() and out.stat().st_size > 1000:
                print(f"  OK · {out.stat().st_size//1024} KB")
                return
            print("  empty file, retry")
            out.unlink(missing_ok=True)
        except Exception as e:
            print(f"  ERR {e}")
            if out.exists() and out.stat().st_size < 1000:
                out.unlink(missing_ok=True)
        time.sleep(5)
    raise RuntimeError("failed after 3 tries")

asyncio.run(main())
