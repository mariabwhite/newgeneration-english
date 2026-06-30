/**
 * GET /api/homework/feed?pin=XXXX&limit=50
 * Учитель видит ленту последних submissions.
 * Простая защита: PIN учителя через query.
 */
const TEACHER_PIN = '7777'; // временный PIN для учителя

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const pin = url.searchParams.get('pin');
  const limit = Math.min(200, Math.max(1, parseInt(url.searchParams.get('limit') || '50', 10)));

  if (pin !== TEACHER_PIN) {
    return new Response(JSON.stringify({ error: 'unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  if (!env.NG) {
    return new Response(JSON.stringify({ error: 'D1 binding NG not configured' }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const result = await env.NG.prepare(`
      SELECT id, student_name, student_id, lesson_path, lesson_title, section_id,
             items_json, score, total, pct, misses_json, created_at
      FROM submissions
      ORDER BY created_at DESC
      LIMIT ?
    `).bind(limit).all();

    return new Response(JSON.stringify({
      ok: true,
      count: result.results?.length || 0,
      submissions: result.results || []
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
      }
    });

  } catch (e) {
    return new Response(JSON.stringify({
      error: 'DB read failed',
      detail: e.message
    }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
}
