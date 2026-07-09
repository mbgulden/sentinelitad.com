# Sentinel ITAD Trust + Lead Content Inventory

**Purpose:** working inventory for turning `sentinelitad.com` into a stronger trust signal and lead generator without exposing private operational material or making unsupported compliance claims.

**Last source pass:** 2026-07-09  
**Public website repo:** `mbgulden/sentinelitad.com`  
**Private/canonical operations repo:** `mbgulden/sentinel-it-asset-logistics`

## Current known public facts

| Area | Known fact | Website use |
|---|---|---|
| Legal/business owner | Growth Web Development LLC DBA Sentinel IT Asset Disposal | Footer, privacy/terms, structured data |
| Brand shorthand | Sentinel ITAD | Header, SEO title, local landing copy |
| Base | Meridian, Idaho; service focus Treasure Valley: Meridian, Boise, Nampa, Eagle | Local SEO, hero, schema `areaServed` |
| Current public phone | 808-498-1125 | CTA/call button until a local Idaho number exists |
| Current email | Michael@growthwebdev.com | Form destination and contact fallback until Sentinel-domain email exists |
| Domain | sentinelitad.com | `CNAME`, sitemap, canonical URLs |
| Core positioning | Security-first local IT asset recovery between expensive national ITAD providers and low-trust junk haulers | Hero, proof section, sales language |
| Brand voice | Small, exclusive, sober, compliance-aware; "Blue Collar Cyber" as internal positioning | Copy direction, not necessarily public tagline yet |
| Capacity | Minivan + Tesla Model Y with 4x6 trailer; roughly 1 rack / 1,500 lb practical tow; garage-scale intake/storage | Internal scoping guidance; avoid overpromising bulk capacity |
| Current resale route | Facebook Marketplace/direct; wants eBay/homelab channels | Future value-recovery page, not a launch blocker |
| Wiping hardware | Hot-swap servers exist | Internal trust roadmap only |
| Wiping/process gap | Wipe tooling, certificate automation, standardized serial logs, and insurance/compliance posture are not complete | Do **not** claim certified data destruction yet |

## Public offer pillars to build around now

1. **Local IT asset pickup** — retired servers, workstations, networking gear, storage arrays, monitors, components, and related office technology.
2. **MSP feeder-bin / recurring pickup** — recurring clutter relief for MSPs with a controlled collection point and scheduled pickups.
3. **Data-bearing media awareness** — drives and removable media separated and routed intentionally; use conservative wording until the tooling is operational.
4. **Value recovery before scrap** — recover reusable servers, RAM, CPUs, NICs, SSDs, GPUs, monitors, rails, cables, and parts when practical.
5. **Responsible downstream routing** — use certified downstream partners when required, but only name/claim them after partner evidence and public wording are approved.

## Primary lead audiences

| Priority | Audience | Pain | Website conversion hook | Current caution |
|---|---|---|---|---|
| A | MSPs / IT service companies | Retired client gear filling storage rooms | Free/recurring pickup, feeder bin, simple handoff | Bin terms and liability wording need final review before aggressive campaign |
| A | SMB offices | Old desktops, servers, networking gear sitting around | Local pickup, accountable operator, clean disposition | Avoid promising same-day/bulk jobs beyond current capacity |
| B | Law / medical / financial offices | Data-bearing media liability | Chain-of-custody intake, media separation, documented disposition path | Do not market enterprise-grade destruction until insurance/tooling/certs are real |
| B | Engineering / CAD / VFX / AI shops | High-value workstations/GPUs/servers retire unevenly | Value recovery and security-aware pickup | Needs stronger resale proof/case examples |
| C | Hawaii MSP/data-center contacts | Existing contact data from prior research | Later remote/referral angle | Not first launch market; Treasure Valley first |

## Trust signals to collect next

