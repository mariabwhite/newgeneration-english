"""Bulk theme swap: shopping → jobs & hobbies. Edits JS arrays + section headers in place."""
import re, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = os.path.join(os.path.dirname(__file__), 'index.html')
with open(p, 'r', encoding='utf-8') as f: s = f.read()
orig_len = len(s)

# ───────── 1. WARMUP MCQ 8 items ─────────
WARMUP_NEW = """const WARMUP = [
  {q:"Which TWO are jobs you do with your hands outdoors or on a building site?", opts:["bricklayer and carpenter","librarian and pharmacist","nurse and bodyguard"], answer:0},
  {q:"A «hairdresser» is someone who…", opts:["sells medicines at a pharmacy","cuts and styles hair","collects refuse from houses"], answer:1},
  {q:"The usual word for the person who takes care of hotel guests at the entrance desk is…", opts:["a tailor","a receptionist","a vet"], answer:1},
  {q:"«To pursue a hobby» means…", opts:["to give it up","to keep doing it seriously, year after year","to try it just once"], answer:1},
  {q:"«To be strapped for cash» is to «to be broke» as «dream job» is to…", opts:["dead-end job","part-time gig","job that fits you perfectly"], answer:2},
  {q:"A «vet» is short for…", opts:["veteran","veterinarian","vetter"], answer:1},
  {q:"If you say «I took up chess last autumn», you mean…", opts:["you quit chess","you started playing chess","you played against a champion"], answer:1},
  {q:"The British word for a person who collects your rubbish from the bins is…", opts:["dustman","garbage boy","wasteman"], answer:0}
];"""
s = re.sub(r"const WARMUP = \[.*?\];", lambda m: WARMUP_NEW, s, count=1, flags=re.DOTALL)

# ───────── 2. PHRASES_0B — 15 modern teen Jobs & Hobbies phrases ─────────
PHRASES_0B_NEW = """const PHRASES_0B = [
  {word:'to land a job',           pos:'phr. verb',   ipa:'/tə lænd ə dʒɒb/',           ru:'заполучить работу',                      def:'to be hired for a job (usually after effort)',                   ex:"She landed a part-time job at a vet clinic last summer."},
  {word:'dream job',               pos:'noun',        ipa:'/driːm dʒɒb/',               ru:'работа мечты',                           def:'the job you most want to have one day',                          ex:"Being a journalist in London is her dream job."},
  {word:'dead-end job',            pos:'noun',        ipa:'/ded end dʒɒb/',             ru:'бесперспективная работа',                def:'a job that gives no promotion and no growth',                    ex:"He stuck a dead-end job for three years before quitting."},
  {word:'part-time gig',           pos:'noun (info)', ipa:'/pɑːt taɪm ɡɪɡ/',            ru:'подработка (на пару часов)',             def:'a small informal job for a few hours a week',                    ex:"I\\u2019ve picked up a part-time gig at the library on Saturdays."},
  {word:'to apply for a job',      pos:'phr. verb',   ipa:'/tə əˈplaɪ fə(r) ə dʒɒb/',   ru:'подать заявку на работу',                def:'to send your CV / fill in a form to be considered',              ex:"I\\u2019m applying for three summer jobs this week."},
  {word:'to be hired / fired',     pos:'passive · phr', ipa:'/tə bi ˈhaɪəd / ˈfaɪəd/',   ru:'быть нанятым / уволенным',               def:'passive: your employer takes you on / lets you go',               ex:"Two new coaches were hired; one was fired after a month."},
  {word:'to pursue a hobby',       pos:'phr. verb',   ipa:'/tə pəˈsjuː ə ˈhɒbi/',       ru:'серьёзно заниматься хобби',              def:'to keep doing it over time, with real commitment',               ex:"If I had more time, I would pursue photography seriously."},
  {word:'to take up (something)',  pos:'phrasal',     ipa:'/tə teɪk ʌp/',               ru:'начать заниматься (хобби)',              def:'to start doing a new hobby or activity',                         ex:"She took up knitting after she retired."},
  {word:'to give (something) up',  pos:'phrasal',     ipa:'/tə ɡɪv ʌp/',                ru:'бросить (хобби/привычку)',               def:'to stop doing an activity you used to do',                       ex:"He gave up chess after losing three tournaments in a row."},
  {word:'to be keen on',           pos:'phr. · adj',  ipa:'/tə bi kiːn ɒn/',            ru:'сильно увлекаться (чем-то)',             def:'to really enjoy something, to be enthusiastic about it',         ex:"She\\u2019s very keen on amateur astronomy."},
  {word:'to be into (something)',  pos:'phr. · adj (info)', ipa:'/tə bi ˈɪntuː/',         ru:'тащиться по (чему-то)',                  def:'informal for \\u00abto be keen on\\u00bb',                      ex:"My brother is really into skateboarding at the moment."},
  {word:'a pastime',               pos:'noun',        ipa:'/ə ˈpɑːstaɪm/',              ru:'времяпрепровождение, увлечение',         def:'a hobby or activity you do for pleasure in free time',           ex:"Chess is a popular pastime among retired engineers."},
  {word:'in my leisure (hours)',   pos:'phr',         ipa:'/ɪn maɪ ˈleʒə/',             ru:'в свободное время',                      def:'during the hours when you\\u2019re not working',                 ex:"In her leisure hours she paints watercolours of the river."},
  {word:'to be a go-to (hobby)',   pos:'phr',         ipa:'/tə bi ə ˈɡəʊ tuː/',         ru:'основное / любимое (хобби)',             def:'the one you always come back to',                                 ex:"Reading mysteries is my go-to pastime on a rainy weekend."},
  {word:'to kill time',            pos:'idiom',       ipa:'/tə kɪl taɪm/',              ru:'убивать время',                          def:'to do something unimportant while waiting',                      ex:"I played mobile chess to kill time at the airport."}
];"""
s = re.sub(r"const PHRASES_0B = \[.*?\];", lambda m: PHRASES_0B_NEW, s, count=1, flags=re.DOTALL)

