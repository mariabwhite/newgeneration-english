"""Generate audio-first voice tracks for every reading passage.

Rule: audio comes before the text in every section. Uses edge-tts.

If edge-tts hits a 403 (Microsoft token rotation), re-run — it only skips
files that are missing or 0-byte.
"""
import asyncio, os, sys
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'assets', 'audio')
os.makedirs(OUT, exist_ok=True)

# Prefer a natural British voice for Bath / Haka / UK-sport texts,
# a storytelling voice for the Wolf fable, and a warm voice for the reading passage.
VOICE_UK_FEMALE = 'en-GB-LibbyNeural'
VOICE_UK_MALE   = 'en-GB-RyanNeural'
VOICE_US_FEMALE = 'en-US-AriaNeural'
VOICE_STORY     = 'en-US-GuyNeural'

CLIPS = [
    ('t1-a-sally-lunns.mp3', VOICE_UK_FEMALE,
     "Sally Lunn's is one of the oldest houses in Bath, from around 1482, "
     "and serves one of the most famous local delicacies — the original Sally Lunn bun, "
     "a unique pastry known for its light and fluffy texture. "
     "This delightful treat still makes Sally Lunn's a popular spot for both locals and tourists "
     "seeking a memorable dining experience. No trip to Bath is complete without indulging in a bun!"),

    ('t1-b-bath-abbey.mp3', VOICE_UK_MALE,
     "Bath Abbey is a stunning architectural masterpiece located in the heart of Bath, "
     "known for its impressive Perpendicular Gothic style. Founded in the seventh century, "
     "it features intricate fan vaulting and beautiful stained-glass windows that create a serene atmosphere. "
     "The iconic west front showcases unique sculptures of angels on ladders, "
     "symbolising a connection to heaven. Visitors can explore its rich history, "
     "attend various events, or simply enjoy the peaceful ambience of this remarkable landmark."),

    ('t1-c-the-circus.mp3', VOICE_UK_FEMALE,
     "The Circus in Bath is an impressive circular structure designed by John Wood the Elder, "
     "completed in 1768. It features three distinct tiers of classical architecture: "
     "Doric at the bottom, Ionic in the middle, and Corinthian at the top. "
     "Inspired by the Colosseum, its unique design creates a sense of movement and elegance. "
     "Notably, it has been home to famous figures such as the artist Thomas Gainsborough "
     "and the explorer David Livingstone, who lived there with their families. "
     "Today, it is still possible to live in this historic location, making it a blend of heritage and modern living. "
     "The Circus is surrounded by trees and is accessed via three streets, "
     "enhancing its visual appeal and architectural significance."),

    ('t1-d-jane-austen.mp3', VOICE_UK_FEMALE,
     "The Jane Austen Centre in Bath offers a captivating glimpse into the life of the famous author "
     "and her connection to the city. Set in a charming Georgian townhouse, "
     "visitors can enjoy engaging exhibitions that highlight the Regency era's fashion, food and society. "
     "The Centre features a life-size wax figure of Jane Austen, allowing guests to see what she might have looked like. "
     "Additionally, visitors can participate in dressing up in period costumes and enjoy delightful refreshments "
     "in the Regency Tea Room, enhancing their experience of Austen's world."),

    ('t1-e-roman-thermae.mp3', VOICE_UK_MALE,
     "The Roman Thermae in Bath is an extraordinary historical site that showcases the ancient Roman approach "
     "to leisure and wellness. Built around natural hot springs, it features impressive architecture "
     "with large columns and intricate mosaics. Visitors can explore various rooms designed for different temperatures, "
     "including warm, hot and cool areas. The complex also includes a museum displaying artifacts from Roman times, "
     "making it a fascinating destination for those interested in history and culture. "
     "Guided tours offer deeper insights into its significance."),

    ('t2-haka.mp3', VOICE_US_FEMALE,
     "The haka is a traditional Maori dance from New Zealand, which is known for its powerful movements "
     "and rhythmic chanting. It is performed by groups, often featuring vigorous foot stomping, body slapping "
     "and expressive facial gestures. The haka has deep cultural roots, celebrating life and nature "
     "rather than just war. Historically, it was used to welcome guests or mark important occasions, "
     "such as weddings and funerals. "
     "One of the most famous haka is 'Ka Mate', created by chief Te Rauparaha in the nineteenth century. "
     "Today, the haka is widely recognised globally, especially through its performance "
     "by New Zealand's national rugby team, the All Blacks, before matches. "
     "This ritual showcases Maori culture and promotes unity and strength among the players. "
     "The haka continues to evolve, with modern performances including women and children. "
     "It remains a vital expression of Maori identity and heritage, "
     "connecting the past with contemporary society. "
     "Whether at sports events or cultural celebrations, the haka captivates audiences "
     "with its energy and significance, making it a cherished part of New Zealand's cultural landscape."),

    ('t3-wolf.mp3', VOICE_STORY,
     "Once upon a time, there was a greedy Wolf who loved to eat. "
     "One day, he feasted too much and got a bone stuck in his throat. "
     "The bone was stuck crosswise, and he could not swallow it or bring it up. "
     "This made the Wolf very uncomfortable because he could not eat anything else. "
     "He felt desperate and needed help. "
     "The Wolf thought of the Crane, who had a long neck and a sharp bill. "
     "He believed that she could easily reach inside his throat and pull out the bone. "
     "So, he hurried to find her. When he found the Crane, he said: "
     "'Please help me! If you pull that bone out for me, I will reward you very generously.' "
     "The Crane was nervous about putting her head inside the mouth of a Wolf. "
     "She knew that wolves were dangerous animals. However, she was also greedy and wanted the reward. "
     "After some hesitation, she decided to help him. "
     "Carefully, the Crane reached into the Wolf's mouth with her long neck and pulled out the bone. "
     "The Wolf felt relieved and happy. He was able to eat again! "
     "But as soon as the bone was gone, the Wolf turned to leave without saying thank you. "
     "The Crane called after him: 'But what about my reward?' "
     "She felt anxious and worried that she would get nothing for her help. "
     "The Wolf turned around angrily and snarled: "
     "'What? Haven't you got your reward? Isn't it enough that I let you take your head out of my mouth?' "
     "The Crane was shocked by his response. "
     "She realised that she would not receive any gratitude from the Wolf. "
     "This story teaches us an important lesson: expect no reward for serving the wicked. "
     "It reminds us to be careful when helping those who are selfish or ungrateful, "
     "as they may not appreciate our kindness at all."),

    ('t4-arm.mp3', VOICE_UK_MALE,
     "Arm wrestling has become a popular and enjoyable sport in the UK, "
     "attracting many people who want to test their strength. "
     "This sport is different from many others because it requires not only physical power but also technique. "
     "Competitors twist their arms in various ways to gain an advantage over their opponent. "
     "In recent years, arm wrestling clubs have grown across the country, "
     "making it easier for enthusiasts to join and practise. "
     "Many people find this sport handy for building strength and improving fitness, "
     "although some may consider it unhealthy if done excessively. "
     "Despite its rising popularity, some newcomers may feel that winning is impossible at first. "
     "However, with practice and dedication, anyone can improve their skills. "
     "The sport offers a unique way to connect with others while having fun and staying active. "
     "Arm wrestling in the UK continues to grow, proving that strength and camaraderie can go hand in hand."),

    ('t5-reading.mp3', VOICE_US_FEMALE,
     "Reading is a popular hobby enjoyed by millions of people around the world. "
     "It brings excitement and adventure into our lives, allowing us to explore extraordinary stories "
     "without leaving our homes. Many readers love detective novels, where they can solve mysteries "
     "alongside the characters. With a magnifying glass in mind, they search for clues and try to figure "
     "out the plot twists before the ending. "
     "For some, reading becomes an obsession. They collect books and spend hours lost in different worlds, "
     "never wanting to give up on a good story. Whether it's a humorous tale or a thrilling mystery, "
     "every book offers something new and interesting. "
     "However, there are times when readers accidentally give away spoilers to friends who haven't finished "
     "the book yet. This can lead to funny situations and playful arguments about revealing too much! "
     "Despite these little mishaps, reading remains a beloved pastime. "
     "It helps us relax and escape from everyday life while improving our imagination and vocabulary. "
     "Whether curled up in bed or sitting in a cafe, readers find joy in every page they turn. "
     "Reading is truly a wonderful hobby that connects people and sparks their creativity."),
]


async def tts_one(filename, voice, text, rate='-6%'):
    path = os.path.join(OUT, filename)
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        print(f'skip (exists): {filename}')
        return
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    try:
        await communicate.save(path)
        size = os.path.getsize(path)
        print(f'ok: {filename}  voice={voice}  {size} bytes')
    except Exception as e:
        print(f'FAIL {filename}: {e}')
        # remove 0-byte file if created
        if os.path.exists(path) and os.path.getsize(path) == 0:
            os.remove(path)


async def main():
    for filename, voice, text in CLIPS:
        await tts_one(filename, voice, text)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    asyncio.run(main())
