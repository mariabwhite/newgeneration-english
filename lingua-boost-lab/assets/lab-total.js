/* lab-total.js — universal Lesson total + CEFR mapping for any Lab lesson.
   Injects the total block at the end of <main> or before <footer>, then
   recounts on every click/input. Heuristic counting across many exercise
   class conventions (matched, correct, right, lit, picked, etc).
   Drop-in: <script src="../../assets/lab-total.js" defer></script>
*/
(function(){
  'use strict';

  function injectBlock(){
    if (document.getElementById('lab-total-block')) return;
    var anchor = document.querySelector('footer') || document.body.lastElementChild;
    var sec = document.createElement('section');
    sec.id = 'lab-total-block';
    sec.style.cssText = 'width:min(100% - 48px, 1320px);margin:32px auto;padding:0 clamp(16px,3vw,28px);font-family:system-ui,sans-serif';
    sec.innerHTML = ''
      + '<div style="background:color-mix(in srgb, var(--accent, #fbbf24) 10%, transparent);border:1px solid color-mix(in srgb, var(--accent, #fbbf24) 35%, transparent);border-radius:14px;padding:18px 22px;text-align:center;color:var(--text,#f3eee5)">'
      +   '<div style="font-family:monospace;font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;color:var(--accent, #fbbf24);font-weight:800;margin-bottom:10px">Lesson score · total</div>'
      +   '<div style="font-weight:900;font-size:2.4rem;color:var(--text,#fff);line-height:1"><span id="lab-total-val">0</span><span style="opacity:.55;font-size:1.4rem;font-weight:700"> / <span id="lab-total-max">0</span></span></div>'
      +   '<div style="font-family:monospace;font-size:.74rem;opacity:.55;margin-top:6px;letter-spacing:.1em">auto-scored · saved in this browser</div>'
      + '</div>'
      + '<div style="margin-top:12px;display:grid;grid-template-columns:1fr 1fr;gap:12px">'
      +   '<div style="background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:12px 16px;text-align:center;color:var(--text,#f3eee5)">'
      +     '<div style="font-family:monospace;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accent, #fbbf24);font-weight:800;margin-bottom:6px">Band score</div>'
      +     '<div style="font-weight:900;font-size:1.6rem;color:var(--text,#fff);line-height:1"><span id="lab-cefr-band">—</span></div>'
      +     '<div style="font-family:monospace;font-size:.66rem;opacity:.55;margin-top:4px">1–6 scale</div>'
      +   '</div>'
      +   '<div style="background:color-mix(in srgb, var(--accent, #fbbf24) 10%, transparent);border:1px solid color-mix(in srgb, var(--accent, #fbbf24) 35%, transparent);border-radius:10px;padding:12px 16px;text-align:center;color:var(--text,#f3eee5)">'
      +     '<div style="font-family:monospace;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--accent, #fbbf24);font-weight:800;margin-bottom:6px">CEFR level</div>'
      +     '<div style="font-weight:900;font-size:1.6rem;color:var(--accent, #fbbf24);line-height:1"><span id="lab-cefr-level">—</span></div>'
      +     '<div style="font-family:monospace;font-size:.66rem;opacity:.55;margin-top:4px">auto-derived</div>'
      +   '</div>'
      + '</div>';
    anchor.parentNode.insertBefore(sec, anchor);
  }

  function recount(){
    var sum = 0;
    sum += document.querySelectorAll('.matched, .match-card.matched').length;
    sum += document.querySelectorAll('.mcq-opts button.right, .mcq-opts button.correct').length;
    sum += document.querySelectorAll('.mc-opts button.right, .mc-opts button.correct, .tfg-opts button.right, .tfg-opts button.correct').length;
    sum += document.querySelectorAll('.cloze-opts button.right, .cloze-opts button.correct').length;
    sum += document.querySelectorAll('.gap-input.correct, .gap-input.right, .gap.correct, .gap.right, .gapfill input.correct').length;
    sum += document.querySelectorAll('.wf-in.right, .wf-in.correct, .oc-in.right, .oc-in.correct, .tr-in.right, .tr-in.correct, .byo-row input.right, .byo-row input.correct').length;
    sum += document.querySelectorAll('.tf-btn.right, .tf-btn.correct').length;
    sum += document.querySelectorAll('.choice.right, .choice.correct, .mc-opt.right, .mc-opt.correct').length;
    sum += document.querySelectorAll('.detective-pill.right, .detective-pill.picked.correct').length;
    sum += document.querySelectorAll('select.mcq.correct').length;
    // Builder is binary — count via status
    sum += document.querySelectorAll('.builder-status.ok').length;
    // Mic-drill matches
    sum += document.querySelectorAll('.mic-feedback.shown:not(.miss)').length;
    // Vocab flips
    sum += document.querySelectorAll('.vocab-card.flipped, .vocab-card.played').length;
    // Tutor inputs
    document.querySelectorAll('.tutor-input').forEach(function(inp){
      var v = parseFloat(inp.value); if (Number.isFinite(v)) sum += v;
    });

    var targets = 0;
    targets += document.querySelectorAll('.mcq-row').length;
    targets += document.querySelectorAll('.mc-row, .tfg-row, .cloze-row').length;
    targets += document.querySelectorAll('.gap-input').length;
    targets += document.querySelectorAll('.gapfill input').length;
    targets += document.querySelectorAll('.wf-in, .oc-in, .tr-in, .byo-row input').length;
    targets += (document.querySelectorAll('.match-card').length / 2 | 0);
    targets += document.querySelectorAll('.tf-q, .tf-item').length;
    targets += document.querySelectorAll('.detective-pill').length;
    targets += document.querySelectorAll('select.mcq').length;
    targets += document.querySelectorAll('.choice-row').length;
    targets += document.querySelectorAll('.mic-row').length;
    targets += document.querySelectorAll('.vocab-card').length;
    targets += document.querySelectorAll('.tutor-input').length * 5; // tutor max 5
    targets += document.querySelectorAll('.builder').length;

    var total = Math.max(targets, 1);
    var capped = Math.min(sum, total);
    var valEl = document.getElementById('lab-total-val');
    var maxEl = document.getElementById('lab-total-max');
    if (valEl) valEl.textContent = capped;
    if (maxEl) maxEl.textContent = total;

    var pct = total > 0 ? capped / total : 0;
    var band = '—', level = '—';
    if (capped > 0) {
      if      (pct >= 0.95) { band = '6';   level = 'C2'; }
      else if (pct >= 0.85) { band = '5.5'; level = 'C1'; }
      else if (pct >= 0.75) { band = '5';   level = 'C1'; }
      else if (pct >= 0.65) { band = '4.5'; level = 'B2'; }
      else if (pct >= 0.55) { band = '4';   level = 'B2'; }
      else if (pct >= 0.45) { band = '3.5'; level = 'B1'; }
      else if (pct >= 0.35) { band = '3';   level = 'B1'; }
      else if (pct >= 0.25) { band = '2.5'; level = 'A2'; }
      else if (pct >= 0.15) { band = '2';   level = 'A2'; }
      else if (pct >= 0.08) { band = '1.5'; level = 'A1'; }
      else                  { band = '1';   level = 'A1'; }
    }
    var bandEl = document.getElementById('lab-cefr-band');
    var lvlEl = document.getElementById('lab-cefr-level');
    if (bandEl) bandEl.textContent = band;
    if (lvlEl) lvlEl.textContent = level;
  }

  function onReady(){
    setTimeout(function(){
      injectBlock();
      document.addEventListener('click', function(){ setTimeout(recount, 60); }, true);
      document.addEventListener('input', function(){ setTimeout(recount, 60); }, true);
      setTimeout(recount, 600);
      setTimeout(recount, 1800);
    }, 350);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
  } else {
    onReady();
  }
})();
