"""Add 5 advanced future-tense blocks between Chapter 4 and Chapter 5.

Blocks (A2 → B1 progression):
  5.5 — Present Continuous for FIXED FUTURE arrangements (I'm meeting Emma at 5 tomorrow)
  5.6 — Future TIME CLAUSES (no 'will' after when/as soon as/until/if)
  5.7 — Shall / Shall we... (polite suggestions)
  5.8 — Be about to + V (immediate future)
  5.9 — Future Continuous intro (will be + V-ing)

Also extends Mixed Future Quest from 10 to 16 Qs.
"""
import pathlib
HERE = pathlib.Path(__file__).parent
HTML = HERE / "index.html"
text = HTML.read_text(encoding="utf-8")

FUTURE_BLOCKS = """
<!-- ===== 5.5 · PRESENT CONTINUOUS FOR FIXED FUTURE ===== -->
<section class="section" id="sec-05b">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>Present Continuous for arrangements</em></h2>
    <span class="tag new">PCont for future · A2 → B1</span>
  </div>
  <div class="section-sub">A fixed plan with a date and a time — use <code>am/is/are + V-ing</code>, not <code>will</code>.</div>

  <div class="card">
    <span class="ex-sticker">📅</span>
    <h3><span class="ex-num">5.5</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>will</th><td>a prediction / a wish</td><td><em>I think it <strong>will rain</strong>.</em></td></tr>
        <tr><th>going to</th><td>a decided plan</td><td><em>We <strong>are going to</strong> buy more soap.</em></td></tr>
        <tr><th>Present Continuous</th><td>a FIXED arrangement — with a time or a person</td><td><em>I <strong>am meeting</strong> Emma at 5 tomorrow.</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">💡 If there is a specific time + a specific person — Present Continuous feels most natural.</div>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">✍</span>
    <h3><span class="ex-num">5.5a</span> Pick the right form</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="am-meeting"><div class="mc-q"><span class="num">1</span><span>I <span class="gap-mini">?</span> Emma at the park at 4 o'clock tomorrow.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-meet">will meet</button><button class="mc-opt" data-v="am-meeting">am meeting</button><button class="mc-opt" data-v="meet">meet</button></div></div>
      <div class="mc-item" data-answer="is-coming"><div class="mc-q"><span class="num">2</span><span>Mum <span class="gap-mini">?</span> back from work at 6 — don't be late!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-come">will come</button><button class="mc-opt" data-v="is-coming">is coming</button><button class="mc-opt" data-v="comes">comes</button></div></div>
      <div class="mc-item" data-answer="will-rain"><div class="mc-q"><span class="num">3</span><span>I think it <span class="gap-mini">?</span> tomorrow — no outdoor bubbles! <em style="color:var(--muted);font-size:.85em">(prediction, not a plan)</em></span></div><div class="mc-opts"><button class="mc-opt" data-v="is-raining">is raining</button><button class="mc-opt" data-v="will-rain">will rain</button><button class="mc-opt" data-v="rains">rains</button></div></div>
      <div class="mc-item" data-answer="are-flying"><div class="mc-q"><span class="num">4</span><span>Next summer we <span class="gap-mini">?</span> to Bodrum. The tickets are already booked!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-fly">will fly</button><button class="mc-opt" data-v="are-flying">are flying</button><button class="mc-opt" data-v="fly">fly</button></div></div>
      <div class="mc-item" data-answer="is-having"><div class="mc-q"><span class="num">5</span><span>John <span class="gap-mini">?</span> his birthday party on Saturday at 3 — he already made the invitations!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-have">will have</button><button class="mc-opt" data-v="is-having">is having</button><button class="mc-opt" data-v="has">has</button></div></div>
      <div class="mc-item" data-answer="am-staying"><div class="mc-q"><span class="num">6</span><span>I <span class="gap-mini">?</span> at Emma's flat this Friday night — Mum already said yes.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-stay">will stay</button><button class="mc-opt" data-v="am-staying">am staying</button><button class="mc-opt" data-v="stay">stay</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05b-pc">Check</button><span class="score-pill" data-score-for="sec-05b-pc">— / 6</span></div>
  </div>
</section>

<!-- ===== 5.6 · FUTURE TIME CLAUSES (no WILL after when / as soon as / until / if) ===== -->
<section class="section" id="sec-05c">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>when, as soon as, until, before, after</em></h2>
    <span class="tag new">time clauses</span>
  </div>
  <div class="section-sub">⚠️ After <code>when / as soon as / before / after / until / if</code> — use PRESENT, even if the meaning is future.</div>

  <div class="card">
    <span class="ex-sticker">⏳</span>
    <h3><span class="ex-num">5.6</span> Mini-theory · the trap</h3>
    <div class="theory">
      <div class="rule">
        ❌ <em>When I <strong>will grow</strong> up, I will travel to London.</em><br>
        ✅ <em>When I <strong>grow</strong> up, I will travel to London.</em><br><br>
        Same rule for: <code>as soon as</code>, <code>before</code>, <code>after</code>, <code>until</code>, <code>if</code>.<br>
        One <strong>will</strong> only — in the MAIN clause. The TIME clause uses Present Simple.
      </div>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">🌱</span>
    <h3><span class="ex-num">5.6a</span> Pick the right verb form</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="grow"><div class="mc-q"><span class="num">1</span><span>When I <span class="gap-mini">?</span> up, I will open a bubble shop.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-grow">will grow</button><button class="mc-opt" data-v="grow">grow</button><button class="mc-opt" data-v="am-growing">am growing</button></div></div>
      <div class="mc-item" data-answer="get-home"><div class="mc-q"><span class="num">2</span><span>I will call you as soon as I <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-get-home">will get home</button><button class="mc-opt" data-v="get-home">get home</button><button class="mc-opt" data-v="am-getting-home">am getting home</button></div></div>
      <div class="mc-item" data-answer="is"><div class="mc-q"><span class="num">3</span><span>If the wind <span class="gap-mini">?</span> strong tomorrow, our bubbles will burst fast.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-be">will be</button><button class="mc-opt" data-v="is">is</button><button class="mc-opt" data-v="was">was</button></div></div>
      <div class="mc-item" data-answer="finishes"><div class="mc-q"><span class="num">4</span><span>John will play when he <span class="gap-mini">?</span> his homework.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-finish">will finish</button><button class="mc-opt" data-v="finishes">finishes</button><button class="mc-opt" data-v="finished">finished</button></div></div>
      <div class="mc-item" data-answer="stops"><div class="mc-q"><span class="num">5</span><span>Barsik won't come out until the storm <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-stop">will stop</button><button class="mc-opt" data-v="stops">stops</button><button class="mc-opt" data-v="stopped">stopped</button></div></div>
      <div class="mc-item" data-answer="arrives"><div class="mc-q"><span class="num">6</span><span>Before Emma <span class="gap-mini">?</span>, we will make a big batch of mixture.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-arrive">will arrive</button><button class="mc-opt" data-v="arrives">arrives</button><button class="mc-opt" data-v="arriving">arriving</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05c-tc">Check</button><span class="score-pill" data-score-for="sec-05c-tc">— / 6</span></div>
  </div>
</section>

<!-- ===== 5.7 · SHALL / Shall we... (polite suggestions) ===== -->
<section class="section" id="sec-05d">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>Shall I…? / Shall we…?</em></h2>
    <span class="tag">polite suggestion</span>
  </div>
  <div class="section-sub">British way to offer help or suggest something together. Only with <code>I</code> and <code>we</code>.</div>

  <div class="card">
    <span class="ex-sticker">🤝</span>
    <h3><span class="ex-num">5.7</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>Shall I…?</th><td>I offer help</td><td><em>Shall I open the window?</em></td></tr>
        <tr><th>Shall we…?</th><td>I suggest doing something together</td><td><em>Shall we go to the park?</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">Only with I / we. Not with he / she / they. Mostly British English.</div>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">💁‍♀️</span>
    <h3><span class="ex-num">5.7a</span> Pick the right suggestion</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="shall-i"><div class="mc-q"><span class="num">1</span><span>You look tired. <span class="gap-mini">?</span> make you a cup of tea?</span></div><div class="mc-opts"><button class="mc-opt" data-v="shall-i">Shall I</button><button class="mc-opt" data-v="shall-we">Shall we</button><button class="mc-opt" data-v="shall-they">Shall they</button></div></div>
      <div class="mc-item" data-answer="shall-we"><div class="mc-q"><span class="num">2</span><span>It's a beautiful day. <span class="gap-mini">?</span> go to the park with the big ring?</span></div><div class="mc-opts"><button class="mc-opt" data-v="shall-i">Shall I</button><button class="mc-opt" data-v="shall-we">Shall we</button><button class="mc-opt" data-v="shall-he">Shall he</button></div></div>
      <div class="mc-item" data-answer="shall-i"><div class="mc-q"><span class="num">3</span><span>Mum, <span class="gap-mini">?</span> help you with the dishes?</span></div><div class="mc-opts"><button class="mc-opt" data-v="shall-she">Shall she</button><button class="mc-opt" data-v="shall-i">Shall I</button><button class="mc-opt" data-v="shall-they">Shall they</button></div></div>
      <div class="mc-item" data-answer="shall-we"><div class="mc-q"><span class="num">4</span><span>Emma, <span class="gap-mini">?</span> start the bubble workshop at 3?</span></div><div class="mc-opts"><button class="mc-opt" data-v="shall-you">Shall you</button><button class="mc-opt" data-v="shall-they">Shall they</button><button class="mc-opt" data-v="shall-we">Shall we</button></div></div>
      <div class="mc-item" data-answer="shall-i"><div class="mc-q"><span class="num">5</span><span>Barsik is sleeping. <span class="gap-mini">?</span> close the door quietly?</span></div><div class="mc-opts"><button class="mc-opt" data-v="shall-i">Shall I</button><button class="mc-opt" data-v="shall-she">Shall she</button><button class="mc-opt" data-v="shall-he">Shall he</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05d-shall">Check</button><span class="score-pill" data-score-for="sec-05d-shall">— / 5</span></div>
  </div>
</section>

<!-- ===== 5.8 · BE ABOUT TO (immediate future) ===== -->
<section class="section" id="sec-05e">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>be about to + V</em></h2>
    <span class="tag">right now · immediate</span>
  </div>
  <div class="section-sub">Something is going to happen in the next few seconds. <code>am/is/are + about to + V</code>.</div>

  <div class="card">
    <span class="ex-sticker">⚡</span>
    <h3><span class="ex-num">5.8</span> Mini-theory</h3>
    <div class="theory">
      <div class="rule"><strong>be about to + V</strong> = immediate future (right now, this second).<br>
      <em>I <strong>am about to blow</strong> the biggest bubble ever — watch!</em><br>
      <em>The bubble <strong>is about to pop</strong> — look at that wobble!</em><br>
      <em>We <strong>are about to leave</strong> — put your shoes on, John!</em></div>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">💥</span>
    <h3><span class="ex-num">5.8a</span> Pick the right form</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="am-about-to"><div class="mc-q"><span class="num">1</span><span>Quiet! I <span class="gap-mini">?</span> blow the giant bubble!</span></div><div class="mc-opts"><button class="mc-opt" data-v="am-about-to">am about to</button><button class="mc-opt" data-v="was-about-to">was about to</button><button class="mc-opt" data-v="will-about-to">will about to</button></div></div>
      <div class="mc-item" data-answer="is-about-to"><div class="mc-q"><span class="num">2</span><span>Watch out — that bubble <span class="gap-mini">?</span> pop any second!</span></div><div class="mc-opts"><button class="mc-opt" data-v="are-about-to">are about to</button><button class="mc-opt" data-v="is-about-to">is about to</button><button class="mc-opt" data-v="was-about-to">was about to</button></div></div>
      <div class="mc-item" data-answer="are-about-to"><div class="mc-q"><span class="num">3</span><span>Hurry up, John! We <span class="gap-mini">?</span> leave the house!</span></div><div class="mc-opts"><button class="mc-opt" data-v="is-about-to">is about to</button><button class="mc-opt" data-v="are-about-to">are about to</button><button class="mc-opt" data-v="will-about-to">will about to</button></div></div>
      <div class="mc-item" data-answer="was-about-to"><div class="mc-q"><span class="num">4</span><span>I <span class="gap-mini">?</span> blow the bubble when Barsik jumped on the table! <em style="color:var(--muted);font-size:.85em">(past)</em></span></div><div class="mc-opts"><button class="mc-opt" data-v="was-about-to">was about to</button><button class="mc-opt" data-v="am-about-to">am about to</button><button class="mc-opt" data-v="will-about-to">will about to</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05e-about">Check</button><span class="score-pill" data-score-for="sec-05e-about">— / 4</span></div>
  </div>
</section>

<!-- ===== 5.9 · FUTURE CONTINUOUS intro (will be + V-ing) ===== -->
<section class="section" id="sec-05f">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>will be + V-ing · Future Continuous</em></h2>
    <span class="tag new">B1 bridge</span>
  </div>
  <div class="section-sub">A long action that will be IN PROGRESS at a specific future moment. "This time tomorrow I will be flying…"</div>

  <div class="card">
    <span class="ex-sticker">🚀</span>
    <h3><span class="ex-num">5.9</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>will</th><td>a short action in the future</td><td><em>Tomorrow I <strong>will fly</strong> to London.</em></td></tr>
        <tr><th>will be + V-ing</th><td>a long action AT a point in the future</td><td><em>This time tomorrow I <strong>will be flying</strong> over the clouds.</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">Use with time pointers: <code>this time tomorrow / next week / at 5pm on Friday</code>.</div>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">🪐</span>
    <h3><span class="ex-num">5.9a</span> Pick will + V or will be + V-ing</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="will-be-sleeping"><div class="mc-q"><span class="num">1</span><span>This time tomorrow I <span class="gap-mini">?</span> on Emma's sofa — pyjama party!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-sleep">will sleep</button><button class="mc-opt" data-v="will-be-sleeping">will be sleeping</button><button class="mc-opt" data-v="am-sleeping">am sleeping</button></div></div>
      <div class="mc-item" data-answer="will-be-blowing"><div class="mc-q"><span class="num">2</span><span>At 4pm on Saturday we <span class="gap-mini">?</span> giant bubbles in the park with Emma.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-blow">will blow</button><button class="mc-opt" data-v="will-be-blowing">will be blowing</button><button class="mc-opt" data-v="blow">blow</button></div></div>
      <div class="mc-item" data-answer="will-fly"><div class="mc-q"><span class="num">3</span><span>I think I <span class="gap-mini">?</span> to London one day. (just a prediction, not an exact moment)</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-fly">will fly</button><button class="mc-opt" data-v="will-be-flying">will be flying</button><button class="mc-opt" data-v="am-flying">am flying</button></div></div>
      <div class="mc-item" data-answer="will-be-studying"><div class="mc-q"><span class="num">4</span><span>Next year this time, John <span class="gap-mini">?</span> in the 2nd grade.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-study">will study</button><button class="mc-opt" data-v="will-be-studying">will be studying</button><button class="mc-opt" data-v="studies">studies</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05f-fc">Check</button><span class="score-pill" data-score-for="sec-05f-fc">— / 4</span></div>
  </div>
</section>

<!-- ===== 5.X · FUTURE TIME MARKERS (vocab for future) ===== -->
<section class="section" id="sec-05g">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>time words for the future</em></h2>
    <span class="tag">time markers · vocab</span>
  </div>
  <div class="section-sub">Little words that tell you WHEN something will happen.</div>

  <div class="card">
    <span class="ex-sticker">⏭</span>
    <h3><span class="ex-num">5.X</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>soon</th><td>in a short time</td><td><em>I will come back soon.</em></td></tr>
        <tr><th>tomorrow</th><td>the next day</td><td><em>Tomorrow we will blow bubbles.</em></td></tr>
        <tr><th>next (week/month/year)</th><td>following period</td><td><em>Next week we are going to Bodrum.</em></td></tr>
        <tr><th>in (10 minutes / an hour / a week)</th><td>after that amount of time</td><td><em>In ten minutes the mixture will be ready.</em></td></tr>
        <tr><th>by (Friday / 2030)</th><td>not later than</td><td><em>By Friday we will have the giant ring.</em></td></tr>
        <tr><th>one day / someday</th><td>at some point in the future</td><td><em>One day my wish will come true.</em></td></tr>
      </table>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">🗓</span>
    <h3><span class="ex-num">5.X.a</span> Fill in the right time marker</h3>
    <div class="bank" id="bank-time">
      <button class="bank-word" data-w="tomorrow">tomorrow</button>
      <button class="bank-word" data-w="next week">next week</button>
      <button class="bank-word" data-w="in ten minutes">in ten minutes</button>
      <button class="bank-word" data-w="by Friday">by Friday</button>
      <button class="bank-word" data-w="one day">one day</button>
      <button class="bank-word" data-w="soon">soon</button>
    </div>
    <div class="drag-text" data-group="time">
      <div class="line-q"><span class="num">1</span><span>The bubble mixture will be ready <span class="drop-gap" data-ans="in ten minutes">?</span>.</span></div>
      <div class="line-q"><span class="num">2</span><span><span class="drop-gap" data-ans="tomorrow">?</span> at 4 pm, Julia is meeting Emma in the park.</span></div>
      <div class="line-q"><span class="num">3</span><span>I will finish the big bubble recipe <span class="drop-gap" data-ans="by Friday">?</span> — Mum's birthday is on Saturday.</span></div>
      <div class="line-q"><span class="num">4</span><span><span class="drop-gap" data-ans="one day">?</span> I will travel to London and see Big Ben.</span></div>
      <div class="line-q"><span class="num">5</span><span>Mum, don't worry, I will be home <span class="drop-gap" data-ans="soon">?</span>!</span></div>
      <div class="line-q"><span class="num">6</span><span><span class="drop-gap" data-ans="next week">?</span> we are going to buy more glycerin and dish soap.</span></div>
    </div>
    <div class="check-row">
      <button class="btn-check" data-check="sec-05g-time">Check</button>
      <button class="btn-reset" data-reset="sec-05g-time">clear</button>
      <span class="score-pill" data-score-for="sec-05g-time">— / 6</span>
    </div>
  </div>
</section>

"""