# ───────── 3. PHRASES_DRILL 15 gap-fills ─────────
PHRASES_DRILL_NEW = """const PHRASES_DRILL = [
  {ctx:"She ______ a part-time job at a vet clinic last summer.",                                              hint:'заполучить работу',                        answer:'landed'},
  {ctx:"Being a journalist in London is her ______ — she has been working towards it since she was fifteen.",   hint:'работа мечты',                             answer:'dream job'},
  {ctx:"He stuck in a ______ for three years before finally quitting.",                                        hint:'бесперспективная работа',                  answer:'dead-end job'},
  {ctx:"I\\u2019ve picked up a ______ at the library on Saturday mornings.",                                     hint:'подработка на пару часов',                 answer:'part-time gig'},
  {ctx:"I\\u2019m ______ three summer jobs this week.",                                                          hint:'подавать заявку на',                        answer:'applying for'},
  {ctx:"Two new coaches ______ this autumn; one ______ after a single month.",                                 hint:'были наняты / были уволены',               answer:'were hired / were fired|were hired, were fired|were hired · were fired'},
  {ctx:"If I had more free time, I would ______ photography seriously.",                                        hint:'серьёзно заниматься (хобби)',               answer:'pursue'},
  {ctx:"My grandmother ______ knitting the year she retired.",                                                   hint:'начала заниматься (хобби)',                 answer:'took up'},
  {ctx:"He ______ chess after losing three tournaments in a row.",                                               hint:'бросил',                                   answer:'gave up'},
  {ctx:"She\\u2019s very ______ amateur astronomy.",                                                              hint:'сильно увлечена чем-то',                   answer:'keen on'},
  {ctx:"My brother is really ______ skateboarding at the moment.",                                               hint:'тащится по',                               answer:'into'},
  {ctx:"Chess is a popular ______ among retired engineers.",                                                     hint:'увлечение, хобби',                         answer:'pastime'},
  {ctx:"In her ______ she paints watercolours of the river.",                                                    hint:'в свободное время',                        answer:'leisure|leisure hours'},
  {ctx:"Reading mysteries is my ______ pastime on a rainy weekend.",                                             hint:'любимое, основное',                        answer:'go-to'},
  {ctx:"I played mobile chess to ______ at the airport until my flight was called.",                             hint:'убить время',                              answer:'kill time'}
];"""
s = re.sub(r"const PHRASES_DRILL = \[.*?\];", lambda m: PHRASES_DRILL_NEW, s, count=1, flags=re.DOTALL)

