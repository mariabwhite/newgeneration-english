"""Restore Hogsmeade tab (tab 2) by copying block-00 through reward from Katya's original lesson,
then injecting it into the halloween-hogsmeade-plus index.html inside a fresh
<div class="hw-pane" data-pane="hogsmeade" hidden>...</div> wrapper that lives after the Halloween pane close."""
import os, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, 'index.html')
SOURCE = os.path.abspath(os.path.join(HERE, '..', '..', 'a2', 'katya-10-hogsmeade-weekend', 'index.html'))

with open(SOURCE, 'r', encoding='utf-8') as f:
    src = f.read()

# Extract from first "<!-- 00 · RECAP -->" comment-area start through end of reward section (before footer).
# Boundaries used:
# start: <section class="section" id="block-00">
# end: last </section> before <footer>
m_start = src.find('<section class="section" id="block-00">')
assert m_start > 0, 'block-00 not found in source'
m_footer = src.find('<footer>')
assert m_footer > 0, 'footer not found in source'
# find the last </section> before footer
sub = src[m_start:m_footer]
last_sec_end = sub.rfind('</section>')
assert last_sec_end > 0
hogsmeade_content = sub[:last_sec_end + len('</section>')]

# Fix image paths — Katya's used relative `assets/img/...`, same as our folder, so no rewrite needed.
# But the "Katya" references in reward and footer—leave as-is for now (Maria said copy FULL as-is).

print(f'Source Hogsmeade content: {len(hogsmeade_content)} chars')

with open(TARGET, 'r', encoding='utf-8') as f:
    tgt = f.read()

# Find Halloween pane close marker — we close Halloween pane right before the former Hogsmeade wrapper.
# Our file currently likely has: </section> (last J★ or glossary) \n </div> \n <!-- ╚═════ ... halloween close
# Let's just look for the comment "╔══════════════════════════ TAB 2 · ХОГСМИД" — in current state it's gone, so we search for the Halloween pane close.

# Current Halloween pane opens at '<div class="hw-pane" data-pane="halloween"' and closes somewhere with </div><!-- ╚═══
# Let's find the closing </div>\n<!-- ╚ pattern immediately after a quest-glossary </section>

glossary_section_pattern = r'(<section class="section" id="quest-glossary">.*?</section>)'
glossary_match = re.search(glossary_section_pattern, tgt, flags=re.DOTALL)
assert glossary_match, 'quest-glossary section not found'
glossary_end_pos = glossary_match.end()

# Find the next </div> after glossary — that is the Halloween pane close.
# If there is already a close, we leave it. Otherwise, after glossary </section>, inject:
#    </div>\n<!-- ╚═ halloween close ═╝ -->\n<!-- ╔═ TAB 2 ═╗ -->\n<div class="hw-pane" data-pane="hogsmeade" hidden>\n[HOGSMEADE CONTENT]\n</div>\n<!-- ╚═ hogsmeade close ═╝ -->

after_glossary = tgt[glossary_end_pos:]
# Does Halloween pane already close here?  Look for '</div>' with pane-close comment within ~200 chars.
close_match = re.search(r'^\s*</div>\s*<!--\s*╚', after_glossary)

tail_remainder = tgt[glossary_end_pos:]

if close_match:
    # Halloween pane already closes — slice between the close marker and the <footer>
    hw_close_end = glossary_end_pos + close_match.end()
    # find <footer> after that
    footer_pos = tgt.find('<footer>', hw_close_end)
    # inject hogsmeade pane between hw_close_end and footer_pos (keeping whatever whitespace is between)
    injection = (
        '\n\n<!-- ╔══════════════════════════ TAB 2 · ХОГСМИД (full Katya L10 copy) ══════════════════════════╗ -->\n'
        '<div class="hw-pane" data-pane="hogsmeade" role="tabpanel" hidden>\n\n'
        + hogsmeade_content +
        '\n\n</div>\n<!-- ╚═════════════════════════════════════════════════╝ -->\n'
    )
    new_tgt = tgt[:hw_close_end] + injection + tgt[footer_pos:]
else:
    # Halloween pane does NOT close yet — close it AND open+fill+close hogsmeade pane right away
    footer_pos = tgt.find('<footer>', glossary_end_pos)
    assert footer_pos > 0
    injection = (
        '\n\n</div>\n'
        '<!-- ╚═══════════════ halloween pane close ═══════════════╝ -->\n\n'
        '<!-- ╔══════════════════════════ TAB 2 · ХОГСМИД (full Katya L10 copy) ══════════════════════════╗ -->\n'
        '<div class="hw-pane" data-pane="hogsmeade" role="tabpanel" hidden>\n\n'
        + hogsmeade_content +
        '\n\n</div>\n<!-- ╚═════════════════════════════════════════════════╝ -->\n\n'
    )
    new_tgt = tgt[:glossary_end_pos] + injection + tgt[footer_pos:]

with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(new_tgt)

print(f'Target size before: {len(tgt):,}')
print(f'Target size after : {len(new_tgt):,}')
print('Hogsmeade restored.')
