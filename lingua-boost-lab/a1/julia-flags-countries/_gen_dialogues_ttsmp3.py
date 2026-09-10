"""Generate 3 airport-dialogue MP3s via ttsmp3.com (Amy BrE)."""
import sys, pathlib, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

DIALOGUES = [
    ("dialog-01-london",
     "At London airport. Officer: Good morning. Where are you from? Julia: I am from Russia. I am Russian. Officer: How long are you staying? Julia: Five days. I am a tourist. Officer: Enjoy your visit!"),
    ("dialog-02-rome",
     "At Rome airport. Officer: Buongiorno. Passport, please. Julia: Here you are. Officer: Where are you from? Julia: I am from Russia. And I speak a little Italian. Officer: Molto bene! Welcome to Italy."),
    ("dialog-03-tokyo",
     "At Tokyo airport. Officer: Konnichiwa. Are you here for business or holiday? Julia: Holiday. I am from Russia. I am Russian. Officer: Do you speak Japanese? Julia: Only two words: konnichiwa and arigato. Officer: That is a good start!"),
]

VOICE = "Amy"

def gen_one(page, slug, text):
    dest = OUT / f"{slug}.mp3"
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"skip  {slug}.mp3 ({dest.stat().st_size} B)")
        return
    page.goto("https://ttsmp3.com/", wait_until="load", timeout=60000)
    page.wait_for_timeout(1500)
    for sel in ["button:has-text('AGREE')", "button:has-text('Consent')", "button:has-text('Accept')", ".fc-cta-consent"]:
        try:
            b = page.locator(sel).first
            if b.is_visible(timeout=1200):
                b.click(); break
        except Exception:
            pass
    page.wait_for_selector("select#sprachwahl", timeout=30000)
    page.select_option("select#sprachwahl", value=VOICE)
    ta = page.locator("textarea#voicetext")
    ta.wait_for(timeout=15000)
    ta.click()
    ta.fill(text)
    with page.expect_download(timeout=60000) as di:
        page.click("input#downloadenbutton")
    di.value.save_as(str(dest))
    print(f"OK    {slug}.mp3 ({dest.stat().st_size} B)")

with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    ctx = br.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36")
    page = ctx.new_page()
    for slug, text in DIALOGUES:
        try:
            gen_one(page, slug, text); time.sleep(1.5)
        except Exception as e:
            print(f"FAIL  {slug}: {e}")
    br.close()
print(f"\nDone. Files in {OUT}")
