/**
 * NGE gate middleware
 *
 * Защищает все маршруты под /lingua-boost-lab/* и /cabinet/*.
 * Если в запросе нет валидной cookie nge_gate — редирект на /enter с возвратным URL.
 *
 * Cookie nge_gate = "<expEpochSeconds>.<hmacSHA256(exp, env.SESSION_SECRET)>"
 * Срок — 30 дней.
 */

interface Env {
  SESSION_SECRET: string;
}

const PROTECTED_PREFIXES = ["/lingua-boost-lab/", "/cabinet/"];
const COOKIE_NAME = "nge_gate";
const COOKIE_TTL_SECONDS = 60 * 60 * 24 * 30;

function isProtected(pathname: string): boolean {
  return PROTECTED_PREFIXES.some((p) => pathname.startsWith(p));
}

function hex(buf: ArrayBuffer): string {
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function hmac(secret: string, message: string): Promise<string> {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign", "verify"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(message));
  return hex(sig);
}

async function verifyCookie(value: string | null, secret: string): Promise<boolean> {
  if (!value) return false;
  const [expStr, sig] = value.split(".");
  if (!expStr || !sig) return false;
  const exp = parseInt(expStr, 10);
  if (!Number.isFinite(exp) || exp < Math.floor(Date.now() / 1000)) return false;
  const expected = await hmac(secret, expStr);
  // constant-time compare not strictly necessary in this threat model, but cheap
  if (expected.length !== sig.length) return false;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) diff |= expected.charCodeAt(i) ^ sig.charCodeAt(i);
  return diff === 0;
}

function readCookie(request: Request, name: string): string | null {
  const header = request.headers.get("Cookie") || "";
  for (const part of header.split(";")) {
    const [k, ...v] = part.trim().split("=");
    if (k === name) return v.join("=");
  }
  return null;
}

export const onRequest: PagesFunction<Env> = async (ctx) => {
  const url = new URL(ctx.request.url);

  // Не трогаем сами api-эндпоинты gate (forms) и страницу входа.
  if (url.pathname === "/enter" || url.pathname.startsWith("/api/gate/")) {
    return ctx.next();
  }

  if (!isProtected(url.pathname)) {
    return ctx.next();
  }

  const cookie = readCookie(ctx.request, COOKIE_NAME);
  const ok = await verifyCookie(cookie, ctx.env.SESSION_SECRET);
  if (ok) return ctx.next();

  // Не пускаем — редирект на /enter с возвратом.
  const target = new URL("/enter", url);
  target.searchParams.set("from", url.pathname + url.search);
  return Response.redirect(target.toString(), 302);
};

// Хелперы экспортируются для api/gate/enter.ts.
export { hmac, COOKIE_NAME, COOKIE_TTL_SECONDS };
