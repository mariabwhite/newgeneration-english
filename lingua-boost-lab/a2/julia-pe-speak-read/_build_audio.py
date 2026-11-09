# _build_audio.py · Julia · PE Day · Speaking + Reading
# Запуск: python _build_audio.py
# Нужно: pip install edge-tts
# Red lines:
#   - en-US only (American family canon)
#   - retry 403 (reference_edge_tts_403_retry): delete 0-byte, sleep 5, retry skip existing
#   - rate -6% для Julia narrator
#   - slug cap 30 (julia-pe-speak-read = 19 ✓)

import asyncio
import os
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("pip install edge-tts first")
    sys.exit(1)

AUDIO_DIR = Path(__file__).parent / "audio"
AUDIO_DIR.mkdir(exist_ok=True)

# Canon voices · en-US only (JULIA_CANON §8)
V_JULIA = "en-US-AriaNeural"      # main narrator, rate -6%
V_MUM   = "en-US-SaraNeural"      # Mum
V_DAD   = "en-US-GuyNeural"       # Dad
V_JOHN  = "en-US-AnaNeural"       # John (child)
V_EMMA  = "en-US-JennyNeural"     # Emma
V_COACH = "en-US-AndrewNeural"    # coach (if needed)

# key → (voice, text, rate)
CLIPS = {
    # ===== CAST STRIP =====
    "cast-julia":   (V_JULIA, "Hi! I'm Julia. I'm nine, and I love running.", "-6%"),
    "cast-mum":     (V_MUM,   "Hi, I am Mum. I make the best pancakes on Sundays.", "+0%"),
    "cast-dad":     (V_DAD,   "I'm Dad. I keep an old silver stopwatch — don't mess with it.", "+0%"),
    "cast-john":    (V_JOHN,  "I'm John! I'm six and I lost one sneaker again.", "+0%"),
    "cast-emma":    (V_EMMA,  "Hey, I'm Emma — Julia's best friend from class.", "+0%"),
    "cast-barsik":  (V_JULIA, "And this is Barsik, our grey cat. He is the king of the house.", "-6%"),

    # ===== 0 · WARM-UP =====
    "scene-warmup": (V_JULIA, "When this tiny thing goes peeeeep, every runner on the field stops, looks up, and listens. Even Barsik runs under the couch. Dad says it's the coach's best friend.", "-6%"),

    # ===== 1 · PICTURE TALK =====
    "pic-tip":      (V_JULIA, "One minute per picture. At least five sentences, not just one word. Use 'be about to' and 'I think will' at least once.", "-6%"),

    # ===== 2 · SPEAKING PART 1 · model answers =====
    "sp-q1-model":  (V_JULIA, "At school we usually have PE on Mondays and Wednesdays. We run, we jump, and sometimes we play soccer in the yard. My favourite sport is running, because I'm pretty fast and I love the wind in my hair, although Dad says I should also try basketball.", "-6%"),
    "sp-q2-model":  (V_JULIA, "Next PE lesson we're going to practise for the big sports day. I'm going to do short sprints with Emma and then we'll jump into the long jump pit. I hope I'll jump further than last week, so that the coach adds me to the main team.", "-6%"),
    "sp-q3-model":  (V_JULIA, "I'd love to try tennis one day, because I like the sound the ball makes on the racket. If my mom says yes, I'll join a tennis club next summer. My dad plays a little tennis too — he could coach me on weekends.", "-6%"),
    "sp-q4-model":  (V_JULIA, "I usually prefer team sports because I love playing with Emma — we laugh a lot, and when the team wins, everyone wins together. On the other hand, when I'm tired of people I like running on my own, so my head gets quiet. Both are good for different moods.", "-6%"),
    "sp-q5-model":  (V_JULIA, "Sure, let's! I'll meet you by the big oak at four. If the weather holds, we'll run two laps around the field. Shall I bring a bottle of water for both of us? Last time we were really thirsty by the end.", "-6%"),
    "sp-q6-model":  (V_JULIA, "In my family, Dad is probably the most into sports. He used to run marathons when he was younger, and he still keeps his old stopwatch in the kitchen drawer. On Sundays we usually go for a long walk in the city park, and sometimes John and I race him home. Even Barsik runs, but only when he hears the pancake pan!", "-6%"),
    "sp-q7-model":  (V_JULIA, "This time next Saturday I'll be running on the school field. Our sports day starts at ten. If the weather is nice, I'll be jumping into the long jump pit at eleven. If it rains, I'll probably be sitting on the couch with Barsik, watching old race videos with Dad.", "-6%"),
    "sp-q8-model":  (V_JULIA, "I think our class has a real chance this year, because Emma is the fastest in the sixty metres and I'm not bad at the long jump. If everyone practises every day, we'll win at least three medals. Although Grade five is tough — their relay team is pretty strong.", "-6%"),
    "sp-q9-model":  (V_JULIA, "By June I will have learned how to do a proper long jump and how to pace myself in a sixty-metre sprint. I'll also have tried basketball for the first time, because Dad promised to practise with me. I hope I'll also have beaten my own record by at least one second.", "-6%"),
    "sp-q10-model": (V_JULIA, "Once, during the school fun-run, John lost one of his sneakers on the second lap — it flew off his foot and landed in a flower bed. He kept running in one shoe and one sock! The coach was laughing so hard she dropped her clipboard. Dad still shows that video on his phone.", "-6%"),

    # ===== 3 · SPEAKING PART 2 · photo cards =====
    "photo-a-model": (V_JULIA, "In this photo I can see a classic American school sports day. It's a sunny morning. On the track, four kids are running the sixty-metre sprint. The girl in a yellow shirt is in front — in a second she'll have crossed the finish line. On the right, the coach is holding a whistle and looking at her stopwatch. In the crowd, I can see Mum clapping like crazy, Dad filming everything with his phone, and John holding a big sign that says GO JULIA. Even Barsik is there — sitting on a bench in a tiny t-shirt, probably wishing he was back home with Turbo. In a minute everyone will be cheering, Mum will have wiped a happy tear, and they'll all go for pancakes.", "-6%"),
    "photo-b-model": (V_JULIA, "This photo catches the exact moment of the long jump — the girl is in the air, mid-flight, her arms thrown forward. Sand is already flying up a little, so she's about to land. She looks really focused and maybe a bit worried — her face is serious, not smiling. On the side, the coach is holding a measuring tape, waiting. In the background, two other kids are stretching before their turn. In the next two seconds she'll land and the coach will be measuring. If she lands well, she'll have beaten her personal record from last month. Honestly, I think she looks strong — I bet her number goes up on the leaderboard in a minute.", "-6%"),

    # ===== 4 · ROLE-PLAY · 12 lines =====
    "rp-emma-1":  (V_EMMA,  "Julia, sports day is this Friday! Shall we practise after school today?", "+0%"),
    "rp-julia-1": (V_JULIA, "Yes, let's! At four o'clock? I'll bring my sneakers and a bottle of water for both of us.", "-6%"),
    "rp-emma-2":  (V_EMMA,  "Perfect. I'm going to run the sixty metres. What about you — what are you going for this year?", "+0%"),
    "rp-julia-2": (V_JULIA, "I'm going to run with you AND try the long jump. Dad says if I practise every day, by Friday I'll have added at least twenty centimetres to my jump.", "-6%"),
    "rp-emma-3":  (V_EMMA,  "Nice. What if it rains on Friday?", "+0%"),
    "rp-julia-3": (V_JULIA, "If it rains, we'll move the races into the gym. But the weather app says sunny all week, so I don't think it will.", "-6%"),
    "rp-emma-4":  (V_EMMA,  "Who's coming to watch you this year?", "+0%"),
    "rp-julia-4": (V_JULIA, "The whole family is coming. Mum is bringing a lunch box of pancakes, Dad is going to film everything on his phone, and they're even bringing Barsik in his carrier — John says the team needs a mascot.", "-6%"),
    "rp-emma-5":  (V_EMMA,  "Haha, a cat mascot? What about Turbo?", "+0%"),
    "rp-julia-5": (V_JULIA, "Turbo is staying home — he's way too slow for a sports day! But I'll tell him all about it when I get back. He's a great listener.", "-6%"),
    "rp-emma-6":  (V_EMMA,  "Shall we meet at nine at the main gate on Friday?", "+0%"),
    "rp-julia-6": (V_JULIA, "Yes! And by eleven we'll have finished our race — then we can grab lunch and cheer for the other classes. Deal?", "-6%"),

    # ===== 4 · FULL DIALOGUE (concat) =====
    "rp-full": (V_JULIA, "Emma. Julia, sports day is this Friday! Shall we practise after school today? Julia. Yes, let's! At four o'clock? I'll bring my sneakers and a bottle of water for both of us. Emma. Perfect. I'm going to run the sixty metres. What about you — what are you going for this year? Julia. I'm going to run with you AND try the long jump. Dad says if I practise every day, by Friday I'll have added at least twenty centimetres to my jump. Emma. Nice. What if it rains on Friday? Julia. If it rains, we'll move the races into the gym. But the weather app says sunny all week, so I don't think it will. Emma. Who's coming to watch you this year? Julia. The whole family is coming. Mum is bringing a lunch box of pancakes, Dad is going to film everything on his phone, and they're even bringing Barsik in his carrier — John says the team needs a mascot. Emma. Haha, a cat mascot? What about Turbo? Julia. Turbo is staying home — he's way too slow for a sports day! But I'll tell him all about it when I get back. He's a great listener. Emma. Shall we meet at nine at the main gate on Friday? Julia. Yes! And by eleven we'll have finished our race — then we can grab lunch and cheer for the other classes. Deal?", "-6%"),

    # ===== 5 · DEBATE MODEL =====
    "debate-model": (V_JULIA, "In my opinion, every kid should do some kind of sport, but it doesn't have to be the same one for everyone. On the one hand, moving your body every day really helps — you sleep better, you feel less stressed, and you also study better. However, on the other hand, I don't think we should force one kid to play soccer if they really prefer chess or drawing. For example, my little brother John hates team games — he always loses one sneaker and gets upset. But he loves climbing trees in the park, so Dad says that counts as sport too. All in all, I think kids should move for at least thirty minutes a day, but they should be free to choose how. Because if you force it, you'll just make them hate it forever.", "-6%"),

    # ===== 10.4 · SPEAK EACH OF 10 FUTURES (model answers) =====
    "fut-01-will":          (V_JULIA, "I think Emma will win the 60 metres, because she already beat me by three-tenths last week. But I will win my own personal best — that's also a win.", "-6%"),
    "fut-02-going-to":      (V_JULIA, "On Saturday I'm going to practise my long jump with Emma at 10 in the morning. On Sunday I'm going to go for a family walk in the park with Mama, Papa and John — Papa is going to time us running home.", "-6%"),
    "fut-03-about-to":      (V_JULIA, "The runner is about to push off the blocks. Her hands are on the ground. The coach is about to blow the whistle. In two seconds, the whole track is about to explode in noise.", "-6%"),
    "fut-04-will-be-ving":  (V_JULIA, "This time next Sunday at 11 I will be walking in the city park with my family. Barsik will be sitting at home on the windowsill, judging. Papa will be timing us as we race the last 100 metres to the gate.", "-6%"),
    "fut-05-will-have":     (V_JULIA, "By June I will have learned how to do a proper long jump and how to pace a 60-metre sprint. I'll also have tried basketball for the first time, because Papa promised to practise with me. I hope I'll have beaten my own record by at least one second.", "-6%"),
    "fut-06-pres-cont":     (V_JULIA, "On Friday after school I'm meeting Emma at the main gate at 4. We're running two laps and then we're grabbing a milkshake. Mama is picking us up at 5:30 sharp.", "-6%"),
    "fut-07-pres-simple":   (V_JULIA, "PE starts at 10 on Mondays and at 2 on Wednesdays. On Friday, the sports day begins at 9 with the opening parade and the first race starts at 10 sharp. The whole thing ends at 2.", "-6%"),
    "fut-08-shall":         (V_JULIA, "Emma, shall we go for a run after school tomorrow? Or shall we practise long jump in the pit? Shall I bring the stopwatch so we can time each other?", "-6%"),
    "fut-09-time-clauses":  (V_JULIA, "When I finish school tomorrow, I'll change into my sneakers and meet Emma on the field. As soon as I get home, I'll feed Turbo his cucumber. If it rains on Saturday, we'll move the practice into the gym.", "-6%"),
    "fut-10-soft":          (V_JULIA, "One day I'd love to try horseback riding. We don't have it at school, but there's a stable near our park. I'd also like to try tennis — Papa says tennis is the best sport for brain and body. I hope one day I'll run in the Olympics — even just once.", "-6%"),

    # ===== 7 · READING · 6 CHAPTERS (narrator) =====
    "story-ch1": (V_JULIA,
                  "Chapter 1. Monday. The chart on the fridge. "
                  "On Monday morning, before school, Julia stood in the kitchen and stared at the fridge. Dad had taped a new white paper to it with a magnet. At the top, in his careful handwriting: Julia's Sports Week, road to Friday. Below, five empty rows, one for each school day. "
                  "Every time you practise, we add a star, said Dad, drinking coffee. By Friday, if the chart is full, your new silver stopwatch time will be faster than Emma's last month. "
                  "Julia looked at her little brother John, who was eating a pancake sideways. You can add stars too, as long as you promise not to draw little snails everywhere. John frowned, he loved drawing Turbo. Mum laughed quietly. Barsik watched everything from the window sill, judging. "
                  "Outside, the first school bus was pulling up. Julia grabbed her backpack and ran.", "-6%"),

    "story-ch2": (V_JULIA,
                  "Chapter 2. Wednesday. The hardest practice. "
                  "By Wednesday afternoon, Julia's legs were on fire. She and Emma had already run four sprints and jumped eight long jumps. The sun was setting behind the gym. "
                  "Shall we go home? asked Emma, flopping onto the grass. No! said Julia. Dad said if we practise every day, by Friday we will have run twenty sprints. We've only done ten. Emma groaned. You are going to kill us. But she got up. They ran three more. "
                  "On the way home, Mum was waiting by the gate with a thermos. Tea with honey, she said. The runners' drink. Julia drank it in one gulp and smiled for the first time all afternoon. "
                  "Back home, she added two more stars to Dad's chart. John added a small drawing of Turbo wearing running shoes. Nobody told him to stop.", "-6%"),

    "story-ch3": (V_JULIA,
                  "Chapter 3. Thursday night. Dad's stopwatch story. "
                  "After dinner on Thursday, Dad took his old silver stopwatch off the kitchen drawer. This thing is older than you, John, he said. The watch was dented on one side. "
                  "I bought it before my first marathon, twenty-two years ago. I ran that race in four hours and nine minutes. Slow, but I finished. Julia held it carefully. The silver was cold. "
                  "On Friday I am giving it to you, Dad said. You hold it during Emma's race. Afterwards, we start it for your race. When you cross the finish line, you stop it. That's YOUR time now, not mine. "
                  "Julia's eyes filled up a little. Even Barsik meowed. Turbo didn't do anything, but that's normal for a snail. "
                  "Don't drop it, John said very seriously. I would never drop it, said Julia.", "-6%"),

    "story-ch4": (V_JULIA,
                  "Chapter 4. Friday morning. Pancakes for luck. "
                  "On Friday morning, the kitchen smelled of hot pancakes and honey. Mum had made a full stack. Eight for Julia, eight for the family, two for Barsik, who only ate one, as always. "
                  "Carbs for the race, Mum said, sliding one onto Julia's plate. John was already dressed in his GO JULIA t-shirt, holding the cardboard sign. "
                  "Look! he shouted. I spelled your name right this time! Julia looked. The J was backwards. Everyone laughed except John, who looked confused. "
                  "Dad put the silver stopwatch into Julia's hand. Pocket. Not backpack. You need to feel it. Julia nodded. She ate her pancakes slowly, Dad said fast eating equals heavy legs. "
                  "By 8:30 the whole family was walking out the door. Turbo stayed home. He was on vacation, in his small jar, eating a piece of cucumber. Julia blew him a kiss.", "-6%"),

    "story-ch5": (V_JULIA,
                  "Chapter 5. The race. Twenty seconds. "
                  "The whistle was in the coach's mouth. Julia was in lane 3, Emma in lane 4. "
                  "Ready, called the coach. Julia felt the stopwatch in her pocket, warm and round. Set. Her heart was pounding so loud she thought the whole crowd could hear it. GO. "
                  "The whistle blew. For one second Julia felt like she was flying. The wind, the grass, the shouting, all mixed together. "
                  "By the ten-metre mark, Emma was half a step ahead. Julia pushed harder. Fifteen metres. Twenty. Thirty. Emma was still ahead. Forty. Fifty. Julia could hear Mum's voice above everyone else: COME ON JULIA! "
                  "Fifty-eight metres. Sixty. The finish-line tape touched her shoulder, and then Emma's. Both girls fell forward onto the grass, laughing, gasping. "
                  "Julia's hand shot into her pocket. STOP. She looked at the stopwatch. Nine point seven two seconds. A new personal best. Emma was nine point six five. "
                  "You won! said Julia. Emma hugged her. You beat your own time by three-tenths. Dad is going to lose his mind.", "-6%"),

    "story-ch6": (V_JULIA,
                  "Chapter 6. Friday evening. Telling Barsik and Turbo. "
                  "That evening, Julia sat on her bedroom floor with her silver medal around her neck and the stopwatch in her hand. Barsik sat in front of her, blinking slowly, clearly bored. Turbo moved maybe one centimetre in ten minutes, his idea of listening. "
                  "I came second, Julia told them. But it's the best second I've ever had. Nine point seven two. That's MY time now. Next year I am going to be faster than Emma, probably. And if I'm not, I'll just be faster than me. "
                  "Barsik yawned. Also, Dad said next summer we will do a 5K together, all four of us, plus Emma. Not you, Barsik. You will stay with Turbo. "
                  "Barsik seemed relieved. Julia smiled, put the stopwatch on her nightstand, and turned off the lamp. Tomorrow, pancakes again. Mum had promised.", "-6%"),

    # ===== kept as backup (old single-passage version) =====
    "story-full": (V_JULIA,
                   "Monday, the plan. It is Monday morning and Julia is at her school in a small American town. Next Friday is the big sports day — the biggest event of the whole semester. This year Julia is going to run the sixty metres and jump into the long jump pit. Her best friend Emma, who sits next to her in class, is going to run with her. Every day this week they are practising in the schoolyard at four o'clock. By Friday morning they will have run twenty short sprints together. Dad even keeps a chart on the fridge. "
                   "Shall we run one more time? asks Emma on Thursday, already a little tired. Yes, let's! says Julia. And after practice, Mum promised us pancakes with honey and raspberry jam. "
                   "Friday morning, the family. On Friday, the sun shines and the air smells of cut grass. Mum, Dad and John are all in the crowd. Mum is holding a lunch box — inside: two flasks of water and a stack of golden pancakes. Dad has his old silver stopwatch in his hand. I bought this for my first marathon, he loves to say. It still works perfectly. John has a big sign that says GO JULIA — the I is backwards, but nobody minds. Even Barsik is there, sitting quietly in his cat carrier in a tiny team t-shirt. Barsik is NOT happy about the whistle. Turbo the snail stayed home — he's way too slow for a sports day. "
                   "The race. The whistle is about to blow. Julia's heart is beating fast — thump, thump, thump. I think I'll win! she whispers to Emma. Emma just smiles and nods. When the whistle blows, both girls shoot forward like arrows. The wind is in Julia's hair, the crowd is cheering, and Mum's voice is the loudest of all. For twenty seconds it's just her, Emma, and the finish line. "
                   "Julia does NOT win the gold medal — Emma does, by half a second. But Julia gets the silver medal. I'm so happy! she says, hugging Emma. Next year I will run even faster. One day I'd like to run in the Olympics. Will you come, Mum? "
                   "Yes, darling, Mum laughs. I'll be there with John, Barsik and Turbo. By then your Dad will have taught John to spell your name on his sign — AND the right way around. Dad smiles, looks at the stopwatch, and quietly adds Julia's new best time to the chart.", "-6%"),

    # ===== 11 · VOCAB CAPSULE (30 items) =====
    "vocab-run":        (V_JULIA, "to run.", "+0%"),
    "vocab-jump":       (V_JULIA, "to jump.", "+0%"),
    "vocab-race":       (V_JULIA, "to race.", "+0%"),
    "vocab-practise":   (V_JULIA, "to practise.", "+0%"),
    "vocab-throw":      (V_JULIA, "to throw.", "+0%"),
    "vocab-catch":      (V_JULIA, "to catch.", "+0%"),
    "vocab-kick":       (V_JULIA, "to kick.", "+0%"),
    "vocab-win":        (V_JULIA, "to win.", "+0%"),
    "vocab-lose":       (V_JULIA, "to lose.", "+0%"),
    "vocab-cheer":      (V_JULIA, "to cheer.", "+0%"),
    "vocab-stretch":    (V_JULIA, "to stretch.", "+0%"),
    "vocab-climb":      (V_JULIA, "to climb.", "+0%"),
    "vocab-pit":        (V_JULIA, "pit.", "+0%"),
    "vocab-sprint":     (V_JULIA, "sprint.", "+0%"),
    "vocab-lap":        (V_JULIA, "lap.", "+0%"),
    "vocab-ball":       (V_JULIA, "ball.", "+0%"),
    "vocab-team":       (V_JULIA, "team.", "+0%"),
    "vocab-match":      (V_JULIA, "match.", "+0%"),
    "vocab-score":      (V_JULIA, "score.", "+0%"),
    "vocab-goal":       (V_JULIA, "goal.", "+0%"),
    "vocab-whistle":    (V_JULIA, "whistle.", "+0%"),
    "vocab-coach":      (V_JULIA, "coach.", "+0%"),
    "vocab-stopwatch":  (V_JULIA, "stopwatch.", "+0%"),
    "vocab-sneakers":   (V_JULIA, "sneakers.", "+0%"),
    "vocab-pe":         (V_JULIA, "P.E. lesson.", "+0%"),
    "vocab-sportsday":  (V_JULIA, "sports day.", "+0%"),
    "vocab-medal":      (V_JULIA, "medal.", "+0%"),
    "vocab-podium":     (V_JULIA, "podium.", "+0%"),
    "vocab-record":     (V_JULIA, "record.", "+0%"),
    "vocab-crowd":      (V_JULIA, "crowd.", "+0%"),
}


