"""Generate 3 city-reading mp3 files for the Japan lesson via edge-tts.

Usage (from the audio/ folder):
    py -3 _gen.py

Retries each clip on 403 per reference_edge_tts_403_retry.md.
"""
import asyncio, os, time, edge_tts

TEXTS = {
    "story-47-ronin.mp3": (
        "The forty-seven ronin. "
        "... "
        "In 1701, a young lord named Asano Naganori arrived at the shogun's court in Edo. "
        "There, a court official called Kira insulted him in public, again and again. "
        "Finally Asano lost his temper, drew his sword, and wounded Kira. "
        "In the shogun's palace, drawing a blade was unforgivable. The same day, Asano was ordered "
        "to commit seppuku — ritual suicide. His lands were taken, and his samurai became ronin: "
        "masterless warriors. "
        "... "
        "Forty-seven of them refused to accept this. "
        "Led by Oishi Kuranosuke, they spent almost two years pretending to be drunks, merchants, "
        "or broken men, so that Kira would stop watching them. "
        "Then, on a snowy December night in 1703, they met in secret, put on armour, and stormed "
        "Kira's mansion in Edo. They found him hiding in a coal shed. They took his head to the "
        "grave of their dead lord Asano. "
        "... "
        "The next morning, all forty-seven surrendered. The shogun allowed them to die with honour. "
        "They committed seppuku together. "
        "Today, their graves stand side by side at Sengakuji temple in Tokyo. "
        "People still leave incense there — more than three hundred years later."
    ),
    "story-tanabata.mp3": (
        "Tanabata — the festival of the star-crossed lovers. "
        "... "
        "In the old sky, there is a great river of light — what we on Earth call the Milky Way. "
        "On one side of this river lived a princess called Orihime. She was the daughter of the Sky "
        "King, and she wove beautiful cloth for the gods every day. But she was lonely. "
        "... "
        "Her father felt sorry for her. On the other side of the sky-river he saw a hard-working "
        "cow-herd called Hikoboshi. The King introduced them — and they fell completely in love. "
        "They married. "
        "... "
        "But love made them forget their work. Orihime stopped weaving, and Hikoboshi let his cows "
        "wander across the sky. The King became angry. He separated them: Orihime on one bank of "
        "the sky-river, Hikoboshi on the other. "
        "Orihime cried so much that her father agreed to one thing. "
        "... "
        "Once a year — on the seventh night of the seventh month — a bridge of magpies would form "
        "across the Milky Way, and the lovers could meet, for one night only. "
        "If it rains on that night, the magpies can't come, and the lovers must wait another year. "
        "... "
        "Every July across Japan, people hang coloured paper wishes on bamboo trees. "
        "They write their deepest hopes on these strips, in memory of Orihime and Hikoboshi — "
        "and in hope that the sky will stay clear."
    ),
    "story-kintsugi.mp3": (
        "Kintsugi — the beauty of broken things. "
        "... "
        "When a ceramic bowl breaks in Japan, there is an old tradition. "
        "The master does not throw the bowl away. "
        "He does not even try to hide the cracks. "
        "Instead, he mixes lacquer with powdered gold, and he uses this gold glue to join the pieces "
        "back together. "
        "This art is called kintsugi — golden joinery. "
        "... "
        "The crack does not disappear. It shines. "
        "The bowl now tells its own history: here is where it fell, here is where it was repaired, "
        "here is where it became stronger. "
        "Many collectors believe that a bowl after kintsugi is more beautiful than before. "
        "... "
        "Modern Japan uses kintsugi as more than an art. It is a quiet philosophy. "
        "After the Tohoku earthquake and tsunami of 2011, after Hiroshima in 1945, after every "
        "disaster — the country does not pretend nothing happened. "
        "It fills the cracks with gold, and keeps going. "
        "... "
        "The message of kintsugi is simple: "
        "you are not less beautiful because you broke. "
        "You are more beautiful, because you were put back together — with care, with gold, and in "
        "full view of everyone who comes to drink from the bowl."
    ),
    "reading-three-faces.mp3": (
        "Japan is a country of contrasts. People usually describe it as the Land of the Rising Sun, "
        "but there is no single Japan. There are at least three faces, and each face tells a different story. "
        "... "
        "Kyoto is the old face. It was the capital for more than a thousand years. Right now, visitors are "
        "walking through quiet shrines, drinking green tea, and watching geishas on the street. Nobody is in "
        "a hurry here. Life follows old traditions — politeness, respect for silence, and the slow rhythm of "
        "the tea ceremony. "
        "... "
        "Tokyo is the fast face. During rush hour, millions of commuters move through the stations. Many "
        "people work long hours, and pressure is part of daily life. These days, Tokyo is becoming even more "
        "international. Technology is everywhere, but something is missing — many residents feel urban "
        "loneliness, and nobody really talks on the metro. "
        "... "
        "Okinawa is the green face. The islands are far in the south, with warm weather all year. People "
        "live longer there than almost anywhere in the world. Why? A strict diet, a lot of walking, and a "
        "strong community. In Okinawa, there is always somebody to help a neighbour. Nothing happens in a "
        "hurry, and everything has its own time. "
        "... "
        "Three faces, one country. Modern life and old tradition live side by side."
    ),
    "kyoto-reading.mp3": (
        "Kyoto was the capital of Japan for more than a thousand years, from 794 to 1868. "
        "Today, Kyoto is a city of about 1.4 million people, and it keeps more than 1,600 temples "
        "and 400 Shinto shrines. Many tourists come here to see the famous Fushimi Inari shrine "
        "with thousands of red torii gates, or to walk through the Arashiyama bamboo forest. "
        "... "
        "Kyoto is also the heart of the tea ceremony. In this ceremony, everything has a meaning "
        "— every movement, every pause, every bow. Even today, students spend years learning it. "
        "In some old streets you can still see geishas walking to work in the early evening, "
        "but nobody is allowed to take photos of them without permission."
    ),
    "tokyo-reading.mp3": (
        "Tokyo is home to more than 37 million people in the greater metropolitan area — "
        "more than any other city in the world. During the morning rush hour, special staff "
        "called oshiya literally push commuters into trains to close the doors. Many employees "
        "work long hours, and some even sleep at their desk — there is a Japanese word for it, "
        "karoshi, which means death from overwork. "
        "... "
        "But Tokyo is not only about pressure. The city has quiet corners too: small gardens "
        "between skyscrapers, tiny tea houses, and the famous Shibuya crossing, where thousands "
        "of people cross the road at the same time in complete silence. Nobody shouts, nobody "
        "runs, and almost nobody talks on the phone. The silence is part of the order."
    ),
    "okinawa-reading.mp3": (
        "Okinawa is a group of islands in the south of Japan, far from Tokyo and even farther "
        "from Kyoto. The weather is warm all year, and the sea is turquoise. But Okinawa is "
        "famous for a very different reason — people live longer here than in almost any other "
        "place in the world. Many residents are more than 90 years old, and some reach 100. "
        "... "
        "Scientists say the reason is a mix of three things. First, a strict diet: a lot of "
        "vegetables, tofu, fish, and very little sugar. Second, a lot of movement — old people "
        "still work in their small gardens every day. Third, a very strong community: nobody "
        "is left alone. If somebody is sick, a neighbour always comes to help. Nothing happens "
        "in a hurry, and everything has its own time."
    ),
}
VOICE = "en-GB-RyanNeural"
HERE = os.path.dirname(os.path.abspath(__file__))

async def gen_one(fname, text, attempt=1):
    path = os.path.join(HERE, fname)
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        print(f"[skip] {fname} already exists")
        return
    try:
        comm = edge_tts.Communicate(text, VOICE, rate="-6%")
        await comm.save(path)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        if size < 2000:
            raise RuntimeError(f"tiny file ({size} B) — token rotation")
        print(f"[ok  ] {fname} ({size // 1024} KB)")
    except Exception as e:
        print(f"[err {attempt}] {fname}: {e}")
        if attempt < 4:
            await asyncio.sleep(5)
            if os.path.exists(path):
                os.remove(path)
            await gen_one(fname, text, attempt + 1)
        else:
            print(f"[FAIL] gave up on {fname}")

async def main():
    for fname, text in TEXTS.items():
        await gen_one(fname, text)
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    t0 = time.time()
    asyncio.run(main())
    print(f"done in {time.time() - t0:.1f}s")
