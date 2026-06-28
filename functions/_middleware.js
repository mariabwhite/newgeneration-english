import { getSessionToken, isPremiumPath, verifySession } from "./_shared/premium-auth.js";

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  if (!isPremiumPath(url.pathname)) {
    return context.next();
  }

  try {
    const token = getSessionToken(request);
    const session = await verifySession(env, token);
    if (session) return context.next();
  } catch {
    // fall through to redirect
  }

  const loginUrl = new URL("/lingua-boost-lab/login.html", url.origin);
  loginUrl.searchParams.set("next", url.pathname + url.search + url.hash);
  return Response.redirect(loginUrl, 302);
}
