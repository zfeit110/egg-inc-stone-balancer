"""Build the Stone Balancer pages from app.template.html.

Inlines the game icons in ./icons as base64 data URIs and writes:
  - stone-balancer.html  bare page content, published as the Claude Artifact
                         (the artifact wrapper supplies doctype/head/viewport)
  - index.html           standalone document for GitHub Pages
  - test-mobile.html     same as index.html, for local mobile-emulation testing
"""
import base64
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
icons_dir = ROOT / "icons"

icons = {
    p.stem: "data:image/" + ("webp" if p.suffix == ".webp" else "png") + ";base64,"
    + base64.b64encode(p.read_bytes()).decode()
    for p in sorted(list(icons_dir.glob("*.png")) + list(icons_dir.glob("*.webp")))
}

tpl = (ROOT / "app.template.html").read_text(encoding="utf-8")
out = tpl.replace('"__ICONS__"', json.dumps(icons))
(ROOT / "stone-balancer.html").write_text(out, encoding="utf-8")

# Standalone document for GitHub Pages: served raw, so it needs the full skeleton.
FAVICON = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg'"
    " viewBox='0 0 100 100'><text y='.9em' font-size='90'>%F0%9F%A5%9A</text></svg>"
)
standalone = "\n".join([
    "<!doctype html>",
    '<html lang="en">',
    "<head>",
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="robots" content="noindex">',
    '<link rel="icon" href="' + FAVICON + '">',
    "</head>",
    "<body>",
    out,
    "</body>",
    "</html>",
    "",
])
(ROOT / "index.html").write_text(standalone, encoding="utf-8")
(ROOT / "test-mobile.html").write_text(standalone, encoding="utf-8")
print(f"built ({len(out):,} bytes, {len(icons)} icons)")
