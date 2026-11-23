"""Full rebuild of Andrew v1 TOEFL mock → Varya v14 "November mock".

All text replaced with fresh topics (no museum/archive/art-history).
Palette: sage moss + warm cream + muted coral (distinct from Andrew v1 beige and v2 grey).
Audio files are inherited from Andrew v1 — regenerate via _gen_audio.py.

Run from folder: python _rebuild.py
"""
import re, pathlib

SRC = pathlib.Path(__file__).parent / "index.html"
t = SRC.read_text(encoding="utf-8")

# ============================================================
# 1. PALETTE · sage moss + warm cream + muted coral
# ============================================================
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
assert old_root in t, "root block missing"
t = t.replace(old_root, new_root)
t = re.sub(r"rgba\(200,\s*104,\s*50,\s*", "rgba(45,85,56,", t)
t = re.sub(r"rgba\(232,\s*162,\s*56,\s*", "rgba(200,116,80,", t)
t = re.sub(r"rgba\(245,\s*181,\s*77,\s*", "rgba(163,85,56,", t)

# ============================================================
# 2. META + HEAD TITLE
# ============================================================
t = t.replace(
    "<title>Diagnostic Mock · TOEFL iBT 2026 · B2+ ceiling · Andrew · LinguaBoost Lab</title>",
    "<title>L14 · TOEFL iBT 2026 Mock · November · C1 · Varya · LinguaBoost Lab</title>",
)
t = t.replace(
    '<meta name="description" content="Diagnostic TOEFL iBT 2026 mock for Andrew Kruglov — B2 / B2+ ceiling. Reading × 29 · Listening × 14 · Writing × 10 BS + Email + Academic Discussion · Speaking × 7 Listen-and-Repeat + 4 Interview. Banded 1–6 per section with weakest-section diagnostic.">',
    '<meta name="description" content="Full TOEFL iBT 2026 mock for Varya · C1 ceiling · November variant. Reading × 29 · Listening × 14 · Writing × 10 BS + Email + Academic Discussion · Speaking × 7 Listen-and-Repeat + 4 Interview. Banded 1–6 per section.">',
)

# ============================================================
# 3. TOPBAR + HERO
# ============================================================
t = t.replace(
    '<span class="brand-sub">c1/toefl-2026-mock-b2plus-andrew</span>',
    '<span class="brand-sub">ielts/varvara-14-toefl-mock-nov</span>',
)
t = t.replace(
    '<span class="pill">Diagnostic Mock · TOEFL iBT 2026 · B2+ ceiling</span>',
    '<span class="pill">L14 · TOEFL iBT 2026 Mock · November · C1</span>',
)
t = t.replace(
    '<div class="eyebrow">C1 · Adult · TOEFL iBT 2026 · Diagnostic · B2+ ceiling</div>',
    '<div class="eyebrow">C1 · Adult · TOEFL iBT 2026 · November full mock</div>',
)
t = t.replace(
    '<h1 class="hero-title">Diagnostic Mock Test — <span class="grad">TOEFL iBT 2026</span></h1>',
    '<h1 class="hero-title">L14 · TOEFL iBT 2026 — <span class="grad">November Mock</span></h1>',
)
t = t.replace(
    '<p class="hero-lead">This is a <strong>calibration run</strong>, not a real exam and not a hard C1 test. Four sections cover the full 2026 blueprint at a <strong>B2 / B2+ ceiling</strong> so we can see your working baseline when the content is comfortably in range. Each section is scored on a <strong>1&ndash;6 band</strong>, with an overall average at the end and an automatic note on your weakest section — that is what the next lesson will target. Honest effort gives us a useful signal; rushing or guessing does not.</p>',
    '<p class="hero-lead">A fresh <strong>full TOEFL iBT 2026 mock</strong> at <strong>C1 ceiling</strong>, with all four sections and new content — campus life, psychology, biology, education policy — not a diagnostic retread. Each section is scored on a <strong>1&ndash;6 band</strong>, with an overall average at the end and an auto note on your weakest section — that is what the next lesson targets. Honest effort gives us a useful signal; rushing or guessing does not.</p>',
)
t = t.replace(
    '<div class="stat"><div class="stat-k">Difficulty</div><div class="stat-v">B2 / B2+</div></div>',
    '<div class="stat"><div class="stat-k">Difficulty</div><div class="stat-v">C1 ceiling</div></div>',
)

# ============================================================
# 4. S04 · READING DAILY LIFE × 3 (full block)
# ============================================================
old_s04_body = """    <div class="task-tag">P1 · Library notice</div>
    <div class="notice">
      <div class="notice-h">Central Public Library — Opening Hours (Autumn 2026)</div>
      <div class="notice-sub">Effective 1 October through 31 January</div>
      <p>Monday to Friday: 09:00 – 20:00. Saturday: 10:00 – 18:00. Sunday: closed, except for the Children's Reading Room, which opens 11:00 – 15:00.</p>
      <p>The library will also be closed on public holidays and on 24 December. Printing and photocopying are available on the ground floor during opening hours. The first ten pages per day are free for registered members; after that, each page costs 20 cents. Colour printing is not available at this branch — please visit the East Branch for colour jobs.</p>
    </div>"""
