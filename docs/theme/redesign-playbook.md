# Redesign Playbook

Use this when redesigning `sentinelitad.com` so the whole site changes coherently instead of accumulating old styles like barnacles.

## Redesign order

1. **Define the new theme tokens first**
   - Update `src/theme/tokens.ts`.
   - Update `:root` in `src/styles/theme.css`.
   - Mirror to `public/style.css` while static deploy remains active.

2. **Update global modules**
   - `BaseLayout.astro`
   - `SiteHeader.astro`
   - `SiteFooter.astro`
   - shared module CSS

3. **Update standard components**
   - `Hero`
   - `WarningStrip`
   - `CardGrid`
   - `TrustPanel`
   - `ProcessTimeline`
   - `SplitSection`
   - `LeadCapture`

4. **Update content only after structure is stable**
   - Content edits should not carry one-off layout fixes.
   - If copy needs a new shape, add a module.

5. **Regenerate/verify static pages**
   - Until Astro is the deployed source, keep `public/` in sync.
   - Update sitemap/nav when page structure changes.

6. **Run ad-hoc verification**
   - Use `/tmp/hermes-verify-*`.
   - Verify theme invariants, page links, HTML/XML parsing, local HTTP 200, and `git diff --check`.

## Theme invariants to preserve unless Michael explicitly changes them

- The global site is light.
- Dark is scoped to modules, CTAs, banners, or specific sections.
- Sentinel feels security-first and local, not “cheap junk removal.”
- Compliance copy is evidence-tied.
- Trust pages should explain what documentation exists and what it means.
- The site should generate leads without implying capabilities that are not operational.

## Files that must change together

| If changing... | Also update... |
|---|---|
| colors/tokens | `src/theme/tokens.ts`, `src/styles/theme.css`, `public/style.css`, `docs/theme/sentinel-theme.md` |
| component markup | `docs/theme/astro-modules.md`, relevant static HTML until migration complete |
| editable content shape | `src/content.config.ts`, `src/content/pages/*.json`, `docs/theme/emdash-integration.md` |
| navigation | `SiteHeader.astro`, static `public/*.html` headers, sitemap |
| footer/legal/contact | `SiteFooter.astro`, static footers, privacy/terms, source docs |
| deployment model | `astro.config.mjs`, `docs/deployment-dns.md`, Cloudflare Pages config |

## Deprecated patterns

Do not add:

- page-specific `<style>` blobs
- new arbitrary hex colors outside tokens
- dark `body` or dark default page wrapper
- untracked one-off buttons/cards
- HTML-only pages with no Astro module equivalent
- compliance claims not backed by source docs

## Verification template

Every redesign commit should have verifier coverage for:

- token presence
- light global theme / scoped dark modules
- no stale hardcoded legacy colors if a palette changed
- all public pages parse as HTML
- sitemap parses and includes public landing pages
- local static server returns HTTP 200 for changed pages
- `git diff --check`
- clean working tree after commit

## Migration endpoint

The end state should be:

```text
EmDash / Astro content + components → Astro build/server output → Cloudflare
```

Not:

```text
Some Astro, some hand-edited static pages, some forgotten CSS, and a prayer.
```
