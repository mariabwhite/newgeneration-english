# Cabinet release and vault checklist

Canonical cabinet URL: https://newgeneration-english.ru/cabinet/

Do not reintroduce cabinet.newgeneration-english.ru as a separate live origin. If the old subdomain exists, it must redirect to the canonical cabinet URL.

## Before a cabinet release

1. Update cabinet/build.txt when browser-visible cabinet behavior changes.
2. Bump cabinet.js and/or data.js query strings in the cabinet HTML entrypoints.
3. Run:

   node scripts/check-cabinet-release.js

4. If active family PINs or family report data changed, regenerate the static iPad fallback vault:

   $env:CABINET_PIN_LIST='<active 4-digit pins separated by comma>'
   node scripts/gen-family-vault-from-live.js
   Remove-Item Env:CABINET_PIN_LIST

The generator writes to cabinet/.vault-next first and replaces cabinet/vault only after every family entry was fetched and encrypted successfully. It must not print PINs into logs.

## iPad fallback contract

Normal login tries Supabase family-data first. If Safari/iPad cannot reach Supabase, cabinet.js tries the encrypted same-origin static vault under cabinet/vault/ and decrypts it in the browser using the entered PIN.

## No-cache policy

GitHub Pages does not apply _headers like Cloudflare Pages. Cabinet HTML files must carry no-cache meta tags, and JS/data assets must use explicit cachebusters.