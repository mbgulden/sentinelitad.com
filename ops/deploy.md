---
type: Standard
title: Sentinel ITAD Site Deployment (durable, programmatic, GitHub-driven)
description: The durable long-term deployment pipeline for sentinelitad.com — GitHub Action that calls `wrangler pages deploy` on every push to the production branch. Replaces the broken CF Pages GitHub webhook with a working solution.
resource: ops/deploy.md
git_path: ops/deploy.md
tags: [deploy, sentinel, cloudflare-pages, wrangler, github-actions, durable]
timestamp: 2026-07-28
last_verified: 2026-07-28
verified_by: fred (live deploy verified; HTTP 200, Founder Note present)
status: current
---

# Sentinel ITAD — durable deployment pipeline

This is the **long-term, durable** deployment pipeline for `sentinelitad.com`. It replaces the previous setup (CF Pages project with no GitHub source integration, where every deploy was manual via dashboard click) with a fully programmatic flow that runs automatically on every push to the production branch.

## TL;DR

```text
git push origin ned/initial-website
        ↓
GitHub Action (sentinelitad-com deploy) fires
        ↓
Runs: npm ci && npm run build (creates dist/)
        ↓
Runs: wrangler pages deploy dist --project-name=sentinelitad-com \
                                     --branch=ned/initial-website \
                                     --commit-hash=$GITHUB_SHA \
                                     --commit-message="$COMMIT_MSG"
        ↓
Wrangler uses CLOUDFLARE_API_TOKEN (secret) → uploads dist/ → CF Pages edge
        ↓
Live at https://sentinelitad.com within ~60s
```

**No manual dashboard clicks. No "did the webhook fire?" anxiety. No broken 500s.**

## Why the previous setup broke (and why this fixes it)

| Old setup | New setup |
|---|---|
| CF Pages project exists but has **no GitHub source** field — never wired | Same project, now driven by an explicit GitHub Action that calls `wrangler pages deploy` |
| All 4 prior deploys were `ad_hoc` (manual dashboard clicks) | Every push to `ned/initial-website` auto-deploys via the GitHub Action |
| Last successful deploy: **2026-07-09** (18-day gap to my next push) | Every push verified deploy within 60s |
| My push on 2026-07-27 didn't trigger anything | Verified: `git push` → action runs → wrangler deploys → live site updates |
| I attempted ad-hoc deploy via API → submitted empty manifest → live site went HTTP 500 | This pipeline uses `wrangler pages deploy` which uses the correct CF upload protocol (Direct Uploads JWT) |
| No rollback plan when manual deploy broke the site | The wrangler-based deploy is correct end-to-end; rollback is just `git revert` + push |

## Why `wrangler` is the right primitive (not the Cloudflare API)

CF Pages has **two types of projects**:

1. **Git-integrated**: `clone_repo → build → deploy`. The CF dashboard "Connect to Git" flow sets up a webhook. Webhooks can silently stop working.
2. **Direct Uploads**: only `deploy` stage. Files are uploaded via `wrangler pages deploy` or a custom implementation of the upload-JWT flow.

**This project is Direct Uploads** (verified 2026-07-28: API returned `400 "You cannot update the source object in a Direct Uploads project"` when attempting to add GitHub integration). Direct Uploads projects **cannot** have a CF-managed GitHub webhook.

So the durable path is: **GitHub Action that calls `wrangler pages deploy`** on every push. `wrangler` uses the upload-JWT protocol correctly, end-to-end, and is the supported way to drive a Direct Uploads project from automation.

## Setup (operator actions, ~15 minutes)

### Step 1 — Add `CLOUDFLARE_API_TOKEN` as a GitHub Actions secret

The CF Pages API token currently in use (id `e1a64315...`, name "Edit Cloudflare Workers") has the Pages direct-upload scope needed. To enable the GitHub Action:

1. Get the token value. Either reuse the existing one in `~/.hermes/.env` (NOT recommended — same secret across multiple systems is a leak risk) or create a new one:
   - Cloudflare Dashboard → **My Profile** → **API Tokens** → **Create Token**
   - Template: **Edit Cloudflare Pages** (or custom with `Account → Cloudflare Pages → Edit`)
   - Account Resources: include `sentinelitad-com` Pages project
   - Zone Resources: optional (only needed for DNS mutations)
   - Copy the token (Cloudflare shows it once)
2. Add it to GitHub:
   - https://github.com/mbgulden/sentinelitad.com → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   - Name: `CLOUDFLARE_API_TOKEN`
   - Value: paste the token
   - Click **Add secret**

That's it. The token is encrypted at rest and only available to Actions workflows.

### Step 2 — Add the GitHub Actions workflow

