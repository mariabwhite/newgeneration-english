#!/usr/bin/env python3
"""Generate 4 IELTS Listening sections via edge-tts.
Voices target real IELTS variety: British + Australian + American.
"""
import asyncio, sys, subprocess
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = Path(__file__).parent

SECTIONS = [
    {
        "file": "section-1.mp3",
        "voice": "en-GB-SoniaNeural",
        "rate": "-8%",
        "text": """Ranger. Hinchingbrooke Country Park, good morning, this is Sam speaking, how can I help?
Teacher. Hello, my name is Rachel Green, I'm a teacher at Elmwood Primary School and I'd like to bring my class of twenty children for an educational visit. Could you tell me a bit about the park please?
Ranger. Of course. The park covers sixty-nine hectares of land just outside Huntingdon, so it's quite a large site.
Teacher. Sixty-nine hectares, that's a lot. What sort of habitats will the children see?
Ranger. There are three main ones. We have wetland, we have grassland, and we have woodland.
Teacher. Great variety, and what about the wetland exactly?
Ranger. The wetland includes lakes, ponds, and a stream that runs through the north of the park. It's a really rich area for wildlife — birds, insects and small mammals.
Teacher. Wonderful. Now, my colleagues and I have been looking at how we could use the visit for different subjects across the curriculum. Do you cover science?
Ranger. Yes, we do. For science, the children look at data about plants — how they grow, what they need, how they change with the seasons.
Teacher. Data, that's excellent. How about geography?
Ranger. Geography is one of our most popular subjects. It includes learning to use a map and compass. The children work in small teams and navigate to points around the park.
Teacher. That sounds fantastic. Do you offer history too?
Ranger. Yes, history looks at changes in land use over the last two hundred years. And there's leisure and tourism as well — that unit mostly concentrates on the park's visitors — who they are, why they come, and what they need.
Teacher. And I saw on your leaflet you also do music?
Ranger. That's right. In the music sessions the children make sounds with natural materials — bits of wood, stones, dried leaves — and then experiment with rhythm and speed. It's very hands-on.
Teacher. That's brilliant. Now, could you tell me a little about the benefits of outdoor educational visits — I have to justify this to the head teacher.
Ranger. Absolutely. First, the visits give children a sense of freedom that they may not have in an ordinary classroom. Second, children learn new skills — practical skills, teamwork, and confidence.
Teacher. Wonderful. And finally, the practical side — what does it cost?
Ranger. The cost is four pounds ninety-five per child. That's four point nine five, in pounds.
Teacher. Four ninety-five per child, understood. And what about the adults who come with us?
Ranger. All adults, such as group leaders, come free of charge. We usually recommend one adult per five children.
Teacher. Perfect. Thank you so much for your help.
Ranger. My pleasure. I'll send you a booking form by email today.""",
    },
    {
        "file": "section-2.mp3",
        "voice": "en-AU-NatashaNeural",
        "rate": "-4%",
        "text": """Good evening everyone, and welcome to our monthly meeting of the Stanthorpe Twinning Association. My name is Emma Carter, I'm the current secretary, and it's a real pleasure to see so many familiar faces here tonight, along with some new members.
Let me start with a quick introduction for those of you who are here for the first time. Stanthorpe is a small town in Queensland, Australia, best known for its granite belt vineyards and cooler climate. Our association has been running for over twenty years. We are twinned with a town in the south of France, and we also have an active exchange programme with a town in Japan. The link with France came first, in the early two thousands, and remains the most active. Some of you may have taken part in the summer wine and food weekend that we organised together last year.
Now, why did we set the association up in the first place. In the beginning, several members wanted to strengthen the town's international profile, but the real driver was the desire to create long-term friendships between families in different countries. That is still very much the focus today.
Since the pandemic, we've had to change how we work. In the past our exchanges were mostly in-person, week-long stays. During the pandemic we moved everything online, which some of you enjoyed, and others really didn't. Now we've settled into a hybrid model — one big in-person exchange per year, plus regular online cultural evenings.
As for membership, at present we have around one hundred and twenty active members. Numbers went down during the pandemic, but they've climbed back and are growing again. If any of you know someone who might be interested, please do bring them along to a meeting.
Now, on to our upcoming event. This one is being held at the Stanthorpe Community Hall. It runs from ten in the morning until four in the afternoon. The type of activity we're offering is a language and craft workshop — you'll pick up basic French or Japanese phrases, and try a traditional craft from the twinned town.
Our guest speaker on the day will be Professor Anna Fischer. Her specialism is intercultural communication, and she'll be giving a short talk after lunch on how small towns can build big international links.
Food will be provided as part of the ticket. We're offering a shared buffet, prepared by our members — French cheeses, Japanese onigiri, and locally baked bread from Stanthorpe.
Finally, to sign up, please use the online booking form on our website. Payment can be made online at the same time. We do have a paper form available as a backup, but online is the fastest way.""",
    },
    {
        "file": "section-3.mp3",
        "voice": "en-GB-RyanNeural",
        "rate": "-3%",
        "text": """Tutor. Hi Alex, hi Sara — thanks for coming in. So, you're planning your joint research project on urban parks and community well-being. Where are you up to?
Alex. Well, we've done the initial reading, and we've narrowed the topic to how small city parks affect the mental health of people who live within a five-minute walk.
Sara. Right, and we've agreed on a plan, but we wanted to check it with you before we start collecting data.
Tutor. Good. What have you agreed you need to do first?
Alex. We agreed we need two things. First, we need a solid framework for measuring well-being — because there are lots of scales out there. Second, we need permission from the local council to run our survey in the parks.
Sara. Yes, those two — a well-being measurement framework, and council permission. Without either, we can't really begin.
Tutor. Sensible. And what challenges do you anticipate?
Sara. Two things worry us. One is recruiting a diverse enough sample — a lot of park users are the same demographic, mostly young professionals. And the other is seasonal variation. If we survey in summer versus winter, we'll get very different behaviour.
Alex. Sample diversity and seasonal effects, yes. Those two are the big ones.
Tutor. Excellent. Now let's talk about the six data-collection stages you've mapped out. Stage one?
Alex. Stage one is direct observation — we'll sit in each park and record how many people arrive and what they do, without approaching them.
Tutor. Good. And stage two?
Sara. Stage two is a satisfaction survey — we'll hand out short paper questionnaires to park users.
Tutor. And stage three?
Alex. Stage three, we'll conduct short structured interviews with a smaller sub-sample of the people who filled in the survey.
Tutor. Interviews. Right. Stage four?
Sara. Stage four is a focus group with council staff — the people who manage the parks — so we understand the operational context.
Tutor. Very good. Stage five?
Alex. Stage five is a mobile-phone diary study, where volunteers log their mood after each visit to the park for two weeks.
Tutor. Mobile diaries — you'll need to check ethics on that one. And stage six?
Sara. Stage six is analysing existing health data from the local clinic — anonymised, of course — to see whether people living close to a park visit their GP less often.
Tutor. Excellent. That's a solid pipeline. Now let's talk timing…""",
    },
    {
        "file": "section-4.mp3",
        "voice": "en-GB-LibbyNeural",
        "rate": "-6%",
        "text": """Good afternoon everyone, and welcome to today's lecture on Céide Fields, one of the most remarkable archaeological sites in Europe. Céide Fields is located on the north coast of County Mayo in Ireland, and it dates from around three and a half thousand BC — which makes it, at roughly five and a half thousand years old, the oldest known enclosed field system anywhere in the world.
Let me start with the site itself. Céide Fields is defined, quite literally, by ancient stone walls. These walls stretch for several kilometres, and they mark out fields, paddocks and enclosures, all beneath a blanket of peat.
Now, how was this extraordinary landscape discovered? The story is a lovely one. In the nineteen thirties, a local schoolteacher named Patrick Caulfield was cutting turf on his land. He noticed piles of stones deep under the peat, arranged in straight lines. He didn't investigate further in his own lifetime, but his son — who became a professional archaeologist — went back to the site and began excavations. So the discovery is really thanks to the farmer's son.
What was the peat itself used for? In this part of Ireland peat, or turf, has been cut and dried for centuries and used as fuel — for heating homes and for cooking. It burns slowly and gives good heat. This use of turf as fuel is what led to the discovery of the walls beneath.
And why has the site been preserved so beautifully? Two reasons. First, the peat is waterlogged. Second, and more importantly, the peat contains a lack of oxygen. Without oxygen, organic materials — wooden tools, pollen, even the imprints of feet — can survive for thousands of years.
Now, let's move on to the society that built these fields. The shape of the enclosures is a very clear feature — most of them are rectangular, not round. Each rectangle would have held a small number of animals or a crop.
Inside their dwellings, the Neolithic farmers used lamps. These were simple stone or shell containers with animal fat as fuel and a wick of moss or plant fibre.
The social unit was small. Analysis of the buildings and enclosures shows that people lived and worked in groups organised around a single family — one family per farmstead.
Time of year mattered a great deal. In summer there was constant outdoor work. But in winter, most activity moved indoors — repairing tools, weaving, telling stories, tending to animals kept close to the home. So winter is when we assume the family spent most of their time inside.
Finally, why did this remarkable society come to an end? Two factors. The first was the soil. Continuous farming, generation after generation, exhausted the soil — its fertility declined, and crops failed. The second factor was climate change. Over several centuries the climate got wetter, with more rain — and heavy rain washed away the topsoil and encouraged the growth of the peat that eventually buried the site. When the soil could no longer support agriculture, the community moved on, and the walls disappeared under the peat that we see today.""",
    },
]


async def gen():
    import edge_tts
    for s in SECTIONS:
        out = HERE / s["file"]
        print(f"[gen] {s['file']} · voice={s['voice']} · rate={s['rate']} · text_len={len(s['text'])}")
        comm = edge_tts.Communicate(
            text=s["text"],
            voice=s["voice"],
            rate=s["rate"],
        )
        await comm.save(str(out))
        print(f"[ok]  {s['file']} · size={out.stat().st_size} bytes")


if __name__ == "__main__":
    asyncio.run(gen())
