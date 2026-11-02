"""Remove old-capsule-remnant hidden block + party-starter audio ref to missing song-good-morning."""
import pathlib, re
HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"
text = HTML.read_text(encoding="utf-8")

# 1) Remove hidden old-capsule-remnant block
pattern = r"<!-- old-capsule-remnant \(hidden, kept for cleanup pass\) -->\s*<div style=\"display:none\">.*?<!-- /old-capsule-remnant -->"
new = re.sub(pattern, "", text, count=1, flags=re.DOTALL)
assert new != text, "old-capsule-remnant block not found"
text = new

# 2) Replace party-starter audio-row with a simple short note (song-good-morning not generated)
party_old = """<!-- ===== SONG OPENER (compact, no sun button) ===== -->
<section class="party-starter">
  <div class="party-copy" style="grid-column:1/-1">
    <div class="party-title">Press play — wake up with Julia</div>
    <div class="party-sub">Monday morning song. One minute of English before we start the lesson.</div>
    <div class="party-audio-row">
      <span class="lbl">Song</span>
      <audio id="party-song" controls preload="metadata" src="audio/song-good-morning.mp3"></audio>
    </div>
  </div>
</section>"""

# Simpler: just remove the audio-row since the mp3 isn't generated
if party_old in text:
    party_new = """<!-- ===== OPENER (no song mp3 generated · just a short intro note) -->"""
    text = text.replace(party_old, party_new)
    print("Removed party-starter block")
else:
    # fallback: remove just the audio line
    audio_line = '<audio id="party-song" controls preload="metadata" src="audio/song-good-morning.mp3"></audio>'
    text = text.replace(audio_line, '<span style="color:var(--muted);font-size:.86rem;font-style:italic">(song to be added)</span>')
    print("Replaced song audio with placeholder note")

HTML.write_text(text, encoding="utf-8")
print(f"Done. File size: {len(text)} chars.")
