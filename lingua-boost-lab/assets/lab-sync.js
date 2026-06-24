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

      // --- Outgoing: Submit broadcasts result to teacher ---
      document.addEventListener('click', function(e){
        var b = e.target.closest('.lp-submit');
        if (!b) return;
        // Wait until lab-pilot renders the report
        setTimeout(function(){
          var sec = b.closest('section.section');
          if (!sec) return;
          var report = sec.querySelector('.lp-report');
          if (!report) return;
          var stats = report.querySelector('.lp-stats');
          var m = (stats && stats.textContent || '').match(/(\d+)\s*\/\s*(\d+)/);
          if (!m) return;
          var title = (sec.querySelector('h2') || {textContent:sec.id}).textContent.trim();
          channel.send({
            type:'broadcast', event:'section-submit',
            payload: { section: title.slice(0,60), score: +m[1], total: +m[2], role: role, ts: Date.now() }
          });
        }, 400);
      });
    }).catch(function(err){
      statusBadge.textContent = '🔴 '+err.message;
      statusBadge.style.background = '#6b7280';
    });
  });
})();
