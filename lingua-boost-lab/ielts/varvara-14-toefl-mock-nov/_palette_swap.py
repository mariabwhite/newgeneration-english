"""One-shot palette swap: beige-warm (Andrew v1) → museum archive (Varya v14).

Palette v3 — Prussian blue + warm cream + classical gold:
  bg #f3efe8 · bg-2 #e8ddc8 · card #fbf7ee · surface-2 #d9ccb0
  text #15213f · muted #3f4b6a · faint #8591a5
  accent #1e3461 (prussian blue) · accent-2 #0a1535 (deep prussian)
  brand #bc8d3d (museum gold) · brand-2 #a3792e (antique brass)
  ok #4b6b43 · miss #a83a2d
"""
import re, pathlib, sys

SRC = pathlib.Path(__file__).parent / "index.html"
text = SRC.read_text(encoding="utf-8")

# 1. Full CSS :root block replacement (lines 14-24 in source)
old_root = """:root{
  --bg:#fff7ea; --bg-2:#faead0; --surface:#ffffff; --card:#fffbf3; --surface-2:#f6e6c8;
  --text:#2e1f14; --muted:#7a6552; --faint:#a89a86;
  --accent:#c86832; --accent-2:#9c4b1e; --accent-on:#ffffff;
  --brand:#e8a238; --brand-2:#f5b54d;
  --line:rgba(200,104,50,.18); --line-2:rgba(200,104,50,.36);
  --ok:#6b9d3f; --miss:#c04a3a;
  --display:"Unbounded","Manrope",system-ui,sans-serif;
  --body:"Manrope",system-ui,sans-serif;
  --mono:"JetBrains Mono",Consolas,monospace;
}"""
new_root = """:root{
  --bg:#f3efe8; --bg-2:#e8ddc8; --surface:#ffffff; --card:#fbf7ee; --surface-2:#d9ccb0;
  --text:#15213f; --muted:#3f4b6a; --faint:#8591a5;
  --accent:#1e3461; --accent-2:#0a1535; --accent-on:#ffffff;
  --brand:#bc8d3d; --brand-2:#a3792e;
  --line:rgba(30,52,97,.18); --line-2:rgba(30,52,97,.36);
  --ok:#4b6b43; --miss:#a83a2d;
  --display:"Unbounded","Manrope",system-ui,sans-serif;
  --body:"Manrope",system-ui,sans-serif;
  --mono:"JetBrains Mono",Consolas,monospace;
}"""
assert old_root in text, "CSS :root block not found verbatim"
text = text.replace(old_root, new_root)

# 2. Bulk rgba() swaps throughout file
# Burnt orange (--accent old) → Prussian blue (--accent new)
text = re.sub(r"rgba\(200,\s*104,\s*50,\s*", "rgba(30,52,97,", text)
# Golden brand (old) → Museum gold (new)
text = re.sub(r"rgba\(232,\s*162,\s*56,\s*", "rgba(188,141,61,", text)
# Light gold (brand-2 old) → Antique brass (brand-2 new)
text = re.sub(r"rgba\(245,\s*181,\s*77,\s*", "rgba(163,121,46,", text)

# 3. Rename "Andrew" references (keep inside quoted test content strings as is, but swap hero + cabinet references)
# Heuristic: standalone "Andrew" word boundary
# NOTE: preserve content quotes; just swap meta title / hero headings
# We do specific swaps in Edit tool instead to avoid false positives

SRC.write_text(text, encoding="utf-8")
print(f"palette swapped · {SRC.name} · {len(text)} chars")
