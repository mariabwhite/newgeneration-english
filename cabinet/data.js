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

  const DATA_BUILD_ID = "20260918-cabinet-data-contract-v18";
  const CACHE_KEY = "nge_data_cache_v18"; // v18: normalized lesson identity
  const CACHE_TTL_MS = 15 * 1000;

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
      if (!obj || obj.build !== DATA_BUILD_ID) return null;
      if (!obj || !obj.ts || (Date.now() - obj.ts) > CACHE_TTL_MS) return null;
      return obj.data;
    } catch (_) { return null; }
  }
  function writeCache(data) {
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ build: DATA_BUILD_ID, ts: Date.now(), data })); } catch (_) {}
  }
  function clearDataCaches() {
    try {
      for (let i = sessionStorage.length - 1; i >= 0; i--) {
        const k = sessionStorage.key(i);
        if (k && k.indexOf("nge_data_cache_") === 0) sessionStorage.removeItem(k);
      }
    } catch (_) {}
  }

  function timeoutSignal(ms) {
    if (typeof AbortController === "undefined") return { signal: undefined, cancel: function () {} };
    const ctrl = new AbortController();
    const timer = setTimeout(function () { ctrl.abort(); }, ms);
    return { signal: ctrl.signal, cancel: function () { clearTimeout(timer); } };
  }

  async function callFn(name, body) {
    const timeout = timeoutSignal(12000);
    let r;
    try {
      r = await fetch(SB_URL + "/functions/v1/" + name, {
        method: "POST",
        cache: "no-store",
        headers: {
          "Authorization": "Bearer " + SB_ANON,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
        signal: timeout.signal,
      });
    } catch (e) {
      if (e && e.name === "AbortError") throw new Error("Сервер не отвечает. Попробуйте ещё раз через минуту.");
      throw e;
    } finally {
      timeout.cancel();
    }
    if (!r.ok) throw new Error("HTTP " + r.status);
    return await r.json();
  }

  // Empty fallback shape — если браузер offline на login-странице,
  // cabinet.js увидит пустые массивы и просто покажет login-форму.
  const EMPTY = { students: [], reports: [], teacher: { id: "teacher", name: "", passwordHash: "" } };

  // Payment defaults — статические реквизиты Марии для кнопки «Оплатить через Т-Банк»
  // в кабинете родителя (cabinet.js renderParent → payment.tinkoffQuickPay).
  // Edge fn family-data пока не возвращает payment — доклеиваем клиентски.
  const PAYMENT_DEFAULTS = {
    sbpPhone: "+7 916 510-17-92",
    sbpBank: "Т-Банк",
    tinkoffQuickPay: "https://www.tinkoff.ru/rm/r_PnDqHEqsDu.EkrmOLeXmQ/MIhLS10143",
    telegram: "https://t.me/mariabwhite",
    recipient: "Бурцева Мария Витальевна",
    bank: "Т-Банк",
    inn: "771771016209",
    purpose: "Оплата занятий английским языком (самозанятая, без НДС)."
  };
  function _ensurePayment(data) {
    if (!data) return data;
    if (!data.payment || typeof data.payment !== "object") {
      data.payment = PAYMENT_DEFAULTS;
    } else {
      // не затираем то, что уже пришло с сервера
      Object.keys(PAYMENT_DEFAULTS).forEach(function (k) {
        if (data.payment[k] == null || data.payment[k] === "") data.payment[k] = PAYMENT_DEFAULTS[k];
      });
    }
    return data;
  }

  function _lessonIdentity(lesson) {
    if (!lesson || !lesson.date) return "";
    const date = String(lesson.date);
    const num = lesson.num == null || lesson.num === "" ? "" : String(lesson.num);
    if (num) return date + "|" + num;
    const topic = String(lesson.topic || "").trim().toLowerCase();
    const url = lesson.url || (lesson.homework && lesson.homework.module_url) || "";
    return date + "|topic:" + topic + "|url:" + String(url);
  }

  function _mergeLesson(a, b) {
    const merged = Object.assign({}, a || {});
    Object.keys(b || {}).forEach(function (key) {
      const value = b[key];
      if (value == null || value === "") return;
      if (key === "homework" && merged.homework && value && typeof value === "object") {
        const current = Object.assign({}, merged.homework);
        Object.keys(value).forEach(function (homeworkKey) {
          if (value[homeworkKey] != null && value[homeworkKey] !== "") current[homeworkKey] = value[homeworkKey];
        });
        const modules = (Array.isArray(current.modules) ? current.modules : [])
          .concat(Array.isArray(value.modules) ? value.modules : []);
        if (modules.length) {
          const seen = new Set();
          current.modules = modules.filter(function (module) {
            const moduleKey = String(module && (module.url || module.title) || "");
            if (seen.has(moduleKey)) return false;
            seen.add(moduleKey);
            return true;
          });
        }
        merged.homework = current;
        return;
      }
      if (key === "status") {
        const rank = { completed: 5, missed: 4, rescheduled: 3, planned: 2, cancelled: 1 };
        if ((rank[value] || 0) >= (rank[merged.status] || 0)) merged.status = value;
        return;
      }
      if (merged[key] == null || merged[key] === "") merged[key] = value;
    });
    return merged;
  }

  function _dedupeLessons(lessons) {
    const byIdentity = new Map();
    (Array.isArray(lessons) ? lessons : []).forEach(function (lesson) {
      if (!lesson || !lesson.date) return;
      const identity = _lessonIdentity(lesson);
      byIdentity.set(identity, byIdentity.has(identity) ? _mergeLesson(byIdentity.get(identity), lesson) : lesson);
    });
    return Array.from(byIdentity.values()).sort(function (a, b) {
      return String(a.date).localeCompare(String(b.date)) || Number(a.num || 0) - Number(b.num || 0);
    });
  }

  function _isActiveLesson(student, lesson) {
    if (!student || !lesson || !lesson.date) return false;
    if (lesson.status === "cancelled") return false;
    const start = student.subscription_span_start;
    const end = student.subscription_span_end;
    if (start && end) return lesson.date >= start && lesson.date <= end;
    const month = student.subscription_month;
    if (month) return lesson.date.startsWith(month);
    return false;
  }

  function _normalizeCabinetPackages(data) {
    if (!data || !Array.isArray(data.students)) return data;
    data.students.forEach(function (student) {
      if (!student || !Array.isArray(student.lessons)) return;

      student.lessons = _dedupeLessons(student.lessons);

      const activeLessons = student.lessons.filter(function (lesson) {
        return _isActiveLesson(student, lesson);
      });
      const completed = activeLessons.filter(function (lesson) {
        return lesson.status === "completed";
      }).length;
      const declaredTotal = Number(student.lessons_in_package) || activeLessons.length || null;
      const declaredUsed = Number(student.lessons_used_this_month);
      const used = Number.isFinite(declaredUsed) ? Math.max(declaredUsed, completed) : completed;
      const first = activeLessons[0];
      const last = activeLessons[activeLessons.length - 1];

      if (!student.subscription_span_start && first) student.subscription_span_start = first.date;
      if (!student.subscription_span_end && last) student.subscription_span_end = last.date;
      if (!student.subscription_month && (student.subscription_span_start || (first && first.date))) {
        student.subscription_month = String(student.subscription_span_start || first.date).slice(0, 7);
      }
      if (declaredTotal != null) student.lessons_in_package = declaredTotal;
      student.lessons_used_this_month = used;
      student.active_package = {
        month: student.subscription_month || null,
        span_start: student.subscription_span_start || null,
        span_end: student.subscription_span_end || null,
        lessons_total: declaredTotal,
        lessons_used: used,
        lesson_dates: activeLessons.map(function (lesson) { return lesson.date; })
      };
    });
    return data;
  }

  function _prepareData(data) {
    _ensurePayment(data);
    _normalizeCabinetPackages(data);
    return data;
  }

  window.NGE_DATA_PROMISE = (async function boot() {
    // 1) Быстрый путь: свежий кэш в sessionStorage
    const cached = readCache();
    if (cached) {
      _prepareData(cached);
      window.NGE_DATA = cached;
      return cached;
    }

    // 2) По сессии выбираем endpoint
    const session = readSession();
    try {
      if (session && session.role === "teacher" && session.teacher_password) {
        const data = await callFn("all-data", { teacher_password: session.teacher_password });
        _prepareData(data);
        writeCache(data);
        window.NGE_DATA = data;
        return data;
      }
      if (session && session.pin) {
        const data = await callFn("family-data", { pin: session.pin });
        _prepareData(data);
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
    _prepareData(data);
    writeCache(data);
    window.NGE_DATA = data;
  };
  window.NGE_DATA_INVALIDATE = function () {
    clearDataCaches();
  };
})();
