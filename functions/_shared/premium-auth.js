const COOKIE_NAME = "ngp_session";
const DEFAULT_SESSION_TTL_SECONDS = 60 * 60 * 24 * 30;
const GATE_TABLE = "premium_gate_state";
const SESSION_TABLE = "premium_sessions";
const LESSONS_URL = "/lingua-boost-lab/premium-lessons.json";
const PREMIUM_HTML_URL = "/lingua-boost-lab/premium.html";

function requireEnv(env) {
  if (!env?.SUPABASE_URL || !env?.SUPABASE_SERVICE_ROLE_KEY) {
    throw new Error("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY");
  }
}

function supabaseHeaders(env, extra = {}) {
  requireEnv(env);
  return {
    apikey: env.SUPABASE_SERVICE_ROLE_KEY,
    Authorization: `Bearer ${env.SUPABASE_SERVICE_ROLE_KEY}`,
    Accept: "application/json",
    "Content-Type": "application/json",
    ...extra,
  };
}

async function supabaseJson(env, path, init = {}) {
  const response = await fetch(`${env.SUPABASE_URL}${path}`, {
    ...init,
    headers: supabaseHeaders(env, init.headers || {}),
  });
  const text = await response.text();
  if (!response.ok) {
    throw new Error(`Supabase ${response.status}: ${text.slice(0, 200)}`);
  }
  return text ? JSON.parse(text) : null;
}

export function parseCookies(header) {
  const cookies = {};
  if (!header) return cookies;
  for (const part of header.split(";")) {
    const idx = part.indexOf("=");
    if (idx === -1) continue;
    const name = part.slice(0, idx).trim();
    const value = part.slice(idx + 1).trim();
    if (name) cookies[name] = value;
  }
  return cookies;
}

export function getSessionToken(request) {
  return parseCookies(request.headers.get("Cookie") || "")[COOKIE_NAME] || "";
}

export function isPremiumPath(pathname) {
  if (!pathname.startsWith("/lingua-boost-lab/")) return false;
  if (pathname.startsWith("/lingua-boost-lab/assets/")) return false;
  if (pathname.startsWith("/lingua-boost-lab/api/")) return false;
  return ![
    "/lingua-boost-lab/login.html",
    "/lingua-boost-lab/premium.html",
    "/lingua-boost-lab/premium-lessons.json",
  ].includes(pathname);
}

export function safeNextUrl(rawNext, origin) {
  if (!rawNext) return "/lingua-boost-lab/premium.html";
  try {
    const url = new URL(rawNext, origin);
    if (url.origin !== origin) return "/lingua-boost-lab/premium.html";
    if (!url.pathname.startsWith("/lingua-boost-lab/")) return "/lingua-boost-lab/premium.html";
    if (url.pathname.endsWith("/login.html")) return "/lingua-boost-lab/premium.html";
    return url.pathname + url.search + url.hash;
  } catch {
    return "/lingua-boost-lab/premium.html";
  }
}

export async function sha256Hex(value) {
  const bytes = new TextEncoder().encode(value);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

export async function loadGateState(env) {
  const rows = await supabaseJson(
    env,
    `/rest/v1/${GATE_TABLE}?select=id,active,pin_salt,pin_hash,gate_version,session_ttl_seconds&limit=1`,
  );
  const state = Array.isArray(rows) ? rows[0] : null;
  if (!state) throw new Error("Premium gate state missing");
  return state;
}

export async function verifyPin(env, pin) {
  const state = await loadGateState(env);
  if (!state.active) return null;
  const candidate = await sha256Hex(`${state.pin_salt}:${pin}`);
  if (candidate !== state.pin_hash) return null;
  return state;
}

export async function createSession(env, gateVersion, ttlSeconds) {
  const token = crypto.randomUUID();
  const expiresAt = new Date(Date.now() + ttlSeconds * 1000).toISOString();
  await supabaseJson(env, `/rest/v1/${SESSION_TABLE}`, {
    method: "POST",
    body: JSON.stringify({
      token,
      gate_version: gateVersion,
      expires_at: expiresAt,
    }),
    headers: {
      Prefer: "return=minimal",
    },
  });
  return { token, expiresAt };
}

export async function getSession(env, token) {
  const rows = await supabaseJson(
    env,
    `/rest/v1/${SESSION_TABLE}?select=token,gate_version,expires_at,revoked_at&token=eq.${encodeURIComponent(token)}&limit=1`,
  );
  return Array.isArray(rows) ? rows[0] || null : null;
}

export async function verifySession(env, token) {
  if (!token) return null;
  const state = await loadGateState(env);
  const session = await getSession(env, token);
  if (!session) return null;
  if (session.revoked_at) return null;
  if (Number(session.gate_version) !== Number(state.gate_version)) return null;
  if (Date.parse(session.expires_at) <= Date.now()) return null;
  return { state, session };
}

export async function revokeSession(env, token) {
  if (!token) return;
  await supabaseJson(env, `/rest/v1/${SESSION_TABLE}?token=eq.${encodeURIComponent(token)}`, {
    method: "DELETE",
    headers: {
      Prefer: "return=minimal",
    },
  });
}

export function buildCookie(token, ttlSeconds) {
  const secure = typeof location !== "undefined" ? location.protocol === "https:" : true;
  const parts = [
    `${COOKIE_NAME}=${token}`,
    "Path=/",
    "HttpOnly",
    "SameSite=Lax",
    `Max-Age=${ttlSeconds}`,
  ];
  if (secure) parts.push("Secure");
  return parts.join("; ");
}

export function clearCookie() {
  const secure = typeof location !== "undefined" ? location.protocol === "https:" : true;
  const parts = [
    `${COOKIE_NAME}=`,
    "Path=/",
    "HttpOnly",
    "SameSite=Lax",
    "Max-Age=0",
    "Expires=Thu, 01 Jan 1970 00:00:00 GMT",
  ];
  if (secure) parts.push("Secure");
  return parts.join("; ");
}

export async function loadPublishedLessons(request) {
  const response = await fetch(new URL(LESSONS_URL, request.url), {
    headers: { Accept: "application/json" },
    cache: "no-store",
  });
  if (!response.ok) throw new Error(`Unable to load premium lessons: ${response.status}`);
  const lessons = await response.json();
  return lessons.filter((lesson) => lesson.published !== false);
}

export async function loadVaultVersion(request) {
  const response = await fetch(new URL(PREMIUM_HTML_URL, request.url), {
    headers: { Accept: "text/html" },
    cache: "no-store",
  });
  if (!response.ok) throw new Error(`Unable to load premium.html: ${response.status}`);
  const html = await response.text();
  const match = html.match(/<meta name="vault-version" content="([^"]+)">/);
  return match ? match[1] : "v0";
}
