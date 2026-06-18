/* lab-persist.js — universal exercise state persistence for Lab lessons.
   Captures class flags + input values + textContent on common exercise
   elements; restores on next page load. Reset via floating button.
   Designed to be drop-in: <script src="path-to/lab-persist.js" defer></script>
   No external deps. Storage: localStorage keyed by location.pathname.
*/
(function(){
  'use strict';

  var KEY = 'lab-persist:' + location.pathname;

  /* state-bearing class flags we will persist (broad list — safe to add) */
  var FLAGS = ['done','correct','wrong','filled','miss','missed','used',
               'selected','sel','revealed','visited','picked','guessed',
               'match','show','shown','placed','hit','ok','heard','spoken',
               'lit','bad','hover','active','recording'];
  var FLAG_SET = Object.create(null);
  FLAGS.forEach(function(f){ FLAG_SET[f] = 1; });

  /* selectors of state-bearing elements (broad) */
  var SEL = [
    '.match-card', '.tf-btn', '.mc-opt', '.mc-q .gap', '.bank-word',
    '.drop-gap', '.gap-input', '.ord-slot', '.ord-pill', '.dict-input',
    '.dict-answer', '.trans-input', '.predict-btn', '.predict-card',
    '.choice-card', '.script-card', '.map-dot', '.postcard',
    '.detective-pill', '.q-row',
    'textarea', '.writing-area', '.oge-transcript', '.oge-results',
    '.utw-card', '.transcript', '.progress-dot', '.rail-step'
  ].join(',');

  /* derive a stable DOM path: prefer id, then walk to data-ex / id / section */
  function pathOf(el){
    if (!el || el === document.body) return null;
    if (el.id) return '#' + el.id;
    var parts = [];
    var n = el;
    while (n && n !== document.body) {
      var p = n.parentElement;
      if (!p) return null;
      var idx = Array.prototype.indexOf.call(p.children, n);
      parts.unshift(idx);
      if (p.id) { parts.unshift('#' + p.id); return parts.join('/'); }
      if (p.dataset && p.dataset.ex)  { parts.unshift('ex:' + p.dataset.ex); return parts.join('/'); }
      if (p.dataset && p.dataset.idx) { parts.unshift('idx:' + p.dataset.idx); return parts.join('/'); }
      if (p.tagName === 'SECTION' && p.id) { parts.unshift('#' + p.id); return parts.join('/'); }
      n = p;
    }
    return parts.length ? parts.join('/') : null;
  }

  function resolve(path){
    if (!path) return null;
    if (path[0] === '#') return document.getElementById(path.slice(1).split('/')[0]) ? walk(document.getElementById(path.slice(1).split('/')[0]), path.split('/').slice(1)) : null;
    if (path.indexOf('ex:') === 0) {
      var parts = path.split('/');
      var root = document.querySelector('[data-ex="' + parts[0].slice(3) + '"]');
      return root ? walk(root, parts.slice(1)) : null;
    }
    return null;
  }
  function walk(root, parts){
    var n = root;
    for (var i=0; i<parts.length; i++){
      var p = parts[i];
      if (p === '' || isNaN(p)) continue;
      n = n.children[+p];
      if (!n) return null;
    }
    return n;
  }

  function pickFlags(el){
    var keep = [];
    if (!el.classList) return keep;
    for (var i=0; i<el.classList.length; i++){
      var c = el.classList[i];
      if (FLAG_SET[c]) keep.push(c);
    }
    return keep;
  }

  function snap(){
    var out = {};
    var nodes = document.querySelectorAll(SEL);
    for (var i=0; i<nodes.length; i++){
      var el = nodes[i];
      var flags = pickFlags(el);
      var hasVal = ('value' in el) && el.value;
      var hasPlaced = el.dataset && el.dataset.placed;
      var isTextLeaf = (el.children.length === 0 && el.textContent && el.textContent.trim());
      var savedText = null;
      if (el.classList.contains('drop-gap') || el.classList.contains('gap-input')
          || el.classList.contains('mc-q')
          || el.classList.contains('ord-slot')
          || el.classList.contains('oge-transcript')
          || el.classList.contains('transcript')
          || el.classList.contains('dict-answer')) {
        savedText = el.textContent || '';
      }
      if (!flags.length && !hasVal && !hasPlaced && savedText === null) continue;
      var path = pathOf(el);
      if (!path) continue;
      var item = {};
      if (flags.length)  item.c = flags;
      if (hasVal)        item.v = el.value;
      if (hasPlaced)     item.p = el.dataset.placed;
      if (savedText !== null) item.t = savedText;
      out[path] = item;
    }
    return out;
  }

  function restore(){
    var raw;
    try { raw = localStorage.getItem(KEY); } catch(e){ return; }
    if (!raw) return;
    var data;
    try { data = JSON.parse(raw); } catch(e){ return; }
    if (!data) return;
    Object.keys(data).forEach(function(path){
      var el = resolve(path);
      if (!el) return;
      var s = data[path];
      if (s.c)            s.c.forEach(function(c){ el.classList.add(c); });
      if (s.v !== undefined && 'value' in el) el.value = s.v;
      if (s.p)            el.dataset.placed = s.p;
      if (s.t !== undefined && el.children.length === 0) el.textContent = s.t;
    });
  }

  var saveT = null;
  function save(){
    clearTimeout(saveT);
    saveT = setTimeout(function(){
      try { localStorage.setItem(KEY, JSON.stringify(snap())); } catch(e){}
    }, 350);
  }

  /* event hooks */
  ['click','input','change','keyup'].forEach(function(ev){
    document.addEventListener(ev, save, true);
  });

  /* restore once DOM + lesson init are ready */
  function onReady(){
    /* wait a beat to let lesson scripts populate banks, lists etc. */
    setTimeout(function(){
      restore();
      addResetBtn();
    }, 300);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
  } else {
    onReady();
  }

  function addResetBtn(){
    if (document.getElementById('lab-reset-btn')) return;
    var btn = document.createElement('button');
    btn.id = 'lab-reset-btn';
    btn.type = 'button';
    btn.innerHTML = '↺ Reset progress';
    btn.title = 'Сбросить прогресс этого урока';
    btn.style.cssText = [
      'position:fixed','bottom:18px','right:18px','z-index:9999',
      'background:#fff','color:#333','border:1.5px solid #999',
      'border-radius:30px','padding:8px 16px',
      'font-family:"JetBrains Mono",ui-monospace,monospace',
      'font-size:.72rem','font-weight:800','letter-spacing:.06em',
      'cursor:pointer','box-shadow:0 4px 14px rgba(0,0,0,.20)',
      'opacity:.85','transition:opacity .2s,transform .15s'
    ].join(';');
    btn.onmouseenter = function(){ btn.style.opacity = '1'; btn.style.transform = 'translateY(-2px)'; };
    btn.onmouseleave = function(){ btn.style.opacity = '.85'; btn.style.transform = 'translateY(0)'; };
    btn.onclick = function(){
      if (confirm('Сбросить прогресс этого урока?\n\n(все ответы, заполненные пропуски, транскрипты и помеченные карточки очистятся)')) {
        try { localStorage.removeItem(KEY); } catch(e){}
        location.reload();
      }
    };
    document.body.appendChild(btn);
  }

  /* expose for console / advanced use */
  window.labPersist = {
    snap:    snap,
    save:    save,
    restore: restore,
    reset: function(){ try { localStorage.removeItem(KEY); } catch(e){} location.reload(); },
    key:     KEY
  };
})();
