/* Jobs & Hobbies: local lesson interactions. Exercises are rendered in HTML. */
(() => {
  'use strict';
  const storageKey = 'jobs-hobbies:v2:' + location.pathname;
  const normalise = value => String(value).normalize('NFKC').toLowerCase()
    .replace(/[‘’`]/g, "'").replace(/[‐‑–—]/g, '-').replace(/\s+/g, ' ').trim()
    .replace(/[.!?]+$/, '').replace(/\bwon't\b/g, 'will not')
    .replace(/\bcan't\b/g, 'cannot').replace(/\bcannot\b/g, 'can not')
    .replace(/\b([a-z]+)n't\b/g, '$1 not');
  const groups = [...document.querySelectorAll('.exercise[data-score-group]')];
  const fields = [...document.querySelectorAll('.exercise input[data-answer], .exercise select[data-answer]')];
  const mcqs = [...document.querySelectorAll('.mcq-row[data-answer]')];
  const writes = [...document.querySelectorAll('textarea')];
  let saveTimer;

  function checkField(field, showFeedback = true) {
    const value = normalise(field.value);
    const correct = value !== '' && field.dataset.answer.split('|').some(a => normalise(a) === value);
    field.classList.toggle('correct', correct);
    field.classList.toggle('right', correct);
    field.classList.toggle('wrong', value !== '' && !correct);
    field.setAttribute('aria-invalid', String(value !== '' && !correct));
    const host = field.closest('.wf-row, .match-row');
    const feedback = host.querySelector('.answer-feedback');
    if (feedback) feedback.textContent = !value || !showFeedback ? '' : correct ? '✓ Correct' : 'Try again — check the hint and the word form.';
    return correct;
  }

  function choose(row, choice) {
    row.dataset.selected = String(choice);
    const correct = String(choice) === row.dataset.answer;
    row.querySelectorAll('[data-choice]').forEach(button => {
      const selected = button.dataset.choice === String(choice);
      button.classList.toggle('correct', selected && correct);
      button.classList.toggle('right', selected && correct);
      button.classList.toggle('wrong', selected && !correct);
      button.setAttribute('aria-pressed', String(selected));
    });
    row.querySelector('.answer-feedback').textContent = correct ? '✓ Correct' : 'Try another answer and explain your choice.';
  }

  function updateCounts() {
    let total = 0, maximum = 0;
    groups.forEach(group => {
      const inputs = [...group.querySelectorAll('input[data-answer], select[data-answer]')];
      const rows = [...group.querySelectorAll('.mcq-row[data-answer]')];
      const score = inputs.filter(input => input.classList.contains('correct')).length + rows.filter(row => row.dataset.selected === row.dataset.answer).length;
      group.querySelector('[data-score]').textContent = String(score);
      group.querySelector('[data-max]').textContent = String(inputs.length + rows.length);
      total += score;
      maximum += inputs.length + rows.length;
    });
    document.getElementById('lesson-score').textContent = String(total);
    document.getElementById('lesson-max').textContent = String(maximum);
    writes.forEach(field => {
      const count = document.querySelector('[data-count-for="' + field.id + '"]');
      if (count) count.textContent = String(field.value.trim().split(/\s+/).filter(Boolean).length);
    });
  }

  function save() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      const state = {fields:{}, choices:{}, writing:{}, features:{}};
      fields.forEach(field => { state.fields[field.id] = field.value; });
      mcqs.forEach(row => { if (row.dataset.selected !== undefined) state.choices[row.dataset.lpKey] = row.dataset.selected; });
      writes.forEach(field => { state.writing[field.id] = field.value; });
      document.querySelectorAll('[data-feature]').forEach(chip => { state.features[chip.dataset.feature] = chip.classList.contains('top') ? 1 : chip.classList.contains('bot') ? 2 : 0; });
      try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) { /* private mode: keep this session usable */ }
    }, 150);
  }

  fields.forEach(field => {
    const check = () => { checkField(field); updateCounts(); save(); };
    field.addEventListener('input', check);
    field.addEventListener('change', check);
    field.addEventListener('blur', check);
    field.addEventListener('keydown', event => {
      if (event.key === 'Enter') { event.preventDefault(); check(); }
    });
  });
  writes.forEach(field => field.addEventListener('input', () => { updateCounts(); save(); }));

  function updateFeatures() {
    const top = document.querySelectorAll('[data-feature].top').length;
    const bottom = document.querySelectorAll('[data-feature].bot').length;
    document.getElementById('features-count').textContent = 'Most important: ' + top + ' / 5 · Least important: ' + bottom + ' / 5' + (top === 5 && bottom === 5 ? ' ✓ Ready to discuss' : '');
    document.querySelectorAll('[data-feature]').forEach(chip => {
      const state = chip.classList.contains('top') ? 'most important' : chip.classList.contains('bot') ? 'least important' : 'unmarked';
      chip.setAttribute('aria-label', chip.textContent + ': ' + state);
    });
  }

  function flip(card) {
    const flipped = card.classList.toggle('flipped');
    card.setAttribute('aria-pressed', String(flipped));
    card.setAttribute('aria-label', card.dataset.word + (flipped ? ': hide meaning' : ': show meaning'));
  }

  const tabs = [...document.querySelectorAll('[data-tv-tab]')];
  function activateTab(tab, focus) {
    tabs.forEach(button => {
      const active = button === tab;
      button.classList.toggle('active', active);
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
      const panel = document.getElementById(button.dataset.tvTab);
      panel.hidden = !active;
      panel.classList.toggle('active', active);
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab,index) => tab.addEventListener('keydown', event => {
    let target;
    if (event.key === 'ArrowRight') target = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft') target = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') target = 0;
    if (event.key === 'End') target = tabs.length - 1;
    if (target !== undefined) { event.preventDefault(); activateTab(tabs[target], true); }
  }));

  function speak(text) {
    const status = document.getElementById('voice-status');
    if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) {
      status.textContent = 'This browser does not support voice playback. Read the displayed text aloud.';
      return;
    }
    window.speechSynthesis.cancel();
    // Keep utterances alive and short enough for browser speech engines.
    const chunks = text.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [text];
    const utterances = chunks.map(chunk => {
      const utterance = new SpeechSynthesisUtterance(chunk.trim());
      utterance.lang = 'en-GB'; utterance.rate = 0.92;
      const voice = window.speechSynthesis.getVoices().find(v => v.lang === 'en-GB');
      if (voice) utterance.voice = voice;
      utterance.onerror = event => { if (!['interrupted','canceled'].includes(event.error)) status.textContent = 'Voice playback is unavailable. The complete text remains on this page.'; };
      return utterance;
    });
    window.__jobsUtterances = utterances;
    status.textContent = 'Reading in English. Use Stop voice to end playback.';
    utterances[utterances.length - 1].onend = () => { status.textContent = 'Playback finished.'; };
    utterances.forEach(utterance => window.speechSynthesis.speak(utterance));
  }

  document.addEventListener('click', event => {
    const option = event.target.closest('[data-choice]');
    if (option) { choose(option.closest('.mcq-row'),option.dataset.choice); updateCounts(); save(); }
    const check = event.target.closest('.check-group');
    if (check) { check.closest('.exercise').querySelectorAll('input[data-answer], select[data-answer]').forEach(field => checkField(field)); updateCounts(); save(); }
    const card = event.target.closest('.vocab-card');
    if (card && !event.target.closest('button,a,input')) flip(card);
    const tab = event.target.closest('[data-tv-tab]');
    if (tab) activateTab(tab, false);
    const chip = event.target.closest('[data-feature]');
    if (chip) {
      if (chip.classList.contains('top')) { chip.classList.remove('top'); chip.classList.add('bot'); }
      else if (chip.classList.contains('bot')) chip.classList.remove('bot');
      else chip.classList.add('top');
      updateFeatures(); save();
    }
    const voiceButton = event.target.closest('[data-say], [data-read]');
    if (voiceButton) speak(voiceButton.dataset.say || document.getElementById(voiceButton.dataset.read).innerText);
    if (event.target.closest('#stop-reading')) { if (window.speechSynthesis) window.speechSynthesis.cancel(); document.getElementById('voice-status').textContent = 'Playback stopped.'; }
  });
  document.addEventListener('keydown', event => {
    if (event.target.matches('.vocab-card') && ['Enter',' '].includes(event.key)) { event.preventDefault(); flip(event.target); }
  });

  function revealAnchor() {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    if (!target) return;
    for (let parent=target.parentElement; parent; parent=parent.parentElement) if (parent.tagName === 'DETAILS') parent.open = true;
    if (target.tagName === 'DETAILS') target.open = true;
  }
  window.addEventListener('hashchange', revealAnchor);
  document.querySelectorAll('a[href="#extra-practice"]').forEach(link => link.addEventListener('click', () => { document.querySelector('.practice-disclosure').open = true; }));
  document.addEventListener('click', event => {
    const button=event.target.closest('.lp-toc-btn');
    if (!button) return;
    const index=[...button.parentElement.children].indexOf(button);
    const target=document.querySelectorAll('section.section')[index];
    if (!target) return;
    for(let parent=target.parentElement;parent;parent=parent.parentElement) if(parent.tagName==='DETAILS') parent.open=true;
  },true);
  const measureHeader=()=>{
    const tabs=document.querySelector('.lesson-tabs');
    const bottom=tabs ? tabs.getBoundingClientRect().bottom : 140;
    document.documentElement.style.setProperty('--lesson-offset',Math.ceil(bottom+16)+'px');
    const padding=Math.ceil(bottom)+'px';
    document.documentElement.style.setProperty('--lesson-header',padding);
    if (document.body.style.paddingTop!==padding || document.body.style.getPropertyPriority('padding-top')!=='important') document.body.style.setProperty('padding-top',padding,'important');
  };
  window.addEventListener('resize',measureHeader);
  setTimeout(measureHeader,350);setTimeout(measureHeader,1400);
  setTimeout(()=>{
    const observer=new ResizeObserver(measureHeader);
    document.querySelectorAll('.topbar,.lesson-tabs,.lab-teacher-banner').forEach(el=>observer.observe(el));
    measureHeader();
  },500);

  try {
    const state = JSON.parse(localStorage.getItem(storageKey) || '{}');
    fields.forEach(field => { if (state.fields && typeof state.fields[field.id] === 'string') field.value = state.fields[field.id]; checkField(field, false); });
    mcqs.forEach(row => { const value = state.choices && state.choices[row.dataset.lpKey]; if (value !== undefined && row.querySelector('[data-choice="' + value + '"]')) choose(row,value); });
    writes.forEach(field => { if (state.writing && typeof state.writing[field.id] === 'string') field.value = state.writing[field.id]; });
    document.querySelectorAll('[data-feature]').forEach(chip => { const v = state.features && state.features[chip.dataset.feature]; chip.classList.toggle('top',v===1);chip.classList.toggle('bot',v===2); });
  } catch (_) { fields.forEach(field => checkField(field,false)); }

  updateFeatures(); updateCounts(); revealAnchor();
  // Shared Lab persistence can restore values after this script. Derive scores
  // from the restored fields too, rather than trusting stale saved CSS flags.
  let syncing = false;
  const reconcile = () => {
    if (syncing) return;
    syncing = true;
    fields.forEach(field => checkField(field, false));
    updateCounts();
    syncing = false;
  };
  document.addEventListener('lab-ready', reconcile);
  setTimeout(reconcile, 900);
  setTimeout(reconcile, 2200);
  window.dispatchEvent(new CustomEvent('lab-ready'));
})();