FUTURE_BLOCKS_PART2 = """
<!-- ===== 5.Y · PRESENT SIMPLE for schedules (timetables, flights) ===== -->
<section class="section" id="sec-05h">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>Present Simple for schedules</em></h2>
    <span class="tag">timetable future</span>
  </div>
  <div class="section-sub">For fixed schedules (trains, planes, lessons, films) — use Present Simple, not will.</div>

  <div class="card">
    <span class="ex-sticker">🕒</span>
    <h3><span class="ex-num">5.Y</span> Mini-theory</h3>
    <div class="theory">
      <div class="rule">For things on a FIXED timetable (schedules you can look up):<br>
      <em>The train <strong>leaves</strong> at 7:40 tomorrow.</em><br>
      <em>Our flight to Bodrum <strong>takes off</strong> at 6:15 am.</em><br>
      <em>The English lesson <strong>starts</strong> at 5 pm.</em><br>
      ⚠️ Not for personal plans — only for scheduled events.</div>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">✈</span>
    <h3><span class="ex-num">5.Y.a</span> Pick the right form</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="leaves"><div class="mc-q"><span class="num">1</span><span>The train to Grandma's village <span class="gap-mini">?</span> at 7:40 tomorrow morning.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-leave">will leave</button><button class="mc-opt" data-v="leaves">leaves</button><button class="mc-opt" data-v="is-leaving">is leaving</button></div></div>
      <div class="mc-item" data-answer="starts"><div class="mc-q"><span class="num">2</span><span>The film <span class="gap-mini">?</span> at 6 — don't be late!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-start">will start</button><button class="mc-opt" data-v="starts">starts</button><button class="mc-opt" data-v="is-starting">is starting</button></div></div>
      <div class="mc-item" data-answer="opens"><div class="mc-q"><span class="num">3</span><span>The Pink Café <span class="gap-mini">?</span> at 10 am every Saturday.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-open">will open</button><button class="mc-opt" data-v="opens">opens</button><button class="mc-opt" data-v="is-opening">is opening</button></div></div>
      <div class="mc-item" data-answer="arrives"><div class="mc-q"><span class="num">4</span><span>Our flight to Bodrum <span class="gap-mini">?</span> in Antalya at 11 am.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-arrive">will arrive</button><button class="mc-opts"><button class="mc-opt" data-v="arrives">arrives</button><button class="mc-opt" data-v="is-arriving">is arriving</button></div></div>
      <div class="mc-item" data-answer="finishes"><div class="mc-q"><span class="num">5</span><span>School <span class="gap-mini">?</span> at 2:15 on Fridays.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-finish">will finish</button><button class="mc-opt" data-v="finishes">finishes</button><button class="mc-opt" data-v="is-finishing">is finishing</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05h-ps">Check</button><span class="score-pill" data-score-for="sec-05h-ps">— / 5</span></div>
  </div>
</section>

<!-- ===== 5.Z · WOULD LIKE / WOULD LOVE / HOPE / WANT (expressing wishes) ===== -->
<section class="section" id="sec-05i">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>I'd like to… / I'd love to… / I hope…</em></h2>
    <span class="tag">wishes · lexis</span>
  </div>
  <div class="section-sub">Softer, politer ways to talk about what you want in the future.</div>

  <div class="card">
    <span class="ex-sticker">💭</span>
    <h3><span class="ex-num">5.Z</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>I want to…</th><td>direct, strong</td><td><em>I want to travel to London.</em></td></tr>
        <tr><th>I'd like to…</th><td>polite, softer (= I would like to)</td><td><em>I'd like to see Big Ben.</em></td></tr>
        <tr><th>I'd love to…</th><td>enthusiastic / dreamy</td><td><em>I'd love to open a bubble shop!</em></td></tr>
        <tr><th>I hope to…</th><td>wish + plan</td><td><em>I hope to visit Grandma this winter.</em></td></tr>
        <tr><th>I'm thinking of + V-ing</th><td>idea in your head</td><td><em>I'm thinking of baking a cake for Mum.</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">All of these point at the future — but with different flavours.</div>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">🌟</span>
    <h3><span class="ex-num">5.Z.a</span> Match the feeling to the sentence</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="id-love-to"><div class="mc-q"><span class="num">1</span><span>Open a bubble shop with Emma! That's my dream! → <span class="gap-mini">?</span></span></div><div class="mc-opts"><button class="mc-opt" data-v="want-to">I want to</button><button class="mc-opt" data-v="id-love-to">I'd love to</button><button class="mc-opt" data-v="hope-to">I hope to</button></div></div>
      <div class="mc-item" data-answer="id-like-to"><div class="mc-q"><span class="num">2</span><span>Polite request to Mum: <span class="gap-mini">?</span> have one more pancake, please.</span></div><div class="mc-opts"><button class="mc-opt" data-v="i-want-to">I want to</button><button class="mc-opt" data-v="id-like-to">I'd like to</button><button class="mc-opt" data-v="im-thinking-of">I'm thinking of</button></div></div>
      <div class="mc-item" data-answer="hope-to"><div class="mc-q"><span class="num">3</span><span>Maybe this winter: <span class="gap-mini">?</span> visit Grandma in her village.</span></div><div class="mc-opts"><button class="mc-opt" data-v="id-love-to">I'd love to</button><button class="mc-opt" data-v="hope-to">I hope to</button><button class="mc-opt" data-v="want-to">I want to</button></div></div>
      <div class="mc-item" data-answer="thinking-of"><div class="mc-q"><span class="num">4</span><span>Idea in my head, not decided yet: I'm <span class="gap-mini">?</span> making a bubble cake.</span></div><div class="mc-opts"><button class="mc-opt" data-v="thinking-of">thinking of</button><button class="mc-opt" data-v="going-to">going to</button><button class="mc-opt" data-v="about-to">about to</button></div></div>
      <div class="mc-item" data-answer="would-love-to"><div class="mc-q"><span class="num">5</span><span>— Would you like to come to my party? — Yes, I <span class="gap-mini">?</span>!</span></div><div class="mc-opts"><button class="mc-opt" data-v="am-loving">am loving</button><button class="mc-opt" data-v="would-love-to">would love to</button><button class="mc-opt" data-v="will-love">will love</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05i-wishes">Check</button><span class="score-pill" data-score-for="sec-05i-wishes">— / 5</span></div>
  </div>
</section>

<!-- ===== 5.W · FUTURE PERFECT intro (will have + V3) ===== -->
<section class="section" id="sec-05j">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Toolkit · <em>will have + V3 · Future Perfect</em></h2>
    <span class="tag new">B1+ bridge</span>
  </div>
  <div class="section-sub">Something that WILL BE finished BEFORE a certain future point. "By 2030 I will have travelled to 10 countries."</div>

  <div class="card">
    <span class="ex-sticker">🏁</span>
    <h3><span class="ex-num">5.W</span> Mini-theory</h3>
    <div class="theory">
      <table>
        <tr><th>Future Simple</th><td><code>will + V</code></td><td><em>I will travel.</em></td></tr>
        <tr><th>Future Continuous</th><td><code>will be + V-ing</code></td><td><em>I will be travelling.</em></td></tr>
        <tr><th>Future Perfect</th><td><code>will have + V3</code></td><td><em>I will have travelled.</em></td></tr>
      </table>
      <div class="rule" style="margin-top:8px">Use for things that will be ALREADY DONE by a future moment. Keywords: <code>by 2030 / by Christmas / by next summer</code>.</div>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">🌅</span>
    <h3><span class="ex-num">5.W.a</span> Pick Future Simple or Future Perfect</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="will-have-travelled"><div class="mc-q"><span class="num">1</span><span>By my 25th birthday, I <span class="gap-mini">?</span> to ten countries.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-travel">will travel</button><button class="mc-opt" data-v="will-have-travelled">will have travelled</button><button class="mc-opt" data-v="am-travelling">am travelling</button></div></div>
      <div class="mc-item" data-answer="will-have-finished"><div class="mc-q"><span class="num">2</span><span>By 6 pm Julia <span class="gap-mini">?</span> all her homework.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-finish">will finish</button><button class="mc-opt" data-v="will-have-finished">will have finished</button><button class="mc-opt" data-v="is-finishing">is finishing</button></div></div>
      <div class="mc-item" data-answer="will-make"><div class="mc-q"><span class="num">3</span><span>Tomorrow after school I <span class="gap-mini">?</span> a huge bubble! (just a simple future action)</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-make">will make</button><button class="mc-opt" data-v="will-have-made">will have made</button><button class="mc-opt" data-v="am-making">am making</button></div></div>
      <div class="mc-item" data-answer="will-have-grown"><div class="mc-q"><span class="num">4</span><span>By next summer John <span class="gap-mini">?</span> ten centimetres!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-grow">will grow</button><button class="mc-opt" data-v="will-have-grown">will have grown</button><button class="mc-opt" data-v="grows">grows</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05j-fp">Check</button><span class="score-pill" data-score-for="sec-05j-fp">— / 4</span></div>
  </div>
</section>

<!-- ===== 5.Ω · FUTURE MEGA QUEST · all 10 ways mixed ===== -->
<section class="section" id="sec-05k">
  <div class="section-hdr">
    <div class="num">5·</div>
    <h2>Future Mega Quest · <em>all 10 ways in one quiz</em></h2>
    <span class="tag new">boss level · 16 Qs</span>
  </div>
  <div class="section-sub">10 ways to talk about the future, 16 mixed questions. Think carefully WHICH flavour of future we need.</div>

  <div class="card">
    <span class="ex-sticker">🏆</span>
    <h3><span class="ex-num">5.Ω</span> Mini-theory · the whole FUTURE toolbox</h3>
    <div class="theory">
      <table>
        <tr><th>1. will</th><td>wish / prediction / promise / decision now</td><td><em>I will travel to London.</em></td></tr>
        <tr><th>2. going to</th><td>decided plan</td><td><em>We are going to buy soap.</em></td></tr>
        <tr><th>3. Present Continuous</th><td>fixed arrangement (time + person)</td><td><em>I'm meeting Emma at 5.</em></td></tr>
        <tr><th>4. Present Simple</th><td>schedule / timetable</td><td><em>The train leaves at 7:40.</em></td></tr>
        <tr><th>5. If…, will…</th><td>first conditional</td><td><em>If it rains, we will stay in.</em></td></tr>
        <tr><th>6. When/as soon as + Pr.S.</th><td>time clause → no will here</td><td><em>When I grow up, I will…</em></td></tr>
        <tr><th>7. Shall I/we…?</th><td>polite offer / suggestion</td><td><em>Shall we go to the park?</em></td></tr>
        <tr><th>8. be about to + V</th><td>immediate (seconds away)</td><td><em>I am about to blow.</em></td></tr>
        <tr><th>9. will be + V-ing</th><td>in progress at a future point</td><td><em>At 5 we will be blowing.</em></td></tr>
        <tr><th>10. will have + V3</th><td>finished BEFORE a future point</td><td><em>By June I will have finished.</em></td></tr>
      </table>
    </div>
  </div>

  <div class="card">
    <span class="ex-sticker">🎯</span>
    <h3><span class="ex-num">5.Ω.a</span> Mega mixed quiz · 16 questions</h3>
    <div class="mc-list">
      <div class="mc-item" data-answer="am-going-to"><div class="mc-q"><span class="num">1</span><span>I already told Emma — after school we <span class="gap-mini">?</span> blow bubbles. (planned)</span></div><div class="mc-opts"><button class="mc-opt" data-v="will">will</button><button class="mc-opt" data-v="am-going-to">am going to</button><button class="mc-opt" data-v="might">might</button></div></div>
      <div class="mc-item" data-answer="is-meeting"><div class="mc-q"><span class="num">2</span><span>Mum <span class="gap-mini">?</span> Aunt Anya at 4pm tomorrow — tea at her flat.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-meet">will meet</button><button class="mc-opt" data-v="is-meeting">is meeting</button><button class="mc-opt" data-v="meets">meets</button></div></div>
      <div class="mc-item" data-answer="leaves"><div class="mc-q"><span class="num">3</span><span>Our train <span class="gap-mini">?</span> at 7:40 am — don't oversleep!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-leave">will leave</button><button class="mc-opt" data-v="leaves">leaves</button><button class="mc-opt" data-v="is-leaving">is leaving</button></div></div>
      <div class="mc-item" data-answer="will-pop"><div class="mc-q"><span class="num">4</span><span>If Barsik touches the bubble, it <span class="gap-mini">?</span>.</span></div><div class="mc-opts"><button class="mc-opt" data-v="pops">pops</button><button class="mc-opt" data-v="will-pop">will pop</button><button class="mc-opt" data-v="is-popping">is popping</button></div></div>
      <div class="mc-item" data-answer="grow"><div class="mc-q"><span class="num">5</span><span>When I <span class="gap-mini">?</span> up, I will open an art studio.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-grow">will grow</button><button class="mc-opt" data-v="grow">grow</button><button class="mc-opt" data-v="am-growing">am growing</button></div></div>
      <div class="mc-item" data-answer="shall-we"><div class="mc-q"><span class="num">6</span><span><span class="gap-mini">?</span> make another batch of bubble mixture?</span></div><div class="mc-opts"><button class="mc-opt" data-v="shall-we">Shall we</button><button class="mc-opt" data-v="will-we">Will we</button><button class="mc-opt" data-v="are-we">Are we</button></div></div>
      <div class="mc-item" data-answer="am-about-to"><div class="mc-q"><span class="num">7</span><span>Shhhh! I <span class="gap-mini">?</span> blow the biggest bubble ever — right now!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will">will</button><button class="mc-opt" data-v="am-about-to">am about to</button><button class="mc-opt" data-v="am-going-to">am going to</button></div></div>
      <div class="mc-item" data-answer="will-be-flying"><div class="mc-q"><span class="num">8</span><span>This time next week I <span class="gap-mini">?</span> to Bodrum!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-fly">will fly</button><button class="mc-opt" data-v="will-be-flying">will be flying</button><button class="mc-opt" data-v="am-flying">am flying</button></div></div>
      <div class="mc-item" data-answer="will-have-finished"><div class="mc-q"><span class="num">9</span><span>By 8pm I <span class="gap-mini">?</span> all my homework.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-finish">will finish</button><button class="mc-opt" data-v="will-have-finished">will have finished</button><button class="mc-opt" data-v="am-finishing">am finishing</button></div></div>
      <div class="mc-item" data-answer="might"><div class="mc-q"><span class="num">10</span><span>Maybe one day I <span class="gap-mini">?</span> be an inventor — I'm not sure yet.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will">will</button><button class="mc-opt" data-v="might">might</button><button class="mc-opt" data-v="am-going-to">am going to</button></div></div>
      <div class="mc-item" data-answer="id-love-to"><div class="mc-q"><span class="num">11</span><span>— Will you come to the park? — Yes, I <span class="gap-mini">?</span>!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-love">will love</button><button class="mc-opt" data-v="id-love-to">I'd love to</button><button class="mc-opt" data-v="am-loving">am loving</button></div></div>
      <div class="mc-item" data-answer="will"><div class="mc-q"><span class="num">12</span><span>— The bowl is heavy! — Don't worry, I <span class="gap-mini">?</span> carry it. (decision this second)</span></div><div class="mc-opts"><button class="mc-opt" data-v="will">will</button><button class="mc-opt" data-v="am-going-to">am going to</button><button class="mc-opt" data-v="am-about-to">am about to</button></div></div>
      <div class="mc-item" data-answer="arrives"><div class="mc-q"><span class="num">13</span><span>As soon as Emma <span class="gap-mini">?</span>, we will start the bubble workshop.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will-arrive">will arrive</button><button class="mc-opt" data-v="arrives">arrives</button><button class="mc-opt" data-v="is-arriving">is arriving</button></div></div>
      <div class="mc-item" data-answer="is-going-to"><div class="mc-q"><span class="num">14</span><span>Look at those dark clouds! It <span class="gap-mini">?</span> rain — we see it coming.</span></div><div class="mc-opts"><button class="mc-opt" data-v="will">will</button><button class="mc-opt" data-v="is-going-to">is going to</button><button class="mc-opt" data-v="might">might</button></div></div>
      <div class="mc-item" data-answer="shall-i"><div class="mc-q"><span class="num">15</span><span>Mum, <span class="gap-mini">?</span> make you a cup of tea?</span></div><div class="mc-opts"><button class="mc-opt" data-v="shall-i">Shall I</button><button class="mc-opt" data-v="will-i">Will I</button><button class="mc-opt" data-v="am-i">Am I</button></div></div>
      <div class="mc-item" data-answer="is-about-to"><div class="mc-q"><span class="num">16</span><span>Watch out — that giant bubble <span class="gap-mini">?</span> pop any second!</span></div><div class="mc-opts"><button class="mc-opt" data-v="will">will</button><button class="mc-opt" data-v="is-about-to">is about to</button><button class="mc-opt" data-v="is-going-to">is going to</button></div></div>
    </div>
    <div class="check-row"><button class="btn-check" data-check="sec-05k-mega">Check my mega score</button><span class="score-pill" data-score-for="sec-05k-mega">— / 16</span></div>
  </div>
</section>

"""

anchor = "<!-- ===== 6 · CHAPTER 5 · SUNSET WISHES · MIGHT / COULD ===== -->"
assert text.count(anchor) == 1, "anchor Chapter 5 not found"
text = text.replace(anchor, FUTURE_BLOCKS + FUTURE_BLOCKS_PART2 + anchor)

HTML.write_text(text, encoding="utf-8")
print(f"Done: 9 Future Toolkit blocks inserted. File size: {len(text)} chars.")
