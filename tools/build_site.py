#!/usr/bin/env python3
"""Builds the static pages: wraps every src/<name>.html body in the shared shell.

Each source file starts with a one-line JSON comment: <!-- {"title": ..., "description": ..., "nav": ...} -->
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://alexriakhin.com/Metronome/"

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{base}assets/img/icon.png">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#F3F2FA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A0E20" media="(prefers-color-scheme: dark)">
<link rel="icon" type="image/png" sizes="32x32" href="favicons/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicons/favicon-16x16.png">
<link rel="apple-touch-icon" href="favicons/apple-touch-icon.png">
<link rel="manifest" href="favicons/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="./"><img src="assets/img/icon.png" alt="" width="34" height="34">Metronome <small>the metronome that listens</small></a>
    <nav aria-label="Main">
      <a href="./#features"{nav_features}>Features</a>
      <a href="support.html"{nav_support}>Support</a>
    </nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <nav aria-label="Footer">
      <a href="./">Home</a>
      <a href="support.html">Support</a>
      <a href="privacy.html">Privacy Policy</a>
      <a href="terms.html">Terms of Use</a>
      <a href="mailto:support@alexriakhin.com">support@alexriakhin.com</a>
    </nav>
    <span class="copy">© 2026 Aleksandr Riakhin</span>
  </div>
</footer>
</body>
</html>
"""


def build():
    pages = []
    for src in sorted((ROOT / "src").glob("*.html")):
        text = src.read_text()
        meta_match = re.match(r"<!--\s*(\{.*?\})\s*-->\n", text)
        meta = json.loads(meta_match.group(1))
        body = text[meta_match.end():]
        name = src.stem
        out = "index.html" if name == "index" else f"{name}.html"
        canonical = BASE if name == "index" else BASE + out
        nav = meta.get("nav", "")
        html = SHELL.format(
            title=meta["title"],
            description=meta["description"],
            canonical=canonical,
            base=BASE,
            body=body.rstrip(),
            nav_features=' aria-current="page"' if nav == "features" else "",
            nav_support=' aria-current="page"' if nav == "support" else "",
        )
        (ROOT / out).write_text(html)
        pages.append(canonical)
        print("wrote", out)

    urls = "\n".join(f"  <url><loc>{u}</loc></url>" for u in pages)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    )


if __name__ == "__main__":
    build()
