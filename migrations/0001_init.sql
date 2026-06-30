-- nge-homework D1 schema · v1 · 2026-06-30
-- Submissions table — главная: каждая сданная домашка
CREATE TABLE IF NOT EXISTS submissions (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  student_name TEXT NOT NULL,
  student_id   TEXT,
  lesson_path  TEXT NOT NULL,
  lesson_title TEXT,
  section_id   TEXT,
  items_json   TEXT NOT NULL,        -- JSON массив заданий с ответами
  score        INTEGER DEFAULT 0,
  total        INTEGER DEFAULT 0,
  pct          INTEGER DEFAULT 0,
  misses_json  TEXT,                  -- JSON массив пропусков для быстрого превью
  created_at   INTEGER NOT NULL,      -- unix timestamp
  user_agent   TEXT,
  ip_country   TEXT
);

CREATE INDEX IF NOT EXISTS idx_subs_student ON submissions(student_name, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_subs_lesson  ON submissions(lesson_path, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_subs_time    ON submissions(created_at DESC);

-- Students table — справочник для PIN-входа
CREATE TABLE IF NOT EXISTS students (
  id   TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  pin  TEXT NOT NULL,
  parent_email TEXT,
  active INTEGER DEFAULT 1,
  created_at INTEGER NOT NULL
);
