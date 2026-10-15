"""Jobs & Hobbies lesson audio: 5 clips via edge-tts + ffmpeg mp3 128k.
Each clip = narrator for a reading section. en-GB voices, slight reverb for warmth."""
import asyncio, os, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, 'assets', 'audio')
os.makedirs(AUDIO, exist_ok=True)

CLIPS = [
    ('reading-bodyguard', 'en-GB-RyanNeural', '-6%', '-3Hz',
     "Being a bodyguard is not what you see in action films. The real work is quiet and patient. "
     "You arrive early, you check the room, you check the doors, you check every car in the car park. "
     "Then you stand two steps behind the person you protect, and you watch everything. "
     "Most days nothing happens. That is a good day. The money is above average, but the hours are long. "
     "Many bodyguards work twelve-hour shifts six days a week. "
     "They have strong training in self-defence, first aid, driving and crowd observation. "
     "The best bodyguards never make the news — because when they are doing their job well, "
     "the person they protect simply walks safely through the day."),
    ('reading-hobbies-by-age', 'en-GB-SoniaNeural', '-4%', '+2Hz',
     "In Britain, people often start a hobby at a particular age — and keep it for life. "
     "Between eight and ten, children usually keep pets, collect stickers, play games with their friends in the park, "
     "and shout in excitement over a new comic book. "
     "Between ten and twelve, many take up gardening, fishing or jogging — the first grown-up hobbies. "
     "From thirteen to fifteen, they fly kites, build chemistry sets, knit, sew, play board games and card games, "
     "and spend afternoons on football and the sports pages of the newspaper. "
     "From sixteen to twenty, parties, cinema, first jobs, and new sports: surfing, photography, bouldering. "
     "After twenty, people often go back to the hobbies of childhood — gardening, collecting, painting, traveling — "
     "but this time with more money and less time."),
    ('reading-jobs-pay', 'en-GB-RyanNeural', '-5%', '-4Hz',
     "Why do some jobs pay more than others? Three main reasons. "
     "First, training years. A doctor studies for six years and then trains for four more. A software engineer "
     "needs five years of serious practice before anyone will trust them with a real project. "
     "A shepherd learns everything on the first week on the farm. "
     "Second, risk. A deep-sea welder earns ten times the wage of an office welder because the risk is ten times higher. "
     "Third, supply and demand. There are many teachers but few orthopaedic surgeons; "
     "so the surgeon earns ten times more, even though the teacher works longer hours and has more responsibility. "
     "The pay is not a measure of how important the job is. It is only a measure of how hard it is to replace you."),
    ('interview-sample', 'en-GB-RyanNeural', '-3%', '+0Hz',
     "Welcome to our London office. Please take a seat. "
     "Could you start by telling us a little about yourself and what brought you to apply for this role? "
     "Thank you. Now, what would you say are your three main strengths — and one honest weakness? "
     "And how did you first hear about our company? "
     "Finally, where do you see yourself in five years? And do you have any questions for us?"),
    ('interview-candidate', 'en-GB-SoniaNeural', '-2%', '+3Hz',
     "Thank you so much for seeing me today. I am very keen on this role because I have been following your projects for two years. "
     "My three main strengths are communication, problem-solving and persistence. My honest weakness is that I sometimes "
     "spend too long perfecting the small details — but I am working on it. "
     "I first heard about you from a presentation at my university. "
     "In five years, I see myself leading a small team on one of your flagship projects. "
     "I do have one question — how is success measured in this role during the first six months?"),
]

async def tts_batch():
    import edge_tts
    for slug, voice, rate, pitch, text in CLIPS:
        path = os.path.join(AUDIO, f'{slug}.mp3')
        if os.path.exists(path) and os.path.getsize(path) > 0:
            print(f'[skip] {slug} ({os.path.getsize(path):,} b)')
            continue
        print(f'[tts]  {slug}  ({voice}, {rate}, {pitch})')
        for attempt in range(3):
            try:
                tts = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
                await tts.save(path)
                if os.path.getsize(path) == 0: raise RuntimeError('empty')
                print(f'       {os.path.getsize(path):,} b OK (try{attempt+1})')
                break
            except Exception as e:
                print(f'       try{attempt+1} ERR {str(e)[:80]}')
                try: os.remove(path)
                except: pass
                if attempt < 2:
                    import time; time.sleep(4)
                else:
                    print(f'       GIVE UP {slug}')

def ffmpeg_fx():
    """Light reverb for warmth."""
    for slug, *_ in CLIPS:
        inp = os.path.join(AUDIO, f'{slug}.mp3')
        out = os.path.join(AUDIO, f'{slug}-fx.mp3')
        if not os.path.exists(inp): continue
        if os.path.exists(out) and os.path.getsize(out) > 0:
            print(f'[fx-skip] {slug}-fx')
            continue
        cmd = f'ffmpeg -y -i "{inp}" -af "aecho=0.6:0.55:40:0.15,volume=1.2" -c:a libmp3lame -b:a 128k "{out}"'
        print(f'$ fx {slug}')
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out):
            print(f'       {os.path.getsize(out):,} b OK')
        else:
            print(f'       ERR {r.stderr[-200:]}')

if __name__ == '__main__':
    print('=== TTS ===')
    asyncio.run(tts_batch())
    print('\n=== FX ===')
    ffmpeg_fx()
    print('\nDONE')
    for s, *_ in CLIPS:
        p = os.path.join(AUDIO, f'{s}-fx.mp3')
        if os.path.exists(p):
            print(f'  {s}-fx: {os.path.getsize(p):,} b')
