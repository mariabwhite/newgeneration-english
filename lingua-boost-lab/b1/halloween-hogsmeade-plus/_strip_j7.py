import re, os
p = os.path.join(os.path.dirname(__file__), 'index.html')
with open(p, 'r', encoding='utf-8') as f: s = f.read()
pat = r'<!-- ═════════════════ QUEST STAGE 7 · 10 STRONG IELTS CONSTRUCTIONS ═════════════════ -->.*?<section class="section" id="quest-ielts">.*?</section>\s*(?=</div>\s*<!-- ╚═)'
new, n = re.subn(pat, '', s, flags=re.DOTALL)
with open(p, 'w', encoding='utf-8') as f: f.write(new)
print('J7 removed:', n)
print('new size:', len(new))
