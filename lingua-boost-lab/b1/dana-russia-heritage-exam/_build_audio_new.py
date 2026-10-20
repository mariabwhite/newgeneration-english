"""Rebuild lst1/lst2/lst3.mp3 for the Culture-themed rewrite.
L1 = 6 speakers (6 different voices) · Tchaikovsky / Levitan / Dostoevsky / Tolstoy / Golden Ring / Aurora
L2 = Anna + Denis dialogue · Yasnaya Polyana
L3 = Host + Anna · Mariinsky soloist
"""
import asyncio, os, subprocess, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, 'assets', 'audio')
TMP = os.path.join(AUDIO, '_tmp')
os.makedirs(TMP, exist_ok=True)

L1 = [
    ('en-GB-SoniaNeural', '-5%', '+2Hz',
     "Speaker A. My grandmother dragged me to Votkinsk last summer — a tiny factory town in the Urals with one proper hotel and a lot of mosquitoes — and I grumbled all the way there. Then we walked into the wooden house where Tchaikovsky was born, saw his first upright piano standing by the window, and I actually started crying. The guide let me put one finger on the key she said he had played the day his mother died. I've been listening to the First Piano Concerto on repeat ever since, and I'm now seriously thinking about applying to Gnesin."),
    ('en-GB-LibbyNeural', '-3%', '+3Hz',
     "Speaker B. We did a two-day art-history trip to the Tretyakov in September and I spent half of it in the Levitan hall. His Golden Autumn is the kind of painting you don't just look at — you literally fall into. I'd always thought landscape painting was boring, something old ladies did on weekends, but Levitan proves me completely wrong. He gives you a bend in the Volga, a thin wooden bridge, and suddenly you want to pack a bag and go there yourself. I bought the reproduction and it's over my bed now."),
    ('en-US-AndrewNeural', '-4%', '+2Hz',
     "Speaker C. For my literature coursework I had to read Crime and Punishment, which I'd been avoiding since year nine. I read it in four days, and on the fifth I took the metro to the Dostoevsky flat museum on Kuznechny Lane. The staircase is the exact one Raskolnikov climbs, step for step — I counted. The ink-well, the desk, the pocket watch stopped at eight thirty-six in the evening of his death. I came home and reread the ending, and this time, I understood the last line."),
    ('en-GB-ThomasNeural', '-6%', '-2Hz',
     "Speaker D. My family went to Yasnaya Polyana for the long weekend — Tolstoy's estate, about three hours south of Moscow. I expected a quick museum visit, but we ended up walking for four hours in the oak forest, past the pond where he swam, past the apple orchard he planted himself. His grave is just a long rectangular mound of grass, no cross, no name, because in old age he decided a cross would be hypocritical. It is honestly the quietest place I have ever stood in my life."),
    ('en-US-AriaNeural', '-3%', '+4Hz',
     "Speaker E. Last autumn my parents took me on the Golden Ring road trip — Suzdal, Vladimir, Yaroslavl, Rostov Veliky — five days in the car, two churches per hour, pancakes with sour cream in every little café. In Suzdal there's a local by-law forbidding any new building taller than a bell tower, so the skyline hasn't changed since the eighteenth century. I didn't know Russia still had places where you can hear the cuckoo above the morning bells. I am going back next spring, I promise myself."),
    ('en-GB-RyanNeural', '-5%', '-3Hz',
     "Speaker F. This March I finally saw the Northern Lights, from a wooden lodge outside Teriberka, two hundred and thirty kilometres above the Arctic Circle. We waited four nights in minus twenty degrees before the sky suddenly turned pink and green at two in the morning, and the whole group just stopped breathing. The physics teacher in me kept whispering it's just solar wind on oxygen atoms, but the rest of me cried quietly in a thermos of tea. I'm applying to the astrophysics track at MSU now."),
]

L2 = [
    ('en-GB-LibbyNeural', '-3%', '+3Hz', "Anna. Denis, guess what — my class is going to Yasnaya Polyana next Friday!"),
    ('en-GB-RyanNeural', '-4%', '-2Hz', "Denis. Lucky you! The whole day in Tolstoy's forest?"),
    ('en-GB-LibbyNeural', '-3%', '+3Hz', "Anna. Almost. We leave Moscow at seven in the morning in two coaches, and we're back around nine in the evening. Our literature teacher is coming — and our history teacher, Pavel Sergeyevich."),
    ('en-GB-RyanNeural', '-4%', '-2Hz', "Denis. Have you booked a guide?"),
    ('en-GB-LibbyNeural', '-3%', '+3Hz', "Anna. Yes, a literature specialist — because half of our class is already reading War and Peace. It costs extra, but the school pays for the coach tickets."),
    ('en-GB-RyanNeural', '-4%', '-2Hz', "Denis. Nice. What are you most excited about?"),
    ('en-GB-LibbyNeural', '-3%', '+3Hz', "Anna. The grave in the forest. I've been to the main house twice before on family trips, but never to the glade where he's buried."),
    ('en-GB-RyanNeural', '-4%', '-2Hz', "Denis. I've never been at all. My parents keep saying we'll go next summer, but next summer never comes."),
    ('en-GB-LibbyNeural', '-3%', '+3Hz', "Anna. Come with us! Actually no — my teacher said the coach is full."),
    ('en-GB-RyanNeural', '-4%', '-2Hz', "Denis. Fine. Take good photos then."),
]

