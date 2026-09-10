"""Generate 7 postcard MP3 clips via ttsmp3.com using Playwright.
Run: python _gen_postcards_ttsmp3.py
"""
import sys, pathlib, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(__file__).parent / "assets" / "audio"
OUT.mkdir(parents=True, exist_ok=True)

POSTCARDS = [
    ("postcard-01-italy",
     "Ciao, mum! I'm in Rome. My friend Marco is Italian — of course! He speaks Italian so fast, but he teaches me two words a day. Yesterday we ate pizza in a small café."),
    ("postcard-02-japan",
     "Hi from Tokyo! It is very big. My host sister Yuki is Japanese. She speaks Japanese and a little English. She showed me how to write my name in Japanese letters."),
    ("postcard-03-brazil",
     "Hola from Brasilia! Well — actually it's olá, not hola, because in Brazil people speak Portuguese, not Spanish. That surprised me. The currency here is the real."),
    ("postcard-04-greece",
     "Kalimera from Athens! Sophia is Greek. She showed me the letters of the Greek alphabet. Some of them look like maths! I bought feta cheese and olives at the market."),
    ("postcard-05-turkey",
     "Merhaba from Istanbul. My friend Emre is Turkish. We drank tiny cups of tea. The capital of Turkey is Ankara, not Istanbul — I always forget!"),
    ("postcard-06-india",
     "Namaste from New Delhi! Priya is Indian. Today we visited the Taj Mahal — well, actually it's in Agra, so we took a train. Priya speaks Hindi and perfect English."),
    ("postcard-07-mexico",
     "Hola from Mexico City! Diego is Mexican and speaks Spanish. He took me for tacos with three kinds of hot sauce. I could not stop drinking water."),
]

VOICE = "Amy"  # calm BrE female (AWS Polly via ttsmp3.com)

def gen_one(page, slug, text):
    dest = OUT / f"{slug}.mp3"
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"skip  {slug}.mp3 ({dest.stat().st_size} B)")
        return
    page.goto("https://ttsmp3.com/", wait_until="load", timeout=60000)
    page.wait_for_timeout(1500)
    # accept cookies if popup shows
    for sel in ["button:has-text('AGREE')", "button:has-text('Consent')", "button:has-text('Accept')", "[aria-label='Consent']", ".fc-cta-consent"]:
        try:
            b = page.locator(sel).first
            if b.is_visible(timeout=1200):
                b.click(); break
        except Exception:
            pass
    # pick voice by value (Amy)
    page.wait_for_selector("select#sprachwahl", timeout=30000)
    page.select_option("select#sprachwahl", value=VOICE)
    # paste text
    ta = page.locator("textarea#voicetext")
    ta.wait_for(timeout=15000)
    ta.click()
    ta.fill(text)
    # "Download as MP3" is an <input type=submit> — clicking it starts synthesis and returns the file
    with page.expect_download(timeout=60000) as di:
        page.click("input#downloadenbutton")
    d = di.value
    d.save_as(str(dest))
    print(f"OK    {slug}.mp3 ({dest.stat().st_size} B)")

with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    ctx = br.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36")
    page = ctx.new_page()
    for slug, text in POSTCARDS:
        try:
            gen_one(page, slug, text)
            time.sleep(1.5)
        except Exception as e:
            print(f"FAIL  {slug}: {e}")
    br.close()
print(f"\nDone. Files in {OUT}")
