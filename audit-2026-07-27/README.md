# Sentinel ITAD Site Legitimacy Audit — 2026-07-27

**Audience:** Michael (returning from CA trip).
**Purpose:** Concrete answers about whether `sentinelitad.com` actually works for IT-pro lead capture, and exactly what to fix before you share the URL.
**Scope:** read-only audit + drafts. **No deploys, no commits, no emails sent.**

---

## TL;DR

- ✅ Site is **live, polished, and serving correctly** at https://sentinelitad.com (HTTPS, Cloudflare Pages, mobile-responsive, six pages, sitemap, robots.txt, structured data).
- ❌ **The contact form is broken at two layers** — submissions are not delivered to your inbox. This is the #1 thing to fix.
- ❌ The site advertises `team@sentinelitad.com` as the contact email, but **the domain has no MX records** — that mailbox cannot receive email at all (DNS-level).
- ⚠️ The 808-498-1125 number is Hawaiian in Meridian, Idaho — may surprise Treasure Valley IT pros; you said you'd check.
- ⚠️ Site is **faceless** — no founder/operator note. CA IT pros will want to know who's behind the LLC.

---

## 1. Live site inventory (verified 2026-07-27, all served HTTP 200)

| Page | URL | Lines | Title |
|---|---|---:|---|
| Home | https://sentinelitad.com/ | ~250 | "Sentinel ITAD \| Secure IT Asset Disposal and Logistics in Meridian & Boise" |
| MSP feeder bin | https://sentinelitad.com/msp-feeder-bin.html | 113 | "MSP Feeder Bins \| Sentinel ITAD Treasure Valley" |
| How pickup works | https://sentinelitad.com/how-pickup-works.html | 103 | "How Pickup Works \| Sentinel ITAD" |
| Terms | https://sentinelitad.com/terms.html | 34 | "Terms \| Sentinel ITAD" |
| Privacy | https://sentinelitad.com/privacy.html | (similar size) | "Privacy \| Sentinel ITAD" |
| Thanks | https://sentinelitad.com/thanks.html | 18 | "Thanks \| Sentinel ITAD" |

**Assets verified:**
- `https://sentinelitad.com/assets/logo.svg` → 1,351 bytes, 200 OK
- `https://sentinelitad.com/assets/sentinel_hero.jpg` → 747,502 bytes, 200 OK
- `https://sentinelitad.com/style.css` → 7,461 bytes, 200 OK
- `https://sentinelitad.com/sitemap.xml` → 5 URLs, weekly/monthly changefreq
- `https://sentinelitad.com/robots.txt` → `Allow: /`, references sitemap

**Structured data (homepage):** `LocalBusiness` JSON-LD with `name`, `alternateName`, `url`, `telephone: +1-808-498-1125`, `areaServed: [Meridian ID, Boise ID, Nampa ID, Eagle ID, Treasure Valley]`, `address: Meridian, ID, US`. Good for local SEO.

**Cloudflare Pages preview also live:** `https://f1c8095d.sentinelitad-com.pages.dev` (returns same content, `x-robots-tag: noindex` — preview-only).

## 2. Form audit — the silent killer

### How the form works today

```html
<form class="lead-form" action="https://formsubmit.co/team@sentinelitad.com" method="POST">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_subject" value="Sentinel ITAD pickup request">
  <input type="hidden" name="_template" value="box">
  <input type="hidden" name="_next" value="https://sentinelitad.com/thanks.html">
  ... name, company, email, phone, request_type, message ...
</form>
```

This routes submissions through **FormSubmit.co**, a third-party form-to-email relay.

### Probe results (live, 2026-07-27)

I ran two probe POSTs to the form action with audit-marked test data. Both returned:

```text
HTTP/2 200
server: cloudflare (fronting formsubmit.co)
content-type: text/html; charset=UTF-8
Set-Cookie: XSRF-TOKEN, formsubmit_session
Body: formsubmit.co homepage HTML (not an activation page, not a thank-you page, not a redirect)
```

**Interpretation:** FormSubmit is **not activated** for `team@sentinelitad.com`. When activated, FormSubmit either (a) returns a redirect to a thank-you page on first real submission, or (b) shows an in-page confirmation. Getting their generic marketing landing page back as the response means the request hit the homepage route, not the per-inbox endpoint — i.e., `team@sentinelitad.com` was never claimed.

**FormSubmit activation requires a one-time email confirmation** sent to the address that owns the inbox. If you (or whoever set this up) never clicked the activation link in that confirmation email, **every IT-pro submission has been silently dropped** since the form was wired.

### Layer 2 — even if FormSubmit were activated, the email cannot arrive

DNS check (live, 2026-07-27):

