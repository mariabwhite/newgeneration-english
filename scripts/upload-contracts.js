// scripts/upload-contracts.js
// Загружает все файлы из site/cabinet/assets/contracts/ в Supabase Storage bucket 'contracts'
// + создаёт строки в таблице public.contracts.
//
// Использует ТОЛЬКО Node.js native fetch (Node 18+). Никаких npm install.
//
// Service_role key читается из ../supabase-config.md (НЕ из git).
//
// Запуск (CMD):
//   cd /d "C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\01_Сайт New Generation — сайт, Lab, кабинет" && node scripts/upload-contracts.js
//
// Запуск (PowerShell):
//   cd "C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\01_Сайт New Generation — сайт, Lab, кабинет"; node scripts/upload-contracts.js

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const CONFIG_MD = path.join(ROOT, "supabase-config.md");
const CONTRACTS_DIR = path.join(ROOT, "site", "cabinet", "assets", "contracts");
const BUCKET = "contracts";

// ---------- 1. read Supabase URL + secret from config ----------
const cfg = fs.readFileSync(CONFIG_MD, "utf-8");
const urlMatch    = cfg.match(/https:\/\/([a-z0-9]+)\.supabase\.co/);
const secretMatch = cfg.match(/(sb_secret_[A-Za-z0-9_-]+)/);
if (!urlMatch || !secretMatch) {
  console.error("ОШИБКА: не нашла URL или secret_key в supabase-config.md");
  process.exit(1);
}
const SUPABASE_URL = `https://${urlMatch[1]}.supabase.co`;
const SECRET = secretMatch[1];

// ---------- 2. helpers ----------
const MIME = { ".pdf":"application/pdf", ".jpg":"image/jpeg", ".jpeg":"image/jpeg", ".png":"image/png", ".webp":"image/webp" };

// Supabase Storage не принимает кириллицу в путях → транслитерация
const TRANS_MAP = {
  'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'zh','з':'z',
  'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
  'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sch',
  'ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya',
  'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'Yo','Ж':'Zh','З':'Z',
  'И':'I','Й':'Y','К':'K','Л':'L','М':'M','Н':'N','О':'O','П':'P','Р':'R',
  'С':'S','Т':'T','У':'U','Ф':'F','Х':'H','Ц':'Ts','Ч':'Ch','Ш':'Sh','Щ':'Sch',
  'Ъ':'','Ы':'Y','Ь':'','Э':'E','Ю':'Yu','Я':'Ya',
  ' ':'_','№':'no','«':'','»':'',',':'','(':'',')':'',
};
function slugifyFilename(name) {
  return name.split('').map((c) => TRANS_MAP[c] !== undefined ? TRANS_MAP[c] : c).join('')
    .replace(/[^a-zA-Z0-9._-]/g, '_')   // всё остальное → _
    .replace(/__+/g, '_');               // схлопнуть подряд idущие _
}

const HEADERS_REST = {
  "apikey": SECRET,
  "Authorization": `Bearer ${SECRET}`,
  "Content-Type": "application/json",
};