new_s04_p1 = """    <div class="task-tag">P1 · Writing-centre appointment email</div>
    <div class="notice">
      <div class="notice-h">Email · From J. Whitfield, Writing Centre · To: ARTH 210 students</div>
      <div class="notice-sub">Subject: 30-minute appointments — new booking rules this term</div>
      <p>Hi all,</p>
      <p>Starting this week, Writing Centre appointments move to a two-tier system. <strong>Thirty-minute slots</strong> are reserved for current-draft feedback: bring a printed or shared Google Doc of at least one full page. <strong>Fifteen-minute drop-ins</strong> are for brainstorming, thesis framing and citation questions — no draft required.</p>
      <p>Book through the online portal at least 24 hours ahead for 30-min slots; drop-ins are first-come, first-served from 14:00 on weekdays. If you miss two booked appointments without cancelling, the system automatically blocks further bookings for two weeks — please cancel through the portal if your plans change.</p>
      <p>Best, Jamie Whitfield</p>
    </div>"""
t = t.replace(old_s04_body, new_s04_p1)

# s04 MCQ 1-3 (library)
t = t.replace(
    """    <div class="mcq-row" data-answer="B">
      <div class="mcq-q"><strong>1.</strong> On a normal Sunday, which part of the library is open?</div>
      <div class="mcq-opts">
        <button data-v="A">A. The whole library, 10:00 – 18:00</button>
        <button data-v="B">B. Only the Children's Reading Room, 11:00 – 15:00</button>
        <button data-v="C">C. Only the printing area on the ground floor</button>
        <button data-v="D">D. Nothing — the building is closed all day</button>
      </div>
      <div class="mcq-note">The notice says Sunday is closed <em>except for the Children's Reading Room</em> 11:00 – 15:00.</div>
    </div>
    <div class="mcq-row" data-answer="C">
      <div class="mcq-q"><strong>2.</strong> A registered member prints 14 pages in black and white in one day. How much does she pay?</div>
      <div class="mcq-opts">
        <button data-v="A">A. Nothing — the first 14 pages are free</button>
        <button data-v="B">B. 20 cents in total</button>
        <button data-v="C">C. 80 cents (4 pages × 20 cents)</button>
        <button data-v="D">D. 2 dollars 80 (14 pages × 20 cents)</button>
      </div>
      <div class="mcq-note">First 10 pages free, then 20¢ per page × 4 extra pages = 80¢.</div>
    </div>
    <div class="mcq-row" data-answer="D">
      <div class="mcq-q"><strong>3.</strong> If you need a colour print, what should you do?</div>
      <div class="mcq-opts">
        <button data-v="A">A. Ask staff at this branch for the colour printer in the back</button>
        <button data-v="B">B. Wait until the Children's Reading Room opens</button>
        <button data-v="C">C. Pay the standard 20 cents per page at this branch</button>
        <button data-v="D">D. Go to the East Branch, which handles colour jobs</button>
      </div>
      <div class="mcq-note">The notice is explicit: colour is not available at this branch — go to the East Branch.</div>
    </div>""",
    """    <div class="mcq-row" data-answer="B">
      <div class="mcq-q"><strong>1.</strong> What is the main difference between the two appointment types?</div>
      <div class="mcq-opts">
        <button data-v="A">A. The 30-minute slots are free; drop-ins cost a small fee.</button>
        <button data-v="B">B. The 30-minute slots are for drafts; drop-ins are for earlier-stage questions without a draft.</button>
        <button data-v="C">C. The 30-minute slots are held in person; drop-ins happen online.</button>
        <button data-v="D">D. Only graduate students may use the 30-minute slots.</button>
      </div>
      <div class="mcq-note">The email contrasts "current-draft feedback" (30-min) with "brainstorming, thesis framing and citation questions — no draft required" (drop-in).</div>
    </div>
    <div class="mcq-row" data-answer="A">
      <div class="mcq-q"><strong>2.</strong> How can a student get a 30-minute appointment?</div>
      <div class="mcq-opts">
        <button data-v="A">A. Book through the online portal at least 24 hours in advance.</button>
        <button data-v="B">B. Arrive at the Writing Centre any weekday from 14:00.</button>
        <button data-v="C">C. Email Jamie Whitfield directly with a draft attached.</button>
        <button data-v="D">D. Join the Children's Reading Room list first.</button>
      </div>
      <div class="mcq-note">"Book through the online portal at least 24 hours ahead for 30-min slots."</div>
    </div>
    <div class="mcq-row" data-answer="C">
      <div class="mcq-q"><strong>3.</strong> What happens if a student misses two booked appointments without cancelling?</div>
      <div class="mcq-opts">
        <button data-v="A">A. They have to pay a small missed-session fee.</button>
        <button data-v="B">B. They are limited to drop-in sessions for the rest of the term.</button>
        <button data-v="C">C. The system blocks their bookings for two weeks.</button>
        <button data-v="D">D. Their course instructor is notified automatically.</button>
      </div>
      <div class="mcq-note">"The system automatically blocks further bookings for two weeks."</div>
    </div>""",
)

