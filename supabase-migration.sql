-- =============================================================
-- NGE Cabinet — migration from data.js → Supabase
-- Generated: 2026-06-01T10:00:35.368Z
-- =============================================================
-- Запускается в SQL Editor. Идемпотентность через DELETE + INSERT.
-- Безопасно перезапускать — все строки удаляются и вставляются заново.

-- ---------- Cleanup (для перезапуска) ----------
delete from public.student_lab_assignments;
delete from public.reports;
delete from public.lessons;
delete from public.subscriptions;
delete from public.contracts;
delete from public.student_parent;
delete from public.parents;
delete from public.students;
delete from public.lab_modules;
delete from public.teacher_info;

-- ---------- 1. TEACHER INFO ----------
insert into public.teacher_info (id, full_name, tinkoff_quick_pay, telegram, phone, contract_number, bank_account, bik, bank, correspondent_account, inn, kpp, payment_purpose) values (1, 'Мария Витальевна Бурцева', 'https://www.tinkoff.ru/rm/r_PnDqHEqsDu.EkrmOLeXmQ/MIhLS10143', 'https://t.me/MariaBurceva_English', '89165101792', '5181572792', '40817810200014652973', '044525974', 'АО "ТБанк"', '30101810145250000974', '7710140679', '771301001', 'Перевод средств по договору № 5181572792 Бурцева Мария Витальевна НДС не облагается');

-- ---------- 2. LAB MODULES ----------
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('Pre-A1', 'Body & Grammar Garden', 'body-and-grammar-pink', '../lingua-boost-lab/pre-a1/body-and-grammar-pink.html', 0);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('Pre-A1', 'Hello! Classroom Fun', 'hello-classroom-fun', '../lingua-boost-lab/pre-a1/hello-classroom-fun.html', 1);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Present Simple Routines', 'a1-01-present-simple-routines', '../lingua-boost-lab/a1/a1-01-present-simple-routines.html', 2);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Present Simple Questions & Negatives', 'a1-02-present-simple-questions-negatives', '../lingua-boost-lab/a1/a1-02-present-simple-questions-negatives.html', 3);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Present Simple + Adverbs of Frequency / There is/are', 'a1-03-present-simple-adverbs-frequency', '../lingua-boost-lab/a1/a1-03-present-simple-adverbs-frequency.html', 4);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Have / Has — My Things', 'a1-04-have-has-my-things', '../lingua-boost-lab/a1/a1-04-have-has-my-things.html', 5);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'My / Your / His / Her', 'a1-05-my-your-his-her', '../lingua-boost-lab/a1/a1-05-my-your-his-her.html', 6);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Prepositions of Place', 'a1-06-prepositions-of-place', '../lingua-boost-lab/a1/a1-06-prepositions-of-place.html', 7);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Instructions & Requests', 'a1-07-instructions-requests', '../lingua-boost-lab/a1/a1-07-instructions-requests.html', 8);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Final Mission (A1)', 'a1-08-final-mission', '../lingua-boost-lab/a1/a1-08-final-mission.html', 9);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Easter English Lesson', 'easter-english-lesson', '../lingua-boost-lab/a1/easter-english-lesson.html', 10);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Past Simple Adventure', 'past-simple-adventure', '../lingua-boost-lab/a1/past-simple-adventure.html', 11);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'Prepositions World', 'prepositions-world', '../lingua-boost-lab/a1/prepositions-world.html', 12);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A1', 'School Words & Pronouns', 'school-words-and-pronouns', '../lingua-boost-lab/a1/school-words-and-pronouns.html', 13);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A2', 'Ancient China Explorer', 'ancient-china-explorer', '../lingua-boost-lab/a2/ancient-china-explorer.html', 14);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A2', 'Core Trainer A2 → B1', 'core-trainer-a2-b1', '../lingua-boost-lab/a2/core-trainer-a2-b1.html', 15);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('A2', 'English Booster A2 → B1', 'english-booster-a2-b1', '../lingua-boost-lab/a2/english-booster-a2-b1.html', 16);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('B1', 'Ancient China Cultural Studies', 'ancient-china-cultural-studies', '../lingua-boost-lab/b1/ancient-china-cultural-studies.html', 17);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('B1', 'Grammar Arcade: Present Continuous vs Present Perfect', 'grammar-arcade-pc-pp', '../lingua-boost-lab/b1/grammar-arcade-pc-pp.html', 18);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('B1', 'Restaurant Menu Lab', 'restaurant-menu-lab', '../lingua-boost-lab/b1/restaurant-menu-lab.html', 19);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('B1', 'Space Explorers', 'space-explorers-english', '../lingua-boost-lab/b1/space-explorers-english.html', 20);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('B1', 'Whispering Library Quest', 'whispering-library-quest', '../lingua-boost-lab/b1/whispering-library-quest.html', 21);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('B1', 'Word Forge: Suffixes & Prefixes', 'word-building-prefixes-and-suffixes', '../lingua-boost-lab/b1/word-building-prefixes-and-suffixes.html', 22);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('B2+', 'Geo Quest: Articles on the Map', 'articles-with-geographical-names', '../lingua-boost-lab/b2-plus/articles-with-geographical-names.html', 23);
insert into public.lab_modules (level, title, slug, url_path, sort_order) values ('C1', 'Stars & Stellar Phenomena', 'stars-and-stellar-phenomena', '../lingua-boost-lab/c1/stars-and-stellar-phenomena.html', 24);

