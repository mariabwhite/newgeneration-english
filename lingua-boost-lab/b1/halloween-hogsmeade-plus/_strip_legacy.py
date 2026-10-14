import re, os
p = os.path.join(os.path.dirname(__file__), 'index.html')
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()
pat = r'<!-- /removed legacy H1-H7 sections \(fully replaced by J1-J6 quest above\) -->\n<section class="section" id="legacy-removed-wrapper" hidden>.*?say you\'ve got to move on\.</span>\s*</div>\s*</div>\s*</div>\s*</section>'
new, n = re.subn(pat, '<!-- /removed legacy H1-H7 sections (fully replaced by J1-J6 quest above) -->', s, flags=re.DOTALL)
with open(p, 'w', encoding='utf-8') as f:
    f.write(new)
print('replacements=', n)
print('size_after=', len(new))
