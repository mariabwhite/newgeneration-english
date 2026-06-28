-- Premium gate for Cloudflare Pages Functions + Supabase
-- Apply with Supabase SQL editor or `supabase db push`.

create table if not exists public.premium_gate_state (
  id int primary key default 1 check (id = 1),
  active boolean not null default true,
  pin_salt text not null,
  pin_hash text not null,
  gate_version int not null default 1,
  session_ttl_seconds int not null default 2592000,
  updated_at timestamptz not null default now()
);

create table if not exists public.premium_sessions (
  token text primary key,
  gate_version int not null,
  expires_at timestamptz not null,
  created_at timestamptz not null default now(),
  revoked_at timestamptz
);

create index if not exists premium_sessions_expires_at_idx
  on public.premium_sessions (expires_at);

alter table public.premium_gate_state enable row level security;
alter table public.premium_sessions enable row level security;

revoke all on public.premium_gate_state from anon, authenticated, public;
revoke all on public.premium_sessions from anon, authenticated, public;

insert into public.premium_gate_state (id, active, pin_salt, pin_hash, gate_version, session_ttl_seconds)
values (
  1,
  true,
  'c8f1d9a3b6e24f0a9c7e1d5b4f3a8c6d',
  '8941ec45e109aeb0a41d060c7dd002b6f2421db6344d07fecdd29946aebdfc49',
  1,
  2592000
)
on conflict (id) do update
set active = excluded.active,
    pin_salt = excluded.pin_salt,
    pin_hash = excluded.pin_hash,
    gate_version = excluded.gate_version,
    session_ttl_seconds = excluded.session_ttl_seconds,
    updated_at = now();

comment on table public.premium_gate_state is
  'Single-row source of truth for the active premium PIN. Bump gate_version when the PIN changes.';

comment on table public.premium_sessions is
  'Server-side premium sessions created after PIN verification.';
