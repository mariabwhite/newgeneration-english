# Audio scripts · Diagnostic Mock TOEFL iBT 2026 (B2+ ceiling) · Andrew

All files live in `./audio/` relative to `index.html`.

**Voice map (edge-tts):**

- Matthew = `en-US-GuyNeural`
- Joanna = `en-US-JennyNeural`
- **Do NOT use** `en-US-DavisNeural` — dead voice, synth will fail silently.

**Rates:**

- Section 06 (Choose a Response) → `+0%`
- Section 07 (Conversation) → `+0%`
- Section 08 (Announcement) → `-5%`
- Section 09 (Academic Talk) → `-5%`
- Section 13 (Listen-and-Repeat) → `-8%`
- Section 14 (Interview questions) → `+0%`

Total clips: **19** (5 + 1 + 1 + 1 + 7 + 4). Section 07 is one dialogue → one `conv-07.mp3` built by concatenating 11 per-turn clips, or synthesize whole script with a dialogue-aware voice.

---

## Section 06 · Choose a Response × 5

### `lstn-06-01.mp3` · Joanna · rate +0%
> Excuse me, do you know where I can print this document before class?

### `lstn-06-02.mp3` · Matthew · rate +0%
> We're having a small barbecue at my place on Saturday afternoon — want to come?

### `lstn-06-03.mp3` · Joanna · rate +0%
> My laptop keeps freezing every ten minutes or so — any idea what might be wrong?

### `lstn-06-04.mp3` · Matthew · rate +0%
> It's almost ten o'clock. Would you like a quick coffee before we head home?

### `lstn-06-05.mp3` · Joanna · rate +0%
> There are two trains back — one at six twenty and one at nine forty. Which one would you take?

---

## Section 07 · Conversation (70 sec) · `conv-07.mp3`

**Setting:** Student goes to the registrar's office hoping to drop a course after the official drop deadline. The admin is firm about the rule but offers an Incomplete grade. 11 turns, ~70 seconds total at natural pace.

**Voice tags:** STUDENT = Joanna (`en-US-JennyNeural`). ADMIN = Matthew (`en-US-GuyNeural`).

**Option A · one combined file** (if your pipeline supports speaker switches, synthesize each turn separately and concatenate with ~250 ms silence between turns):

### Turn 1 · STUDENT (Joanna)
> Hi, sorry to bother you — I was wondering if I could still drop one of my courses, Economics 240?

### Turn 2 · ADMIN (Matthew)
> Let me check the dates. Hmm — the drop deadline for this semester was October the first. We're almost two weeks past that.

### Turn 3 · STUDENT (Joanna)
> I know, I'm really sorry. The workload turned out heavier than I expected, and I'm worried I'll fail it.

### Turn 4 · ADMIN (Matthew)
> I understand, but the deadline exists for a reason. If I let you drop now, I'd have to let everyone else drop too — and the course is already past the midterm.

### Turn 5 · STUDENT (Joanna)
> Isn't there any way to make an exception? My other courses are fine, it's just this one.

### Turn 6 · ADMIN (Matthew)
> I can't change the drop status, no. But what I can do is talk to you about an Incomplete.

### Turn 7 · STUDENT (Joanna)
> An Incomplete? How does that work?

### Turn 8 · ADMIN (Matthew)
> You'd get an "I" on your transcript instead of a grade, and you'd have one semester to finish the missing work. If you finish, the "I" is replaced with your real grade. If you don't, it turns into an F.

### Turn 9 · STUDENT (Joanna)
> So I'd have until the end of the spring semester to catch up?

### Turn 10 · ADMIN (Matthew)
> Exactly. Your instructor has to agree first — I'd recommend talking to Dr Patel this week. If he signs off, come back here with the form and I'll process it the same day.

### Turn 11 · STUDENT (Joanna)
> Okay, that's actually a lot more helpful than I expected. Thank you — I'll go see him tomorrow.

