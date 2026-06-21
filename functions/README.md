# Cloudflare Pages Functions · NGE gate

Эта папка — server-side functions для newgeneration-english.ru.

## Что они делают

`_middleware.ts` запускается на **каждом** запросе к сайту. Логика:
- Открытые пути (главная, программы, путеводитель, etc.) — пропускаем без проверки.
- Защищённые пути (`/lingua-boost-lab/*` и `/cabinet/*`) — требуем cookie `nge_gate`.
- Cookie выдаётся при правильном PIN на `/enter` → POST `/api/gate/enter`.
- Срок cookie — 30 дней.

## Что Маша должна сделать в Cloudflare dashboard (одноразово)

1. Открыть https://dash.cloudflare.com → Workers & Pages → выбрать проект `newgeneration-english`.
2. **Settings → Environment variables → Production → Add variable:**
   - Variable name: `SESSION_SECRET`
   - Value: `mjoXyrPBve3L8u4e6SqsYgxuVlQhIQubBwVKTasvXzimZnWS2NhWISOxmgR_suhZ`
   - Type: **Encrypt** (галочка) — чтобы значение спряталось после сохранения.
3. Save → Cloudflare сам передеплоит проект через ~1 минуту.

После этого:
- `https://newgeneration-english.ru/lingua-boost-lab/…` → редирект на `/enter`.
- Ввести PIN `Watchmaker-2026-Q3` → возврат к запрошенной странице, cookie на 30 дней.

## Как сбросить cookie вручную (если PIN сменится)

В DevTools → Application → Cookies → найти `nge_gate` → удалить. Или зайти в режиме инкогнито.

## Что ещё в коде живёт

- `GATE_PIN_HASH` в `api/gate/enter.ts` = sha256 текущего gate-PIN. Если PIN ротируется — пересчитать хэш и закоммитить.
- Rate-limit: 5 неправильных попыток / 15 минут / IP. Хранится в cookie `nge_gate_attempts`.
- `SESSION_SECRET` НЕ должен попасть в git — он только в Cloudflare env vars.
