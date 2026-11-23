"""Round 3 TTS: Mustangs, Dolphins, Robert & the dog, and (optional) placeholder for t15."""
import asyncio, os, sys
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets', 'audio')
os.makedirs(OUT, exist_ok=True)

V_US_F = 'en-US-AriaNeural'
V_US_M = 'en-US-GuyNeural'
V_UK_F = 'en-GB-LibbyNeural'
V_UK_M = 'en-GB-RyanNeural'
V_NG = 'en-NG-AbeoNeural'   # Nigerian English male — right origin for Ken Saro-Wiwa adaptation

CLIPS = [
    ('t12-mustangs.mp3', V_US_M,
     "The image of horses running freely across the plains is a popular symbol of the American West. "
     "However, mustangs are not native to the United States. "
     "When Spanish armies came to the New World in the sixteenth century, they brought horses with them. "
     "Horses had been extinct in the Americas for about twelve thousand years. "
     "The wild horses that now live in the western part of the United States are called mustangs. "
     "The word comes from the Spanish word mesteño, meaning wild or stray. "
     "The mustangs' ancestors were Spanish horses that had escaped from Spanish soldiers. "
     "Over many years, the mustang population in the western United States grew. "
     "By the end of the nineteenth century, about two million mustangs roamed the countryside. "
     "Farmers and ranchers complained that the mustangs destroyed their crops "
     "and ate food meant for farm animals. "
     "Some mustangs were used in movies about the Wild West. "
     "Although some people tried to protect wild horses as early as 1925, "
     "the mustang population kept shrinking because many farmers killed them "
     "or removed them from the western plains and prairies. "
     "By 1970, fewer than seventeen thousand mustangs remained in the USA. "
     "In 1971, the US Congress passed a law to protect these wild horses. "
     "Today, the government manages areas with too many mustangs. "
     "Some of the horses are even offered for adoption. "
     "About thirty-seven thousand mustangs currently live in the United States."),

    ('t13-dolphins.mp3', V_US_F,
     "Dolphins are amazing animals. Weighing over 1,000 pounds and growing up to 12 feet long, "
     "dolphins are mammals that need air to survive. "
     "Every 15 minutes or so, dolphins rise to the surface of the water "
     "to breathe through a blowhole on top of their bodies. "
     "To continue breathing and prevent drowning while they rest, "
     "dolphins sleep with only half of their brain at a time! "
     "They close one eye and sleep near the surface of the water, "
     "swimming slowly and coming up for air. "
     "This is called 'logging' because the slow-moving dolphins look like floating logs. "
     "There are about 40 different kinds of dolphins, "
     "and they all use a special ability called echolocation to find food in the water. "
     "Dolphins send out sound waves that bounce off objects "
     "and come back as echoes that tell them where the object is. "
     "Dolphins also talk to one another through a series of clicking sounds — "
     "sometimes making up to 300 sounds per second."),

    ('t15-robert.mp3', V_NG,
     "Robert's new employer was a young medical doctor just returned from abroad. "
     "He was cheerful, exuberant and polite. He did not once lose his temper, "
     "he did not shout at Robert, he called him by his first name, "
     "and always asked him about his wife, children and other members of his family. "
     "Robert thought he had at last found fulfilment, the more so as the young doctor appeared to be a bachelor. "
     "Stewards, including Robert, prefer to serve a bachelor. "
     "Because every bachelor is as wax in the hands of his steward. "
     "The latter decides what is to be spent on grocery, how much food is to be served at meal times, "
     "what is to be done with the remnants of food. "
     "In short, he holds the bachelor's life in his hands. And that is tremendous power. "
     "So, Robert quickly settled into his new situation and took full control of the house. "
     "There was no wife breathing down Robert's neck and limiting his authority. "
     "There were no children whose nappies and numerous clothes had to be washed. "
     "He did not have to cook several meals a day. "
     "The young man ate but once a day, except for the cup of coffee and toast early in the morning. "
     "Trouble began when the young man announced after six months that his wife was about to join him. "
     "Robert's face fell visibly at the announcement. "
     "But who knew, the lady might not be an ogre after all. "
     "Which is precisely what happened in the event. "
     "The lady was as young and cheerful as her husband. She, too, took an interest in Robert. "
     "She was European and excited about her first visit to Africa. "
     "She appeared pleased to have Robert's assistance. "
     "She spent the day asking Robert about African food, "
     "watching Robert at work in the kitchen and lending a helping hand where possible. "
     "She made sure Robert stopped work early so that he could get home to his family, "
     "and she did not make a fuss if Robert turned up late some odd mornings. "
     "Robert began to feel like a human being, and he felt extremely grateful to his new employers. "
     "The only source of worry in the new situation was the dog. "
     "For the young lady had arrived with a dog called Bingo. "
     "And Robert watched with absolute amazement and great incredulity as the lady spoke tenderly to the dog. "
     "She ensured that he was well fed and she held the dog lovingly in her arms, "
     "brushed his hair and tended him carefully. "
     "The dog appeared as important to the lady as her husband and, indeed, Robert thought, "
     "in the order of things, the dog was more important than himself. "
     "And he detested this state of affairs. "
     "He could understand a stray, dirty dog with flies around its ears being beaten "
     "and chased away from the dwellings of men. "
     "He could understand a dog wandering around rubbish heaps in search of food. "
     "But a dog who slept on the sofa, a dog who was fed tinned food on a plate, "
     "a dog who was brushed and cleaned, a dog who drank good tinned milk, "
     "was entirely beyond his comprehension. "
     "On one occasion, the lady took the dog to a doctor. "
     "And that was the straw that broke the camel's back. "
     "All that day, Robert felt his stomach turn and when he got home in the evening "
     "and saw his children, with distended stomachs, playing on the dirty road near the door, "
     "and watched them hungrily swallow their food, he asked himself, 'Who born dog?' "
     "And all of a sudden he developed a pathological hatred for Bingo the dog, "
     "his master's dog."),
]


async def tts_one(filename, voice, text, rate='-6%'):
    path = os.path.join(OUT, filename)
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        print(f'skip (exists): {filename}')
        return
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(path)
        print(f'ok: {filename}  voice={voice}  {os.path.getsize(path)} bytes')
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
