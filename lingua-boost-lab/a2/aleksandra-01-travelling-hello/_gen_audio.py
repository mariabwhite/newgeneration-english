"""Generate all MP3 audio files for Aleksandra L1 Travelling lesson.
Windows-safe (utf-8 stdout, no crashes on em-dash / non-ASCII).
Run: python _gen_audio.py
"""
import sys, asyncio, pathlib
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

VOICE_F = "en-US-AriaNeural"   # Sasha, receptionist, narration
VOICE_M = "en-US-GuyNeural"    # Marco, seatmate, other male guests

# id -> (text, voice_key)
PHRASES = {
    # ─── Section 1 · Greetings ────────────────────────────────
    "gr-01": ("Hi.", "f"),
    "gr-02": ("Hello.", "f"),
    "gr-03": ("Good morning.", "f"),
    "gr-04": ("Good afternoon.", "f"),
    "gr-05": ("Good evening.", "f"),
    "gr-06": ("How are you?", "f"),
    "gr-07": ("I'm fine, thanks. And you?", "f"),
    "gr-08": ("Nice to meet you.", "f"),

    # ─── Section 2 · Name ─────────────────────────────────────
    "nm-01": ("My name is Aleksandra.", "f"),
    "nm-02": ("I'm Aleksandra.", "f"),
    "nm-03": ("What's your name?", "f"),
    "nm-04": ("You can call me Sasha.", "f"),
    "nm-05": ("Nice to meet you too.", "f"),
    "nm-06": ("Sorry, could you say that again?", "f"),
    "nm-07": ("Sorry, what's your name?", "f"),
    "nm-08": ("I didn't catch your name.", "f"),

    # ─── Section 3 · Where from ───────────────────────────────
    "fr-01": ("Where are you from?", "f"),
    "fr-02": ("I'm from Russia.", "f"),
    "fr-03": ("I'm Russian.", "f"),
    "fr-04": ("I live in Moscow.", "f"),
    "fr-05": ("I'm Russian, but I live in Berlin now.", "f"),
    "fr-06": ("How about you?", "f"),
    "fr-07": ("And you?", "f"),
    "fr-08": ("Whereabouts?", "f"),
    # country-nationality pairs
    "cn-ru": ("Russia. Russian.", "f"),
    "cn-it": ("Italy. Italian.", "f"),
    "cn-de": ("Germany. German.", "f"),
    "cn-fr": ("France. French.", "f"),
    "cn-es": ("Spain. Spanish.", "f"),
    "cn-tr": ("Turkey. Turkish.", "f"),
    "cn-cn": ("China. Chinese.", "f"),
    "cn-jp": ("Japan. Japanese.", "f"),
    "cn-uk": ("The United Kingdom. British.", "f"),
    "cn-us": ("The United States. American.", "f"),
    "cn-br": ("Brazil. Brazilian.", "f"),
    "cn-in": ("India. Indian.", "f"),

    # ─── Section 4 · Job ──────────────────────────────────────
    "jb-01": ("What do you do?", "f"),
    "jb-02": ("I'm a designer.", "f"),
    "jb-03": ("I work in marketing.", "f"),
    "jb-04": ("I work as a manager at Yandex.", "f"),
    "jb-05": ("I'm a student.", "f"),
    "jb-06": ("I'm retired.", "f"),
    "jb-07": ("I'm on maternity leave.", "f"),
    "jb-08": ("I'm self-employed.", "f"),
    # job words
    "j-teacher": ("A teacher.", "f"),
    "j-doctor": ("A doctor.", "f"),
    "j-designer": ("A designer.", "f"),
    "j-lawyer": ("A lawyer.", "f"),
    "j-engineer": ("An engineer.", "f"),
    "j-manager": ("A manager.", "f"),
    "j-translator": ("A translator.", "f"),
    "j-student": ("A student.", "f"),
    "j-writer": ("A writer.", "f"),
    "j-accountant": ("An accountant.", "f"),
    "j-nurse": ("A nurse.", "f"),
    "j-architect": ("An architect.", "f"),

    # ─── Section 5 · Dialogues ────────────────────────────────
    # Scene 1 · Hotel check-in Barcelona
    "d1-01r": ("Good afternoon! Do you have a reservation?", "f"),
    "d1-01y": ("Yes, hello. My name is Aleksandra Lyubaeva. I have a booking for two nights.", "f"),
    "d1-02r": ("Lovely. Could I see your passport, please?", "f"),
    "d1-02y": ("Here you are.", "f"),
    "d1-03r": ("Thank you. And where are you from, Miss Lyubaeva?", "f"),
    "d1-03y": ("I'm from Russia. I live in Moscow.", "f"),
    "d1-04r": ("Enjoy your stay!", "f"),

    # Scene 2 · Plane seatmate
    "d2-01n": ("Hi. Are you flying to Istanbul for work or pleasure?", "m"),
    "d2-01y": ("Just for a short holiday. How about you?", "f"),
    "d2-02n": ("I'm going home. I live there. What do you do?", "m"),
    "d2-02y": ("I'm a designer. I work at a small studio.", "f"),
    "d2-03n": ("Nice. Is this your first time in Istanbul?", "m"),
    "d2-03y": ("Yes, it is. Do you have any tips?", "f"),

    # Scene 3 · Breakfast, meeting Marco
    "d3-01m": ("Good morning. Is this seat free?", "m"),
    "d3-01y": ("Yes, please. Have a seat.", "f"),
    "d3-02m": ("Thank you. I'm Marco, by the way.", "m"),
    "d3-02y": ("Nice to meet you, Marco. I'm Aleksandra — you can call me Sasha.", "f"),
    "d3-03m": ("Where are you from, Sasha?", "m"),
    "d3-03y": ("I'm from Russia. And you?", "f"),
    "d3-04m": ("Italy — Milan. What do you do back home?", "m"),
    "d3-04y": ("I'm a designer. What about you?", "f"),

    # ─── Section 6 · Reading ──────────────────────────────────
    "rd-full": ("Marco is thirty-five. He is Italian and he lives in Milan. He is a photographer. He is in Rome for a two-day meeting. In the lobby he meets Sasha. Sasha is from Russia. She lives in Moscow and she works in marketing at a small company. She is in Rome on holiday with a friend. They talk for ten minutes about the weather, the coffee and the traffic. Marco recommends a small restaurant near the Pantheon. Sasha thanks him and writes down the name.", "f"),

    # ─── Section 7 · Speaking prompts ─────────────────────────
    "sp-01": ("What's your name?", "f"),
    "sp-02": ("Where are you from?", "f"),
    "sp-03": ("Where do you live now?", "f"),
    "sp-04": ("What do you do?", "f"),
    "sp-05": ("Do you like your job?", "f"),
    "sp-06": ("How often do you travel?", "f"),
    "sp-07": ("What's your favourite country?", "f"),
    "sp-08": ("Why are you learning English?", "f"),
    # Fix-the-lie provocation
    "sp-fl": ("So, you're a doctor from Saint Petersburg, right?", "f"),

    # ─── Section 8 · Present Simple basics ────────────────────
    # positive
    "ps-01": ("I travel a lot for work.", "f"),
    "ps-02": ("You speak English very well.", "f"),
    "ps-03": ("We fly to Turkey every summer.", "f"),
    "ps-04": ("She travels every summer.", "f"),
    "ps-05": ("He lives in Milan.", "f"),
    "ps-06": ("The hotel opens at seven.", "f"),
    # negative
    "ps-07": ("I don't fly often.", "f"),
    "ps-08": ("He doesn't like airports.", "f"),
    "ps-09": ("We don't stay in hostels.", "f"),
    # questions · travelling
    "psq-01": ("Do you travel often?", "f"),
    "psq-02": ("Where do you usually go on holiday?", "f"),
    "psq-03": ("Do you prefer the beach or the mountains?", "f"),
    "psq-04": ("How do you get to the airport?", "f"),
    "psq-05": ("Do you speak any other languages?", "f"),
    "psq-06": ("Does your family travel with you?", "f"),
    "psq-07": ("Do you like flying?", "f"),
    "psq-08": ("How long does the flight to Turkey take?", "f"),
    "psq-09": ("Where do you stay when you travel?", "f"),
    "psq-10": ("Do you take a lot of photos when you travel?", "f"),
}

async def gen_one(aid: str, text: str, vkey: str, out_dir: pathlib.Path):
    voice = VOICE_F if vkey == "f" else VOICE_M
    dest = out_dir / f"{aid}.mp3"
    if dest.exists() and dest.stat().st_size > 500:
        print(f"  skip  {aid}  (exists)")
        return
    tts = edge_tts.Communicate(text=text, voice=voice, rate="-8%")
    await tts.save(str(dest))
    print(f"  ok    {aid}  {voice}  \"{text[:60]}{'…' if len(text)>60 else ''}\"")

async def main():
    out_dir = pathlib.Path(__file__).parent / "assets" / "audio"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"→ {out_dir}")
    print(f"→ {len(PHRASES)} phrases")
    for aid, (text, vkey) in PHRASES.items():
        try:
            await gen_one(aid, text, vkey, out_dir)
        except Exception as e:
            print(f"  ERR   {aid}  {e}")
    print("done.")

if __name__ == "__main__":
    asyncio.run(main())
