#!/usr/bin/env python3
"""Generate the animated SVGs used by README.md (dark + light variant of each).

    python3 scripts/readme-art.py        # writes assets/readme/*.svg

GitHub renders SVGs in READMEs as images: CSS/SMIL animations run, scripts do not.
Each file carries a prefers-reduced-motion fallback.
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "readme"

THEMES = {
    "dark": dict(
        bg0="#04060c", bg1="#0b1424", grid="#7dd3fc", grid_op=0.05, ink="#e6f1ff",
        muted="#7b8aa3", cyan="#22d3ee", violet="#a78bfa", hot="#ff3d8b", ring_op=0.18,
    ),
    "light": dict(
        bg0="#f8fafc", bg1="#e8eef7", grid="#0f172a", grid_op=0.05, ink="#0b1220",
        muted="#5b6b84", cyan="#0891b2", violet="#7c3aed", hot="#db2777", ring_op=0.22,
    ),
}

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
CALM = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def frame(w, h, t, body, style=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>
  <radialGradient id="bg" cx="30%" cy="45%" r="85%">
    <stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg0']}"/>
  </radialGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['cyan']}"/><stop offset="1" stop-color="{t['violet']}"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="{t['grid']}" stroke-opacity="{t['grid_op']}"/>
  </pattern>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>{style} {CALM}</style>
<rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#grid)"/>
{body}
</svg>
"""


def hero(t):
    w, h, cx, cy, r, period = 1200, 460, 300, 230, 170, 6.0
    rnd = random.Random(7)
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r * k / 4:.1f}" fill="none" stroke="{t["cyan"]}" stroke-opacity="{t["ring_op"]}"/>'
        for k in range(1, 5)
    )
    cross = (
        f'<path d="M{cx - r} {cy}H{cx + r}M{cx} {cy - r}V{cy + r}" stroke="{t["cyan"]}" stroke-opacity="{t["ring_op"] * 0.7}"/>'
    )
    blips, flagged = [], [(38, 0.62), (155, 0.83), (262, 0.45)]
    for _ in range(46):
        ang, rad = rnd.uniform(0, 360), r * math.sqrt(rnd.uniform(0.04, 0.95))
        x, y = cx + rad * math.cos(math.radians(ang)), cy + rad * math.sin(math.radians(ang))
        delay = ang / 360 * period
        blips.append(
            f'<circle class="blip" cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(1.6, 2.8):.1f}" fill="{t["cyan"]}" style="animation-delay:{delay:.2f}s"/>'
        )
    for i, (ang, f) in enumerate(flagged):
        x, y = cx + r * f * math.cos(math.radians(ang)), cy + r * f * math.sin(math.radians(ang))
        d = ang / 360 * period
        blips.append(
            f'<g><circle class="ping" cx="{x:.1f}" cy="{y:.1f}" r="4" fill="none" stroke="{t["hot"]}" stroke-width="1.6" style="animation-delay:{d:.2f}s"/>'
            f'<circle class="ping" cx="{x:.1f}" cy="{y:.1f}" r="4" fill="none" stroke="{t["hot"]}" stroke-width="1.2" style="animation-delay:{d + 0.6:.2f}s"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{t["hot"]}" filter="url(#glow)"/></g>'
        )
    sweep = (
        f'<defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{t["cyan"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["cyan"]}" stop-opacity=".45"/></linearGradient></defs>'
        f'<g class="sweep"><path d="M{cx} {cy}L{cx + r} {cy}A{r} {r} 0 0 0 {cx + r * math.cos(math.radians(-40)):.1f} {cy + r * math.sin(math.radians(-40)):.1f}Z" fill="url(#sw)"/>'
        f'<path d="M{cx} {cy}H{cx + r}" stroke="{t["cyan"]}" stroke-width="1.5" filter="url(#glow)"/></g>'
    )
    tx = 560
    text = f"""
<g font-family="{MONO}" font-size="13" letter-spacing="4" fill="{t['muted']}">
  <circle class="live" cx="{tx + 6}" cy="148" r="5" fill="{t['hot']}"/>
  <text x="{tx + 22}" y="153">LIVE · POLYMARKET INSIDER RADAR</text>
</g>
<text x="{tx}" y="238" font-family="{SANS}" font-size="70" font-weight="200" letter-spacing="9" fill="url(#shine)">PREDICTABLE</text>
<text x="{tx + 2}" y="290" font-family="{SANS}" font-size="22" font-weight="300" fill="{t['ink']}" fill-opacity=".78">The bets that were predictable — for someone.</text>
<g font-family="{MONO}" font-size="13" letter-spacing="2" fill="{t['muted']}">
  <text x="{tx + 2}" y="342">new accounts · impossible odds · perfect timing</text>
</g>
<rect x="{tx + 2}" y="366" width="64" height="2" fill="url(#accent)"/>
"""
    shine = f"""<defs><linearGradient id="shine" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
  <stop offset="0" stop-color="{t['ink']}"/><stop offset=".42" stop-color="{t['ink']}"/>
  <stop offset=".5" stop-color="{t['cyan']}"/><stop offset=".58" stop-color="{t['ink']}"/><stop offset="1" stop-color="{t['ink']}"/>
  <animate attributeName="x1" values="-1;1" dur="5s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="0;2" dur="5s" repeatCount="indefinite"/>
</linearGradient></defs>"""
    style = f"""
.sweep {{ transform-origin: {cx}px {cy}px; animation: spin {period}s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.blip {{ opacity: .15; animation: blip {period}s linear infinite; }}
@keyframes blip {{ 0% {{ opacity: .95; }} 35% {{ opacity: .2; }} 100% {{ opacity: .15; }} }}
.ping {{ transform-box: fill-box; transform-origin: center; animation: ping 2.4s ease-out infinite; }}
@keyframes ping {{ 0% {{ transform: scale(1); opacity: .9; }} 100% {{ transform: scale(5); opacity: 0; }} }}
.live {{ animation: live 1.6s ease-in-out infinite; }}
@keyframes live {{ 50% {{ opacity: .25; }} }}"""
    return frame(w, h, t, shine + rings + cross + sweep + "".join(blips) + text, style)


