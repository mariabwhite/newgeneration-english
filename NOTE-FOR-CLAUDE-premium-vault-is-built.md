# Note for Claude: Premium Vault is now manifest-driven

Premium Vault architecture has already been rebuilt.

Do not return to manual edits where lesson folder, premium card and encrypted Vault are maintained separately.

## Current rule

New premium lesson flow:

1. Add lesson files under:

   `site-public-clean/lingua-boost-lab/<level>/<lesson-slug>/index.html`

2. Add one entry to:

   `site-public-clean/lingua-boost-lab/premium-lessons.json`

   Use `series` for the course/content family and `section` for the actual `premium.html` `data-series` bucket. If they are the same, `section` may be omitted.

3. Run:

   ```powershell
   $env:PREMIUM_PIN='...'
   node scripts/build-premium-vault.mjs
   Remove-Item Env:\PREMIUM_PIN
   ```

4. Verify:

   ```powershell
   $env:PREMIUM_PIN='...'
   node scripts/build-premium-vault.mjs --check
   Remove-Item Env:\PREMIUM_PIN
   ```

5. Audit lesson links:

   ```powershell
   node scripts/audit-premium-links.mjs
   node scripts/audit-premium-links.mjs --live
   ```

## What the build script does

- Reads `premium-lessons.json`.
- Checks duplicate ids.
- Checks physical lesson targets.
- Checks premium cards.
- Checks that each card is in the expected `data-series` section.
- Inserts missing cards into the proper `data-series` section.
- Builds encrypted Vault from manifest.
- Updates `vault-version`.
- Fails `--check` if manifest, HTML cards and Vault drift apart.

## Link audit

`scripts/audit-premium-links.mjs` checks that every published premium lesson URL maps to a local file. With `--live`, it also checks the live `https://newgeneration-english.ru` URL.

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

`premium link audit OK: 24 lessons, 0 warnings, live checked`

The lesson `travel-talk-2` is included:

`./b1/travel-talk-light-and-bright-2/`
