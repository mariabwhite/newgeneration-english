/**
 * /api/ai-feedback — Cloudflare Pages Function
 * Прокси на Cloudflare Workers AI (Llama 3.1 8B Instruct).
 * Бесплатно, без ключей, тот же origin что сайт (нет иностранщины).
 */

const SYSTEM_PROMPT = `You are a warm, precise English tutor giving feedback to a Russian-speaking teenager (B1 level) right after they submitted a section of an OGE / B1 mock lesson.
Style: friendly but never cheerful-fake; concrete, not generic; reply in Russian.
Length: 4–7 short sentences, no padding.
Always include:
- 1 sentence: "что получилось" (anchor on a real correct answer if provided)
- 1–2 sentences: главную ошибку (the specific item id + correct form)
- 1 sentence: micro-rule reminder (e.g. "after enjoy → Ving", "passive = be + V3")
- 1 sentence: что делать на следующем уроке.
Never invent answers that weren't provided. If the user submitted only correct ones — congratulate briefly and suggest the next harder topic from the lesson.`;

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const payload = await request.json();
    const userContent = String(payload.userContent || payload.content || '').slice(0, 4000);
    const model = payload.model || '@cf/meta/llama-3.1-8b-instruct';

    if (!userContent.trim()) {
      return new Response(JSON.stringify({ error: 'empty content' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    if (!env.AI) {
      return new Response(JSON.stringify({
        error: 'AI binding not configured',
        hint: 'Add AI binding in Cloudflare Pages dashboard or wrangler.toml'
      }), { status: 500, headers: { 'Content-Type': 'application/json' } });
    }

    const result = await env.AI.run(model, {
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user',   content: userContent }
      ],
      max_tokens: 600,
      temperature: 0.7
    });

    const text = result?.response || result?.result?.response || '';
    if (!text || !text.trim()) {
      throw new Error('Empty AI response');
    }

    return new Response(JSON.stringify({
      text: text.trim(),
      model
    }), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
      }
    });

  } catch (e) {
    return new Response(JSON.stringify({
      error: e.message || 'AI failed',
      fallback: 'Молодец, что прислала! На следующем уроке разберём подробнее.'
    }), {
      status: 200,  // fallback вместо хард-фейла
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}
