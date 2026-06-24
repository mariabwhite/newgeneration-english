-- Migration · Lab двусторонний сэйв
-- Run: supabase db push (или paste в Supabase SQL editor)

create table if not exists public.lab_submissions (
  id uuid primary key default gen_random_uuid(),
  room_id text not null,
  lesson_path text not null,
  section_id text,
  section_title text,
  student_role text default 'student',
  score int not null default 0,
  total int not null default 0,
  pct int generated always as (case when total > 0 then (score * 100) / total else 0 end) stored,
  misses jsonb default '[]'::jsonb,
  wpm int,
  created_at timestamptz default now()
);

create index if not exists lab_subs_room_time on public.lab_submissions (room_id, created_at desc);
create index if not exists lab_subs_lesson_time on public.lab_submissions (lesson_path, created_at desc);

-- RLS · открыто для anon · room_id = capability token, защищается длиной/непредсказуемостью
alter table public.lab_submissions enable row level security;

drop policy if exists "lab_subs_insert_anon" on public.lab_submissions;
create policy "lab_subs_insert_anon" on public.lab_submissions
  for insert to anon, authenticated
  with check (true);

drop policy if exists "lab_subs_select_anon" on public.lab_submissions;
create policy "lab_subs_select_anon" on public.lab_submissions
  for select to anon, authenticated
  using (true);
