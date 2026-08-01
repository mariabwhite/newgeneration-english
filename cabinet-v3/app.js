/*
 * cabinet-v3 · тонкий SPA
 *
 * Auth flow:
 *   1. Пользователь вводит 4-значный PIN
 *   2. POST /functions/v1/family-data {pin}
 *   3. Edge function проверяет SHA256(pin) против students.pin_hash
 *   4. Возвращает JSON: {student, parents, subs, lessons, contracts, teacher}
 *   5. Клиент кэширует в sessionStorage (не localStorage — очищается при закрытии таба)
 *   6. Role picker → parent или student view
 *   7. Контракты открываются через POST /contract-signed-url {pin, contract_id} → 60-сек URL
 *
 * Никакого data.js, никакого vault-decrypt в браузере, никакого cache-bust'а.
 */

(function () {
  'use strict';

  const SB_URL = 'https://iqzlphbvmfgoygnozbya.supabase.co';
  const SB_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxemxwaGJ2bWZnb3lnbm96YnlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAxNjg2ODMsImV4cCI6MjA5NTc0NDY4M30.SvpjaT31L2pRWWi6CU6ZISYu0_wYEK-yqf6q7GizBHs';

  const SESSION_KEY = 'nge_v3_session';

  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  function loadSession() {
    try { return JSON.parse(sessionStorage.getItem(SESSION_KEY) || 'null'); }
    catch { return null; }
  }
  function saveSession(s) { sessionStorage.setItem(SESSION_KEY, JSON.stringify(s)); }
  function clearSession() { sessionStorage.removeItem(SESSION_KEY); }

  async function callFn(name, body) {
    const r = await fetch(`${SB_URL}/functions/v1/${name}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${SB_ANON}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });
    return r.json();
  }

  // ---- Views ----

  function showLogin() {
    $('loginScreen').hidden = false;
    $('rolePicker').hidden = true;
    $('dashboard').hidden = true;
    $('logoutBtn').hidden = true;
    $('pinInput').focus();
  }

  function showRolePicker(session) {
    $('loginScreen').hidden = true;
    $('rolePicker').hidden = false;
    $('dashboard').hidden = true;
    $('logoutBtn').hidden = false;
    const greeting = session.data.student.greeting_parent || session.data.student.greeting_student || 'Здравствуйте';
    $('pickerGreeting').textContent = greeting.replace(/,.+/, '');
    // student взрослый (no parent) — сразу student view
    if (session.data.student.is_adult && (!session.data.parents || !session.data.parents.length)) {
      pickRole(session, 'student');
    }
  }

  function pickRole(session, role) {
    session.role = role;
    saveSession(session);
    renderDashboard(session);
  }

  function renderDashboard(session) {
    $('loginScreen').hidden = true;
    $('rolePicker').hidden = true;
    $('dashboard').hidden = false;
    $('logoutBtn').hidden = false;

    const d = session.data;
    const s = d.student;
    const isParent = session.role === 'parent';

    const greeting = isParent
      ? (s.greeting_parent || 'Здравствуйте')
      : (s.greeting_student || `Привет, ${s.name}`);

    const currentSub = (d.subscriptions || [])[0];
    const upcomingLesson = (d.lessons || []).find(l => l.status === 'planned');
    const completed = (d.lessons || []).filter(l => l.status === 'completed').length;
    const planned = (d.lessons || []).filter(l => l.status === 'planned').length;

    let html = `
      <div class="dash-hero">
        <h1>${esc(greeting)}</h1>
        <p class="sub">${isParent ? 'Кабинет родителя' : 'Кабинет ученика'} · ${esc(s.name)} · ${esc(s.level || '')}</p>
      </div>

      <div class="card">
        <div class="grid">
          <div class="stat"><div class="stat-label">Формат</div><div class="stat-value">${esc(s.format || '—')}</div></div>
          <div class="stat"><div class="stat-label">Длительность</div><div class="stat-value">${esc(s.duration || '—')}</div></div>
          <div class="stat"><div class="stat-label">Расписание</div><div class="stat-value">${esc(s.schedule || '—')}</div></div>
          <div class="stat"><div class="stat-label">Стоимость занятия</div><div class="stat-value">${s.price_per_lesson ? s.price_per_lesson + ' ₽' : '—'}</div></div>
        </div>
      </div>
    `;

    // Current subscription
    if (currentSub) {
      html += `
        <div class="card">
          <h2>Абонемент · ${esc(currentSub.month)}</h2>
          <div class="grid">
            <div class="stat"><div class="stat-label">Занятий</div><div class="stat-value">${currentSub.lessons_used}/${currentSub.lessons_in_package}</div></div>
            ${currentSub.package_amount ? `<div class="stat"><div class="stat-label">Сумма</div><div class="stat-value">${currentSub.package_amount} ₽</div></div>` : ''}
            <div class="stat"><div class="stat-label">Статус</div><div class="stat-value">${currentSub.paid ? '🟢 Оплачен' : '🟡 Ожидает'}</div></div>
          </div>
          ${currentSub.payment_note ? `<p style="margin-top:14px;color:var(--muted);font-size:13px">${esc(currentSub.payment_note)}</p>` : ''}
        </div>
      `;
    }

    // Lessons
    if (d.lessons && d.lessons.length) {
      html += `<div class="card"><h2>Уроки</h2><p class="sub">Пройдено: ${completed} · В плане: ${planned}</p><table><thead><tr><th>Дата</th><th>№</th><th>Тема</th><th>Статус</th></tr></thead><tbody>`;
      d.lessons.slice().reverse().forEach(l => {
        html += `<tr>
          <td>${esc(l.lesson_date)}</td>
          <td>${l.num || '—'}</td>
          <td>${esc(l.topic || '—')}${l.homework_module_url ? ` · <a href="${esc(l.homework_module_url)}" target="_blank" rel="noreferrer">${esc(l.homework_module_title || 'урок')}</a>` : ''}</td>
          <td><span class="status-badge status-${l.status}">${l.status === 'completed' ? 'Пройден' : 'Запланирован'}</span></td>
        </tr>`;
      });
      html += `</tbody></table></div>`;
    }

    // Contracts — только parent view (или взрослый solo)
    if (isParent || s.is_adult) {
      if (d.contracts && d.contracts.length) {
        html += `<div class="card"><h2>🔐 Договор и документы</h2><p class="sub">Файлы хранятся в защищённом хранилище. Кликните — откроется по временной ссылке (60 сек).</p>`;
        d.contracts.forEach(c => {
          html += `<button class="contract-btn" data-contract-id="${esc(c.id)}">
            <span>📄 ${esc(c.original_filename || '—')}</span>
            <small>${c.doc_type || ''} · ${Math.round((c.file_size || 0) / 1024)} KB</small>
          </button>`;
        });
        html += `</div>`;
      } else {
        html += `<div class="card"><h2>🔐 Договор</h2><p class="sub">Документов пока нет. Свяжитесь с Марией.</p></div>`;
      }
    }

    // Teacher contact
    if (d.teacher) {
      html += `<div class="card">
        <h2>Связь</h2>
        <p><strong>${esc(d.teacher.full_name)}</strong></p>
        ${d.teacher.telegram ? `<p><a href="https://t.me/${esc(d.teacher.telegram.replace(/^@/,''))}" target="_blank" rel="noreferrer">Telegram: ${esc(d.teacher.telegram)}</a></p>` : ''}
        ${d.teacher.phone ? `<p>Телефон: ${esc(d.teacher.phone)}</p>` : ''}
      </div>`;
    }

    $('dashboard').innerHTML = html;

    // Bind contract clicks
    $('dashboard').querySelectorAll('[data-contract-id]').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.dataset.contractId;
        const old = btn.innerHTML;
        btn.innerHTML = '⏳ Открываю…';
        btn.disabled = true;
        try {
          const r = await callFn('contract-signed-url', { pin: session.pin, contract_id: id });
          if (r.url) {
            window.open(r.url, '_blank', 'noopener,noreferrer');
            btn.innerHTML = old;
          } else {
            btn.innerHTML = '❌ ' + (r.error || 'ошибка');
          }
        } catch (e) {
          btn.innerHTML = '❌ ' + e.message;
        } finally {
          setTimeout(() => { btn.disabled = false; btn.innerHTML = old; }, 3000);
        }
      });
    });
  }

  // ---- Init ----

  $('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const pin = $('pinInput').value.trim();
    const msg = $('loginMsg');
    msg.hidden = true;
    if (!/^\d{4}$/.test(pin)) {
      msg.textContent = 'PIN — 4 цифры'; msg.className = 'msg err'; msg.hidden = false;
      return;
    }
    $('loginBtn').disabled = true;
    $('loginBtn').textContent = 'Проверяю…';
    try {
      const r = await callFn('family-data', { pin });
      if (r.error) {
        msg.textContent = r.error === 'PIN_NOT_FOUND' ? 'PIN не подошёл' : ('Ошибка: ' + r.error);
        msg.className = 'msg err'; msg.hidden = false;
        $('loginBtn').disabled = false; $('loginBtn').textContent = 'Войти';
        return;
      }
      const session = { pin, data: r };
      saveSession(session);
      // если взрослый без parent — сразу student view
      if (r.student.is_adult && (!r.parents || !r.parents.length)) {
        session.role = 'student';
        saveSession(session);
        renderDashboard(session);
      } else {
        showRolePicker(session);
      }
    } catch (e) {
      msg.textContent = 'Сеть недоступна: ' + e.message;
      msg.className = 'msg err'; msg.hidden = false;
      $('loginBtn').disabled = false; $('loginBtn').textContent = 'Войти';
    }
  });

  document.querySelectorAll('.role-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const session = loadSession();
      if (!session) { showLogin(); return; }
      pickRole(session, btn.dataset.role);
    });
  });

  $('logoutBtn').addEventListener('click', () => {
    clearSession();
    showLogin();
  });

  // ---- Boot ----
  // Handoff from legacy /cabinet/: #pin=XXXX in URL fragment (not sent to server)
  async function tryHashPin() {
    const m = /(?:^|[#&])pin=(\d{4})(?:&|$)/.exec(location.hash);
    if (!m) return false;
    const pin = m[1];
    history.replaceState(null, '', location.pathname);
    try {
      const r = await callFn('family-data', { pin });
      if (r && !r.error) {
        const session = { pin, data: r };
        if (r.student.is_adult && (!r.parents || !r.parents.length)) session.role = 'student';
        saveSession(session);
        return true;
      }
    } catch {}
    return false;
  }

  (async () => {
    if (await tryHashPin()) {
      const s = loadSession();
      if (s && s.role) renderDashboard(s);
      else if (s) showRolePicker(s);
      return;
    }
    const existing = loadSession();
    if (existing && existing.data && existing.role) {
      renderDashboard(existing);
    } else if (existing && existing.data) {
      showRolePicker(existing);
    } else {
      showLogin();
    }
  })();
})();
