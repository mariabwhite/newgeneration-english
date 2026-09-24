"""Generate all MP3 audio files for Aleksandra L2 — First day in Rome.
Windows-safe (utf-8 stdout; rate=-3% to avoid WinError 1455 on long clips).
Run: python _gen_audio.py

NOTE: assets/audio/ currently contains LEFTOVER mp3s copied from L1
(gr-*, nm-*, fr-*, cn-*, jb-*, d1-*, d2-*, d3-*, ps-*, psq-*, sp-06..sp-08,
sp-fl, j-*). Those IDs are NOT referenced by L2's index.html. Safe to delete.

Colliding IDs (sp-01..sp-05, rd-full) exist with WRONG L1 text — delete them
before running so this script re-generates them with L2 content.
"""
import sys, asyncio, pathlib
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

# ─── Voice roster ──────────────────────────────────────────────
VOICE_SASHA    = "en-GB-SoniaNeural"   # Sasha "you" lines + narration + numbers/vocab
VOICE_M        = "en-US-GuyNeural"     # Barista / Marco / male stranger
VOICE_GIULIA   = "en-US-JennyNeural"   # Giulia / female stranger
VOICE_NARRATOR = "en-GB-SoniaNeural"   # rd-full postcard reading

# id -> (voice, text)
CLIPS = {
    # ─── Section 1 · Warm-up recall ──────────────────────────────
    "sp-01": (VOICE_SASHA, "Good morning."),
    "sp-02": (VOICE_SASHA, "My name is Aleksandra. You can call me Sasha."),
    "sp-03": (VOICE_SASHA, "I'm from Russia. I live in Moscow."),
    "sp-04": (VOICE_SASHA, "I work in marketing at a small company."),
    "sp-05": (VOICE_SASHA, "I drink coffee every morning."),

    # ─── Section 2 · Café menu + polite orders ───────────────────
    "cafe-01": (VOICE_SASHA, "Espresso — one euro fifty."),
    "cafe-02": (VOICE_SASHA, "Cappuccino — two euros twenty."),
    "cafe-03": (VOICE_SASHA, "Croissant — one euro eighty."),
    "cafe-04": (VOICE_SASHA, "Pasta — twelve euros."),
    "cafe-05": (VOICE_SASHA, "Tiramisu — five euros fifty."),
    "cafe-06": (VOICE_SASHA, "Bottle of water — one euro."),
    "cafe-07": (VOICE_SASHA, "Could I have a cappuccino, please?"),
    "cafe-08": (VOICE_SASHA, "I'd like a croissant."),

    # ─── Section 3 · Directions vocab (flashcards + phrases) ─────
    "dir-01": (VOICE_SASHA, "At the corner, turn left."),
    "dir-02": (VOICE_SASHA, "Turn right after the fountain."),
    "dir-03": (VOICE_SASHA, "Go straight for two blocks."),
    "dir-04": (VOICE_SASHA, "The café is near the Pantheon."),
    "dir-05": (VOICE_SASHA, "The shop is next to the bakery."),
    "dir-06": (VOICE_SASHA, "The hotel is opposite the church."),
    "dir-07": (VOICE_SASHA, "The parking is behind the museum."),
    "dir-08": (VOICE_SASHA, "Meet me in front of the fountain."),
    "dir-09": (VOICE_SASHA, "Excuse me, where is the Trevi Fountain?"),
    "dir-10": (VOICE_SASHA, "How do I get to the Pantheon?"),
    "dir-11": (VOICE_SASHA, "Is it far?"),
    "dir-12": (VOICE_SASHA, "It's five minutes on foot."),
    # dictation targets
    "dir-13": (VOICE_SASHA, "Turn right, then go straight."),
    "dir-14": (VOICE_SASHA, "It's opposite the church."),

    # ─── Section 4 · Numbers + price ─────────────────────────────
    "num-01": (VOICE_SASHA, "One."),
    "num-02": (VOICE_SASHA, "Two."),
    "num-03": (VOICE_SASHA, "Three."),
    "num-04": (VOICE_SASHA, "Four."),
    "num-05": (VOICE_SASHA, "Five."),
    "num-06": (VOICE_SASHA, "Six."),
    "num-07": (VOICE_SASHA, "Seven."),
    "num-08": (VOICE_SASHA, "Eight."),
    "num-09": (VOICE_SASHA, "Nine."),
    "num-10": (VOICE_SASHA, "Ten."),
    "num-11": (VOICE_SASHA, "Twenty."),
    "num-12": (VOICE_SASHA, "Thirty."),
    "num-13": (VOICE_SASHA, "Forty."),
    "num-14": (VOICE_SASHA, "Fifty."),
    "num-15": (VOICE_SASHA, "Sixty."),
    "num-16": (VOICE_SASHA, "Seventy."),
    "num-17": (VOICE_SASHA, "Eighty."),
    "num-18": (VOICE_SASHA, "Ninety."),
    "num-19": (VOICE_SASHA, "One hundred."),
    "num-20": (VOICE_SASHA, "Four euros fifty."),

    # ─── Section 5 · Scene 1 · Café (Barista + Sasha) ────────────
    "s5-1-01": (VOICE_M,     "Good morning! What can I get you?"),
    "s5-1-02": (VOICE_SASHA, "Good morning. Could I have a cappuccino and a croissant, please?"),
    "s5-1-03": (VOICE_M,     "Of course. Anything else?"),
    "s5-1-04": (VOICE_SASHA, "No, that's all, thank you. How much is it?"),
    "s5-1-05": (VOICE_M,     "Four euros, please."),
    "s5-1-06": (VOICE_SASHA, "Here you are. Grazie mille!"),
    "s5-1-07": (VOICE_M,     "Prego! Enjoy your day."),

    # ─── Section 5 · Scene 2 · Directions (male stranger) ────────
    "s5-2-01": (VOICE_SASHA, "Excuse me, where is the Trevi Fountain?"),
    "s5-2-02": (VOICE_M,     "Go straight for two minutes, then turn right at the little church."),
    "s5-2-03": (VOICE_SASHA, "Turn right at the church. Is it far?"),
    "s5-2-04": (VOICE_M,     "No, it's very close. Five minutes on foot — you'll see it on your left."),
    "s5-2-05": (VOICE_SASHA, "Thanks a lot!"),
    "s5-2-06": (VOICE_M,     "You're welcome. Have a nice day."),

    # ─── Section 5 · Scene 3 · Shop (Giulia + Sasha) ─────────────
    "s5-3-01": (VOICE_GIULIA, "Hello! Are you looking for something in particular?"),
    "s5-3-02": (VOICE_SASHA,  "Yes, I'd like a small notebook — leather, if you have one."),
    "s5-3-03": (VOICE_GIULIA, "Of course. This one is handmade in Florence. Where are you from?"),
    "s5-3-04": (VOICE_SASHA,  "I'm from Russia. I live in Moscow. It's beautiful — how much is it?"),
    "s5-3-05": (VOICE_GIULIA, "Eighteen euros. And what do you do in Moscow?"),
    "s5-3-06": (VOICE_SASHA,  "I work in marketing at a small company. I'll take the notebook — thank you."),
    "s5-3-07": (VOICE_GIULIA, "Wonderful. Enjoy your stay in Rome!"),

    # ─── Section 6 · Reading · Postcard to Nastya ────────────────
    "rd-full": (VOICE_NARRATOR,
        "Ciao, Nastya! Rome is amazing. This morning I drink a cappuccino near "
        "the Pantheon — one euro fifty, and it is the best coffee in my life. "
        "I walk to the Trevi Fountain, but I get lost, and a friendly man shows "
        "me the way. I buy a small leather notebook in a shop and I speak "
        "English with the shop assistant Giulia. She is very nice. This evening "
        "I meet Marco again — the photographer from the hotel breakfast — for "
        "aperitivo at seven. Tomorrow we go to the Colosseum. Miss you! "
        "Kisses, Sasha."),

    # ─── Section 7 · Speaking role-play prompts ──────────────────
    "sp7-01": (VOICE_SASHA, "You're at the café. Order a coffee and a croissant. Target: Could I have…"),
    "sp7-02": (VOICE_SASHA, "Stop a stranger and ask the way to the museum. Target: Excuse me, where is…"),
    "sp7-03": (VOICE_SASHA, "Tell a new person your name, where you're from, and what you do. Three sentences."),
    "sp7-04": (VOICE_SASHA, "In a shop: ask How much is it? and negotiate — say it's too expensive."),
    "sp7-05": (VOICE_SASHA, "Aperitivo with Marco: ask him three Do you? or Where do you? questions."),
    "sp7-06": (VOICE_SASHA, "Sixty-second monologue: My first day in Rome — use five phrases from Sections two to six."),
}


async def gen_one(aid: str, voice: str, text: str, out_dir: pathlib.Path):
    dest = out_dir / f"{aid}.mp3"
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"  skip  {aid:<10}  (exists, {dest.stat().st_size} bytes)")
        return
    tts = edge_tts.Communicate(text=text, voice=voice, rate="-3%")
    await tts.save(str(dest))
    preview = text[:60] + ("…" if len(text) > 60 else "")
    print(f"  ok    {aid:<10}  {voice:<22}  \"{preview}\"")


async def main():
    out_dir = pathlib.Path(__file__).parent / "assets" / "audio"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"→ {out_dir}")
    print(f"→ {len(CLIPS)} clips to process")
    fails = 0
    for aid, (voice, text) in CLIPS.items():
        try:
            await gen_one(aid, voice, text, out_dir)
        except Exception as e:
            print(f"  FAIL  {aid}  {e}")
            fails += 1
    print(f"done. {len(CLIPS)} total, {fails} failed.")


if __name__ == "__main__":
    asyncio.run(main())
