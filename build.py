"""Build stone-balancer.html from app.template.html.

Inlines the game icons (scratchpad icons/ dir, falling back to ./icons) as
base64 data URIs, and writes test-mobile.html with a viewport meta tag for
local mobile-emulation testing (the published artifact wrapper adds its own).
"""
import base64
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
CANDIDATES = [
    ROOT / "icons",
]

icons_dir = next((d for d in CANDIDATES if d.is_dir()), None)
if icons_dir is None:
    raise SystemExit("no icons directory found")

icons = {
    p.stem: "data:image/" + ("webp" if p.suffix == ".webp" else "png") + ";base64," + base64.b64encode(p.read_bytes()).decode()
    for p in sorted(list(icons_dir.glob("*.png")) + list(icons_dir.glob("*.webp")))
}

tpl = (ROOT / "app.template.html").read_text(encoding="utf-8")
out = tpl.replace('"__ICONS__"', json.dumps(icons))
(ROOT / "stone-balancer.html").write_text(out, encoding="utf-8")
(ROOT / "test-mobile.html").write_text(
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n' + out,
    encoding="utf-8",
)
print(f"built stone-balancer.html ({len(out):,} bytes, {len(icons)} icons)")