def tell(t):
    w, h, left, right, top, base = 1200, 330, 80, 1120, 70, 250
    rnd = random.Random(3)
    jump_x, entry_x = 930, 700
    pts, x = [], left
    while x < jump_x:
        pts.append((x, base - 6 - rnd.uniform(0, 8)))
        x += 14
    pts += [(jump_x + 6, base - 40), (jump_x + 14, top + 40), (jump_x + 22, top + 6), (right, top)]
    path = "M" + " L".join(f"{px:.0f} {py:.1f}" for px, py in pts)
    # Real length for the draw-in dash (pathLength + CSS dashes is unreliable in Safari).
    length = math.ceil(sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))) + 2
    entry_y = next(py for px, py in pts if px >= entry_x)
    body = f"""
<g font-family="{MONO}" font-size="12" letter-spacing="2" fill="{t['muted']}">
  <text x="{left}" y="44">A LONGSHOT, AS THE MARKET SAW IT</text>
  <text x="{right}" y="{top - 14}" text-anchor="end">100¢</text>
  <text x="{right}" y="{base + 26}" text-anchor="end">4¢</text>
</g>
<path d="M{left} {base}H{right}" stroke="{t['muted']}" stroke-opacity=".25" stroke-dasharray="2 6"/>
<path d="M{left} {top}H{right}" stroke="{t['muted']}" stroke-opacity=".15" stroke-dasharray="2 6"/>
<path class="line" d="{path}" fill="none" stroke="url(#accent)" stroke-width="3" stroke-linejoin="round" filter="url(#glow)"/>
<g class="mark">
  <line x1="{entry_x}" y1="{entry_y:.1f}" x2="{entry_x}" y2="{top + 30}" stroke="{t['hot']}" stroke-opacity=".6" stroke-dasharray="3 4"/>
  <circle cx="{entry_x}" cy="{entry_y:.1f}" r="7" fill="{t['hot']}" filter="url(#glow)"/>
  <text x="{entry_x}" y="{top + 18}" text-anchor="middle" font-family="{SANS}" font-size="17" fill="{t['ink']}">someone bought — big</text>
</g>
<g class="news">
  <text x="{jump_x - 14}" y="{top + 100}" text-anchor="end" font-family="{SANS}" font-size="17" fill="{t['ink']}" fill-opacity=".8">then the news broke</text>
</g>
"""
    style = """
.line { stroke-dasharray: LEN; stroke-dashoffset: LEN; animation: draw 9s ease-in-out infinite; }
@keyframes draw { 0% { stroke-dashoffset: LEN; } 55%, 92% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: 0; opacity: 0; } }
.mark { opacity: 0; animation: mark 9s ease-out infinite; }
@keyframes mark { 0%, 34% { opacity: 0; } 40%, 92% { opacity: 1; } 100% { opacity: 0; } }
.news { opacity: 0; animation: news 9s ease-out infinite; }
@keyframes news { 0%, 52% { opacity: 0; } 58%, 92% { opacity: 1; } 100% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .line { stroke-dashoffset: 0; } .mark, .news { opacity: 1; } }""".replace(
        "LEN", str(length)
    )
    return frame(w, h, t, body, style)