| Need | Why it matters | Minimum artifact |
|---|---|---|
| Final public brand/name | Consistency across domain, schema, invoices, terms, forms | Chosen display name and DBA wording |
| Sentinel-domain email | Looks less improvised than Growth Web email | `pickup@sentinelitad.com` or `secure@sentinelitad.com` forwarding/live mailbox |
| Logo/favicons/social card | Search/social trust and less stock-site feel | SVG mark, 512px PNG, favicon, OG image |
| Local photos | Proves real local operation | Michael/operator photo, vehicle/trailer, bins, staged intake area, representative enterprise gear |
| Insurance wording | Allows trust without legal overreach | Certificate on file + approved public sentence |
| Intake receipt template | Lets site show accountability | Fake/sample pickup receipt with non-client test data |
| Asset/media log template | Demonstrates process | Sample CSV/PDF with fake serials |
| Downstream partner evidence | Supports responsible recycling claims | Partner certs, accepted materials, public wording permission |
| Wipe/certificate sample | Enables stronger data-destruction page later | Test-drive certificate with serials/fake client and method details |
| Lead routing backend | Prevents lost forms | Form destination, spam control, SLA, autoresponder copy |

## Copy that is safe now

- "Secure local IT asset recovery."
- "Documented intake available for sensitive pickups."
- "Data-bearing media is handled separately and routed according to the agreed disposition path."
- "Reusable equipment is recovered before recycling where practical."
- "Certified downstream routing is available when required."
- "Based in Meridian and serving the Treasure Valley."

## Copy to avoid until proven

- "R2v3 certified" / "NAID AAA certified" unless Sentinel itself holds it.
- "Certified data destruction" until tooling, logs, verification, certificate template, and insurance posture are live.
- "NIST 800-88 aligned" except for specific jobs actually performed under a tested process.
- "Fully insured" until exact insurance coverage and wording are confirmed.
- "Zero landfill" unless downstream partner documentation supports it.
- National-scale claims, guaranteed same-day bulk capacity, or data-center-scale language.

## Source map

| Source | What it contributes | Public-site use |
|---|---|---|
| `/home/ubuntu/work/sentinel-it-asset-logistics/docs/strategy/sentinel-itad-business-plan-summary.md` | Positioning, market thesis, target audiences, service tiers, Blue Collar Cyber concept | Messaging, audience pages, trust roadmap |
| `/home/ubuntu/work/sentinel-it-asset-logistics/docs/compliance/data-sanitization-protocol-summary.md` | Media handling requirements, certificate fields, wipe-tooling gaps | Compliance-safe copy rules, future "drive handling" page requirements |
| `/home/ubuntu/work/sentinel-it-asset-logistics/docs/outreach/msp_outreach_kit.md` | MSP feeder-bin pitch and Treasure Valley MSP targets | MSP landing page, one-page flyer, outreach CTA |
| `/home/ubuntu/work/sentinel-it-asset-logistics/docs/outreach/sial-lead-contact-view.md` | Deduped local contact view and outreach rewrite rule | Sales targets; do not expose private contacts publicly |
| `/home/ubuntu/work/sentinel-it-asset-logistics/docs/partners/downstream_partners_research.md` | R2v3 downstream partner options near Meridian | Internal partner validation; public wording only after approval |
| `/home/ubuntu/work/sentinel-it-asset-logistics/docs/workspace-index.md` | Canonical workspace boundaries | Prevents leaking private ops into public website repo |
| `/home/ubuntu/work/sentinel-it-asset-logistics/okf/research/sentinel-itad-existing-content-map-2026-07-07.md` | Existing content map and anti-duplication rules | Research index; future agents should read before new lead/contact work |

## Immediate website content backlog from this pass

1. Add an MSP feeder-bin landing page with conservative, no-certification-overclaim language.
2. Add a "How pickup works" page with sample intake fields and a fake pickup record.
3. Add a "Data-bearing media" page only after a minimal tested wipe/logging process exists; until then keep it framed as media separation and routing.
4. Produce a one-page PDF/flyer for MSP walk-ins after logo/email are decided.
5. Replace generated hero art with real local photos.
6. Add downstream partner language only after certificates and permission to name/describe partners are confirmed.
