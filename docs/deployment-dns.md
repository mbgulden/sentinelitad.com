# sentinelitad.com Deployment and DNS Notes

## Current state

- GitHub repo: `mbgulden/sentinelitad.com`
- Deployment: GitHub Pages workflow from branch `ned/initial-website`
- Current preview URL: `https://mbgulden.github.io/sentinelitad.com/`
- `public/CNAME` is present and contains `sentinelitad.com`.
- GitHub Pages API currently reports `cname: null` because the domain does not resolve yet.

## DNS still needed

`sentinelitad.com` currently fails DNS resolution. Do not expect the custom domain to work until DNS is pointed at the Pages host or a Cloudflare Pages project.

### Option A — GitHub Pages apex domain

Create these A records at the DNS provider:

| Type | Name | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `mbgulden.github.io` |

Then set the Pages custom domain to `sentinelitad.com` in GitHub repo settings and wait for the certificate to issue.

### Option B — Cloudflare Pages

Create a Cloudflare Pages project from this repo using:

- Build command: none
- Output directory: `public`
- Production branch: `ned/initial-website` unless a main branch is later created
- Custom domain: `sentinelitad.com`

Cloudflare will create the required DNS records automatically if the zone is on Cloudflare.

## Do not change without approval

DNS is live infrastructure. Update it only after Michael confirms which deployment host should own `sentinelitad.com`.
