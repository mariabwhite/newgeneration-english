"""Round 2 TTS: Sydney, Girls, Ant & Grasshopper, Julia, Dogs, Billy Elliot."""
import asyncio, os, sys
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets', 'audio')
os.makedirs(OUT, exist_ok=True)

V_UK_F = 'en-GB-LibbyNeural'
V_UK_M = 'en-GB-RyanNeural'
V_US_F = 'en-US-AriaNeural'
V_US_M = 'en-US-GuyNeural'
V_AU_F = 'en-AU-NatashaNeural'    # Aussie for Sydney
V_AU_M = 'en-AU-WilliamNeural'
V_BRIT_YOUNG = 'en-GB-SoniaNeural'  # for Billy Elliot narration

CLIPS = [
    ('t6-a-barangaroo.mp3', V_AU_F,
     "Barangaroo Reserve has more than 75,000 native trees and bushes, "
     "as well as walking and cycling tracks. "
     "This 22-hectare waterfront area is a lovely spot for a stroll or bike along the harbour. "
     "You can also find a lot of shops, restaurants, and event and exhibition space here."),

    ('t6-b-qvb.mp3', V_AU_M,
     "If you have some money to spend, you should go to the Romanesque-style Queen Victoria Building, or 'QVB'. "
     "Even if you're not planning to buy anything, it's worth a visit just to admire this beautifully restored building "
     "and its colourful windows and mosaic floors."),

    ('t6-c-opera.mp3', V_AU_F,
     "The Sydney Opera House is an iconic building on the shores of Sydney Harbour in Sydney, Australia. "
     "It is shaped like the sails of a boat. Many concerts and events take place there, "
     "with 2000 performances a year presented by Opera Australia, Australia's national opera company."),

    ('t6-d-rocks.mp3', V_AU_M,
     "The Rocks became established in 1788. Now it's a fantastic base for sightseeing. "
     "Spectacular harbour views, heritage-listed buildings, museums, shops, galleries and cute cafés "
     "make this area a great place to stay. From here, many of Sydney's top tourist attractions "
     "are within easy walking distance, including the Sydney Harbour Bridge, the Opera House, "
     "and the Royal Botanic Gardens."),

    ('t6-e-taronga.mp3', V_AU_F,
     "One of Sydney's most famous attractions is home to over 4,000 animals, "
     "including Australian native wildlife, as well as rare and endangered exotic animals. "
     "Here, you can enjoy close-up encounters with iconic Aussie wildlife and other animals from around the world. "
     "Highlights include the African Savannah exhibit, Tiger Trek, chimpanzees and gorillas."),

    ('t7-girls.mp3', V_US_F,
     "It is no surprise that girls spend more time doing unpaid household chores than boys. "
     "Girls spend 40 per cent more time, which is 160 million more hours every day. "
     "In some countries, this figure is a lot higher. A report from the United Nations children's agency UNICEF "
     "highlights this gap. According to the report, many girls lose important chances to learn, "
     "grow and enjoy their childhood. The report also says that this inequality among children means "
     "gender stereotypes continue and women and girls have to do more work across generations. "
     "Most work done by girls is very physical. Most girls cook, clean, collect firewood or water "
     "and care for children and elderly relatives. In some African countries, girls spend 26 hours a week "
     "on household chores. Knowing the problems girls face is the first important step towards gender equality."),

    ('t8-ant.mp3', V_US_M,
     "Once upon a time there lived an ant and a grasshopper in a grassy meadow. "
     "All day long the ant worked very hard, collecting grains of wheat from a farmer's field. "
     "She hurried to the field every morning, as soon as it was light enough to see by, "
     "and came back with a heavy grain of wheat balanced on her head. "
     "She put the grain of wheat carefully away in the storage, "
     "and then hurried back to the field for another one. "
     "All day long she worked, without stop or rest, going back and forth from the field, "
     "collecting the grains of wheat and storing them carefully at home. "
     "The grasshopper looked at the ant and laughed. "
     "'Why do you work so hard, dear ant? Come, rest a bit, listen to my song. "
     "Summer is here, the days are long and bright. Why waste this sunshine?' "
     "The ant ignored him and just hurried to the field a little faster. "
     "'What a silly little ant you are!' he said to the ant. "
     "'Come, come and dance with me! Forget about work! Enjoy the summer! Live a little!' "
     "And then the grasshopper hopped away, singing and dancing merrily. "
     "Summer faded into autumn, and autumn turned into winter. "
     "The sun was hardly seen, and the days were short and grey, the nights were long and dark. "
     "It became freezing cold, and snow began to fall. "
     "The grasshopper didn't want to sing any more. He was cold and hungry. "
     "He had nowhere to shelter from the snow, and nothing to eat. "
     "The meadow and the farmer's field were covered in snow, and there was no food for him to eat. "
     "'Oh, what shall I do? Where shall I go?' cried the poor grasshopper. "
     "Suddenly he remembered the ant. 'Ah, I'll ask the ant for food and shelter!' said the grasshopper happily. "
     "So off he went to the ant's house and knocked at her door. "
     "'Hello, ant!' he cried cheerfully. 'Here I am, to sing for you, as I warm myself by your fire, "
     "while you get me some food from that storage of yours!' "
     "The ant looked at the grasshopper and said, 'All summer long I was working hard. "
     "And all you did was making fun of me, singing and dancing. "
     "Why didn't you think of winter then? Find somewhere else to sing, grasshopper! "
     "There is no food for you here!' And the ant shut the door in the grasshopper's face. "
     "It is wise to worry about tomorrow today."),

    ('t9-julia.mp3', V_UK_F,
     "Someone I admire is my cousin Julia. She's five years older than me, so she's 17 now "
     "and she lives in Bristol. She's very friendly and confident "
     "and she's got long, wavy, brown hair and brown eyes. "
     "She's medium height, slim and very fit because she's a dancer. "
     "She's been dancing since she was six years old and trains every day at her dance school. "
     "She wants to be a famous dancer, but it's a very uneasy profession because it's so competitive. "
     "She often dances in shows and I love watching her dance. "
     "Laura is very busy because she also studies photography at university. "
     "She's a really good photographer and has taken lots of amazing photos of me and my family. "
     "Her photos have won a few prizes and last year one of her photos was in an exhibition "
     "at an art gallery in London. Laura doesn't have a lot of free time "
     "and she's also trying to learn Chinese because she wants to go to China next year "
     "to do a photography course. I think Laura is very hard-working "
     "and she will become a professional dancer one day."),

    ('t10-dogs.mp3', V_US_F,
     "Research says climate change transformed dogs from animals resembling cats to how they look today. "
     "Researchers say that 40 million years ago, dogs were smaller and hunted and ambushed their prey like cats. "
     "The changing climate reduced the number of forests in North America, "
     "so the shape and food-gathering habits of dogs changed. "
     "New grasslands meant dogs had fewer places to hide to ambush their victims. "
     "They changed their hunting styles and grew longer legs. "
     "Scientists looked at how dogs evolved by looking at the elbows and teeth of 32 different species "
     "that lived up to 40 million years ago. "
     "The dogs' elbows and teeth clearly showed evolutionary change. "
     "Dogs used to have elbows like those of cats. "
     "The front paws swivelled so they could grab and hold on to their prey. "
     "Elbows changed in dogs to let them run farther. "
     "This meant they could chase their prey over long distances. "
     "The teeth in dogs became harder and more efficient so they could keep the prey they caught."),

    ('t11-billy-elliot.mp3', V_BRIT_YOUNG,
     "Miss says I've got promise. She spends half the lesson just teaching me — "
     "she doesn't bother with the others half the time. They're always moaning on about it. "
     "'Can we have a go, miss? When's it our turn, miss? It's not fair, miss, just because he's a boy, miss…' "
     "'Shut up, Debbie, I'm busy.' "
     "Oh, I was looking forward to the Saturday lesson all week. "
     "Once I started, I could just go on for ever. It was right what Miss said about stamina. "
     "It may look easy, but it's not. It's hard, but I could keep going for hours. "
     "I must have been mad to go to ballet class instead of boxing. "
     "It had to happen. Michael kept warning me. 'Dad will find out. What are you going to do then?' "
     "I knew he was right, but I kept thinking, just this week, just one more lesson, "
     "then I'll go back to the boxing. And I got more and more into it, and better and better at it, "
     "and Dad never turned up to watch me boxing any more… I just thought it was going to go on forever. "
     "And of course, he unexpectedly turned up right in the middle of class. "
     "'Pick up your leg, Billy. Swing it! Swing two three, round two three, up two three. "
     "What do you call that? Let's have a bit of grace, Billy Elliot!' "
     "I was swinging my leg round, slow circle, trying to make it as smooth as cream — "
     "and I looked up and there was my dad standing in the door. "
     "I just froze. I thought I was going to die. "
     "I thought he was going to rush out and kill me. "
     "Miss was still going on… 'Up two three, swing two three. Like a princess, Deborah. "
     "Beautiful necks! One two three… what's up with you?' "
     "She said that when she saw me standing still. "
     "Then the music stopped and she turned round and saw Dad. He'd gone blood red. "
     "'You! Out! Now!' he snapped. "
     "I could see her out of the corner of my eye, leaning forward towards him as if she could eat him. "
     "The last thing I wanted was a screaming match between her and my dad. "
     "I started walking towards him. 'Please, miss. Don't,' I hissed as I went past. "
     "It was so embarrassing. Dad thought I was a wimp for dancing; "
     "she thought I was a wimp for not standing up to him. I'd had it. "
     "The door banged behind me. He grabbed my arm and pushed me in front. "
     "'Right, you've got some explaining to do,' he said. And he marched me home."),
]


async def tts_one(filename, voice, text, rate='-6%'):
    path = os.path.join(OUT, filename)
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        print(f'skip (exists): {filename}')
        return
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(path)
        size = os.path.getsize(path)
        print(f'ok: {filename}  voice={voice}  {size} bytes')
    except Exception as e:
        print(f'FAIL {filename}: {e}')
        if os.path.exists(path) and os.path.getsize(path) == 0:
            os.remove(path)


async def main():
    for filename, voice, text in CLIPS:
        await tts_one(filename, voice, text)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(main())
