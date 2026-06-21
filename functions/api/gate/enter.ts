/**
 * POST /api/gate/enter
 * Body (form-urlencoded): pin=<string>, from=<optional return path>
 *
 * Хэширует входящий PIN, сравнивает с зашитым GATE_PIN_HASH (sha256 константа).
 * При совпадении выдаёт httpOnly cookie nge_gate=exp.hmac.
 * Простой rate-limit через cookie nge_gate_attempts.
 */

interface Env {
  SESSION_SECRET: string;
}

const GATE_PIN_HASH = "b9169d38442158a96b9ab0a9b77a87d830b74ba9b559c94b29d6044bfbee7faa"; // sha256(Watchmaker-2026-Q3)
const COOKIE_NAME = "nge_gate";
const COOKIE_TTL_SECONDS = 60 * 60 * 24 * 30;
const MAX_ATTEMPTS = 5;
const ATTEMPT_WINDOW_SECONDS = 60 * 15;

function hex(buf: ArrayBuffer): string {
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function sha256(s: string): Promise<string> {
  return hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s)));
}

async function hmac(secret: string, message: string): Promise<string> {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  return hex(await crypto.subtle.sign("HMAC", key, enc.encode(message)));
}

function readCookie(request: Request, name: string): string | null {
  const header = request.headers.get("Cookie") || "";
  for (const part of header.split(";")) {
    const [k, ...v] = part.trim().split("=");
    if (k === name) return v.join("=");
  }
  return null;
}

function safeFrom(from: string | null): string {
  if (!from || !from.startsWith("/")) return "/";
  // не пускаем на эндпоинты gate, чтобы не зациклить
  if (from.startsWith("/enter") || from.startsWith("/api/gate/")) return "/";
  return from;
}

export const onRequestPost: PagesFunction<Env> = async (ctx) => {
  const form = await ctx.request.formData();
  const pin = String(form.get("pin") || "").trim();
  const fromRaw = String(form.get("from") || "/");
  const from = safeFrom(fromRaw);

  // Rate-limit per IP (Cloudflare CF-Connecting-IP).
  const ip = ctx.request.headers.get("CF-Connecting-IP") || "unknown";
  const attemptCookieRaw = readCookie(ctx.request, "nge_gate_attempts") || "0:0";
  const [count, windowStart] = attemptCookieRaw.split(":").map((n) => parseInt(n, 10) || 0);
  const now = Math.floor(Date.now() / 1000);
  let attempts = count;
  let windowAt = windowStart;
  if (now - windowAt > ATTEMPT_WINDOW_SECONDS) {
    attempts = 0;
    windowAt = now;
  }
  if (attempts >= MAX_ATTEMPTS) {
    return new Response("Too many attempts. Try again in 15 minutes.", { status: 429 });
  }

  const inputHash = await sha256(pin);
  if (inputHash !== GATE_PIN_HASH) {
    attempts += 1;
    const back = new URL(ctx.request.url);
    back.pathname = "/enter";
    back.search = "";
    back.searchParams.set("e", "1");
    back.searchParams.set("from", from);
    return new Response(null, {
      status: 302,
      headers: {
        Location: back.toString(),
        "Set-Cookie": `nge_gate_attempts=${attempts}:${windowAt}; Path=/; Max-Age=${ATTEMPT_WINDOW_SECONDS}; HttpOnly; Secure; SameSite=Lax`,
      },
    });
  }

  const exp = Math.floor(Date.now() / 1000) + COOKIE_TTL_SECONDS;
  const sig = await hmac(ctx.env.SESSION_SECRET, String(exp));
  const cookieValue = `${exp}.${sig}`;

  const headers = new Headers();
  headers.set("Location", from);
  headers.append("Set-Cookie", `${COOKIE_NAME}=${cookieValue}; Path=/; Max-Age=${COOKIE_TTL_SECONDS}; HttpOnly; Secure; SameSite=Lax`);
  headers.append("Set-Cookie", `nge_gate_attempts=; Path=/; Max-Age=0`);
  return new Response(null, { status: 302, headers });
};

