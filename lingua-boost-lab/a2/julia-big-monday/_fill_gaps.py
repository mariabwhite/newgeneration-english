"""Fill the remaining grammar + vocab gaps identified in the audit.

VOCAB TAB — adds 3 new sections (school furniture, breakfast items, Bodrum holiday).
GRAMMAR TAB — adds 11 new sections covering ALL the themes Julia has studied but not yet drilled in this recap:
  - 4 Question types + short answers
  - Frequency adverbs
  - Numbers 1-20 cardinal
  - Present Perfect intro
  - Past Cont vs Past Simple (while/when)
  - There is / There are
  - Articles a/an/the
  - Might / Could
  - Conditional If...then
  - Object pronouns me/him/her
  - How much vs How many
"""
import pathlib
HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"
text = HTML.read_text(encoding="utf-8")

VOCAB_FILL = """
<!-- ===== VOCAB RECALL · School furniture (recap-01) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">V+</div>
    <h2>Vocab Recall · <em>School furniture &amp; stationery</em></h2>
    <span class="tag">school · 8 items</span>
  </div>
  <div class="section-sub">Items in Julia's classroom from Recap 01 · Back to School.</div>
  <div class="card">
    <span class="ex-sticker">📚</span>
    <h3><span class="ex-num">V+.9</span> Pick the right school item</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="ruler"><div class="mc-q"><span class="num">1</span><span>I measure a line with a <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="ruler">ruler</button><button class="mc-opt" data-v="rubber">rubber</button><button class="mc-opt" data-v="board">board</button></div></div>
      <div class="mc-item" data-answer="rubber"><div class="mc-q"><span class="num">2</span><span>I made a mistake — pass me the <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="ruler">ruler</button><button class="mc-opt" data-v="rubber">rubber</button><button class="mc-opt" data-v="pencil">pencil</button></div></div>
      <div class="mc-item" data-answer="notebook"><div class="mc-q"><span class="num">3</span><span>I write my English homework in my <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="desk">desk</button><button class="mc-opt" data-v="notebook">notebook</button><button class="mc-opt" data-v="chair">chair</button></div></div>
      <div class="mc-item" data-answer="desk"><div class="mc-q"><span class="num">4</span><span>Emma and I share a <span class="gap-mini">?</span> at school.</span></div><div class="mc-opts"><button class="mc-opt" data-v="desk">desk</button><button class="mc-opt" data-v="chair">chair</button><button class="mc-opt" data-v="board">board</button></div></div>
      <div class="mc-item" data-answer="board"><div class="mc-q"><span class="num">5</span><span>Mrs. Green writes on the <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="board">board</button><button class="mc-opt" data-v="notebook">notebook</button><button class="mc-opt" data-v="schoolbag">schoolbag</button></div></div>
      <div class="mc-item" data-answer="schoolbag"><div class="mc-q"><span class="num">6</span><span>I put all my books in my <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="desk">desk</button><button class="mc-opt" data-v="schoolbag">schoolbag</button><button class="mc-opt" data-v="chair">chair</button></div></div>
      <div class="mc-item" data-answer="pencil"><div class="mc-q"><span class="num">7</span><span>I draw with a <span class="gap-mini">?</span> and colour with pens.</span></div><div class="mc-opts"><button class="mc-opt" data-v="pencil">pencil</button><button class="mc-opt" data-v="rubber">rubber</button><button class="mc-opt" data-v="ruler">ruler</button></div></div>
      <div class="mc-item" data-answer="chair"><div class="mc-q"><span class="num">8</span><span>Sit on your <span class="gap-mini">?</span>, John! The lesson is starting.</span></div><div class="mc-opts"><button class="mc-opt" data-v="chair">chair</button><button class="mc-opt" data-v="board">board</button><button class="mc-opt" data-v="desk">desk</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-school-items">Check</button><span class="score-pill" data-score-for="sec-school-items">— / 8</span></div>
  </div>
</section>

<!-- ===== VOCAB RECALL · Breakfast items (recap-01) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">V+</div>
    <h2>Vocab Recall · <em>Breakfast table — plate, glass, fork…</em></h2>
    <span class="tag">kitchen · 8 items</span>
  </div>
  <div class="section-sub">Things on the breakfast table from Recap 01.</div>
  <div class="card">
    <span class="ex-sticker">🍳</span>
    <h3><span class="ex-num">V+.10</span> Pick the right item</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="fork"><div class="mc-q"><span class="num">1</span><span>I eat pancakes with a <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="spoon">spoon</button><button class="mc-opt" data-v="fork">fork</button><button class="mc-opt" data-v="knife">knife</button></div></div>
      <div class="mc-item" data-answer="spoon"><div class="mc-q"><span class="num">2</span><span>I eat cereal with a <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="fork">fork</button><button class="mc-opt" data-v="spoon">spoon</button><button class="mc-opt" data-v="plate">plate</button></div></div>
      <div class="mc-item" data-answer="knife"><div class="mc-q"><span class="num">3</span><span>Mum uses a <span class="gap-mini">?</span> to cut the bread.</span></div><div class="mc-opts"><button class="mc-opt" data-v="knife">knife</button><button class="mc-opt" data-v="fork">fork</button><button class="mc-opt" data-v="jar">jar</button></div></div>
      <div class="mc-item" data-answer="plate"><div class="mc-q"><span class="num">4</span><span>Put your pancakes on a <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="plate">plate</button><button class="mc-opt" data-v="glass">glass</button><button class="mc-opt" data-v="cup">cup</button></div></div>
      <div class="mc-item" data-answer="glass"><div class="mc-q"><span class="num">5</span><span>I drink juice from a <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="cup">cup</button><button class="mc-opt" data-v="glass">glass</button><button class="mc-opt" data-v="plate">plate</button></div></div>
      <div class="mc-item" data-answer="jam"><div class="mc-q"><span class="num">6</span><span>Grandma made strawberry <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="jam">jam</button><button class="mc-opt" data-v="juice">juice</button><button class="mc-opt" data-v="eggs">eggs</button></div></div>
      <div class="mc-item" data-answer="eggs"><div class="mc-q"><span class="num">7</span><span>Mum fries <span class="gap-mini">?</span> for Sunday breakfast.</span></div><div class="mc-opts"><button class="mc-opt" data-v="juice">juice</button><button class="mc-opt" data-v="jam">jam</button><button class="mc-opt" data-v="eggs">eggs</button></div></div>
      <div class="mc-item" data-answer="cereal"><div class="mc-q"><span class="num">8</span><span>Fast breakfast on a school day: <span class="gap-mini">?</span> with milk.</span></div><div class="mc-opts"><button class="mc-opt" data-v="cereal">cereal</button><button class="mc-opt" data-v="eggs">eggs</button><button class="mc-opt" data-v="jam">jam</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-breakfast">Check</button><span class="score-pill" data-score-for="sec-breakfast">— / 8</span></div>
  </div>
</section>

<!-- ===== VOCAB RECALL · Bodrum holiday (bodrum goes-to) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">V+</div>
    <h2>Vocab Recall · <em>Julia goes to Bodrum — holiday vocab</em></h2>
    <span class="tag">travel · 8 words</span>
  </div>
  <div class="section-sub">The summer trip to Turkey — suitcase, airport, pool, beach…</div>
  <div class="card">
    <span class="ex-sticker">🏖</span>
    <h3><span class="ex-num">V+.11</span> Fill in the holiday word</h3>
    <div class="bank" id="bank-holiday">
      <button class="bank-word" data-w="suitcase">suitcase</button>
      <button class="bank-word" data-w="ticket">ticket</button>
      <button class="bank-word" data-w="airport">airport</button>
      <button class="bank-word" data-w="hotel">hotel</button>
      <button class="bank-word" data-w="pool">pool</button>
      <button class="bank-word" data-w="beach">beach</button>
      <button class="bank-word" data-w="sea">sea</button>
      <button class="bank-word" data-w="ice cream">ice cream</button>
    </div>
    <div class="drag-text" data-group="holiday">
      <div class="line-q"><span class="num">1</span><span>Pack your <span class="drop-gap" data-ans="suitcase">?</span> — we're leaving tomorrow!</span></div>
      <div class="line-q"><span class="num">2</span><span>Don't forget your plane <span class="drop-gap" data-ans="ticket">?</span> and passport.</span></div>
      <div class="line-q"><span class="num">3</span><span>We take a taxi to the <span class="drop-gap" data-ans="airport">?</span>.</span></div>
      <div class="line-q"><span class="num">4</span><span>Our <span class="drop-gap" data-ans="hotel">?</span> has 5 floors and a beautiful garden.</span></div>
      <div class="line-q"><span class="num">5</span><span>John swims in the <span class="drop-gap" data-ans="pool">?</span> every morning.</span></div>
      <div class="line-q"><span class="num">6</span><span>We walk along the <span class="drop-gap" data-ans="beach">?</span> at sunset.</span></div>
      <div class="line-q"><span class="num">7</span><span>The <span class="drop-gap" data-ans="sea">?</span> is warm and blue.</span></div>
      <div class="line-q"><span class="num">8</span><span>In the afternoon we always have strawberry <span class="drop-gap" data-ans="ice cream">?</span>.</span></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-holiday">Check</button>
      <button class="btn-reset" data-reset="sec-holiday">clear</button>
      <span class="score-pill" data-score-for="sec-holiday">— / 8</span>
    </div>
  </div>
</section>

"""

