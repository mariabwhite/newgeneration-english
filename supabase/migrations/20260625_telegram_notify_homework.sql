-- ============================================================================
-- Безопасный путь для TG-уведомлений когда ученик прислал домашку.
-- БЕЗ AI Hub. БЕЗ Bot token в фронте. Полностью внутри Supabase.
--
-- Архитектура:
--   1. pg_net extension даёт PostgreSQL возможность делать HTTP-запросы
--   2. Bot token хранится в Supabase Vault (encrypted)
--   3. AFTER INSERT trigger на lab_submissions ловит section_id='homework-batch'
--   4. Trigger зовёт https://api.telegram.org/bot<token>/sendMessage
--   5. Маша получает сообщение в чат сразу после того как ученик жмёт «Отправить»
--
-- НЕ применять автоматически — Маша применяет один раз когда хочет включить.
--
-- ШАГИ ПРИМЕНЕНИЯ (Маша делает один раз через Supabase SQL editor):
-- ============================================================================
--
-- ШАГ 1 — включить расширения (если не включены):
--   create extension if not exists pg_net with schema extensions;
--   create extension if not exists supabase_vault with schema vault;
--
-- ШАГ 2 — положить секреты в Vault (один раз).
--   Замени <BOT_TOKEN> на свой токен от @BotFather (формат 1234567:AAA-BBB...)
--   Chat ID Маши уже известен из reference_ai_hub: 335307188
--
--   select vault.create_secret('<BOT_TOKEN>', 'telegram_bot_token');
--   select vault.create_secret('335307188',  'telegram_chat_id');
--
-- ШАГ 3 — применить функцию + триггер ниже (paste этот файл целиком).
-- ============================================================================

create or replace function public.notify_homework_to_telegram()
returns trigger
language plpgsql
security definer
set search_path = public, extensions, vault
as $$
declare
  bot_token text;
  chat_id   text;
  msg       text;
  pretty_lesson text;
  student_label text;
  items_n int;
  request_id bigint;
begin
  -- Только batches домашки
  if new.section_id is null or new.section_id <> 'homework-batch' then
    return new;
  end if;

  -- Достаём секреты из vault
  select decrypted_secret into bot_token from vault.decrypted_secrets where name = 'telegram_bot_token' limit 1;
  select decrypted_secret into chat_id   from vault.decrypted_secrets where name = 'telegram_chat_id'   limit 1;

  if bot_token is null or chat_id is null then
    return new;
  end if;

  items_n := coalesce(jsonb_array_length(new.misses), 0);
  pretty_lesson := replace(replace(new.lesson_path, '/lingua-boost-lab/', ''), '/', ' / ');
  student_label := coalesce(new.student_role, new.room_id);

  msg := '📚 *Новая домашка от ученика*' || E'\n\n' ||
         '👤 ' || coalesce(replace(new.room_id, 'student-', ''), 'unknown') || E'\n' ||
         '📖 урок: `' || pretty_lesson || '`' || E'\n' ||
         '🔢 заданий: *' || items_n || '*' || E'\n' ||
         '🕒 ' || to_char(new.created_at, 'DD.MM HH24:MI') || E'\n\n' ||
         'Открыть: https://cabinet.newgeneration-english.ru/teacher-lab';

  -- Async POST
  select net.http_post(
    url     := 'https://api.telegram.org/bot' || bot_token || '/sendMessage',
    headers := jsonb_build_object('Content-Type', 'application/json'),
    body    := jsonb_build_object(
      'chat_id', chat_id,
      'text',    msg,
      'parse_mode', 'Markdown',
      'disable_web_page_preview', true
    )
  ) into request_id;

  return new;
exception when others then
  -- Ошибки уведомления не должны ломать INSERT
  raise warning 'telegram notify failed: %', SQLERRM;
  return new;
end;
$$;

drop trigger if exists trg_notify_homework on public.lab_submissions;
create trigger trg_notify_homework
  after insert on public.lab_submissions
  for each row
  execute function public.notify_homework_to_telegram();

-- ============================================================================
-- Готово. Теперь как только ученик жмёт «📤 Отправить учителю» в любом уроке —
-- Маше падает сообщение в Telegram чат прямо из Supabase, без посредников.
--
-- Если перестало работать или хочешь сменить токен:
--   select vault.update_secret(<secret_id>, '<NEW_TOKEN>'); -- найти id в vault.secrets
--
-- Если хочешь отключить временно:
--   drop trigger trg_notify_homework on public.lab_submissions;
-- ============================================================================
