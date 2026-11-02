"""Wrap sections into 4 tabs (Julia's canon from pet-shop-snail).

Tabs:
  📖 Story      → warm-up riddle + Meet the Family (reading + bios + TF + dialogue + who-said)
  🐾 Vocab      → sec-vocab-shopping, sec-vocab-fair, sec-vocab-hall
  🔀 Grammar    → sec-grammar (6 tenses table + 12 MCQ + 15 irregular verbs)
  📝 Workbook   → sec-07 Theory corner + sec-08 Big Recap + sec-09 Vocab Capsule

Also injects the tab-bar HTML + JS click handler.
"""
import pathlib
HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"
text = HTML.read_text(encoding="utf-8")

# 1) Insert tab-bar + open <div id="tab-story"> AFTER cast-strip, BEFORE sec-01 warm-up riddle
anchor_before_warmup = '<!-- ===== 1 · WARM-UP RIDDLE ===== -->'
tab_bar_html = """<!-- ===== TAB BAR (Julia's canon · 4 tabs) ===== -->
<nav class="tab-bar">
  <button class="tab-btn active" data-tab="story">📖 Урок</button>
  <button class="tab-btn" data-tab="vocab">🐾 Vocab</button>
  <button class="tab-btn" data-tab="grammar">🔀 Grammar</button>
  <button class="tab-btn" data-tab="workbook">📝 Рабочая тетрадь</button>
</nav>

<div id="tab-story" class="tab-panel active">

"""
assert text.count(anchor_before_warmup) == 1
text = text.replace(anchor_before_warmup, tab_bar_html + anchor_before_warmup)

# 2) Close </div> for tab-story + open tab-vocab BEFORE sec-vocab-shopping
anchor_vocab_start = '<!-- ===== 3 · VOCAB RECALL · SHOPPING DAY (containers + shop lexis) ===== -->'
vocab_switch = """</div><!-- /tab-story -->

<div id="tab-vocab" class="tab-panel">

"""
assert text.count(anchor_vocab_start) == 1
text = text.replace(anchor_vocab_start, vocab_switch + anchor_vocab_start)

# 3) Close vocab + open grammar BEFORE sec-grammar
anchor_grammar_start = "<!-- ===== 6 · GRAMMAR RECAP · ALL TENSES WITHOUT A MONDAY FRAME ===== -->"
grammar_switch = """</div><!-- /tab-vocab -->

<div id="tab-grammar" class="tab-panel">

"""
assert text.count(anchor_grammar_start) == 1
text = text.replace(anchor_grammar_start, grammar_switch + anchor_grammar_start)

# 4) Close grammar + open workbook BEFORE sec-07 Theory corner
anchor_workbook_start = "<!-- ===== 7 · THEORY CORNER · WILL vs GOING TO ===== -->"
workbook_switch = """</div><!-- /tab-grammar -->

<div id="tab-workbook" class="tab-panel">

"""
assert text.count(anchor_workbook_start) == 1
text = text.replace(anchor_workbook_start, workbook_switch + anchor_workbook_start)

# 5) Close workbook BEFORE wrap-up
anchor_wrapup = "<!-- ===== WRAP-UP ===== -->"
close_last = """</div><!-- /tab-workbook -->

"""
assert text.count(anchor_wrapup) == 1
text = text.replace(anchor_wrapup, close_last + anchor_wrapup)

# 6) Inject JS tab-switcher into existing <script> block (before the closing IIFE line)
# Find the IIFE closer "})();" of the first inline script block
js_tab = """
  // Tab switcher (Julia's canon · 4 tabs)
  document.querySelectorAll('.tab-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const key=btn.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
      btn.classList.add('active');
      const panel=document.getElementById('tab-'+key);
      if(panel)panel.classList.add('active');
      // scroll smoothly to tab-bar top so new tab starts at top of viewport
      const bar=document.querySelector('.tab-bar');
      if(bar){const y=bar.getBoundingClientRect().top+window.scrollY-60;window.scrollTo({top:y,behavior:'smooth'});}
    });
  });
"""
# Insert BEFORE "})();" line that closes the main IIFE
# We find the last occurrence inside the first <script>...</script> block.
# Simplest: find "// Scroll-to-top sticky button" area and inject right after it
anchor_scroll_block_end = '    topBtn.addEventListener(\'click\',()=>window.scrollTo({top:0,behavior:\'smooth\'}));\n  }'
assert anchor_scroll_block_end in text, "scroll-top handler marker not found"
text = text.replace(anchor_scroll_block_end, anchor_scroll_block_end + "\n" + js_tab)

HTML.write_text(text, encoding="utf-8")
print(f"Done: tabs inserted. File size: {len(text)} chars.")