GRAMMAR_FILL = """
<!-- ===== GRAMMAR · 4 Question Types + Short Answers ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>4 Question types + short answers</em></h2>
    <span class="tag">questions · base</span>
  </div>
  <div class="section-sub">The four ways to ask a question in English — and how to answer in one short line.</div>
  <div class="card">
    <span class="ex-sticker">❓</span>
    <h3><span class="ex-num">G+.12</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>Type</th><th>Pattern</th><th>Short answer</th></tr>
        <tr><td>Yes/No</td><td><code>Is / Do / Can + subject + V?</code></td><td><em>Yes, I am. / No, she doesn't. / Yes, we can.</em></td></tr>
        <tr><td>Wh-</td><td><code>What / Where / When / Why + aux + subj + V?</code></td><td><em>At 7 o'clock. / In the park.</em></td></tr>
        <tr><td>Who-subject</td><td><code>Who + V?</code> (no aux!)</td><td><em>Julia does. / Mum.</em></td></tr>
        <tr><td>Negative</td><td><code>subject + aux + NOT + V</code></td><td><em>She isn't / doesn't / can't.</em></td></tr>
      </table>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">💬</span>
    <h3><span class="ex-num">G+.13</span> Pick the right question form</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="does-she-live"><div class="mc-q"><span class="num">1</span><span><span class="gap-mini">?</span> in Moscow?</span></div><div class="mc-opts"><button class="mc-opt" data-v="she-lives">She lives</button><button class="mc-opt" data-v="does-she-live">Does she live</button><button class="mc-opt" data-v="is-she-live">Is she live</button></div></div>
      <div class="mc-item" data-answer="where-does-john-sleep"><div class="mc-q"><span class="num">2</span><span><span class="gap-mini">?</span>, under the bed?</span></div><div class="mc-opts"><button class="mc-opt" data-v="where-does-john-sleep">Where does John sleep</button><button class="mc-opt" data-v="where-john-sleeps">Where John sleeps</button><button class="mc-opt" data-v="where-is-john-sleep">Where is John sleep</button></div></div>
      <div class="mc-item" data-answer="who-made"><div class="mc-q"><span class="num">3</span><span><span class="gap-mini">?</span> the pancakes? — Mum.</span></div><div class="mc-opts"><button class="mc-opt" data-v="who-made">Who made</button><button class="mc-opt" data-v="who-did-make">Who did make</button><button class="mc-opt" data-v="who-did-made">Who did made</button></div></div>
      <div class="mc-item" data-answer="she-doesnt-like"><div class="mc-q"><span class="num">4</span><span>Julia <span class="gap-mini">?</span> onions. She never eats them.</span></div><div class="mc-opts"><button class="mc-opt" data-v="not-likes">not likes</button><button class="mc-opt" data-v="doesnt-like">doesn't like</button><button class="mc-opt" data-v="isnt-like">isn't like</button></div></div>
      <div class="mc-item" data-answer="yes-she-does"><div class="mc-q"><span class="num">5</span><span>— Does Mum make pancakes on Sundays? — <span class="gap-mini">?</span></span></div><div class="mc-opts"><button class="mc-opt" data-v="yes-she-is">Yes, she is.</button><button class="mc-opt" data-v="yes-she-does">Yes, she does.</button><button class="mc-opt" data-v="yes-she-makes">Yes, she makes.</button></div></div>
      <div class="mc-item" data-answer="no-he-isnt"><div class="mc-q"><span class="num">6</span><span>— Is Vova listening to the teacher? — <span class="gap-mini">?</span> He's sleeping!</span></div><div class="mc-opts"><button class="mc-opt" data-v="no-he-doesnt">No, he doesn't.</button><button class="mc-opt" data-v="no-he-isnt">No, he isn't.</button><button class="mc-opt" data-v="no-he-not">No, he not.</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-questions">Check</button><span class="score-pill" data-score-for="sec-questions">— / 6</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · Frequency adverbs ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Frequency adverbs — how often?</em></h2>
    <span class="tag">adverbs</span>
  </div>
  <div class="section-sub">always / usually / often / sometimes / rarely / never — they go BEFORE the normal verb and AFTER am/is/are.</div>
  <div class="card">
    <span class="ex-sticker">⏱</span>
    <h3><span class="ex-num">G+.14</span> Mini-theory · frequency ladder</h3>
    <div class="theory">
      <table>
        <tr><th>100%</th><td><code>always</code></td><td><em>I always get up at 7.</em></td></tr>
        <tr><th>~80%</th><td><code>usually</code></td><td><em>Mum usually drives us.</em></td></tr>
        <tr><th>~60%</th><td><code>often</code></td><td><em>We often visit Grandma.</em></td></tr>
        <tr><th>~40%</th><td><code>sometimes</code></td><td><em>Sometimes I walk.</em></td></tr>
        <tr><th>~15%</th><td><code>rarely</code></td><td><em>He rarely eats fish.</em></td></tr>
        <tr><th>0%</th><td><code>never</code></td><td><em>I never drink coffee.</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">BEFORE a normal verb: <code>I <strong>always</strong> walk</code>. AFTER am/is/are: <code>She is <strong>never</strong> late</code>.</div>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">📊</span>
    <h3><span class="ex-num">G+.15</span> Pick the right frequency word</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="always"><div class="mc-q"><span class="num">1</span><span>Barsik <span class="gap-mini">?</span> sleeps on the window sill — every day, no exception.</span></div><div class="mc-opts"><button class="mc-opt" data-v="never">never</button><button class="mc-opt" data-v="always">always</button><button class="mc-opt" data-v="rarely">rarely</button></div></div>
      <div class="mc-item" data-answer="never"><div class="mc-q"><span class="num">2</span><span>Julia <span class="gap-mini">?</span> drinks coffee — she is only 9!</span></div><div class="mc-opts"><button class="mc-opt" data-v="never">never</button><button class="mc-opt" data-v="often">often</button><button class="mc-opt" data-v="always">always</button></div></div>
      <div class="mc-item" data-answer="usually"><div class="mc-q"><span class="num">3</span><span>I <span class="gap-mini">?</span> have cereal, but sometimes pancakes.</span></div><div class="mc-opts"><button class="mc-opt" data-v="never">never</button><button class="mc-opt" data-v="usually">usually</button><button class="mc-opt" data-v="rarely">rarely</button></div></div>
      <div class="mc-item" data-answer="sometimes"><div class="mc-q"><span class="num">4</span><span>We <span class="gap-mini">?</span> go to the city park on Sundays — not every week.</span></div><div class="mc-opts"><button class="mc-opt" data-v="sometimes">sometimes</button><button class="mc-opt" data-v="always">always</button><button class="mc-opt" data-v="never">never</button></div></div>
      <div class="mc-item" data-answer="often"><div class="mc-q"><span class="num">5</span><span>Emma and I <span class="gap-mini">?</span> meet at the Pink Café after school.</span></div><div class="mc-opts"><button class="mc-opt" data-v="rarely">rarely</button><button class="mc-opt" data-v="often">often</button><button class="mc-opt" data-v="never">never</button></div></div>
      <div class="mc-item" data-answer="rarely"><div class="mc-q"><span class="num">6</span><span>John <span class="gap-mini">?</span> finishes his porridge — he hates it.</span></div><div class="mc-opts"><button class="mc-opt" data-v="always">always</button><button class="mc-opt" data-v="rarely">rarely</button><button class="mc-opt" data-v="often">often</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-freq">Check</button><span class="score-pill" data-score-for="sec-freq">— / 6</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · Numbers 1-20 cardinal ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Numbers 1–20 — type them out</em></h2>
    <span class="tag">numbers · spelling</span>
  </div>
  <div class="section-sub">Numbers from your Bodrum lessons.</div>
  <div class="card">
    <span class="ex-sticker">🔢</span>
    <h3><span class="ex-num">G+.16</span> Type the number as a word</h3>
    <div class="input-list">
      <div class="input-row"><span class="num">1</span><div class="prompt">1 → <b>?</b></div><input type="text" data-ans="one"></div>
      <div class="input-row"><span class="num">2</span><div class="prompt">4 → <b>?</b></div><input type="text" data-ans="four"></div>
      <div class="input-row"><span class="num">3</span><div class="prompt">7 → <b>?</b></div><input type="text" data-ans="seven"></div>
      <div class="input-row"><span class="num">4</span><div class="prompt">10 → <b>?</b></div><input type="text" data-ans="ten"></div>
      <div class="input-row"><span class="num">5</span><div class="prompt">11 → <b>?</b></div><input type="text" data-ans="eleven"></div>
      <div class="input-row"><span class="num">6</span><div class="prompt">12 → <b>?</b></div><input type="text" data-ans="twelve"></div>
      <div class="input-row"><span class="num">7</span><div class="prompt">13 → <b>?</b></div><input type="text" data-ans="thirteen"></div>
      <div class="input-row"><span class="num">8</span><div class="prompt">15 → <b>?</b></div><input type="text" data-ans="fifteen"></div>
      <div class="input-row"><span class="num">9</span><div class="prompt">18 → <b>?</b></div><input type="text" data-ans="eighteen"></div>
      <div class="input-row"><span class="num">10</span><div class="prompt">20 → <b>?</b></div><input type="text" data-ans="twenty"></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-numbers">Check</button><button class="btn-reset" data-reset="sec-numbers">clear</button><span class="score-pill" data-score-for="sec-numbers">— / 10</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · Present Perfect intro ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Present Perfect — Have you ever…?</em></h2>
    <span class="tag new">A2 → B1 bridge</span>
  </div>
  <div class="section-sub">The tense that connects the past with NOW. Used in the Halloween lesson: <em>Have you seen a ghost?</em></div>
  <div class="card">
    <span class="ex-sticker">🧠</span>
    <h3><span class="ex-num">G+.17</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>Subject</th><th>have / has</th><th>V3 (3rd form)</th></tr>
        <tr><td>I / you / we / they</td><td><code>have</code></td><td>been / seen / done</td></tr>
        <tr><td>he / she / it</td><td><code>has</code></td><td>been / seen / done</td></tr>
      </table>
      <div class="rule" style="margin-top:8px">Use for life experience: <code>I have been to London</code>. Negative: <code>haven't / hasn't</code>. Question: <code>Have you ever…? Has she ever…?</code> Short: <em>Yes, I have. / No, I haven't.</em></div>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">🎃</span>
    <h3><span class="ex-num">G+.18</span> Pick have / has / have been / has seen …</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="have"><div class="mc-q"><span class="num">1</span><span>I <span class="gap-mini">?</span> seen a real ghost — in the castle!</span></div><div class="mc-opts"><button class="mc-opt" data-v="have">have</button><button class="mc-opt" data-v="has">has</button><button class="mc-opt" data-v="is">is</button></div></div>
      <div class="mc-item" data-answer="has"><div class="mc-q"><span class="num">2</span><span>Julia <span class="gap-mini">?</span> been to Bodrum two times.</span></div><div class="mc-opts"><button class="mc-opt" data-v="have">have</button><button class="mc-opt" data-v="has">has</button><button class="mc-opt" data-v="is">is</button></div></div>
      <div class="mc-item" data-answer="have-you-ever"><div class="mc-q"><span class="num">3</span><span><span class="gap-mini">?</span> tried Scottish Fold kittens?</span></div><div class="mc-opts"><button class="mc-opt" data-v="have-you-ever">Have you ever</button><button class="mc-opt" data-v="do-you-ever">Do you ever</button><button class="mc-opt" data-v="are-you-ever">Are you ever</button></div></div>
      <div class="mc-item" data-answer="havent"><div class="mc-q"><span class="num">4</span><span>No, I <span class="gap-mini">?</span> been to London — but I will one day!</span></div><div class="mc-opts"><button class="mc-opt" data-v="havent">haven't</button><button class="mc-opt" data-v="hasnt">hasn't</button><button class="mc-opt" data-v="not">not</button></div></div>
      <div class="mc-item" data-answer="hasnt-finished"><div class="mc-q"><span class="num">5</span><span>John <span class="gap-mini">?</span> his homework yet.</span></div><div class="mc-opts"><button class="mc-opt" data-v="hasnt-finished">hasn't finished</button><button class="mc-opt" data-v="havent-finished">haven't finished</button><button class="mc-opt" data-v="didnt-finished">didn't finished</button></div></div>
      <div class="mc-item" data-answer="yes-i-have"><div class="mc-q"><span class="num">6</span><span>— Have you ever eaten sushi? — <span class="gap-mini">?</span> It was great!</span></div><div class="mc-opts"><button class="mc-opt" data-v="yes-i-have">Yes, I have.</button><button class="mc-opt" data-v="yes-i-did">Yes, I did.</button><button class="mc-opt" data-v="yes-i-am">Yes, I am.</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-pp">Check</button><span class="score-pill" data-score-for="sec-pp">— / 6</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · Past Cont vs Past Simple (while / when) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Past Cont vs Past Simple — while / when</em></h2>
    <span class="tag">interrupted action</span>
  </div>
  <div class="section-sub">A long action in the past + a short one that cuts it off. From Shopping Day.</div>
  <div class="card">
    <span class="ex-sticker">🧠</span>
    <h3><span class="ex-num">G+.19</span> Mini-theory</h3>
    <div class="theory">
      <div class="rule">· <strong>WHILE</strong> + Past Continuous (long action)<br>· <strong>WHEN</strong> + Past Simple (short action)<br><em>While I <strong>was eating</strong> breakfast, the phone <strong>rang</strong>.</em><br><em>When Mum <strong>came</strong> home, I <strong>was reading</strong> a book.</em></div>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">⚡</span>
    <h3><span class="ex-num">G+.20</span> Pick Past Simple or Past Continuous</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="was-reading"><div class="mc-q"><span class="num">1</span><span>I <span class="gap-mini">?</span> when Mum came home.</span></div><div class="mc-opts"><button class="mc-opt" data-v="read">read</button><button class="mc-opt" data-v="was-reading">was reading</button><button class="mc-opt" data-v="am-reading">am reading</button></div></div>
      <div class="mc-item" data-answer="rang"><div class="mc-q"><span class="num">2</span><span>While Mum was cooking, the phone <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="was-ringing">was ringing</button><button class="mc-opt" data-v="rang">rang</button><button class="mc-opt" data-v="rings">rings</button></div></div>
      <div class="mc-item" data-answer="was-playing"><div class="mc-q"><span class="num">3</span><span>John <span class="gap-mini">?</span> with his dinosaurs when it started to rain.</span></div><div class="mc-opts"><button class="mc-opt" data-v="was-playing">was playing</button><button class="mc-opt" data-v="played">played</button><button class="mc-opt" data-v="plays">plays</button></div></div>
      <div class="mc-item" data-answer="fell"><div class="mc-q"><span class="num">4</span><span>Emma was running fast — and she <span class="gap-mini">?</span> down!</span></div><div class="mc-opts"><button class="mc-opt" data-v="was-falling">was falling</button><button class="mc-opt" data-v="fell">fell</button><button class="mc-opt" data-v="falls">falls</button></div></div>
      <div class="mc-item" data-answer="was-sleeping"><div class="mc-q"><span class="num">5</span><span>Barsik <span class="gap-mini">?</span> peacefully when the doorbell rang.</span></div><div class="mc-opts"><button class="mc-opt" data-v="slept">slept</button><button class="mc-opt" data-v="was-sleeping">was sleeping</button><button class="mc-opt" data-v="is-sleeping">is sleeping</button></div></div>
      <div class="mc-item" data-answer="saw"><div class="mc-q"><span class="num">6</span><span>While we were walking to school, we <span class="gap-mini">?</span> a huge black cat.</span></div><div class="mc-opts"><button class="mc-opt" data-v="were-seeing">were seeing</button><button class="mc-opt" data-v="saw">saw</button><button class="mc-opt" data-v="see">see</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-pastcont-vs">Check</button><span class="score-pill" data-score-for="sec-pastcont-vs">— / 6</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · There is / There are ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>There is / There are</em></h2>
    <span class="tag">existence</span>
  </div>
  <div class="section-sub">To say what exists in a place: there is (singular), there are (plural).</div>
  <div class="card">
    <span class="ex-sticker">🏠</span>
    <h3><span class="ex-num">G+.21</span> Pick is or are</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="there-is"><div class="mc-q"><span class="num">1</span><span><span class="gap-mini">?</span> a big park near our flat.</span></div><div class="mc-opts"><button class="mc-opt" data-v="there-is">There is</button><button class="mc-opt" data-v="there-are">There are</button></div></div>
      <div class="mc-item" data-answer="there-are"><div class="mc-q"><span class="num">2</span><span><span class="gap-mini">?</span> three of us in the family.</span></div><div class="mc-opts"><button class="mc-opt" data-v="there-is">There is</button><button class="mc-opt" data-v="there-are">There are</button></div></div>
      <div class="mc-item" data-answer="there-are"><div class="mc-q"><span class="num">3</span><span><span class="gap-mini">?</span> six kittens on Mrs. Pilsberry's table.</span></div><div class="mc-opts"><button class="mc-opt" data-v="there-is">There is</button><button class="mc-opt" data-v="there-are">There are</button></div></div>
      <div class="mc-item" data-answer="there-is"><div class="mc-q"><span class="num">4</span><span><span class="gap-mini">?</span> a long queue at the ticket booth.</span></div><div class="mc-opts"><button class="mc-opt" data-v="there-is">There is</button><button class="mc-opt" data-v="there-are">There are</button></div></div>
      <div class="mc-item" data-answer="there-isnt"><div class="mc-q"><span class="num">5</span><span><span class="gap-mini">?</span> any milk in the fridge — Mum, I need some for cereal!</span></div><div class="mc-opts"><button class="mc-opt" data-v="there-isnt">There isn't</button><button class="mc-opt" data-v="there-arent">There aren't</button></div></div>
      <div class="mc-item" data-answer="are-there"><div class="mc-q"><span class="num">6</span><span><span class="gap-mini">?</span> any Scottish Folds in your flat? — No, we have Barsik!</span></div><div class="mc-opts"><button class="mc-opt" data-v="is-there">Is there</button><button class="mc-opt" data-v="are-there">Are there</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-thereis">Check</button><span class="score-pill" data-score-for="sec-thereis">— / 6</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · Articles a / an / the ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Articles — a / an / the</em></h2>
    <span class="tag">articles · base</span>
  </div>
  <div class="section-sub">Little words that go before nouns.</div>
  <div class="card">
    <span class="ex-sticker">📘</span>
    <h3><span class="ex-num">G+.22</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>a</th><td>before a consonant sound</td><td><em>a cat · a book · a hotel</em></td></tr>
        <tr><th>an</th><td>before a vowel sound (a/e/i/o/u)</td><td><em>an apple · an egg · an owl · an hour</em></td></tr>
        <tr><th>the</th><td>when both people know what we mean</td><td><em>Close the door. · the sun · the Queen</em></td></tr>
      </table>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">✏️</span>
    <h3><span class="ex-num">G+.23</span> Pick a / an / the</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="a"><div class="mc-q"><span class="num">1</span><span>Barsik is <span class="gap-mini">?</span> big grey cat.</span></div><div class="mc-opts"><button class="mc-opt" data-v="a">a</button><button class="mc-opt" data-v="an">an</button><button class="mc-opt" data-v="the">the</button></div></div>
      <div class="mc-item" data-answer="an"><div class="mc-q"><span class="num">2</span><span>I ate <span class="gap-mini">?</span> apple for breakfast.</span></div><div class="mc-opts"><button class="mc-opt" data-v="a">a</button><button class="mc-opt" data-v="an">an</button><button class="mc-opt" data-v="the">the</button></div></div>
      <div class="mc-item" data-answer="the"><div class="mc-q"><span class="num">3</span><span>Close <span class="gap-mini">?</span> door, please — it's cold!</span></div><div class="mc-opts"><button class="mc-opt" data-v="a">a</button><button class="mc-opt" data-v="an">an</button><button class="mc-opt" data-v="the">the</button></div></div>
      <div class="mc-item" data-answer="a"><div class="mc-q"><span class="num">4</span><span>Mrs. Pilsberry is <span class="gap-mini">?</span> cat breeder.</span></div><div class="mc-opts"><button class="mc-opt" data-v="a">a</button><button class="mc-opt" data-v="an">an</button><button class="mc-opt" data-v="the">the</button></div></div>
      <div class="mc-item" data-answer="an"><div class="mc-q"><span class="num">5</span><span>In the garden there was <span class="gap-mini">?</span> old brown owl.</span></div><div class="mc-opts"><button class="mc-opt" data-v="a">a</button><button class="mc-opt" data-v="an">an</button><button class="mc-opt" data-v="the">the</button></div></div>
      <div class="mc-item" data-answer="the"><div class="mc-q"><span class="num">6</span><span><span class="gap-mini">?</span> sun was big and orange.</span></div><div class="mc-opts"><button class="mc-opt" data-v="a">a</button><button class="mc-opt" data-v="an">an</button><button class="mc-opt" data-v="the">the</button></div></div>
      <div class="mc-item" data-answer="an"><div class="mc-q"><span class="num">7</span><span>Can I have <span class="gap-mini">?</span> ice cream, please?</span></div><div class="mc-opts"><button class="mc-opt" data-v="a">a</button><button class="mc-opt" data-v="an">an</button><button class="mc-opt" data-v="the">the</button></div></div>
      <div class="mc-item" data-answer="the"><div class="mc-q"><span class="num">8</span><span>I'm going to <span class="gap-mini">?</span> airport tomorrow — flight to Bodrum!</span></div><div class="mc-opts"><button class="mc-opt" data-v="a">a</button><button class="mc-opt" data-v="an">an</button><button class="mc-opt" data-v="the">the</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-articles">Check</button><span class="score-pill" data-score-for="sec-articles">— / 8</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · Might / Could (Halloween) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Might / Could — maybe, possibly</em></h2>
    <span class="tag">modals · possibility</span>
  </div>
  <div class="section-sub">Two modals for things that are not sure — maybe yes, maybe no. From Halloween.</div>
  <div class="card">
    <span class="ex-sticker">🔮</span>
    <h3><span class="ex-num">G+.24</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>might</th><td>maybe · not sure (50/50)</td><td><em>It might rain later.</em></td></tr>
        <tr><th>could</th><td>possibility · ability in past</td><td><em>That could be a ghost! · When I was 5, I could swim.</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">After might/could — bare V (no <code>to</code>, no <code>-s</code>).</div>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">👻</span>
    <h3><span class="ex-num">G+.25</span> Pick might or could</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="might"><div class="mc-q"><span class="num">1</span><span>Take an umbrella — it <span class="gap-mini">?</span> rain this afternoon.</span></div><div class="mc-opts"><button class="mc-opt" data-v="must">must</button><button class="mc-opt" data-v="might">might</button><button class="mc-opt" data-v="should">should</button></div></div>
      <div class="mc-item" data-answer="could"><div class="mc-q"><span class="num">2</span><span>When I was six, I <span class="gap-mini">?</span> already read small books.</span></div><div class="mc-opts"><button class="mc-opt" data-v="could">could</button><button class="mc-opt" data-v="might">might</button><button class="mc-opt" data-v="must">must</button></div></div>
      <div class="mc-item" data-answer="might"><div class="mc-q"><span class="num">3</span><span>Who is at the door? It <span class="gap-mini">?</span> be the postman.</span></div><div class="mc-opts"><button class="mc-opt" data-v="might">might</button><button class="mc-opt" data-v="can">can</button><button class="mc-opt" data-v="should">should</button></div></div>
      <div class="mc-item" data-answer="could"><div class="mc-q"><span class="num">4</span><span>Shhh… that <span class="gap-mini">?</span> be a real ghost!</span></div><div class="mc-opts"><button class="mc-opt" data-v="should">should</button><button class="mc-opt" data-v="could">could</button><button class="mc-opt" data-v="must">must</button></div></div>
      <div class="mc-item" data-answer="might-not"><div class="mc-q"><span class="num">5</span><span>John <span class="gap-mini">?</span> come to the party — he has a cold.</span></div><div class="mc-opts"><button class="mc-opt" data-v="might-not">might not</button><button class="mc-opt" data-v="must-not">must not</button><button class="mc-opt" data-v="should-not">should not</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-might">Check</button><span class="score-pill" data-score-for="sec-might">— / 5</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · Conditional If...then ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>First conditional — If…, then will…</em></h2>
    <span class="tag new">A2 → B1</span>
  </div>
  <div class="section-sub">If something happens, something else will happen. One rule, million uses.</div>
  <div class="card">
    <span class="ex-sticker">🧩</span>
    <h3><span class="ex-num">G+.26</span> Mini-theory</h3>
    <div class="theory">
      <div class="rule"><strong>If</strong> + Present Simple, <strong>will</strong> + V.<br><em>If it rains, we will stay at home.</em><br><em>If you are hungry, I will make you a sandwich.</em></div>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">🌧</span>
    <h3><span class="ex-num">G+.27</span> Complete the First Conditional</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="will-stay"><div class="mc-q"><span class="num">1</span><span>If it rains tomorrow, we <span class="gap-mini">?</span> at home.</span></div><div class="mc-opts"><button class="mc-opt" data-v="stay">stay</button><button class="mc-opt" data-v="will-stay">will stay</button><button class="mc-opt" data-v="stayed">stayed</button></div></div>
      <div class="mc-item" data-answer="finish"><div class="mc-q"><span class="num">2</span><span>If John <span class="gap-mini">?</span> his homework, he can play.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-finish">will finish</button><button class="mc-opt" data-v="finish">finish</button><button class="mc-opt" data-v="finishes">finishes</button></div></div>
      <div class="mc-item" data-answer="will-eat"><div class="mc-q"><span class="num">3</span><span>If Mum makes pancakes, Barsik <span class="gap-mini">?</span> half of them.</span></div><div class="mc-opts"><button class="mc-opt" data-v="eats">eats</button><button class="mc-opt" data-v="will-eat">will eat</button><button class="mc-opt" data-v="ate">ate</button></div></div>
      <div class="mc-item" data-answer="is"><div class="mc-q"><span class="num">4</span><span>If it <span class="gap-mini">?</span> sunny on Friday, we'll go to the park for Mum's birthday.</span></div><div class="mc-opts"><button class="mc-opt" data-v="is">is</button><button class="mc-opt" data-v="will-be">will be</button><button class="mc-opt" data-v="was">was</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-cond">Check</button><span class="score-pill" data-score-for="sec-cond">— / 4</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · Object pronouns (me / him / her / us / them) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Object pronouns — me / him / her / us / them</em></h2>
    <span class="tag">pronouns</span>
  </div>
  <div class="section-sub">The second form of the pronoun — after a verb or preposition. From the Pet Shop lesson.</div>
  <div class="card">
    <span class="ex-sticker">🔁</span>
    <h3><span class="ex-num">G+.28</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>subject</th><td>I</td><td>you</td><td>he</td><td>she</td><td>it</td><td>we</td><td>they</td></tr>
        <tr><th>object</th><td><code>me</code></td><td><code>you</code></td><td><code>him</code></td><td><code>her</code></td><td><code>it</code></td><td><code>us</code></td><td><code>them</code></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">Use the OBJECT form after a verb or a preposition: <code>Mum drives <strong>us</strong>.</code> · <code>Give it to <strong>her</strong>.</code></div>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">💬</span>
    <h3><span class="ex-num">G+.29</span> Pick the right pronoun</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="us"><div class="mc-q"><span class="num">1</span><span>Mum drives John and <span class="gap-mini">?</span> to school every day.</span></div><div class="mc-opts"><button class="mc-opt" data-v="we">we</button><button class="mc-opt" data-v="us">us</button><button class="mc-opt" data-v="our">our</button></div></div>
      <div class="mc-item" data-answer="him"><div class="mc-q"><span class="num">2</span><span>John lost his shoe — we all looked for <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="he">he</button><button class="mc-opt" data-v="him">him</button><button class="mc-opt" data-v="it">it</button></div></div>
      <div class="mc-item" data-answer="her"><div class="mc-q"><span class="num">3</span><span>Emma is my friend. I love <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="she">she</button><button class="mc-opt" data-v="her">her</button><button class="mc-opt" data-v="hers">hers</button></div></div>
      <div class="mc-item" data-answer="them"><div class="mc-q"><span class="num">4</span><span>The kittens are tiny. Mrs. Pilsberry sells <span class="gap-mini">?</span> for 50 000 roubles.</span></div><div class="mc-opts"><button class="mc-opt" data-v="they">they</button><button class="mc-opt" data-v="them">them</button><button class="mc-opt" data-v="theirs">theirs</button></div></div>
      <div class="mc-item" data-answer="me"><div class="mc-q"><span class="num">5</span><span>Can you help <span class="gap-mini">?</span>, please? I can't find my book.</span></div><div class="mc-opts"><button class="mc-opt" data-v="I">I</button><button class="mc-opt" data-v="me">me</button><button class="mc-opt" data-v="my">my</button></div></div>
      <div class="mc-item" data-answer="it"><div class="mc-q"><span class="num">6</span><span>Barsik is sleeping — don't wake <span class="gap-mini">?</span> up!</span></div><div class="mc-opts"><button class="mc-opt" data-v="he">he</button><button class="mc-opt" data-v="him">him</button><button class="mc-opt" data-v="it">it</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-pronouns">Check</button><span class="score-pill" data-score-for="sec-pronouns">— / 6</span></div>
  </div>
</section>

<!-- ===== GRAMMAR · How much / How many ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>How much / How many?</em></h2>
    <span class="tag">quantity</span>
  </div>
  <div class="section-sub">Countable vs uncountable — one of the first things you learn.</div>
  <div class="card">
    <span class="ex-sticker">🧮</span>
    <h3><span class="ex-num">G+.30</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>How many</th><td>countable (plural)</td><td><em>How many apples? How many kittens?</em></td></tr>
        <tr><th>How much</th><td>uncountable (singular, no -s)</td><td><em>How much milk? How much honey? How much money?</em></td></tr>
      </table>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">🍎</span>
    <h3><span class="ex-num">G+.31</span> Pick much or many</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="many"><div class="mc-q"><span class="num">1</span><span>How <span class="gap-mini">?</span> kittens were on the table?</span></div><div class="mc-opts"><button class="mc-opt" data-v="much">much</button><button class="mc-opt" data-v="many">many</button></div></div>
      <div class="mc-item" data-answer="much"><div class="mc-q"><span class="num">2</span><span>How <span class="gap-mini">?</span> honey do we need for the pancakes?</span></div><div class="mc-opts"><button class="mc-opt" data-v="much">much</button><button class="mc-opt" data-v="many">many</button></div></div>
      <div class="mc-item" data-answer="many"><div class="mc-q"><span class="num">3</span><span>How <span class="gap-mini">?</span> tickets did Julia buy at the fair?</span></div><div class="mc-opts"><button class="mc-opt" data-v="much">much</button><button class="mc-opt" data-v="many">many</button></div></div>
      <div class="mc-item" data-answer="much"><div class="mc-q"><span class="num">4</span><span>How <span class="gap-mini">?</span> milk is left in the carton?</span></div><div class="mc-opts"><button class="mc-opt" data-v="much">much</button><button class="mc-opt" data-v="many">many</button></div></div>
      <div class="mc-item" data-answer="much"><div class="mc-q"><span class="num">5</span><span>How <span class="gap-mini">?</span> does a Scottish Fold cost? — About 50 000 roubles.</span></div><div class="mc-opts"><button class="mc-opt" data-v="much">much</button><button class="mc-opt" data-v="many">many</button></div></div>
      <div class="mc-item" data-answer="many"><div class="mc-q"><span class="num">6</span><span>How <span class="gap-mini">?</span> languages do people in Europe speak?</span></div><div class="mc-opts"><button class="mc-opt" data-v="much">much</button><button class="mc-opt" data-v="many">many</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-howmany">Check</button><span class="score-pill" data-score-for="sec-howmany">— / 6</span></div>
  </div>
</section>

"""

marker_vocab_close = '</div><!-- /tab-vocab -->'
assert text.count(marker_vocab_close) == 1
text = text.replace(marker_vocab_close, VOCAB_FILL + marker_vocab_close)

marker_grammar_close = '</div><!-- /tab-grammar -->'
assert text.count(marker_grammar_close) == 1
text = text.replace(marker_grammar_close, GRAMMAR_FILL + marker_grammar_close)

HTML.write_text(text, encoding="utf-8")
print(f"Done: filled all gaps. File size: {len(text)} chars.")
