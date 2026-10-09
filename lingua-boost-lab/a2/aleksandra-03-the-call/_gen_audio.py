"""Generate all MP3 audio files for Aleksandra L3 · The Call · Herceg Novi.
Windows-safe (utf-8 stdout, no crashes on em-dash / non-ASCII).
Run: python _gen_audio.py
"""
import sys, asyncio, pathlib
sys.stdout.reconfigure(encoding='utf-8')

import edge_tts

VOICE_SASHA = "en-GB-SoniaNeural"   # Sasha (female British)
VOICE_M     = "en-US-GuyNeural"     # Marco / barista / stranger (male)
VOICE_F     = "en-US-JennyNeural"   # other female voices if needed

# id -> (text, voice_key)   voice_key: s / m / f
PHRASES = {
    # ─── S1 · Warm-up recall ──────────────────────────────────
    "sp-01": ("Good morning.", "s"),
    "sp-02": ("My name is Aleksandra. You can call me Sasha.", "s"),
    "sp-03": ("I'm from Russia. I'm in Paris this week.", "s"),
    "sp-04": ("I work in marketing at a small company.", "s"),
    "sp-05": ("I drink coffee every morning.", "s"),

    # ─── S2 · Café menu + polite orders + Wi-Fi ──────────────
    "cafe-01": ("Espresso — one euro fifty.", "s"),
    "cafe-02": ("Cappuccino — two euros twenty.", "s"),
    "cafe-03": ("Croissant — one euro eighty.", "s"),
    "cafe-04": ("Pasta — twelve euros.", "s"),
    "cafe-05": ("Tiramisu — five euros fifty.", "s"),
    "cafe-06": ("Bottle of water — one euro.", "s"),
    "cafe-07": ("Could I have a cappuccino, please?", "s"),
    "cafe-08": ("I'd like a croissant.", "s"),
    "cafe-09": ("Could I have the Wi-Fi password, please?", "s"),
    "cafe-10": ("Is there Wi-Fi here?", "s"),

    # ─── S3 · Directions ─────────────────────────────────────
    "dir-01": ("At the corner, turn left.", "s"),
    "dir-02": ("Turn right after the fountain.", "s"),
    "dir-03": ("Go straight for two blocks.", "s"),
    "dir-04": ("The café is near the Old Town gate.", "s"),
    "dir-05": ("The SIM-card shop is next to the bakery.", "s"),
    "dir-06": ("The pharmacy is opposite the church.", "s"),
    "dir-07": ("The parking is behind the market.", "s"),
    "dir-08": ("Meet me in front of the fountain.", "s"),
    "dir-09": ("Excuse me, where is the SIM-card shop?", "s"),
    "dir-10": ("How do I get to the Old Town?", "s"),
    "dir-11": ("Is it far?", "s"),
    "dir-12": ("It's five minutes on foot.", "s"),
    "dir-13": ("Turn right, then go straight.", "s"),
    "dir-14": ("It's opposite the church.", "s"),

    # ─── S4 · Numbers + time + prices ────────────────────────
    "num-01": ("One.", "s"),
    "num-02": ("Two.", "s"),
    "num-03": ("Three.", "s"),
    "num-04": ("Four.", "s"),
    "num-05": ("Five.", "s"),
    "num-06": ("Six.", "s"),
    "num-07": ("Seven.", "s"),
    "num-08": ("Eight.", "s"),
    "num-09": ("Nine.", "s"),
    "num-10": ("Ten.", "s"),
    "num-11": ("Twenty.", "s"),
    "num-12": ("Thirty.", "s"),
    "num-13": ("Forty.", "s"),
    "num-14": ("Fifty.", "s"),
    "num-15": ("Sixty.", "s"),
    "num-16": ("Seventy.", "s"),
    "num-17": ("Eighty.", "s"),
    "num-18": ("Ninety.", "s"),
    "num-19": ("One hundred.", "s"),
    "num-20": ("Four euros fifty.", "s"),
    "tm-01":  ("At six Moscow time.", "s"),
    "tm-02":  ("In two hours.", "s"),
    "tm-03":  ("Half past four.", "s"),
    "tm-04":  ("Fifteen euros.", "s"),

    # ─── S5 · Scene 1 · Café + Wi-Fi (Barista M / Sasha) ─────
    "s5-1-01": ("Good morning! What can I get you?", "m"),
    "s5-1-02": ("Good morning. Could I have a cappuccino and a croissant, please?", "s"),
    "s5-1-03": ("Of course. Anything else?", "m"),
    "s5-1-04": ("Yes — is there Wi-Fi here? I have a call in two hours.", "s"),
    "s5-1-05": ("We do. The password is on your receipt. Four euros fifty, please.", "m"),
    "s5-1-06": ("Here you are. Thank you so much.", "s"),
    "s5-1-07": ("You're welcome. Enjoy!", "m"),

    # ─── S5 · Scene 2 · Stranger / SIM-card shop (M / Sasha) ─
    "s5-2-01": ("Excuse me, where is the nearest SIM-card shop?", "s"),
    "s5-2-02": ("Go straight for one minute, then turn right at the little church. The shop is opposite the pharmacy.", "m"),
    "s5-2-03": ("Turn right at the church. Is it far?", "s"),
    "s5-2-04": ("No, it's very close. Five minutes on foot — you'll see a yellow sign.", "m"),
    "s5-2-05": ("Thanks a lot!", "s"),
    "s5-2-06": ("You're welcome. Have a nice day.", "m"),

    # ─── S5 · Scene 3 · Phone call with Marco (M / Sasha) ────
    "s5-3-01": ("Hi Sasha, it's Marco. Can you talk?", "m"),
    "s5-3-02": ("Hi Marco! I'm busy right now — I have a meeting at six Moscow time.", "s"),
    "s5-3-03": ("Oh, no problem. When are you free?", "m"),
    "s5-3-04": ("After nine pm. Could I call you back? I'll be in a Wi-Fi zone at home.", "s"),
    "s5-3-05": ("Of course. I don't have mobile data here either. Give me a call at ten.", "m"),
    "s5-3-06": ("Great — I'll call you at ten. Thanks for understanding.", "s"),
    "s5-3-07": ("No problem. Talk to you later!", "m"),

    # ─── S6 · Reading · WhatsApp to Mum ──────────────────────
    "rd-full": ("Hi Mum! I'm fine. I'm in Paris this week — a short trip for a project. I don't have mobile data on my French SIM yet, so I write to you from a small café near the hotel. I drink a cappuccino every morning — one euro fifty, and the croissant is very good. This afternoon I have a call with my colleague from Moscow at six Moscow time — that's four pm here in Paris. I'm free after nine pm. Tomorrow I buy a SIM card at a small shop opposite the pharmacy. I'm happy. Miss you! Kisses, Sasha.", "s"),

    # ─── Vocab Capsule · 30 phrases from WhatsApp vocab ──────
    "v-15min":     ("In fifteen minutes.", "s"),
    "v-after9":    ("After nine pm.", "s"),
    "v-early":     ("Early in the morning.", "s"),
    "v-tilllate":  ("Till late at night.", "s"),
    "v-free36":    ("I'm free from three to six.", "s"),
    "v-meet8":     ("I have a meeting at eight.", "s"),
    "v-busy":      ("I'm busy right now.", "s"),
    "v-15now":     ("I have fifteen minutes now.", "s"),
    "v-whenfree":  ("What time are you free?", "s"),
    "v-whentalk":  ("When can we talk?", "s"),
    "v-callback":  ("Can I call you back?", "s"),
    "v-callhome":  ("I'll call you when I get home.", "s"),
    "v-giveacall": ("Give me a call.", "s"),
    "v-notphone":  ("I can't call you by phone.", "s"),
    "v-onlywifi":  ("Only on Wi-Fi.", "s"),
    "v-wifizone":  ("I'll be in a Wi-Fi zone.", "s"),
    "v-inparis":   ("I'm in Paris this week.", "s"),
    "v-justarrived":("I just arrived here.", "s"),
    "v-nodata":    ("I don't have mobile data yet.", "s"),
    "v-getsim":    ("I'm going to get a SIM card.", "s"),
    "v-nowifi":    ("There is no Wi-Fi here.", "s"),
    "v-biztrip":   ("I'm on a business trip.", "s"),
    "v-backmonday":("I'll be back on Monday.", "s"),
    "v-justback":  ("I just got back.", "s"),
    "v-friendrec": ("My friend recommended you.", "s"),
    "v-reachout":  ("I was told to reach out to you.", "s"),
    "v-ifpossible":("If possible.", "s"),
    "v-great":     ("That would be great.", "s"),
    "v-noproblem": ("No problem.", "s"),
    "v-sorry":     ("Sorry about that.", "s"),
    "v-appreciate":("I appreciate it.", "s"),

    # ─── S7 · Speaking role-play prompts ─────────────────────
    "sp7-01": ("You're at a café in Paris. Order a cappuccino and ask for the Wi-Fi password. Target: Could I have…", "s"),
    "sp7-02": ("Stop a stranger and ask the way to the pharmacy. Target: Excuse me, where is…", "s"),
    "sp7-03": ("Introduce yourself to a new neighbour: name, where you're from, what you do. Three sentences.", "s"),
    "sp7-04": ("In a shop: ask the price of a SIM card and say it's a bit expensive. Target: How much is it?", "s"),
    "sp7-05": ("Phone call: say you're busy right now and suggest a new time. Target: I'm busy… / Could I call you back…", "s"),
    "sp7-06": ("Sixty-second monologue: My first week in Paris — use five phrases from Sections two to six.", "s"),
}

VOICES = {"s": VOICE_SASHA, "m": VOICE_M, "f": VOICE_F}

async def gen_one(aid: str, text: str, vkey: str, out_dir: pathlib.Path):
    voice = VOICES[vkey]
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
