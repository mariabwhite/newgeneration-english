-- ОПЦИОНАЛЬНАЯ миграция · отдельная таблица для домашки
-- НЕ обязательно применять — homework сейчас пишется в lab_submissions
-- с section_id='homework-batch'. Эта миграция нужна только если Маша
-- захочет разделить аналитику submits и homework на отдельные источники.
--
-- Применить: Supabase SQL editor → paste → Run.

create table if not exists public.lab_homework (
  id uuid primary key default gen_random_uuid(),
  room_id text not null,
  student_name text,
  lesson_path text not null,
  lesson_title text,
  items_count int not null default 0,
  items jsonb not null default '[]'::jsonb,
  status text default 'pending',           -- pending | reviewed | archived
  reviewed_at timestamptz,
  teacher_notes text,
  created_at timestamptz default now()
);

create index if not exists lab_hw_room_time on public.lab_homework (room_id, created_at desc);
create index if not exists lab_hw_lesson_time on public.lab_homework (lesson_path, created_at desc);
create index if not exists lab_hw_status on public.lab_homework (status, created_at desc) where status = 'pending';

alter table public.lab_homework enable row level security;

drop policy if exists "lab_hw_insert_anon" on public.lab_homework;
create policy "lab_hw_insert_anon" on public.lab_homework
  for insert to anon, authenticated
  with check (true);

drop policy if exists "lab_hw_select_anon" on public.lab_homework;
create policy "lab_hw_select_anon" on public.lab_homework
  for select to anon, authenticated
  using (true);

drop policy if exists "lab_hw_update_anon" on public.lab_homework;
create policy "lab_hw_update_anon" on public.lab_homework
  for update to anon, authenticated
  using (true)
  with check (true);