# s04 P2 (prof email → lab autoclave notice)
t = t.replace(
    """    <div class="task-tag">P2 · Email from a professor</div>
    <div class="notice">
      <div class="notice-h">Email · From Prof. Daniels · To: Business 201 students</div>
      <div class="notice-sub">Subject: Meeting on Friday — rescheduled</div>
      <p>Hi everyone,</p>
      <p>I have to attend a department review on Friday morning, so our 10:00 group meeting will not go ahead as planned. I'd like to move it to the <strong>same time on Monday</strong>, in Room B-214 (one floor below our usual room). We'll keep the agenda identical: the two case studies and your three-slide pitch.</p>
      <p>If you can't make Monday, please send me a short message by Thursday evening so I know how many to expect. I will not be able to meet individually this week.</p>
      <p>Best, L. Daniels</p>
    </div>""",
    """    <div class="task-tag">P2 · Biology lab autoclave notice</div>
    <div class="notice">
      <div class="notice-h">Life Sciences Lab · Autoclave Protocol (Revised)</div>
      <div class="notice-sub">Posted next to the autoclave on Floor 2 · effective Monday 7 November</div>
      <p>The autoclave now runs on a <strong>timed-slot sign-up</strong>. Each cycle is 90 minutes; book no more than two consecutive slots per day per user. Load only in <strong>autoclave-grade bags</strong> with the yellow indicator tape visible from the door — bags without visible tape will be removed and returned unprocessed.</p>
      <p>After the cycle finishes, remove your load within 30 minutes to free the chamber for the next user. Media bottles must be loosened by a quarter turn before the cycle; <strong>fully sealed containers are forbidden</strong> and have caused two incidents this term.</p>
    </div>""",
)

t = t.replace(
    """    <div class="mcq-row" data-answer="A">
      <div class="mcq-q"><strong>4.</strong> What is the main purpose of the email?</div>
      <div class="mcq-opts">
        <button data-v="A">A. To move the group meeting from Friday to Monday</button>
        <button data-v="B">B. To cancel the whole course for the week</button>
        <button data-v="C">C. To ask students to choose new case studies</button>
        <button data-v="D">D. To invite students to a department review</button>
      </div>
      <div class="mcq-note">Opening and middle paragraphs make the reschedule explicit; the agenda stays the same.</div>
    </div>
    <div class="mcq-row" data-answer="C">
      <div class="mcq-q"><strong>5.</strong> Where will the Monday meeting take place?</div>
      <div class="mcq-opts">
        <button data-v="A">A. In the department review room</button>
        <button data-v="B">B. In the usual room, one hour later</button>
        <button data-v="C">C. In Room B-214, one floor below the usual room</button>
        <button data-v="D">D. In the professor's office</button>
      </div>
      <div class="mcq-note">"Room B-214 (one floor below our usual room)".</div>
    </div>
    <div class="mcq-row" data-answer="B">
      <div class="mcq-q"><strong>6.</strong> What should a student do if Monday does not work for them?</div>
      <div class="mcq-opts">
        <button data-v="A">A. Come to Friday anyway and wait outside</button>
        <button data-v="B">B. Send the professor a short message by Thursday evening</button>
        <button data-v="C">C. Book an individual meeting during the week</button>
        <button data-v="D">D. Skip the pitch and submit it by email</button>
      </div>
      <div class="mcq-note">Last paragraph specifies the Thursday-evening heads-up; individual meetings are not available.</div>
    </div>""",
    """    <div class="mcq-row" data-answer="B">
      <div class="mcq-q"><strong>4.</strong> Why is the yellow indicator tape required?</div>
      <div class="mcq-opts">
        <button data-v="A">A. It makes the bags easier to carry.</button>
        <button data-v="B">B. It allows staff to confirm the right bag type was used without opening it.</button>
        <button data-v="C">C. It marks the bag as biohazard waste.</button>
        <button data-v="D">D. It shows which cycle temperature was used.</button>
      </div>
      <div class="mcq-note">"Bags without visible tape will be removed" — the tape is the visible confirmation of autoclave-grade material.</div>
    </div>
    <div class="mcq-row" data-answer="A">
      <div class="mcq-q"><strong>5.</strong> What is the time limit for removing a load after the cycle finishes?</div>
      <div class="mcq-opts">
        <button data-v="A">A. 30 minutes</button>
        <button data-v="B">B. 90 minutes</button>
        <button data-v="C">C. 2 hours</button>
        <button data-v="D">D. By the end of the day</button>
      </div>
      <div class="mcq-note">"Remove your load within 30 minutes to free the chamber for the next user."</div>
    </div>
    <div class="mcq-row" data-answer="D">
      <div class="mcq-q"><strong>6.</strong> Why must media bottles be loosened before the cycle?</div>
      <div class="mcq-opts">
        <button data-v="A">A. To let the yellow tape adhere properly.</button>
        <button data-v="B">B. To speed up the 90-minute cycle.</button>
        <button data-v="C">C. To match the sign-up portal format.</button>
        <button data-v="D">D. Because sealed containers have caused incidents this term.</button>
      </div>
      <div class="mcq-note">"Fully sealed containers are forbidden and have caused two incidents this term."</div>
    </div>""",
)

