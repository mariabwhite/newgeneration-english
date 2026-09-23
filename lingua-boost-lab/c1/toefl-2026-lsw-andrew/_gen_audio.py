"""Generate 8 mp3s for TOEFL 2026 LSW Andrew lesson via edge-tts."""
import sys, asyncio, pathlib
sys.stdout.reconfigure(encoding='utf-8')
import edge_tts

OUT = pathlib.Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

MALE   = "en-US-GuyNeural"     # Matthew role — academic male
FEMALE = "en-US-JennyNeural"   # Joanna role — academic female
MALE2  = "en-US-AndrewNeural"  # variation for model 4
FEMALE2= "en-US-AriaNeural"    # variation for model 3

CLIPS = [
    ("text-03-title", MALE,
     "Global battery-storage deployment reached roughly one hundred and eight gigawatts in twenty twenty-five — a forty percent year-on-year rise driven overwhelmingly by lithium-iron-phosphate chemistry, which now accounts for around ninety percent of new installations. China alone was responsible for close to sixty percent of these additions, and utility-scale projects made up roughly four-fifths of the total. Prices continued to fall in parallel. BloombergNEF placed the average pack price at seventy dollars per kilowatt-hour — a forty-five percent drop in a single year. Total global spending on grid storage in twenty twenty-five approached sixty-six billion dollars. Analysts caution, however, that supply-chain concentration and grid-integration constraints could slow the pace as installations scale further."),

    ("talk-08-battery", MALE,
     "The story of grid-scale battery storage in twenty twenty-five is one of the clearest examples we have of exponential deployment in the energy sector. According to the IEA Global Energy Review twenty twenty-six, roughly one hundred and eight gigawatts of new storage came online last year — a forty percent jump on the year before. Chemistry has consolidated with equal speed: lithium-iron-phosphate — LFP — now accounts for close to ninety percent of new installations, largely because of its cycle life and its lower dependence on cobalt and nickel. Prices have collapsed in parallel. BloombergNEF places the average pack price at seventy dollars per kilowatt-hour, a forty-five percent year-on-year drop. Geographically, China alone was responsible for roughly sixty percent of the additions, and utility-scale projects made up around four-fifths of the total. Total global spending on power storage reached sixty-six billion dollars in twenty twenty-five. The obvious question is whether this pace can be sustained; analysts warn that supply-chain concentration and grid-integration constraints may slow further growth."),

    ("talk-09-perovskite", FEMALE,
     "For more than a decade, perovskite photovoltaics hovered on the edge of commercial viability — extraordinary efficiency gains in the laboratory, undermined every time by rapid degradation once the cell was exposed to real-world humidity, heat and sunlight. According to a twenty twenty-five Nature Reviews Clean Tech overview, that Achilles heel has finally begun to close. In December twenty twenty-four, Qcells reported a certified power-conversion efficiency of twenty-eight point six percent on a full-area M-ten silicon–perovskite tandem — the current world record. Single-junction perovskites have crossed twenty-seven percent, and silicon–perovskite tandems in the laboratory now exceed thirty-four percent. Oxford PV is already shipping seventy-two-cell tandem modules to US customers at a rated twenty-four point five percent. On the stability side, a new generation of lead-tin perovskite devices has demonstrated roughly sixty-six percent longer operational lifespan than earlier lead-based cells. Taken together, these advances suggest that perovskite tandems have crossed the commercial threshold; the remaining challenge is manufacturing scale-up rather than fundamental physics."),

    ("model-14-1-battery", MALE,
     "LFP has come to dominate grid-scale storage — close to ninety percent of new installations in twenty twenty-five — for a combination of practical and geopolitical reasons. Practically, LFP delivers several thousand full charge cycles at good capacity retention and does not depend on cobalt or nickel, which makes it safer, cheaper and less exposed to volatile mineral markets. Geopolitically, it has been possible to scale the supply chain almost entirely within China, which drove pack prices to around seventy dollars per kilowatt-hour last year — a forty-five percent year-on-year fall. For a grid operator making a twenty-year procurement decision, those three factors — cost, safety and supply-chain predictability — are essentially decisive."),

    ("model-14-2-perovskite", FEMALE,
     "The Qcells twenty-eight point six percent record from December twenty twenty-four matters because of what was measured, not just what it measured. It was a full-area M-ten silicon-perovskite tandem, certified by an independent test institute — in other words, a device on a real production wafer, not a laboratory sliver. That closes the historical gap between spectacular record cells and shippable modules. Combined with Oxford PV already shipping twenty-four point five percent tandem modules to US customers and new lead-tin devices demonstrating roughly sixty-six percent longer operational lifespan, the picture that emerges is of a technology that has crossed the commercial threshold. The bottleneck now sits at manufacturing scale-up, not at fundamental physics."),

    ("model-14-3-dac", FEMALE2,
     "The DAC cost curve is stubborn largely because of physics. Climeworks currently operates at roughly one thousand to thirteen hundred dollars per tonne, and the industry's aspirational targets of two to three hundred dollars per tonne by twenty thirty and one to two hundred by twenty thirty-five are enormously ambitious. The dominant reason is energy: capturing a single tonne of carbon dioxide from ambient air requires roughly two thousand kilowatt-hours, which either eats into renewable capacity that could be doing other useful work, or defaults to fossil-fuelled electricity, undermining the point. ETH Zurich's realistic modelling puts long-run costs at two hundred and thirty to five hundred and forty dollars per tonne — still an order of magnitude above the aspirational floor."),

    ("model-14-4-policy", MALE2,
     "The gap between leaders and laggards on the renewable transition is largely a gap in policy stability, not in resources or technology. China leads on deployment because it treats grid-scale storage manufacturing as strategic industrial policy — long-horizon subsidies, predictable procurement, vertical integration from mines to cells. Northern-European countries lead on grid integration because they price carbon consistently and give operators multi-decade certainty on rules. Laggard economies typically have the raw resource — plenty of sun, plenty of wind — but their policy signals flip every election cycle, which raises the cost of capital for every renewable project. From a long-term perspective, coordinated international policy is essential for a viable climate transition."),

    ("revision-14b-keys", MALE,
     "One. The technology has crossed a decisive commercial threshold. "
     "Two. Occidental monetizes the captured carbon through enhanced oil recovery. "
     "Three. Perovskite tandems have hovered on the edge of viability for years. "
     "Four. Deployment continues to ramp exponentially, quarter on quarter. "
     "Five. Rapid degradation was long the Achilles heel of the field. "
     "Six. Current DAC costs remain an order of magnitude above the aspirational target. "
     "Seven. From a long-term perspective, coordinated international policy is essential."),
]

async def gen(slug, voice, text):
    dest = OUT / f"{slug}.mp3"
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"skip  {slug}.mp3"); return
    c = edge_tts.Communicate(text, voice, rate="-3%")
    await c.save(str(dest))
    print(f"OK    {slug}.mp3 ({dest.stat().st_size} B, voice={voice})")

async def main():
    for slug, voice, text in CLIPS:
        try: await gen(slug, voice, text)
        except Exception as e: print(f"FAIL  {slug}: {e}")

asyncio.run(main())
print("\nDone.")
