-- =============================================================
-- NGE Cabinet — contracts storage extension
-- Применяется ПОСЛЕ supabase-schema.sql
-- Цель: вернуть сканы договоров в кабинеты родителей через приватный Storage bucket
-- =============================================================

-- ---------- 1. Расширяем таблицу contracts ----------
-- contract-запись теперь = ОДИН ФАЙЛ (не один контракт-объект)
-- если у одного ученика несколько страниц договора — несколько строк
alter table public.contracts
  add column if not exists storage_bucket    text default 'contracts',
  add column if not exists storage_path      text,           -- 'andrei-kruglov/01_договор_стр1.pdf'
  add column if not exists original_filename text,           -- '01_договор_стр1.pdf'
  add column if not exists mime_type         text,
  add column if not exists file_size         bigint,
  add column if not exists doc_type          text;           -- 'договор' / 'согласие_на_ПД' / 'доп'

create index if not exists contracts_storage_path_idx on public.contracts(storage_path);

-- ---------- 2. Storage RLS: parents видят свои файлы ----------
-- Bucket 'contracts' создаётся в UI Supabase (private). После создания — эти политики работают.

drop policy if exists "contracts storage: teacher all"        on storage.objects;
drop policy if exists "contracts storage: parent select own"  on storage.objects;
drop policy if exists "contracts storage: student select own" on storage.objects;

-- Учитель — полный доступ ко всему bucket
create policy "contracts storage: teacher all"
  on storage.objects for all
  using (bucket_id = 'contracts' and public.is_teacher())
  with check (bucket_id = 'contracts' and public.is_teacher());

-- Родитель — видит только файлы своего ребёнка (путь начинается со slug ученика)
create policy "contracts storage: parent select own"
  on storage.objects for select
  using (
    bucket_id = 'contracts'
    and exists (
      select 1
      from public.student_parent sp
      join public.parents  p on p.id = sp.parent_id
      join public.students s on s.id = sp.student_id
      where p.profile_id = auth.uid()
        and storage.objects.name like s.slug || '/%'
    )
  );

-- Студент (если у него есть login) — видит свои файлы
create policy "contracts storage: student select own"
  on storage.objects for select
  using (
    bucket_id = 'contracts'
    and exists (
      select 1 from public.students s
      where s.profile_id = auth.uid()
        and storage.objects.name like s.slug || '/%'
    )
  );

-- =============================================================
-- DONE.
-- Дальше: создать bucket 'contracts' (private) в UI Supabase
-- → запустить scripts/upload-contracts.js
-- =============================================================
