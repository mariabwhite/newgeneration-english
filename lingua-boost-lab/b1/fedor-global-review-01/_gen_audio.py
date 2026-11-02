"""Generate 8 micro-listening clips for Fedya global review Lab.
Uses edge-tts. Retries on 403 (Microsoft token rotation).
"""
import asyncio, os, sys, time
import edge_tts

OUT = os.path.join(os.path.dirname(__file__), "assets", "audio")
os.makedirs(OUT, exist_ok=True)

CLIPS = [
    ("china-travel-plans", "en-GB-RyanNeural",
     "This is Fedya. He is so excited. In two weeks his family is going to Beijing for ten days. They are going to stay in a hotel near the Forbidden City. Fedya will probably try all the street food. He loves dumplings! His dad says they might also visit the Great Wall. Fedya will start packing tomorrow."),
    ("china-first-day", "en-GB-RyanNeural",
     "Yesterday was Fedya's first day in Beijing. He and his parents arrived at the airport in the morning and took a taxi to the hotel. In the afternoon they walked around the Forbidden City. It was beautiful. For dinner they had Peking duck in a little restaurant. Fedya bought two postcards for his grandma."),
    ("china-hotel-room", "en-GB-RyanNeural",
     "Right now Fedya is sitting in his hotel room in Beijing. His mum is unpacking her suitcase. His dad is calling the reception to ask about the swimming pool. Fedya is looking out of the window. He can see the Forbidden City and some old buildings with red roofs. He thinks it's amazing."),
    ("china-airport", "en-GB-RyanNeural",
     "Good evening, sir. Welcome to Beijing. May I see your passport, please? Thank you. Could you tell me the purpose of your visit? OK, tourism. And how long are you staying in China? Ten days. Perfect, enjoy your trip."),
    ("china-taxi", "en-GB-SoniaNeural",
     "Hi! Where are you going? Beijing Hotel? OK, no problem. It's about forty minutes by car. The price is one hundred eighty yuan. Would you like me to turn on the air conditioning? Great. Please put on your seatbelt. We are leaving."),
    ("china-hotel", "en-GB-RyanNeural",
     "Good evening and welcome to the Beijing Hotel. Do you have a reservation? Protasov, let me check. Yes, I've got you here. A double room on the fifth floor for three nights. Breakfast is served from seven to ten a m, on the second floor. Is there anything else you need?"),
    ("china-restaurant", "en-GB-SoniaNeural",
     "Hi there! Welcome to our noodle shop. Here's the menu. Would you like something to drink first? Water with no ice, OK. Our bestseller is the beef noodle soup. It is quite spicy though. Do you want it spicy or mild? Mild, got it. Any food allergies I should know about?"),
    ("china-directions", "en-GB-RyanNeural",
     "Excuse me, I'm looking for the Forbidden City. Am I going the right way? Oh, you need to turn around. Walk back to the big crossroad, then turn left. The entrance is about ten minutes on foot. Watch out for the bikes. They come very fast. Good luck!"),
]

async def one(slug, voice, text, attempt=1):
    path = os.path.join(OUT, f"{slug}.mp3")
    try:
        comm = edge_tts.Communicate(text, voice, rate="-5%")
        await comm.save(path)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        if size < 1000:
            raise Exception(f"empty file ({size} bytes)")
        print(f"OK  {slug}.mp3  {size} bytes  ({voice})")
        return True
    except Exception as e:
        print(f"ERR {slug}.mp3 attempt {attempt} :: {e}")
        if attempt < 3:
            await asyncio.sleep(5)
            return await one(slug, voice, text, attempt+1)
        return False

async def main():
    # sequential to avoid 403 bursts
    for slug, voice, text in CLIPS:
        if os.path.exists(os.path.join(OUT, f"{slug}.mp3")) and os.path.getsize(os.path.join(OUT, f"{slug}.mp3")) > 1000:
            print(f"SKIP {slug}.mp3 (already exists)")
            continue
        await one(slug, voice, text)
        await asyncio.sleep(0.4)
    print(f"\nDone. OUT = {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
