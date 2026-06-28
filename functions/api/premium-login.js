import {
  buildCookie,
  createSession,
  loadPublishedLessons,
  loadVaultVersion,
  safeNextUrl,
  verifyPin,
} from "../_shared/premium-auth.js";

export async function onRequestPost(context) {
  const { request, env } = context;
  const contentType = request.headers.get("content-type") || "";
  const origin = new URL(request.url).origin;
  let pin = "";
  let next = "";

  if (contentType.includes("application/json")) {
    const body = await request.json().catch(() => ({}));
    pin = String(body.pin || "").trim();
    next = String(body.next || "");
  } else {
    const form = await request.formData();
    pin = String(form.get("pin") || "").trim();
    next = String(form.get("next") || "");
  }

  if (!pin) {
    return Response.json({ ok: false, error: "PIN_REQUIRED" }, { status: 400 });
  }

  try {
    const state = await verifyPin(env, pin);
    if (!state) {
      return Response.json({ ok: false, error: "PIN_INVALID" }, { status: 401 });
    }

    const sessionTtl = Number(state.session_ttl_seconds || 0) || 60 * 60 * 24 * 30;
    const session = await createSession(env, state.gate_version, sessionTtl);
    const redirectTo = safeNextUrl(next, origin);
    const [lessons, version] = await Promise.all([
      loadPublishedLessons(request),
      loadVaultVersion(request),
    ]);

    return Response.json(
      {
        ok: true,
        redirectTo,
        version,
        gateVersion: state.gate_version,
        lessons,
      },
      {
        headers: {
          "Set-Cookie": buildCookie(session.token, sessionTtl),
          "Cache-Control": "no-store",
        },
      },
    );
  } catch (error) {
    return Response.json(
      { ok: false, error: "SERVER_ERROR", message: error.message },
      { status: 500 },
    );
  }
}
