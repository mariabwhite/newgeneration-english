"""Generate 8 edge-tts audio clips for Anya's Night Train quest · v2 extended.
Voice: en-US-AriaNeural. Stories ~250-350 words each = ~90-130 sec.
"""
import asyncio, os
import edge_tts

VOICE = "en-US-AriaNeural"
OUT_DIR = os.path.join(os.path.dirname(__file__), "assets", "audio")
os.makedirs(OUT_DIR, exist_ok=True)

STORIES = {
    "01-harbour.mp3": (
        "The Night Train stops at the harbour at six twelve in the morning. "
        "The sky is turning pink and gold, and a thin fog is rising from the water. "
        "I am opening my journal on my lap when I see him through the window — the old brass seller. "
        "He is waiting on the pier, exactly where I met him last August. He is wearing the same brown coat and the same wool cap. "
        "I step off the train and walk slowly along the wet stones. "
        "Last August, I say quietly, you were very patient with me. The ferry was late, the sky was grey, the waves were loud and cold. "
        "I waited two whole hours on this pier. I talked to you for a long time. "
        "You showed me a small compass from your old leather box. I asked about the direction to the island across the water. "
        "You smiled kindly, you pointed to the horizon and you answered me very slowly, word by word. "
        "I listened carefully and I learned the names of three winds: the north wind, the east wind, and the one you called the whispering wind. "
        "He is smiling now, under his white moustache. He is giving me the same brass compass, and it is heavy in my hand. "
        "Take it, he is saying softly. The train will need a compass. The sea is wide and the stations are many. "
        "I put the brass compass into my coat pocket. It is warm, like a small living thing. "
        "The train whistles once, twice. I nod to the old seller and I climb back to my carriage. "
        "My first artifact is in my pocket. The journey has really begun."
    ),
    "02-market.mp3": (
        "The Night Train stops again at seven forty, right at the edge of the Saturday market. "
        "My grandmother is standing on the small wooden platform with our old wicker basket. "
        "She is waving at me through the mist. I ran to her and hugged her very tight. "
        "Do you remember last Saturday? I said with a smile. She just laughed. "
        "Last Saturday we went to the market together, early in the morning. "
        "We took the big wicker basket and we walked for twenty minutes down the narrow street. "
        "The market was busy and full of warm bread smells. A kind woman sold big red apples at the first stall. "
        "I chose ten of them and I paid with a small blue note. She gave me change in bright silver coins. "
        "Then I saw a warm green scarf on another stall and I tried it on. "
        "You said it was perfect for autumn, so I bought it without thinking. "
        "After that, we drank hot black tea and we ate warm bread with yellow cheese. "
        "A small boy ran past us very fast and he nearly caught my hand. "
        "My basket fell on the ground, but luckily nothing broke inside. "
        "I came home tired and happy that evening. I wrote about the whole day in my journal before I fell asleep. "
        "Grandma is laughing now. She is handing me the basket with ten fresh red apples and a loaf of bread. "
        "For the train, she is saying. For the long journey ahead."
    ),
    "03-lighthouse.mp3": (
        "The train pulls up at the stony base of the cliff. The lighthouse stands above me, grey and tall and very silent. "
        "The same ghost cat is sitting on the top step, washing its paw in the moonlight. "
        "Hello, old friend, I am saying as I climb out of the carriage. Do you remember last Halloween? "
        "At midnight the waves were crashing loudly against the cliff. The green seaweed was shining in the moonlight on the wet rocks. "
        "I was climbing the old wooden stairs of the lighthouse when I heard a soft bell somewhere above me. "
        "While I was walking up, step by step, a small ghost was whispering near the dusty window. "
        "You, dear cat, were sitting on the very top step, and your little paw was shaking a little. "
        "When I finally reached the top, the bell rang once again, clear and bright. "
        "The old ghost told me a secret, something about my grandmother and a silver book, and then it disappeared into the fog. "
        "I never told anyone the secret, but I wrote one word about it in my journal. "
        "The cat is meowing softly now. It is pushing a small bronze bell toward me with its paw. "
        "For the compass, it seems to say with its sea-green eyes. For your journey on the Night Train. "
        "I take the bell and tie it to the loop on my compass. It makes a tiny silver sound in the wind. "
        "Two artifacts now. The train is waiting."
    ),
    "04-temples.mp3": (
        "The train slides quietly into the temple valley. The morning sun is warm on the stone columns. "
        "Our guide is waiting on the platform with an old leather map rolled under her arm. "
        "Welcome back, Anya, she is saying with a slow smile. I have been waiting for you since dawn. "
        "I have been to five sacred temples with her since July. I have never seen a map as old as the one in the first temple — it was made of real deer skin. "
        "Our guide has walked these dusty roads for ten long years. She knows every curve and every small flower. "
        "She has already shown us three secret paths through the mountains, and we haven't finished the whole expedition yet. "
        "I have taken many photos since September — maybe three hundred, maybe more. "
        "My grandmother has kept every single postcard I have sent her this year. She keeps them in a wooden box next to her bed. "
        "We have known our guide for three months now and she really feels like family. "
        "She has taught us the names of twelve plants and the story of the river. "
        "She is giving me the old map now. It has travelled with me for ten years, she is saying, and it has seen many brave feet. "
        "Now it will travel with you. You will find your own paths. "
        "I take the map carefully with both hands. It is soft and warm, and it smells like old mountains. "
        "I put it inside my journal. The train whistles. I run back."
    ),
    "05-postcards.mp3": (
        "The postman is standing at the old wooden depot with a small stack of yellow letters in his gloved hands. "
        "He is handing me a bright postcard with a bustling square on it. From August, he is saying with a friendly nod. "
        "I used to send postcards every single week when I was younger. Now I mostly send voice memos to my friends. "
        "My suitcase used to be empty and quiet — just one pair of socks and a toothbrush. "
        "Now it is always full of bustling souvenirs: shells, dried flowers, folded tickets, small stones. "
        "I used to think that a postcard was just a boring paper rectangle. "
        "Now I know it is a small window into one quiet day in one bright city. "
        "My grandmother didn't use to keep photographs on her walls, because she said they faded too fast. "
        "Instead, she used to keep every postcard in a wooden drawer by the window. "
        "She used to say that a postcard carries a smell of a city, even after many years. "
        "If you open an old postcard and you breathe deeply, you can still smell the sea or the market or the rain. "
        "Take this one, the postman is saying kindly. He puts the postcard in my hand. "
        "You wrote it last August, from the harbour, when you were waiting for the ferry. "
        "I read my own handwriting and I smile. It feels like meeting an older sister I had forgotten about."
    ),
    "06-city.mp3": (
        "The train is pulling slowly into Central Station. The light outside is bright and cold. "
        "Masha is standing on the platform with two tall paper cups of coffee. She is waving one of them above her head. "
        "Your town is waking up, she is laughing. Come, look. "
        "My town has a small square in the middle, with a round stone fountain in it. "
        "I walk through the pedestrian zone every single morning on my way to school. "
        "The bakery on the corner opens at seven, and it always smells of warm cinnamon. "
        "The pharmacy stays open until midnight for emergencies. "
        "Right now the small children are playing loudly at the playground near the bench. "
        "A grey-haired man is reading a newspaper on a park bench under the big oak tree. "
        "Two women are crossing the stone bridge towards the metro station, both carrying heavy bags. "
        "The traffic light on the corner is turning red. A boy is sitting quietly near the statue of the old mayor. "
        "The library doors are opening for the morning, and three students are already waiting. "
        "Masha and I walk to the fountain and we sit on the warm stone edge. "
        "I am leaning carefully over the water. A shiny copper coin is lying at the bottom among the leaves. "
        "I am picking it up slowly with my fingers. For later, I am whispering to Masha. "
        "She smiles. She knows about my collection."
    ),
    "07-hogsmeade.mp3": (
        "The train is slowing down at Hogsmeade Halt. The sky is dark purple, the colour of old plums. "
        "A huge orange Jack-o'-lantern is burning brightly on the wooden platform. "
        "Children in bright costumes are running between the carriages, laughing and shouting. "
        "Remember last Halloween? I am asking my pumpkin-shaped friend who is riding with me on the train. "
        "On Halloween night, Jack walked alone through Sleepy Hollow. "
        "A witch was flying on her black broom above the haunted church tower. "
        "A small black cat sat on an orange pumpkin and watched him with bright green eyes. "
        "While Jack was walking down the main street, children shouted trick or treat from every doorway. "
        "He gave them bright paper-wrapped candy and he put on his new skeleton costume. "
        "Then the old witch whispered a long spell above the trees, and the whole hollow lit up with blue fire. "
        "Jack was not afraid. He waved at the witch and the witch waved back, friendly. "
        "I take a little Jack-o'-lantern from the station seller. It fits in my hand. "
        "It glows softly, warm and orange, like a small sleeping heart. I put it in my bag, next to the compass and the bell."
    ),
    "08-observatory.mp3": (
        "The Night Train is returning home to the Dawn Observatory, just as the sun begins to set. "
        "The whole sky is orange and pink and lavender, like a huge painted scarf. "
        "Five brass telescopes are standing in a row on the stone roof, each one pointing at a different part of the evening sky. "
        "I climb up to the roof slowly, with all my eight artifacts in my bag. "
        "I want to practise my five futures, one at each telescope. "
        "At the first telescope, I say: Tomorrow I will probably visit my aunt. I haven't decided yet. That is Future Simple with will. "
        "At the second telescope, I say: On Saturday I am going to buy brass for my dad. I already have the money ready in my coat pocket. That is going to. "
        "At the third telescope, I say: I am meeting Masha at four on Monday. She already confirmed by text. That is Present Continuous for an arrangement. "
        "At the fourth telescope, I say: The ferry leaves at seven fifteen tomorrow and the train arrives in the city at eleven forty. That is Present Simple for a timetable. "
        "At the fifth telescope, I say: By twenty thirty I will have finished school. By the age of twenty five I will have travelled to three continents. That is Future Perfect. "
        "And there is one more rule, I say to the open sky. "
        "When I finish school, I will travel. As soon as the ferry arrives, I will board. By the time I come back, the sky will have turned pink again. "
        "No will after when, after as soon as, or after by the time. Only Present Simple. Only present. "
        "The quest is complete. Eight stations, eight artifacts, all my tenses."
    ),
}

async def gen_one(filename: str, text: str, rate="-6%"):
    out_path = os.path.join(OUT_DIR, filename)
    print(f"  --> {filename}  ({len(text)} chars)")
    comm = edge_tts.Communicate(text=text, voice=VOICE, rate=rate)
    await comm.save(out_path)
    size = os.path.getsize(out_path)
    print(f"      saved {size:,} bytes")
    return out_path, size

async def main():
    print(f"Generating {len(STORIES)} clips --> {OUT_DIR}")
    results = []
    for fname, text in STORIES.items():
        try:
            path, size = await gen_one(fname, text)
            results.append((fname, size, None))
        except Exception as e:
            print(f"  !! {fname} FAILED: {e}")
            results.append((fname, 0, str(e)))
    print("\nSummary:")
    for fname, size, err in results:
        status = "OK" if size > 1000 else ("EMPTY" if size == 0 else "SMALL")
        print(f"  {fname:28}  {size:>8,} bytes  {status}  {err or ''}")

if __name__ == "__main__":
    asyncio.run(main())
