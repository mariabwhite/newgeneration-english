# Note for Claude: Premium Vault is now manifest-driven

Premium Vault architecture has already been rebuilt.

Do not return to manual edits where lesson folder, premium card and encrypted Vault are maintained separately.

## Current rule

New premium lesson flow:

1. Add lesson files under:

   `site-public-clean/lingua-boost-lab/<level>/<lesson-slug>/index.html`

2. Add one entry to:

   `site-public-clean/lingua-boost-lab/premium-lessons.json`

3. Run:

   ```powershell
   $env:PREMIUM_PIN='...'
   node "C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\01_Сайт New Generation — сайт, Lab, кабинет\scripts\build-premium-vault.mjs"
   Remove-Item Env:\PREMIUM_PIN
   ```

4. Verify:

   ```powershell
   $env:PREMIUM_PIN='...'
   node "C:\Users\Whitenois\Desktop\Новый центр управления\08_Projects\01_Сайт New Generation — сайт, Lab, кабинет\scripts\build-premium-vault.mjs" --check
   Remove-Item Env:\PREMIUM_PIN
   ```

## What the build script does

- Reads `premium-lessons.json`.
- Checks duplicate ids.
- Checks physical lesson targets.
- Checks premium cards.
- Inserts missing cards into the proper `data-series` section.
- Builds encrypted Vault from manifest.
- Updates `vault-version`.
- Fails `--check` if manifest, HTML cards and Vault drift apart.

## Logout / de-login

`premium.html` now has full access reset:

- button `Сбросить доступ`;
- hash route `premium.html#lock`;
- clears `nge-vault-cache`;
- clears `nge-vault-cache-v`;
- clears `nge-vault-pin`;
- removes real lesson URLs from buttons;
- keeps cards visible: no blur, no hidden titles, no disabled-looking cards.

## Current verified state

`premium check OK: 24 published lessons, 24 cards`

The lesson `travel-talk-2` is included:

`./b1/travel-talk-light-and-bright-2/`
## Cloudflare / Supabase update

The premium gate is now split between Cloudflare Pages Functions and Supabase.

Environment variables required in deployment:

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

Server routes:

- `functions/api/premium-login.js`
- `functions/api/premium-lessons.js`
- `functions/api/premium-logout.js`
- `functions/_middleware.js`

Supabase tables:

- `premium_gate_state`
- `premium_sessions`

Browser behavior:

- no PIN persistence in browser storage;
- `premium.html` uses `/api/premium-lessons` first;
- local Vault fallback remains only for non-server environments;
- `#lock` and the reset button revoke the server session and clear local access.
