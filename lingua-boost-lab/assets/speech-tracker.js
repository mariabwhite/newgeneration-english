/* speech-tracker.js — drop-in recording + WPM + benchmark widget for Lab lessons.
   Usage:
     <div class="speech-tracker" data-mode="olympiad" data-max-sec="120"
          data-title="Mock IELTS Part 2 · 2 min monologue"></div>
     <script src="path-to/speech-tracker.js" defer></script>

   Modes: olympiad · ielts · oge · conversational
   Uses Web Speech Recognition (Chrome / Edge). Falls back to a notice in Firefox/Safari.
   No external deps.
*/
(function(){
  'use strict';

  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  var BENCHMARKS = {
    olympiad:       { min: 120, max: 160, label: 'Olympiad · B2+' },
    ielts:          { min: 110, max: 160, label: 'IELTS Speaking' },
    oge:            { min:  95, max: 135, label: 'ОГЭ Speaking' },
    conversational: { min: 100, max: 150, label: 'Conversational' }
  };

  var CSS = [
    '.speech-tracker{background:linear-gradient(135deg,rgba(160,127,255,.10),rgba(217,70,160,.06));border:2px solid rgba(160,127,255,.32);border-radius:14px;padding:18px 22px;margin:18px 0;font-family:"Manrope",system-ui,sans-serif;color:inherit}',
    '.speech-tracker h3.st-title{margin:0 0 12px;font-family:"Unbounded","Manrope",sans-serif;font-size:1.04rem;font-weight:800;letter-spacing:-.01em}',
    '.st-eyebrow{display:inline-block;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:.66rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#A07FFF;background:rgba(160,127,255,.14);padding:3px 10px;border-radius:5px;margin-bottom:6px}',
    '.st-top{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:12px}',
    '.st-mic{background:#9B7FE8;color:#fff;border:none;border-radius:8px;padding:9px 18px;font-family:"JetBrains Mono",ui-monospace,monospace;font-weight:800;letter-spacing:.06em;font-size:.78rem;text-transform:uppercase;cursor:pointer;transition:transform .12s}',
    '.st-mic:hover{transform:translateY(-1px)}',
    '.st-mic.recording{background:#D946A0;animation:st-pulse 1.2s infinite}',
    '@keyframes st-pulse{0%,100%{box-shadow:0 0 0 0 rgba(217,70,160,.42)}50%{box-shadow:0 0 0 8px rgba(217,70,160,0)}}',
    '.st-timer{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:1.1rem;font-weight:900;color:#A07FFF;min-width:140px;text-align:center;background:rgba(160,127,255,.08);border:1px solid rgba(160,127,255,.25);border-radius:6px;padding:4px 10px}',
    '.st-mode{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:.68rem;letter-spacing:.1em;color:#A07FFF;font-weight:700;opacity:.85}',
    '.st-meters{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:12px}',
    '.st-meter{background:rgba(160,127,255,.08);border:1px solid rgba(160,127,255,.22);border-radius:10px;padding:9px 14px;text-align:center}',
    '.st-meter .st-label{display:block;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:.62rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(160,127,255,.85);margin-bottom:4px;font-weight:800}',
    '.st-meter .st-value{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:1.5rem;font-weight:900;color:inherit}',
    '.st-wpm.ok{color:#5B8C5A}',
    '.st-wpm.low{color:#D58A2C}',
    '.st-wpm.high{color:#B14545}',
    '.st-transcript{background:rgba(0,0,0,.06);border:1px dashed rgba(160,127,255,.3);border-radius:8px;padding:10px 14px;min-height:60px;font-size:.94rem;line-height:1.55;margin-bottom:10px}',
    '.st-transcript:empty::before{content:"Your speech will appear here as text — try a full 1–2 minute answer."; opacity:.55;font-style:italic;font-size:.88rem}',
    '.st-verdict{font-family:"Playfair Display","Times New Roman",serif;font-style:italic;font-size:1.02rem;padding:10px 14px;background:rgba(160,127,255,.08);border-left:3px solid #A07FFF;border-radius:0 8px 8px 0}',
    '.st-verdict:empty{padding:0;border:0;background:none}',
    '.st-note{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:.7rem;letter-spacing:.06em;color:rgba(160,127,255,.85);margin-top:8px}'
  ].join('');

  function injectStyle(){
    if (document.getElementById('speech-tracker-css')) return;
    var s = document.createElement('style');
    s.id = 'speech-tracker-css';
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function fmt(s){
    s = Math.max(0, Math.round(s));
    var m = Math.floor(s/60), r = s%60;
    return m + ':' + (r<10 ? '0' : '') + r;
  }
  function countWords(s){
    return ((s||'').trim().match(/\b[\w'-]+\b/g) || []).length;
  }

  function mount(el){
    if (el.dataset.mounted) return;
    el.dataset.mounted = '1';

    var mode = el.dataset.mode || 'conversational';
    var maxSec = parseInt(el.dataset.maxSec || '120', 10);
    var title = el.dataset.title || 'Recording &amp; speed tracker';
    var bench = BENCHMARKS[mode] || BENCHMARKS.conversational;

    el.innerHTML =
      '<span class="st-eyebrow">🎤 Speech Tracker</span>' +
      '<h3 class="st-title">' + title + '</h3>' +
      '<div class="st-top">' +
        '<button class="st-mic" type="button">🎤 Start recording</button>' +
        '<span class="st-timer">0:00 / ' + fmt(maxSec) + '</span>' +
        '<span class="st-mode">' + bench.label + ' · target ' + bench.min + '-' + bench.max + ' WPM</span>' +
      '</div>' +
      '<div class="st-meters">' +
        '<div class="st-meter"><span class="st-label">Words</span><span class="st-value st-words">0</span></div>' +
        '<div class="st-meter"><span class="st-label">WPM</span><span class="st-value st-wpm">—</span></div>' +
      '</div>' +
      '<div class="st-transcript"></div>' +
      '<div class="st-verdict"></div>' +
      '<div class="st-note">Chrome / Edge только. Можно записывать несколько раз — каждый run перезаписывает.</div>';

    var micBtn      = el.querySelector('.st-mic');
    var timerEl     = el.querySelector('.st-timer');
    var wordsEl     = el.querySelector('.st-words');
    var wpmEl       = el.querySelector('.st-wpm');
    var transcript  = el.querySelector('.st-transcript');
    var verdictEl   = el.querySelector('.st-verdict');

    var rec = null;
    var recording = false;
    var startTime = 0;
    var timerInt  = null;
    var finalText = '';
    var interimText = '';

    function update(){
      var full = (finalText + ' ' + interimText).trim();
      var w = countWords(full);
      var elapsedSec = (Date.now() - startTime)/1000;
      var elapsedMin = elapsedSec/60;
      var wpm = elapsedMin > 0.08 ? Math.round(w / elapsedMin) : null;

      wordsEl.textContent = w;
      wpmEl.textContent = (wpm == null ? '—' : wpm);
      timerEl.textContent = fmt(elapsedSec) + ' / ' + fmt(maxSec);
      transcript.textContent = full;

      wpmEl.className = 'st-value st-wpm';
      if (wpm != null) {
        if (wpm < bench.min) wpmEl.classList.add('low');
        else if (wpm > bench.max) wpmEl.classList.add('high');
        else wpmEl.classList.add('ok');
      }
    }

    function stop(){
      if (!recording) return;
      recording = false;
      try { rec.stop(); } catch(_) {}
      clearInterval(timerInt);
      micBtn.textContent = '🎤 Record again';
      micBtn.classList.remove('recording');

      var full = (finalText + ' ' + interimText).trim();
      var w = countWords(full);
      var elapsedSec = Math.max(0.001, (Date.now() - startTime)/1000);
      var wpm = elapsedSec > 4 ? Math.round(w / (elapsedSec/60)) : 0;

      var verdict;
      if (w === 0) {
        verdict = '<em>No speech captured. Try again — speak closer to the mic.</em>';
      } else if (wpm < bench.min - 20) {
        verdict = '🐢 <strong>' + wpm + ' WPM</strong> · too slow for ' + bench.label + '. Target ' + bench.min + '–' + bench.max + '. Push the pace — full sentences with fewer pauses.';
      } else if (wpm < bench.min) {
        verdict = '🚶 <strong>' + wpm + ' WPM</strong> · a touch slow. Target ' + bench.min + '–' + bench.max + '. Try shorter pauses between phrases.';
      } else if (wpm <= bench.max) {
        verdict = '🎯 <strong>' + wpm + ' WPM</strong> · within target range for ' + bench.label + '. Good pace.';
      } else if (wpm <= bench.max + 20) {
        verdict = '🏃 <strong>' + wpm + ' WPM</strong> · slightly fast. Articulation suffers past ' + bench.max + '. Slow ~10 %.';
      } else {
        verdict = '🚀 <strong>' + wpm + ' WPM</strong> · too fast. Examiners lose your structure past ' + (bench.max + 20) + '. Take measured pauses between clauses.';
      }

      verdictEl.innerHTML = verdict +
        '<div style="margin-top:8px;font-family:\'JetBrains Mono\',monospace;font-style:normal;font-size:.78rem;opacity:.85">' +
        'words: <strong>' + w + '</strong> · time: <strong>' + fmt(elapsedSec) + '</strong>' +
        '</div>';
    }

    micBtn.addEventListener('click', function(){
      if (recording) { stop(); return; }
      if (!SR) {
        transcript.textContent = '⚠ Web Speech Recognition is not available in this browser. Use Chrome or Edge.';
        return;
      }
      finalText = '';
      interimText = '';
      transcript.textContent = '';
      verdictEl.textContent = '';
      startTime = Date.now();
      recording = true;

      rec = new SR();
      rec.lang = 'en-GB';
      rec.interimResults = true;
      rec.continuous = true;

      rec.onresult = function(ev){
        var interim = '';
        for (var i = ev.resultIndex; i < ev.results.length; i++){
          var r = ev.results[i];
          if (r.isFinal) finalText += (finalText ? ' ' : '') + r[0].transcript.trim();
          else interim += r[0].transcript;
        }
        interimText = interim;
        update();
      };
      rec.onerror = function(e){
        transcript.textContent += ' [mic error: ' + e.error + ']';
      };
      rec.onend = function(){
        if (recording) stop();
      };
      try { rec.start(); } catch(_){}

      micBtn.textContent = '⏹ Stop';
      micBtn.classList.add('recording');

      timerInt = setInterval(function(){
        update();
        var elapsedSec = (Date.now() - startTime)/1000;
        if (elapsedSec >= maxSec) stop();
      }, 250);
    });
  }

  function init(){
    injectStyle();
    document.querySelectorAll('.speech-tracker[data-mode]').forEach(mount);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.SpeechTracker = { mount: mount, init: init };
})();
