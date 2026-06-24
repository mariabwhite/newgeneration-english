// supabase/functions/lab-ai-review/index.ts
// Deploy: supabase functions deploy lab-ai-review --no-verify-jwt
// Set secret: supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
//
// Accepts POST { mode: "writing"|"speaking", text|transcript, target?, wpm?, lesson }
// Returns { review: "<markdown разбор>" }

import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const ANTHROPIC_API_KEY = Deno.env.get("ANTHROPIC_API_KEY") ?? "";
const MODEL = "claude-opus-4-7";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function systemPrompt(mode: string): string {
  return `Ты — мягкий, но точный преподаватель английского. Разбираешь ответ ученика B1+ на русском.
Формат разбора:
- 4-7 пунктов
- каждый: «<цитата ошибки> → <правильный вариант>» + 1 строка пояснения по-русски
- категории: части речи, времена, предлоги, порядок слов, лексика, естественность
- если ошибок нет — короткая похвала + 1-2 совета как сделать звучнее
${mode === "speaking" ? "- учти, что это распознанная речь (могут быть огрехи распознавания, не считай их ошибками произношения)" : ""}
- НЕ переписывай весь текст, разбирай только проблемные места
- 6-8 строк максимум`;
}

function userPrompt(payload: any): string {
  if (payload.mode === "writing") {
    return `Ученик написал:\n\n"${payload.text}"\n\nРазбери.`;
  }
  if (payload.mode === "speaking") {
    let prompt = `Ученик произнёс (распознано через Web Speech):\n\n"${payload.transcript}"`;
    if (payload.target) prompt += `\n\nЦелевая фраза была: "${payload.target}"`;
    if (payload.wpm) prompt += `\n\nСкорость: ${payload.wpm} WPM (норма 130-160)`;
    return prompt + "\n\nРазбери произношение/грамматику цитатами + дай рекомендацию.";
  }
  return JSON.stringify(payload);
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return new Response("POST only", { status: 405, headers: CORS });

  if (!ANTHROPIC_API_KEY) {
    return new Response(JSON.stringify({ error: "ANTHROPIC_API_KEY not set in Supabase secrets" }), {
      status: 500, headers: { ...CORS, "Content-Type": "application/json" }
    });
  }

  let payload: any;
  try { payload = await req.json(); }
  catch { return new Response(JSON.stringify({ error: "bad json" }), { status: 400, headers: { ...CORS, "Content-Type": "application/json" } }); }

  if (!payload.mode || (!payload.text && !payload.transcript)) {
    return new Response(JSON.stringify({ error: "mode + text|transcript required" }), { status: 400, headers: { ...CORS, "Content-Type": "application/json" } });
  }

  const aResp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 800,
      system: systemPrompt(payload.mode),
      messages: [{ role: "user", content: userPrompt(payload) }],
    }),
  });

  if (!aResp.ok) {
    const t = await aResp.text();
    return new Response(JSON.stringify({ error: "anthropic " + aResp.status + ": " + t.slice(0, 300) }), {
      status: 502, headers: { ...CORS, "Content-Type": "application/json" }
    });
  }
  const data = await aResp.json();
  const review = data?.content?.[0]?.text ?? "(пустой ответ)";

  return new Response(JSON.stringify({ review, model: MODEL }), {
    status: 200, headers: { ...CORS, "Content-Type": "application/json" }
  });
});
