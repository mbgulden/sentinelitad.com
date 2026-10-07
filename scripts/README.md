# Site chrome (header/footer) workflow

The header and footer are **not** hand-edited per page. They live once, in:

- `public/partials/header.html` — canonical header template
  (placeholders: `{{BRAND_HREF}}`, `{{NAV_BLOCK}}`, `{{CTA_HREF}}`, `{{CTA_TEXT}}`)
- `public/partials/footer.html` — canonical footer (no placeholders)

`scripts/stamp-chrome.py` renders them into every page under `public/`
between marker comments (`<!-- CHROME:HEADER -->` … `<!-- /CHROME:HEADER -->`,
same for footer). Per-page differences (nav variant, CTA target/text, active
nav item) live in the script's `PAGES` table — the only page-specific chrome
config in the repo.

## Making a header/footer change

1. Edit `public/partials/header.html` or `public/partials/footer.html`
   (or the `PAGES` table in the script for per-page config).
2. Run from the repo root:
   ```
   python3 scripts/stamp-chrome.py
   ```
3. Review: `git diff public/` — page bodies must not change, only chrome regions.
4. Push as one commit per change-set (e.g. via `gh-commit-files.py`).

## Drift check

```
python3 scripts/stamp-chrome.py --check
```

Exits 1 and lists pages whose chrome differs from the stamped output.
Run it before pushing chrome changes, or wire it into CI.

## Notes

- `thanks.html` carries the standard header/footer (it had none before).
- `privacy.html` / `terms.html` keep their minimal header (brand + CTA) and no
  footer, exactly as before — no visual changes there.
- we-buy pages keep their `#sell` "Get an offer" CTA (their sell-form anchor).
- The active nav item gets `aria-current="page"` (no visual change; not styled).
- Page bodies are never touched by the script — verified byte-identical
  outside the chrome regions.
