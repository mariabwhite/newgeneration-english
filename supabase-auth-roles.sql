-- =============================================================
-- NGE Cabinet — auth roles delta
-- Применяется ПОСЛЕ supabase-schema.sql
-- Цель: чтобы при первом входе Маши (teacher) её профиль создавался
-- с role='teacher', а не default 'student'.
-- =============================================================

create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
declare
  user_role role_t := 'student';
begin
  -- Teacher emails (Маша)
  if new.email in ('maria.v.burtseva@gmail.com', 'whitenois@mail.ru') then
    user_role := 'teacher';
  end if;

  -- Parent emails (из data.js) — назначаем role='parent'
  if new.email in (
    'elenavit-2005@mail.ru',          -- Сова Елена (взрослая ученица — но мы пометим как parent для семейного входа)
    'meet.me.here@mail.ru'            -- Изотова Ольга Игоревна
    -- остальные родительские emails сюда же когда соберём
  ) then
    user_role := 'parent';
  end if;

  insert into public.profiles (id, role, email, full_name)
  values (new.id, user_role, new.email, coalesce(new.raw_user_meta_data->>'full_name', new.email))
  on conflict (id) do update set role = excluded.role, email = excluded.email;

  return new;
end; $$;

-- При повторном применении — пересоздать триггер чтобы взял новую функцию
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- =============================================================
-- DONE.
-- =============================================================
