# Sentinel Console — Build Spec and Data Schemas

**Task:** t_2dcba0d8 (spec) → feeds t_5c9b413d (ned, build + launch).
**Owner of this doc:** George. **Audience:** ned, building v1 from this alone.
**Read with:** the infra preflight report (t_a2425db5) for hosting, hostname, tunnel, and Access.
**Rule of the house:** agents update JSON, never HTML. The page is a thin viewer over `data/*.json`.

This spec fixes every design decision so the build has no forks. Where this doc and the preflight
conflict, stop and comment on the build task instead of improvising.

---

## 0. What the console is

A single phone-first page, served from this box over the Cloudflare Tunnel and gated by Cloudflare
Access (Michael only). It shows today's day, the week, a route, the asset library, current pricing,
the tool links, and a visit log. Everything is data-driven: the HTML and JS are fixed, the content
lives in five JSON files that agents rewrite on a schedule.

The console is a working surface for the operator, not a public marketing site. It links to the
asset library at `/home/ubuntu/work/sentinel-assets/` so a phone never depends on Dropbox.

---

## 1. Data schemas (the heart of it)

Five files under the site's `data/` directory. Each example below is the **real first seed** for
this week (Oct 20-23, 2026), pulled from `week.json`, `ASSETS.md`, and the standing pricing
decisions. Every block is valid JSON and parses as-is. The seed *text* is illustrative of shape and
content; the derived files ship verbatim from `week.json` (e.g. the real `today.json` carries the
week plan's exact block titles).

### 1.1 `data/today.json` — the day

Shape: `date`, `generated`, `timezone`, and `blocks[]`. A block is one scheduled unit of the day.

| Field | Type | Meaning |
|---|---|---|
| `date` | string | `YYYY-MM-DD`, the day this file describes |
| `generated` | string | ISO 8601 timestamp the nightly roll wrote this file |
| `timezone` | string | IANA zone, `America/Boise` |
| `blocks[].start` | string | `HH:MM` 24-hour, local |
| `blocks[].end` | string | `HH:MM` 24-hour, local |
| `blocks[].title` | string | One short line, what the block is |
| `blocks[].detail` | string | The working detail: names, numbers, next steps |
| `blocks[].action.type` | enum | `call` / `maps` / `link` / `none` |
| `blocks[].action.label` | string | Button text (empty when `type` is `none`) |
| `blocks[].action.target` | string | Digits for `call`, a map or URL for `maps`/`link`, empty for `none` |
| `blocks[].status` | enum | `upcoming` / `current` / `done` |

`action.target` conventions:
- `call` → bare digits or `tel:2082863000` (the renderer builds the `tel:` link).
- `maps` → a Google Maps directions URL (`https://www.google.com/maps/dir/?api=1&destination=…`).
- `link` → a full `https://` URL.

Seed (first seeded day, 2026-10-20):

```json
{
  "date": "2026-10-20",
  "generated": "2026-10-19T21:00:00-07:00",
  "timezone": "America/Boise",
  "blocks": [
    {
      "start": "09:30",
      "end": "11:00",
      "title": "MSP call block",
      "detail": "Call order, tap to dial. 1. CompuNet (Nolan Schoo / Tom McFarlin) 208-286-3000, Meridian. 2. MicroTech (Randy Amorebieta) 208-345-0054, Boise. 3. CMIT (Scott Freund) 208-608-5500, Meridian. 4. Fisher's (Darren Reynolds) 208-947-3600, Boise. 5. Bytagig (John Jackson) 833-465-5913, Boise. 6. Treasure Valley IT (Michael A. Lukes) 208-367-1000, Boise. Pitch: a standing local home for retired gear, a locked feeder bin picked up on a schedule.",
      "action": {
        "type": "call",
        "label": "Tap to call CompuNet",
        "target": "208-286-3000"
      },
      "status": "upcoming"
    },
    {
      "start": "11:00",
      "end": "12:30",
      "title": "eBay hardware photography",
      "detail": "Photo queue for the first Sentinel eBay listing wave. White background, bright light, all four sides plus the model and serial plate. Shoot every unit on the sell pile; the listing packet draft lands today for review.",
      "action": {
        "type": "none",
        "label": "",
        "target": ""
      },
      "status": "upcoming"
    },
    {
      "start": "13:00",
      "end": "14:30",
      "title": "Listing review with Jimmy + Gusto check",
      "detail": "1. Review the eBay listing packet with Jimmy (this morning's photos go in). 2. Gusto payroll, run by 4:00 PM Pacific, pay period Oct 2-15.",
      "action": {
        "type": "link",
        "label": "Open Gusto payroll",
        "target": "https://app.gusto.com/pay/payrolls/new"
      },
      "status": "upcoming"
    }
  ]
}
```

### 1.2 `data/week.json` — the week

Shape: `week_of`, `timezone`, and `days` (a map of `YYYY-MM-DD` to a block array). The block shape
is identical to `today.json` blocks. This is the **source** the nightly roll reads to derive
`today.json`.

| Field | Type | Meaning |
|---|---|---|
| `week_of` | string | `YYYY-MM-DD`, the week's first day |
| `timezone` | string | IANA zone, `America/Boise` |
| `days` | object | Key = date (`YYYY-MM-DD`), value = array of blocks (same shape as 1.1) |

Seed note: the week plan runs Tue-Fri, so this week has four date keys. The renderer treats a
missing day as "rest day" and shows a short one-liner instead of a blank list.

Seed (full work week):

```json
{
  "week_of": "2026-10-20",
  "timezone": "America/Boise",
  "days": {
    "2026-10-20": [
      {
        "start": "09:30",
        "end": "11:00",
        "title": "MSP call block",
        "detail": "Six MSP calls, tap to dial. CompuNet 208-286-3000, MicroTech 208-345-0054, CMIT 208-608-5500, Fisher's 208-947-3600, Bytagig 833-465-5913, Treasure Valley IT 208-367-1000. Pitch the feeder bin and a standing local disposition channel.",
        "action": {
          "type": "call",
          "label": "Tap to call first stop",
          "target": "208-286-3000"
        },
        "status": "upcoming"
      },
      {
        "start": "11:00",
        "end": "12:30",
        "title": "eBay hardware photography",
        "detail": "Shoot the first listing wave; white background, all four sides plus the model and serial plate.",
        "action": {
          "type": "none",
          "label": "",
          "target": ""
        },
        "status": "upcoming"
      },
      {
        "start": "13:00",
        "end": "14:30",
        "title": "Listing review + Gusto check",
        "detail": "Review the packet with Jimmy; run Gusto payroll by 4:00 PM Pacific.",
        "action": {
          "type": "link",
          "label": "Open Gusto payroll",
          "target": "https://app.gusto.com/pay/payrolls/new"
        },
        "status": "upcoming"
      }
    ],
    "2026-10-21": [
      {
        "start": "09:30",
        "end": "11:00",
        "title": "MSP shop visits (route)",
        "detail": "Drive route, four stops. 1. CompuNet, 1111 S Silverstone Way Ste 200, Meridian. 2. CMIT, 289 SW 5th Ave, Meridian. 3. MicroTech, 125 E 50th St, Garden City. 4. Fisher's, 575 E 42nd St, Garden City. Bring business cards and the one-pager; ask who handles retired equipment and pitch the feeder bin.",
        "action": {
          "type": "maps",
          "label": "Open the route in Maps",
          "target": "https://www.google.com/maps/dir/?api=1&destination=1111+S+Silverstone+Way+Ste+200+Meridian+ID"
        },
        "status": "upcoming"
      },
      {
        "start": "11:00",
        "end": "12:30",
        "title": "Visit follow-ups",
        "detail": "Log every visit while it is fresh: who, what they said, the next step. Send thank-you emails and update the contact tracker.",
        "action": {
          "type": "none",
          "label": "",
          "target": ""
        },
        "status": "upcoming"
      },
      {
        "start": "13:00",
        "end": "14:30",
        "title": "Listing drafts",
        "detail": "Draft the eBay listings from Tuesday's photos; send them to Jimmy for review.",
        "action": {
          "type": "none",
          "label": "",
          "target": ""
        },
        "status": "upcoming"
      }
    ],
    "2026-10-22": [
      {
        "start": "09:30",
        "end": "11:00",
        "title": "Pickup run",
        "detail": "Primary pickup: HP 2920-48G-POE+ 48-port managed switch, $50, Kuna. Listing: facebook.com/marketplace/item/4698153720407952. Bring cargo space, $50 cash, and a dolly.",
        "action": {
          "type": "link",
          "label": "Open the listing",
          "target": "https://www.facebook.com/marketplace/item/4698153720407952"
        },
        "status": "upcoming"
      },
      {
        "start": "11:00",
        "end": "12:30",
        "title": "Hardware intake + testing",
        "detail": "Photograph condition, run the power-on test, log serials, and decide sell, recycle, or parts. Update the inventory tracker.",
        "action": {
          "type": "none",
          "label": "",
          "target": ""
        },
        "status": "upcoming"
      },
      {
        "start": "13:00",
        "end": "14:30",
        "title": "Listing drafts",
        "detail": "Draft more listings from the intake pile. Goal: everything photographed this week has a draft by end of day.",
        "action": {
          "type": "none",
          "label": "",
          "target": ""
        },
        "status": "upcoming"
      }
    ],
    "2026-10-23": [
      {
        "start": "09:30",
        "end": "11:00",
        "title": "Backlog session with Jimmy",
        "detail": "Review the week's results (calls, visits, pickups, live listings), build next week's task queue, and decide on the polo and iron-on logo, the pickup route system, and feeder-bin placements.",
        "action": {
          "type": "none",
          "label": "",
          "target": ""
        },
        "status": "upcoming"
      },
      {
        "start": "11:00",
        "end": "12:30",
        "title": "Overflow / catch-up",
        "detail": "Catch-up buffer for anything that slipped. If everything is done, use it for the polo and logo order.",
        "action": {
          "type": "none",
          "label": "",
          "target": ""
        },
        "status": "upcoming"
      },
      {
        "start": "16:00",
        "end": "17:00",
        "title": "Rodney Reeve RAM pickup",
        "detail": "Rodney Reeve picks up the $50 16GB ECC stick, confirmed Friday 4-5 PM. He asked about more 16GB sticks at $50 each; set a quantity before he arrives.",
        "action": {
          "type": "none",
          "label": "",
          "target": ""
        },
        "status": "upcoming"
      }
    ]
  }
}
```

### 1.3 `data/links.json` — tool groups

Shape: `groups[]` with `name` and `items[]` of `{ label, url, note }`.

| Field | Type | Meaning |
|---|---|---|
| `groups[].name` | string | Group heading (Money and Payroll, Selling, …) |
| `groups[].items[].label` | string | The link text |
| `groups[].items[].url` | string | Full `https://` URL or `tel:` link |
| `groups[].items[].note` | string | One line of context |

Seed — grounded URLs from the week plan and the live site. The four account-specific deep links
that do not exist anywhere on this box (FareHarbor seller dashboard, eBay My eBay, the kanban board
URL, the Dropbox folder share link) use a **`[SEED]`** marker: they point at the verified platform
homepage today and are swapped for the signed-in URL the first time it is confirmed. ned renders
them as-is; the marker rides in the note so the swap is a one-line data edit, not a code change.

```json
{
  "groups": [
    {
      "name": "Money and Payroll",
      "items": [
        {
          "label": "Gusto payroll",
          "url": "https://app.gusto.com/pay/payrolls/new",
          "note": "Run by 4:00 PM Pacific each payday; the week plan points at this deep link."
        }
      ]
    },
    {
      "name": "Selling",
      "items": [
        {
          "label": "eBay (sell hub)",
          "url": "https://www.ebay.com/",
          "note": "Open the seller tools from the signed-in account. [SEED] swap for the signed-in My eBay / Sell link once confirmed."
        },
        {
          "label": "Facebook Marketplace (Kuna switch listing)",
          "url": "https://www.facebook.com/marketplace/item/4698153720407952",
          "note": "Live listing from the week plan; used price $120-200."
        },
        {
          "label": "Facebook Marketplace (home)",
          "url": "https://www.facebook.com/marketplace/",
          "note": "Local buy and sell, Treasure Valley area."
        }
      ]
    },
    {
      "name": "Booking and Ops",
      "items": [
        {
          "label": "FareHarbor",
          "url": "https://www.fareharbor.com/",
          "note": "Booking platform home. [SEED] swap for the signed-in seller dashboard URL once confirmed."
        },
        {
          "label": "Kanban board",
          "url": "https://app.growthwebdev.com/kanban",
          "note": "Shared agent task board. [SEED] confirm the exact board URL with Jimmy."
        },
        {
          "label": "Dropbox folder",
          "url": "https://www.dropbox.com/",
          "note": "The _Sentinel ITAD folder. [SEED] swap for the folder share link once confirmed."
        }
      ]
    },
    {
      "name": "Company",
      "items": [
        {
          "label": "sentinelitad.com",
          "url": "https://sentinelitad.com/",
          "note": "Public site: services, MSP bins, pickup process, FAQ."
        },
        {
          "label": "Call or text",
          "url": "tel:8084981125",
          "note": "808-498-1125, the outbound line."
        }
      ]
    }
  ]
}
```

### 1.4 `data/assets.json` — the asset library index

Shape: `items[]` of `{ label, file, kind, view, note }`. `file` is a path **under**
`/home/ubuntu/work/sentinel-assets/`; the console serves it from there so a phone link is
self-contained.

| Field | Type | Meaning |
|---|---|---|
| `items[].label` | string | Human label |
| `items[].file` | string | Path under `sentinel-assets/` |
| `items[].kind` | enum | `pdf` / `html` / `xlsx` / `md` |
| `items[].view` | enum | `print` / `phone` (how to surface it) |
| `items[].note` | string | When to use it |

Seed — 11 high-value, phone/field-relevant files from `ASSETS.md` (not the full 212-file tree; the
console surfaces the ones the operator taps daily, and the rest stay reachable in the asset library):

```json
{
  "items": [
    {
      "label": "One-pager (leave-behind)",
      "file": "sales-kit/one-pager.md",
      "kind": "md",
      "view": "phone",
      "note": "Field visits and walk-ins."
    },
    {
      "label": "Service menu and pricing",
      "file": "sales-kit/service-menu.md",
      "kind": "md",
      "view": "phone",
      "note": "Source for the pricing section; draft, prices pending sign-off."
    },
    {
      "label": "Dual-pitch sheet",
      "file": "sales-kit/dual-pitch-sheet.pdf",
      "kind": "pdf",
      "view": "print",
      "note": "Calls and email attachments."
    },
    {
      "label": "Pickup receipt template",
      "file": "sales-kit/sentinel-pickup-receipt.html",
      "kind": "html",
      "view": "phone",
      "note": "Completed pickups, signed on site."
    },
    {
      "label": "Chain-of-custody record",
      "file": "sales-kit/sentinel-chain-of-custody.html",
      "kind": "html",
      "view": "phone",
      "note": "Every job, filed with the CDD."
    },
    {
      "label": "Sanitization certificate",
      "file": "sales-kit/sentinel-sanitization-certificate.html",
      "kind": "html",
      "view": "phone",
      "note": "Proof of wipe, one row per drive serial."
    },
    {
      "label": "Certificate of data destruction",
      "file": "certificate-of-data-destruction.html",
      "kind": "html",
      "view": "print",
      "note": "Final deliverable per job, CDD-2026-NNNN."
    },
    {
      "label": "QR labels (jobs 0001-0100)",
      "file": "sales-kit/sentinel-qr-labels-SIT-2026-0001-0100.pdf",
      "kind": "pdf",
      "view": "print",
      "note": "Print for field visits."
    },
    {
      "label": "Asset labels (IDs 000001-000050)",
      "file": "sales-kit/sentinel-asset-labels-SIT-A-000001-000050.pdf",
      "kind": "pdf",
      "view": "print",
      "note": "Asset tagging, print and apply."
    },
    {
      "label": "Profit calculator",
      "file": "profit-calculator.xlsx",
      "kind": "xlsx",
      "view": "phone",
      "note": "Quotes, buyback, and margin analysis."
    },
    {
      "label": "FAQ (15 answers)",
      "file": "faq.md",
      "kind": "md",
      "view": "phone",
      "note": "Console and website content."
    }
  ]
}
```

All 11 referenced files exist on disk (verified). `view: phone` renders inline; `view: print` opens
a print/share sheet.

### 1.5 `data/pricing.json` — the pricing card

Content is sourced from the **standing pricing decisions** (pickup terms as Michael set them,
recorded in the service-v2 doc, batch 17). These are real, current numbers — the unconfirmed draft
tiers in `sales-kit/service-menu.md` stay out of the console until signed off. Schema:

| Field | Type | Meaning |
|---|---|---|
| `as_of` | string | `YYYY-MM-DD`, the date the numbers were last confirmed |
| `currency` | string | `USD` |
| `service_area.primary` | string | Core free-pickup geography |
| `service_area.beyond` | string | What applies outside it |
| `service_area.hawaii` | string | Hawaii handling |
| `pickup_fees[]` | array | entries: tier, condition, fee, note |
| `trip_fee` | object | amount, applies, note |
| `crt_rule` | object | amount, unit, condition, note |
| `battery_rule` | object | ups_and_lead_acid, loose_lithium |
| `insured` | string | The insurance line |

Seed — actual content:

```json
{
  "as_of": "2026-10-20",
  "currency": "USD",
  "service_area": {
    "primary": "Treasure Valley (Meridian, Boise, Nampa, Eagle) and Ada + Canyon counties",
    "beyond": "Case by case; a trip fee applies outside Ada and Canyon counties",
    "hawaii": "Pickup coordination for established contacts"
  },
  "pickup_fees": [
    {
      "tier": "Free pickup",
      "condition": "10 or more computers or laptops, or any server or networking load",
      "fee": 0,
      "note": "The door-opener; signed pickup receipt on every job."
    },
    {
      "tier": "Small load",
      "condition": "Fewer than 10 computers or laptops",
      "fee": 75,
      "note": "Flat fee, waived when the gear has buyback value."
    }
  ],
  "trip_fee": {
    "amount": 50,
    "applies": "Outside Ada and Canyon counties",
    "note": "Case by case; waived when the load qualifies for a free pickup."
  },
  "crt_rule": {
    "amount": 25,
    "unit": "each",
    "condition": "CRT monitors or televisions, with a qualifying load",
    "note": "Priced at pickup, receipt given. Swollen or leaking units route to a hazardous path."
  },
  "battery_rule": {
    "ups_and_lead_acid": "UPS and lead-acid batteries accepted with loads at the standard pickup fee",
    "loose_lithium": "Loose lithium batteries declined"
  },
  "insured": "General liability coverage in place; a pickup receipt and documented custody on every job."
}
```

Source of these numbers: "free pickup for 10+ computers/laptops or any server/networking load; $75
flat for smaller loads (waived when gear has buyback value); Ada + Canyon counties free with a
qualifying load; beyond that, $50 trip fee or case-by-case; CRTs $25 each with a qualifying load;
UPS/lead-acid batteries welcome with loads; loose lithium declined." The draft tiers in
`service-menu.md` (~$150/hr, $12/drive, $79/$129/$199/mo) are marked DRAFT and stay out until
Michael signs them off.

---

## 2. Page structure and mobile-first rules

One `index.html`, a small amount of vanilla JS, one small CSS file. No external frameworks, no
build step, no CDN. Sections in this order (single column, scroll):

1. **Today** — `today.json` blocks as a timeline. The block whose window contains "now" gets
   `status: current` styling (filled marker); `done` is struck and dimmed. A `call` action renders
   a large tap-to-dial button.
2. **Calls** — a compact dial section: every `call` action in `today.json` (and the week) as a
   one-tap number, grouped by name.
3. **Route** — the day's `maps` actions as a vertical list of stops with a one-tap "open in Maps"
   button per stop, plus a "whole route" directions link.
4. **Assets** — `assets.json` as a list; tap opens inline (phone) or the print/share sheet (print).
5. **Pricing** — `pricing.json` rendered as a clean card: service area, pickup fees, trip fee, CRT,
   batteries, insurance. This is the operator's quick reference on a call.
6. **Tools** — `links.json` groups as a grouped list of one-tap links.
7. **Log a visit** — the visit-log form (section 4). In v1 it renders with a "setup pending" state
   because the backend arrives in task G; the form is present and the fields are final, but a
   submit before G lands shows a clear "wired up in task G" notice. It records nothing silently.

### Mobile-first rules (hard)

- **Single column.** The page is a stack; the console is built for a phone in one hand.
- **Tap targets 48px or larger.** Every button and list row is at least 48px tall; call buttons
  are larger.
- **No external frameworks.** No React, no Bootstrap, no Google Fonts, no icon font. Inline SVG
  only, hand-rolled.
- **Total weight under 300 KB.** The whole page (HTML + CSS + JS + the five JSON seeds) under
  300 KB so it loads on a throttled LTE connection. The JSON seeds above total roughly 13 KB; the
  budget is almost all left for markup and styles.
- **Works on LTE.** No lazy-loaded hero, no blocking third-party calls. First paint is local.
- **Data, not code, is the moving part.** The page reads the five JSON files; a content change is a
  JSON edit, never an HTML edit.

---

## 3. The nightly update contract

Who writes what, when, and what degrades gracefully.

**The roll (21:00 America/Boise — the file zone IS Mountain Time, so 21:00 MT and 21:00
America/Boise are the same moment; the cron keys off the America/Boise zone, DST-safe, a fixed
offset stays wrong across DST):**
A nightly job (cron, agent-run) does three things, in order:

1. **Mark the day done.** In `week.json`, set every block whose `end` is at or before "now" for
   today to `status: done`, and the block containing "now" (if any) to `current`. This is the only
   write the roll makes to `week.json`.
2. **Derive tomorrow's today.json.** Read `week.json` for tomorrow's date, copy its blocks
   verbatim, set each to `upcoming`, and write `today.json` with `date = tomorrow`,
   `generated = <now>`, and `timezone` carried through. If `week.json` has no key for tomorrow
   (a rest day, e.g. a Saturday), write a `today.json` with an empty `blocks` array and a one-line
   note — the renderer shows "Rest day. Nothing scheduled."
3. **Keep the last good file.** Before overwriting `today.json`, the job copies the current file to
   `data/last-good/today.json`. This is the rollback source.

**"Done" marking means:** a block is `done` when its `end` time has passed. It is a visual state
(strike + dim), not a deletion. The operator can still read what happened; nothing is removed from
the week until Jimmy seeds the next one.

**The stale-data failure mode (required, tested):**
The console day rolls at 21:00 MT: the page computes "today" with a 21:00 rollover, so after a good
roll `today.json`'s date (set to tomorrow) always matches. If the nightly roll fails, or
`week.json` is missing a day it should have, the page must degrade to the last good state and say
so. Concretely:
- The renderer always fetches `data/last-good/today.json` first. If `data/today.json` is missing,
  malformed JSON, or has a `date` that does not match the console day, the page renders
  **`last-good/today.json`** in full.
- A **visible stale banner** sits at the top of the page whenever the served `today.json` `date` or
  `generated` is older than 26 hours, or whenever it was served from `last-good`. The banner reads,
  in positive voice, what the data is and when it was last written — for example, "Showing
  Tuesday's plan, last updated Monday 9:00 PM Mountain. The nightly refresh has not landed yet."
- **A blank page is a build failure.** The renderer has a fallback path that always produces
  output; an empty `today.json` renders "Rest day. Nothing scheduled." rather than a white screen.

**Ownership:** Jimmy seeds `week.json` each week from the week plan. The nightly job derives
`today.json`. ned (the build owner) runs the page. Michael approves week content. During the week
nobody edits `today.json` by hand except the nightly roll; hand edits get overwritten at 21:00.

---

## 4. Visit-log form (feeds task G)

The "Log a visit" section captures a field visit while it is fresh. v1 renders the form with the
final fields and a "setup pending" state (wired in task G). When G lands, a submit appends a record
to `data/visits.json` (created then) and, where useful, back-fills the matching `week.json` block.

Fields:

| Field | Type | Required | Notes |
|---|---|---|---|
| `who` | string | yes | Person talked to |
| `company` | string | yes | The organization |
| `outcome` | enum | yes | `interested` / `follow-up` / `not-interested` / `picked-up` / `other` |
| `note` | string | no | What they said, next step |
| `follow_up_date` | string | no | `YYYY-MM-DD`, when to check back |

A record:

```json
{
  "logged_at": "2026-10-21T14:20:00-07:00",
  "who": "Scott Freund",
  "company": "CMIT Solutions",
  "outcome": "follow-up",
  "note": "Runs about 40 retired Dell OptiPlexes a year. Wants the feeder bin in the server room. Send the one-pager.",
  "follow_up_date": "2026-10-24"
}
```

The `outcome` picklist is fixed at those five values. `other` takes a free-text note so nothing is
forced into the wrong bucket.

---

## 5. Build handoff (for ned)

- Site directory and serving are defined by the preflight: `/home/ubuntu/work/sentinel-console/`
  with `index.html` + `data/*.json` + `assets/` (a symlink into `sentinel-assets`), served by host
  nginx on port 8490, fronted by tunnel `4a6097ff` to `console.sentinelitad.com`, gated by a
  Cloudflare Access app (Email OTP, Michael only).
- The stale-banner path and the "rest day" path are acceptance items, not polish.
- Where this spec and the preflight disagree, comment on the build task; do not improvise.

---

## 6. Open questions

1. **Four `[SEED]` tool URLs** (FareHarbor seller dashboard, eBay My eBay, kanban board, Dropbox
   folder share link) do not exist on this box. They ship as verified platform homepages with a
   `[SEED]` note. **Needed from Michael/Jimmy:** the four signed-in URLs, so they swap in as
   one-line `data/links.json` edits. This is a data update, not a build decision.
2. **The visit-log backend (task G)** is the only deferred part of the form. Everything else in the
   form is final.
3. **`today.json` timezone:** confirmed by the muse review (t_42178ab5). The week plan and files
   use `America/Boise` (Mountain); the roll keys off the `America/Boise` zone — DST-safe, a fixed
   offset stays wrong across DST — and the stale check uses the 21:00-rollover console day, so the
   date always matches after a good roll.

Nothing in this list blocks the build: items 1 and 2 are data and a follow-up task, and item 3 is
confirmed by the review.