-- ---------- 3. STUDENTS ----------
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('andrei-kruglov', '34d7364c-ba79-81e0-9e00-eb54d63b0dc1', 'Андрей Круглов', null, 'Привет, Андрей', 'Здравствуйте, Юлия Борисовна', true, 'B2', 'индивидуально', '1.5 часа', 2, 'вторник 14:30 / четверг 10:30 (+20 мин)', 'Актуализировано 20.05.2026: остаётся 3 урока до летних каникул — 27.05 (вт 14:30), 29.05 (чт 10:30+20мин), 02.06 (вт 14:30 — перенос чт-формата, время как обычное вт). После 02.06 уходит на каникулы до сентября 2026, с высылкой ему форм.', 'разговорный английский, школа, подготовка к TOEFL/IELTS', 2500, 20000, true);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('sova-elena', '34d7364c-ba79-81ba-b4d6-e8b07e6ed7f7', 'Сова Елена Витальевна', null, null, null, false, 'A2', 'индивидуально', '90 мин', 1, 'вторник 19:00', 'Май-абонемент 7 уроков (вт 19:00): 4 проведены + 3 оплачены вперёд. Все даты — регулярные вторники, без сдвигов. 28.04→19.05 = первые 4 (grammar×2 + Wind in the Willows + SIM/coffee сегодня). 26.05/2.06/9.06 — оставшиеся 3.', 'взрослый ученик, медленный темп, через карточки и опоры', 2000, null, true);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('sova-ekaterina', '34d7364c-ba79-810e-ac5b-f35b5a113898', 'Сова Екатерина', 'Катя', null, null, false, 'B1', 'индивидуально', '90 мин', 1, 'понедельник 18:00 (на каникулах)', 'На 19.05.2026 отпущена на каникулы. Запланированные уроки на этой неделе не проводятся. Возобновление — уточнить с родителем.', null, null, null, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('fedor-protasov', '34d7364c-ba79-8135-bda3-f409c1cf93a2', 'Фёдор Протасов', null, null, null, false, 'A2/B1', 'индивидуально', '90 мин', 1, 'вторник 16:00 / четверг 20:00 / пятница 20:00 / воскресенье 14:40', 'Расписание актуализировано 19.05.2026: вт 16:00 / чт 20:00 (раньше 20:15) / пт 20:00 + добавилось воскресенье 14:40 (после Дениса и пары). Май-абонемент: 6 проведено (1, 2, 3, 4, 5, 8), 14/15.05 перенесены на 17.05 — Pinocchio комбинированный.', 'Spotlight 9 + страны + Past Simple irregular + there is/are/was/were', null, null, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('ivanov-ivan', '3537364c-ba79-813d-a84b-ee42fad1bd19', 'Иванов Иван', 'Иван', null, null, false, 'B1+/B2', 'индивидуально', '90 мин', 1, 'пятница 17:30', null, null, 2000, 10000, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('daniella-libova', '34d7364c-ba79-81af-9ba9-f423aede5524', 'Даниэлла Либова', null, null, null, false, 'B2+', 'индивидуально', '90 мин', 1, 'понедельник 18:00 / четверг 18:00', 'Май-абонемент 8 уроков. Отыграно 4 (4, 7, 11, 18 completed). На неделе 19-25.05 уроков нет (плавающий график). Дальше 21, 25, 28 — времена под подтверждение. Расписание плавающее → нужна редактируемость через кабинет (open issue).', 'подготовка к ЕГЭ (word formation, exam speaking)', null, null, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('denis-shalmanov', '34d7364c-ba79-81a5-bdd8-ce47d7b050d7', 'Денис Шалманов', null, 'Здравствуйте, Денис', 'Здравствуйте, Денис', false, 'A1', 'индивидуально', '90 мин', 1, 'воскресенье 10:30', 'Май закрыт полностью (5 уроков проведены). Июнь оплачен 31.05.2026: 4 воскресенья × 2 500 ₽ = 10 000 ₽. Стабильный темп без скачков и откатов.', null, 2500, 10000, true);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('anya-isaeva', '34d7364c-ba79-8199-879a-d0400012561e', 'Аня Исаева', null, null, null, false, null, 'индивидуально', '90 мин', 1, 'понедельник 17:00', null, null, 2500, null, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('yulya-lushina', '34d7364c-ba79-81b5-8215-fdfe91bec709', 'Юля Лушина', null, 'Привет, Юлия', null, false, null, 'индивидуально', '90 мин', 1, 'понедельник 12:00', 'Понедельник 12:00. На неделе 1-7 июня — разовый перенос на среду 3 июня.', null, 2000, null, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('yulya-izotova', '34d7364c-ba79-81fa-8d1b-ed43ce161b3b', 'Юля Изотова', null, 'Привет, Юлия', null, false, 'A1+', 'индивидуально', '90 мин', 1, 'понедельник 16:00 / пятница 15:30', 'Май-абонемент 8 уроков (оплачено 8). На 18.05 отыграно 5 (1, 4, 8, 15, 18). 11 мая — пропуск, не в счёт. Дальше 22, 25, 29.', 'Старлайт 3 / Past Simple, неправильные глаголы, лексика по темам', 2000, 18000, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('sofia-pavlova', '34d7364c-ba79-817f-85f8-c6f87fd4d85c', 'Соня Павлова', null, 'Привет, София', null, false, 'B2/B2+', 'индивидуально', '90 мин', 1, 'четверг 17:00', null, 'ЕГЭ: лексика B2+, word formation, writing, speaking', 2000, 8000, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('ekaterina-mariya-pair', '34d7364c-ba79-81f0-ba7f-d87dcd7dfd19', 'Екатерина и Мария', null, null, null, false, null, 'парное занятие', '90 мин', 1, 'четверг 18:00 / воскресенье 13:35', 'Пара не подтвердила завтра четверг 21.05 — статус под вопросом (на 20.05.2026)', null, 1500, 12000, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('ekaterina-medvedeva-solo', null, 'Катя Медведева', null, 'Привет, Екатерина', 'Здравствуйте, Марина', false, 'B1', 'индивидуально (раздельно с Машей с 28.05)', '90 мин', 1, 'четверг 18:00 / воскресенье 13:35', 'С 28.05.2026 переходят на раздельный формат: Катя — 18:00, Маша — 19:00. Завтрашний урок 21.05 не подтверждён → переносится на 28.05.', null, 1500, 6000, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('maria-kuznetsova-solo', null, 'Маша Кузнецова', null, 'Привет, Мария', 'Здравствуйте, Елена', false, 'B1', 'индивидуально (раздельно с Катей с 28.05)', '90 мин', 1, 'четверг 19:00 / воскресенье 13:35', 'С 28.05.2026 переходят на раздельный формат: Маша — 19:00, Катя — 18:00. Завтрашний урок 21.05 не подтверждён → переносится на 28.05.', null, 1500, 6000, false);
insert into public.students (slug, notion_id, name, nickname, greeting_student, greeting_parent, casual_greeting, level, format, duration, lessons_per_week, schedule, stability_note, goal, price_per_lesson, monthly_package, is_adult) values ('katya-marakina', '34d7364c-ba79-8173-a103-f60f2bb5f124', 'Катя Маракина', null, null, null, false, 'B1', 'индивидуально', '90 мин', 1, 'вторник 17:00 + воскресенье 12:00 (по 90 мин)', 'Май-июнь абонемент 8 уроков (4 вт + 4 вс) до 14.06.2026. Старт 19.05.2026. С 14.06 — летний пересбор. Проведено 3 из 8. История: 26.04, 3.05, 10.05 cancelled (согласованные), 17.05 missed (без предупреждения).', null, 2500, 20000, false);

-- pair: Катя Медведева ↔ Маша Кузнецова
-- (если в data.js появится отдельная запись пары — раскомментировать)
-- update public.students set pair_partner_id = (select id from public.students where slug='maria-kuznetsova') where slug='ekaterina-medvedeva';
-- update public.students set pair_partner_id = (select id from public.students where slug='ekaterina-medvedeva') where slug='maria-kuznetsova';

-- ---------- 4. PARENTS + student_parent links ----------
insert into public.parents (full_name, passport, email, phone, address) values ('Сова Елена Витальевна', '4524 №179806', 'elenavit-2005@mail.ru', '+79671403548', '105203, Москва, ул. Первомайская, д.113, кв.29');
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'sova-ekaterina'), (select id from public.parents where full_name = 'Сова Елена Витальевна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Протасова Мария Петровна', null, null, null, null);
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'fedor-protasov'), (select id from public.parents where full_name = 'Протасова Мария Петровна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Подлесных Татьяна Анатольевна', '4524 514335 (06.11.2024)', 'ryabina8@list.ru', '+79057502111', 'Москва, пос. Сосенское, п. Коммунарка, ул. Ясная, д.5, кв.33');
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'ivanov-ivan'), (select id from public.parents where full_name = 'Подлесных Татьяна Анатольевна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Либова Юлия Игоревна', null, null, null, null);
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'daniella-libova'), (select id from public.parents where full_name = 'Либова Юлия Игоревна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Исаева Наталья Вячеславовна', '4514 567410 (УФМС России по г.Москве)', 'platemir@yandex.ru', null, 'Москва, Береговой пр-д, д.7, кв.95');
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'anya-isaeva'), (select id from public.parents where full_name = 'Исаева Наталья Вячеславовна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Лушин Александр Анатольевич', null, null, null, null);
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'yulya-lushina'), (select id from public.parents where full_name = 'Лушин Александр Анатольевич' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Изотова Ольга Игоревна', '4510 764054', 'meet.me.here@mail.ru', '+79269754602', null);
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'yulya-izotova'), (select id from public.parents where full_name = 'Изотова Ольга Игоревна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Анатольева Галина Анатольевна', '45 24 № 708384 (ГУ МВД по г.Москве)', null, null, 'Москва, Зельев переулок, д.3, кв.4');
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'sofia-pavlova'), (select id from public.parents where full_name = 'Анатольева Галина Анатольевна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Медведева Марина Сергеевна (Катя) / Лихолева Елена Сергеевна (Маша)', null, null, null, null);
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), (select id from public.parents where full_name = 'Медведева Марина Сергеевна (Катя) / Лихолева Елена Сергеевна (Маша)' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Медведева Марина Сергеевна', '4523 521762 (04.05.2023)', 'marine_medvedeva@rambler.ru', '+79165478727', 'Москва, ул. Островитянова, д.9 кв.947');
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), (select id from public.parents where full_name = 'Медведева Марина Сергеевна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Лихолева Елена Сергеевна', '4519 568773 (ГУ МВД России по г.Москве)', 'ivan-tenaivanova@ya.ru (уточнить)', null, 'Москва, ул. Акад. Волгина, д.8А');
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), (select id from public.parents where full_name = 'Лихолева Елена Сергеевна' limit 1));
insert into public.parents (full_name, passport, email, phone, address) values ('Кедрова Татьяна Владимировна', '45 08 445532', null, null, 'Москва, Сиреневый б-р, д.44, корп.1, кв.163');
insert into public.student_parent (student_id, parent_id) values ((select id from public.students where slug = 'katya-marakina'), (select id from public.parents where full_name = 'Кедрова Татьяна Владимировна' limit 1));

