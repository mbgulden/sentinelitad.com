# Phone Forwarding Checklist — 808-498-1125

The site currently advertises `808-498-1125` as the public phone. **You decided (2026-07-27): keep the number on the site, forward it from the Hawaiian carrier to your cell.**

Goal: every call to `808-498-1125` rings your cell, regardless of where you are.

## Why this is the right call

- The Hawaiian number is **already in the site's brand** — JSON-LD `LocalBusiness` schema, every page footer, every CTA button, every thanks page.
- Treasure Valley IT pros will see a Hawaiian number and either (a) call it because they don't care, or (b) mention "interesting area code" — both are fine. The OKF operating brief notes: "Hawaiian number may be a conversation starter."
- Zero risk of exposing your real cell on a public marketing site.
- Zero per-minute cost if you have a Hawaiian carrier plan with free forwarding (most do).

## Quick diagnosis (5 minutes from your phone)

1. **Call 808-498-1125 from a different phone** (a friend's, a Google Voice number, or your work cell if you have one).
2. **Listen for:**
   - **Your own voice / your cell voicemail** → already forwarded. You're done — no work needed.
   - **"The number you have dialed has not been assigned" / "disconnected" / dead air** → number is dead. Call Hawaiian carrier to reactivate or port to a new line.
   - **A Hawaii-area voicemail greeting** (different accent, different city name) → not forwarded. Proceed with carrier-side forwarding below.

## Carrier-side forwarding (5 minutes)

The exact menu names vary by carrier. The general sequence for **Hawaiian Telcom, Spectrum Hawaii, or T-Mobile Hawaii**:

### Hawaiian Telcom (most common in HI)

1. Log in to your account at hawaiiantel.com.
2. Go to **My Account → Phone → Call Forwarding** (or dial `*72` from your Hawaiian line and follow prompts).
3. Choose **"Forward all calls"** (not selective — selective forwarding misses voicemail-only or after-hours calls).
4. Enter your 10-digit cell number.
5. Save. You should hear a confirmation tone.
6. Test from another phone.

### T-Mobile Hawaii

1. Log in to my.t-mobile.com or use the T-Mobile app.
2. Go to **Manage add-ons → Call forwarding** (some plans require the "Scam Shield" or "Name ID" toggle for forwarding controls).
3. Set unconditional forwarding to your cell.
4. Save and test.

### Spectrum Hawaii

1. Log in to spectrum.net → My Account → Voice → Settings.
2. Enable **"Forward all calls to"** and enter your cell.
3. Save and test.

## What you should hear when testing

| Result | Meaning |
|---|---|
| Hawaiian line rings → your cell rings → you answer | ✅ Working |
| Hawaiian line rings → your cell rings once → goes to your cell voicemail | ✅ Working (cell carrier forwarding is fine) |
| Hawaiian line rings → your cell voicemail picks up after 4+ rings | ✅ Working but cell is slow to ring — set your cell to ring longer before voicemail |
| Hawaiian line rings → Hawaiian voicemail picks up | ❌ Forwarding not active — re-do the steps above |
| Hawaiian line rings → "disconnected" or fast-busy | ❌ Hawaiian line is dead — call carrier support |

## Important caveats

- **Hawaiian carriers sometimes charge per forwarded minute.** Check your plan — T-Mobile and Spectrum typically include free forwarding; Hawaiian Telcom may charge ~$0.05/minute. If expensive, the alternative is to ask the carrier to **port the 808 number to a free forwarding service** (Google Voice porting works for most US numbers).
- **If your cell is unreachable or off**, forwarded calls may go to Hawaiian voicemail (which IT pros won't want to leave a message on). Solution: forward to a number that *always* rings, or set your cell's voicemail to clearly identify you as Sentinel ITAD.
- **Do not** publish a separate "voicemail" greeting that says "leave a message" — Treasure Valley IT pros expect a human. If you can't answer live, return the call within 2 hours during business hours and update the site's thanks.html to say so.

## What I did NOT do

- ❌ No site file edits (no commit, no push, no Cloudflare Pages deploy).
- ❌ No calls placed to 808-498-1125 (would tie up your line).
- ❌ No carrier-side mutations (requires your Hawaiian carrier login).
- ❌ No Google Voice attempt (you reported that errored out — abandoned).
- ❌ No DNS changes — the DNS routing we set up for `team@sentinelitad.com` is independent of the phone number.

## Status after this fix

Once carrier-side forwarding is active and tested, the only thing between you and "share the URL with CA IT pros" is the **Founder Note** (ready as a draft at `audit-2026-07-27/founder-note-snippet.html`) and a self-test of the contact form end-to-end.

Send me a one-liner when carrier forwarding is confirmed and I'll do the self-test on your behalf.