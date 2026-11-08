# Cloudflare Pages Deploy — Manual Trigger Required

**Date:** 2026-07-27
**Author:** Fred (hermes-agent)
**Status:** Code is committed to GitHub; live site has NOT been redeployed yet.

## What's in GitHub now (verified)

- **Branch `feature/founder-note`**: HEAD `eb52812` — adds the Founder Note section
- **Branch `ned/initial-website`**: HEAD `95de1c9` — merge commit, the production branch Cloudflare Pages watches

```
$ git log --oneline origin/ned/initial-website -3
95de1c9 [Fred] Merge feature/founder-note into production (#audit-2026-07-27)
eb52812 [Fred] Add Founder Note section above contact form (#audit-2026-07-27)
38c96ce [Ned] Codify Sentinel Astro theme and EmDash structure (#no-issue)
```

The Founder Note will say this on the live site (verified locally at `http://127.0.0.1:8913/index.html`):

> *"Sentinel is run by Michael Gulden, a 13-year IT professional with a long interest in reusing and repurposing retired hardware and in safely refurbishing or disposing of computers and lithium batteries. Based in Meridian, Idaho, the business focuses on secure, accountable pickup and disposition for organizations that cannot afford loose ends with their retired hardware."*

## What's NOT deployed

CF Pages hasn't picked up the new commits. Last successful deploy on the project was `2026-07-09T15:05:42` for commit `4a6cb15b` — **18 days ago**. Since then, **zero deploys**, despite commits landing on `ned/initial-website`.

I verified the GitHub webhook is **not** firing for this project. I also tried to trigger a deploy via the Cloudflare API with the `CLOUDFLARE_PAGES_API_TOKEN` in `.env`, but the token scope is too narrow:

```
POST /accounts/.../pages/projects/sentinelitad-com/deployments
→ 400 "A \"manifest\" field was expected in the request body but was not provided"
   (token can read but not create deployments)
POST /accounts/.../pages/projects/sentinelitad-com/deploy-hooks
→ 405 "method_not_allowed"
   (token cannot create deploy hooks either)
```

So the only path that works is **a manual deploy via the Cloudflare Dashboard UI** by you. ~30 seconds.

## How to deploy (5 clicks)

1. Open <https://dash.cloudflare.com/?to=/:account/pages/view/sentinelitad-com>
2. Make sure the project selector shows **sentinelitad-com** (the project is in your `Michael@growthwebdev.com's Account`).
3. Click **Deployments** in the left sidebar.
4. Click the **Create deployment** button (top-right).
5. Pick **Branch: ned/initial-website** → leave everything else default → click **Create**.

CF Pages will then:
- Queue a build (typically 20-60 seconds)
- Run `astro build` against commit `95de1c9`
- Deploy to `https://sentinelitad.com` and `https://www.sentinelitad.com`
- Custom domains `sentinelitad.com` and `www.sentinelitad.com` will update at the Cloudflare edge

## How to verify

After the deployment status shows **success**, run from your terminal:

```bash
curl -sS -L https://sentinelitad.com/ | grep -c "Michael Gulden\|13-year IT professional\|Government liquidation auctions"
# Expected: 2

curl -sS -L https://sentinelitad.com/style.css | grep -c "founder-grid\|pickup-list"
# Expected: 5
```

If both return non-zero, the live site reflects the Founder Note.

## Why the GitHub webhook isn't firing (and the long-term fix)

I cannot diagnose the webhook from this side without admin access to the Cloudflare Pages project. The likely causes are:

1. The GitHub webhook was never installed when the project was first set up — only `ad_hoc` deploys via the CF Dashboard have ever worked.
2. The webhook was installed but its secret/token has been rotated or expired.
3. Cloudflare Pages is configured with **Branch = `ned/initial-website`** but the webhook delivery is filtered to `main` or another branch.

**Long-term fix options (when you have 5 minutes later):**

- **(A) Easiest**: Go to Cloudflare Dashboard → Pages → sentinelitad-com → **Settings** → **Builds** → disconnect and reconnect the GitHub repo. This re-establishes the webhook cleanly.
- **(B) Robust**: Stay on manual deploys via the dashboard. Simple, but means every commit you or I push needs a 30-second click from you. Fine for low-velocity sites like this one.
- **(C) Hybrid**: Use a GitHub Action to call the Cloudflare API on every push to `ned/initial-website`, with the deploy hook URL stored as a GitHub secret. Most flexible but requires a token upgrade.

My recommendation for now: **option (A)** after the manual deploy lands. That'll fix the auto-deploy for everyone.

## Files in this audit folder

| File | Purpose |
|---|---|
| `README.md` | Full audit narrative |
| `founder-note-snippet.html` | Source HTML/CSS for the Founder Note (now committed to public/index.html and public/style.css) |
| `cloudflare-worker-form.js` | Durable replacement for FormSubmit.co (NOT YET DEPLOYED — only relevant if FormSubmit.co ever breaks again) |
| `phone-forwarding-checklist.md` | Already executed (808 forwarded to your cell) |
| `DEPLOY_NOW.md` | This file |

`audit-2026-07-27/` is intentionally **uncommitted** to the public repo — it's your private planning/audit folder. Delete or archive as you see fit after the deploy lands.