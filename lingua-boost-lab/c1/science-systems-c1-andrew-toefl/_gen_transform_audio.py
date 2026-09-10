"""Generate 6 TTS clips for the transformed TOEFL lesson via ttsmp3.com."""
import sys, pathlib, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

CLIPS = [
    ("text-1-genetic-engineering",
     "In recent years, scientists have made significant progress in modifying plant DNA in order to increase resistance to pests and extreme weather conditions. These innovations allow crops to survive in environments where traditional agriculture would fail. As a result, food production has become more stable in certain regions. "
     "However, this approach raises serious concerns. Critics argue that altering genetic structures may lead to unpredictable long-term consequences. For example, modified genes could spread to wild plant species, which in turn might disrupt natural ecosystems and reduce biodiversity. "
     "Some researchers believe that these risks can be managed through strict regulation, while others insist that the potential damage remains too uncertain."),
    ("model-1-nuclear",
     "Opinions remain divided because nuclear energy combines major advantages with potentially catastrophic risks. Supporters emphasise low carbon emissions and continuous, weather-independent output, while opponents focus on accidents, radioactive waste, and high construction costs. Historical disasters such as Chernobyl and Fukushima continue to shape public opinion both emotionally and politically. As a result, debates about nuclear power almost always blend scientific evidence with social fear — and this combination makes consensus extremely difficult."),
    ("model-2-materials",
     "Biodegradable polymers reduce environmental impact because they decompose under specific natural conditions, unlike traditional plastics that remain in ecosystems for decades. Modern packaging derived from plant-based polymers already breaks down more efficiently in landfills and oceans. This innovation could significantly improve sustainability across manufacturing and waste management. However, durability and production costs remain serious challenges, so researchers continue searching for the right balance between ecology and economic practicality."),
    ("model-3-neuroscience",
     "People rely on emotion because emotional responses are much faster than analytical reasoning. In stressful or uncertain situations, the brain prioritises quick reactions over careful analysis — a survival mechanism that still operates in modern life. For instance, during financial crises many investors panic and sell impulsively, even when the data suggests that staying calm would be rational. Emotions are not weakness; they are an evolutionary shortcut, but the same shortcut can mislead us in environments evolution never anticipated."),
    ("model-4-zoology",
     "Endangered species are difficult to protect because their survival depends on several interconnected factors: habitat protection, conservation policy, human behaviour and global environmental conditions. Even if one area is rigorously protected, illegal hunting or climate change can still threaten the same species elsewhere. For example, the Amur leopard remains critically endangered partly because protected reserves cannot fully prevent poaching beyond their borders. From a broader perspective, real protection requires coordinated international effort rather than isolated local action."),
    ("revision-keys",
     "One. This field focuses on the intersection of biology and technology. "
     "Two. It plays a crucial role in shaping modern policy debates. "
     "Three. One major concern is that the long-term consequences remain uncertain. "
     "Four. This may lead to unpredictable disruptions across natural ecosystems. "
     "Five. From a long-term perspective, coordinated international effort is essential. "
     "Six. The main benefit is that decisions become more evidence-based. "
     "Seven. It is crucial to strike a balance between innovation and responsibility."),
]

VOICE = "Amy"

def gen(page, slug, text):
    dest = OUT / f"{slug}.mp3"
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"skip  {slug}.mp3 ({dest.stat().st_size} B)"); return
    page.goto("https://ttsmp3.com/", wait_until="load", timeout=60000)
    page.wait_for_timeout(1500)
    for sel in ["button:has-text('AGREE')", "button:has-text('Consent')", "button:has-text('Accept')", ".fc-cta-consent"]:
        try:
            b = page.locator(sel).first
            if b.is_visible(timeout=1200): b.click(); break
        except Exception: pass
    page.wait_for_selector("select#sprachwahl", timeout=30000)
    page.select_option("select#sprachwahl", value=VOICE)
    ta = page.locator("textarea#voicetext"); ta.wait_for(timeout=15000); ta.click(); ta.fill(text)
    with page.expect_download(timeout=90000) as di:
        page.click("input#downloadenbutton")
    di.value.save_as(str(dest))
    print(f"OK    {slug}.mp3 ({dest.stat().st_size} B)")

with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    ctx = br.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36")
    page = ctx.new_page()
    for slug, text in CLIPS:
        try: gen(page, slug, text); time.sleep(1.5)
        except Exception as e: print(f"FAIL  {slug}: {e}")
    br.close()
print(f"\nDone. Files in {OUT}")
