/* lab-mic-wpm.js — universal WPM (words per minute) meter for any mic-drill.
   Wraps any existing `.mic-row` (data-target="...") with a WPM annotation
   in the .mic-feedback span. Idempotent — won't double-wrap.
   Drop-in: <script src="../../assets/lab-mic-wpm.js" defer></script>
   Norm: B1+ adult English speech 130-160 WPM. Below 100 = slow, above 180 = fast. */
(function(){
  if (window.__labMicWpmLoaded) return;
  window.__labMicWpmLoaded = true;

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function wpmLabel(wpm){
    if (wpm < 100) return wpm+' WPM · можно быстрее (норма 130-160)';
    if (wpm <= 170) return wpm+' WPM · норма (130-160)';
    return wpm+' WPM · быстро (норма 130-160)';
  }

  ready(function(){
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return; // browser without Web Speech — nothing to do

    document.querySelectorAll('.mic-row').forEach(function(row){
      if (row.__wpmEnhanced) return;
      row.__wpmEnhanced = true;

      var btn = row.querySelector('.mic-btn, button[class*="mic"]');
      var fb  = row.querySelector('.mic-feedback');
      var tr  = row.querySelector('.mic-transcript');
      if (!btn) return;

      // Hook into the click handler — wrap rec start
      var t0 = 0;
      var origAdd = btn.addEventListener.bind(btn);
      // We can't intercept old listeners cleanly, so use MutationObserver
      // approach: watch fb textContent for `Match`/`Close`/`Missed` patterns
      // and inject WPM after them. That's lesson-handler agnostic.
      if (fb) {
        var lastSeen = '';
        var mo = new MutationObserver(function(){
          var txt = fb.textContent || '';
          if (!txt || txt === lastSeen) return;
          lastSeen = txt;
          // Skip if already has WPM
          if (/WPM/.test(txt)) return;
          // Only annotate when there's a match score
          if (!/Match|Close|Missed/i.test(txt) && !/✓|~|✗/.test(txt)) return;

          var transcript = (tr && tr.textContent ? tr.textContent : '').replace(/^"|"$/g,'').trim();
          var words = (transcript.match(/\S+/g) || []).length;
          if (words < 2) return;

          // Use row.dataset.wpm if lesson already computed it
          var wpm = parseInt(row.dataset.wpm || '0', 10);
          if (!wpm) {
            // Fallback: estimate from transcript word count + assumed 4s duration
            // (we don't have start time post-hoc, so estimate conservatively)
            var assumedSec = Math.max(2, words * 0.5);
            wpm = Math.round(words / assumedSec * 60);
          }
          fb.textContent = txt + ' · ' + wpmLabel(wpm);
        });
        mo.observe(fb, { childList: true, characterData: true, subtree: true });
      }

      // Time the recognition more accurately: monkey-patch start if possible
      var origClick = null;
      btn.addEventListener('click', function(){
        t0 = Date.now();
        // After ~3s, expected results — capture and compute
        setTimeout(function captureWpm(){
          var transcript = (tr && tr.textContent ? tr.textContent : '').replace(/^"|"$/g,'').trim();
          var words = (transcript.match(/\S+/g) || []).length;
          if (words >= 2 && !row.dataset.wpm) {
            var dt = Math.max(0.5, (Date.now() - t0) / 1000);
            var wpm = Math.round(words / dt * 60);
            row.dataset.wpm = wpm;
            row.dataset.attempted = '1';
            // Re-trigger MutationObserver by appending invisible char to fb
            if (fb && fb.textContent && !/WPM/.test(fb.textContent)) {
              fb.textContent = fb.textContent + ' · ' + wpmLabel(wpm);
            }
          }
        }, 4500);
      }, true); // capture phase, before lesson handler
    });
  });
})();