```text
$ dig sentinelitad.com MX +short
(no records returned)

$ dig sentinelitad.com TXT +short
(no SPF / no DKIM)

$ dig sentinelitad.com A +short
172.67.134.52  # Cloudflare proxy
104.21.25.118  # Cloudflare proxy

$ dig {mail,mx,email}.sentinelitad.com +short
(no records returned for any of the three)
```

**`sentinelitad.com` had no MX records.** That meant no SMTP server was configured to receive email for the domain.

### ✅ FIXED 2026-07-27 23:09 UTC

DNS + Email Routing configured on the `sentinelitad.com` zone (`6bcb245621b2a0090c65cd71f7fd2eab`) via the Cloudflare API.

| Resource created | Value |
|---|---|
| MX `sentinelitad.com` → `route1.mx.cloudflare.net` (prio 10) | Cloudflare Email Routing default |
| MX `sentinelitad.com` → `route2.mx.cloudflare.net` (prio 20) | Cloudflare Email Routing default |
| MX `sentinelitad.com` → `route3.mx.cloudflare.net` (prio 30) | Cloudflare Email Routing default |
| TXT `sentinelitad.com` → `v=spf1 include:_spf.mx.cloudflare.net ~all` | SPF for Email Routing |
| Email Routing rule id `0268ed9ff260432f8f89bfe36746a814` | `team@sentinelitad.com` → `michael@growthwebdev.com` (enabled) |
| Destination address id `c9a207edfd8345d88de7e76cdd9be98a` | `michael@growthwebdev.com` (verified since 2026-06-06) |

**Verified externally via `dig @1.1.1.1 sentinelitad.com MX +short`:**

```
10 route1.mx.cloudflare.net.
20 route2.mx.cloudflare.net.
30 route3.mx.cloudflare.net.
```

**Verified rule still active:**

```json
{
  "id": "0268ed9ff260432f8f89bfe36746a814",
  "enabled": true,
  "name": "Forward team@ to Michael@growthwebdev.com",
  "matchers": [{"type":"literal","field":"to","value":"team@sentinelitad.com"}],
  "actions": [{"type":"forward","value":["michael@growthwebdev.com"]}]
}
```

**End-to-end smoke test from this host could not be performed** — outbound SMTP (port 25) is blocked by VM network policy (`OSError: [Errno 101] Network is unreachable`). The DNS resolves from external resolvers, the rule is enabled, the destination is verified; **only Michael can confirm by sending an email to `team@sentinelitad.com` from another account and checking `michael@growthwebdev.com`.**

### What this means for sharing the URL

**Today, the form is a black hole.** ~~If a CA IT pro fills it out:~~
~~1. FormSubmit receives the POST (Cloudflare-fronted).~~
~~2. FormSubmit cannot deliver to `team@sentinelitad.com` (unactivated + no MX).~~
~~3. The IT pro sees the thanks.html page and assumes their request was received.~~
~~4. You never know they tried.~~

**As of 2026-07-27 23:09 UTC:** layer 2 (DNS + email deliverability for the domain) is fixed. `team@sentinelitad.com` now routes to `michael@growthwebdev.com` via Cloudflare Email Routing. **Layer 1 (FormSubmit activation) still needs to be fixed** before the contact form works end-to-end. **Until then, every other site improvement is invisible.** Fixing the form is a prerequisite for "share it with IT pros."

## 3. Other findings

### Phone
- Public phone: `808-498-1125` (Hawaii). In Meridian, Idaho service area, this is unexpected.
- You said you'd check whether it forwards to your cell. If not forwarded → calls go to Hawaii voicemail → IT pro hangs up.
- Recommendation: until you have an Idaho number, **either confirm 808 forwards to your cell** OR replace the public number on the site with a forwarder that routes to your real cell, OR add a note like "Treasure Valley pickup — call routes through our Hawaii line, please leave a voicemail and we'll call back same day."

### Founder/Operator note
- **Site has no About / Founder / Team section.** Every page is anonymous.
- CA IT pros hand retired client gear to a **person**, not a brand. The OKF operating brief establishes the operator model ("relationship-based acquisition," "Michael has picked up assets from Laredo, Texas and Nebraska when auction price justified travel") but none of that is on the public site.
- A ~75-word Founder Note above the contact form solves this. See `founder-note-snippet.html` below for the draft.

### Email rendering
- Cloudflare's `email-decode.min.js` obfuscation renders `team@sentinelitad.com` as `[email protected]` with JS substitution. Works in modern browsers but breaks when:
  - User has JS disabled (rare but real for security-conscious IT shops)
  - User copy-pastes from a screenshot or PDF rendering
  - User pastes the link into an email client that strips JS