async function rest(method, pathname, body) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1${pathname}`, {
    method,
    headers: { ...HEADERS_REST, ...(method === "POST" ? { Prefer: "return=representation" } : {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await r.text();
  if (!r.ok) throw new Error(`REST ${method} ${pathname} → ${r.status}: ${text}`);
  return text ? JSON.parse(text) : null;
}

async function uploadFile(storagePath, buffer, mime) {
  const url = `${SUPABASE_URL}/storage/v1/object/${BUCKET}/${encodeURI(storagePath)}`;
  const r = await fetch(url, {
    method: "POST",
    headers: {
      "apikey": SECRET,
      "Authorization": `Bearer ${SECRET}`,
      "Content-Type": mime,
      "x-upsert": "true",
    },
    body: buffer,
  });
  const text = await r.text();
  if (!r.ok) throw new Error(`Storage ${r.status}: ${text}`);
  return text;
}

// ---------- 3. folder → student slug mapping ----------
const FOLDER_TO_SLUGS = {
  "sova-family": ["sova-elena", "sova-ekaterina"],
};

// ---------- 4. main ----------
async function main() {
  console.log("Supabase URL:", SUPABASE_URL);
  console.log("Contracts:    ", CONTRACTS_DIR);

  // check bucket
  const bResp = await fetch(`${SUPABASE_URL}/storage/v1/bucket/${BUCKET}`, {
    headers: { "apikey": SECRET, "Authorization": `Bearer ${SECRET}` },
  });
  if (!bResp.ok) {
    console.error(`\nОШИБКА: bucket '${BUCKET}' не найден (HTTP ${bResp.status}).`);
    console.error("Создай его в UI: Supabase → Storage → New bucket → 'contracts' → Private.");
    process.exit(1);
  }
  console.log("Bucket 'contracts' OK.");

  // wipe existing contracts rows
  console.log("\nЧищу public.contracts перед заливкой...");
  try {
    await rest("DELETE", `/contracts?id=neq.00000000-0000-0000-0000-000000000000`);
  } catch (e) {
    console.warn("warn delete:", e.message);
  }

  // fetch students id+slug map
  const students = await rest("GET", `/students?select=id,slug`);
  const slugToId = Object.fromEntries(students.map((s) => [s.slug, s.id]));

  const folders = fs.readdirSync(CONTRACTS_DIR).filter((f) => fs.statSync(path.join(CONTRACTS_DIR, f)).isDirectory());

  let total = 0, ok = 0, fail = 0;

  for (const folder of folders) {
    const folderPath = path.join(CONTRACTS_DIR, folder);
    const slugs = FOLDER_TO_SLUGS[folder] || [folder];
    const studentRecords = slugs.map((s) => ({ slug: s, id: slugToId[s] })).filter((s) => s.id);
    if (!studentRecords.length) {
      console.warn(`\n[${folder}] ни один из slug-ов не найден в БД: ${slugs.join(", ")}`);
      continue;
    }

    console.log(`\n[${folder}] → ${studentRecords.map(s => s.slug).join(", ")}`);

    const files = fs.readdirSync(folderPath);
    for (const file of files) {
      const filePath = path.join(folderPath, file);
      if (!fs.statSync(filePath).isFile()) continue;
      total++;

      const ext = path.extname(file).toLowerCase();
      const mime = MIME[ext] || "application/octet-stream";
      const buf = fs.readFileSync(filePath);
      const primarySlug = studentRecords[0].slug;
      const safeFile = slugifyFilename(file);   // транслит для Storage
      const storagePath = `${primarySlug}/${safeFile}`;

      try {
        await uploadFile(storagePath, buf, mime);
      } catch (e) {
        console.log(`  ✗ ${file} — upload: ${e.message}`);
        fail++; continue;
      }

      // doc type
      let docType = "договор";
      if (/согласие/i.test(file)) docType = "согласие_на_ПД";
      else if (/доп/i.test(file)) docType = "доп";
      else if (/реквизит/i.test(file)) docType = "реквизиты";

      // one contracts row per linked student
      for (const sRec of studentRecords) {
        try {
          await rest("POST", `/contracts`, {
            student_id: sRec.id,
            status: "signed",
            signed_date: null,
            storage_bucket: BUCKET,
            storage_path: storagePath,
            original_filename: file,
            mime_type: mime,
            file_size: buf.length,
            doc_type: docType,
            note: studentRecords.length > 1 ? `общий документ (${studentRecords.map(x => x.slug).join(" + ")})` : null,
          });
        } catch (e) {
          console.log(`  ✗ ${file} db insert for ${sRec.slug}: ${e.message}`);
          fail++;
        }
      }
      console.log(`  ✓ ${file} (${(buf.length / 1024).toFixed(0)} КБ, ${docType})`);
      ok++;
    }
  }

  console.log(`\n=== ИТОГ: загружено ${ok} из ${total} файлов, ошибок ${fail}`);
}

main().catch((e) => {
  console.error("FATAL:", e);
  process.exit(1);
});