**Option B · single-script synth** (if voice-switch isn't supported, cue the file as a plain narration with "Student:" and "Administrator:" labels spoken aloud — less clean but functional).

---

## Section 08 · Announcement · `ann-08.mp3` · Matthew · rate -5%

~50 sec, campus-library PA announcement register.

> Good morning, everyone. This is a brief update from the Main Library ahead of exam week. From Monday the eleventh through Friday the fifteenth, the library will open at seven a.m. instead of nine, and close at midnight instead of ten p.m., to give you extra time to prepare.
>
> Please note that during this week the entire third floor will be a silent-study floor — no group work, no phone calls. Group study rooms on the first floor can still be booked online for conversation.
>
> One more thing: because of complaints last term, only water in sealed bottles is allowed inside the library during exam week. No coffee, no food, no snacks — please use the café on the ground floor. Thank you, and good luck with your exams.

---

## Section 09 · Academic Talk · `talk-09.mp3` · Joanna · rate -5%

~90 sec, 160–180 words, light academic register. Mini-lecture: "Why humans like background music while they study."

> Many of us have a strong preference for studying with music in the background. Why is that, and does it actually help? Research on this is more mixed than people often assume, but there's a reasonable summary we can offer today.
>
> The usual starting point is a study by a group of psychologists at Glasgow University. They found that students revising for a maths exam performed slightly better when they had instrumental music playing at a low, steady volume, compared with students working in complete silence. The effect was small but consistent. The leading explanation is that gentle, familiar sound masks random noise from the environment and reduces the mental energy you spend ignoring distractions.
>
> However — and this is important — the same researchers found no benefit, and sometimes a clear cost, when the music had lyrics, or when the volume was high enough to grab attention. And for tasks involving heavy reading or genuinely new material, silence is probably still the safer default.

---

## Section 13 · Listen-and-Repeat × 7 · rate -8%

### `lnr-13-01.mp3` · Joanna · 6 words
> I usually have coffee for breakfast.

### `lnr-13-02.mp3` · Matthew · 8 words
> My brother works at a small design studio.

### `lnr-13-03.mp3` · Joanna · 10 words
> We're planning a short trip to the mountains next weekend.

### `lnr-13-04.mp3` · Matthew · 12 words
> If the weather is good tomorrow, we'll probably eat lunch outside.

### `lnr-13-05.mp3` · Joanna · 13 words
> She told me she had already seen that film at least twice before.

### `lnr-13-06.mp3` · Matthew · 15 words
> The book I ordered online last week finally arrived, and it looks even better than expected.

### `lnr-13-07.mp3` · Joanna · 16 words
> Despite feeling tired after the long flight, he unpacked his things and went straight to the office.

---

## Section 14 · Interview questions × 4 · rate +0%

Each clip is just the examiner's question read once; the student answers off-mic. Keep the delivery natural, not slow.

### `intv-14-01.mp3` · Joanna
> Describe your typical morning. What do you usually do between waking up and leaving the house?

### `intv-14-02.mp3` · Matthew
> Do you prefer spending your free time alone or with other people? Why?

### `intv-14-03.mp3` · Joanna
> Describe a city you have visited that stayed in your memory. What made it memorable?

### `intv-14-04.mp3` · Matthew
> If you could change one thing about the way you learn English, what would it be and why?

---

## Suggested edge-tts command (reference)

```powershell
# Example — Matthew clip, default rate
edge-tts --voice en-US-GuyNeural --text "..." --write-media ann-08.mp3 --rate=-5%

# Joanna, L&R item, slowed
edge-tts --voice en-US-JennyNeural --text "I usually have coffee for breakfast." --write-media lnr-13-01.mp3 --rate=-8%
```

For `conv-07.mp3`, synthesize each of the 11 turns to a separate temp file, then concat with ffmpeg:

```powershell
# After generating conv-07-01.mp3 ... conv-07-11.mp3
ffmpeg -f concat -safe 0 -i list.txt -c copy conv-07.mp3
```

where `list.txt` lists the turn files in order, each preceded by a short pre-baked silence (`silence-250ms.mp3`) to make speaker switches audible.
