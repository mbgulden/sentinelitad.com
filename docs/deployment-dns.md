# sentinelitad.com Deployment and DNS Notes

## Current state

- GitHub repo: `mbgulden/sentinelitad.com`
- Current GitHub Pages preview/fallback: `https://mbgulden.github.io/sentinelitad.com/`
- Preferred production host per Michael: **Cloudflare Pages**
- Output directory: `public`
- Build command: none
- Production branch: `ned/initial-website` until a main/default production branch is created
- Custom domain target: `sentinelitad.com`

## Cloudflare Pages setup

Create or connect a Cloudflare Pages project with:

| Setting | Value |
|---|---|
| Project name | `sentinelitad-com` |
| Repository | `mbgulden/sentinelitad.com` |
| Production branch | `ned/initial-website` |
| Framework preset | None / static |
| Build command | empty / none |
| Build output directory | `public` |
| Custom domain | `sentinelitad.com` |
| Optional `www` | `www.sentinelitad.com` redirecting to apex |

## DNS still needed

`sentinelitad.com` currently fails DNS resolution from this VM. The custom domain will not work until the domain is in Cloudflare DNS or otherwise pointed at the Cloudflare Pages custom-domain target.

If the zone is managed by Cloudflare, use the Pages custom domain flow and let Cloudflare create the required CNAME/flattened records. If the zone is outside Cloudflare, add the CNAME target Cloudflare Pages provides after the project/custom domain is created.

## GitHub Pages fallback

GitHub Pages remains useful as a preview URL while Cloudflare comes online:

- `https://mbgulden.github.io/sentinelitad.com/`

The existing `public/CNAME` contains `sentinelitad.com`, but Cloudflare Pages does not require that file. It is harmless as a domain marker and can be removed later if Cloudflare-specific deployment complains.


## Cloudflare work performed — 2026-07-09

- Created Cloudflare Pages project: `sentinelitad-com`.
- First direct deployment URL: `https://f1c8095d.sentinelitad-com.pages.dev`.
- Added Pages custom domains through the Cloudflare API:
  - `sentinelitad.com`
  - `www.sentinelitad.com`
- Added proxied Cloudflare DNS CNAME records pointing both apex and `www` to `sentinelitad-com.pages.dev`. Cloudflare will flatten the apex record.

Propagation/certificate state may lag creation. Verify with:

```bash
curl -I https://sentinelitad.com/
curl -I https://www.sentinelitad.com/
curl -I https://sentinelitad-com.pages.dev/
```

If Cloudflare Pages reports `CNAME record not set`, wait for DNS propagation and re-check the Pages domain status.
