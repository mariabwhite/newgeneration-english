"""Palette v3 → Olive. Swaps the sage-moss palette to dusty olive + mustard."""
import re, pathlib
SRC = pathlib.Path(__file__).parent / "index.html"
t = SRC.read_text(encoding="utf-8")

old_root = """:root{
  --bg:#f1eee4; --bg-2:#e2decb; --surface:#ffffff; --card:#f8f4e8; --surface-2:#d2cab2;
  --text:#1e2a1c; --muted:#4a5a44; --faint:#8a9686;
  --accent:#2d5538; --accent-2:#1a3a24; --accent-on:#ffffff;
  --brand:#c87450; --brand-2:#a35538;
  --line:rgba(45,85,56,.18); --line-2:rgba(45,85,56,.36);
  --ok:#4a7a3d; --miss:#a3402c;
  --display:"Unbounded","Manrope",system-ui,sans-serif;
  --body:"Manrope",system-ui,sans-serif;
  --mono:"JetBrains Mono",Consolas,monospace;
}"""
new_root = """:root{
  --bg:#ecebe0; --bg-2:#d8d4b8; --surface:#ffffff; --card:#f3f0dd; --surface-2:#c2bd96;
  --text:#262a18; --muted:#4e5236; --faint:#8a8f6a;
  --accent:#6b7a3d; --accent-2:#4a5724; --accent-on:#ffffff;
  --brand:#b5985c; --brand-2:#8f7640;
  --line:rgba(107,122,61,.20); --line-2:rgba(107,122,61,.40);
  --ok:#5b7a3d; --miss:#a3402c;
  --display:"Unbounded","Manrope",system-ui,sans-serif;
  --body:"Manrope",system-ui,sans-serif;
  --mono:"JetBrains Mono",Consolas,monospace;
}"""
assert old_root in t, "sage root block not found — check prior rebuild"
t = t.replace(old_root, new_root)
t = re.sub(r"rgba\(45,\s*85,\s*56,\s*", "rgba(107,122,61,", t)
t = re.sub(r"rgba\(200,\s*116,\s*80,\s*", "rgba(181,152,92,", t)
t = re.sub(r"rgba\(163,\s*85,\s*56,\s*", "rgba(143,118,64,", t)

SRC.write_text(t, encoding="utf-8")
print(f"olive palette set · {SRC.name} · {len(t)} chars")
