import {
  getSessionToken,
  loadPublishedLessons,
  loadVaultVersion,
  verifySession,
} from "../_shared/premium-auth.js";

export async function onRequestGet(context) {
  const { request, env } = context;
  try {
    const token = getSessionToken(request);
    const session = await verifySession(env, token);
    if (!session) {
      return Response.json({ ok: false, error: "UNAUTHORIZED" }, { status: 401 });
    }

    const [lessons, version] = await Promise.all([
      loadPublishedLessons(request),
      loadVaultVersion(request),
    ]);

    return Response.json(
      {
        ok: true,
        version,
        lessons,
      },
      {
        headers: {
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