-- ---------- 5. SUBSCRIPTIONS ----------
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05', 8, 5, 20000, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'sova-elena'), '2026-05', 7, 4, null, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'sova-ekaterina'), '2026-05', 4, 4, null, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05', 13, 7, null, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'ivanov-ivan'), '2026-05', 5, 4, 10000, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'daniella-libova'), '2026-05', 8, 4, null, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-06', 4, 0, 10000, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'anya-isaeva'), '2026-05', 4, 3, null, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'yulya-lushina'), '2026-06', 4, 0, null, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05', 8, 5, 18000, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'sofia-pavlova'), '2026-05', 4, 0, 8000, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05', 9, 5, 12000, false);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05', 9, 5, 6000, true);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05', 9, 5, 6000, false);
insert into public.subscriptions (student_id, month, lessons_in_package, lessons_used, package_amount, paid) values ((select id from public.students where slug = 'katya-marakina'), '2026-05', 8, 3, 20000, true);

-- ---------- 6. LESSONS ----------
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05-05', 1, 'completed', 'Введение: polymers, sciences, water (тематический блок B2-C1)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05-07', 2, 'completed', 'Продолжение блока: polymers, sciences, water', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05-12', 3, 'completed', 'Nuclear physics + polymers', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05-14', 4, 'completed', 'Allergy — тема, лексика, дискуссия', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05-19', 5, 'completed', 'TOEFL по темам — наука, нейробиология, полимеры (повторение блока)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05-21', 6, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05-26', 7, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05-28', 8, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-elena'), '2026-04-28', 1, 'completed', 'Грамматика #1: simple + perfect tenses', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-elena'), '2026-05-05', 2, 'completed', 'Грамматика #2: passive voice + past perfect', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-elena'), '2026-05-12', 3, 'completed', 'The Wind in the Willows — чтение книги для детей, лексика, обсуждение', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-elena'), '2026-05-19', 4, 'completed', 'SIM-карты и кофе — практическая лексика и диалоги', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-elena'), '2026-05-26', 5, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-elena'), '2026-06-02', 6, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-elena'), '2026-06-09', 7, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-ekaterina'), '2026-05-04', 1, 'completed', 'ОГЭ / ЕГЭ — повторение лексики и формат экзамена', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-ekaterina'), '2026-05-11', 2, 'completed', 'Книги — жанры, рассказы, лексика', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-ekaterina'), '2026-05-18', 3, 'completed', 'Неправильные глаголы с предлогом — отработка форм и употребление', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sova-ekaterina'), '2026-05-25', 4, 'completed', 'Финальное повторение завершено — все слова, темы, книжки. На каникулы до сентября.', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-01', 1, 'completed', 'Туристический английский — Китай (лексика, клише)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-05', 2, 'completed', 'Туристический английский — Италия', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-07', 3, 'completed', 'Грамматический юнит', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-08', 4, 'completed', 'Повторение неправильных глаголов', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-12', 5, 'completed', 'Туристические клише', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-14', 6, 'rescheduled', 'Перенесён на 17.05 (технические трудности)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-15', 7, 'rescheduled', 'Перенесён на 17.05 (технические трудности)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-17', 8, 'completed', 'Pinocchio (комбинированный за 14 и 15.05) — чтение, простейшие слова, работа с книгой', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-19', 9, 'completed', 'Древний Китай — лексика, история, обсуждение', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-21', 10, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-22', 11, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-26', 12, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-28', 13, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'fedor-protasov'), '2026-05-29', 14, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ivanov-ivan'), '2026-05-01', 1, 'completed', 'Чтение — художественные тексты про путешествия во времени', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ivanov-ivan'), '2026-05-08', 2, 'completed', 'Аудирование академического уровня + новая лексика', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ivanov-ivan'), '2026-05-15', 3, 'completed', 'Грамматика — целенаправленная подготовка к МЦК', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ivanov-ivan'), '2026-05-22', 4, 'missed', 'Пропуск (Иван проспал)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ivanov-ivan'), '2026-05-29', 5, 'completed', 'Устная практика — летние планы и каникулы', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'daniella-libova'), '2026-05-04', 1, 'completed', 'Speaking — устная практика, разговорная часть', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'daniella-libova'), '2026-05-07', 2, 'completed', 'Speaking — устная практика (продолжение)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'daniella-libova'), '2026-05-11', 3, 'completed', 'ЕГЭ-практика — устные части, разбор заданий', 'Пройти Word Building (префиксы и суффиксы) — упражнения 1 и 2. К следующему уроку.', '../lingua-boost-lab/b1/word-building-prefixes-and-suffixes.html', 'Word Building');
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'daniella-libova'), '2026-05-14', 4, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'daniella-libova'), '2026-05-18', 5, 'completed', 'Battle of Levels — чтение из учебника Музлановой (трудный текст)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'daniella-libova'), '2026-05-21', 6, 'cancelled', 'Отменено — Даниэлла не сможет (Маша подтвердила 20.05)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'daniella-libova'), '2026-05-25', 7, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'daniella-libova'), '2026-05-28', 8, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-05-03', 1, 'completed', 'Одежда — лексика и описания', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-05-10', 2, 'completed', 'Present Simple / Present Continuous + базовые конструкции', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-05-17', 3, 'completed', 'Дома — лексика, описания, что есть дома', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-05-24', 4, 'completed', 'Повторение темы «дома» (закрепление)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-05-31', 5, 'completed', 'Город — лексика, городские объекты', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-06-07', 6, 'planned', 'Город — расширяем городскую лексику, описания', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-06-14', 7, 'planned', 'Шоппинг в городе — фразы для магазина (Can I have / How much is / I would like)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-06-21', 8, 'planned', 'Направления в городе — Go straight / Turn left, right / It is near', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-06-28', 9, 'planned', 'Кофе в городе — заказ кофе (I would like a cappuccino / To go please)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'anya-isaeva'), '2026-05-04', 1, 'completed', 'Города — конкретная лексика, заканчивали тему', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'anya-isaeva'), '2026-05-11', 2, 'completed', 'Present Perfect — теория и Speaking по нему', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'anya-isaeva'), '2026-05-18', 3, 'completed', 'Города — функции города (городские объекты) + Present Continuous в контексте', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'anya-isaeva'), '2026-05-25', 4, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-lushina'), '2026-05-18', 1, 'completed', 'Cute vampire English v1 (Pre-A1) — face/body parts, HSKT video, friendly vampire family.', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-lushina'), '2026-05-25', 2, 'completed', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-lushina'), '2026-06-01', 3, 'rescheduled', 'Перенос с понедельника на среду 3 июня (по договорённости).', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-lushina'), '2026-06-03', 4, 'planned', 'Vampire English v8 — Music & Friends (Pre-A1, 90 min).', 'Откройте на айпаде, нажимайте на картинки и значки 🔊 — всё озвучено.', '../lingua-boost-lab/pre-a1/julia-vampire/index.html?v=1', '🦇 Открыть урок');
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-lushina'), '2026-06-08', 5, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-01', 1, 'completed', 'еда — лексика', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-04', 2, 'completed', 'магазины + история про Юлию (чтение, лексика)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-08', 3, 'completed', 'контейнеры/бутылки/банки + Present Simple', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-11', null, 'missed', 'Пропуск (не в счёт абонемента)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-15', 4, 'completed', 'неправильные глаголы, времена, истории', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-18', 5, 'completed', 'Swimming pool — лексика и активности (бассейн)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-22', 6, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-25', 7, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05-29', 8, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sofia-pavlova'), '2026-05-07', 1, 'planned', 'ЕГЭ: повторение лексики апреля + word formation / vocabulary MCQ', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sofia-pavlova'), '2026-05-14', 2, 'planned', 'Reading B2 / B2+: тематический текст + вопросы ЕГЭ', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sofia-pavlova'), '2026-05-21', 3, 'planned', 'Writing / email: структура, ответы, собственные вопросы', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'sofia-pavlova'), '2026-05-28', 4, 'planned', 'Speaking + grammar consolidation: времена, passive, modals', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-03', 1, 'completed', 'Введение / повторение всех грамматических тем', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-07', 2, 'completed', 'Повторение и конспекты', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-10', 3, 'completed', 'Праздники и дни рождения — лексика, диалоги', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-14', 4, 'completed', 'Petting — вариант 4 или 5 (формулировку точно уточнить)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-17', 5, 'completed', 'Экология — введение темы', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-21', 6, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-24', 7, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-28', 8, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05-31', 9, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-03', 1, 'completed', 'Введение / повторение всех грамматических тем', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-07', 2, 'completed', 'Повторение и конспекты', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-10', 3, 'completed', 'Праздники и дни рождения — лексика, диалоги', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-14', 4, 'completed', 'Petting — вариант 4 или 5 (формулировку точно уточнить)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-17', 5, 'completed', 'Экология — введение темы', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-21', 6, 'rescheduled', 'Перенос на 28.05 — не подтвердили завтра', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-24', 7, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-28', 8, 'planned', 'Первый раздельный урок (Катя — 18:00)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'ekaterina-medvedeva-solo'), '2026-05-31', 9, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-03', 1, 'completed', 'Введение / повторение всех грамматических тем', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-07', 2, 'completed', 'Повторение и конспекты', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-10', 3, 'completed', 'Праздники и дни рождения — лексика, диалоги', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-14', 4, 'completed', 'Petting — вариант 4 или 5 (формулировку точно уточнить)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-17', 5, 'completed', 'Экология — введение темы', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-21', 6, 'rescheduled', 'Перенос на 28.05 — не подтвердили завтра', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-24', 7, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-28', 8, 'planned', 'Первый раздельный урок (Маша — 19:00)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'maria-kuznetsova-solo'), '2026-05-31', 9, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-04-26', null, 'cancelled', 'Согласованный перенос (история до абонемента)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-05-03', null, 'cancelled', 'Согласованный перенос (история до абонемента)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-05-10', null, 'cancelled', 'Согласованный перенос (история до абонемента)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-05-17', null, 'missed', 'Пропуск без предупреждения (история до абонемента)', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-05-19', 1, 'completed', 'Времена, техники решения ОГЭ', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-05-24', 2, 'completed', 'Кулинария и времена, страны мира', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-05-25', 3, 'completed', 'Италия: известные люди, чудеса света + немного про Ирландию', null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-05-31', 4, 'planned', 'Jerusalem — A City of Three Faiths (speaking-focus, Would, Modals)', 'Интерактивный B1-урок: 17 секций, аудио, говорение, Would-конструкции, модальные глаголы. Можно открыть до занятия — пробежаться по vocabulary, дать ушам привыкнуть к narrator-аудио.', '../lingua-boost-lab/b1/jerusalem-three-faiths/?v=4cbcbaf', 'Открыть урок Jerusalem');
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-06-02', 5, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-06-07', 6, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-06-09', 7, 'planned', null, null, null, null);
insert into public.lessons (student_id, lesson_date, num, status, topic, homework_text, homework_module_url, homework_module_title) values ((select id from public.students where slug = 'katya-marakina'), '2026-06-14', 8, 'planned', 'Последний урок до летнего пересбора', null, null, null);