async def synth_one(key, voice, text, rate):
    """Generate one mp3 with retry on 403 (edge-tts token rotation)."""
    out = AUDIO_DIR / f"{key}.mp3"
    if out.exists() and out.stat().st_size > 1024:
        return "skip"
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(str(out))
        if out.exists() and out.stat().st_size < 1024:
            out.unlink(missing_ok=True)
            return "zero"
        return "ok"
    except Exception as e:
        if out.exists() and out.stat().st_size < 1024:
            out.unlink(missing_ok=True)
        return f"err: {e}"


async def main():
    retry_pass = 0
    while retry_pass < 3:
        pending = [(k, v, t, r) for k, (v, t, r) in CLIPS.items()
                   if not (AUDIO_DIR / f"{k}.mp3").exists()
                   or (AUDIO_DIR / f"{k}.mp3").stat().st_size < 1024]
        if not pending:
            print(f"\nOK: all {len(CLIPS)} clips present.")
            return
        print(f"\n=== pass {retry_pass+1} - {len(pending)} clips to build ===")
        results = {}
        for k, v, t, r in pending:
            res = await synth_one(k, v, t, r)
            results[k] = res
            tag = "OK " if res == "ok" else ("SKIP" if res == "skip" else "ERR ")
            try:
                print(f"  {tag} {k}  [{res}]")
            except Exception:
                print(f"  {tag} {k}  [got error - cannot print details]")
        failed = [k for k, r in results.items() if r not in ("ok", "skip")]
        if not failed:
            print(f"\nOK: pass {retry_pass+1} clean - all built.")
            return
        print(f"\n{len(failed)} failed - sleeping 5s before retry ...")
        await asyncio.sleep(5)
        retry_pass += 1
    print(f"\nSTOP: after 3 passes. Remaining failures - check manually.")


if __name__ == "__main__":
    asyncio.run(main())