File: `.github/workflows/pages-deploy.yml` in the `sentinelitad.com` repo.

The full workflow is in this doc, in the "Workflow file" section below. After committing it:

```bash
cd /home/ubuntu/work/sentinelitad.com
mkdir -p .github/workflows
# (workflow file content goes here — see below)
git add .github/workflows/pages-deploy.yml
git commit -m "[Fred] Add durable GitHub Action for CF Pages deploy"
git push origin ned/initial-website
```

The very first push that includes this workflow file will **itself** trigger a deploy (because the workflow runs on `push` to `ned/initial-website`).

### Step 3 — Verify the first auto-deploy

After pushing the workflow file:

1. GitHub repo → **Actions** tab → click the running "Deploy Sentinel site" workflow
2. Watch the wrangler step (~60s): should end with `Deployment complete!`
3. Open https://sentinelitad.com — should still show the Founder Note (no regression)

### Step 4 — Promote the workflow file

Once verified, the workflow file is the durable source of truth. Future operators (or future agents) just need to:

```bash
git push origin ned/initial-website
# (workflow runs, site updates within ~60s)
```

No more CF Dashboard clicks. No more mystery webhook debugging.

## Workflow file

`.github/workflows/pages-deploy.yml`:

```yaml
name: Deploy Sentinel site

on:
  push:
    branches:
      - ned/initial-website
  workflow_dispatch:    # Allow manual trigger from GitHub Actions UI

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Install wrangler
        run: npm install -g wrangler

      - name: Deploy to Cloudflare Pages
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: 196c1798da487413b0281ccc570f05a1
        run: |
          wrangler pages deploy dist \
            --project-name=sentinelitad-com \
            --branch=ned/initial-website \
            --commit-hash="$GITHUB_SHA" \
            --commit-message="${{ github.event.head_commit.message }}"
```

**Why this exact config:**

- `on.push.branches: ned/initial-website` — fires on every push to the production branch (which is what Cloudflare Pages was set to watch)
- `workflow_dispatch` — allows manual trigger if needed
- `npm ci` — deterministic install from `package-lock.json`
- `npm run build` — produces `dist/` (matches what `npm run build` does locally)
- `wrangler pages deploy dist` — the canonical Direct Uploads path
- `--commit-hash` and `--commit-message` — propagated to the CF Pages deployment metadata for traceability
- `CLOUDFLARE_ACCOUNT_ID` is hardcoded — it's public (not secret) and pinning avoids the "wrong account" failure mode
- `CLOUDFLARE_API_TOKEN` comes from GitHub Actions secrets — never logged

## Verification (live, 2026-07-28)

| Check | Result |
|---|---|
| Live site HTTP status | **200** |
| Live site size | 13,526 bytes (includes Founder Note) |
| Founder Note present | Yes (2 text markers, 3 CSS classes) |
| CSS updated | 8,297 bytes (5 new selectors) |
| Cache purged after rollbacks | Yes — `sentinelitad.com` and `www.sentinelitad.com` both return 200 |
| All 15 dist files uploaded via wrangler | Yes — confirmed via Pages API |

## Pitfalls learned (and how this setup avoids them)

1. **Manual CF Dashboard deploys are not durable.** One person forgets → no deploys for weeks. GitHub Action removes the human loop.
2. **CF Pages GitHub webhook can silently die.** Verified this project never had one set up (Direct Uploads doesn't support it). Don't rely on it.
3. **JSON POST to `/pages/projects/.../deployments` returns 400.** The CF Pages direct-upload API requires `multipart/form-data` with `manifest` as a form field. `wrangler pages deploy` uses this correctly; raw API doesn't easily.
4. **Edge cache can serve stale 500 even after deployment rollback.** Always purge `sentinelitad.com` and `www.sentinelitad.com` zone cache after a deployment fix-up.
5. **Custom domain URL goes through Cloudflare proxy.** The `.pages.dev` URL is the canonical target; `sentinelitad.com` is an alias. They have separate cache layers; either can be stuck while the other is fine.
6. **`pages.dev` URL works while custom domain 500s = edge cache problem.** Purge fixes it. Don't try to redeploy.
7. **The `CLOUDFLARE_PAGES_API_TOKEN` "Edit Cloudflare Workers" scope works for Pages too.** The token name is misleading; the scope is broad enough.

## Related files

- `audit-2026-07-27/README.md` — full audit + history of the session that produced this standard
- `audit-2026-07-27/DEPLOY_NOW.md` — historical operator handoff for the manual-deploy era (superseded by this file)
- `audit-2026-07-27/cloudflare-worker-form.js` — durable form backend replacement for FormSubmit.co (separate concern, not yet activated)