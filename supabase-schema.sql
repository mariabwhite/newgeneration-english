-- =============================================================
-- NGE Cabinet — Supabase schema
-- Generated: 2026-06-01 by Claude
-- =============================================================
-- Дизайн:
--   • profiles      → обёртка над auth.users + роль (student / parent / teacher)
--   • students      → 12 учеников
--   • parents       → родители (один ученик может иметь несколько родителей; одна
--                     мама может быть родителем нескольких учеников)
--   • subscriptions → месячные абонементы
--   • lessons       → конкретные уроки с датой, статусом, темой
--   • reports       → parent reports + диагностики
--   • contracts     → ТОЛЬКО метаданные (status, signed_date) — файлы не в БД
--   • lab_modules   → каталог Lab-уроков
--   • student_lab_assignments → какие модули какому ученику отданы
-- =============================================================

-- ---------- 0. ENUMS (idempotent) ----------
do $$ begin
  if not exists (select 1 from pg_type where typname = 'role_t') then
    create type role_t as enum ('student','parent','teacher','admin');
  end if;
  if not exists (select 1 from pg_type where typname = 'lesson_status_t') then
    create type lesson_status_t as enum ('planned','completed','missed','cancelled','rescheduled');
  end if;
  if not exists (select 1 from pg_type where typname = 'report_type_t') then
    create type report_type_t as enum ('parent_report','diagnostic','note');
  end if;
  if not exists (select 1 from pg_type where typname = 'report_status_t') then
    create type report_status_t as enum ('draft','ready','sent','archived');
  end if;
  if not exists (select 1 from pg_type where typname = 'contract_status_t') then
    create type contract_status_t as enum ('signed','pending','expired','none');
  end if;
end $$;

