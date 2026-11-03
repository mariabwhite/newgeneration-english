"""Generate edge-tts audio for all listening blocks in Sport in Our Life lesson.

Clips:
- speakers 1-4 (my F3 block): Marta(F AmE), Jack(M BrE), Sofia(F BrE), Tom(M AmE)
- read-aloud: Netball (F BrE), Table Tennis (M BrE)
- FIPI L1-4: 4 short texts (jogging girl, golf club man, referee, lady & TV)
- FIPI L5: 5 speakers A-E
- FIPI L6-11: full interview (journalist + respondent)
"""
import asyncio, os, sys, pathlib
import edge_tts

sys.stdout.reconfigure(encoding="utf-8")
OUT = pathlib.Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

# Voice map
VOICE_F_US = "en-US-AriaNeural"
VOICE_M_US = "en-US-GuyNeural"
VOICE_F_GB = "en-GB-SoniaNeural"
VOICE_M_GB = "en-GB-RyanNeural"
VOICE_F_GB2 = "en-GB-LibbyNeural"
VOICE_M_GB2 = "en-GB-ThomasNeural"

CLIPS = [
    # ---- F3 (my block): 4 speakers for match task ----
    ("f3-speaker1-marta.mp3", VOICE_F_US,
     "My favourite kind of sport is hiking. Every weekend my parents, my little brother and I go to the forest or the mountains near our town. We walk for hours, take photos and have a picnic. I don't like gyms or stadiums. I love being outside with my family. For me it's the best way to spend a Sunday."),
    ("f3-speaker2-jack.mp3", VOICE_M_GB,
     "I started playing football when I was five, and now I train with the junior team every day after school. My coach says I have real talent. I know many people become professional footballers only when they're really lucky, but I'll do my best. One day I would like to play for Manchester City. That's what I'm working for."),
    ("f3-speaker3-sofia.mp3", VOICE_F_GB,
     "Last year I was in the school swimming team and I was really happy about it. But in May I hurt my shoulder badly during training, and the doctor said I had to stop swimming for a year. Now I only watch competitions on TV. I miss my team a lot, but I know I'll come back when my shoulder is healthy."),
    ("f3-speaker4-tom.mp3", VOICE_M_US,
     "I'd love to go in for fencing or martial arts, but at our school we only have football, basketball and volleyball. That's a pity. My cousin goes to a school in Moscow and they have everything — judo, archery, even horse riding. I wish our head teacher would open more sports clubs for us."),

    # ---- Read aloud models (speaking Task 1) ----
    ("read-netball.mp3", VOICE_F_GB,
     "Netball is played by over twenty million people in more than seventy countries of the world. It was invented in eighteen ninety-two as women's basketball. However, netball is different from basketball in many ways. For example, the ball and the basket are smaller and the court is bigger. The players cannot run with the ball. They are not allowed to touch the players who they are playing with. Netball has seven players in each team, not five as in basketball. During the twentieth century, the game became very popular in English-speaking countries. Traditionally, only girls and women have played netball. Nowadays, netball is the number one women's sport in the world, but boys and men are starting to play it too."),
    ("read-table-tennis.mp3", VOICE_M_GB,
     "Table tennis is the third most played sport in the world after football and cricket. It is considered to be an indoor version of lawn tennis. However, they have a lot of differences. Table tennis has a different scoring system, a smaller ball, smaller rackets, and a smaller playing area. Modern table tennis was invented at the end of the nineteenth century in England. Very soon the new sport became popular all over the world. In nineteen oh one, competitions with over three hundred participants were already being held. According to numerous studies, table tennis has great effects on human health. It keeps the brain sharp and improves the player's coordination. Since nineteen eighty-eight, table tennis has been an Olympic sport."),

    # ---- FIPI L1-4 (short MCQ texts written to fit each correct answer) ----
    ("fipi-l1-jogging-girl.mp3", VOICE_F_US,
     "Hi, I'm Lucy. I started jogging two years ago, and now I run every single day. Some of my friends laugh at me when it's raining or snowing, but I don't care at all. For me, jogging in winter is just as nice as in summer. I just put on my special jacket and go. The weather or the season doesn't stop me. Running outside gives me so much energy, no matter what the sky looks like."),
    ("fipi-l2-golf-club.mp3", VOICE_M_US,
     "You know, I joined that new sports club last month. The membership itself is pretty reasonable, and the gym is included for free. The swimming pool and the billiard room are also free for members. The only thing you actually have to pay extra for is golf, because the course is run by a separate company. So if you want to play golf, bring your wallet. Everything else, you can just show up and use."),
    ("fipi-l3-referee.mp3", VOICE_M_GB,
     "That was a difficult match for me as a referee. The players were really aggressive from the first minute, pushing and shoving each other all the time. I had to blow my whistle and stop the game for a few minutes to calm them down. Honestly, if I hadn't done that, we would have ended up with half the team on the bench with broken legs and bruises. Nobody wants to see players getting hurt. That's why I made that decision."),
    ("fipi-l4-tv-lady.mp3", VOICE_F_GB,
     "Could you please change the channel, dear? I know the football final is on tonight, and I know your team is playing, but I really wanted to watch my favourite Discovery programme. It's about African elephants and I've been waiting for it all week. Please, just for one hour. You can read the match result online afterwards. Thank you so much."),

    # ---- FIPI L5 (5 speakers → 6 topics: 2 home sports, 3 day off, 1 sports centre, 4 disagreement, 5 healthy eating; extra = 6 popular sports) ----
    ("fipi-l5-speaker-a.mp3", VOICE_F_US,
     "I don't really like going to the gym. There are always too many people and it's expensive. What I do instead is work out in my living room. I have a yoga mat, some light dumbbells and an exercise video. Three times a week, right after breakfast, I do a thirty-minute session. It's convenient and it works for me."),
    ("fipi-l5-speaker-b.mp3", VOICE_M_GB,
     "My Saturdays are always the same, and I love it. I wake up late, around ten. Then I have a long breakfast with coffee and a good book. In the afternoon, I usually go to the park or meet friends. In the evening I watch a film. No gym, no running, no sport at all. It's my recovery day."),
    ("fipi-l5-speaker-c.mp3", VOICE_F_GB,
     "In our town there is a brand new sports centre. It opened last year, right in the middle of the city. It has three swimming pools, a huge gym, tennis courts and even a climbing wall. I buy a monthly card, which is very reasonable. Honestly, I think it's the best place in our town for anyone who likes sport."),
    ("fipi-l5-speaker-d.mp3", VOICE_M_US,
     "Last Sunday I had a big argument with my best friend. We were supposed to go cycling together, but she showed up two hours late. I was really angry because I had been waiting for her in the park. We shouted at each other and then she just went home. We haven't spoken since. I hope we can talk soon and fix things."),
    ("fipi-l5-speaker-e.mp3", VOICE_F_GB,
     "Three years ago I decided to change the way I eat. Now I never buy fast food. I eat lots of fruit and vegetables, fish twice a week, and I drink water instead of fizzy drinks. I feel so much better. I have more energy, I sleep well and I almost never get colds. Food really is medicine."),

    # ---- FIPI L6-11 (interview journalist ↔ respondent) ----
    ("fipi-l6-11-interview.mp3", VOICE_F_GB,
     "Journalist: Hello, and welcome to our sports show. Today we're talking to a teenage listener about sport in her family. Thanks for coming! "
     "Respondent: Thanks for inviting me. "
     "Journalist: Let's start with your brother. He's an athlete, isn't he? "
     "Respondent: Yes, my brother plays ice hockey professionally. He's a goalkeeper on a youth team. "
     "Journalist: What a cool job! And what sports does your family love in general? "
     "Respondent: We're a sporty family. Everyone in our family loves football and hockey. We watch all the matches together on TV. "
     "Journalist: What about you personally? "
     "Respondent: My favourite kind of sport is figure skating. I've been doing it for seven years. "
     "Journalist: Where do you train? "
     "Respondent: Well, our city is quite small, but we have a brand new skating rink and swimming pool. They are both on the opposite side of the city from where I live. I take a bus to get there. "
     "Journalist: And how often does your brother practise football? "
     "Respondent: Football is just a hobby for him, really. He practises every day because his main sport is hockey, and running helps him stay fit. "
     "Journalist: Interesting! One last question — what about your dad? Does he do any sport? "
     "Respondent: My dad is a football coach! Actually, he flew to Germany last week for a training course with other coaches. He'll be back on Friday. "
     "Journalist: Thank you so much for this interview. Keep skating!"),
]


async def gen_one(filename: str, voice: str, text: str):
    """Generate one MP3; retry once on 403."""
    path = OUT / filename
    if path.exists() and path.stat().st_size > 1000:
        print(f"skip (exists): {filename}")
        return
    for attempt in (1, 2, 3):
        try:
            communicate = edge_tts.Communicate(text, voice, rate="-5%")
            await communicate.save(str(path))
            if path.stat().st_size > 1000:
                print(f"ok · {filename} · {path.stat().st_size // 1024} KB · {voice}")
                return
        except Exception as e:
            print(f"attempt {attempt} fail {filename}: {e}")
            await asyncio.sleep(3 * attempt)
    print(f"FAIL · {filename}")


async def main():
    for i, (fn, v, t) in enumerate(CLIPS, 1):
        print(f"[{i}/{len(CLIPS)}]")
        await gen_one(fn, v, t)
        await asyncio.sleep(1)


asyncio.run(main())
print(f"\nTotal: {len(list(OUT.glob('*.mp3')))} mp3 files in {OUT}")
