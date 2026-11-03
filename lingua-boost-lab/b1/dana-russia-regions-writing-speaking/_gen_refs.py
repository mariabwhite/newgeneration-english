#!/usr/bin/env python3
# Generate 6 reference-text narrations (one per Vocab Pack).
import asyncio, time
from pathlib import Path
import edge_tts

OUT = Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

REFS = {
    "pack1-traditions-reference.mp3": ("en-GB-SoniaNeural", (
        "Russian traditions form a surprisingly thick layer under modern life. Most of them existed long before Christianity arrived in the tenth century. "
        "Pancake Week, Maslenitsa, is a farewell to winter: for seven days people eat blini -- round golden pancakes that symbolise the sun -- and on the final Sunday they burn a straw doll of winter on a huge bonfire. "
        "Easter, Paskha, brings a different food cycle: tall sweet bread called kulich, soft curd pyramids called paskha, and painted eggs that children tap against each other to see whose shell survives. "
        "Summer belongs to Ivan Kupala, a solstice festival where young people jump over fires and float candle-wreaths down the river. "
        "In autumn the ritual calendar quiets down until the New Year -- the biggest holiday of all. The President speaks on television just before midnight, the Kremlin chimes ring out, and families eat Olivier salad and open mandarins. "
        "Across all these festivals, three verbs come back again and again: to celebrate, to observe a tradition, to pass down or to hand down from grandparent to grandchild. They are the backbone of this whole topic in your Writing and Speaking."
    )),
    "pack2-proverbs-reference.mp3": ("en-GB-ThomasNeural", (
        "In EGE Writing Task 38, Criterion K3, which assesses lexis, rewards precise idiomatic language. A well-placed Russian proverb with a correct English equivalent is almost a guaranteed point if it fits the argument. "
        "The trick is to use it as a bridge between two paragraphs, not as decoration. Try this template: As a Russian proverb says, quote, which perfectly captures the point that -- and then paraphrase the proverb in your own words. That is what examiners want to see. "
        "Russian proverbs usually fall into four groups. "
        "Work and effort: without work you won't even pull a fish out of a pond; the wolf is fed by its legs; repetition is the mother of learning. "
        "Caution and wisdom: the slower you ride, the further you'll get; measure seven times, cut once; morning is wiser than evening. "
        "Home and family: being a guest is good, but being home is better; the apple falls not far from the tree. "
        "Consequences: what you sow, that's what you'll reap; strike the iron while it's hot. "
        "Memorise one from each group -- four well-placed proverbs is enough to signal a strong lexical range."
    )),
    "pack3-languages-reference.mp3": ("en-GB-LibbyNeural", (
        "Russian is the only state language of the whole Federation, but inside the twenty-two republics another thirty-seven languages hold the status of co-official. "
        "Street signs, government documents and school certificates appear in two scripts side by side. In total, scholars count more than one hundred and fifty native languages, from Tatar -- spoken by five million people around Kazan -- to Evenki, a reindeer-herder language of the Siberian Far East with fewer than five thousand speakers left. "
        "These languages fall into four main families. Turkic covers Tatar, Bashkir, Chuvash and Yakut. Mongolic gives us Buryat near Lake Baikal and Kalmyk from Elista -- Europe's only Buddhist capital. "
        "Nakh-Dagestanian, concentrated in the North Caucasus, contains over forty languages in Dagestan alone. The Uralic family -- Komi, Udmurt, Mari -- forms a northern belt from the Baltic to the Urals. "
        "Some are thriving: Tatar has newspapers and television, and the Yakut film industry is one of Russia's most lively regional cinemas. Others are endangered -- UNESCO lists sixteen Russian minority languages as critically at risk, and republics now run immersion kindergartens to save them."
    )),
    "pack4-regions-reference.mp3": ("en-GB-RyanNeural", (
        "Russia is enormous. It covers more than seventeen million square kilometres, borders fourteen countries and spans eleven time zones -- when the sun sets over Kaliningrad on the Baltic, children in Kamchatka are already brushing their teeth for school the next morning. "
        "The country is officially divided into eighty-nine federal subjects: twenty-two republics, nine territories, forty-six provinces and others. "
        "Geographically, Russia is a story of belts. The tundra runs along the Arctic coast -- treeless, frozen most of the year, with reindeer herders and polar nights. South of it lies the taiga, the largest forest belt in the world. Further south again begins the steppe, the open grassland that once belonged to nomadic peoples. "
        "Mountain ranges frame the country: the Caucasus in the south with Mt Elbrus, five thousand six hundred and forty-two metres, the highest peak in Europe; the Urals dividing Europe and Asia; and the Altai in Siberia. "
        "The most unusual places are often remote: the volcanic peninsula of Kamchatka with its three hundred volcanoes, Lake Baikal -- the deepest and oldest freshwater lake on Earth, holding one fifth of the world's unfrozen fresh water -- the Kola Peninsula with its two hundred nights of aurora a year, and Kaliningrad, a tiny exclave on the Baltic that produces ninety per cent of the world's amber. "
        "For your essay, pick two or three of these and bring them to life."
    )),
    "pack5-towns-reference.mp3": ("en-GB-MaisieNeural", (
        "If you want to understand Russia beyond Moscow and St Petersburg, go to a small town. "
        "Within a two-hundred-kilometre radius north-east of the capital lies the Golden Ring -- a loop of eight ancient towns first described by the critic Yuri Bychkov in nineteen sixty-seven. The best known is Suzdal, which has fewer than ten thousand inhabitants but more than fifty churches, two monasteries and a wooden-architecture museum. Its July Cucumber Fair draws crowds from all over central Russia. "
        "Vladimir, the former capital of medieval Rus, keeps its stone Golden Gate from eleven sixty-four and the Assumption Cathedral where grand princes were crowned. Further north, Yaroslavl celebrated its millennium in two thousand and ten and is a UNESCO heritage site. "
        "Even tinier are the character towns. Myshkin, with just five and a half thousand people, built an entire tourist industry around a legend about a mouse that woke a sleeping prince. Plyos on the Volga was Isaac Levitan's favourite painting spot. Kolomna near Moscow is famous for its red-brick kremlin and pastila -- a traditional apple candy whose recipe was almost lost in the Soviet era. "
        "What all these towns share is the vocabulary you need for Writing and Speaking: quaint, cobbled, whitewashed, provincial, heritage site, artisan. For an essay, pick two towns and contrast them with Moscow or St Petersburg -- that is an easy organisation win."
    )),
    "pack6-crafts-reference.mp3": ("en-GB-ThomasNeural", (
        "Each traditional Russian craft is tied to one town, one colour palette and one material. "
        "Khokhloma, born in the forest villages near Nizhny Novgorod in the seventeenth century, is wooden tableware painted red, black and gold. The gold is a chemical trick with aluminium powder, linseed oil and a hot oven. "
        "Gzhel, from a village of the same name near Moscow, is porcelain painted in cobalt blue on a white glaze, fired twice. Its bouquets, birds and winter landscapes have been copied worldwide. "
        "Palekh lacquer miniatures -- tiny fairy-tale scenes painted in gold leaf on papier-mache boxes with a deep black background -- only appeared in the nineteen twenties, when former icon painters had to find a new subject after the revolution. "
        "Zhostovo trays, from a village in the Moscow Oblast, started in the nineteenth century: metal trays hand-painted with a central floral bouquet, each flower built from up to twenty brushstrokes. "
        "Vologda lace is woven with up to sixty wooden bobbins called koklyushki, producing geometric white-on-white snowflakes. "
        "Pavlovo Posad shawls are hand-printed woollen shawls with huge flower bouquets. "
        "And of course the matryoshka -- the nested wooden doll from Sergiev Posad -- was invented only in the eighteen nineties but has become Russia's single most recognisable souvenir. "
        "For your essay, remember the key vocab: craftsmanship, handmade, to carve, to glaze, pattern, brushstroke, lacquer, ceramics, embroidery, bobbin lace."
    )),
}

async def tts(voice, text, path, retries=3):
    for i in range(1, retries+1):
        try:
            c = edge_tts.Communicate(text, voice)
            await c.save(str(path))
            if path.stat().st_size > 500:
                return
        except Exception as e:
            print(f"  attempt {i} failed: {e}")
        time.sleep(5)
    raise RuntimeError(f"failed {path.name}")

async def main():
    for i, (fname, (voice, text)) in enumerate(REFS.items(), 1):
        p = OUT / fname
        print(f"[{i}/6] {fname} ({voice}) ...")
        await tts(voice, text, p)
        print(f"  -> {p.stat().st_size//1024} KB")

if __name__ == "__main__":
    asyncio.run(main())
