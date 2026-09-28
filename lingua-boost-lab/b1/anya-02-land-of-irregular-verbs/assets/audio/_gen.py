"""Generate family-chants.mp3 via edge-tts for sec-18 dictation."""
import sys, asyncio
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

SCRIPT = """Family one, the -ought family. Buy, bought, bought. Bring, brought, brought. Think, thought, thought.

Family two, the -ew family. Know, knew, known. Grow, grew, grown. Fly, flew, flown.

Family three, the i to a family. Sing, sang, sung. Drink, drank, drunk. Swim, swam, swum.

Family four, the -ame family. Come, came, come. Once again — come, came, come."""

VOICE = "en-GB-LibbyNeural"

async def main():
    communicate = edge_tts.Communicate(SCRIPT, VOICE, rate="-15%")
    await communicate.save("family-chants.mp3")
    print("OK family-chants.mp3")

if __name__ == "__main__":
    asyncio.run(main())