-- ---------- 7. REPORTS ----------
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'anya-isaeva'), '2026-05', 'parent_report', 'draft', 'Отчёт родителю · май 2026', 'родитель', 'Аня молодец: закончили блок по теме города, ввели Present Perfect и закрепили три формы настоящего времени — Present Simple, Present Continuous и Present Perfect. Прописали диктант; дальше — города, другие страны, спорт и travelling.', '# Краткий вывод

Аня прошла первый блок занятий по понедельникам. Основной фокус был на устной базе, простых личных вопросах, there is / there are, предлогах места и городской лексике. Устная речь начала становиться увереннее: пауз меньше, фразы собираются ровнее, но грамматические конструкции нужно доводить до автоматизма.

# Сегодня, 11 мая

Аня молодец: закончили блок по теме города, ввели Present Perfect и собрали три формы настоящего времени — Present Simple, Present Continuous и Present Perfect. Прописали диктант. Дальше переходим к полезным новым темам: города, другие страны, спорт и travelling.

# Следующий фокус

Закрепление Present Simple / Present Continuous / Present Perfect через устную практику, диктанты и новые темы: города, другие страны, спорт и travelling.', 'https://www.notion.so/35a7364cba7981b787b5cf8960ca9354');
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'denis-shalmanov'), '2026-05', 'parent_report', 'ready', '2026-05 — Денис Шалманов — student report', 'Денис Шалманов', 'Денис, спасибо за стабильный темп в мае! Все 5 воскресений проведены: одежда → Present Simple/Continuous → дома → повтор домов → город. Май закрыт полностью, ничего не должны. К оплате за июнь — 10 000 ₽ (4 урока × 2 500).', 'Добрый день!

