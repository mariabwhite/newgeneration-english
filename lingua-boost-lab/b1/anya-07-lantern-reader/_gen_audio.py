"""Generate 12 edge-tts audio files for L7 The Scrapbook."""
import asyncio, os, sys
import edge_tts

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "audio")
os.makedirs(OUT, exist_ok=True)

NARRATOR = "en-US-AvaMultilingualNeural"
GRANDMA = "en-GB-SoniaNeural"
ANYA = "en-US-EmmaMultilingualNeural"
KEEPER = "en-GB-RyanNeural"
GUIDE = "en-US-BrianMultilingualNeural"

RATE_SLOW = "-12%"
RATE_NORMAL = "-4%"

TASKS = [
    ("01-prologue.mp3", NARRATOR, RATE_SLOW, """
One. The train. It is a cold Friday in November. Anya caught the last afternoon train from the city and arrived at a small country station. Grandma was waiting on the empty platform with a thermos of tea. "You have grown," Grandma said and gave her a long hug. The journey had been long, but Anya was smiling.

Two. The kitchen. The old wooden kitchen smelled of apples and herbs. Grandma lit two candles, because the November afternoons get dark very early. On the table, a brown cardboard box. "Your mother sent it last week," Grandma said. "Open it. We have waited for you."

Three. The first object. Anya opened the box. On top, a small brass compass. "Where did you catch this?" Grandma asked. Anya laughed. "At the harbour, last May. Do you remember? I waited two hours for the ferry. The old brass seller gave it to me as a goodbye gift."

Four. The second object. Under the compass lay a woven basket, very small. "And this?" "That is from the Saturday market, in June. I used to go there every weekend with you. I bargained for it. The stall seller said five coins, I said three."

Five. The third object. A tiny grey stone. "Sacred stone, July," Anya said. "A kind guide gave it to me in the sixth temple. I climbed an ancient path for two hours to get there. He told me that every traveller takes one stone home."

Six. Tonight and tomorrow. "We have three more — the postcard, the bell and the telescope," Grandma said, "but save them for tomorrow. Tonight, tell me about these three. I will put the kettle on. And after dinner we will start the scrapbook."
"""),
    ("02-reading-a-first-three-pages.mp3", ANYA, RATE_SLOW, """
The first three pages of my scrapbook.

Page one. Harbour, May. I still remember the afternoon I met the brass seller. The ferry was two hours late, and the pier smelled of salt and old rope. I sat on a wooden bench and watched the seagulls. An old man in a blue cap came up to me and asked, "Are you lost, young traveller?" I said no, I was waiting. He smiled and gave me a tiny compass. "This will show you the right direction, even when the horizon is empty." I have kept it ever since.

Page two. Market, June. In June Grandma and I used to go to the Saturday market every single week. I used to be afraid of the sellers, but by the end of the month I used to walk between the stalls like I owned the whole place. I bought a small basket for four coins. I bargained for it myself. The seller laughed, weighed the herbs into it, and gave me a paper receipt. Grandma said she had never seen me so proud.

Page three. Temples, July. In July I took a long journey to a valley of six ancient temples. Our guide was a quiet man with grey hair. We climbed an ancient path while he was telling us the story of each dome. At the sixth temple he gave me a tiny grey stone. "Every real traveller takes one home," he whispered. I have carried it in a soft cloth ever since.

Three months, three gifts. When I look at the three objects on Grandma's kitchen table, I am not the same girl. In May I used to ask people to help me. By July I was finding my own path. Something had changed, and I had not even noticed. That is why I am writing all this down, now, at eleven years old, in November, before I forget how it felt.
"""),
    ("03-reading-b-grandma-letter.mp3", GRANDMA, RATE_SLOW, """
Dear Anyechka,

I have received the small cardboard box from your mother. Everything inside has arrived safely. The compass still points north. I have already checked twice. I have spent half an hour just holding each object, one by one, by the kitchen window.

When you arrive on Friday, we will open the box together properly. But I cannot wait, so I am writing down my questions now. Will you tell me, at the station or over dinner, who exactly gave you the brass compass? Was he the same old man you mentioned in your August postcard? I think I saw him in a photograph, but I am not sure.

About the basket. Are you going to tell me the real price? I know you used to say "four coins" in front of your mum, but your father swears it was three. And how did you learn to bargain so fast? Last May you were too shy to ask for the time at the harbour.

The sacred stone worries me a little. Your guide said every traveller takes one home, but have you kept it in a soft cloth as he asked? If you have not, please bring it on Friday and I will find a piece of my grandmother's old scarf for it.

About the postcard. I have read it three times. Your handwriting was terrible, but I understood every word. We will put the postcard, the bell and the telescope out on Saturday. Three objects on Friday, three on Saturday. One whole year in two cold afternoons.

Write me the exact arrival time. I will be at the platform fifteen minutes early. With love, Grandma.
"""),
    ("04-dialogue-compass-basket.mp3", None, RATE_NORMAL, [
        (GRANDMA, "So, tell me about the man at the harbour. Was he really that old?"),
        (ANYA, "Very old, Grandma. He had a blue cap and a white beard. He used to sell brass tools every afternoon."),
        (GRANDMA, "And the compass, did you ask for it, or did he just give it to you?"),
        (ANYA, "He gave it. He said, you have been waiting more patiently than most grown-ups. Take this. I have kept it on my desk ever since."),
        (GRANDMA, "And the basket, how did the real bargain work?"),
        (ANYA, "I said three coins, he said six, we argued for ten minutes, and we agreed on four. Dad is wrong. I paid four, not three."),
        (GRANDMA, "Good girl. Four is a fair price for a woven basket that size."),
    ]),
    ("05-dialogue-stone-postcard.mp3", None, RATE_NORMAL, [
        (ANYA, "Grandma, the stone is still wrapped in that red cloth, look. I have never unwrapped it, only the day the guide gave it to me."),
        (GRANDMA, "Very good. Did the guide say anything else at the sixth temple?"),
        (ANYA, "He said, a sacred stone does not need to shine. Keep it close, not visible. I think about that sentence a lot."),
        (GRANDMA, "That is a beautiful sentence. Now, the August postcard. Why was your handwriting so terrible?"),
        (ANYA, "Because the plane was boarding! I wrote the whole thing in three minutes, standing at a tiny café in a bustling airport."),
        (GRANDMA, "Did you post it yourself?"),
        (ANYA, "Yes, I ran to a red post box right at the gate. I will never forget the smell of coffee at that café."),
    ]),
    ("06-dialogue-bell-telescope.mp3", None, RATE_NORMAL, [
        (GRANDMA, "So, the bronze bell. Who gave this to you? The lighthouse keeper?"),
        (ANYA, "Yes. He was a quiet man with a grey beard. At midnight on October thirty-first he rang a big bell three times, and then he gave me this small one."),
        (GRANDMA, "And the telescope? It is very small."),
        (ANYA, "The observatory keeper let me borrow it for a week. When I brought it back, he said, keep it. You have been looking through it more often than I have."),
        (GRANDMA, "Will you look at the sky tonight?"),
        (ANYA, "Yes. If the fog clears, we will see Orion above the garden. By midnight we will have counted at least three constellations."),
        (GRANDMA, "Good. Then let us finish the scrapbook first, so we can go outside before it gets too cold."),
    ]),
    ("vocab-harbour.mp3", GRANDMA, RATE_SLOW, """
Listen. Harbour. Ferry. Pier. Brass. Compass. Horizon.
At the harbour last May, Anya waited two hours for the ferry. The ferry was late. The brass seller gave her a tiny compass. She looked at the horizon and felt happy.
"""),
    ("vocab-market.mp3", None, RATE_NORMAL, [
        (ANYA, "Excuse me, how much is this small basket?"),
        (GUIDE, "Six coins, young lady. Six coins."),
        (ANYA, "Six is too much. I can pay three."),
        (GUIDE, "Three? No, no. Five. Just for you."),
        (ANYA, "Four coins. That is my last price."),
        (GUIDE, "Four coins. All right, four. You bargain like a grandmother."),
    ]),
    ("vocab-temples.mp3", GUIDE, RATE_SLOW, """
Listen to the guide. Temple. Sacred. Ancient. Path. Stone.
We climbed an ancient path for two hours. At the sixth temple I gave Anya a small grey stone. I whispered, every real traveller takes one home. She has carried it in a soft cloth ever since.
"""),
    ("vocab-postcards.mp3", ANYA, RATE_NORMAL, """
Listen. Postcard. Envelope. Stamp. Handwriting. Suitcase.
I had only three minutes at the airport café. My handwriting was terrible because the plane was already boarding. I ran to a red post box right at the gate and posted the card. One week later Grandma received my postcard from a bustling airport.
"""),
    ("vocab-lighthouse.mp3", KEEPER, RATE_SLOW, """
Listen to the lighthouse keeper. Lighthouse. Cliff. Fog. Midnight. Whisper.
At midnight on October thirty-first the big bell rang three times. I was climbing the cliff path in thick fog. The old keeper came out of the lighthouse door and placed a small bronze bell in my hand. This one is yours now. Ring it when you need to remember a secret.
"""),
    ("vocab-observatory.mp3", KEEPER, RATE_SLOW, """
Listen to the observatory keeper. Observatory. Telescope. Dawn. Constellation. Planet.
I stood at the observatory before the first light. The keeper let me look through his small brass telescope. Keep it, he said after a week. You have used it more often than I have. I promised him I would come back next summer and tell him about every constellation I see.
"""),
]