# s04 P3 (cafe → bookstore buyback)
t = t.replace(
    """    <div class="task-tag">P3 · Café menu / discount sign</div>
    <div class="notice">
      <div class="notice-h">Blue Harbour Café — Student Discount</div>
      <div class="notice-sub">Weekdays only, 14:00 – 17:00</div>
      <p>Show a valid student ID at the counter and get <strong>20% off</strong> any hot drink and one baked item. The discount cannot be combined with other promotions, including the "buy five, get one free" loyalty stamp card.</p>
      <p>Takeaway cups are available, but reusable cups brought from home get an extra 10 cents off per drink.</p>
    </div>""",
    """    <div class="task-tag">P3 · Campus bookstore buyback sign</div>
    <div class="notice">
      <div class="notice-h">University Bookstore — End-of-Term Buyback</div>
      <div class="notice-sub">11 – 15 December, 09:00 – 17:00 · Lower Level</div>
      <p>We buy back used textbooks in <strong>good condition</strong> — no missing pages, no water damage, limited highlighting. You will get up to <strong>50% of the sticker price</strong> for titles reordered for next term; titles not on the reorder list earn a flat <strong>$5 per book</strong> as general-pool stock.</p>
      <p>Bring your student ID. Access codes and digital-only bundles are <strong>not</strong> eligible. Payment is by store credit or direct deposit — cash is not available at the counter.</p>
    </div>""",
)

t = t.replace(
    """    <div class="mcq-row" data-answer="D">
      <div class="mcq-q"><strong>7.</strong> A student orders a latte and a croissant on a Tuesday at 15:00. What applies?</div>
      <div class="mcq-opts">
        <button data-v="A">A. 20% off the latte only, nothing off the croissant</button>
        <button data-v="B">B. Full price — the discount only works on weekends</button>
        <button data-v="C">C. 20% off plus a loyalty stamp automatically added</button>
        <button data-v="D">D. 20% off the hot drink and the baked item</button>
      </div>
      <div class="mcq-note">Weekday afternoon fits the window; the discount covers both items. Loyalty stamps cannot be combined.</div>
    </div>
    <div class="mcq-row" data-answer="A">
      <div class="mcq-q"><strong>8.</strong> How can a customer get an additional 10 cents off a drink?</div>
      <div class="mcq-opts">
        <button data-v="A">A. By bringing a reusable cup from home</button>
        <button data-v="B">B. By using a loyalty stamp card at the same time</button>
        <button data-v="C">C. By ordering before 14:00</button>
        <button data-v="D">D. By asking for a takeaway cup instead of a mug</button>
      </div>
      <div class="mcq-note">Last line of the sign spells out the reusable-cup bonus.</div>
    </div>""",
    """    <div class="mcq-row" data-answer="C">
      <div class="mcq-q"><strong>7.</strong> A student brings a textbook with light highlighting that is on next term's reorder list. What price does she get?</div>
      <div class="mcq-opts">
        <button data-v="A">A. The full sticker price in cash.</button>
        <button data-v="B">B. A flat $5 per book because of the highlighting.</button>
        <button data-v="C">C. Up to 50% of the sticker price as store credit or direct deposit.</button>
        <button data-v="D">D. Nothing — any highlighting disqualifies the book.</button>
      </div>
      <div class="mcq-note">Light highlighting is within "limited highlighting", and the book is on the reorder list → up to 50% sticker. Payment is credit or direct deposit.</div>
    </div>
    <div class="mcq-row" data-answer="D">
      <div class="mcq-q"><strong>8.</strong> Which of the following will the bookstore <em>NOT</em> buy back?</div>
      <div class="mcq-opts">
        <button data-v="A">A. A used textbook with no highlighting</button>
        <button data-v="B">B. A textbook on the reorder list with a cracked spine</button>
        <button data-v="C">C. A used paperback not on the reorder list</button>
        <button data-v="D">D. A one-time digital access code</button>
      </div>
      <div class="mcq-note">"Access codes and digital-only bundles are not eligible."</div>
    </div>""",
)

# section img alt
t = t.replace(
    'alt="Library notice board — Daily Life reading"',
    'alt="Campus bulletin board — Daily Life reading"',
)
t = t.replace(
    """  <p class="section-sub">Everyday reading at B2 level — a notice, a short email, and a café sign. Read each one, then answer the questions below it. One best answer per question.</p>""",
    """  <p class="section-sub">Everyday campus reading — a writing-centre email, a biology-lab autoclave notice, and a bookstore buyback sign. Read each one, then answer the questions. One best answer per question.</p>""",
)

