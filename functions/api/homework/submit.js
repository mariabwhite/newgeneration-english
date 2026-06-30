/**
 * POST /api/homework/submit
 * Ученик присылает домашку → пишем в D1 (binding NG)
 *
 * Body JSON:
 * {
 *   student_name: "Катя Медведева",
 *   student_id?: "ekaterina-medvedeva-solo",
 *   lesson_path: "/lingua-boost-lab/b1/oge-mock-mix-01/",
 *   lesson_title?: "OGE Mock #1",
 *   section_id?: "block-practice-grammar",
 *   items: [{ question, kind, correct, student_answer, ok }, ...],
 *   score?: 8,
 *   total?: 10,
 *   pct?: 80,
 *   misses?: ["item-1: didn't read → hadn't read", ...]
 * }
 */
export async function onRequestPost(context) {
  const { request, env } = context;

  if (!env.NG) {
    return new Response(JSON.stringify({
      error: 'D1 binding NG not configured'
    }), { status: 500, headers: jsonHeaders() });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON' }), {
      status: 400, headers: jsonHeaders()
    });
  }

  const student_name = String(body.student_name || '').trim().slice(0, 120);
  const lesson_path  = String(body.lesson_path || '').trim().slice(0, 300);

  if (!student_name || !lesson_path) {
    return new Response(JSON.stringify({
      error: 'student_name and lesson_path are required'
    }), { status: 400, headers: jsonHeaders() });
  }

  const items_json = JSON.stringify(Array.isArray(body.items) ? body.items : []);
  const misses_json = body.misses ? JSON.stringify(body.misses) : null;
  const ua = String(request.headers.get('user-agent') || '').slice(0, 300);

  try {
    const result = await env.NG.prepare(`
      INSERT INTO submissions
        (student_name, student_id, lesson_path, lesson_title, section_id,
         items_json, score, total, pct, misses_json, created_at, user_agent)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      student_name,
      body.student_id || null,
      lesson_path,
      body.lesson_title || null,
      body.section_id || null,
      items_json,
      Number(body.score) || 0,
      Number(body.total) || 0,
      Number(body.pct) || 0,
      misses_json,
      Math.floor(Date.now() / 1000),
      ua
    ).run();

    return new Response(JSON.stringify({
      ok: true,
      id: result.meta?.last_row_id || null,
      message: 'Домашка отправлена учителю'
    }), { headers: jsonHeaders() });

  } catch (e) {
    return new Response(JSON.stringify({
      error: 'DB write failed',
      detail: e.message
    }), { status: 500, headers: jsonHeaders() });
  }
}

export async function onRequestOptions() {
  return new Response(null, { headers: corsHeaders() });
}

function jsonHeaders() {
  return {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Cache-Control': 'no-store'
  };
}

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };
}
