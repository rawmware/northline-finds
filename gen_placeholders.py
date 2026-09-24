#!/usr/bin/env python3
"""Generate branded SVG placeholder images for products without photos.

Usage: python3 gen_placeholders.py [--products path]
Writes assets/img/<id>.svg for every product that has no photo yet.
Re-run build.py afterwards.
"""
import argparse
import html
import json
import re
from pathlib import Path

STORE = Path(__file__).resolve().parent
RESEARCH_JSON = STORE.parent / "research" / "products.json"
IMG_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".svg"]

ICONS = {
    "kitchen": '<path d="M4 17h16"/><path d="M12 7a8 8 0 0 1 8 8H4a8 8 0 0 1 8-8z"/><path d="M12 7V4"/><circle cx="12" cy="3" r="1"/>',
    "home": '<path d="M4 11l8-7 8 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-6h4v6"/>',
    "car": '<path d="M5 15l1.6-4.6A2 2 0 0 1 8.5 9h7a2 2 0 0 1 1.9 1.4L19 15"/><path d="M4 15h16v4h-2.5"/><path d="M4 15v4h2.5"/><circle cx="8" cy="19" r="1.6"/><circle cx="16" cy="19" r="1.6"/>',
    "pet": '<circle cx="8.5" cy="10" r="1.8"/><circle cx="15.5" cy="10" r="1.8"/><circle cx="5.8" cy="14.5" r="1.8"/><circle cx="18.2" cy="14.5" r="1.8"/><path d="M12 12.5c2.8 0 5 2 5 4.2 0 1.4-1.2 2.3-2.6 2.3-1 0-1.7-.5-2.4-.5s-1.4.5-2.4.5c-1.4 0-2.6-.9-2.6-2.3 0-2.2 2.2-4.2 5-4.2z"/>',
    "phone & gadgets": '<rect x="8" y="3" width="8" height="18" rx="2"/><path d="M11 18h2"/>',
}
DEFAULT_ICON = '<path d="M12 3l2.6 5.6 6 .7-4.4 4.1 1.1 5.9-5.3-3-5.3 3 1.1-5.9L3.4 9.3l6-.7z"/>'


def wrap_name(name, max_chars=22):
    words, lines, cur = name.split(), [], ""
    for w in words:
        if len((cur + " " + w).strip()) > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines[:2]


def placeholder_svg(name, category):
    icon = ICONS.get(category.lower(), DEFAULT_ICON)
    lines = wrap_name(name)
    texts = "".join(
        f'<text x="400" y="{640 + i * 52}" text-anchor="middle" font-family="Inter, Arial, sans-serif" '
        f'font-size="40" font-weight="700" fill="#0b2a5b">{html.escape(line)}</text>'
        for i, line in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f2f7fd"/>
      <stop offset="1" stop-color="#dfeafb"/>
    </linearGradient>
  </defs>
  <rect width="800" height="800" fill="url(#g)"/>
  <rect x="270" y="200" width="260" height="260" rx="60" fill="#ffffff" stroke="#d7e3f5" stroke-width="3"/>
  <g transform="translate(330,262) scale(7)" fill="none" stroke="#0b2a5b" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{icon}</g>
  {texts}
  <text x="400" y="740" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="24" font-weight="600" fill="#7d8aa0" letter-spacing="4">NORTHLINE FINDS</text>
</svg>
"""


def safe_id(pid):
    return re.sub(r"[^a-z0-9\-_]", "-", str(pid).lower()).strip("-") or "product"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--products", default=str(RESEARCH_JSON))
    args = ap.parse_args()
    data = json.loads(Path(args.products).read_text(encoding="utf-8"))
    products = data["products"] if isinstance(data, dict) and "products" in data else data
    made = []
    for p in products:
        sid = safe_id(p.get("id", ""))
        if any((STORE / "assets" / "img" / (sid + ext)).exists() for ext in IMG_EXTS):
            continue
        (STORE / "assets" / "img" / (sid + ".svg")).write_text(
            placeholder_svg(p.get("name", "Product"), p.get("category", "")), encoding="utf-8")
        made.append(sid)
    print(f"Generated {len(made)} placeholder SVGs: {made or 'none needed'}")


if __name__ == "__main__":
    main()