# ============================================================
# 5. S05 · READING ACADEMIC PASSAGE (psychology)
# ============================================================
old_s05_passage = """    <div class="passage">
      <h4>Why we forget what we read</h4>
      <p>Most people have had the experience of finishing a long article or a chapter of a book and realising, half an hour later, that they can barely remember what it said. This is not a sign of a poor memory. In fact, forgetting most of what we read is normal, and researchers now describe it as a feature of how the brain stores information rather than a failure of attention.</p>
      <p>One important factor is what psychologists call <em>passive reading</em>. When we read smoothly, our eyes keep moving even if we are not actively building meaning. The text feels familiar as it passes, so we assume we understand it. However, familiarity is not the same as memory. Studies suggest that readers who regularly stop and summarise a section in their own words recall roughly twice as much a week later, compared with readers who simply continue to the next paragraph.</p>
      <p>A second factor is the lack of a clear reason to remember. The brain is efficient and tends to drop information it does not expect to use again. In classroom experiments, students who were told before a text that they would later teach the material to a classmate retained far more detail than students who were simply asked to read for comprehension. The difference was significant even when neither group ended up teaching anyone — the expectation alone changed how the information was stored.</p>
      <p>None of this means that reading is wasted. Even forgotten reading shapes background knowledge, vocabulary and the sense of how arguments are built. But if the goal is to remember specific points, two small habits do most of the work: pausing to put the main idea in your own words, and reading with a reason — a question you want answered, a decision you want to make, or someone you plan to tell about it.</p>
    </div>"""
new_s05_passage = """    <div class="passage">
      <h4>The misinformation effect in eyewitness memory</h4>
      <p>In a classic series of experiments carried out at the University of Washington in the 1970s, Elizabeth Loftus showed participants a short film of a traffic accident and then asked them questions about what they had seen. One group was asked, "How fast were the cars going when they <em>hit</em> each other?" A second group was asked the same question with the word <em>smashed</em> in place of <em>hit</em>. A week later, the two groups returned and were asked, among other things, whether they had seen broken glass at the accident scene. There had been no broken glass in the film, yet participants who had earlier heard the word <em>smashed</em> were more than twice as likely to "remember" seeing some.</p>
      <p>This finding, now known as the <em>misinformation effect</em>, challenged a popular view of memory as a kind of recording that could be rewound and replayed. Instead, Loftus and others argued, each time a memory is recalled it is partially reconstructed, and new information encountered after the event — through questioning, news reports, or conversations with other witnesses — can be absorbed into the original memory without the person noticing.</p>
      <p>The implications for the legal system have been significant. Several jurisdictions have revised police interview protocols so that officers avoid leading language and separate witnesses before they can discuss what they saw. Jury instructions have also changed: in some courts, jurors are now explicitly told that confident testimony is not the same as accurate testimony, and that details recalled with great certainty may still have been introduced after the event.</p>
      <p>Yet the misinformation effect should not be read as a verdict that memory is fundamentally unreliable. Most recollections of ordinary events are broadly accurate, and witnesses who are interviewed quickly, with open-ended questions, remain a useful source. The warning is narrower: memory is plastic enough that the <em>way</em> we ask about the past can quietly change what the past looks like.</p>
    </div>"""
t = t.replace(old_s05_passage, new_s05_passage)

t = t.replace(
    'alt="Reader with fragments of letters dissolving upwards — Why we forget what we read"',
    'alt="Fading film reel — the misinformation effect in eyewitness memory"',
)

