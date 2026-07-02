import { getSessionToken, loadPublishedLessons, verifySession } from "./_shared/premium-auth.js";

function normalizePremiumPath(value, origin) {
  try {
    const url = new URL(value || "", origin);
    let path = url.pathname;
    if (!path.startsWith("/lingua-boost-lab/")) return "";
    if (path.endsWith("/index.html")) path = path.slice(0, -10);
    if (!path.endsWith("/") && !/\.[a-z0-9]+$/i.test(path)) path += "/";
    return path;
  } catch {
    return "";
  }
}

function isLabServicePath(pathname) {
  if (!pathname.startsWith("/lingua-boost-lab/")) return true;
  if (pathname.startsWith("/lingua-boost-lab/assets/")) return true;
  return [
    "/lingua-boost-lab/login.html",
    "/lingua-boost-lab/premium.html",
    "/lingua-boost-lab/premium-lessons.json",
  ].includes(pathname);
}

async function isPublishedPremiumPath(request, pathname) {
  if (isLabServicePath(pathname)) return false;
  const origin = new URL(request.url).origin;
  const lessonBase = `${origin}/lingua-boost-lab/`;
  const here = normalizePremiumPath(pathname, origin);
  if (!here) return false;
  const lessons = await loadPublishedLessons(request);
  return lessons.some((lesson) => normalizePremiumPath(lesson && lesson.url, lessonBase) === here);
}

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  let shouldProtect = false;
  try {
    shouldProtect = await isPublishedPremiumPath(request, url.pathname);
  } catch (error) {
    shouldProtect = false;
  }

  if (!shouldProtect) {
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