# ───────── 4. TV_VOCAB — 6 jobs/hobbies tabs ─────────
TV_VOCAB_NEW = """const TV_VOCAB = {
  'tv-shops': [
    {term:'bricklayer', ipa:'/ˈbrɪkˌleɪə/', ru:'каменщик', ex:'The garden wall was built by two bricklayers in three days.'},
    {term:'hairdresser', ipa:'/ˈheəˌdresə/', ru:'парикмахер', ex:'My hair is cut by the same hairdresser every month.'},
    {term:'barber', ipa:'/ˈbɑːbə/', ru:'мужской парикмахер / цирюльник', ex:'Grandfather goes to the old-fashioned barber on the corner.'},
    {term:'receptionist', ipa:'/rɪˈsepʃənɪst/', ru:'администратор', ex:'Hotel keys are handed out by the receptionist.'},
    {term:'pharmacist / chemist', ipa:'/ˈfɑːməsɪst/', ru:'фармацевт', ex:'Medicines are sold only by a licensed pharmacist.'},
    {term:'dustman / refuse collector', ipa:'/ˈdʌstmən/', ru:'мусорщик', ex:'The bins are emptied by the dustmen every Wednesday.'},
    {term:'bodyguard', ipa:'/ˈbɒdiɡɑːd/', ru:'телохранитель', ex:'The US president is protected by Secret Service bodyguards.'},
    {term:'librarian', ipa:'/laɪˈbreəriən/', ru:'библиотекарь', ex:'New books are ordered by the librarian every month.'},
    {term:'carpenter', ipa:'/ˈkɑːpɪntə/', ru:'плотник', ex:'The bookshelf was made by a local carpenter in his garage.'},
    {term:'tailor', ipa:'/ˈteɪlə/', ru:'портной', ex:'His wedding suit was sewn by an old Italian tailor.'},
    {term:'vet / veterinarian', ipa:'/vet/', ru:'ветеринар', ex:'Our puppy is vaccinated by the local vet every year.'},
    {term:'nurse', ipa:'/nɜːs/', ru:'медсестра / медбрат', ex:'A night nurse was hired to look after the elderly patient.'},
    {term:'shepherd', ipa:'/ˈʃepəd/', ru:'пастух', ex:'A shepherd works alone with his dog for most of the day.'},
    {term:'journalist / reporter', ipa:'/ˈdʒɜːnəlɪst/', ru:'журналист', ex:'The scandal was uncovered by two young journalists.'},
    {term:'dentist', ipa:'/ˈdentɪst/', ru:'стоматолог', ex:'A new dentist has been hired at the clinic down the road.'},
    {term:'mechanic', ipa:'/mɪˈkænɪk/', ru:'механик, автослесарь', ex:'Her car was repaired by a mechanic in two hours.'}
  ],
  'tv-money': [
    {term:'salary', ipa:'/ˈsæləri/', ru:'зарплата (помесячная)', ex:'A librarian\\u2019s salary is modest but very stable.'},
    {term:'wage(s)', ipa:'/weɪdʒ/', ru:'зарплата (почасовая / недельная)', ex:'Builders are usually paid a weekly wage, not a salary.'},
    {term:'bonus', ipa:'/ˈbəʊnəs/', ru:'премия, бонус', ex:'A Christmas bonus was given to all permanent staff.'},
    {term:'commission', ipa:'/kəˈmɪʃn/', ru:'комиссия, процент с продаж', ex:'Estate agents earn most of their money in commission.'},
    {term:'overtime', ipa:'/ˈəʊvətaɪm/', ru:'сверхурочные', ex:'Nurses are often paid double for weekend overtime.'},
    {term:'to apply for a job', ipa:'/tə əˈplaɪ fər ə dʒɒb/', ru:'подать заявку на работу', ex:'She applied for three summer jobs online.'},
    {term:'to be hired', ipa:'/tə bi ˈhaɪəd/', ru:'быть нанятым', ex:'Two apprentices were hired for the summer.'},
    {term:'to be fired / sacked', ipa:'/tə bi ˈfaɪəd/', ru:'быть уволенным', ex:'He was fired for turning up late four Mondays in a row.'},
    {term:'to resign / to quit', ipa:'/tə rɪˈzaɪn/', ru:'уволиться по собственному желанию', ex:'She resigned after the new manager arrived.'},
    {term:'to be promoted', ipa:'/tə bi prəˈməʊtɪd/', ru:'быть повышенным', ex:'He was promoted to senior editor after only one year.'},
    {term:'employee', ipa:'/ɪmˈplɔɪiː/', ru:'работник, сотрудник', ex:'The company has 200 employees in the London office.'},
    {term:'employer', ipa:'/ɪmˈplɔɪə/', ru:'работодатель', ex:'A good employer gives training and real responsibility.'},
    {term:'employment', ipa:'/ɪmˈplɔɪmənt/', ru:'трудоустройство', ex:'Youth employment rose by 3% last quarter.'},
    {term:'unemployment', ipa:'/ˌʌnɪmˈplɔɪmənt/', ru:'безработица', ex:'Unemployment is highest in small coastal towns.'},
    {term:'self-employed', ipa:'/ˌself ɪmˈplɔɪd/', ru:'самозанятый / ИП', ex:'My aunt is self-employed as a wedding photographer.'},
    {term:'full-time / part-time', ipa:'/fʊl taɪm/', ru:'полная / неполная занятость', ex:'He has a full-time job on weekdays and a part-time gig on Saturdays.'}
  ],
  'tv-clothes': [
    {term:'hobby', ipa:'/ˈhɒbi/', ru:'хобби', ex:'His main hobby is model aviation.'},
    {term:'pastime', ipa:'/ˈpɑːstaɪm/', ru:'времяпрепровождение', ex:'Chess is a popular pastime among retired engineers.'},
    {term:'leisure', ipa:'/ˈleʒə/', ru:'досуг, свободное время', ex:'What do you do in your leisure hours?'},
    {term:'to collect (stamps / coins)', ipa:'/tə kəˈlekt/', ru:'коллекционировать', ex:'Stamps have been collected in our family for 60 years.'},
    {term:'to knit / to sew', ipa:'/tə nɪt / tə səʊ/', ru:'вязать / шить', ex:'She knits scarves and sews skirts for her sisters.'},
    {term:'to paint watercolours', ipa:'/tə peɪnt ˈwɔːtəkʌləz/', ru:'писать акварелью', ex:'He paints watercolours of the river on weekends.'},
    {term:'to play chess / cards', ipa:'/tə pleɪ tʃes/', ru:'играть в шахматы / карты', ex:'We played chess every evening last summer.'},
    {term:'to go hiking / cycling', ipa:'/tə ɡəʊ ˈhaɪkɪŋ/', ru:'ходить в походы / кататься на велосипеде', ex:'They go hiking every weekend in the Lake District.'},
    {term:'to go fishing / dancing', ipa:'/tə ɡəʊ ˈfɪʃɪŋ/', ru:'ходить на рыбалку / танцевать', ex:'My grandfather goes fishing every Saturday morning.'},
    {term:'to practise an instrument', ipa:'/tə ˈpræktɪs/', ru:'упражняться на муз. инструменте', ex:'He practises the violin for an hour every day.'},
    {term:'to join a club', ipa:'/tə dʒɔɪn ə klʌb/', ru:'вступить в клуб / секцию', ex:'I joined the school chess club in September.'},
    {term:'to take up chess', ipa:'/tə teɪk ʌp/', ru:'начать играть в шахматы', ex:'She took up chess at the age of ten.'},
    {term:'to give up karate', ipa:'/tə ɡɪv ʌp/', ru:'бросить карате', ex:'He gave up karate at twelve.'},
    {term:'amateur', ipa:'/ˈæmətə/', ru:'любитель (не профессионал)', ex:'She\\u2019s an amateur astronomer with a serious telescope.'},
    {term:'enthusiast', ipa:'/ɪnˈθjuːziæst/', ru:'энтузиаст, фанат', ex:'He is a model-railway enthusiast with 300 metres of track.'},
    {term:'to be hooked on', ipa:'/tə bi hʊkt ɒn/', ru:'подсесть на (хобби)', ex:'My little brother is hooked on online chess puzzles.'}
  ],
  'tv-goods': [
    {term:'to work overtime', ipa:'/tə wɜːk ˈəʊvətaɪm/', ru:'работать сверхурочно', ex:'Nurses work a lot of overtime at Christmas.'},
    {term:'to meet a deadline', ipa:'/tə miːt ə ˈdedlaɪn/', ru:'уложиться в срок', ex:'Journalists must meet strict deadlines every day.'},
    {term:'to handle customers', ipa:'/tə ˈhændl ˈkʌstəməz/', ru:'работать с клиентами', ex:'Receptionists must handle difficult customers politely.'},
    {term:'to work with your hands', ipa:'/tə wɜːk wɪð jɔː hændz/', ru:'работать руками', ex:'Carpenters work with their hands all day.'},
    {term:'to work outdoors', ipa:'/tə wɜːk aʊtˈdɔːz/', ru:'работать на открытом воздухе', ex:'Shepherds and bricklayers both work outdoors.'},
    {term:'to work indoors', ipa:'/tə wɜːk ɪnˈdɔːz/', ru:'работать в помещении', ex:'A librarian works indoors; a vet is sometimes in the open.'},
    {term:'to work with people / animals / numbers / machines', ipa:'/tə wɜːk wɪð/', ru:'работать с людьми / животными / числами / техникой', ex:'A good vet must work with both animals and anxious owners.'},
    {term:'shift work', ipa:'/ʃɪft wɜːk/', ru:'сменная работа', ex:'Shift work can be hard on your sleep.'},
    {term:'night shift / day shift', ipa:'/naɪt ʃɪft/', ru:'ночная / дневная смена', ex:'She hates the night shift at the hospital.'},
    {term:'to train for a job', ipa:'/tə treɪn fə(r)/', ru:'учиться на профессию', ex:'He is training for a job as an electrician.'},
    {term:'an apprentice', ipa:'/ən əˈprentɪs/', ru:'ученик, подмастерье', ex:'The old tailor took on two apprentices last spring.'},
    {term:'to be in charge of', ipa:'/tə bi ɪn tʃɑːdʒ ɒv/', ru:'отвечать за, руководить', ex:'She is in charge of ten junior staff.'},
    {term:'to deal with (customers)', ipa:'/tə diːl wɪð/', ru:'иметь дело с', ex:'A hairdresser deals with hundreds of customers a month.'},
    {term:'to report to (a boss)', ipa:'/tə rɪˈpɔːt tuː/', ru:'подчиняться (руководителю)', ex:'All junior editors report to the chief editor.'},
    {term:'rewarding (job)', ipa:'/rɪˈwɔːdɪŋ/', ru:'приносящий удовлетворение', ex:'Being a vet is tiring but rewarding.'},
    {term:'demanding (job)', ipa:'/dɪˈmɑːndɪŋ/', ru:'требовательный, нагрузочный', ex:'Journalism is a demanding profession with long hours.'}
  ],
  'tv-customer': [
    {term:'job interview', ipa:'/dʒɒb ˈɪntəvjuː/', ru:'собеседование на работу', ex:'My job interview is on Wednesday at ten.'},
    {term:'CV / resume', ipa:'/siː viː/', ru:'резюме', ex:'Please send your CV to our HR email.'},
    {term:'covering letter', ipa:'/ˈkʌvərɪŋ ˈletə/', ru:'сопроводительное письмо', ex:'A short covering letter is still expected in Britain.'},
    {term:'experience / work experience', ipa:'/ɪkˈspɪəriəns/', ru:'опыт работы', ex:'Three years of experience in retail is a plus.'},
    {term:'qualifications', ipa:'/ˌkwɒlɪfɪˈkeɪʃnz/', ru:'квалификация, дипломы', ex:'What qualifications do you have for this role?'},
    {term:'skills', ipa:'/skɪlz/', ru:'умения, навыки', ex:'Communication skills matter more than diplomas sometimes.'},
    {term:'strengths and weaknesses', ipa:'/streŋkθs/', ru:'сильные и слабые стороны', ex:'Name three of your strengths and one weakness.'},
    {term:'to be well-paid / badly-paid', ipa:'/wel peɪd/', ru:'хорошо / плохо оплачиваемый', ex:'Nursing is rewarding but badly-paid in many countries.'},
    {term:'to earn (a living)', ipa:'/tə ɜːn/', ru:'зарабатывать на жизнь', ex:'She earns a living as a wedding photographer.'},
    {term:'take-home pay', ipa:'/teɪk həʊm peɪ/', ru:'зарплата на руки (после налогов)', ex:'Her take-home pay is 85% of her gross salary.'},
    {term:'flexible hours', ipa:'/ˈfleksəbl ˈaʊəz/', ru:'гибкий график', ex:'Flexible hours were introduced last year.'},
    {term:'to be made redundant', ipa:'/tə bi meɪd rɪˈdʌndənt/', ru:'попасть под сокращение', ex:'Twenty staff were made redundant when the factory closed.'},
    {term:'promotion', ipa:'/prəˈməʊʃn/', ru:'повышение', ex:'A promotion was offered to her after six months.'},
    {term:'pay rise', ipa:'/peɪ raɪz/', ru:'повышение зарплаты', ex:'A 5% pay rise is expected this spring.'},
    {term:'to retire', ipa:'/tə rɪˈtaɪə/', ru:'выйти на пенсию', ex:'He retired at 65 and immediately took up gardening.'},
    {term:'pension', ipa:'/ˈpenʃn/', ru:'пенсия', ex:'Her state pension is topped up by a small private one.'}
  ],
  'tv-adv': [
    {term:'hard (work)', ipa:'/hɑːd/', ru:'тяжёлый (о работе)', ex:'Bricklaying is hard work in July.'},
    {term:'hardly (ever)', ipa:'/ˈhɑːdli/', ru:'почти никогда', ex:'A good tailor hardly ever makes a mistake with measurements.'},
    {term:'late (hours)', ipa:'/leɪt/', ru:'поздний (о часах)', ex:'Doctors sometimes work very late hours.'},
    {term:'lately', ipa:'/ˈleɪtli/', ru:'в последнее время', ex:'Lately she has taken up watercolour painting.'},
    {term:'near (the office)', ipa:'/nɪə/', ru:'рядом (с офисом)', ex:'His flat is near the office — a ten-minute walk.'},
    {term:'nearly (every day)', ipa:'/ˈnɪəli/', ru:'почти (каждый день)', ex:'She practises the violin nearly every day.'},
    {term:'well-trained', ipa:'/wel treɪnd/', ru:'хорошо обученный', ex:'A well-trained bodyguard reacts in half a second.'},
    {term:'badly-trained', ipa:'/ˈbædli treɪnd/', ru:'плохо обученный', ex:'A badly-trained dog can be dangerous.'},
    {term:'highly-skilled', ipa:'/ˈhaɪli skɪld/', ru:'высококвалифицированный', ex:'Carpenters are highly-skilled workers.'},
    {term:'low-skilled', ipa:'/ləʊ skɪld/', ru:'низкоквалифицированный', ex:'Low-skilled jobs are the first to be lost to automation.'},
    {term:'full-time', ipa:'/fʊl taɪm/', ru:'на полный день', ex:'A full-time nurse works 36-40 hours a week.'},
    {term:'part-time', ipa:'/pɑːt taɪm/', ru:'на неполный день', ex:'He has a part-time job at a cafe on weekends.'},
    {term:'self-employed', ipa:'/ˌself ɪmˈplɔɪd/', ru:'самозанятый', ex:'A self-employed tailor keeps all his earnings — but pays his own tax.'},
    {term:'permanent / temporary', ipa:'/ˈpɜːmənənt/', ru:'постоянный / временный', ex:'She was offered a permanent contract after two temporary ones.'},
    {term:'freelance', ipa:'/ˈfriːlɑːns/', ru:'на фрилансе', ex:'He works freelance for three magazines at once.'},
    {term:'under-paid', ipa:'/ˌʌndə peɪd/', ru:'недооплачиваемый', ex:'Teachers are often under-paid for the hours they put in.'}
  ]
};"""
s = re.sub(r"const TV_VOCAB = \{.*?\n\};\s*", lambda m: TV_VOCAB_NEW + "\n", s, count=1, flags=re.DOTALL)

