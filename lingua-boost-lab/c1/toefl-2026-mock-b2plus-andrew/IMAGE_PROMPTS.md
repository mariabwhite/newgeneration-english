# Image prompts · Diagnostic Mock · Andrew

Palette shared across all images (Lab brand):
- cream background `#fff7ea`
- warm orange accent `#c86832`
- deep brown ink `#2e1f14`
- gold highlight `#e8a238`

Style rules (all 6 prompts):
- Flat editorial / lifestyle magazine aesthetic, soft natural light
- No readable text anywhere
- No faces, no identifiable people
- No logos, no brand marks
- No gradients beyond the color blocks
- All images: generate 2 variations to pick from

Deliver into `./assets/img/` with these filenames (so the HTML can wire them in later):

| Slot | Filename | Where in Lab | Aspect | Purpose |
|---|---|---|---|---|
| 1 | `hero.webp` | Hero card (replaces current gradient) | 16:9 | Overall mock vibe |
| 2 | `img-s04.webp` | Section 04 header | 16:9 | Daily-life reading |
| 3 | `img-s05.webp` | Section 05 passage header | 16:9 | Academic reading theme |
| 4 | `img-s09.webp` | Section 09 Academic Talk | square | Background music + study |
| 5 | `img-s11.webp` | Section 11 Email task | 16:9 | Writing an email |
| 6 | `img-s15.webp` | Section 15 Scoring summary | square | Diagnostic dial / 1–6 bands |

---

## 1 · Hero · `hero.webp` · 16:9

> Warm-tone minimalist flat-lay on a cream desk (#fff7ea), top-down 90° angle: an open English textbook with blurred illegible pages, a slim mechanical pencil resting across it, a brass wristwatch showing 11:00, a small cup of black coffee, scattered colored sticky notes in warm orange (#c86832) and gold (#e8a238), the corner of a slim laptop showing a blurred scoring dashboard with four colored bars (no readable numbers), one small houseplant in a terracotta pot. Soft morning light from the left. Palette: cream background, warm orange and gold accents, muted brown ink. Editorial lifestyle photography, 35mm feel, soft shadows, high-end magazine aesthetic. 16:9 landscape. No readable text, no faces, no logos.

## 2 · Reading · Daily Life · `img-s04.webp` · 16:9

> Clean library bulletin-board scene: a quiet reading hall in soft morning light, warm wooden shelves blurred in the background, a corkboard in focus with three pinned paper notices (all notices deliberately blurred / illegible). On the desk below, a sealed water bottle and a laminated opening-hours card (text illegible). Palette: cream (#fff7ea), warm oak brown, brass accents, a single warm orange (#c86832) pin on the corkboard. Editorial flat photography feel, horizontal 16:9. No readable text, no faces, no logos.

## 3 · Reading · Academic passage "Why we forget what we read" · `img-s05.webp` · 16:9

> Warm minimalist editorial illustration: a reader seen only from behind (no identifiable features) sitting in a soft armchair, holding an open book. Above the head, small fragments of letters and partial words float upwards and softly dissolve into the air like gentle smoke, suggesting fading memory. The floating fragments must be abstract shapes, not readable words. Palette: cream (#fff7ea) background, warm orange (#c86832) and gold (#e8a238) highlights on the chair fabric and book spine. Flat editorial vector illustration, no outlines, no faces. 16:9 landscape. No readable text, no logos.

## 4 · Listening · Academic Talk "Background music while studying" · `img-s09.webp` · square

> Top-down flat-lay of a wooden study desk at night: open notebook with illegible pencil marks that look like handwriting but are not readable, a pair of over-ear headphones resting on the pages, a small cup of herbal tea, a tiny houseplant, a warm desk lamp casting a soft golden pool of light from the top-right corner. Palette: cream (#fff7ea), warm brown wood, brass lamp, soft orange (#c86832) accent on the headphones cushion. Editorial flat-lay photography, square aspect ratio. No readable text, no faces, no logos.

## 5 · Writing · Email · `img-s11.webp` · 16:9

> Minimalist editorial illustration: a laptop screen showing an email interface draft (interface shapes present but the text is deliberately blurred and illegible). On the keyboard rests a hand (fingers only, cut off at the wrist — no identifiable features). A cold half-finished cup of coffee next to the laptop; a window in the background showing warm dusk light coming through half-closed blinds. Palette: cream (#fff7ea) background, warm orange (#c86832) accent on the laptop power light and coffee cup rim, muted brown everywhere else. Flat editorial illustration, 16:9 landscape, no readable text, no face, no logo.

## 6 · Scoring / Diagnostic dial · `img-s15.webp` · square

> Flat editorial illustration of a scoring gauge card: a half-circle dial with six clearly separated color-coded band segments labelled only with large numerals 1, 2, 3, 4, 5, 6 (these digits are the ONLY readable glyphs in the image — nothing else). A dial needle points between bands 3 and 4, suggesting a mid-range diagnostic result. Palette: cream (#fff7ea) card background, warm orange (#c86832) needle and band 4, gold (#e8a238) for band 5-6, muted red for band 1-2, deep brown (#2e1f14) outlines. Minimalist UI dashboard aesthetic, flat vector, square aspect. No logos, no faces.

---

## Generation hints

- **If using ChatGPT / DALL-E 3**: paste one prompt at a time, request 2 variations, download PNG, then convert to webp (quality 80) to save bandwidth.
- **If using Gamma**: these prompts work in Gamma's "generate image" flow — expect flatter illustration output than photographic.
- **If using Flux Kontext**: lead with the style tag (`flat editorial illustration`, `top-down flat-lay`), then composition, then palette. Flux follows this ordering.
- **File sizes**: all webp outputs should be under 200 KB. If larger, run through squoosh.app at quality 75.
- **Fallback**: if the hero image is not ready by lesson time, the current gradient-only hero works fine — do NOT block deployment on images.
