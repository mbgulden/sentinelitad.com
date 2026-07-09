#!/usr/bin/env python3
"""Sentinel ITAD theme verification helper.

This is the repo-local equivalent of the ad-hoc /tmp verifier agents should run
when changing theme/module files. Keep it focused and boring.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FAIL: list[str] = []


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def require(condition: bool, label: str) -> None:
    if not condition:
        FAIL.append(label)


required = [
    "public/style.css",
    "src/styles/theme.css",
    "src/theme/tokens.ts",
    "src/layouts/BaseLayout.astro",
    "src/components/Hero.astro",
    "src/components/CardGrid.astro",
    "src/components/TrustPanel.astro",
    "src/components/LeadCapture.astro",
    "src/content.config.ts",
    "src/content/pages/home.json",
    "docs/theme/sentinel-theme.md",
    "docs/theme/astro-modules.md",
    "docs/theme/emdash-integration.md",
    "docs/theme/redesign-playbook.md",
]
for rel in required:
    p = ROOT / rel
    require(p.exists(), f"missing {rel}")
    require(not p.exists() or p.stat().st_size > 0, f"empty {rel}")

css = text("public/style.css")
theme_css = text("src/styles/theme.css")
tokens = text("src/theme/tokens.ts")

require("color-scheme: light;" in css, "public CSS must keep light color-scheme")
require("color-scheme: dark;" not in css, "public CSS must not set global dark color-scheme")
require("--bg: #f7f8fb" in css, "public CSS must keep light page bg token")
require(".dark { background:" in css, "dark background must remain scoped to .dark")
require("color-scheme: light;" in theme_css, "Astro theme CSS must keep light color-scheme")
require("dark backgrounds only inside scoped modules" in tokens or "Dark backgrounds only inside scoped modules" in tokens, "tokens must document dark scope rule")

for rel in ["public/index.html", "public/msp-feeder-bin.html", "public/how-pickup-works.html", "public/privacy.html", "public/terms.html", "public/thanks.html"]:
    try:
        HTMLParser().feed(text(rel))
    except Exception as exc:  # pragma: no cover - direct script
        FAIL.append(f"HTML parse failed {rel}: {exc}")

for rel in ["public/sitemap.xml", "public/assets/logo.svg"]:
    try:
        ET.parse(ROOT / rel)
    except Exception as exc:  # pragma: no cover
        FAIL.append(f"XML/SVG parse failed {rel}: {exc}")

for rel in ["src/content/pages/home.json", "src/content/pages/msp-feeder-bin.json", "src/content/pages/how-pickup-works.json"]:
    try:
        data = json.loads(text(rel))
        require("title" in data and "hero" in data, f"{rel} must include title and hero")
    except Exception as exc:  # pragma: no cover
        FAIL.append(f"JSON parse failed {rel}: {exc}")

result = subprocess.run(["git", "diff", "--check"], cwd=ROOT, text=True, capture_output=True)
if result.returncode:
    FAIL.append("git diff --check failed: " + (result.stdout + result.stderr).strip())

if FAIL:
    print("FAIL")
    for item in FAIL:
        print("-", item)
    sys.exit(1)

print("PASS: Sentinel theme/Astro/EmDash scaffolding invariants hold")
