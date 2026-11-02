"""Expand Vocab + Grammar tabs with FULL inventory from Julia's past 10 lessons.

Adds into Vocab tab:
  - Containers (cup/bottle/jar/can/carton/tin/packet/box/bag/bar)  — shopping
  - Food market (12 items)                                          — bodrum day 2
  - Pet shop vocab + baby animals                                   — pet-shop-snail
  - Household chores                                                — may-chores
  - 9 Countries (country/capital/nationality/language)              — flags-countries

Adds into Grammar tab:
  - Was/Were                                                        — recap-01
  - Prepositions of place                                           — recap-01
  - Prepositions of time (in/on/at)                                 — recap-01
  - Modal verbs CAN / MAY / MUST / SHOULD                           — chores + pet-shop
  - Comparatives / Superlatives                                     — animal-exhibition
  - Have got / has got                                              — new emphasis
  - Numbers + Ordinals (1st-10th)                                   — bodrum

Adds into Workbook tab:
  - MEGA Irregular Verbs grid (40 verbs type-input)                 — irregular-verbs
"""
import pathlib
HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"
text = HTML.read_text(encoding="utf-8")

# ========================================================================
# VOCAB TAB — insert new vocab sections BEFORE </div><!-- /tab-vocab -->
# ========================================================================

VOCAB_EXTRA = """
<!-- ===== VOCAB RECALL · Containers (shopping-day) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">V+</div>
    <h2>Vocab Recall · <em>Containers — what food comes in</em></h2>
    <span class="tag">shopping · recall</span>
  </div>
  <div class="section-sub">10 containers from Shopping Day: cup, bottle, jar, can, carton, tin, packet, box, bag, bar.</div>
  <div class="card">
    <span class="ex-sticker">🥫</span>
    <h3><span class="ex-num">V+.1</span> Match food &amp; container</h3>
    <div class="bank" id="bank-containers">
      <button class="bank-word" data-w="cup">cup</button>
      <button class="bank-word" data-w="bottle">bottle</button>
      <button class="bank-word" data-w="jar">jar</button>
      <button class="bank-word" data-w="can">can</button>
      <button class="bank-word" data-w="carton">carton</button>
      <button class="bank-word" data-w="tin">tin</button>
      <button class="bank-word" data-w="packet">packet</button>
      <button class="bank-word" data-w="box">box</button>
      <button class="bank-word" data-w="bag">bag</button>
      <button class="bank-word" data-w="bar">bar</button>
    </div>
    <div class="drag-text" data-group="containers">
      <div class="line-q"><span class="num">1</span><span>a <span class="drop-gap" data-ans="cup">?</span> of tea</span></div>
      <div class="line-q"><span class="num">2</span><span>a <span class="drop-gap" data-ans="bottle">?</span> of water</span></div>
      <div class="line-q"><span class="num">3</span><span>a <span class="drop-gap" data-ans="jar">?</span> of honey</span></div>
      <div class="line-q"><span class="num">4</span><span>a <span class="drop-gap" data-ans="can">?</span> of coke</span></div>
      <div class="line-q"><span class="num">5</span><span>a <span class="drop-gap" data-ans="carton">?</span> of milk</span></div>
      <div class="line-q"><span class="num">6</span><span>a <span class="drop-gap" data-ans="tin">?</span> of tuna fish</span></div>
      <div class="line-q"><span class="num">7</span><span>a <span class="drop-gap" data-ans="packet">?</span> of biscuits</span></div>
      <div class="line-q"><span class="num">8</span><span>a <span class="drop-gap" data-ans="box">?</span> of cereal</span></div>
      <div class="line-q"><span class="num">9</span><span>a <span class="drop-gap" data-ans="bag">?</span> of apples</span></div>
      <div class="line-q"><span class="num">10</span><span>a <span class="drop-gap" data-ans="bar">?</span> of chocolate</span></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-containers">Check</button>
      <button class="btn-reset" data-reset="sec-containers">clear</button>
      <span class="score-pill" data-score-for="sec-containers">— / 10</span>
    </div>
  </div>
</section>

<!-- ===== VOCAB RECALL · Food market (bodrum-day-2) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">V+</div>
    <h2>Vocab Recall · <em>Food market — Julia in Bodrum</em></h2>
    <span class="tag">food · 12 words</span>
  </div>
  <div class="section-sub">Remember the little market where you bought fruit and vegetables with Mum last summer?</div>
  <div class="card">
    <span class="ex-sticker">🍅</span>
    <h3><span class="ex-num">V+.2</span> Pick the right food word</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="lemon"><div class="mc-q"><span class="num">1</span><span>Yellow and sour, you squeeze it into tea — <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="apple">apple</button><button class="mc-opt" data-v="lemon">lemon</button><button class="mc-opt" data-v="potato">potato</button></div></div>
      <div class="mc-item" data-answer="tomato"><div class="mc-q"><span class="num">2</span><span>Red, round, in salad — <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="tomato">tomato</button><button class="mc-opt" data-v="orange">orange</button><button class="mc-opt" data-v="cucumber">cucumber</button></div></div>
      <div class="mc-item" data-answer="cucumber"><div class="mc-q"><span class="num">3</span><span>Long, green, crunchy — <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="apple">apple</button><button class="mc-opt" data-v="cucumber">cucumber</button><button class="mc-opt" data-v="onion">onion</button></div></div>
      <div class="mc-item" data-answer="onion"><div class="mc-q"><span class="num">4</span><span>Round, strong smell, makes you cry — <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="onion">onion</button><button class="mc-opt" data-v="orange">orange</button><button class="mc-opt" data-v="potato">potato</button></div></div>
      <div class="mc-item" data-answer="potato"><div class="mc-q"><span class="num">5</span><span>You cook it, you can make chips with it — <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="apple">apple</button><button class="mc-opt" data-v="tomato">tomato</button><button class="mc-opt" data-v="potato">potato</button></div></div>
      <div class="mc-item" data-answer="bread"><div class="mc-q"><span class="num">6</span><span>You cut it into slices, you eat it with butter — <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="cheese">cheese</button><button class="mc-opt" data-v="bread">bread</button><button class="mc-opt" data-v="meat">meat</button></div></div>
      <div class="mc-item" data-answer="milk"><div class="mc-q"><span class="num">7</span><span>White drink, you have it with cereal — <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="milk">milk</button><button class="mc-opt" data-v="butter">butter</button><button class="mc-opt" data-v="meat">meat</button></div></div>
      <div class="mc-item" data-answer="cheese"><div class="mc-q"><span class="num">8</span><span>Yellow, from milk, mice love it — <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="butter">butter</button><button class="mc-opt" data-v="cheese">cheese</button><button class="mc-opt" data-v="milk">milk</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-food">Check</button>
      <span class="score-pill" data-score-for="sec-food">— / 8</span>
    </div>
  </div>
</section>

<!-- ===== VOCAB RECALL · Pet shop + baby animals (pet-shop-snail) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">V+</div>
    <h2>Vocab Recall · <em>Pet shop — animals and their babies</em></h2>
    <span class="tag">animals · babies</span>
  </div>
  <div class="section-sub">From your Pet Shop lesson with Turbo the snail. Adult animals + their baby names.</div>
  <div class="card">
    <span class="ex-sticker">🐾</span>
    <h3><span class="ex-num">V+.3</span> Match adult → baby</h3>
    <div class="bank" id="bank-babies">
      <button class="bank-word" data-w="puppy">puppy</button>
      <button class="bank-word" data-w="kitten">kitten</button>
      <button class="bank-word" data-w="chick">chick</button>
      <button class="bank-word" data-w="rabbit kit">rabbit kit</button>
      <button class="bank-word" data-w="piglet">piglet</button>
      <button class="bank-word" data-w="calf">calf</button>
      <button class="bank-word" data-w="lamb">lamb</button>
      <button class="bank-word" data-w="duckling">duckling</button>
    </div>
    <div class="drag-text" data-group="babies">
      <div class="line-q"><span class="num">1</span><span>a baby dog is a <span class="drop-gap" data-ans="puppy">?</span></span></div>
      <div class="line-q"><span class="num">2</span><span>a baby cat is a <span class="drop-gap" data-ans="kitten">?</span></span></div>
      <div class="line-q"><span class="num">3</span><span>a baby chicken is a <span class="drop-gap" data-ans="chick">?</span></span></div>
      <div class="line-q"><span class="num">4</span><span>a baby rabbit is a <span class="drop-gap" data-ans="rabbit kit">?</span></span></div>
      <div class="line-q"><span class="num">5</span><span>a baby pig is a <span class="drop-gap" data-ans="piglet">?</span></span></div>
      <div class="line-q"><span class="num">6</span><span>a baby cow is a <span class="drop-gap" data-ans="calf">?</span></span></div>
      <div class="line-q"><span class="num">7</span><span>a baby sheep is a <span class="drop-gap" data-ans="lamb">?</span></span></div>
      <div class="line-q"><span class="num">8</span><span>a baby duck is a <span class="drop-gap" data-ans="duckling">?</span></span></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-babies">Check</button>
      <button class="btn-reset" data-reset="sec-babies">clear</button>
      <span class="score-pill" data-score-for="sec-babies">— / 8</span>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">🏠</span>
    <h3><span class="ex-num">V+.4</span> Pet shop items — pick the right word</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="cage"><div class="mc-q"><span class="num">1</span><span>You keep a hamster in a <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="bowl">bowl</button><button class="mc-opt" data-v="cage">cage</button><button class="mc-opt" data-v="leash">leash</button></div></div>
      <div class="mc-item" data-answer="bowl"><div class="mc-q"><span class="num">2</span><span>A dog eats from a <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="bowl">bowl</button><button class="mc-opt" data-v="collar">collar</button><button class="mc-opt" data-v="tank">tank</button></div></div>
      <div class="mc-item" data-answer="leash"><div class="mc-q"><span class="num">3</span><span>You walk a dog on a <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="collar">collar</button><button class="mc-opt" data-v="leash">leash</button><button class="mc-opt" data-v="toy">toy</button></div></div>
      <div class="mc-item" data-answer="tank"><div class="mc-q"><span class="num">4</span><span>Goldfish live in a <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="cage">cage</button><button class="mc-opt" data-v="tank">tank</button><button class="mc-opt" data-v="bowl">bowl</button></div></div>
      <div class="mc-item" data-answer="collar"><div class="mc-q"><span class="num">5</span><span>You put a <span class="gap-mini">?</span> around a dog's neck.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="leash">leash</button><button class="mc-opt" data-v="toy">toy</button><button class="mc-opt" data-v="collar">collar</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-petshop">Check</button>
      <span class="score-pill" data-score-for="sec-petshop">— / 5</span>
    </div>
  </div>
</section>

<!-- ===== VOCAB RECALL · Household chores (may-chores) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">V+</div>
    <h2>Vocab Recall · <em>Household chores</em></h2>
    <span class="tag">chores · verbs</span>
  </div>
  <div class="section-sub">The chores Julia and John help Mum with at home. Verbs + what goes with them.</div>
  <div class="card">
    <span class="ex-sticker">🧹</span>
    <h3><span class="ex-num">V+.5</span> Pick the right verb for each chore</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="wash"><div class="mc-q"><span class="num">1</span><span>I always <span class="gap-mini">?</span> the dishes after dinner.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="wash">wash</button><button class="mc-opt" data-v="feed">feed</button><button class="mc-opt" data-v="sweep">sweep</button></div></div>
      <div class="mc-item" data-answer="make"><div class="mc-q"><span class="num">2</span><span>Please <span class="gap-mini">?</span> your bed — it is a mess!</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="do">do</button><button class="mc-opt" data-v="make">make</button><button class="mc-opt" data-v="feed">feed</button></div></div>
      <div class="mc-item" data-answer="sweep"><div class="mc-q"><span class="num">3</span><span>Can you <span class="gap-mini">?</span> the floor, please?</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="sweep">sweep</button><button class="mc-opt" data-v="wash">wash</button><button class="mc-opt" data-v="cook">cook</button></div></div>
      <div class="mc-item" data-answer="take-out"><div class="mc-q"><span class="num">4</span><span>John, <span class="gap-mini">?</span> the rubbish, please!</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="take-out">take out</button><button class="mc-opt" data-v="dry">dry</button><button class="mc-opt" data-v="water">water</button></div></div>
      <div class="mc-item" data-answer="water"><div class="mc-q"><span class="num">5</span><span>Don't forget to <span class="gap-mini">?</span> the plants.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="feed">feed</button><button class="mc-opt" data-v="water">water</button><button class="mc-opt" data-v="sweep">sweep</button></div></div>
      <div class="mc-item" data-answer="feed"><div class="mc-q"><span class="num">6</span><span>Julia, time to <span class="gap-mini">?</span> Barsik — he is hungry!</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="feed">feed</button><button class="mc-opt" data-v="walk">walk</button><button class="mc-opt" data-v="tidy">tidy</button></div></div>
      <div class="mc-item" data-answer="tidy"><div class="mc-q"><span class="num">7</span><span>Please <span class="gap-mini">?</span> your room — your toys are everywhere.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="tidy">tidy</button><button class="mc-opt" data-v="cook">cook</button><button class="mc-opt" data-v="wash">wash</button></div></div>
      <div class="mc-item" data-answer="do"><div class="mc-q"><span class="num">8</span><span>Have you got time to <span class="gap-mini">?</span> your homework?</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="make">make</button><button class="mc-opt" data-v="do">do</button><button class="mc-opt" data-v="take">take</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-chores">Check</button>
      <span class="score-pill" data-score-for="sec-chores">— / 8</span>
    </div>
  </div>
</section>

<!-- ===== VOCAB RECALL · 9 Countries (flags-countries) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">V+</div>
    <h2>Vocab Recall · <em>9 Countries — flags, capitals, languages</em></h2>
    <span class="tag">world · nationalities</span>
  </div>
  <div class="section-sub">From your Flags &amp; Countries lesson. Remember these 9 countries you can talk about?</div>
  <div class="card">
    <span class="ex-sticker">🌍</span>
    <h3><span class="ex-num">V+.6</span> Match the country with its capital</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="paris"><div class="mc-q"><span class="num">1</span><span>The capital of France is <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="paris">Paris</button><button class="mc-opt" data-v="berlin">Berlin</button><button class="mc-opt" data-v="rome">Rome</button></div></div>
      <div class="mc-item" data-answer="rome"><div class="mc-q"><span class="num">2</span><span>The capital of Italy is <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="madrid">Madrid</button><button class="mc-opt" data-v="rome">Rome</button><button class="mc-opt" data-v="ankara">Ankara</button></div></div>
      <div class="mc-item" data-answer="tokyo"><div class="mc-q"><span class="num">3</span><span>The capital of Japan is <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="brasilia">Brasília</button><button class="mc-opt" data-v="tokyo">Tokyo</button><button class="mc-opt" data-v="moscow">Moscow</button></div></div>
      <div class="mc-item" data-answer="ankara"><div class="mc-q"><span class="num">4</span><span>The capital of Turkey is <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="istanbul">Istanbul</button><button class="mc-opt" data-v="ankara">Ankara</button><button class="mc-opt" data-v="madrid">Madrid</button></div></div>
      <div class="mc-item" data-answer="moscow"><div class="mc-q"><span class="num">5</span><span>The capital of Russia is <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="moscow">Moscow</button><button class="mc-opt" data-v="berlin">Berlin</button><button class="mc-opt" data-v="rome">Rome</button></div></div>
      <div class="mc-item" data-answer="canberra"><div class="mc-q"><span class="num">6</span><span>The capital of Australia is <span class="gap-mini">?</span></span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="sydney">Sydney</button><button class="mc-opt" data-v="canberra">Canberra</button><button class="mc-opt" data-v="tokyo">Tokyo</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-countries-capitals">Check</button>
      <span class="score-pill" data-score-for="sec-countries-capitals">— / 6</span>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">🗣</span>
    <h3><span class="ex-num">V+.7</span> Nationalities &amp; languages</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="french"><div class="mc-q"><span class="num">1</span><span>People in France are <span class="gap-mini">?</span> and they speak <strong>French</strong>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="french">French</button><button class="mc-opt" data-v="france">france</button><button class="mc-opt" data-v="paris">Paris</button></div></div>
      <div class="mc-item" data-answer="japanese"><div class="mc-q"><span class="num">2</span><span>People in Japan are <span class="gap-mini">?</span> and speak Japanese.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="japanese">Japanese</button><button class="mc-opt" data-v="japan">japan</button><button class="mc-opt" data-v="tokyo">tokyo</button></div></div>
      <div class="mc-item" data-answer="portuguese"><div class="mc-q"><span class="num">3</span><span>Brazilians speak <span class="gap-mini">?</span>, not Spanish!</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="brazilian">Brazilian</button><button class="mc-opt" data-v="spanish">Spanish</button><button class="mc-opt" data-v="portuguese">Portuguese</button></div></div>
      <div class="mc-item" data-answer="spanish"><div class="mc-q"><span class="num">4</span><span>In Spain people speak <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="spain">Spain</button><button class="mc-opt" data-v="spanish">Spanish</button><button class="mc-opt" data-v="english">English</button></div></div>
      <div class="mc-item" data-answer="german"><div class="mc-q"><span class="num">5</span><span>People in Germany speak <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="german">German</button><button class="mc-opt" data-v="dutch">Dutch</button><button class="mc-opt" data-v="english">English</button></div></div>
      <div class="mc-item" data-answer="english"><div class="mc-q"><span class="num">6</span><span>In Australia people speak <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="australian">Australian</button><button class="mc-opt" data-v="english">English</button><button class="mc-opt" data-v="german">German</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-nationalities">Check</button>
      <span class="score-pill" data-score-for="sec-nationalities">— / 6</span>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">💵</span>
    <h3><span class="ex-num">V+.8</span> Currencies — what do they pay with?</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="lira"><div class="mc-q"><span class="num">1</span><span>In Turkey people pay with <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="lira">lira</button><button class="mc-opt" data-v="euro">euro</button><button class="mc-opt" data-v="yen">yen</button></div></div>
      <div class="mc-item" data-answer="euro"><div class="mc-q"><span class="num">2</span><span>In France, Germany, Italy and Spain they use the <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="rouble">rouble</button><button class="mc-opt" data-v="euro">euro</button><button class="mc-opt" data-v="dollar">dollar</button></div></div>
      <div class="mc-item" data-answer="yen"><div class="mc-q"><span class="num">3</span><span>In Japan the currency is the <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="yen">yen</button><button class="mc-opt" data-v="real">real</button><button class="mc-opt" data-v="peso">peso</button></div></div>
      <div class="mc-item" data-answer="rouble"><div class="mc-q"><span class="num">4</span><span>In Russia people pay with the <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="rouble">rouble</button><button class="mc-opt" data-v="dollar">dollar</button><button class="mc-opt" data-v="yen">yen</button></div></div>
      <div class="mc-item" data-answer="real"><div class="mc-q"><span class="num">5</span><span>In Brazil the money is called the <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="real">real</button><button class="mc-opt" data-v="peso">peso</button><button class="mc-opt" data-v="dollar">dollar</button></div></div>
      <div class="mc-item" data-answer="dollar"><div class="mc-q"><span class="num">6</span><span>In Australia it's the Australian <span class="gap-mini">?</span>.</span></div>
        <div class="mc-opts"><button class="mc-opt" data-v="pound">pound</button><button class="mc-opt" data-v="dollar">dollar</button><button class="mc-opt" data-v="rand">rand</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-currencies">Check</button>
      <span class="score-pill" data-score-for="sec-currencies">— / 6</span>
    </div>
  </div>
</section>

"""

