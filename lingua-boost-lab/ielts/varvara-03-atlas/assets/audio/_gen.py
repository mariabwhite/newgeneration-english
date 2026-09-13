"""Generate 6 IELTS listening MP3s for varvara-03-atlas via edge-tts.
Run: py -3 _gen.py
"""
import asyncio, sys
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent

TRACKS = [
    ("l-01-concert.mp3", "en-GB-SoniaNeural",
     "Right, and about the venue for the autumn concert. "
     "Originally we planned to hold it at the Town Hall, and a lot of you still expect it there. "
     "But following last month's roof survey we have moved it. "
     "It will now be in Saint Michael's Church on King Street, "
     "not the Library Hall that some of you may have seen listed on our website last week - "
     "that page was outdated and has now been corrected. "
     "Ticket prices are unchanged: eight pounds standard, five pounds concessions."),

    ("l-02-modules.mp3", "en-GB-RyanNeural",
     "Right, so let's go through your four core modules for term one. "
     "Media Ethics is delivered in two full-day intensives, so mark that as intensive block. "
     "Digital Cultures stays with the traditional weekly ninety-minute seminar - weekly seminar. "
     "Research Methods, unusually, is entirely self-paced online: "
     "you access it whenever suits you, before the end-of-term deadline. "
     "And finally the Dissertation Prep module uses one-to-one supervisor tutorials, "
     "booked directly with your assigned supervisor."),

    ("l-03-gardens.mp3", "en-GB-LibbyNeural",
     "Good morning everyone, welcome to Elmswood Botanic Gardens. "
     "If you look at the plan you'll see we're standing at the main entrance in the south. "
     "Directly ahead of you, on the central axis, is the palm house, our largest glasshouse. "
     "In the top-left corner is the herbarium, where our dried plant collections are kept - "
     "that room is not open to casual visitors. "
     "In the top-right corner is the seed bank, a partnership with Kew opened in twenty twenty-three. "
     "On your left as you go in, just past the palm house, is the tea room and shop, "
     "and on your right, opposite it, is the education pavilion, "
     "where children's workshops run at weekends."),

    ("l-04-course.mp3", "en-GB-SoniaNeural",
     "Great, let me take some details. Can I have your family name? "
     "Yes - Sulesh. S. U. L. E. S. H. "
     "Right, Sulesh. Which course did you want to book? "
     "The IELTS evening course, please, not the Saturday one. "
     "OK. Tuesdays and Thursdays, six thirty to eight thirty. "
     "Starts on the eighteenth of October. "
     "The cost is two hundred and ninety-five pounds for the eight-week block - "
     "I had two hundred and seventy-five pounds written down originally but the price was updated last week. "
     "There's a discount if you pay by direct debit, bringing it to two hundred and seventy pounds. "
     "Direct debit, please. And my nearest tube - King's Cross, not Camden Town."),

    ("l-05-ceide.mp3", "en-GB-LibbyNeural",
     "One of the most striking features of the Kaida Fields site "
     "is the way the ancient stone walls lie preserved directly beneath the modern layer of peat. "
     "The site is remarkable partly because it was discovered by pure accident - "
     "a farmer's son noticed unusual stone patterns in the nineteen thirties while cutting turf. "
     "The reason the walls survive at all comes down to preservation conditions: "
     "the acidic, oxygen-poor peat that grew over them acted as a natural preservative. "
     "Analysis of pollen from the site suggests farming continued for roughly six centuries "
     "before the community was pushed out by falling fertility in the soil and worsening rainfall."),

    ("l-06-tour.mp3", "en-GB-MaisieNeural",
     "Hi, I wanted to ask about the Sunday walking tour. "
     "Sure. It leaves from Trafalgar Square at ten a.m. - meet by the north lion. "
     "It takes about two hours and finishes at Covent Garden. "
     "Group size is capped at fifteen - smaller than most walking tours in the city. "
     "And what's included? "
     "The guide, obviously, plus a small printed map. "
     "Coffee is not included - you can buy that at the end. "
     "And the tour goes ahead in any weather, so bring a raincoat."),
]


async def one(name, voice, text):
    out = HERE / name
    print(f"  {name}  [{voice}]  {len(text)} chars")
    await edge_tts.Communicate(text, voice, rate="-5%").save(str(out))
    print(f"    -> {out.stat().st_size // 1024} KB")


async def main():
    for name, voice, text in TRACKS:
        await one(name, voice, text)


if __name__ == "__main__":
    asyncio.run(main())
    print("done.")
