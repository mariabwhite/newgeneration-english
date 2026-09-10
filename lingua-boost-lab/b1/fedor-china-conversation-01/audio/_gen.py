#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Edge-TTS audio generator for fedor-china-conversation-01.

Generates MP3 files for:
  - vocab pronunciations (24)
  - immigration role-play lines (12)
  - hotel role-play lines (12)
  - taxi gap-scene full read (1)
  - restaurant gap-scene full read (1)
  - listening stories (3)
  - prompt-card data-say (13)

Voices (British):
  - Sonia (en-GB-SoniaNeural)  = female / student / Emma role
  - Ryan  (en-GB-RyanNeural)   = male   / officer / driver / waiter
"""
import sys, os, asyncio, edge_tts

# Windows console UTF-8 (per lab _gen.py convention)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

VOICE_F = "en-GB-SoniaNeural"
VOICE_M = "en-GB-RyanNeural"

HERE = os.path.dirname(os.path.abspath(__file__))

def slug(s):
    s = s.lower().replace("'", "").replace(",", "").replace(".", "")
    s = s.replace("/", "-").replace(" ", "-")
    s = "".join(c for c in s if c.isalnum() or c == "-")
    return s[:40]

# ---------- 1 · VOCAB (24) ----------
VOCAB = [
    ("boarding-pass",   "boarding pass"),
    ("immigration",     "immigration"),
    ("customs",         "customs"),
    ("to-declare",      "to declare"),
    ("return-ticket",   "a return ticket"),
    ("to-stay-at",      "to stay at"),
    ("purpose",         "a purpose"),
    ("taxi-rank",       "a taxi rank"),
    ("ride-hailing",    "a ride-hailing app"),
    ("qr-code",         "a QR code"),
    ("subway",          "a subway"),
    ("check-in",        "to check in"),
    ("reservation",     "a reservation"),
    ("key-card",        "a key card"),
    ("to-order",        "to order"),
    ("spicy",           "spicy"),
    ("allergic-to",     "to be allergic to"),
    ("menu",            "a menu"),
    ("bill",            "the bill"),
    ("to-bargain",      "to bargain"),
    ("expensive",       "expensive"),
    ("receipt",         "a receipt"),
    ("lost",            "lost"),
    ("embassy",         "an embassy"),
]

# ---------- 2 · IMMIGRATION ROLE-PLAY (12) ----------
IMMIGRATION = [
    ("officer-01", VOICE_M, "Passport, please."),
    ("officer-02", VOICE_M, "Purpose of your visit?"),
    ("officer-03", VOICE_M, "How long are you staying?"),
    ("officer-04", VOICE_M, "Where are you staying?"),
    ("officer-05", VOICE_M, "Do you have a return ticket?"),
    ("officer-06", VOICE_M, "Enjoy your stay in China."),
    ("student-01", VOICE_F, "Here you are."),
    ("student-02", VOICE_F, "The purpose of my visit is tourism."),
    ("student-03", VOICE_F, "I'm staying for ten days."),
    ("student-04", VOICE_F, "I'm staying at the Grand Beijing Hotel in Chaoyang."),
    ("student-05", VOICE_F, "Yes, my return flight is on the twentieth of October."),
    ("student-06", VOICE_F, "Thank you very much!"),
]

# ---------- 3 · HOTEL ROLE-PLAY (12) ----------
HOTEL = [
    ("reception-01", VOICE_F, "Good evening. Welcome to the Grand Beijing."),
    ("reception-02", VOICE_F, "Do you have a reservation?"),
    ("reception-03", VOICE_F, "Could I see your passport, please?"),
    ("reception-04", VOICE_F, "One twin room for four nights. Correct?"),
    ("reception-05", VOICE_F, "Breakfast is included, from seven to ten in the restaurant on floor two."),
    ("reception-06", VOICE_F, "Here is your key card. Room 508, on the fifth floor. Enjoy your stay!"),
    ("guest-01", VOICE_M, "Good evening. Thank you."),
    ("guest-02", VOICE_M, "Yes, I have a reservation under Protasov."),
    ("guest-03", VOICE_M, "Of course. Here you are."),
    ("guest-04", VOICE_M, "Yes, that's right — one twin room for four nights."),
    ("guest-05", VOICE_M, "Great, thank you. And what's the Wi-Fi password, please?"),
    ("guest-06", VOICE_M, "Thank you very much. Have a good evening!"),
]

# ---------- 4 · GAP-SCENE · TAXI (full read) ----------
SCENE_TAXI_LINES = [
    (VOICE_F, "You: Excuse me, to this address, please."),
    (VOICE_M, "Driver: OK. Get in."),
    (VOICE_F, "You: How much is it, more or less?"),
    (VOICE_M, "Driver: Around eighty yuan."),
    (VOICE_F, "You: Could you turn on the meter, please?"),
    (VOICE_M, "Driver: Yes, yes."),
    (VOICE_F, "You: Stop here, please. Can I pay by WeChat?"),
    (VOICE_M, "Driver: Sure, scan the QR code."),
    (VOICE_F, "You: Thank you. Could I get a receipt?"),
]

# ---------- 5 · GAP-SCENE · RESTAURANT (full read) ----------
SCENE_REST_LINES = [
    (VOICE_F, "You: Excuse me, could I see the menu with pictures, please?"),
    (VOICE_M, "Waiter: Sure, one moment."),
    (VOICE_F, "You: What do you recommend for a first-timer?"),
    (VOICE_M, "Waiter: The beef noodles are famous here. A bit hot."),
    (VOICE_F, "You: OK, but not too spicy, please. I'm allergic to peanuts."),
    (VOICE_M, "Waiter: No peanuts, understood. Anything to drink?"),
    (VOICE_F, "You: Water, please. Not hot."),
    (VOICE_F, "You: Everything was great! Could I have the bill, please?"),
    (VOICE_M, "Waiter: Sure. Card or WeChat?"),
    (VOICE_F, "You: WeChat, please."),
]

# ---------- 6 · LISTENING STORIES (3) ----------
LISTENING = [
    ("story-01-airport-announcement", VOICE_F,
     "Attention please, passengers of flight CA nine two eight to Moscow. "
     "Your flight is now boarding at gate B seventeen. "
     "The gate will close at eleven twenty. "
     "Please have your boarding pass and passport ready. "
     "Passengers travelling with children can board first."),
    ("story-02-hotel-check-in", VOICE_M,
     "Good afternoon, sir. I'm afraid your reservation is for tomorrow, not for today. "
     "But you're lucky. We do have one room available tonight. "
     "It is a bit smaller than the one you booked, and it is on the second floor, not on the fifth. "
     "The price is the same. Would you like to take it?"),
    ("story-03-street-directions", VOICE_F,
     "Excuse me, are you lost? "
     "You want the subway? OK, so you go straight along this street for about two minutes. "
     "You will see a big red sign on your left. "
     "Turn left there, and the metro entrance is right there, next to a coffee shop. "
     "It's called exit C. Don't take exit A, it's on the other side of the road."),
]

# ---------- 7 · PROMPT CARDS (13 data-say) ----------
PROMPTS = [
    ("prompt-01-where-china",     VOICE_F, "Where in China are you flying, and for how many days?"),
    ("prompt-02-afraid",          VOICE_F, "What are you a little afraid of on this trip?"),
    ("prompt-03-chinese-say",     VOICE_F, "One thing you already know how to say in Chinese. Say it now."),
    ("prompt-04-where-from",      VOICE_M, "Where are you from originally?"),
    ("prompt-05-dish-try",        VOICE_M, "What is a dish I really must try here?"),
    ("prompt-06-thank-you",       VOICE_M, "How do you say thank you in your language?"),
    ("prompt-07-first-time",      VOICE_M, "Is this your first time in this city too?"),
    ("prompt-08-sports",          VOICE_M, "Do you play football, basketball or video games?"),
    ("prompt-09-metro",           VOICE_M, "How do I get to the metro from here?"),
]


async def _one(voice, text, out):
    if os.path.exists(out) and os.path.getsize(out) > 500:
        print(f"skip {os.path.basename(out)}")
        return
    comm = edge_tts.Communicate(text, voice=voice, rate="-8%")
    await comm.save(out)
    size = os.path.getsize(out)
    print(f"ok   {os.path.basename(out)}  ({size} B)")


async def main():
    # Directories
    for sub in ("vocab", "roleplay-immigration", "roleplay-hotel",
                "scene", "listening", "prompt"):
        os.makedirs(os.path.join(HERE, sub), exist_ok=True)

    tasks = []
    # vocab
    for key, phrase in VOCAB:
        out = os.path.join(HERE, "vocab", f"{slug(key)}.mp3")
        tasks.append(_one(VOICE_F, phrase, out))
    # immigration
    for key, v, txt in IMMIGRATION:
        out = os.path.join(HERE, "roleplay-immigration", f"{key}.mp3")
        tasks.append(_one(v, txt, out))
    # hotel
    for key, v, txt in HOTEL:
        out = os.path.join(HERE, "roleplay-hotel", f"{key}.mp3")
        tasks.append(_one(v, txt, out))
    # scenes — one MP3 per full scene, concatenated at TTS-level per line
    #   easier: one file per line inside scene subfolder
    for i, (v, txt) in enumerate(SCENE_TAXI_LINES, 1):
        out = os.path.join(HERE, "scene", f"taxi-{i:02d}.mp3")
        tasks.append(_one(v, txt, out))
    for i, (v, txt) in enumerate(SCENE_REST_LINES, 1):
        out = os.path.join(HERE, "scene", f"restaurant-{i:02d}.mp3")
        tasks.append(_one(v, txt, out))
    # listening
    for key, v, txt in LISTENING:
        out = os.path.join(HERE, "listening", f"{key}.mp3")
        tasks.append(_one(v, txt, out))
    # prompts
    for key, v, txt in PROMPTS:
        out = os.path.join(HERE, "prompt", f"{key}.mp3")
        tasks.append(_one(v, txt, out))

    # Run sequentially (edge-tts is fine with small concurrency, keep it safe on Windows)
    for i in range(0, len(tasks), 6):
        await asyncio.gather(*tasks[i:i+6])

    print(f"\nDONE · {len(tasks)} clips.")


if __name__ == "__main__":
    asyncio.run(main())
