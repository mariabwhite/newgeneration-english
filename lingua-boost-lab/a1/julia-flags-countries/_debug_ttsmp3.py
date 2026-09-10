"""Debug — dump ttsmp3.com layout to find current selectors."""
import sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    br = pw.chromium.launch(headless=True)
    ctx = br.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36")
    page = ctx.new_page()
    page.goto("https://ttsmp3.com/", wait_until="load", timeout=45000)
    page.wait_for_timeout(3500)
    html = page.content()
    p = pathlib.Path(__file__).parent / "_ttsmp3_dump.html"
    p.write_text(html, encoding="utf-8")
    # find textarea, select elements
    print("URL:", page.url)
    print("Title:", page.title())
    for sel in ["textarea", "select", "button", "a"]:
        els = page.locator(sel).all()
        print(f"\n== {sel} ({len(els)}) ==")
        for e in els[:12]:
            try:
                nm = e.evaluate("el => el.id + '|' + el.name + '|' + (el.className||'') + '|' + (el.type||'') + '|' + (el.textContent||'').slice(0,40)")
                print("  ", nm)
            except Exception:
                pass
    br.close()
