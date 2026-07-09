# Astro Modules for Sentinel ITAD

This repo currently deploys static HTML from `public/`, but the canonical future structure is Astro under `src/`. New agents should build new page patterns in Astro first, then mirror into static output until the deployment is switched to `astro build` output.

## Directory structure

```text
src/
  components/
    SiteHeader.astro
    SiteFooter.astro
    Hero.astro
    WarningStrip.astro
    CardGrid.astro
    TrustPanel.astro
    ProcessTimeline.astro
    SplitSection.astro
    LeadCapture.astro
  content/
    pages/
      home.json
      msp-feeder-bin.json
      how-pickup-works.json
  content.config.ts
  layouts/
    BaseLayout.astro
  styles/
    theme.css
  theme/
    tokens.ts
```

## Component contracts

### `BaseLayout.astro`

Use for every page.

Props:

| Prop | Type | Required | Notes |
|---|---|---:|---|
| `title` | string | yes | Browser/SEO title |
| `description` | string | yes | Meta description |
| `canonical` | string | no | Defaults to current path under `https://sentinelitad.com` |

Includes global theme CSS, `SiteHeader`, main slot, and `SiteFooter`.

### `SiteHeader.astro`

Canonical navigation:

- Services
- MSP bins
- Pickup process
- Contact

Do not clone nav per page. Update this component if nav changes.

### `Hero.astro`

Use once at top of landing/service pages.

Props:

```ts
{
  eyebrow: string;
  title: string;
  body: string;
  image?: string;
  imageAlt?: string;
  ctas?: { label: string; href: string; variant?: "primary" | "secondary" }[];
  bullets?: string[];
  caption?: string;
}
```

Rules:

- Keep hero background light.
- Use one clear conversion CTA.
- Do not put unsupported certification claims in hero copy.

### `WarningStrip.astro`

Use for compliance boundaries or important trust framing.

Props:

```ts
{ strong: string; body: string }
```

This is a light amber strip by default. Do not turn it into a dark global banner.

### `CardGrid.astro`

Use for services, audience pain points, benefits, material classes.

Props:

```ts
{
  eyebrow: string;
  title: string;
  body?: string;
  cards: { title: string; body: string; href?: string }[];
  id?: string;
}
```

Default: 4-up desktop, 2-up tablet, 1-up mobile.

### `TrustPanel.astro`

The allowed dark section. Use for proof/trust/compliance posture.

Props:

```ts
{
  eyebrow: string;
  title: string;
  items: { title: string; body: string }[];
  id?: string;
}
```

Rules:

- This is where dark background is appropriate.
- Keep all text high-contrast with `--dark-text` / `--dark-muted`.
- Use numbered proof items.

### `ProcessTimeline.astro`

Use for sequence/process pages.

Props:

```ts
{
  eyebrow: string;
  title: string;
  steps: { title: string; body: string }[];
  id?: string;
}
```

Default: 4 steps. If more than 4, split into two timelines or a card grid.

### `SplitSection.astro`

Use for “good fits / not a fit”, “media handling / compliance boundary”, or side-by-side comparison.

Props:

```ts
{
  left: { eyebrow: string; title: string; body?: string; items?: string[]; tone?: "good" | "caution" };
  right: { eyebrow: string; title: string; body?: string; items?: string[]; tone?: "good" | "caution" };
}
```

Use `tone: "caution"` for red × list markers.

### `LeadCapture.astro`

Use at the bottom of conversion pages.

Props:

```ts
{
  eyebrow: string;
  title: string;
  body: string;
  ctas?: { label: string; href: string; variant?: "primary" | "secondary" }[];
  form?: boolean;
}
```

`form: true` renders the temporary FormSubmit form. Prefer a Cloudflare Worker/Turnstile form later.

## Page assembly pattern

Recommended page order:

```astro
<BaseLayout title={page.title} description={page.description}>
  <Hero {...page.hero} />
  {page.warning && <WarningStrip {...page.warning} />}
  <CardGrid id="services" ... />
  <TrustPanel id="proof" ... />
  <ProcessTimeline id="process" ... />
  <SplitSection ... />
  <LeadCapture ... />
</BaseLayout>
```

## Anti-drift rule

If you need a visual pattern not covered here:

1. Add a named component under `src/components/`.
2. Add CSS using existing tokens in `src/styles/theme.css` and `public/style.css` if still serving static output.
3. Document the module here.
4. Add verifier checks for the new module.

No copy-pasted inline style blobs. We are trying to prevent the usual archaeological dig six months from now.
