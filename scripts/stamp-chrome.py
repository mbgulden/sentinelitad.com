#!/usr/bin/env python3
"""Stamp shared header/footer chrome into sentinelitad.com public/*.html pages.

The canonical chrome lives in public/partials/header.html and
public/partials/footer.html. This script is the ONLY writer of chrome:
edit the partials, run this script, review the diff, push.

Usage:
    python3 scripts/stamp-chrome.py            # stamp all pages in public/
    python3 scripts/stamp-chrome.py --check    # exit 1 if any page's chrome
                                               # differs from stamped output
    python3 scripts/stamp-chrome.py --root DIR # operate on DIR instead of
                                               # public/ (repo root assumed)

How it works:
  - Each page carries its chrome between marker comments:
        <!-- CHROME:HEADER --> ... <!-- /CHROME:HEADER -->
        <!-- CHROME:FOOTER --> ... <!-- /CHROME:FOOTER -->
    On the first run for a page without markers, the script finds the
    existing <header class="site-header"> / <footer> blocks and wraps them.
  - Per-page differences (nav variant, CTA target, active nav item) come from
    the PAGES table below -- the only place page-specific chrome lives.
  - The active nav item gets aria-current="page" (no visual change; style.css
    does not target it).
  - thanks.html has no chrome of its own; the script inserts the standard
    header after <body> and the footer before </body>.
  - privacy.html / terms.html keep their minimal header (brand + CTA, no nav)
    and no footer -- preserved exactly as today.

Workflow:
    1. Edit public/partials/header.html or public/partials/footer.html
    2. Run: python3 scripts/stamp-chrome.py
    3. Review: git diff public/
    4. Push (one commit per change-set, e.g. via gh-commit-files.py)
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HEADER_PARTIAL = "public/partials/header.html"
FOOTER_PARTIAL = "public/partials/footer.html"

HEADER_OPEN = "<!-- CHROME:HEADER -->"
HEADER_CLOSE = "<!-- /CHROME:HEADER -->"
FOOTER_OPEN = "<!-- CHROME:FOOTER -->"
FOOTER_CLOSE = "<!-- /CHROME:FOOTER -->"

# Nav item variants. hrefs are root-relative so one template serves every page.
NAV_FULL5 = [
    ("/#services", "Services"),
    ("msp-feeder-bin.html", "MSP bins"),
    ("how-pickup-works.html", "Pickup process"),
    ("we-buy-used-it-equipment.html", "We buy gear"),
    ("/#contact", "Contact"),
]
NAV_SLIM4 = [
    ("/#services", "Services"),
    ("msp-feeder-bin.html", "MSP bins"),
    ("how-pickup-works.html", "Pickup process"),
    ("/#contact", "Contact"),
]

# Per-page chrome config. `active` is the nav href of the current page (or None).
# `footer: False` preserves pages that intentionally have no footer.
PAGES = {
    "index.html":                    {"brand": "/", "nav": NAV_FULL5, "cta": "/#contact", "cta_text": "Request pickup", "active": None},
    "how-pickup-works.html":         {"brand": "/", "nav": NAV_SLIM4, "cta": "/#contact", "cta_text": "Request pickup", "active": "how-pickup-works.html"},
    "msp-feeder-bin.html":           {"brand": "/", "nav": NAV_SLIM4, "cta": "/#contact", "cta_text": "Request pickup", "active": "msp-feeder-bin.html"},
    "we-buy-used-it-equipment.html": {"brand": "/", "nav": NAV_FULL5, "cta": "#sell",     "cta_text": "Get an offer",   "active": "we-buy-used-it-equipment.html"},
    "we-buy-server-ram.html":        {"brand": "/", "nav": NAV_FULL5, "cta": "#sell",     "cta_text": "Get an offer",   "active": None},
    "we-buy-retired-it-assets.html": {"brand": "/", "nav": NAV_FULL5, "cta": "#sell",     "cta_text": "Get an offer",   "active": None},
    "privacy.html":                  {"brand": "/", "nav": None,      "cta": "/#contact", "cta_text": "Request pickup", "active": None, "footer": False},
    "terms.html":                    {"brand": "/", "nav": None,      "cta": "/#contact", "cta_text": "Request pickup", "active": None, "footer": False},
    "thanks.html":                   {"brand": "/", "nav": NAV_FULL5, "cta": "/#contact", "cta_text": "Request pickup", "active": None},
}


def render_nav(items, active):
    if not items:
        return ""
    lines = ['  <nav aria-label="Primary navigation">']
    for href, label in items:
        cur = ' aria-current="page"' if href == active else ""
        lines.append(f'    <a href="{href}"{cur}>{label}</a>')
    lines.append("  </nav>")
    return "\n".join(lines) + "\n"


def render_header(cfg, partial):
    nav_block = render_nav(cfg["nav"], cfg.get("active"))
    return (
        partial.replace("{{BRAND_HREF}}", cfg["brand"])
               .replace("{{NAV_BLOCK}}", nav_block)
               .replace("{{CTA_HREF}}", cfg["cta"])
               .replace("{{CTA_TEXT}}", cfg["cta_text"])
    )


def indent_block(text, spaces=2):
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line
                     for line in text.rstrip("\n").split("\n"))


def wrap_markers(kind, chrome):
    if kind == "header":
        o, c = HEADER_OPEN, HEADER_CLOSE
    else:
        o, c = FOOTER_OPEN, FOOTER_CLOSE
    return f"  {o}\n{indent_block(chrome)}\n  {c}"


def replace_or_insert(page_text, kind, chrome):
    """Replace the marked chrome region; wrap existing raw blocks on first run;
    insert fresh chrome for pages missing it (thanks.html)."""
    o, c = (HEADER_OPEN, HEADER_CLOSE) if kind == "header" else (FOOTER_OPEN, FOOTER_CLOSE)
    new_block = wrap_markers(kind, chrome)
    if o in page_text:
        pattern = re.compile(r"^[ \t]*" + re.escape(o) + r".*?" + re.escape(c),
                             re.S | re.M)
        return pattern.sub(lambda _: new_block, page_text, count=1), True
    def line_start(m):
        ls = page_text.rfind("\n", 0, m.start()) + 1
        assert page_text[ls:m.start()].strip() == "", "indent before chrome block"
        return ls

    if kind == "header":
        m = re.search(r'<header class="site-header">.*?</header>', page_text, re.S)
        if m:
            s = line_start(m)
            return (page_text[:s] + new_block + page_text[m.end():]), True
        # no header at all: insert after <body...> line
        m = re.search(r"<body[^>]*>\n", page_text)
        assert m, "no <body> found"
        return page_text[:m.end()] + new_block + "\n" + page_text[m.end():], True
    else:
        m = re.search(r"<footer>.*?</footer>", page_text, re.S)
        if m:
            s = line_start(m)
            return (page_text[:s] + new_block + page_text[m.end():]), True
        # no footer at all: insert before </body>
        m = re.search(r"</body>", page_text)
        assert m, "no </body> found"
        return page_text[:m.start()] + new_block + "\n" + page_text[m.start():], True


def stamp_page(path, header_partial, footer_partial, check=False):
    cfg = PAGES[path.name]
    text = path.read_text()
    new_text, _ = replace_or_insert(text, "header", render_header(cfg, header_partial))
    if cfg.get("footer", True):
        new_text, _ = replace_or_insert(new_text, "footer", footer_partial)
    if check:
        return text != new_text
    if new_text != text:
        path.write_text(new_text)
        return True
    return False


def main():
    args = sys.argv[1:]
    check = "--check" in args
    root = REPO_ROOT
    if "--root" in args:
        root = Path(args[args.index("--root") + 1]).resolve()
    public = root / "public"
    header_partial = (root / HEADER_PARTIAL).read_text()
    footer_partial = (root / FOOTER_PARTIAL).read_text()

    changed, drift = [], []
    for name in sorted(PAGES):
        path = public / name
        assert path.exists(), f"missing page: {path}"
        if stamp_page(path, header_partial, footer_partial, check=check):
            (drift if check else changed).append(name)

    if check:
        if drift:
            print("CHROME DRIFT in: " + ", ".join(drift))
            return 1
        print("chrome OK: all pages match stamped output")
        return 0
    print("stamped: " + (", ".join(changed) if changed else "no changes (idempotent)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
