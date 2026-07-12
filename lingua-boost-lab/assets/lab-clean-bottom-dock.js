/* LinguaBoost Lab clean bottom dock · v1 · canon from speaking-prep-2026 */
(function(){
  'use strict';

  function ready(fn){
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  function addStyle(){
    if (document.getElementById('lab-clean-bottom-dock-style')) return;
    var st = document.createElement('style');
    st.id = 'lab-clean-bottom-dock-style';
    st.textContent = [
      'html body:not(.clean-dock-show-lex) > .vocab-box,',
      'html body:not(.clean-dock-show-lex) > .lab-lex-box,',
      'html body:not(.clean-dock-show-lex) > #labVocabBox,',
      'html body .lp-fab,',
      'html body .lp-fab-btn,',
      'html body > #lab-reset-btn{',
      '  display:none!important;visibility:hidden!important;pointer-events:none!important;',
      '}',
      'html body.clean-dock-show-lex > .vocab-box,',
      'html body.clean-dock-show-lex > .lab-lex-box,',
      'html body.clean-dock-show-lex > #labVocabBox{',
      '  display:block!important;visibility:visible!important;pointer-events:auto!important;',
      '}',
      'html body.clean-dock-show-lex > .vocab-box.expanded{',
      '  max-width:min(360px,calc(100vw - 24px))!important;width:min(360px,calc(100vw - 24px))!important;',
      '  right:12px!important;bottom:112px!important;left:auto!important;top:auto!important;',
      '}',
      'html body .lp-overlay.show,',
      'html body .lab-hw-overlay.show{',
      '  display:flex!important;visibility:visible!important;pointer-events:auto!important;',
      '}',
      '.speaking-bottom-dock{',
      '  position:fixed;right:14px;bottom:12px;z-index:1005;',
      '  display:flex;flex-direction:column;gap:8px;width:104px;',
      '}',
      '.speaking-bottom-dock button{',
      '  width:104px;min-height:40px;border-radius:11px;',
      '  border:1px solid var(--line-3,rgba(245,200,66,.24));',
      '  background:color-mix(in srgb,#fff 90%,var(--accent,#F5C842) 10%);color:#111827;',
      '  box-shadow:0 8px 20px rgba(0,0,0,.42);',
      '  font:900 9.5px/1.08 var(--mono,"JetBrains Mono",monospace);',
      '  letter-spacing:.07em;text-transform:uppercase;cursor:pointer;padding:7px 8px;',
      '}',
      '.speaking-bottom-dock button:first-child{',
      '  background:linear-gradient(135deg,var(--brand-2,#A8C7EA),var(--accent,#F5C842));',
      '  color:var(--accent-on,#0F1216);border-color:rgba(255,255,255,.18);',
      '}',
      '.speaking-bottom-dock button:hover{border-color:var(--accent,#F5C842)}',
      '@media(max-width:1024px){',
      '  .speaking-bottom-dock{left:min(calc(100vw - 150px),620px);right:auto;bottom:10px;width:96px;gap:7px}',
      '  .speaking-bottom-dock button{width:96px;min-height:38px;font-size:9px}',
      '  html body.clean-dock-show-lex > .vocab-box.expanded{left:12px!important;right:auto!important;width:calc(100vw - 24px)!important}',
      '}'
    ].join('\n');
    document.head.appendChild(st);
  }

  function findSection(pattern){
    var sections = Array.prototype.slice.call(document.querySelectorAll('section, .section, [id]'));
    return sections.find(function(el){
      var text = ((el.id || '') + ' ' + (el.className || '') + ' ' + (el.textContent || '').slice(0, 220)).toLowerCase();
      return pattern.test(text);
    });
  }

  function openVocabulary(){
    var lex = document.querySelector('.vocab-box,.lab-lex-box,#labVocabBox');
    if (lex) {
      document.body.classList.add('clean-dock-show-lex');
      lex.style.removeProperty('display');
      lex.style.removeProperty('visibility');
      lex.style.removeProperty('pointer-events');
      try { lex.click(); } catch(e) {}
      return;
    }
    var sec = findSection(/vocab|vocabulary|lexicon|словар/);
    if (sec) sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function openResults(){
    document.body.classList.remove('clean-dock-show-lex');
    document.querySelectorAll('.lp-overlay.show,.lab-hw-overlay.show').forEach(function(el){
      el.classList.remove('show');
    });
    var btn = document.querySelector('.lp-fab-btn');
    if (btn) {
      try { btn.click(); return; } catch(e) {}
    }
    var total = document.getElementById('lab-total-block') || findSection(/final|итог|result|score|total/);
    if (total) total.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function install(){
    addStyle();
    if (document.querySelector('.speaking-bottom-dock')) return;
    var dock = document.createElement('div');
    dock.className = 'speaking-bottom-dock';
    dock.innerHTML = '<button type="button" data-clean-lex>VOCABULARY</button><button type="button" data-clean-total>RESULTS</button>';
    document.body.appendChild(dock);
    positionDock(dock);
    dock.querySelector('[data-clean-lex]').addEventListener('click', openVocabulary);
    dock.querySelector('[data-clean-total]').addEventListener('click', openResults);
  }

  function positionDock(dock){
    var narrowDevice = Math.min(screen.width || 0, screen.height || 0) <= 520;
    if (!narrowDevice) return;
    dock.style.right = 'auto';
    dock.style.left = window.innerWidth > 700 ? '620px' : 'calc(100vw - 150px)';
  }

  ready(function(){
    install();
    setTimeout(install, 600);
    setTimeout(install, 1600);
    setTimeout(install, 2600);
  });
})();