marker_vocab_close = '</div><!-- /tab-vocab -->'
assert text.count(marker_vocab_close) == 1
text = text.replace(marker_vocab_close, VOCAB_EXTRA + marker_vocab_close)

# ========================================================================
# GRAMMAR TAB — add Was/Were + Prepositions + Modals + Comparatives + Have got + Numbers
# ========================================================================

GRAMMAR_EXTRA = """
<!-- ===== GRAMMAR RECAP · Was / Were (recap-01) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Was / Were</em></h2>
    <span class="tag">Past of to be</span>
  </div>
  <div class="section-sub">The past form of am/is/are. Easy — just two forms.</div>
  <div class="card">
    <span class="ex-sticker">⏮</span>
    <h3><span class="ex-num">G+.1</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>Subject</th><th>Past of to be</th><th>Example</th></tr>
        <tr><td>I / he / she / it</td><td><code>was</code></td><td><em>I was at school. Barsik was happy.</em></td></tr>
        <tr><td>we / you / they</td><td><code>were</code></td><td><em>We were at the fair. The kittens were tiny.</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">Negative: <code>wasn't / weren't</code>. Question: <code>Was I…? Were they…?</code></div>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">✍</span>
    <h3><span class="ex-num">G+.2</span> Pick was or were</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="was"><div class="mc-q"><span class="num">1</span><span>Yesterday I <span class="gap-mini">?</span> at the fair with Mum.</span></div><div class="mc-opts"><button class="mc-opt" data-v="was">was</button><button class="mc-opt" data-v="were">were</button></div></div>
      <div class="mc-item" data-answer="were"><div class="mc-q"><span class="num">2</span><span>The six kittens <span class="gap-mini">?</span> grey and fluffy.</span></div><div class="mc-opts"><button class="mc-opt" data-v="was">was</button><button class="mc-opt" data-v="were">were</button></div></div>
      <div class="mc-item" data-answer="was"><div class="mc-q"><span class="num">3</span><span>John <span class="gap-mini">?</span> very excited to see the horses.</span></div><div class="mc-opts"><button class="mc-opt" data-v="was">was</button><button class="mc-opt" data-v="were">were</button></div></div>
      <div class="mc-item" data-answer="were"><div class="mc-q"><span class="num">4</span><span>Emma and I <span class="gap-mini">?</span> hungry after the ride.</span></div><div class="mc-opts"><button class="mc-opt" data-v="was">was</button><button class="mc-opt" data-v="were">were</button></div></div>
      <div class="mc-item" data-answer="was"><div class="mc-q"><span class="num">5</span><span>The queue <span class="gap-mini">?</span> very long.</span></div><div class="mc-opts"><button class="mc-opt" data-v="was">was</button><button class="mc-opt" data-v="were">were</button></div></div>
      <div class="mc-item" data-answer="werent"><div class="mc-q"><span class="num">6</span><span>Mrs. Pilsberry's kittens <span class="gap-mini">?</span> cheap at all!</span></div><div class="mc-opts"><button class="mc-opt" data-v="wasnt">wasn't</button><button class="mc-opt" data-v="werent">weren't</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-was-were">Check</button>
      <span class="score-pill" data-score-for="sec-was-were">— / 6</span>
    </div>
  </div>
</section>

<!-- ===== GRAMMAR RECAP · Prepositions of place (recap-01) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Prepositions of place</em></h2>
    <span class="tag">where?</span>
  </div>
  <div class="section-sub">The little words that say WHERE things are: in, on, under, next to, behind, in front of, between.</div>
  <div class="card">
    <span class="ex-sticker">📍</span>
    <h3><span class="ex-num">G+.3</span> Pick the right preposition</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="on"><div class="mc-q"><span class="num">1</span><span>Barsik is sitting <span class="gap-mini">?</span> the window sill.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="under">under</button></div></div>
      <div class="mc-item" data-answer="under"><div class="mc-q"><span class="num">2</span><span>John's shoe is <span class="gap-mini">?</span> the sofa.</span></div><div class="mc-opts"><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="under">under</button><button class="mc-opt" data-v="behind">behind</button></div></div>
      <div class="mc-item" data-answer="in"><div class="mc-q"><span class="num">3</span><span>The honey is <span class="gap-mini">?</span> the jar.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="at">at</button><button class="mc-opt" data-v="next to">next to</button></div></div>
      <div class="mc-item" data-answer="next to"><div class="mc-q"><span class="num">4</span><span>Emma is sitting <span class="gap-mini">?</span> Julia in class.</span></div><div class="mc-opts"><button class="mc-opt" data-v="between">between</button><button class="mc-opt" data-v="next to">next to</button><button class="mc-opt" data-v="under">under</button></div></div>
      <div class="mc-item" data-answer="behind"><div class="mc-q"><span class="num">5</span><span>Vova sits <span class="gap-mini">?</span> Julia and Emma — at the back.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in front of">in front of</button><button class="mc-opt" data-v="behind">behind</button><button class="mc-opt" data-v="on">on</button></div></div>
      <div class="mc-item" data-answer="in front of"><div class="mc-q"><span class="num">6</span><span>Mrs. Green stands <span class="gap-mini">?</span> the board.</span></div><div class="mc-opts"><button class="mc-opt" data-v="behind">behind</button><button class="mc-opt" data-v="in front of">in front of</button><button class="mc-opt" data-v="under">under</button></div></div>
      <div class="mc-item" data-answer="between"><div class="mc-q"><span class="num">7</span><span>Mum's car is parked <span class="gap-mini">?</span> two trees.</span></div><div class="mc-opts"><button class="mc-opt" data-v="between">between</button><button class="mc-opt" data-v="next to">next to</button><button class="mc-opt" data-v="on">on</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-prep-place">Check</button>
      <span class="score-pill" data-score-for="sec-prep-place">— / 7</span>
    </div>
  </div>
</section>

<!-- ===== GRAMMAR RECAP · Prepositions of time ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Prepositions of time — in / on / at</em></h2>
    <span class="tag">when?</span>
  </div>
  <div class="section-sub">3 little words, 3 clear rules.</div>
  <div class="card">
    <span class="ex-sticker">🕒</span>
    <h3><span class="ex-num">G+.4</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>at</th><td>time of the day</td><td><em>at 7 o'clock · at half past three · at night · at the weekend</em></td></tr>
        <tr><th>on</th><td>day / date</td><td><em>on Monday · on Friday · on 15 November · on her birthday</em></td></tr>
        <tr><th>in</th><td>month / season / year / part of the day</td><td><em>in November · in summer · in 2026 · in the morning</em></td></tr>
      </table>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">⏰</span>
    <h3><span class="ex-num">G+.5</span> Pick in / on / at</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="at"><div class="mc-q"><span class="num">1</span><span>Mum wakes me <span class="gap-mini">?</span> half past seven.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="at">at</button></div></div>
      <div class="mc-item" data-answer="on"><div class="mc-q"><span class="num">2</span><span>I have English <span class="gap-mini">?</span> Monday and Thursday.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="at">at</button></div></div>
      <div class="mc-item" data-answer="in"><div class="mc-q"><span class="num">3</span><span>Mum's birthday is <span class="gap-mini">?</span> November.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="at">at</button></div></div>
      <div class="mc-item" data-answer="on"><div class="mc-q"><span class="num">4</span><span>The fair is <span class="gap-mini">?</span> Sunday — don't be late!</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="at">at</button></div></div>
      <div class="mc-item" data-answer="in"><div class="mc-q"><span class="num">5</span><span>Barsik always sleeps <span class="gap-mini">?</span> the afternoon.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="at">at</button></div></div>
      <div class="mc-item" data-answer="at"><div class="mc-q"><span class="num">6</span><span><span class="gap-mini">?</span> night the city is quiet.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="at">at</button></div></div>
      <div class="mc-item" data-answer="in"><div class="mc-q"><span class="num">7</span><span>In Bodrum we went to the beach every day <span class="gap-mini">?</span> summer.</span></div><div class="mc-opts"><button class="mc-opt" data-v="in">in</button><button class="mc-opt" data-v="on">on</button><button class="mc-opt" data-v="at">at</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-prep-time">Check</button>
      <span class="score-pill" data-score-for="sec-prep-time">— / 7</span>
    </div>
  </div>
</section>

<!-- ===== GRAMMAR RECAP · Modal verbs CAN / MAY / MUST / SHOULD ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Modals — can, may, must, should</em></h2>
    <span class="tag">A2 → B1</span>
  </div>
  <div class="section-sub">Four modal verbs you already know (CAN, MAY) and two new ones (MUST, SHOULD).</div>
  <div class="card">
    <span class="ex-sticker">🔑</span>
    <h3><span class="ex-num">G+.6</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>can</th><td>ability / permission</td><td><em>I can swim. · Can I open the window?</em></td></tr>
        <tr><th>may</th><td>polite permission</td><td><em>May I come in? · May I have another pancake?</em></td></tr>
        <tr><th>must</th><td>strong rule (NEW)</td><td><em>You must wear a seat belt in the car.</em></td></tr>
        <tr><th>should</th><td>advice (NEW)</td><td><em>You should drink more water. It's good for you.</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">After every modal — the verb is BARE (no <code>to</code>, no <code>-s</code>): <code>she can swim</code>, not <em>she can to swims</em>.</div>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">💬</span>
    <h3><span class="ex-num">G+.7</span> Pick the right modal</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="can"><div class="mc-q"><span class="num">1</span><span>Julia <span class="gap-mini">?</span> speak English quite well.</span></div><div class="mc-opts"><button class="mc-opt" data-v="can">can</button><button class="mc-opt" data-v="must">must</button><button class="mc-opt" data-v="may">may</button></div></div>
      <div class="mc-item" data-answer="may"><div class="mc-q"><span class="num">2</span><span>Teacher, <span class="gap-mini">?</span> I go to the toilet, please?</span></div><div class="mc-opts"><button class="mc-opt" data-v="should">should</button><button class="mc-opt" data-v="may">may</button><button class="mc-opt" data-v="must">must</button></div></div>
      <div class="mc-item" data-answer="must"><div class="mc-q"><span class="num">3</span><span>You <span class="gap-mini">?</span> be quiet in the library — it's the rule.</span></div><div class="mc-opts"><button class="mc-opt" data-v="can">can</button><button class="mc-opt" data-v="may">may</button><button class="mc-opt" data-v="must">must</button></div></div>
      <div class="mc-item" data-answer="should"><div class="mc-q"><span class="num">4</span><span>You look tired. You <span class="gap-mini">?</span> go to bed earlier.</span></div><div class="mc-opts"><button class="mc-opt" data-v="should">should</button><button class="mc-opt" data-v="must">must</button><button class="mc-opt" data-v="can">can</button></div></div>
      <div class="mc-item" data-answer="can"><div class="mc-q"><span class="num">5</span><span>Barsik <span class="gap-mini">?</span> open the kitchen door with his paw. Clever cat!</span></div><div class="mc-opts"><button class="mc-opt" data-v="can">can</button><button class="mc-opt" data-v="should">should</button><button class="mc-opt" data-v="must">must</button></div></div>
      <div class="mc-item" data-answer="should"><div class="mc-q"><span class="num">6</span><span>John, you <span class="gap-mini">?</span> put your shoes near the door — then you won't lose them!</span></div><div class="mc-opts"><button class="mc-opt" data-v="should">should</button><button class="mc-opt" data-v="may">may</button><button class="mc-opt" data-v="must">must</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-modals">Check</button>
      <span class="score-pill" data-score-for="sec-modals">— / 6</span>
    </div>
  </div>
</section>

<!-- ===== GRAMMAR RECAP · Comparatives / Superlatives (animal-exhibition) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Comparatives &amp; Superlatives</em></h2>
    <span class="tag">bigger · the biggest</span>
  </div>
  <div class="section-sub">From the Animal Exhibition. Compare 2 things (bigger than) or 3+ (the biggest of all).</div>
  <div class="card">
    <span class="ex-sticker">📏</span>
    <h3><span class="ex-num">G+.8</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>Short adjective</th><td>+ <code>-er / -est</code></td><td><em>big → bigger → the biggest</em></td></tr>
        <tr><th>Long adjective</th><td><code>more / the most</code> + adj</td><td><em>beautiful → more beautiful → the most beautiful</em></td></tr>
        <tr><th>Irregular</th><td>—</td><td><em>good → better → the best · bad → worse → the worst</em></td></tr>
      </table>
    </div>
  </div>
  <div class="card">
    <span class="ex-sticker">🐘</span>
    <h3><span class="ex-num">G+.9</span> Compare the animals from the Exhibition</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="bigger"><div class="mc-q"><span class="num">1</span><span>The elephant is <span class="gap-mini">?</span> than the lion.</span></div><div class="mc-opts"><button class="mc-opt" data-v="bigger">bigger</button><button class="mc-opt" data-v="more big">more big</button><button class="mc-opt" data-v="the biggest">the biggest</button></div></div>
      <div class="mc-item" data-answer="the tallest"><div class="mc-q"><span class="num">2</span><span>The giraffe is <span class="gap-mini">?</span> animal in the zoo.</span></div><div class="mc-opts"><button class="mc-opt" data-v="taller">taller</button><button class="mc-opt" data-v="the tallest">the tallest</button><button class="mc-opt" data-v="more tall">more tall</button></div></div>
      <div class="mc-item" data-answer="more beautiful"><div class="mc-q"><span class="num">3</span><span>The peacock is <span class="gap-mini">?</span> than the pigeon.</span></div><div class="mc-opts"><button class="mc-opt" data-v="beautifuler">beautifuler</button><button class="mc-opt" data-v="more beautiful">more beautiful</button><button class="mc-opt" data-v="most beautiful">most beautiful</button></div></div>
      <div class="mc-item" data-answer="the most interesting"><div class="mc-q"><span class="num">4</span><span>For John the carousel was <span class="gap-mini">?</span> thing at the fair.</span></div><div class="mc-opts"><button class="mc-opt" data-v="more interesting">more interesting</button><button class="mc-opt" data-v="the most interesting">the most interesting</button><button class="mc-opt" data-v="interestinger">interestinger</button></div></div>
      <div class="mc-item" data-answer="better"><div class="mc-q"><span class="num">5</span><span>Mum's pancakes are <span class="gap-mini">?</span> than the shop ones.</span></div><div class="mc-opts"><button class="mc-opt" data-v="gooder">gooder</button><button class="mc-opt" data-v="better">better</button><button class="mc-opt" data-v="more good">more good</button></div></div>
      <div class="mc-item" data-answer="the best"><div class="mc-q"><span class="num">6</span><span>Barsik thinks HE is <span class="gap-mini">?</span> cat in the whole world.</span></div><div class="mc-opts"><button class="mc-opt" data-v="the best">the best</button><button class="mc-opt" data-v="the goodest">the goodest</button><button class="mc-opt" data-v="better">better</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-compar">Check</button>
      <span class="score-pill" data-score-for="sec-compar">— / 6</span>
    </div>
  </div>
</section>

<!-- ===== GRAMMAR RECAP · Have got / Has got ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Have got / Has got</em></h2>
    <span class="tag">possession</span>
  </div>
  <div class="section-sub">The way British kids say "I have…" — have got / has got.</div>
  <div class="card">
    <span class="ex-sticker">👜</span>
    <h3><span class="ex-num">G+.10</span> Pick have got or has got</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="has got"><div class="mc-q"><span class="num">1</span><span>Barsik <span class="gap-mini">?</span> golden-green eyes.</span></div><div class="mc-opts"><button class="mc-opt" data-v="have got">have got</button><button class="mc-opt" data-v="has got">has got</button></div></div>
      <div class="mc-item" data-answer="have got"><div class="mc-q"><span class="num">2</span><span>Julia and John <span class="gap-mini">?</span> brown hair.</span></div><div class="mc-opts"><button class="mc-opt" data-v="have got">have got</button><button class="mc-opt" data-v="has got">has got</button></div></div>
      <div class="mc-item" data-answer="has got"><div class="mc-q"><span class="num">3</span><span>Mum <span class="gap-mini">?</span> long wavy brown hair.</span></div><div class="mc-opts"><button class="mc-opt" data-v="have got">have got</button><button class="mc-opt" data-v="has got">has got</button></div></div>
      <div class="mc-item" data-answer="have got"><div class="mc-q"><span class="num">4</span><span>I <span class="gap-mini">?</span> three friends in my class.</span></div><div class="mc-opts"><button class="mc-opt" data-v="have got">have got</button><button class="mc-opt" data-v="has got">has got</button></div></div>
      <div class="mc-item" data-answer="havent got"><div class="mc-q"><span class="num">5</span><span>We <span class="gap-mini">?</span> a dog, but we've got a cat.</span></div><div class="mc-opts"><button class="mc-opt" data-v="hasnt got">hasn't got</button><button class="mc-opt" data-v="havent got">haven't got</button></div></div>
      <div class="mc-item" data-answer="has got"><div class="mc-q"><span class="num">6</span><span>Mrs. Pilsberry <span class="gap-mini">?</span> six beautiful kittens.</span></div><div class="mc-opts"><button class="mc-opt" data-v="have got">have got</button><button class="mc-opt" data-v="has got">has got</button></div></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-havegot">Check</button>
      <span class="score-pill" data-score-for="sec-havegot">— / 6</span>
    </div>
  </div>
</section>

<!-- ===== GRAMMAR RECAP · Numbers &amp; Ordinals (bodrum) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">G+</div>
    <h2>Grammar · <em>Ordinal numbers — 1st, 2nd, 3rd …</em></h2>
    <span class="tag">numbers</span>
  </div>
  <div class="section-sub">Numbers for order (not count): first, second, third… tenth.</div>
  <div class="card">
    <span class="ex-sticker">🏅</span>
    <h3><span class="ex-num">G+.11</span> Match the number with the ordinal</h3>
    <div class="input-list">
      <div class="input-row"><span class="num">1</span><div class="prompt">1 → <b>?</b></div><input type="text" data-ans="first" placeholder="1 → …"></div>
      <div class="input-row"><span class="num">2</span><div class="prompt">2 → <b>?</b></div><input type="text" data-ans="second" placeholder="2 → …"></div>
      <div class="input-row"><span class="num">3</span><div class="prompt">3 → <b>?</b></div><input type="text" data-ans="third" placeholder="3 → …"></div>
      <div class="input-row"><span class="num">4</span><div class="prompt">4 → <b>?</b></div><input type="text" data-ans="fourth" placeholder="4 → …"></div>
      <div class="input-row"><span class="num">5</span><div class="prompt">5 → <b>?</b></div><input type="text" data-ans="fifth" placeholder="5 → …"></div>
      <div class="input-row"><span class="num">6</span><div class="prompt">8 → <b>?</b></div><input type="text" data-ans="eighth" placeholder="8 → …"></div>
      <div class="input-row"><span class="num">7</span><div class="prompt">9 → <b>?</b></div><input type="text" data-ans="ninth" placeholder="9 → …"></div>
      <div class="input-row"><span class="num">8</span><div class="prompt">10 → <b>?</b></div><input type="text" data-ans="tenth" placeholder="10 → …"></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-ordinals">Check</button>
      <button class="btn-reset" data-reset="sec-ordinals">clear</button>
      <span class="score-pill" data-score-for="sec-ordinals">— / 8</span>
    </div>
  </div>
</section>

"""

