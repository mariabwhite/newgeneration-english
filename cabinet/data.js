/**
 * NG English · cabinet · data.js bootstrap (2026-08-01)
 *
 * Раньше здесь лежал 2300-строчный JSON со всеми учениками, PIN-хешами,
 * отчётами и teacher-данными — доступно всем через GH Pages.
 *
 * Теперь этот файл — тонкий bootstrap: получает данные из Supabase по PIN
 * (родитель/ученик видит ТОЛЬКО свою семью) или по teacher-паролю (Мария
 * видит всё). Результат кладёт в window.NGE_DATA чтобы cabinet.js работал
 * без единой правки render-логики.
 *
 * Форма ответа тождественна старому data.js:
 *   { students: [...], reports: [...], teacher: {id,name,passwordHash} }
 *
 * Rollback: mv .data.js.bak-before-supabase-bootstrap → data.js.
 */
(function () {
  "use strict";

  const SB_URL  = "https://iqzlphbvmfgoygnozbya.supabase.co";
  const SB_ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlxemxwaGJ2bWZnb3lnbm96YnlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAxNjg2ODMsImV4cCI6MjA5NTc0NDY4M30.SvpjaT31L2pRWWi6CU6ZISYu0_wYEK-yqf6q7GizBHs";

  const CACHE_KEY = "nge_data_cache_v1";
  const CACHE_TTL_MS = 5 * 60 * 1000;

  const SESSION_KEY = "nge_session_v2";
  function readSession() {
    try {
      const raw = localStorage.getItem(SESSION_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (_) { return null; }
  }

  function readCache() {
    try {
      const raw = sessionStorage.getItem(CACHE_KEY);
      if (!raw) return null;
      const obj = JSON.parse(raw);
      if (!obj || !obj.ts || (Date.now() - obj.ts) > CACHE_TTL_MS) return null;
      return obj.data;
    } catch (_) { return null; }
  }
  function writeCache(data) {
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ ts: Date.now(), data })); } catch (_) {}
  }

  async function callFn(name, body) {
    const r = await fetch(SB_URL + "/functions/v1/" + name, {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + SB_ANON,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    return await r.json();
  }

  // Empty fallback shape — если браузер offline на login-странице,
  // cabinet.js увидит пустые массивы и просто покажет login-форму.
  const EMPTY = { students: [], reports: [], teacher: { id: "teacher", name: "", passwordHash: "" } };

  window.NGE_DATA_PROMISE = (async function boot() {
    // 1) Быстрый путь: свежий кэш в sessionStorage
    const cached = readCache();
    if (cached) {
      window.NGE_DATA = cached;
      return cached;
    }

    // 2) По сессии выбираем endpoint
    const session = readSession();
    try {
      if (session && session.role === "teacher" && session.teacher_password) {
        const data = await callFn("all-data", { teacher_password: session.teacher_password });
        writeCache(data);
        window.NGE_DATA = data;
        return data;
      }
      if (session && session.pin) {
        const data = await callFn("family-data", { pin: session.pin });
        writeCache(data);
        window.NGE_DATA = data;
        return data;
      }
    } catch (e) {
      // fall through to EMPTY — login-page может продолжать работать
      console.warn("[data.js] bootstrap fetch failed:", e && e.message);
    }

    // 3) Нет сессии (login-страница) — возвращаем пустую заглушку.
    //    Логин сам вызовет edge-fn напрямую через NGECabinet.tryLogin.
    window.NGE_DATA = EMPTY;
    return EMPTY;
  })();

  window.NGE_DATA_READY = window.NGE_DATA_PROMISE.then(function (d) { return d; });

  // Helper для cabinet.js: сохранить только что полученные данные вручную
  // (используется после tryLogin — чтобы не перезапрашивать).
  window.NGE_DATA_HYDRATE = function (data) {
    writeCache(data);
    window.NGE_DATA = data;
  };
  window.NGE_DATA_INVALIDATE = function () {
    try { sessionStorage.removeItem(CACHE_KEY); } catch (_) {}
  };
})();