-- ---------- 1. PROFILES (роли) ----------
create table if not exists public.profiles (
  id              uuid primary key references auth.users(id) on delete cascade,
  role            role_t not null,
  email           text   not null,
  full_name       text,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

create index if not exists profiles_role_idx on public.profiles(role);

-- ---------- 2. STUDENTS ----------
create table if not exists public.students (
  id                   uuid primary key default gen_random_uuid(),
  slug                 text unique not null,           -- 'yulya-lushina' (для URL)
  notion_id            text,
  name                 text not null,
  nickname             text,
  greeting_student     text,
  greeting_parent      text,
  casual_greeting      boolean default false,
  level                text,
  format               text default 'индивидуально',
  duration             text default '90 мин',
  lessons_per_week     int default 1,
  schedule             text,                            -- 'понедельник 12:00'
  stability_note       text,
  goal                 text,
  price_per_lesson     numeric(10,2),
  monthly_package      numeric(10,2),
  is_adult             boolean default false,
  pair_partner_id      uuid references public.students(id), -- для Кати+Маши
  active               boolean default true,
  profile_id           uuid references public.profiles(id), -- если у ученика есть login
  created_at           timestamptz not null default now(),
  updated_at           timestamptz not null default now()
);

create index if not exists students_active_idx on public.students(active);
create index if not exists students_pair_idx   on public.students(pair_partner_id) where pair_partner_id is not null;

-- ---------- 3. PARENTS ----------
create table if not exists public.parents (
  id              uuid primary key default gen_random_uuid(),
  profile_id      uuid references public.profiles(id), -- login родителя
  full_name       text not null,
  passport        text,                                -- для договоров
  email           text,
  phone           text,
  address         text,
  birthday        date,
  role_label      text default 'primary',              -- primary / secondary
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

create table if not exists public.student_parent (
  student_id      uuid references public.students(id) on delete cascade,
  parent_id       uuid references public.parents(id)  on delete cascade,
  primary key (student_id, parent_id)
);

-- ---------- 4. SUBSCRIPTIONS ----------
create table if not exists public.subscriptions (
  id                    uuid primary key default gen_random_uuid(),
  student_id            uuid not null references public.students(id) on delete cascade,
  month                 text not null,                  -- '2026-06'
  lessons_in_package    int  not null,
  lessons_used          int  not null default 0,
  package_amount        numeric(10,2),
  paid                  boolean default false,
  paid_at               timestamptz,
  payment_note          text,
  created_at            timestamptz not null default now(),
  updated_at            timestamptz not null default now(),
  unique (student_id, month)
);

create index if not exists subscriptions_student_idx on public.subscriptions(student_id);

-- ---------- 5. LESSONS ----------
create table if not exists public.lessons (
  id                  uuid primary key default gen_random_uuid(),
  student_id          uuid not null references public.students(id) on delete cascade,
  subscription_id     uuid references public.subscriptions(id),
  lesson_date         date not null,
  num                 int,                            -- порядковый номер в абонементе
  status              lesson_status_t not null default 'planned',
  topic               text,
  activities          text[],                         -- ['grammar','speaking']
  covered             text,                           -- что прошли
  notes_private       text,                           -- только для учителя
  -- interactive lesson link
  interactive_url     text,                           -- URL урока в Lab
  interactive_title   text,                           -- '🦇 Открыть урок'
  -- homework
  homework_text       text,
  homework_module_url text,
  homework_module_title text,
  homework_done       boolean default false,
  created_at          timestamptz not null default now(),
  updated_at          timestamptz not null default now()
);

create index if not exists lessons_student_date_idx on public.lessons(student_id, lesson_date);
create index if not exists lessons_status_idx       on public.lessons(status);

-- ---------- 6. REPORTS ----------
create table if not exists public.reports (
  id                uuid primary key default gen_random_uuid(),
  student_id        uuid not null references public.students(id) on delete cascade,
  month             text not null,                    -- '2026-05'
  type              report_type_t not null default 'parent_report',
  status            report_status_t not null default 'draft',
  title             text not null,
  recipient_label   text,                             -- 'Ольга Игоревна'
  short_message     text,
  content_markdown  text,
  notion_url        text,
  sent_at           timestamptz,
  created_at        timestamptz not null default now(),
  updated_at        timestamptz not null default now()
);

create index if not exists reports_student_month_idx on public.reports(student_id, month);
create index if not exists reports_status_idx        on public.reports(status);

-- ---------- 7. CONTRACTS (только метаданные!) ----------
create table if not exists public.contracts (
  id              uuid primary key default gen_random_uuid(),
  student_id      uuid not null references public.students(id) on delete cascade,
  parent_id       uuid references public.parents(id),
  status          contract_status_t not null default 'pending',
  signed_date     date,
  note            text,                               -- 'общий договор семьи Сова' и т.д.
  -- Никаких путей к файлам / содержимого / сканов в БД!
  -- Файлы — локально у Маши + Notion-ссылка через note
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

create index if not exists contracts_student_idx on public.contracts(student_id);

-- ---------- 8. LAB MODULES (каталог) ----------
create table if not exists public.lab_modules (
  id              uuid primary key default gen_random_uuid(),
  level           text not null,                      -- 'Pre-A1' / 'A1' / 'B1' …
  title           text not null,
  slug            text unique not null,               -- 'julia-vampire'
  url_path        text not null,                      -- '/lingua-boost-lab/pre-a1/julia-vampire/'
  active          boolean default true,
  sort_order      int default 0,
  created_at      timestamptz not null default now()
);

create index if not exists lab_modules_level_idx on public.lab_modules(level);

-- ---------- 9. STUDENT-LAB ASSIGNMENTS ----------
create table if not exists public.student_lab_assignments (
  id              uuid primary key default gen_random_uuid(),
  student_id      uuid not null references public.students(id) on delete cascade,
  lab_module_id   uuid not null references public.lab_modules(id) on delete cascade,
  assigned_at     timestamptz not null default now(),
  completed       boolean default false,
  completed_at    timestamptz,
  unique (student_id, lab_module_id)
);

-- ---------- 10. TEACHER SINGLETON (payment, brand) ----------
create table if not exists public.teacher_info (
  id                    int primary key default 1 check (id = 1),
  full_name             text not null,
  tinkoff_quick_pay     text,
  telegram              text,
  phone                 text,
  contract_number       text,
  bank_account          text,
  bik                   text,
  bank                  text,
  correspondent_account text,
  inn                   text,
  kpp                   text,
  payment_purpose       text
);

-- =============================================================
-- RLS (Row Level Security)
-- =============================================================
alter table public.profiles                enable row level security;
alter table public.students                enable row level security;
alter table public.parents                 enable row level security;
alter table public.student_parent          enable row level security;
alter table public.subscriptions           enable row level security;
alter table public.lessons                 enable row level security;
alter table public.reports                 enable row level security;
alter table public.contracts               enable row level security;
alter table public.lab_modules             enable row level security;
alter table public.student_lab_assignments enable row level security;
alter table public.teacher_info            enable row level security;

-- Helper: проверка что текущий user — учитель
create or replace function public.is_teacher() returns boolean
language sql stable security definer as $$
  select exists(
    select 1 from public.profiles
    where id = auth.uid() and role in ('teacher','admin')
  );
$$;

-- --- PROFILES ---
drop policy if exists "profiles: own row read" on public.profiles;
create policy "profiles: own row read"   on public.profiles for select using (id = auth.uid());
drop policy if exists "profiles: teacher all" on public.profiles;
create policy "profiles: teacher all"    on public.profiles for all    using (public.is_teacher());

-- --- STUDENTS ---
-- Студент видит только свою запись
drop policy if exists "students: self read" on public.students;
create policy "students: self read"      on public.students for select using (profile_id = auth.uid());
-- Родитель видит своих детей
drop policy if exists "students: parent read" on public.students;
create policy "students: parent read"    on public.students for select using (
  exists (
    select 1 from public.student_parent sp
    join public.parents p on p.id = sp.parent_id
    where sp.student_id = students.id and p.profile_id = auth.uid()
  )
);
drop policy if exists "students: teacher all" on public.students;
create policy "students: teacher all"    on public.students for all    using (public.is_teacher());

-- --- PARENTS ---
drop policy if exists "parents: self read" on public.parents;
create policy "parents: self read"       on public.parents for select using (profile_id = auth.uid());
drop policy if exists "parents: teacher all" on public.parents;
create policy "parents: teacher all"     on public.parents for all    using (public.is_teacher());

-- --- STUDENT-PARENT link ---
drop policy if exists "spjoin: self read" on public.student_parent;
create policy "spjoin: self read"        on public.student_parent for select using (
  exists (select 1 from public.parents p where p.id = parent_id and p.profile_id = auth.uid())
  or exists (select 1 from public.students s where s.id = student_id and s.profile_id = auth.uid())
);
drop policy if exists "spjoin: teacher all" on public.student_parent;
create policy "spjoin: teacher all"      on public.student_parent for all    using (public.is_teacher());

-- --- SUBSCRIPTIONS ---
drop policy if exists "subs: student self" on public.subscriptions;
create policy "subs: student self"       on public.subscriptions for select using (
  exists (select 1 from public.students s where s.id = student_id and s.profile_id = auth.uid())
);
drop policy if exists "subs: parent read" on public.subscriptions;
create policy "subs: parent read"        on public.subscriptions for select using (
  exists (
    select 1 from public.student_parent sp
    join public.parents p on p.id = sp.parent_id
    where sp.student_id = subscriptions.student_id and p.profile_id = auth.uid()
  )
);
drop policy if exists "subs: teacher all" on public.subscriptions;
create policy "subs: teacher all"        on public.subscriptions for all    using (public.is_teacher());

-- --- LESSONS ---
drop policy if exists "lessons: student self" on public.lessons;
create policy "lessons: student self"    on public.lessons for select using (
  exists (select 1 from public.students s where s.id = student_id and s.profile_id = auth.uid())
);
drop policy if exists "lessons: parent read" on public.lessons;
create policy "lessons: parent read"     on public.lessons for select using (
  exists (
    select 1 from public.student_parent sp
    join public.parents p on p.id = sp.parent_id
    where sp.student_id = lessons.student_id and p.profile_id = auth.uid()
  )
);
drop policy if exists "lessons: teacher all" on public.lessons;
create policy "lessons: teacher all"     on public.lessons for all    using (public.is_teacher());

-- --- REPORTS (sent визны родителю/студенту, draft только учителю) ---
drop policy if exists "reports: student sent" on public.reports;
create policy "reports: student sent"    on public.reports for select using (
  status = 'sent' and exists (select 1 from public.students s where s.id = student_id and s.profile_id = auth.uid())
);
drop policy if exists "reports: parent sent" on public.reports;
create policy "reports: parent sent"     on public.reports for select using (
  status = 'sent' and exists (
    select 1 from public.student_parent sp
    join public.parents p on p.id = sp.parent_id
    where sp.student_id = reports.student_id and p.profile_id = auth.uid()
  )
);
drop policy if exists "reports: teacher all" on public.reports;
create policy "reports: teacher all"     on public.reports for all    using (public.is_teacher());

-- --- CONTRACTS (только учитель видит — родитель сам знает что подписал) ---
drop policy if exists "contracts: teacher all" on public.contracts;
create policy "contracts: teacher all"   on public.contracts for all    using (public.is_teacher());

-- --- LAB MODULES (публично для всех залогиненых) ---
drop policy if exists "lab: any authed read" on public.lab_modules;
create policy "lab: any authed read"     on public.lab_modules for select using (auth.uid() is not null);
drop policy if exists "lab: teacher all" on public.lab_modules;
create policy "lab: teacher all"         on public.lab_modules for all    using (public.is_teacher());

-- --- STUDENT-LAB ASSIGNMENTS ---
drop policy if exists "labasn: student self" on public.student_lab_assignments;
create policy "labasn: student self"     on public.student_lab_assignments for select using (
  exists (select 1 from public.students s where s.id = student_id and s.profile_id = auth.uid())
);
drop policy if exists "labasn: parent read" on public.student_lab_assignments;
create policy "labasn: parent read"      on public.student_lab_assignments for select using (
  exists (
    select 1 from public.student_parent sp
    join public.parents p on p.id = sp.parent_id
    where sp.student_id = student_lab_assignments.student_id and p.profile_id = auth.uid()
  )
);
drop policy if exists "labasn: teacher all" on public.student_lab_assignments;
create policy "labasn: teacher all"      on public.student_lab_assignments for all    using (public.is_teacher());

-- --- TEACHER INFO (публично читается всеми — это реквизиты для оплаты) ---
drop policy if exists "teacher_info: any read" on public.teacher_info;
create policy "teacher_info: any read"   on public.teacher_info for select using (true);
drop policy if exists "teacher_info: teacher upd" on public.teacher_info;
create policy "teacher_info: teacher upd" on public.teacher_info for all    using (public.is_teacher());

-- =============================================================
-- TRIGGERS — auto updated_at
-- =============================================================
create or replace function public.touch_updated_at() returns trigger
language plpgsql as $$
begin new.updated_at = now(); return new; end; $$;

do $$
declare t text;
begin
  for t in select unnest(array['profiles','students','parents','subscriptions','lessons','reports','contracts'])
  loop
    execute format('drop trigger if exists trg_touch_%I on public.%I', t, t);
    execute format('create trigger trg_touch_%I before update on public.%I for each row execute function public.touch_updated_at()', t, t);
  end loop;
end$$;

-- =============================================================
-- HANDLE NEW USER (создать profile при регистрации через Auth)
-- =============================================================
create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, role, email, full_name)
  values (new.id, 'student', new.email, coalesce(new.raw_user_meta_data->>'full_name', new.email));
  return new;
end; $$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- =============================================================
-- DONE. Migration script will populate data after this DDL runs.
-- =============================================================