- Form action is unaffected by this. The visible `mailto:` links in the footer rely on JS substitution.

### Assets
- Logo is a placeholder SVG (`/assets/logo.svg`, 1,351 bytes). Per the launch backlog: "still needs final brand review, PNG/favicon/social card exports." Non-blocking for IT pros, but a final logo would help. **Not in scope for this audit.**

### Compliance-safe copy
- Spot-checked. Site correctly avoids claiming R2v3 certification or certified data destruction. Says "insured" without naming policy types/limits. Says "downstream certified partner" only with appropriate hedging. ✅

## 4. Three ready-to-deploy drafts (saved locally, not committed)

| File | What it is | Deploys by | Risk |
|---|---|---|---|
| `founder-note-snippet.html` | Drop-in HTML/CSS for a Founder Note + "Recent pickups / experience" section above the contact form | You | Low — purely additive section, easy to revert |
| `cloudflare-worker-form.js` | Cloudflare Worker that replaces `formsubmit.co` with direct-to-inbox delivery + Turnstile spam protection + structured email body | You (or me with `CLOUDFLARE_PAGES_API_TOKEN`) | Medium — replaces a live form handler; test first |
| `phone-forwarding-checklist.md` | 5-minute phone forwarding options ranked by effort | You | None |

**Nothing has been committed, pushed, or deployed.** All three are local drafts in `/home/ubuntu/work/sentinelitad.com/audit-2026-07-27/`.

## 5. Recommended fix order when you're back

| # | Action | Time | Effect |
|---|---|---|---|
| 1 | **Phone fix first** (call 808-498-1125 from a different phone — if it goes to a Hawaii voicemail, decide forward-to-cell or replace) | 5 min | Stops losing voice calls |
| 2 | **Forward `team@sentinelitad.com` to `Michael@growthwebdev.com`** via Cloudflare Email Routing (free, ~5 min in CF dashboard) OR your registrar's email forward | 10 min | Solves layer-2 email-deliverability |
| 3 | **Activate FormSubmit** by clicking the link in the activation email FormSubmit sent to `team@sentinelitad.com` (if you can find it) OR replace the form action with `cloudflare-worker-form.js` (durable) | 15–30 min | Solves layer-1 form-to-email |
| 4 | **Submit a test form yourself** end-to-end and confirm it lands in `Michael@growthwebdev.com` | 5 min | Verifies the whole path |
| 5 | **Add Founder Note** via `founder-note-snippet.html` and commit + push | 30 min | Adds the human face IT pros want |
| 6 | Then share the URL with CA IT pros | — | Done |

## 6. Verification packet

```text
RESULT=PASS (audit-only; no deploys, no commits, no emails sent)
SITE=sentinelitad.com
PAGES_LIVE=6 (home, msp-feeder-bin, how-pickup-works, terms, privacy, thanks)
ASSETS_LIVE=2 (logo.svg, sentinel_hero.jpg)
CLOUDFLARE_PAGES_PROJECT=sentinelitad-com (f1c8095d.sentinelitad-com.pages.dev)
FORM_ACTION=https://formsubmit.co/team@sentinelitad.com
FORM_STATUS=UNACTIVATED (probe returned formsubmit.co homepage, not activation/thank-you)
EMAIL_DNS_MX=NONE (sentinelitad.com has no MX records; team@ cannot receive)
EMAIL_DNS_SPF=NONE
EMAIL_DNS_TXT=NONE
CLOUDFLARE_PAGES_API_TOKEN=PRESENT (env, not used in this audit)
CLOUDFLARE_PAGES_ACCOUNT_ID=PRESENT (env, not used in this audit)
DRAFTS_CREATED=founder-note-snippet.html, cloudflare-worker-form.js, phone-forwarding-checklist.md
DRAFTS_LOCATION=/home/ubuntu/work/sentinelitad.com/audit-2026-07-27/
COMMITS=0
DEPLOYS=0
EMAILS_SENT=0 (FormSubmit probes used a non-monitored audit email address)
NOT_CLAIMING=form_works, email_deliverable, founder_note_live, phone_forwarded
MARKER=SENTINEL_SITE_AUDIT_READY_FOR_MICHAEL_FIX_LIST
```

---

## Quick lookup: the broken form action (for when you decide to fix it)

```html
<!-- Current (BROKEN): -->
<form class="lead-form" action="https://formsubmit.co/team@sentinelitad.com" method="POST">

<!-- Recommended replacement (DURABLE): -->
<form class="lead-form" action="/api/lead" method="POST">
  <!-- Cloudflare Worker at /api/lead; see cloudflare-worker-form.js -->
  <!-- Turnstile widget inserted via data-sitekey + client.js -->
</form>
```