Отправляю краткий отчёт по нашим занятиям за май.

# Календарь занятий — май (5 занятий)

- **3 мая** — Одежда: лексика, описания (завершали тему)
- **10 мая** — Past Simple / Past Continuous, stative verbs
- **17 мая** — Дома: лексика, описания
- **24 мая** — *запланирован*
- **31 мая** — *запланирован*

3 из 5 проведены, 2 впереди.

# По прогрессу

**Мы** идём в стабильном темпе. Темы по бытовой лексике хорошо ложатся, грамматику времён (Past Simple, Past Continuous, stative verbs) разбираем основательно. Видно, что вы спокойно осваиваете новый материал и активно работаете на уроке.

# Зоны роста

- Вывод изученной лексики в свободную речь (пока больше в распознавании)
- Автоматизм времён — особенно различение Past Simple vs Past Continuous в потоке
- Расширение бытовой тематики (работа, транспорт, дорога)

# Следующая задача

**Вам** стоит чаще проговаривать новые слова и темы вслух между уроками — даже 10–15 минут речи о прошедшем дне в Past Simple дают сильный эффект. На уроках **мы** продолжаем тематические блоки + закрепление времён в свободной речи.

# Майский абонемент

5 воскресений мая (3, 10, 17, 24, 31). Стоимость занятия 2 500 ₽.

