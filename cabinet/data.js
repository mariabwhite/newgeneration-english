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

  const CACHE_KEY = "nge_data_cache_v8"; // v8: close-of-day display fixes for 15.09
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

  function _normalizeAleksandraLyubaeva(data) {
    if (!data || !Array.isArray(data.students)) return data;
    data.students.forEach(function (student) {
      if (!student || student.name !== "Александра Любаева") return;

      const lessons = Array.isArray(student.lessons) ? student.lessons : [];
      const byDate = {};
      lessons.forEach(function (lesson) {
        if (lesson && lesson.date) byDate[lesson.date] = lesson;
      });

      const first = byDate["2026-09-14"];
      if (!first) return;

      const plannedDates = ["2026-09-24", "2026-09-25", "2026-09-28", "2026-10-01", "2026-10-02", "2026-10-05", "2026-10-08", "2026-10-09", "2026-10-12"];
      const planned = plannedDates
        .map(function (date, index) {
          const lesson = byDate[date] || { date: date };
          return Object.assign({}, lesson, {
            num: index + 2,
            status: "planned",
            topic: null,
            homework: null
          });
        });

      student.subscription_month = "2026-10";
      student.subscription_span_start = "2026-09-14";
      student.subscription_span_end = planned.length ? planned[planned.length - 1].date : "2026-10-23";
      student.lessons_in_package = 10;
      student.lessons_used_this_month = 1;
      student.monthly_package = student.monthly_package || 35000;
      student.payment_status = student.payment_status || "Ожидает";
      student.lessons = [Object.assign({}, first, { num: 1, status: "completed" })].concat(planned);

      student.archived_packages = [{
        label: "Сентябрь · пилот · 3/3 · 10 500 ₽",
        lessons: ["2026-09-07", "2026-09-10", "2026-09-11"]
          .map(function (date, index) {
            const lesson = byDate[date];
            if (!lesson) return null;
            return {
              num: index + 1,
              date: lesson.date,
              status: lesson.status || "completed",
              topic: lesson.topic || "",
              homework: lesson.homework || null,
              url: lesson.homework && lesson.homework.modules && lesson.homework.modules[0] ? lesson.homework.modules[0].url : "",
              title: lesson.homework && lesson.homework.modules && lesson.homework.modules[0] ? lesson.homework.modules[0].title : "Открыть"
            };
          })
          .filter(Boolean)
      }];

      const payments = [
        { month: "Сентябрь · пилот", package: "3 × 3 500 ₽", amount: "10 500 ₽", status: "paid", date: null, note: "пилотные уроки" },
        { month: "Октябрь 2026", package: "10 × 3 500 ₽", amount: "35 000 ₽", status: "pending", date: null, note: "активный абонемент · 1/10" }
      ];
      student.payments = payments;
      data.payments = payments;
    });
    return data;
  }

  function _archiveLessonFrom(lesson, num) {
    if (!lesson) return null;
    return {
      num: num,
      date: lesson.date,
      status: lesson.status || "completed",
      topic: lesson.topic || "",
      homework: lesson.homework || null,
      url: lesson.homework && lesson.homework.modules && lesson.homework.modules[0] ? lesson.homework.modules[0].url : "",
      title: lesson.homework && lesson.homework.modules && lesson.homework.modules[0] ? lesson.homework.modules[0].title : "Открыть"
    };
  }

  function _normalizeCloseOfDay20260915(data) {
    if (!data || !Array.isArray(data.students)) return data;
    const twinSlugs = {
      "ekaterina-medvedeva-solo": true,
      "maria-kuznetsova-solo": true
    };

    data.students.forEach(function (student) {
      if (!student || !Array.isArray(student.lessons)) return;
      const lessons = student.lessons;
      const byDate = {};
      lessons.forEach(function (lesson) {
        if (lesson && lesson.date) byDate[lesson.date] = lesson;
      });

      if (twinSlugs[student.slug]) {
        const activeDates = ["2026-09-15", "2026-09-22", "2026-09-29"];
        const activeLessons = activeDates.map(function (date, index) {
          const lesson = byDate[date] || { date: date };
          return Object.assign({}, lesson, {
            num: index + 1,
            status: index === 0 ? "completed" : "planned",
            topic: lesson.topic || null,
            homework: lesson.homework || null
          });
        });
        const archiveDates = ["2026-08-13", "2026-08-16", "2026-09-01", "2026-09-03", "2026-09-08", "2026-09-10"];
        const archiveLessons = archiveDates
          .map(function (date, index) { return _archiveLessonFrom(byDate[date], index + 1); })
          .filter(Boolean);

        student.subscription_month = "2026-09";
        student.subscription_span_start = "2026-09-15";
        student.subscription_span_end = "2026-09-29";
        student.lessons_in_package = 3;
        student.lessons_used_this_month = 1;
        student.payment_status = "Оплачено";
        student.lessons = activeLessons;
        student.archived_packages = [{
          label: "Август–сентябрь · закрытый пакет · 6/6",
          lessons: archiveLessons
        }];
        return;
      }

      if (student.slug === "sova-elena") {
        const activeDates = ["2026-09-15", "2026-09-16", "2026-09-23", "2026-09-30"];
        student.subscription_span_start = "2026-09-15";
        student.subscription_span_end = "2026-09-30";
        student.lessons_in_package = 4;
        student.lessons_used_this_month = 1;
        student.lessons = activeDates.map(function (date, index) {
          const lesson = byDate[date] || { date: date };
          return Object.assign({}, lesson, {
            num: index + 1,
            status: index === 0 ? "completed" : "planned"
          });
        });
      }
    });
    return data;
  }

  window.NGE_DATA_PROMISE = (async function boot() {
    // 1) Быстрый путь: свежий кэш в sessionStorage
    const cached = readCache();
    if (cached) {
      _ensurePayment(cached);
      _normalizeAleksandraLyubaeva(cached);
      _normalizeCloseOfDay20260915(cached);
      window.NGE_DATA = cached;
      return cached;
    }

    // 2) По сессии выбираем endpoint
    const session = readSession();
    try {
      if (session && session.role === "teacher" && session.teacher_password) {
        const data = await callFn("all-data", { teacher_password: session.teacher_password });
        _ensurePayment(data);
        _normalizeAleksandraLyubaeva(data);
        _normalizeCloseOfDay20260915(data);
        writeCache(data);
        window.NGE_DATA = data;
        return data;
      }
      if (session && session.pin) {
        const data = await callFn("family-data", { pin: session.pin });
        _ensurePayment(data);
        _normalizeAleksandraLyubaeva(data);
        _normalizeCloseOfDay20260915(data);
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
    _ensurePayment(data);
    _normalizeAleksandraLyubaeva(data);
    _normalizeCloseOfDay20260915(data);
    writeCache(data);
    window.NGE_DATA = data;
  };
  window.NGE_DATA_INVALIDATE = function () {
    try { sessionStorage.removeItem(CACHE_KEY); } catch (_) {}
  };
})();
