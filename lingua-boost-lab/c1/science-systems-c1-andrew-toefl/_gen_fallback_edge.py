"""Fallback: generate 5 remaining TOEFL clips via edge-tts if ttsmp3 stalled."""
import sys, asyncio, pathlib
sys.stdout.reconfigure(encoding='utf-8')
import edge_tts

OUT = pathlib.Path(__file__).parent / "assets" / "audio"
V = "en-GB-SoniaNeural"  # calm BrE female, matches ttsmp3 Amy in tone

CLIPS = {
    "model-1-nuclear":
        "Opinions remain divided because nuclear energy combines major advantages with potentially catastrophic risks. Supporters emphasise low carbon emissions and continuous, weather-independent output, while opponents focus on accidents, radioactive waste, and high construction costs. Historical disasters such as Chernobyl and Fukushima continue to shape public opinion both emotionally and politically. As a result, debates about nuclear power almost always blend scientific evidence with social fear — and this combination makes consensus extremely difficult.",
    "model-2-materials":
        "Biodegradable polymers reduce environmental impact because they decompose under specific natural conditions, unlike traditional plastics that remain in ecosystems for decades. Modern packaging derived from plant-based polymers already breaks down more efficiently in landfills and oceans. This innovation could significantly improve sustainability across manufacturing and waste management. However, durability and production costs remain serious challenges, so researchers continue searching for the right balance between ecology and economic practicality.",
    "model-3-neuroscience":
        "People rely on emotion because emotional responses are much faster than analytical reasoning. In stressful or uncertain situations, the brain prioritises quick reactions over careful analysis — a survival mechanism that still operates in modern life. For instance, during financial crises many investors panic and sell impulsively, even when the data suggests that staying calm would be rational. Emotions are not weakness; they are an evolutionary shortcut, but the same shortcut can mislead us in environments evolution never anticipated.",
    "model-4-zoology":
        "Endangered species are difficult to protect because their survival depends on several interconnected factors: habitat protection, conservation policy, human behaviour and global environmental conditions. Even if one area is rigorously protected, illegal hunting or climate change can still threaten the same species elsewhere. For example, the Amur leopard remains critically endangered partly because protected reserves cannot fully prevent poaching beyond their borders. From a broader perspective, real protection requires coordinated international effort rather than isolated local action.",
    "revision-keys":
        "One. This field focuses on the intersection of biology and technology. "
        "Two. It plays a crucial role in shaping modern policy debates. "
        "Three. One major concern is that the long-term consequences remain uncertain. "
        "Four. This may lead to unpredictable disruptions across natural ecosystems. "
        "Five. From a long-term perspective, coordinated international effort is essential. "
        "Six. The main benefit is that decisions become more evidence-based. "
        "Seven. It is crucial to strike a balance between innovation and responsibility.",
}

async def gen(slug, text):
    dest = OUT / f"{slug}.mp3"
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"skip  {slug}.mp3"); return
    c = edge_tts.Communicate(text, V, rate="-3%")
    await c.save(str(dest))
    print(f"OK    {slug}.mp3 ({dest.stat().st_size} B)")

async def main():
    for slug, text in CLIPS.items():
        try: await gen(slug, text)
        except Exception as e: print(f"FAIL  {slug}: {e}")

asyncio.run(main())
print("\nDone.")