- Оплачено 7 500 ₽ (3 урока: 3, 10, 17) + 2 переноса с апреля
- К оплате за 24 и 31 мая: **5 000 ₽**
', 'https://www.notion.so/3637364cba7981a98085ef806ef7deb2');
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'yulya-izotova'), '2026-05', 'parent_report', 'ready', '2026-05 — Юля Изотова — parent report', 'Изотова Ольга Игоревна', 'Юля стабильно идёт вперёд: 4 из 9 уроков проведены (еда, магазины, контейнеры, неправильные глаголы). Формат историй работает особенно хорошо. Один пропуск 11 мая, 4 урока впереди (18, 22, 25, 29).', 'Добрый день!

Отправляю краткий отчёт по занятиям **Юли** за май.

# Календарь занятий — май (9 занятий)

- **1 мая** — Еда: лексика
- **4 мая** — Магазины + история про Юлию (чтение, лексика)
- **8 мая** — Контейнеры / бутылки / банки + Present Simple
- **11 мая** — *пропуск*
- **15 мая** — Неправильные глаголы, времена, истории
- **18 мая** — *запланирован*
- **22 мая** — *запланирован*
- **25 мая** — *запланирован*
- **29 мая** — *запланирован*

4 из 9 проведены, 1 пропуск, 4 впереди.

