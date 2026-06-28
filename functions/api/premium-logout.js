import { clearCookie, getSessionToken, revokeSession, safeNextUrl } from "../_shared/premium-auth.js";

export async function onRequest(context) {
  const { request, env } = context;
  const token = getSessionToken(request);
  if (token) {
    await revokeSession(env, token).catch(() => {});
  }

  const url = new URL(request.url);
  const rawNext = url.searchParams.get("next");
  const resolvedNext = rawNext ? safeNextUrl(rawNext, url.origin) : "";
  const next = resolvedNext && resolvedNext !== "/lingua-boost-lab/premium.html"
    ? resolvedNext
    : "/lingua-boost-lab/login.html";
  return new Response(null, {
    status: 302,
    headers: {
      Location: new URL(next, url.origin).toString(),
      "Set-Cookie": clearCookie(),
      "Cache-Control": "no-store",
    },
  });
}