# ───────── 5. Section headers (h2) ─────────
header_swaps = [
    ("Warm-up · 15 phrases modern teenagers actually use about shopping &amp; money",
     "Warm-up · 15 phrases modern teenagers actually use about jobs &amp; hobbies"),
    ("Vocabulary · 20 words to own",
     "Vocabulary · 20 jobs &amp; hobbies words to own"),
    ("Vocabulary speaking · 10 rounds, 10 games",
     "Vocabulary speaking · 10 rounds, 10 games · jobs &amp; hobbies"),
    ("Vocabulary practice · match + fill",
     "Vocabulary practice · match job to description + fill passive"),
    ("Features of a Good Shopping Centre",
     "Features of a Good Job / Dream Job"),
    ("Features practice · gap-fill from the checklist",
     "Features-of-a-Job practice · gap-fill from the checklist"),
    ("Shop Assistant · Two Sides of the Counter",
     "Bodyguard · Two Sides of the Job"),
    ("Shop-assistant practice · advantage or disadvantage?",
     "Bodyguard practice · advantage or disadvantage?"),
    ("The Verger · by W. Somerset Maugham",
     "Unusual Jobs: A Bodyguard · adapted from Afanasyeva Unit 1"),
    ("Phrasal Verb · TO PUT",
     "Phrasal verbs around work &amp; hobbies · take up / give up / apply for / look into"),
    ("Modal Verbs · Can / Could / May / Might + be able to",
     "Passive voice · 8 tenses + Conditionals 0/1/2/3/mixed + wish"),
    ("OGE Grammar · Tasks 20-28 · Word transformation · 9 gaps · Shopping topic",
     "OGE Grammar · Tasks 20-28 · Word transformation · 9 gaps · Jobs topic"),
    ("OGE Vocabulary · Tasks 29-34 · Word formation · 6 gaps · Shopping topic",
     "OGE Vocabulary · Tasks 29-34 · Word formation · 6 gaps · EMPLOY / CARE / COLLECT / CREATE"),
    ("Reading · Shopping in Britain",
     "Reading · Hobbies in Britain · by age (Afanasyeva Unit 1 stage p.5)"),
    ("Reading 2 · «What Makes Money Valuable?»",
     "Reading 2 · «Why Some Jobs Pay More Than Others»"),
    ("Adverbs · dual forms + irregular degrees of comparison",
     "Conditionals · 0 / 1 / 2 / 3 / mixed + wish · drill"),
    ("Focus · <em>what</em> vs <em>which</em> + fitting-room verbs",
     "Focus · reported speech in job interviews ·  <em>what</em> vs <em>which</em>"),
    ("Shop English · at the fitting room, at the till",
     "Interview English · in the interview room, on the phone"),
    ("Eight quick multiple-choice questions on British shops and money. Answer from memory first, then check.",
     "Eight quick multiple-choice questions on jobs &amp; hobbies vocabulary. Answer from memory first, then check."),
    ("tap a card to flip · then answer the 6 questions below using at least 5 of these phrases",
     "tap a card to flip · then answer the 6 questions below using at least 5 of these jobs/hobbies phrases"),
    ("B · Money &amp; banking", "B · Hire / fire / salary"),
    ("C · Clothes &amp; fashion", "C · Hobbies &amp; pastimes"),
    ("D · What a shopping centre sells", "D · What people actually DO at work"),
    ("E · Customer verbs &amp; till English", "E · Job-interview English"),
    ("F · Tricky adverbs (hard/hardly, near/nearly…)", "F · Tricky adverbs (hard/hardly, late/lately, near/nearly) + full-time/part-time"),
    ("A · Types of shops", "A · Jobs vocabulary"),
    ("These words come back in every section — the reading and «The Verger» especially.",
     "These words come back in every section — the Bodyguard reading and the Conditionals drill especially."),
    ("📖 Full Topical Vocabulary from the textbook (Unit 3 · pp. 91-134)",
     "📖 Full Topical Vocabulary from the textbook (Afanasyeva 8 · Unit 1 · pp. 5-55)"),
    ("Pick 5 items you think are the MOST important (green) for a great shopping centre, and 5 you think are the LEAST important (red). Compare with your partner and defend your choice.",
     "Pick 5 features you think are the MOST important (green) in a job, and 5 you think are the LEAST important (red). Compare with your partner and defend your choice."),
    ("Ten sentences describing a shopping centre. Type the missing feature from the checklist above.",
     "Ten sentences describing a job. Type the missing feature from the checklist above."),
]
for old, new in header_swaps:
    s = s.replace(old, new)

with open(p, 'w', encoding='utf-8') as f: f.write(s)
print(f'swap done. before={orig_len:,} after={len(s):,}')