# По прогрессу

Юля стабильно идёт вперёд. Формат историй и сюжетных занятий работает особенно хорошо: через них лучше запоминается и грамматика, и тематическая лексика. На занятиях много чтения и новых слов, Юля включена.

# Зоны роста

- Вывод трёх времён (Present Simple, Present Continuous, Past Simple) в собственную речь — пока больше в распознавании
- Закрепление неправильных глаголов (повторяем регулярно, нужна автоматизация)
- Расширение тематической лексики через короткие связные истории

# Следующая задача

Продолжаем закреплять грамматику через истории, делаем больше устной практики. До конца мая — 4 занятия. Юле стоит каждый раз короткими историями использовать новые слова и неправильные глаголы.

# Майский абонемент — 9 занятий

Понедельники и пятницы. Стоимость занятия 2 000 ₽. Итого: **18 000 ₽** (оплачено).

Один пропуск 11 мая остаётся непроведённым — при возможности можем отработать или переоформить как перенос.
', 'https://www.notion.so/3637364cba798136a342cf0593982b17');
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'sova-ekaterina'), '2026-05', 'parent_report', 'draft', 'Отчёт родителю · май 2026', 'родитель', 'Катя стабильно работает на уровне B1. В мае фокус — books / book genres, phrasal verbs и ОГЭ-формат; важно фиксировать ошибки и выводить лексику в речь.', '# Краткий вывод