marker_grammar_close = '</div><!-- /tab-grammar -->'
assert text.count(marker_grammar_close) == 1
text = text.replace(marker_grammar_close, GRAMMAR_EXTRA + marker_grammar_close)

# ========================================================================
# WORKBOOK TAB — add MEGA irregular verbs grid (40 verbs)
# ========================================================================

WORKBOOK_EXTRA = """
<!-- ===== WORKBOOK · MEGA Irregular Verbs grid (irregular-verbs lesson) ===== -->
<section class="section">
  <div class="section-hdr">
    <div class="num">W+</div>
    <h2>Workbook · <em>MEGA Irregular Verbs grid — 40 verbs</em></h2>
    <span class="tag">type V2</span>
  </div>
  <div class="section-sub">All the irregular verbs you learned in the Bakery Story lesson — type the Past Simple form. Lowercase.</div>
  <div class="card">
    <span class="ex-sticker">🔀</span>
    <h3><span class="ex-num">W+.1</span> Type the Past Simple of each verb</h3>
    <div class="input-list">
      <div class="input-row"><span class="num">1</span><div class="prompt">be (I/he/she) → <b>?</b></div><input type="text" data-ans="was"></div>
      <div class="input-row"><span class="num">2</span><div class="prompt">be (we/you/they) → <b>?</b></div><input type="text" data-ans="were"></div>
      <div class="input-row"><span class="num">3</span><div class="prompt">have → <b>?</b></div><input type="text" data-ans="had"></div>
      <div class="input-row"><span class="num">4</span><div class="prompt">do → <b>?</b></div><input type="text" data-ans="did"></div>
      <div class="input-row"><span class="num">5</span><div class="prompt">go → <b>?</b></div><input type="text" data-ans="went"></div>
      <div class="input-row"><span class="num">6</span><div class="prompt">come → <b>?</b></div><input type="text" data-ans="came"></div>
      <div class="input-row"><span class="num">7</span><div class="prompt">see → <b>?</b></div><input type="text" data-ans="saw"></div>
      <div class="input-row"><span class="num">8</span><div class="prompt">eat → <b>?</b></div><input type="text" data-ans="ate"></div>
      <div class="input-row"><span class="num">9</span><div class="prompt">drink → <b>?</b></div><input type="text" data-ans="drank"></div>
      <div class="input-row"><span class="num">10</span><div class="prompt">run → <b>?</b></div><input type="text" data-ans="ran"></div>
      <div class="input-row"><span class="num">11</span><div class="prompt">sit → <b>?</b></div><input type="text" data-ans="sat"></div>
      <div class="input-row"><span class="num">12</span><div class="prompt">stand → <b>?</b></div><input type="text" data-ans="stood"></div>
      <div class="input-row"><span class="num">13</span><div class="prompt">swim → <b>?</b></div><input type="text" data-ans="swam"></div>
      <div class="input-row"><span class="num">14</span><div class="prompt">sing → <b>?</b></div><input type="text" data-ans="sang"></div>
      <div class="input-row"><span class="num">15</span><div class="prompt">take → <b>?</b></div><input type="text" data-ans="took"></div>
      <div class="input-row"><span class="num">16</span><div class="prompt">give → <b>?</b></div><input type="text" data-ans="gave"></div>
      <div class="input-row"><span class="num">17</span><div class="prompt">make → <b>?</b></div><input type="text" data-ans="made"></div>
      <div class="input-row"><span class="num">18</span><div class="prompt">get → <b>?</b></div><input type="text" data-ans="got"></div>
      <div class="input-row"><span class="num">19</span><div class="prompt">find → <b>?</b></div><input type="text" data-ans="found"></div>
      <div class="input-row"><span class="num">20</span><div class="prompt">buy → <b>?</b></div><input type="text" data-ans="bought"></div>
      <div class="input-row"><span class="num">21</span><div class="prompt">bring → <b>?</b></div><input type="text" data-ans="brought"></div>
      <div class="input-row"><span class="num">22</span><div class="prompt">think → <b>?</b></div><input type="text" data-ans="thought"></div>
      <div class="input-row"><span class="num">23</span><div class="prompt">teach → <b>?</b></div><input type="text" data-ans="taught"></div>
      <div class="input-row"><span class="num">24</span><div class="prompt">catch → <b>?</b></div><input type="text" data-ans="caught"></div>
      <div class="input-row"><span class="num">25</span><div class="prompt">win → <b>?</b></div><input type="text" data-ans="won"></div>
      <div class="input-row"><span class="num">26</span><div class="prompt">lose → <b>?</b></div><input type="text" data-ans="lost"></div>
      <div class="input-row"><span class="num">27</span><div class="prompt">leave → <b>?</b></div><input type="text" data-ans="left"</div></div>
      <div class="input-row"><span class="num">28</span><div class="prompt">feel → <b>?</b></div><input type="text" data-ans="felt"></div>
      <div class="input-row"><span class="num">29</span><div class="prompt">meet → <b>?</b></div><input type="text" data-ans="met"></div>
      <div class="input-row"><span class="num">30</span><div class="prompt">sleep → <b>?</b></div><input type="text" data-ans="slept"></div>
      <div class="input-row"><span class="num">31</span><div class="prompt">keep → <b>?</b></div><input type="text" data-ans="kept"></div>
      <div class="input-row"><span class="num">32</span><div class="prompt">read → <b>?</b></div><input type="text" data-ans="read"></div>
      <div class="input-row"><span class="num">33</span><div class="prompt">write → <b>?</b></div><input type="text" data-ans="wrote"></div>
      <div class="input-row"><span class="num">34</span><div class="prompt">speak → <b>?</b></div><input type="text" data-ans="spoke"></div>
      <div class="input-row"><span class="num">35</span><div class="prompt">break → <b>?</b></div><input type="text" data-ans="broke"></div>
      <div class="input-row"><span class="num">36</span><div class="prompt">wear → <b>?</b></div><input type="text" data-ans="wore"></div>
      <div class="input-row"><span class="num">37</span><div class="prompt">grow → <b>?</b></div><input type="text" data-ans="grew"></div>
      <div class="input-row"><span class="num">38</span><div class="prompt">know → <b>?</b></div><input type="text" data-ans="knew"></div>
      <div class="input-row"><span class="num">39</span><div class="prompt">forget → <b>?</b></div><input type="text" data-ans="forgot"></div>
      <div class="input-row"><span class="num">40</span><div class="prompt">tell → <b>?</b></div><input type="text" data-ans="told"></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-mega-irreg">Check all 40</button>
      <button class="btn-reset" data-reset="sec-mega-irreg">clear</button>
      <span class="score-pill" data-score-for="sec-mega-irreg">— / 40</span>
    </div>
  </div>
</section>

"""

marker_workbook_close = '</div><!-- /tab-workbook -->'
assert text.count(marker_workbook_close) == 1
text = text.replace(marker_workbook_close, WORKBOOK_EXTRA + marker_workbook_close)

HTML.write_text(text, encoding="utf-8")
print(f"Done: expanded recap. File size: {len(text)} chars.")
