"""Delete Monday chapters 1-5 (lines 730-1315) and inject new Vocab Recall + Grammar Recap blocks.

Reads the current index.html, replaces the range of lines corresponding to
old Monday chapters with a new unified block of:
  - Vocab Recall by theme (Shopping / Fair / Halloween / Chores)
  - Irregular Verbs mega grid
  - Grammar Recap (Present Simple / Past Simple / Past Continuous / going to / will)
"""
import pathlib

HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"
text = HTML.read_text(encoding="utf-8")

START = "<!-- ===== 3 · CHAPTER 1 · MORNING (Present Simple + frequency + time) ===== -->"
END = "<!-- ===== 7 · THEORY CORNER · WILL vs GOING TO ===== -->"

i = text.find(START)
j = text.find(END)
assert i != -1 and j != -1, f"markers not found: start={i} end={j}"

NEW_BLOCK = """<!-- ===== 3 · VOCAB RECALL · SHOPPING DAY (containers + shop lexis) ===== -->
<section class="section" id="sec-vocab-shopping">
  <div class="section-hdr">
    <div class="num">3</div>
    <h2>Vocab Recall · <em>Shopping Day — containers &amp; shop lexis</em></h2>
    <span class="tag">recall · match + fill</span>
  </div>
  <div class="section-sub">Remember these from Shopping Day with Julia? Match the word to the picture — then put it in the sentence.</div>

  <div class="card">
    <span class="ex-sticker">\U0001F4B0</span>
    <h3><span class="ex-num">3.1</span> Match the word with the picture (shopping)</h3>
    <p style="color:var(--muted);font-size:.86rem">Click a word, then click its picture.</p>
    <div class="match-wrap" id="match-shopping">
      <div class="match-pics" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(100px,1fr));gap:8px;margin-bottom:10px">
        <div class="match-pic" data-w="shop-assistant"><img src="img/vocab/shop-assistant.png" alt="shop assistant" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
        <div class="match-pic" data-w="price-tag"><img src="img/vocab/price-tag.png" alt="price tag" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
        <div class="match-pic" data-w="till"><img src="img/vocab/till.png" alt="till" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
        <div class="match-pic" data-w="fitting-room"><img src="img/vocab/fitting-room.png" alt="fitting room" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
        <div class="match-pic" data-w="receipt"><img src="img/vocab/receipt.png" alt="receipt" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
        <div class="match-pic" data-w="hanger"><img src="img/vocab/hanger.png" alt="hanger" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
        <div class="match-pic" data-w="mirror"><img src="img/vocab/mirror.png" alt="mirror" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
        <div class="match-pic" data-w="shopping-bag"><img src="img/vocab/shopping-bag.png" alt="shopping bag" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
        <div class="match-pic" data-w="cash"><img src="img/vocab/cash.png" alt="cash" style="width:100%;border-radius:8px;border:1.5px solid var(--line);background:#fff"></div>
      </div>
      <div class="match-words" id="match-shopping-words" style="display:flex;flex-wrap:wrap;gap:6px;padding:10px;background:var(--card-2);border:1.5px dashed var(--accent-3);border-radius:10px">
        <button class="bank-word" data-w="receipt">receipt</button>
        <button class="bank-word" data-w="mirror">mirror</button>
        <button class="bank-word" data-w="price-tag">price tag</button>
        <button class="bank-word" data-w="shopping-bag">shopping bag</button>
        <button class="bank-word" data-w="shop-assistant">shop assistant</button>
        <button class="bank-word" data-w="fitting-room">fitting room</button>
        <button class="bank-word" data-w="hanger">hanger</button>
        <button class="bank-word" data-w="till">till</button>
        <button class="bank-word" data-w="cash">cash</button>
      </div>
    </div>
    <p style="color:var(--muted);font-size:.82rem;margin-top:8px;font-style:italic">(click word → click picture; click picture again to clear)</p>
  </div>

  <div class="card">
    <span class="ex-sticker">\U0001F6D2</span>
    <h3><span class="ex-num">3.2</span> Fill the shop sentence</h3>
    <div class="bank" id="bank-shop-fill">
      <button class="bank-word" data-w="price tag">price tag</button>
      <button class="bank-word" data-w="receipt">receipt</button>
      <button class="bank-word" data-w="fitting room">fitting room</button>
      <button class="bank-word" data-w="till">till</button>
      <button class="bank-word" data-w="hanger">hanger</button>
      <button class="bank-word" data-w="cash">cash</button>
      <button class="bank-word" data-w="shop assistant">shop assistant</button>
      <button class="bank-word" data-w="shopping bag">shopping bag</button>
    </div>
    <div class="drag-text" data-group="shop-fill">
      <div class="line-q"><span class="num">1</span><span>I asked the <span class="drop-gap" data-ans="shop assistant">?</span> for a bigger size.</span></div>
      <div class="line-q"><span class="num">2</span><span>Look at the <span class="drop-gap" data-ans="price tag">?</span> — these jeans are 2 500 roubles.</span></div>
      <div class="line-q"><span class="num">3</span><span>Can I try this on? Where is the <span class="drop-gap" data-ans="fitting room">?</span>, please?</span></div>
      <div class="line-q"><span class="num">4</span><span>The <span class="drop-gap" data-ans="till">?</span> is over there — you pay there.</span></div>
      <div class="line-q"><span class="num">5</span><span>Please keep the <span class="drop-gap" data-ans="receipt">?</span> — maybe you'll change your mind.</span></div>
      <div class="line-q"><span class="num">6</span><span>Hang the dress on this <span class="drop-gap" data-ans="hanger">?</span>, please.</span></div>
      <div class="line-q"><span class="num">7</span><span>Do you have <span class="drop-gap" data-ans="cash">?</span>, or will you use a card?</span></div>
      <div class="line-q"><span class="num">8</span><span>My <span class="drop-gap" data-ans="shopping bag">?</span> is so heavy I can't carry it!</span></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-vocab-shopping-fill">Check</button>
      <button class="btn-reset" data-reset="sec-vocab-shopping-fill">clear</button>
      <span class="score-pill" data-score-for="sec-vocab-shopping-fill">— / 8</span>
    </div>
  </div>
</section>

<!-- ===== 4 · VOCAB RECALL · FAIR + ANIMALS ===== -->
<section class="section" id="sec-vocab-fair">
  <div class="section-hdr">
    <div class="num">4</div>
    <h2>Vocab Recall · <em>the Fair, the Pet Shop, the Animal Exhibition</em></h2>
    <span class="tag">recall · MCQ + fill</span>
  </div>
  <div class="section-sub">Remember last summer’s trip to the city fair with Emma and John? Mrs. Pilsberry’s Scottish Folds? Julia’s Pet Shop with the snail? Let’s see what stuck.</div>

  <div class="card">
    <span class="ex-sticker">\U0001F3AA</span>
    <h3><span class="ex-num">4.1</span> Pick the right word</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="queue">
        <div class="mc-q"><span class="num">1</span><span>At the gate of the fair there was a long <span class="gap-mini">?</span> for tickets.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="queue">queue</button><button class="mc-opt" data-v="shelf">shelf</button><button class="mc-opt" data-v="cash">cash</button></div>
      </div>
      <div class="mc-item" data-answer="ticket">
        <div class="mc-q"><span class="num">2</span><span>John put his orange <span class="gap-mini">?</span> in his pocket and kept it like a treasure.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="receipt">receipt</button><button class="mc-opt" data-v="ticket">ticket</button><button class="mc-opt" data-v="hanger">hanger</button></div>
      </div>
      <div class="mc-item" data-answer="carousel">
        <div class="mc-q"><span class="num">3</span><span>John rode a painted white horse on the <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="Ferris wheel">Ferris wheel</button><button class="mc-opt" data-v="aquarium">aquarium</button><button class="mc-opt" data-v="carousel">carousel</button></div>
      </div>
      <div class="mc-item" data-answer="breeder">
        <div class="mc-q"><span class="num">4</span><span>Mrs. Pilsberry is a cat <span class="gap-mini">?</span> — she sells Scottish Folds.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="shop assistant">shop assistant</button><button class="mc-opt" data-v="breeder">breeder</button><button class="mc-opt" data-v="teacher">teacher</button></div>
      </div>
      <div class="mc-item" data-answer="kittens">
        <div class="mc-q"><span class="num">5</span><span>Six fluffy grey <span class="gap-mini">?</span> with folded ears sat on her table.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="rabbits">rabbits</button><button class="mc-opt" data-v="parrots">parrots</button><button class="mc-opt" data-v="kittens">kittens</button></div>
      </div>
      <div class="mc-item" data-answer="50 000">
        <div class="mc-q"><span class="num">6</span><span>A purebred Scottish Fold kitten costs about <span class="gap-mini">?</span> roubles.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="500">500</button><button class="mc-opt" data-v="5 000">5 000</button><button class="mc-opt" data-v="50 000">50 000</button></div>
      </div>
      <div class="mc-item" data-answer="aquarium">
        <div class="mc-q"><span class="num">7</span><span>In the Animal Exhibition there was a small <span class="gap-mini">?</span> with goldfish.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="aquarium">aquarium</button><button class="mc-opt" data-v="cauldron">cauldron</button><button class="mc-opt" data-v="hanger">hanger</button></div>
      </div>
      <div class="mc-item" data-answer="snail">
        <div class="mc-q"><span class="num">8</span><span>In the Pet Shop Julia bought a special pet — a <span class="gap-mini">?</span> called Turbo.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="parrot">parrot</button><button class="mc-opt" data-v="snail">snail</button><button class="mc-opt" data-v="owl">owl</button></div>
      </div>
      <div class="mc-item" data-answer="stroke">
        <div class="mc-q"><span class="num">9</span><span>Mrs. Pilsberry said: “You can <span class="gap-mini">?</span> them very gently — one finger.”</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="hold">hold</button><button class="mc-opt" data-v="stroke">stroke</button><button class="mc-opt" data-v="throw">throw</button></div>
      </div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-vocab-fair-mc">Check</button>
      <span class="score-pill" data-score-for="sec-vocab-fair-mc">— / 9</span>
    </div>
  </div>
</section>

<!-- ===== 5 · VOCAB RECALL · HALLOWEEN ===== -->
<section class="section" id="sec-vocab-hall">
  <div class="section-hdr">
    <div class="num">5</div>
    <h2>Vocab Recall · <em>Halloween night at the castle</em></h2>
    <span class="tag">recall · match</span>
  </div>
  <div class="section-sub">All these words from your Halloween lesson. Match the word with the emoji — then put the right one in the sentence.</div>

  <div class="card">
    <span class="ex-sticker">\U0001F383</span>
    <h3><span class="ex-num">5.1</span> Fill in the sentence with the right Halloween word</h3>
    <div class="bank" id="bank-hall">
      <button class="bank-word" data-w="pumpkin">pumpkin</button>
      <button class="bank-word" data-w="ghost">ghost</button>
      <button class="bank-word" data-w="witch">witch</button>
      <button class="bank-word" data-w="costume">costume</button>
      <button class="bank-word" data-w="candy">candy</button>
      <button class="bank-word" data-w="broomstick">broomstick</button>
      <button class="bank-word" data-w="cauldron">cauldron</button>
      <button class="bank-word" data-w="bat">bat</button>
      <button class="bank-word" data-w="haunted">haunted</button>
      <button class="bank-word" data-w="trick or treat">trick or treat</button>
    </div>
    <div class="drag-text" data-group="hall">
      <div class="line-q"><span class="num">1</span><span>People carve faces on a big <span class="drop-gap" data-ans="pumpkin">?</span> and put a candle inside.</span></div>
      <div class="line-q"><span class="num">2</span><span>At midnight a white <span class="drop-gap" data-ans="ghost">?</span> walked down the castle stairs.</span></div>
      <div class="line-q"><span class="num">3</span><span>Julia’s costume was a <span class="drop-gap" data-ans="witch">?</span> with a tall black hat.</span></div>
      <div class="line-q"><span class="num">4</span><span>Children knock on the door and shout “<span class="drop-gap" data-ans="trick or treat">?</span>!”</span></div>
      <div class="line-q"><span class="num">5</span><span>Emma’s <span class="drop-gap" data-ans="costume">?</span> was a big white sheet with eye-holes — a sweet ghost.</span></div>
      <div class="line-q"><span class="num">6</span><span>In the castle garden, the witch cooked a magic potion in her big <span class="drop-gap" data-ans="cauldron">?</span>.</span></div>
      <div class="line-q"><span class="num">7</span><span>A <span class="drop-gap" data-ans="broomstick">?</span> is what the witch flies on.</span></div>
      <div class="line-q"><span class="num">8</span><span>People hang paper <span class="drop-gap" data-ans="bat">?</span>s on strings for decoration.</span></div>
      <div class="line-q"><span class="num">9</span><span>A <span class="drop-gap" data-ans="haunted">?</span> house is a scary place where ghosts live.</span></div>
      <div class="line-q"><span class="num">10</span><span>Julia’s bag was full of <span class="drop-gap" data-ans="candy">?</span> after the trick-or-treating.</span></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-vocab-hall-fill">Check</button>
      <button class="btn-reset" data-reset="sec-vocab-hall-fill">clear</button>
      <span class="score-pill" data-score-for="sec-vocab-hall-fill">— / 10</span>
    </div>
  </div>
</section>

<!-- ===== 6 · GRAMMAR RECAP · ALL TENSES WITHOUT A MONDAY FRAME ===== -->
<section class="section" id="sec-grammar">
  <div class="section-hdr">
    <div class="num">6</div>
    <h2>Grammar Recap · <em>everything we’ve done, in one place</em></h2>
    <span class="tag">A2 → B1</span>
  </div>
  <div class="section-sub">Six tenses, one sweep. Each line — one tense. Think WHEN it happens, then pick.</div>

  <div class="card">
    <span class="ex-sticker">\U0001F9E0</span>
    <h3><span class="ex-num">6.1</span> Mini-theory — the 6 shapes we use</h3>
    <div class="theory">
      <h4>Six faces of a verb</h4>
      <table>
        <tr><th>Tense</th><th>Shape</th><th>Example</th></tr>
        <tr><td>Present Simple</td><td><code>V / Vs</code></td><td><em>Julia drives to school every day.</em></td></tr>
        <tr><td>Present Continuous</td><td><code>am/is/are + V-ing</code></td><td><em>She is driving now.</em></td></tr>
        <tr><td>Past Simple</td><td><code>V2</code></td><td><em>She drove yesterday.</em></td></tr>
        <tr><td>Past Continuous</td><td><code>was/were + V-ing</code></td><td><em>She was driving when the cat jumped.</em></td></tr>
        <tr><td>going to (future plan)</td><td><code>am/is/are + going to + V</code></td><td><em>She is going to drive us tomorrow.</em></td></tr>
        <tr><td>will (prediction / promise)</td><td><code>will + V</code></td><td><em>She will drive if it rains.</em></td></tr>
      </table>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">\U0001F3AF</span>
    <h3><span class="ex-num">6.2</span> Pick the right tense — 12 mixed items</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="goes">
        <div class="mc-q"><span class="num">1</span><span>Julia <span class="gap-mini">?</span> to school every weekday. <em style="color:var(--muted);font-size:.85em">(every day → ?)</em></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="is going">is going</button><button class="mc-opt" data-v="goes">goes</button><button class="mc-opt" data-v="went">went</button></div>
      </div>
      <div class="mc-item" data-answer="is-drawing">
        <div class="mc-q"><span class="num">2</span><span>Right now Emma <span class="gap-mini">?</span> a flower in her copybook.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="draws">draws</button><button class="mc-opt" data-v="is-drawing">is drawing</button><button class="mc-opt" data-v="drew">drew</button></div>
      </div>
      <div class="mc-item" data-answer="ate">
        <div class="mc-q"><span class="num">3</span><span>Yesterday the cat <span class="gap-mini">?</span> my sausage!</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="eats">eats</button><button class="mc-opt" data-v="ate">ate</button><button class="mc-opt" data-v="is eating">is eating</button></div>
      </div>
      <div class="mc-item" data-answer="was-eating">
        <div class="mc-q"><span class="num">4</span><span>I <span class="gap-mini">?</span> pancakes when the cat jumped on the table.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="ate">ate</button><button class="mc-opt" data-v="was-eating">was eating</button><button class="mc-opt" data-v="eat">eat</button></div>
      </div>
      <div class="mc-item" data-answer="are-going-to">
        <div class="mc-q"><span class="num">5</span><span>After school we <span class="gap-mini">?</span> meet at the café. <em style="color:var(--muted);font-size:.85em">(decided this morning)</em></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="will">will</button><button class="mc-opt" data-v="are-going-to">are going to</button><button class="mc-opt" data-v="go">go</button></div>
      </div>
      <div class="mc-item" data-answer="will">
        <div class="mc-q"><span class="num">6</span><span>— The bag is heavy! — I <span class="gap-mini">?</span> help you! <em style="color:var(--muted);font-size:.85em">(decision this second)</em></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="am-going-to">am going to</button><button class="mc-opt" data-v="will">will</button><button class="mc-opt" data-v="help">help</button></div>
      </div>
      <div class="mc-item" data-answer="forgot">
        <div class="mc-q"><span class="num">7</span><span>I <span class="gap-mini">?</span> my English book in the kitchen yesterday.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="forgets">forgets</button><button class="mc-opt" data-v="forgotted">forgotted</button><button class="mc-opt" data-v="forgot">forgot</button></div>
      </div>
      <div class="mc-item" data-answer="never">
        <div class="mc-q"><span class="num">8</span><span>Julia <span class="gap-mini">?</span> walks to school — Mum drives her every day.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="always">always</button><button class="mc-opt" data-v="never">never</button><button class="mc-opt" data-v="usually">usually</button></div>
      </div>
      <div class="mc-item" data-answer="was-sitting">
        <div class="mc-q"><span class="num">9</span><span>Barsik <span class="gap-mini">?</span> on the window sill when the doorbell rang.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="sat">sat</button><button class="mc-opt" data-v="was-sitting">was sitting</button><button class="mc-opt" data-v="is-sitting">is sitting</button></div>
      </div>
      <div class="mc-item" data-answer="will-rain">
        <div class="mc-q"><span class="num">10</span><span>Mum says it <span class="gap-mini">?</span> on Friday — but I don’t believe her.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="is raining">is raining</button><button class="mc-opt" data-v="rains">rains</button><button class="mc-opt" data-v="will-rain">will rain</button></div>
      </div>
      <div class="mc-item" data-answer="am-going-to-bake">
        <div class="mc-q"><span class="num">11</span><span>On Mum’s birthday I <span class="gap-mini">?</span> a strawberry cake. <em style="color:var(--muted);font-size:.85em">(a planned event)</em></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="will-bake">will bake</button><button class="mc-opt" data-v="am-going-to-bake">am going to bake</button><button class="mc-opt" data-v="baked">baked</button></div>
      </div>
      <div class="mc-item" data-answer="are-living">
        <div class="mc-q"><span class="num">12</span><span>These days we <span class="gap-mini">?</span> in a new flat near the park. <em style="color:var(--muted);font-size:.85em">(a temporary situation → ?)</em></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="live">live</button><button class="mc-opt" data-v="are-living">are living</button><button class="mc-opt" data-v="lived">lived</button></div>
      </div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-grammar-mc">Check</button>
      <span class="score-pill" data-score-for="sec-grammar-mc">— / 12</span>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">\U0001F501</span>
    <h3><span class="ex-num">6.3</span> Irregular Verbs — type the Past Simple form (V2)</h3>
    <p style="color:var(--muted);font-size:.86rem">Lowercase, no spaces. Same list as in Bakery Story — you know these.</p>
    <div class="input-list">
      <div class="input-row"><span class="num">1</span><div class="prompt">eat → <b>?</b></div><input type="text" data-ans="ate" placeholder="eat → …"></div>
      <div class="input-row"><span class="num">2</span><div class="prompt">run → <b>?</b></div><input type="text" data-ans="ran" placeholder="run → …"></div>
      <div class="input-row"><span class="num">3</span><div class="prompt">forget → <b>?</b></div><input type="text" data-ans="forgot" placeholder="forget → …"></div>
      <div class="input-row"><span class="num">4</span><div class="prompt">be (I / he / she) → <b>?</b></div><input type="text" data-ans="was" placeholder="be → …"></div>
      <div class="input-row"><span class="num">5</span><div class="prompt">be (we / you / they) → <b>?</b></div><input type="text" data-ans="were" placeholder="be → …"></div>
      <div class="input-row"><span class="num">6</span><div class="prompt">go → <b>?</b></div><input type="text" data-ans="went" placeholder="go → …"></div>
      <div class="input-row"><span class="num">7</span><div class="prompt">see → <b>?</b></div><input type="text" data-ans="saw" placeholder="see → …"></div>
      <div class="input-row"><span class="num">8</span><div class="prompt">take → <b>?</b></div><input type="text" data-ans="took" placeholder="take → …"></div>
      <div class="input-row"><span class="num">9</span><div class="prompt">drink → <b>?</b></div><input type="text" data-ans="drank" placeholder="drink → …"></div>
      <div class="input-row"><span class="num">10</span><div class="prompt">buy → <b>?</b></div><input type="text" data-ans="bought" placeholder="buy → …"></div>
      <div class="input-row"><span class="num">11</span><div class="prompt">make → <b>?</b></div><input type="text" data-ans="made" placeholder="make → …"></div>
      <div class="input-row"><span class="num">12</span><div class="prompt">come → <b>?</b></div><input type="text" data-ans="came" placeholder="come → …"></div>
      <div class="input-row"><span class="num">13</span><div class="prompt">give → <b>?</b></div><input type="text" data-ans="gave" placeholder="give → …"></div>
      <div class="input-row"><span class="num">14</span><div class="prompt">read → <b>?</b></div><input type="text" data-ans="read" placeholder="read → …"></div>
      <div class="input-row"><span class="num">15</span><div class="prompt">write → <b>?</b></div><input type="text" data-ans="wrote" placeholder="write → …"></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-grammar-irreg">Check</button>
      <button class="btn-reset" data-reset="sec-grammar-irreg">clear</button>
      <span class="score-pill" data-score-for="sec-grammar-irreg">— / 15</span>
    </div>
  </div>
</section>

"""

# Rebuild
new_text = text[:i] + NEW_BLOCK + text[j:]
HTML.write_text(new_text, encoding="utf-8")
print(f"Done: cut old chapters ({j - i} chars), inserted new block ({len(NEW_BLOCK)} chars)")
print(f"New file size: {len(new_text)} chars (was {len(text)})")