old_s05_mcq = """    <div class="mcq-row" data-answer="B">
      <div class="mcq-q"><strong>1.</strong> What is the main idea of the passage?</div>
      <div class="mcq-opts">
        <button data-v="A">A. Most adults have poor memory and should read less demanding texts.</button>
        <button data-v="B">B. Forgetting much of what we read is normal, but two small habits sharply improve recall.</button>
        <button data-v="C">C. Teaching other people is the only reliable way to remember a book.</button>
        <button data-v="D">D. Reading is largely wasted unless it is linked to a formal exam.</button>
      </div>
      <div class="mcq-note">The whole passage normalises forgetting and then recommends two concrete habits in the final paragraph.</div>
    </div>
    <div class="mcq-row" data-answer="C">
      <div class="mcq-q"><strong>2.</strong> According to paragraph 2, why does passive reading often fail to produce memory?</div>
      <div class="mcq-opts">
        <button data-v="A">A. Readers skip difficult words and move too fast through the text.</button>
        <button data-v="B">B. The eyes stop moving before the paragraph ends.</button>
        <button data-v="C">C. Readers mistake the familiar feel of the text for actual understanding.</button>
        <button data-v="D">D. The brain only stores the first sentence of each paragraph.</button>
      </div>
      <div class="mcq-note">"Familiarity is not the same as memory" — the whole point of the paragraph.</div>
    </div>
    <div class="mcq-row" data-answer="A">
      <div class="mcq-q"><strong>3.</strong> What did the classroom experiment show about expecting to teach the material?</div>
      <div class="mcq-opts">
        <button data-v="A">A. The expectation alone improved how much the students remembered.</button>
        <button data-v="B">B. Only students who actually taught someone later remembered the text.</button>
        <button data-v="C">C. The expectation made students read more slowly and skip the end.</button>
        <button data-v="D">D. There was no difference between the two groups.</button>
      </div>
      <div class="mcq-note">The paragraph specifies that the difference held "even when neither group ended up teaching anyone".</div>
    </div>
    <div class="mcq-row" data-answer="D">
      <div class="mcq-q"><strong>4.</strong> In paragraph 3, the word <em>retained</em> is closest in meaning to:</div>
      <div class="mcq-opts">
        <button data-v="A">A. forgot</button>
        <button data-v="B">B. explained</button>
        <button data-v="C">C. questioned</button>
        <button data-v="D">D. kept in memory</button>
      </div>
      <div class="mcq-note">"Retained far more detail" — kept, held onto. The other options are the opposite or unrelated.</div>
    </div>
    <div class="mcq-row" data-answer="B">
      <div class="mcq-q"><strong>5.</strong> Why does the author include the sentence "None of this means that reading is wasted"?</div>
      <div class="mcq-opts">
        <button data-v="A">A. To contradict the earlier studies and dismiss their results.</button>
        <button data-v="B">B. To soften the previous point and show that forgotten reading still has value.</button>
        <button data-v="C">C. To introduce a new topic unrelated to memory.</button>
        <button data-v="D">D. To warn readers that most books are a bad use of time.</button>
      </div>
      <div class="mcq-note">The function is a concession before the two-habits conclusion — a classic B2+ discourse move.</div>
    </div>
    <div class="mcq-row" data-answer="C">
      <div class="mcq-q"><strong>6.</strong> What can be inferred about a reader who stops after each section to summarise it aloud?</div>
      <div class="mcq-opts">
        <button data-v="A">A. They will read fewer books in total each year.</button>
        <button data-v="B">B. They will remember less than someone who reads straight through.</button>
        <button data-v="C">C. They are more likely to recall the content a week later than a smooth reader.</button>
        <button data-v="D">D. They will only benefit from the habit when preparing to teach a class.</button>
      </div>
      <div class="mcq-note">Paragraph 2: readers who summarise in their own words "recall roughly twice as much a week later". The inference follows directly.</div>
    </div>"""
new_s05_mcq = """    <div class="mcq-row" data-answer="C">
      <div class="mcq-q"><strong>1.</strong> What is the main idea of the passage?</div>
      <div class="mcq-opts">
        <button data-v="A">A. Memory is so unreliable that eyewitness testimony should be banned.</button>
        <button data-v="B">B. The word <em>smashed</em> always produces false memories of broken glass.</button>
        <button data-v="C">C. Memories are partly reconstructed and can be reshaped by later information — with legal consequences.</button>
        <button data-v="D">D. The 1970s Loftus experiments have been discredited by later research.</button>
      </div>
      <div class="mcq-note">The three middle paragraphs build this arc; the final paragraph bounds the claim.</div>
    </div>
    <div class="mcq-row" data-answer="B">
      <div class="mcq-q"><strong>2.</strong> Why does the author contrast the words <em>hit</em> and <em>smashed</em> in paragraph 1?</div>
      <div class="mcq-opts">
        <button data-v="A">A. To show that English synonyms are often confused with each other.</button>
        <button data-v="B">B. To demonstrate how the wording of a question changed what witnesses later "remembered".</button>
        <button data-v="C">C. To argue that the second group watched a different film.</button>
        <button data-v="D">D. To prove that there really was broken glass at the scene.</button>
      </div>
      <div class="mcq-note">Paragraph 1 ends with the two-fold increase in false broken-glass memory tied directly to the loaded word.</div>
    </div>
    <div class="mcq-row" data-answer="D">
      <div class="mcq-q"><strong>3.</strong> According to the passage, what does the misinformation effect challenge?</div>
      <div class="mcq-opts">
        <button data-v="A">A. The idea that witnesses sometimes lie under pressure.</button>
        <button data-v="B">B. The idea that memory improves with repeated questioning.</button>
        <button data-v="C">C. The idea that broken glass is often present at accident scenes.</button>
        <button data-v="D">D. The idea that memory works like a recording that can be rewound and replayed.</button>
      </div>
      <div class="mcq-note">Paragraph 2 names and rejects exactly this "recording" view of memory.</div>
    </div>
    <div class="mcq-row" data-answer="A">
      <div class="mcq-q"><strong>4.</strong> In paragraph 2, the word <em>absorbed</em> is closest in meaning to:</div>
      <div class="mcq-opts">
        <button data-v="A">A. taken in</button>
        <button data-v="B">B. rejected</button>
        <button data-v="C">C. exaggerated</button>
        <button data-v="D">D. repeated out loud</button>
      </div>
      <div class="mcq-note">New information is "absorbed into the original memory" = taken in, incorporated.</div>
    </div>
    <div class="mcq-row" data-answer="C">
      <div class="mcq-q"><strong>5.</strong> Why does the author mention the changes to jury instructions in paragraph 3?</div>
      <div class="mcq-opts">
        <button data-v="A">A. To criticise jurors for trusting confident witnesses.</button>
        <button data-v="B">B. To show that the legal system is slow to change.</button>
        <button data-v="C">C. To illustrate a concrete real-world response to the research findings.</button>
        <button data-v="D">D. To introduce a new topic about jury deliberation.</button>
      </div>
      <div class="mcq-note">The paragraph is the passage's "so-what" — a practical consequence of Loftus's work.</div>
    </div>
    <div class="mcq-row" data-answer="B">
      <div class="mcq-q"><strong>6.</strong> What can be inferred about a witness who is interviewed quickly and with open-ended questions?</div>
      <div class="mcq-opts">
        <button data-v="A">A. Their testimony is guaranteed to be perfectly accurate.</button>
        <button data-v="B">B. Their testimony is more useful than one shaped by later, leading questioning.</button>
        <button data-v="C">C. They will remember more details than people with written notes.</button>
        <button data-v="D">D. They should never be used in court cases.</button>
      </div>
      <div class="mcq-note">The final paragraph explicitly says such witnesses "remain a useful source" — and the whole passage implies the alternative is much worse.</div>
    </div>"""