L3 = [
    ('en-GB-ThomasNeural', '-4%', '-2Hz', "Host. Anna, thanks for joining us. You are only 24, but you already dance the leading role of Odette in Swan Lake. Tell us how it all started."),
    ('en-GB-SoniaNeural', '-3%', '+3Hz', "Anna. Well, I grew up in Petrozavodsk, in a family of amateur musicians. My mother played in the city orchestra, so music was our dinner-table conversation. But interestingly, I didn't want to be a dancer. I wanted to be a figure skater. I only changed my mind at eleven after a Mariinsky touring company visited our local theatre."),
    ('en-GB-ThomasNeural', '-4%', '-2Hz', "Host. Where did you train?"),
    ('en-GB-SoniaNeural', '-3%', '+3Hz', "Anna. I did my first years at the Petrozavodsk choreographic school, then moved to Saint Petersburg for the Vaganova Academy. I joined the Mariinsky at nineteen, danced in the corps for three years, and became a principal soloist last September. My signature roles are Odette-Odile in Swan Lake and Giselle."),
    ('en-GB-ThomasNeural', '-4%', '-2Hz', "Host. Have you performed abroad?"),
    ('en-GB-SoniaNeural', '-3%', '+3Hz', "Anna. Yes, one tour in Milan, and last summer we performed in Tokyo for two weeks. Both tours were useful, but I always want to come home to the Mariinsky stage. My audience is here — the Petersburg public, who have been watching ballet for three centuries."),
    ('en-GB-ThomasNeural', '-4%', '-2Hz', "Host. What's the biggest difficulty in your work?"),
    ('en-GB-SoniaNeural', '-3%', '+3Hz', "Anna. Money is not the main issue — the theatre pays well. The real problem is time. A new production takes three months of daily rehearsal before the premiere. And an injury can ruin months of preparation."),
    ('en-GB-ThomasNeural', '-4%', '-2Hz', "Host. Any advice for young girls who want to enter ballet?"),
    ('en-GB-SoniaNeural', '-3%', '+3Hz', "Anna. Two things. First — don't listen to people who say ballet is finished, nobody watches it any more. They're wrong. Second — start small, but start early. A local dance class counts. A YouTube channel counts. Show your love of the stage, don't just talk about it."),
]

async def tts(voice, rate, pitch, text, path):
    import edge_tts
    for attempt in range(3):
        try:
            await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(path)
            if os.path.getsize(path) > 0: return True
        except Exception as e:
            print(f"  err {str(e)[:60]}")
            try: os.remove(path)
            except: pass
            if attempt < 2:
                import time; time.sleep(3)
    return False

def concat(parts, out):
    """Concat MP3s via ffmpeg concat demuxer."""
    listfile = out + '.lst'
    with open(listfile, 'w', encoding='utf-8') as f:
        for p in parts:
            f.write(f"file '{p.replace(chr(92), '/')}'\n")
    cmd = f'ffmpeg -y -f concat -safe 0 -i "{listfile}" -c:a libmp3lame -b:a 128k "{out}"'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try: os.remove(listfile)
    except: pass
    return r.returncode == 0

async def build(name, clips):
    print(f'=== {name} ===')
    parts = []
    for i, (voice, rate, pitch, text) in enumerate(clips):
        p = os.path.join(TMP, f'{name}-{i:02d}.mp3')
        if not os.path.exists(p):
            print(f'  [{i+1}/{len(clips)}] {voice} r={rate} p={pitch}')
            ok = await tts(voice, rate, pitch, text, p)
            if not ok:
                print(f'    FAIL')
                return
        parts.append(p)
    final = os.path.join(AUDIO, f'{name}.mp3')
    print(f'  concat → {final}')
    if concat(parts, final):
        print(f'  OK {os.path.getsize(final):,} b')
    else:
        print(f'  concat FAIL')

async def main():
    await build('lst1', L1)
    await build('lst2', L2)
    await build('lst3', L3)
    print('\n=== DONE ===')
    for n in ['lst1','lst2','lst3']:
        p = os.path.join(AUDIO, f'{n}.mp3')
        if os.path.exists(p):
            print(f'  {n}.mp3: {os.path.getsize(p):,} b')

asyncio.run(main())
