# EmDash Integration Plan

EmDash is the intended CMS/editing layer for the Astro version of `sentinelitad.com`.

Source checked: `emdash` npm package and upstream README. EmDash is an Astro integration that provides CMS/admin/API capabilities and stores content as structured data rather than hand-edited HTML strings.

## Current integration state

Files added:

- `package.json` with `astro` and `emdash` dependencies.
- `astro.config.mjs` with gated EmDash integration.
- `src/content.config.ts` defining editable `pages` content shape.
- `src/content/pages/*.json` seed content for Home, MSP feeder bin, and How Pickup Works pages.
- Astro components include `data-emdash-block` and `data-emdash-field` markers for block/field intent.

The integration is **gated** behind `ENABLE_EMDASH=true`:

```bash
ENABLE_EMDASH=true npm run dev
```

Without that variable, Astro can build statically without needing a local CMS database. This keeps ordinary agents from breaking static preview/deploy while the CMS environment is being configured.

## Astro config pattern

`astro.config.mjs` uses:

```js
if (process.env.ENABLE_EMDASH === "true") {
  const { default: emdash } = await import("emdash/astro");
  const { sqlite } = await import("emdash/db");

  integrations.push(
    emdash({
      database: sqlite({
        url: process.env.EMDASH_SQLITE_URL ?? "file:./.emdash/sentinelitad.db",
      }),
    }),
  );
}
```

Cloudflare production should eventually switch to D1/R2/Workers configuration once admin editing is ready. Until then, the static site remains safe and deployable.

## Editable content model

Editable page seed data lives in:

```text
src/content/pages/
  home.json
  msp-feeder-bin.json
  how-pickup-works.json
```

Schema lives in:

```text
src/content.config.ts
```

Current editable fields:

- `title`
- `description`
- `slug`
- `navLabel`
- `hero.eyebrow`
- `hero.title`
- `hero.body`
- `hero.image`
- `hero.imageAlt`
- `hero.ctas[]`
- `warning.strong`
- `warning.body`
- `cards[]`
- `trustItems[]`
- `steps[]`
- `primaryCta`

## Block markers

Components carry markers so future editing tooling and agents know what is safe to edit:

| Component | Marker |
|---|---|
| Hero | `data-emdash-field="hero"` |
| WarningStrip | `data-emdash-field="warning"` |
| CardGrid | `data-emdash-block="card-grid"` |
| TrustPanel | `data-emdash-block="trust-panel"` |
| ProcessTimeline | `data-emdash-block="process-timeline"` |
| SplitSection | `data-emdash-block="split-section"` |
| LeadCapture | `data-emdash-block="lead-capture"` |

## Editing rules for Michael / agents

Safe to edit in EmDash:

- headlines
- paragraph copy
- card titles/body
- CTA labels/URLs
- warning strip copy
- service page ordering once block ordering is surfaced

Do not casually edit in EmDash:

- compliance claims
- insurance wording beyond approved phrasing
- R2v3 / NAID / NIST language
- phone/email/legal-name facts without updating the source docs
- CSS tokens or component layout rules

Those need repo changes and verification.

## Future Cloudflare CMS deployment checklist

Before enabling EmDash in production:

- [ ] Confirm Cloudflare account has Dynamic Workers capability or disable plugin worker loaders per EmDash docs.
- [ ] Create D1 database for Sentinel CMS content.
- [ ] Create R2 bucket for media library if using uploaded assets.
- [ ] Set admin auth policy.
- [ ] Decide whether public form moves to EmDash forms plugin or a dedicated Cloudflare Worker/Turnstile endpoint.
- [ ] Update Cloudflare Pages/Workers deployment from static `public/` deploy to Astro/EmDash server output.
- [ ] Run migration: static HTML pages → Astro routes backed by `src/content/pages/*.json` / EmDash content.
- [ ] Keep `docs/theme/redesign-playbook.md` as the no-drift rule during migration.

## Local commands

Install dependencies:

```bash
npm install
```

Static Astro build, no CMS:

```bash
npm run build
```

Local EmDash-enabled development with SQLite:

```bash
ENABLE_EMDASH=true EMDASH_SQLITE_URL=file:./.emdash/sentinelitad.db npm run dev
```

If EmDash or its API changes, update this file and `astro.config.mjs` in the same commit. Stale CMS docs are how sites become haunted.