t = t.replace(old_s05_mcq, new_s05_mcq)

t = t.replace(
    """  <p class="section-sub">Short academic text at B2+ level. Read once at normal pace, then answer six questions: main idea, two detail, vocab-in-context, function, inference.</p>""",
    """  <p class="section-sub">Short academic text at C1 level — psychology and the law. Read once at normal pace, then answer six questions: main idea, two detail, vocab-in-context, function, inference.</p>""",
)

# ============================================================
# 6. S11 · WRITING EMAIL · student emails advisor to add a class late
# ============================================================
t = t.replace(
    """    <h3>Scenario</h3>
    <p>You are a university student in Professor Chen's course. An unexpected family event (travel for your grandmother's hospital stay) means you cannot submit your essay on the current deadline. Write an email asking Professor Chen for a <strong>48-hour extension</strong>. Be polite, give the reason briefly, propose the new deadline, and offer to send any evidence if needed.</p>""",
    """    <h3>Scenario</h3>
    <p>You are a university student and course registration closed yesterday. You would still like to <strong>add PSYC 210 · Intro to Cognitive Psychology</strong> because a required class was cancelled and you now have a gap in your schedule. Write an email to your academic advisor, Dr Harper, asking whether a late add is possible. Be polite, explain the situation briefly, state that you have already spoken to the PSYC 210 instructor who is open to it, and ask what the next step is.</p>""",
)

t = t.replace(
    """    <div class="write">
      <textarea placeholder="Dear Professor Chen, ..."></textarea>
      <div class="write-meta"><span>Target length: 80–150 words</span><span class="wc">Words: <strong>0</strong></span></div>
      <button class="sample-toggle">Show C1 model</button>
      <div class="sample-reveal">Dear Professor Chen,

I hope this email finds you well. I am writing to ask whether it would be possible to have a 48-hour extension on the Methods essay, which is currently due this Friday.

Over the weekend my grandmother was admitted to hospital, and I have had to travel to be with my family and help with practical arrangements. I will have reliable access to my notes again from Wednesday evening, so I am confident I could submit a complete draft by Sunday at 23:59.

I apologise for the short notice. I am happy to send any supporting documents, including a letter from the hospital, if that would be helpful.

Thank you very much for considering this request.

Kind regards,
Andrew Kruglov</div>
    </div>""",
    """    <div class="write">
      <textarea placeholder="Dear Dr Harper, ..."></textarea>
      <div class="write-meta"><span>Target length: 80–150 words</span><span class="wc">Words: <strong>0</strong></span></div>
      <button class="sample-toggle">Show C1 model</button>
      <div class="sample-reveal">Dear Dr Harper,

I hope you are well. I am writing to ask whether a late add is still possible this term. My registered class in Linguistics was cancelled on Monday, which has left a gap in my schedule, and I would like to replace it with PSYC 210 · Intro to Cognitive Psychology.

I have already spoken to the instructor, Dr Mallory, who is open to admitting me provided the registrar's office approves the late entry. I am happy to catch up on the first two weeks of readings independently.

Could you let me know what the next step is on your end, and whether I need to submit a specific form? I appreciate your help with this.

Kind regards,
Varvara Sules</div>
    </div>""",
)

