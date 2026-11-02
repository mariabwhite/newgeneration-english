"""Generate reading audio for anya-05-dawn-observatory via edge-tts.
Retry on 403 (Microsoft token rotation)."""
import asyncio, os, sys, time
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "audio")
os.makedirs(OUT, exist_ok=True)

VOICE = "en-US-AriaNeural"  # female, clear
RATE = "-5%"

READING = (
    "At six in the morning Anya and grandma walk up the hill. "
    "The sea is pink. The air is cold. "
    "Today you will see the future, grandma says. "
    "A wooden observatory stands on the cliff. The door creaks. "
    "Five brass telescopes shine in the first sunlight. "
    "Look through Telescope One. Tell me what you will do today. "
    "Anya looks. I will call Masha. I will drink hot tea. I will finish my book. "
    "Telescope Two is longer. What are you going to study at university? "
    "Anya sees her future self with a camera. "
    "I am going to be a nature photographer. "
    "Telescope Three is small. What are you doing tomorrow? "
    "I am meeting my cousin at four. We are flying to Bergen on Friday. "
    "Telescope Four points at the harbour. "
    "The ferry leaves at seven fifteen every morning, grandma reads from the schedule. "
    "The sun rises at six forty-two tomorrow. "
    "Telescope Five is golden. "
    "By twenty forty you will have travelled to twenty countries, grandma whispers. "
    "By the time you are thirty you will have learned three languages. "
    "The sun climbs. The horizon turns orange. "
    "Future is a direction, grandma says, not a mystery. "
    "When you come here next year, I will give you the keys."
)

CLIP1 = (
    "Tomorrow is going to be a busy day. "
    "I am going to bake an apple pie in the morning. "
    "Then I am meeting Anya at the station at four. "
    "We are flying to Oslo on Friday to visit her aunt. "
    "I have already packed the suitcases."
)
CLIP2 = (
    "Attention please. "
    "The train to Bergen leaves at seven fifteen from platform three. "
    "The ferry to Trondheim departs at nine o'clock sharp. "
    "The bus to the airport arrives at the station every twenty minutes. "
    "Please check the screens for your departure."
)
CLIP3 = (
    "I will tell you about your future, child. "
    "By twenty thirty you will have finished school. "
    "You will speak three languages fluently. "
    "In twenty thirty-two you will move to a city by the sea. "
    "By the time you are twenty-five, you will have travelled to ten countries. "
    "And one day you will come back to this observatory as a teacher."
)

CLIPS = [
    ("reading-dawn-observatory", READING, VOICE, "-5%"),
    ("listen-clip1-grandma",       CLIP1, "en-US-JennyNeural",  "-5%"),
    ("listen-clip2-station",       CLIP2, "en-GB-RyanNeural",   "-3%"),
    ("listen-clip3-crystal",       CLIP3, "en-GB-SoniaNeural",  "-8%"),
]

async def one(name, text, voice, rate):
    path = os.path.join(OUT, name + ".mp3")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"[skip] {name}.mp3 exists")
        return
    for attempt in range(5):
        try:
            c = edge_tts.Communicate(text, voice, rate=rate)
            await c.save(path)
            sz = os.path.getsize(path)
            if sz < 1000:
                raise Exception(f"0/empty file ({sz}b)")
            print(f"[ok] {name}.mp3 {sz:,}b")
            return
        except Exception as e:
            print(f"[retry {attempt+1}] {name}: {e}")
            if os.path.exists(path):
                os.remove(path)
            await asyncio.sleep(5)
    print(f"[FAIL] {name}")

async def main():
    for args in CLIPS:
        await one(*args)

asyncio.run(main())
print("done.")