Катя работает на уровне B1. Основные блоки: ОГЭ-формат, books / book genres и phrasal verbs.

# Ближайший фокус

Book genres → vocabulary table → questions → B1 multiple choice → matching → interview → short result check.', 'https://www.notion.so/35a7364cba7981a2801af0ed869d847f');
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05', 'parent_report', 'draft', 'Отчёт родителю Екатерины · май 2026', 'родитель (Екатерина Медведева)', 'Катя работала ровно и стабильно: word formation, suffixes/prefixes, gerund/infinitive, used to и ОГЭ. Speaking стал собраннее, лучше держится фрейм.', '# Краткий вывод

Катя работала ровно и стабильно. Понимание тем стало лучше, speaking подрос.

# Май

9 занятий × 1 500 руб. = 13 500 руб.', 'https://www.notion.so/35a7364cba7981bea07ddf8a902b1f13');
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'ekaterina-mariya-pair'), '2026-05', 'parent_report', 'draft', 'Отчёт родителю Марии · май 2026', 'родитель (Мария Кузнецова)', 'Маша работает в паре с Катей. Нужна дополнительная опора на построение предложения и точечная практика: gerund/infinitive, word formation, spelling и более полные ответы.', '# Краткий вывод

Маша работает в паре с Катей и проходит те же темы. По последним работам точность временно просела: нужны опора на построение предложения и точечная практика.

# Примечание

Отдельной личной карточки Марии Кузнецовой не найдено, строка связана с общей карточкой пары Екатерина и Мария.', 'https://www.notion.so/35a7364cba7981489de5fa224b04e372');
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'andrei-kruglov'), '2026-05', 'diagnostic', 'draft', 'TOEFL диагностика · 2026', 'родитель', 'Андрей показывает уверенный B2. TOEFL-style diagnostic estimate — 4.0/6.0. Сильные стороны Reading и Listening; фокус роста — Writing/Speaking accuracy.', '# Краткий вывод

Андрей показывает уверенный общий уровень B2. Диагностическая оценка по TOEFL iBT 2026 classroom scale — 4.0 из 6.0.

# План

Reading, real-audio listening, email + academic discussion writing, structured speaking, collocations/articles/plurals.', 'https://www.notion.so/35a7364cba79812492a3dcc970b5ceef');
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'daniella-libova'), '2026-05', 'parent_report', 'draft', 'Отчёт родителю · май 2026', 'Юлия Игоревна', 'Дана укрепляется: грамматика подросла, ответы стали ровнее. Сильные разделы — аудирование и чтение; зоны роста — spelling, word formation, speaking и writing по критериям ЕГЭ.', '# Краткий вывод

В апреле Дана работала в формате подготовки к ЕГЭ: грамматика, словообразование, устная часть и диагностические задания. Подключали TOEFL-формат и Langart.

# Май

6 занятий к оплате после переноса 2 занятий из апреля.', 'https://www.notion.so/35a7364cba7981ef858beda6387ad2f5');
insert into public.reports (student_id, month, type, status, title, recipient_label, short_message, content_markdown, notion_url) values ((select id from public.students where slug = 'yulya-lushina'), '2026-05', 'parent_report', 'draft', 'Отчёт родителю · май 2026', 'родитель', 'Юля занимается в игровом формате. Главный прогресс — узнавание английского в понятных ситуациях, реакция на команды и повторение коротких фраз.', '# Краткий вывод

Юля занимается в игровом формате: движение, картинки, персонажи, игрушки и короткие повторяющиеся фразы.

# Следующий фокус

Body and face, This is my..., I have..., He/She/It has..., feelings, animals, actions.', 'https://www.notion.so/35a7364cba79819c9339d3c4f4953e46');

-- ---------- 8. CONTRACTS ----------
-- contracts заполняются через scripts/upload-contracts.js (один файл = одна строка)
-- этот скрипт загружает PDF/JPG/PNG в Storage bucket 'contracts' и создаёт записи в БД

-- =============================================================
-- DONE.
-- =============================================================