# ============================================================
# 7. S12 · WRITING ACADEMIC DISCUSSION · laptops in lecture halls
# ============================================================
t = t.replace(
    """    <div class="post">
      <div class="post-h">Professor's prompt</div>
      <p>Some universities are considering a <strong>mandatory first-year "wellbeing" course</strong> covering sleep, nutrition, mental health, and stress management. Do you think such a course should be required of all students? Why or why not?</p>
    </div>

    <div class="post">
      <div class="post-h">Sarah · against</div>
      <p>I don't see the point. Most students know the basics already — eat better, sleep more, don't panic. The real reason people are stressed is the workload itself. Adding another required course just means another box to tick and even less time to actually sleep. I'd rather see smaller class sizes.</p>
    </div>

    <div class="post">
      <div class="post-h">Mark · for</div>
      <p>I'm in favour. A lot of us arrived at university with almost no life skills — I didn't know how to cook or how to notice when I was anxious. One shared course would at least give everyone the same baseline, and it would signal that the university actually cares about student health.</p>
    </div>""",
    """    <div class="post">
      <div class="post-h">Professor's prompt</div>
      <p>Some universities are now considering a <strong>ban on laptops and tablets in lecture halls</strong>, arguing that typing distracts both the user and nearby students and encourages passive note-copying. Others say that handwriting is too slow for many fields and that a ban penalises students with disabilities. <strong>Should universities ban laptops in lectures?</strong> Give your position.</p>
    </div>

    <div class="post">
      <div class="post-h">Dan · for a ban</div>
      <p>Yes — the evidence is pretty clear that typed notes become verbatim transcripts and that handwritten notes force you to compress ideas. More importantly, when half the row is on laptops you can see everyone drifting onto chat, and the drift spreads. A chemistry lecture isn't the place to be answering messages.</p>
    </div>

    <div class="post">
      <div class="post-h">Lin · against a ban</div>
      <p>Blanket bans are lazy. I have carpal issues and simply cannot handwrite for ninety minutes; I'd be forced to drop courses. The real problem is how lectures are taught — if they're boring enough that laptops win, you need better lectures, not new rules. Allow laptops in dedicated rows if distraction is the worry.</p>
    </div>""",
)

t = t.replace(
    """    <div class="write">
      <textarea placeholder="I agree with Mark that ..."></textarea>
      <div class="write-meta"><span>Target length: 100–130 words</span><span class="wc">Words: <strong>0</strong></span></div>
      <button class="sample-toggle">Show C1 model</button>
      <div class="sample-reveal">I actually agree with Mark more than with Sarah. Yes, the workload is a real problem, but you cannot fix it by hoping students already know how to look after themselves — many of us simply don't.

In my first term I lived on instant noodles and five hours of sleep, and I didn't realise how much that was affecting my grades until a friend pointed it out. One shared course wouldn't magically solve stress, but it would give everyone a basic language for noticing early warning signs — and that is harder to pick up on your own than Sarah's reply suggests.

I would make the course short — maybe six sessions — so it adds support without becoming yet another assessed burden.</div>
    </div>""",
    """    <div class="write">
      <textarea placeholder="I lean towards Lin's position, though ..."></textarea>
      <div class="write-meta"><span>Target length: 100–130 words</span><span class="wc">Words: <strong>0</strong></span></div>
      <button class="sample-toggle">Show C1 model</button>
      <div class="sample-reveal">I lean towards Lin more than Dan, though with a sharper edge. A blanket ban treats a teaching problem as a student problem — if a ninety-minute lecture only works when the room has been forcibly disarmed, it is probably the wrong format for the material in the first place.

That said, Dan is right that distraction does spread; I've watched a whole row scroll together on bad days. The reasonable middle is a <em>devices-off zone</em> for the first and last rows combined with recorded lectures, so that students who need laptops can still participate, and students who want to hand-write have a quieter area. That gives us the benefit Dan wants without Lin's disability concern.</div>
    </div>""",
)

# ============================================================
# 8. S14 · SPEAKING INTERVIEW × 4
# ============================================================
t = t.replace(
    """      <div class="lnr-text"><strong>Q1.</strong> Describe your typical morning. What do you usually do between waking up and leaving the house?</div>""",
    """      <div class="lnr-text"><strong>Q1.</strong> Describe a skill or subject you have taught yourself (without a teacher). What helped you most, and what was hardest?</div>""",
)
t = t.replace(
    """      <div class="lnr-text"><strong>Q2.</strong> Do you prefer spending your free time alone or with other people? Why?</div>""",
    """      <div class="lnr-text"><strong>Q2.</strong> Some people believe success comes mostly from hard work; others believe it comes mostly from luck and circumstances. Which position is closer to your own, and why?</div>""",
)
t = t.replace(
    """      <div class="lnr-text"><strong>Q3.</strong> Describe a city you have visited that stayed in your memory. What made it memorable?</div>""",
    """      <div class="lnr-text"><strong>Q3.</strong> Should universities keep required general-education courses (literature, science, ethics for all majors), or let students choose freely from the start? Explain.</div>""",
)
t = t.replace(
    """      <div class="lnr-text"><strong>Q4.</strong> If you could change one thing about the way you learn English, what would it be and why?</div>""",
    """      <div class="lnr-text"><strong>Q4.</strong> Describe a recent change in your routine — work, study, or personal — that turned out better than you expected. What made the difference?</div>""",
)

# ============================================================
# 9. Finally: rename any remaining "Andrew" mentions (text + alt attrs)
# ============================================================
t = t.replace("Andrew Kruglov", "Varvara Sules")
t = t.replace("Andrew's", "Varya's")
t = re.sub(r"\bAndrew\b", "Varya", t)

SRC.write_text(t, encoding="utf-8")
print(f"rebuild done · {SRC.name} · {len(t)} chars")
