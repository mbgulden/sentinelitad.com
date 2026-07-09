# Sentinel ITAD Website Theme

**Status:** canonical theme guidance for all future Sentinel website work.  
**Applies to:** static pages in `public/` now, Astro components/content in `src/` as the site migrates.

## Prime directive

The site is a **light website**.

Dark backgrounds with light text are allowed only inside scoped modules:

- `.dark` trust panels / proof modules
- `.primary` buttons
- warning/status/CTA strips when intentionally scoped
- small badges, labels, or inline accents

Do **not** make `body`, the global page wrapper, ordinary cards, forms, or standard content sections dark. We are selling trust, not a cyberpunk vape shop.

## Canonical files

| Purpose | File |
|---|---|
| Current deployed CSS | `public/style.css` |
| Astro theme CSS mirror | `src/styles/theme.css` |
| Typed token source | `src/theme/tokens.ts` |
| Theme documentation | `docs/theme/sentinel-theme.md` |
| Astro module guide | `docs/theme/astro-modules.md` |
| EmDash integration guide | `docs/theme/emdash-integration.md` |
| Redesign playbook | `docs/theme/redesign-playbook.md` |

When changing visual style, update **all four**: CSS, tokens, module docs, and redesign notes. Do not patch one page by hand and leave fossils everywhere.

## Brand posture

- Public name: **Sentinel IT Asset Disposal and Logistics**
- Short name: **Sentinel ITAD**
- Voice: local, security-first, sober, competent
- Avoid: junk-hauler language, exaggerated certification claims, giant-enterprise cosplay
- Trust frame: documented intake, media awareness, insured, partner-routed where needed, no magic certificates

## Theme tokens

| Token | Value | Use |
|---|---:|---|
| `--bg` | `#f7f8fb` | Global page background |
| `--surface` | `#ffffff` | Cards, forms, normal modules |
| `--surface-2` | `#f0f4f8` | Alternate light surfaces |
| `--ink` | `#111827` | Headings / strong text |
| `--text` | `#172033` | Body text |
| `--muted` | `#5b6475` | Supporting text |
| `--line` | `#d8e0ea` | Borders |
| `--dark` | `#071018` | Scoped dark sections only |
| `--dark-2` | `#101923` | Scoped dark gradient only |
| `--dark-text` | `#f5f7fb` | Text inside dark sections |
| `--dark-muted` | `#b9c2d2` | Muted text inside dark sections |
| `--teal` | `#087f70` | Main accent, links, check marks |
| `--teal-bright` | `#38f2d0` | Accent inside dark modules |
| `--blue` | `#285fbd` | Secondary accent |
| `--warn` | `#9a6700` | Warning/caution labels |

Typed mirror: `src/theme/tokens.ts`.

## Layout rules

- Max content width: `1180px`.
- Page gutter: `calc(100% - 2rem)` pattern from current CSS.
- Desktop grids:
  - cards: 4 columns
  - proof lists: 2 columns
  - process timelines: 4 columns
  - split sections: 2 columns
- Breakpoints:
  - `880px`: hero/contact/split collapse to one column; cards/timeline/proof become 2 columns
  - `560px`: all grids become 1 column; nav hidden; CTA stacking allowed

## Typography

- Body: `Inter, system-ui, -apple-system, Segoe UI, sans-serif`
- Mono/eyebrows: `Geist Mono, monospace`
- H1: large, tight, trust-forward; do not use paragraph walls in the hero.
- Eyebrow labels: uppercase mono, teal, short.

## Module vocabulary

All new pages should be assembled from these standard modules:

1. `SiteHeader`
2. `Hero`
3. `WarningStrip`
4. `CardGrid`
5. `TrustPanel`
6. `ProcessTimeline`
7. `SplitSection`
8. `LeadCapture`
9. `SiteFooter`

If a new design needs another module, add it once under `src/components/`, document it in `docs/theme/astro-modules.md`, and reuse it. No one-off CSS kingdoms.

## Compliance copy rules

Safe public language:

- “Secure local IT asset disposal and logistics.”
- “Documented intake available for sensitive pickups.”
- “Data-bearing media is handled separately.”
- “Certificates and additional insured documentation are available for approved jobs.”
- “Certified downstream routing is available when required.”

Avoid unless evidence exists:

- “R2v3 certified”
- “NAID AAA certified”
- “Certified data destruction” as a blanket claim
- “NIST 800-88 aligned” unless job/tooling/evidence actually supports it
- “Zero landfill”
- “Fully insured” without exact approved wording/coverage boundaries

## Acceptance checks for agents

Before committing visual work:

- `public/style.css` still contains `color-scheme: light;`.
- `public/style.css` does **not** contain `color-scheme: dark;`.
- `body` remains light; dark backgrounds are scoped to module classes.
- New pages use existing modules/classes instead of new ad hoc layouts.
- Sitemap/nav are updated for new public pages.
- Run an ad-hoc `/tmp/hermes-verify-*` verifier covering the changed behavior.
