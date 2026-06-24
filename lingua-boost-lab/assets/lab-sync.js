/* lab-sync.js — Supabase Realtime two-way sync for Lab lessons.
   Teacher and student joined to the same channel see each other's:
     • TOC clicks (one scrolls → other scrolls)
     • Section submits + scores
   Cross-device: phone, tablet, Yandex, Chrome — single channel via URL ?sync=<roomId>.

   Activation: open URL with ?sync=<roomId>&role=teacher|student
   Without ?sync=, the script is a no-op (regular solo lesson). */
(function(){
  if (window.__labSyncLoaded) return;
  window.__labSyncLoaded = true;

  var SUPABASE_URL  = "https://iqzlphbvmfgoygnozbya.supabase.co";
  var SUPABASE_ANON = "sb_publishable_hYhBk3xS90uouUFd_DZWUw_sOv-6JGO";

  function qs(name){
    var m = location.search.match(new RegExp('[?&]'+name+'=([^&]+)'));
    return m ? decodeURIComponent(m[1]) : null;
  }

  var roomId = qs('sync');
  if (!roomId) return; // solo mode — no sync
  var role = qs('role') || 'student';

  function loadSDK(){
    return new Promise(function(resolve, reject){
      if (window.supabase && window.supabase.createClient) return resolve(window.supabase);
      var s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js';
      s.async = true;
      s.onload = function(){ resolve(window.supabase); };
      s.onerror = function(){ reject(new Error('Supabase SDK load failed')); };
      document.head.appendChild(s);
    });
  }

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function badge(text, color){
    var el = document.createElement('div');
    el.textContent = text;
    el.style.cssText = 'position:fixed;left:50%;top:14px;transform:translateX(-50%);'+
      'z-index:9999;padding:7px 16px;border-radius:50px;font:800 11px/1 "JetBrains Mono",monospace;'+
      'letter-spacing:.14em;text-transform:uppercase;background:'+color+';color:#fff;'+
      'box-shadow:0 6px 22px rgba(0,0,0,.25);';
    document.body.appendChild(el);
    return el;
  }

  ready(function(){
    var statusBadge = badge('🔌 connecting…', '#6b7280');

    loadSDK().then(function(sb){
      var client = sb.createClient(SUPABASE_URL, SUPABASE_ANON);
      var channel = client.channel('lab-sync:'+roomId, {
        config: { broadcast: { self: false } }
      });

      var sectionEls = [];
      var observer = null;
      var muteOutgoing = false;

      // --- Incoming events ---
      channel
        .on('broadcast', { event: 'scroll-to' }, function(payload){
          var p = payload.payload || {};
          var el = document.getElementById(p.id);
          if (el) {
            muteOutgoing = true;
            el.scrollIntoView({ behavior:'smooth', block:'start' });
            setTimeout(function(){ muteOutgoing = false; }, 1200);
          }
        })
        .on('broadcast', { event: 'section-submit' }, function(payload){
          var p = payload.payload || {};
          if (role !== 'teacher') return; // teacher sees student's submits
          var note = badge('📋 '+p.role+' сдал '+p.section+' · '+p.score+'/'+p.total, '#0033A0');
          setTimeout(function(){ note.remove(); }, 5000);
        })
        .subscribe(function(status){
          if (status === 'SUBSCRIBED') {
            statusBadge.textContent = '🟢 '+role+' · room '+roomId;
            statusBadge.style.background = role === 'teacher' ? '#D52B1E' : '#2E7D32';
          } else if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
            statusBadge.textContent = '🔴 sync error';
            statusBadge.style.background = '#6b7280';
          }
        });

      // --- Live DOM-state sync · каждое действие ученика → у учителя ---
      // Передаём изменения классов (.right/.wrong/.filled/.matched/.correct/.selected)
      // и значения input/textarea на tracked-элементах.
      // Учитель применяет то же самое к своему DOM.
      var TRACK_SEL = '.gap,.match-item,.match-card,.mcq-opts button,.mc-opts button,' +
        '.tfns-row button,.mc-item button,.wf-row input,.gapfill input,.bank-word,' +
        '.classify-item,.ord-pill,.predict-card,.choice-card,.vocab-card,.dict-input,' +
        '.builder button,textarea,.match-row select';
      var TRACK_CLASSES = ['right','wrong','filled','matched','correct','selected',
        'used','revealed','flipped','picked','show','shown','sel','ok','hit'];

      function pathOf(el){
        // Стабильный path по id или index chain до section[id]
        if (!el || el === document.body) return null;
        if (el.id) return '#'+el.id;
        var parts = [];
        var n = el;
        while (n && n !== document.body) {
          var p = n.parentElement;
          if (!p) return null;
          var idx = Array.prototype.indexOf.call(p.children, n);
          parts.unshift(idx);
          if (p.id) { parts.unshift('#'+p.id); return parts.join('/'); }
          if (p.tagName === 'SECTION' && p.id) { parts.unshift('#'+p.id); return parts.join('/'); }
          n = p;
        }
        return null;
      }
      function resolve(path){
        if (!path) return null;
        var parts = path.split('/');
        var first = parts.shift();
        var root = first[0] === '#' ? document.getElementById(first.slice(1)) : null;
        if (!root) return null;
        var n = root;
        for (var i=0; i<parts.length; i++){
          var idx = parseInt(parts[i], 10);
          if (isNaN(idx)) continue;
          n = n.children[idx];
          if (!n) return null;
        }
        return n;
      }
      function pickFlags(el){
        var keep = [];
        if (!el.classList) return keep;
        for (var i=0; i<TRACK_CLASSES.length; i++) {
          if (el.classList.contains(TRACK_CLASSES[i])) keep.push(TRACK_CLASSES[i]);
        }
        return keep;
      }

      var sendThrottle = {}; // path -> last-sent-ts
      function maybeSend(el){
        var path = pathOf(el);
        if (!path) return;
        var now = Date.now();
        if (sendThrottle[path] && now - sendThrottle[path] < 120) return;
        sendThrottle[path] = now;
        var payload = { path: path, classes: pickFlags(el) };
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') payload.value = el.value || '';
        if (el.tagName === 'SELECT') payload.value = el.value || '';
        if (el.textContent && el.matches && (el.matches('.gap') || el.matches('.match-item'))) {
          payload.text = el.textContent.slice(0, 80);
        }
        channel.send({ type:'broadcast', event:'dom-state', payload: payload });
      }

      // Apply incoming state
      channel.on('broadcast', { event:'dom-state' }, function(p){
        var data = p.payload || {};
        var el = resolve(data.path);
        if (!el) return;
        muteOutgoing = true;
        // Reset tracked classes then re-apply
        TRACK_CLASSES.forEach(function(c){ if (el.classList) el.classList.remove(c); });
        (data.classes || []).forEach(function(c){ el.classList && el.classList.add(c); });
        if ('value' in data && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT')) {
          el.value = data.value;
        }
        if (data.text && el.matches && (el.matches('.gap') || el.matches('.match-item'))) {
          el.textContent = data.text;
        }
        setTimeout(function(){ muteOutgoing = false; }, 200);
      });

      // Watch classList changes on tracked elements
      function bindLiveSync(){
        var nodes = document.querySelectorAll(TRACK_SEL);
        nodes.forEach(function(el){
          if (el.__syncBound) return;
          el.__syncBound = true;
          var mo = new MutationObserver(function(){
            if (muteOutgoing) return;
            maybeSend(el);
          });
          mo.observe(el, { attributes:true, attributeFilter:['class'], childList:true, characterData:true, subtree:true });
          // input/textarea also fire on input
          if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') {
            el.addEventListener('input', function(){ if (!muteOutgoing) maybeSend(el); });
            el.addEventListener('change', function(){ if (!muteOutgoing) maybeSend(el); });
          }
        });
      }
      bindLiveSync();
      // Re-bind when DOM grows (sym-grid, dynamic content)
      var bodyObs = new MutationObserver(function(){ bindLiveSync(); });
      bodyObs.observe(document.body, { childList:true, subtree:true });

      // --- Outgoing: TOC click broadcasts scroll target ---
      function bindTocBroadcast(){
        var toc = document.querySelector('.lp-toc');
        if (!toc) {
          // Lab-pilot hasn't created TOC yet — wait
          return setTimeout(bindTocBroadcast, 300);
        }
        sectionEls = [].slice.call(document.querySelectorAll('section.section'));
        toc.querySelectorAll('.lp-toc-btn').forEach(function(btn, i){
          btn.addEventListener('click', function(){
            if (muteOutgoing) return;
            var sec = sectionEls[i];
            if (sec && sec.id) {
              channel.send({
                type: 'broadcast', event: 'scroll-to',
                payload: { id: sec.id, idx: i, role: role }
              });
            }
          }, true);
        });
      }
      bindTocBroadcast();

      // --- Outgoing: Submit · broadcast live + persist to Supabase ---
      document.addEventListener('click', function(e){
        var b = e.target.closest('.lp-submit');
        if (!b) return;
        // Wait until lab-pilot renders the report
        setTimeout(async function(){
          var sec = b.closest('section.section');
          if (!sec) return;
          var report = sec.querySelector('.lp-report');
          if (!report) return;
          var stats = report.querySelector('.lp-stats');
          var m = (stats && stats.textContent || '').match(/(\d+)\s*\/\s*(\d+)/);
          if (!m) return;
          var title = (sec.querySelector('h2') || {textContent:sec.id}).textContent.trim();
          var misses = [];
          report.querySelectorAll('.lp-item').forEach(function(item){
            misses.push(item.textContent.replace(/\s+/g,' ').trim().slice(0, 200));
          });
          var payload = {
            section_id: sec.id, section_title: title.slice(0,80),
            score: +m[1], total: +m[2], role: role, ts: Date.now()
          };
          // Live broadcast
          channel.send({ type:'broadcast', event:'section-submit', payload: payload });
          // Persist (history)
          try {
            await client.from('lab_submissions').insert({
              room_id: roomId,
              lesson_path: location.pathname,
              section_id: sec.id,
              section_title: title.slice(0,80),
              student_role: role,
              score: +m[1], total: +m[2],
              misses: misses
            });
          } catch (e) { console.warn('[lab-sync] persist failed', e); }
        }, 400);
      });
    }).catch(function(err){
      statusBadge.textContent = '🔴 '+err.message;
      statusBadge.style.background = '#6b7280';
    });
  });
})();