async def say(text, voice, rate, path):
    tts = edge_tts.Communicate(text.strip(), voice=voice, rate=rate)
    await tts.save(path)


async def say_dialogue(parts, rate, path, workdir):
    import subprocess
    tmp = []
    for idx, (voice, text) in enumerate(parts):
        p = os.path.join(workdir, f"_tmp_{idx:02d}.mp3")
        tts = edge_tts.Communicate(text.strip(), voice=voice, rate=rate)
        await tts.save(p)
        tmp.append(p)
    listfile = os.path.join(workdir, "_concat.txt")
    with open(listfile, "w", encoding="utf-8") as fp:
        for p in tmp:
            fp.write(f"file '{p.replace(chr(92), '/') }'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", path], check=True, capture_output=True)
    for p in tmp:
        try: os.remove(p)
        except: pass
    try: os.remove(listfile)
    except: pass


async def main():
    for name, voice, rate, payload in TASKS:
        out = os.path.join(OUT, name)
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            print(f"skip {name}")
            continue
        print(f"gen  {name}")
        try:
            if isinstance(payload, list):
                await say_dialogue(payload, rate, out, OUT)
            else:
                await say(payload, voice, rate, out)
            print(f"ok   {name} ({os.path.getsize(out)} bytes)")
        except Exception as e:
            print(f"ERR  {name}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
