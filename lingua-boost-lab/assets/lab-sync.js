/* lab-sync.js v4 — Realtime sync (optional) + always-on persist + identity.
   • С URL ?sync=<roomId>&role=teacher|student — двусторонняя live-комната.
   • Без ?sync — solo-mode: каждый submit идёт в Supabase lab_submissions.
   • На первый submit спрашивает имя ученика → сохраняет в localStorage,
     room_id становится 'student-<slug>'. Маша фильтрует по нему в БД. */
(function(){
  if (window.__labSyncLoaded) return;
  window.__labSyncLoaded = true;

  var SUPABASE_URL  = "https://iqzlphbvmfgoygnozbya.supabase.co";
  var SUPABASE_ANON = "sb_publishable_hYhBk3xS90uouUFd_DZWUw_sOv-6JGO";

  function qs(name){
    var m = location.search.match(new RegExp('[?&]'+name+'=([^&]+)'));
    return m ? decodeURIComponent(m[1]) : null;
  }

  var syncParam = qs('sync');
  var soloMode  = !syncParam;
  var role      = qs('role') || (soloMode ? 'solo' : 'student');
  var roomId;
  if (soloMode) {
    // Если имя уже сохранено — используем сразу 'student-<slug>'.
    // Иначе временный solo-* до первого submit, на котором спросим имя.
    var savedName = '';
    try { savedName = localStorage.getItem('lab-student-name') || ''; } catch(e){}
    if (savedName) {
      roomId = 'student-' + slugify(savedName);
      role = 'solo:' + savedName;
    } else {
      try {
        var stored = localStorage.getItem('lab-solo-id');
        if (!stored) {
          stored = 'solo-' + Math.random().toString(36).slice(2,10);
          localStorage.setItem('lab-solo-id', stored);
        }
        roomId = stored;
      } catch(e) {
        roomId = 'solo-' + Date.now().toString(36);
      }
    }
  } else {
    roomId = syncParam;
  }

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

  function slugify(s){
    return (s||'').toLowerCase().replace(/[^a-zа-яё0-9]+/gi,'-').replace(/^-+|-+$/g,'').slice(0,30);
  }

  // ---- Identity (имя ученика) ----
  function getStoredName(){
    try { return localStorage.getItem('lab-student-name') || ''; } catch(e){ return ''; }
  }
  function saveName(n){
    try { localStorage.setItem('lab-student-name', n); } catch(e){}
  }

  function injectIdentityStyle(){
    if (document.getElementById('lab-identity-style')) return;
    var s = document.createElement('style');
    s.id = 'lab-identity-style';
    s.textContent = ''+
      '.lab-id-overlay{position:fixed;inset:0;background:rgba(20,15,40,.55);'+
        'backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);'+
        'z-index:99998;display:flex;align-items:center;justify-content:center;'+
        'animation:labIdFade .25s ease-out}'+
      '@keyframes labIdFade{from{opacity:0}to{opacity:1}}'+
      '.lab-id-modal{background:linear-gradient(135deg,#fbf8ff 0%,#f0e9ff 100%);'+
        'border:1px solid #d4c0f7;border-left:5px solid #7c3aed;'+
        'border-radius:18px;padding:28px 32px;max-width:420px;width:92vw;'+
        'box-shadow:0 24px 60px rgba(124,58,237,.32);font-family:"Manrope",sans-serif}'+
      '[data-lab-theme="dark"] .lab-id-modal{background:linear-gradient(135deg,#1e1a2e 0%,#241c3e 100%);'+
        'border-color:#5b3aa8;color:#f3eee5}'+
      '.lab-id-modal h3{margin:0 0 8px;font:800 1.25rem/1.25 "Manrope",sans-serif;color:#4a2d8a}'+
      '[data-lab-theme="dark"] .lab-id-modal h3{color:#e9d6ff}'+
      '.lab-id-modal p{margin:0 0 16px;font:500 .92rem/1.55 "Manrope",sans-serif;color:#4a3a6b}'+
      '[data-lab-theme="dark"] .lab-id-modal p{color:#c5b8e6}'+
      '.lab-id-input{width:100%;box-sizing:border-box;padding:13px 16px;border-radius:10px;'+
        'border:1.5px solid #d4c0f7;background:#fff;font:600 1rem/1.3 "Manrope",sans-serif;'+
        'color:#1a1f2e;outline:none;transition:border-color .15s}'+
      '.lab-id-input:focus{border-color:#7c3aed;box-shadow:0 0 0 4px rgba(124,58,237,.12)}'+
      '[data-lab-theme="dark"] .lab-id-input{background:#15102a;border-color:#5b3aa8;color:#f3eee5}'+
      '.lab-id-actions{display:flex;gap:10px;margin-top:16px;justify-content:flex-end}'+
      '.lab-id-btn{padding:11px 18px;border-radius:10px;border:0;cursor:pointer;'+
        'font:700 .88rem/1 "Manrope",sans-serif;transition:transform .15s,box-shadow .15s}'+
      '.lab-id-skip{background:transparent;color:#7c3aed;border:1.5px solid #d4c0f7}'+
      '.lab-id-ok{background:linear-gradient(135deg,#7c3aed 0%,#a855f7 100%);color:#fff}'+
      '.lab-id-ok:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(124,58,237,.42)}'+
      '.lab-id-ok:disabled{opacity:.5;cursor:not-allowed;transform:none;box-shadow:none}';
    document.head.appendChild(s);
  }

  function askName(){
    return new Promise(function(resolve){
      injectIdentityStyle();
      var existing = getStoredName();
      if (existing) return resolve(existing);

      var overlay = document.createElement('div');
      overlay.className = 'lab-id-overlay';
      overlay.innerHTML =
        '<div class="lab-id-modal">'+
          '<h3>Как тебя зовут?</h3>'+
          '<p>Имя нужно один раз — чтобы наставник видел твои результаты по всем урокам.</p>'+
          '<input type="text" class="lab-id-input" placeholder="Например, Тимофей" maxlength="40">'+
          '<div class="lab-id-actions">'+
            '<button type="button" class="lab-id-btn lab-id-skip">Пропустить</button>'+
            '<button type="button" class="lab-id-btn lab-id-ok" disabled>Продолжить</button>'+
          '</div>'+
        '</div>';
      document.body.appendChild(overlay);
      var input = overlay.querySelector('.lab-id-input');
      var ok = overlay.querySelector('.lab-id-ok');
      var skip = overlay.querySelector('.lab-id-skip');
      setTimeout(function(){ input.focus(); }, 30);
      function finish(name){
        if (name) saveName(name);
        overlay.remove();
        resolve(name || '');
      }
      input.addEventListener('input', function(){
        ok.disabled = input.value.trim().length < 2;
      });
      input.addEventListener('keydown', function(e){
        if (e.key === 'Enter' && !ok.disabled) finish(input.value.trim());
        if (e.key === 'Escape') finish('');
      });
      ok.addEventListener('click', function(){ if (!ok.disabled) finish(input.value.trim()); });
      skip.addEventListener('click', function(){ finish(''); });
    });
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
    var statusBadge = soloMode ? null : badge('🔌 connecting…', '#6b7280');

    loadSDK().then(function(sb){
      var client  = sb.createClient(SUPABASE_URL, SUPABASE_ANON);
      var channel = null;
      var muteOutgoing = false;

      if (!soloMode) {
        channel = client.channel('lab-sync:'+roomId, {
          config: { broadcast: { self: false } }
        });

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
            if (role !== 'teacher') return;
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

        var TRACK_SEL = '.gap,.match-item,.match-card,.mcq-opts button,.mc-opts button,' +
          '.tfns-row button,.mc-item button,.wf-row input,.gapfill input,.bank-word,' +
          '.classify-item,.ord-pill,.predict-card,.choice-card,.vocab-card,.dict-input,' +
          '.builder button,textarea,.match-row select';
        var TRACK_CLASSES = ['right','wrong','filled','matched','correct','selected',
          'used','revealed','flipped','picked','show','shown','sel','ok','hit'];

        function pathOf(el){
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

        var sendThrottle = {};
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

        channel.on('broadcast', { event:'dom-state' }, function(p){
          var data = p.payload || {};
          var el = resolve(data.path);
          if (!el) return;
          muteOutgoing = true;
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
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') {
              el.addEventListener('input', function(){ if (!muteOutgoing) maybeSend(el); });
              el.addEventListener('change', function(){ if (!muteOutgoing) maybeSend(el); });
            }
          });
        }
        bindLiveSync();
        var bodyObs = new MutationObserver(function(){ bindLiveSync(); });
        bodyObs.observe(document.body, { childList:true, subtree:true });

        function bindTocBroadcast(){
          var toc = document.querySelector('.lp-toc');
          if (!toc) return setTimeout(bindTocBroadcast, 300);
          var sectionEls = [].slice.call(document.querySelectorAll('section.section'));
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
      } // end if !soloMode

      // --- Submit handler — работает В ОБОИХ режимах.
      //     Solo: спросить имя на первом submit, потом persist в lab_submissions.
      //     Sync: broadcast + persist.
      document.addEventListener('click', function(e){
        var b = e.target.closest('.lp-submit');
        if (!b) return;
        setTimeout(async function(){
          var sec = b.closest('section.section');
          if (!sec) return;
          var report = sec.querySelector('.lp-report');
          if (!report) return;
          var stats = report.querySelector('.lp-stats');
          var m = (stats && stats.textContent || '').match(/(\d+)\s*\/\s*(\d+)/);
          if (!m) return;

          // В solo-режиме — на первом submit без имени всплывёт модалка.
          if (soloMode && /^solo-/.test(roomId)) {
            var nm = await askName();
            if (nm) {
              roomId = 'student-' + slugify(nm);
              role = 'solo:' + nm;
            }
          }

          var title = (sec.querySelector('h2') || {textContent:sec.id}).textContent.trim();
          var misses = [];
          report.querySelectorAll('.lp-item').forEach(function(item){
            misses.push(item.textContent.replace(/\s+/g,' ').trim().slice(0, 200));
          });
          var payload = {
            section_id: sec.id, section_title: title.slice(0,80),
            score: +m[1], total: +m[2], role: role, ts: Date.now()
          };
          if (channel) {
            channel.send({ type:'broadcast', event:'section-submit', payload: payload });
          }
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
      if (statusBadge) {
        statusBadge.textContent = '🔴 '+err.message;
        statusBadge.style.background = '#6b7280';
      }
    });
  });
})();
