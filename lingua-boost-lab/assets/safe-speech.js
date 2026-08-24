(function () {
  "use strict";

  var current = null;
  var timer = null;
  var DEFAULT_TIMEOUT_MS = 12000;

  function clearTimer() {
    if (timer) clearTimeout(timer);
    timer = null;
  }

  function stop() {
    clearTimer();
    current = null;
    try {
      if (window.speechSynthesis) window.speechSynthesis.cancel();
    } catch (_) {}
  }

  function speak(text, options) {
    options = options || {};
    if (!text || !window.speechSynthesis || !window.SpeechSynthesisUtterance) return Promise.resolve(false);
    stop();
    return new Promise(function (resolve) {
      var done = false;
      function finish(value) {
        if (done) return;
        done = true;
        clearTimer();
        current = null;
        resolve(value);
      }
      try {
        var u = new SpeechSynthesisUtterance(String(text));
        if (options.lang) u.lang = options.lang;
        if (options.rate) u.rate = options.rate;
        if (options.pitch) u.pitch = options.pitch;
        if (options.volume != null) u.volume = options.volume;
        if (options.voice) u.voice = options.voice;
        u.onend = function () { finish(true); };
        u.onerror = function () { finish(false); };
        current = u;
        timer = setTimeout(function () {
          try { window.speechSynthesis.cancel(); } catch (_) {}
          finish(false);
        }, options.timeout || DEFAULT_TIMEOUT_MS);
        window.speechSynthesis.speak(u);
      } catch (_) {
        finish(false);
      }
    });
  }

  function getEnglishVoice(prefer) {
    try {
      var voices = window.speechSynthesis && window.speechSynthesis.getVoices ? window.speechSynthesis.getVoices() : [];
      if (!voices || !voices.length) return null;
      var re = prefer ? new RegExp(prefer, "i") : null;
      return (re && voices.find(function (v) { return re.test((v.name || "") + " " + (v.lang || "")); }))
        || voices.find(function (v) { return /^en-GB/i.test(v.lang || ""); })
        || voices.find(function (v) { return /^en/i.test(v.lang || ""); })
        || null;
    } catch (_) { return null; }
  }

  window.NGESafeSpeech = { speak: speak, stop: stop, getEnglishVoice: getEnglishVoice };
})();