def trio(t):
    w, h = 1200, 230
    cols = [
        ("FIND", "every trade, every wallet", "find"),
        ("SCORE", "nine signals, one number", "score"),
        ("FOLLOW", "every move, every 8 minutes", "follow"),
    ]
    out = []
    for i, (title, line, kind) in enumerate(cols):
        x0 = 60 + i * 380
        gx, gy = x0 + 40, 115
        if kind == "find":
            glyph = (
                f'<circle cx="{gx}" cy="{gy}" r="26" fill="none" stroke="url(#accent)" stroke-width="2.5"/>'
                f'<line x1="{gx + 19}" y1="{gy + 19}" x2="{gx + 36}" y2="{gy + 36}" stroke="url(#accent)" stroke-width="3" stroke-linecap="round"/>'
                f'<circle class="pulse" cx="{gx}" cy="{gy}" r="6" fill="{t["hot"]}"/>'
            )
        elif kind == "score":
            glyph = "".join(
                f'<rect class="bar" x="{gx - 26 + k * 14}" y="{gy - hgt}" width="9" height="{hgt}" rx="2" fill="url(#accent)" style="animation-delay:{k * 0.25:.2f}s"/>'
                for k, hgt in enumerate([14, 26, 20, 40])
            )
        else:
            glyph = (
                f'<path d="M{gx - 30} {gy + 22} C{gx - 10} {gy - 30} {gx + 8} {gy + 40} {gx + 30} {gy - 22}" fill="none" stroke="url(#accent)" stroke-width="2.5" stroke-dasharray="4 6"/>'
                f'<circle class="ride" r="6" fill="{t["hot"]}"><animateMotion dur="3.2s" repeatCount="indefinite" '
                f'path="M{gx - 30} {gy + 22} C{gx - 10} {gy - 30} {gx + 8} {gy + 40} {gx + 30} {gy - 22}"/></circle>'
            )
        out.append(
            f"""<g>{glyph}
<text x="{x0 + 100}" y="{gy - 6}" font-family="{MONO}" font-size="20" letter-spacing="6" fill="{t['ink']}">{title}</text>
<text x="{x0 + 100}" y="{gy + 22}" font-family="{SANS}" font-size="16" font-weight="300" fill="{t['muted']}">{line}</text></g>"""
        )
    style = """
.pulse { animation: pulse 1.8s ease-in-out infinite; }
@keyframes pulse { 50% { opacity: .2; } }
.bar { transform-box: fill-box; transform-origin: bottom; animation: bar 2.4s ease-in-out infinite; }
@keyframes bar { 50% { transform: scaleY(.45); } }"""
    return frame(w, h, t, "".join(out), style)


def button(t):
    w, h = 520, 96
    body = f"""
<defs><linearGradient id="glint" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
<clipPath id="pill"><rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="{(h - 16) / 2}"/></clipPath></defs>
<rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="{(h - 16) / 2}" fill="{t['bg0']}" stroke="url(#accent)" stroke-width="2.5" filter="url(#glow)"/>
<g clip-path="url(#pill)"><rect class="glint" x="-160" y="0" width="140" height="{h}" fill="url(#glint)"/></g>
<text x="{w / 2}" y="{h / 2 + 7}" text-anchor="middle" font-family="{MONO}" font-size="20" letter-spacing="6" fill="{t['ink']}">OPEN THE DASHBOARD  →</text>
"""
    style = """
.glint { animation: glint 3.5s ease-in-out infinite; }
@keyframes glint { 0% { transform: translateX(0); } 60%, 100% { transform: translateX(720px); } }"""
    svg = frame(w, h, t, body, style)
    # A button has no card background: drop the framed rectangles.
    return svg.replace(f'<rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>', "").replace(
        f'<rect width="{w}" height="{h}" rx="18" fill="url(#grid)"/>', ""
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, make in [("hero", hero), ("tell", tell), ("trio", trio), ("button", button)]:
        for theme, t in THEMES.items():
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(make(t))
            print(f"wrote {path.relative_to(OUT.parent.parent)} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
