# sentinelitad.com

Public website repository for **Sentinel IT Asset Disposal and Logistics** — Growth Web Development LLC's secure IT asset disposal, logistics, recovery, and ITAD lead-generation site for Meridian, Boise, Nampa, Eagle, and the Treasure Valley.

## Purpose

This repo is for the public marketing site only:

- trust-forward landing page
- local SEO for IT asset disposal, secure pickup, and data-bearing media handling
- lead capture form for pickups, bin placement, and decommissioning projects
- public-facing terms/FAQ that do not overclaim certification or tooling that is not yet operational

Operational docs, contacts, valuation scripts, and private lead research remain in the canonical business repo:

- `mbgulden/sentinel-it-asset-logistics`
- local path: `/home/ubuntu/work/sentinel-it-asset-logistics`

## Website planning docs

- `docs/website-brief.md` — positioning, audiences, SEO terms, compliance caveat.
- `docs/content-checklist.md` — collection checklist for identity, proof, lead-gen, and SEO assets.
- `docs/trust-lead-content-inventory.md` — current gathered facts, safe/unsafe copy, audience map, trust-signal gaps, and source map.
- `docs/intake-questions.md` — lead intake questions for pickup/bin/decommissioning requests.
- `docs/deployment-dns.md` — deployment and DNS notes.
- `docs/launch-backlog.md` — public-launch backlog.
- `docs/partners/certified-recycling-partners.md` — possible certified downstream recycling partners to validate.
- `docs/operations/secure-itad-workflow.md` — working secure intake/wipe/destruction/disposition workflow and tooling plan.
- `docs/templates/` — sample printable receipt, asset/media log, certificate/report, and wipe/destruction stickers.

## Theme / Astro / EmDash guidance

Future website work must follow the theme system:

- `docs/theme/sentinel-theme.md` — canonical visual style, tokens, rules, and compliance-safe copy boundaries.
- `docs/theme/astro-modules.md` — standard Astro components and page assembly patterns.
- `docs/theme/emdash-integration.md` — EmDash CMS integration, editable fields, and deployment checklist.
- `docs/theme/redesign-playbook.md` — redesign process so old styles do not linger.
- `src/` — Astro-ready layouts, components, content schema, seed content, and typed theme tokens.

Rule: the global site is light. Dark backgrounds are scoped to modules, CTAs, banners, or selected sections only.

## Current implementation

Static HTML/CSS in `public/`:

```text
public/index.html
public/thanks.html
public/terms.html
public/style.css
public/assets/sentinel_hero.jpg
```

## Deployment target

Primary deployment target: Cloudflare Pages pointed at `public/`. GitHub Pages remains a working preview/fallback until Cloudflare DNS is live.

Domain target: `sentinelitad.com`.

## Compliance wording rule

Do **not** claim Sentinel is R2v3, NAID, fully insured, or certified for data destruction until the supporting process and evidence exists.

Current safe positioning:

> Secure local IT asset disposal and logistics with tracked intake, responsible handling of data-bearing media, value recovery where practical, and certified downstream partner routing when required.

Boring wording. Fewer lawsuits.
