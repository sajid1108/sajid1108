"""Generates the pixel-art SVGs under assets/ for the profile README.

Run from the repo root:  python scripts/build_assets.py
Everything is deterministic (seeded), so re-running only changes what you edit.
"""
import math
import random
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- palette ---
BG = "#0b0c0e"
PANEL = "#111316"
EDGE = "#23272c"
STEEL_DK = "#2b2f34"
STEEL = "#555c64"
STEEL_MD = "#7d858e"
STEEL_LT = "#b9bfc6"
BONE = "#e6e1d6"
GOLD = "#d4a017"
GOLD_DK = "#8a6a12"
RUST = "#c4532d"
TEXT = "#c9ced4"
MUTED = "#7b828b"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

# ------------------------------------------------------------- pixel font ---
# 5x7 glyphs, one string per row, '#' = on.
G = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", "..#..", ".#..."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    "-": [".....", ".....", ".....", "####.", ".....", ".....", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "@": [".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".####"],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "*": [".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."],
    "#": [".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "<": ["...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."],
    ">": [".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."],
    "(": ["..#..", ".#...", "#....", "#....", "#....", ".#...", "..#.."],
    ")": ["..#..", "...#.", "....#", "....#", "....#", "...#.", "..#.."],
    "%": ["##..#", "##..#", "...#.", "..#..", ".#...", "#..##", "#..##"],
    "·": [".....", ".....", ".....", ".##..", ".##..", ".....", "....."],
}


def text_width(s, scale, gap=1):
    return len(s) * (5 + gap) * scale - gap * scale


def pixel_text(s, x, y, scale, fill, gap=1, extra=""):
    """Render s as merged horizontal runs of rects (keeps the SVG small)."""
    out = []
    cx = x
    for ch in s.upper():
        rows = G[ch]
        for r, row in enumerate(rows):
            c = 0
            while c < 5:
                if row[c] == "#":
                    start = c
                    while c < 5 and row[c] == "#":
                        c += 1
                    out.append(
                        f'<rect x="{cx + start * scale}" y="{y + r * scale}" '
                        f'width="{(c - start) * scale}" height="{scale}"/>'
                    )
                else:
                    c += 1
        cx += (5 + gap) * scale
    return f'<g fill="{fill}"{extra}>' + "".join(out) + "</g>"


# ------------------------------------------------------------- the mask -----
# Original pixel-art metal mask: pointed dome, brow ridges with a centre gem,
# temple spikes, and two long cheek bars over the face (lips and beard show
# through). Only the left half is drawn; it is mirrored, with the right side
# shaded a step darker (light from the left).
#   H hood  h hood edge  D/M/L/W steel dark->white  G gem  E eye slit
#   S skin  R lips  K mouth  B beard  b beard texture
MASK_LEFT = [
 "..............L",
 ".............LW",
 "...........DMLW",
 ".........DMMLWL",
 "........DMMLWLL",
 ".......DMMLLWLM",
 "......DMMLLWLLM",
 ".....DMMLLLWLMM",
 ".....DMMLLLLLMM",
 "....DMMMLLLLMMM",
 "...HDMMLLLLMMDG",
 "..HDMLLWWLLLDGG",
 "..HDMLLLLLLMMDG",
 "..HDDMMMMMMMMDL",
 "LMHDEEEEEEEEDLL",
 ".MHDEEEEEEEEDLL",
 "..HDMEEEEEEEDLL",
 "..HDMMEEEEEDDLL",
 "..HDMLMDLWMDDLL",
 "..HDMLMDLWMDLLM",
 "..HHDMMDLWMDMMM",
 "..HHHDDDLWMDDDD",
 "..HHBBBDLWMDSSS",
 "..hHBBBDLWMDSRR",
 "..hHBbBDLWMDRKK",
 "..hHBBBDLWMDSRR",
 "...hBBbDLWMDBBB",
 "...hHBBDLWMDBbB",
 "....hBBDLWMDBBB",
 ".....hBDLWMDBBb",
 "......hDLWMDhBB",
 ".......DLWMD.hh",
 ".......DLWMD...",
 ".......DDDDD...",
]
_DARKER = {"W": "L", "L": "M"}
MASK = []
for _row in MASK_LEFT:
    _right = "".join(_DARKER.get(ch, ch) for ch in reversed(_row))
    MASK.append(_row + _right)
assert all(len(r) == 30 for r in MASK)
MASK_COLORS = {
    "H": "#1b1e22", "h": "#2c3137", "D": STEEL_DK, "M": STEEL_MD, "L": STEEL_LT,
    "W": "#eef0f2", "G": GOLD, "E": "#050506", "S": "#6e4b34", "R": "#3e2418",
    "K": "#050506", "B": "#0f1012", "b": "#30343a",
}


def mask_svg(x, y, px, eye_glow=True):
    out = []
    for r, row in enumerate(MASK):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            cls = ' class="eye"' if eye_glow and ch == "E" else ""
            out.append(
                f'<rect{cls} x="{x + c * px}" y="{y + r * px}" width="{px}" '
                f'height="{px}" fill="{MASK_COLORS[ch]}"/>'
            )
    return "".join(out)


# --------------------------------------------------------- shared bits ------
def svg_open(w, h, extra_style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" shape-rendering="crispEdges">'
        f"<style>"
        f".flk{{animation:flk 4s steps(1) infinite}}"
        f"@keyframes flk{{0%{{opacity:1}}50%{{opacity:.25}}100%{{opacity:1}}}}"
        f".eye{{animation:eye 6s steps(1) infinite}}"
        f"@keyframes eye{{0%,92%{{fill:#050506}}93%,97%{{fill:{GOLD}}}98%{{fill:#050506}}}}"
        f".blink{{animation:blink 1.1s steps(1) infinite}}"
        f"@keyframes blink{{50%{{opacity:0}}}}"
        f"{extra_style}"
        f"@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}"
        f"</style>"
    )


def write(name, body):
    (OUT / name).write_text(body, encoding="utf-8")
    print(f"wrote assets/{name}  ({len(body) / 1024:.1f} KB)")


# ------------------------------------------------------------- header -------
# Original pixel sky-dragon (Rayquaza-inspired) wrapped through the pipeline.
# The body is rasterised from a spline: each cell is shaded by where it sits along
# the body (plates, seams, gold rings) and across it (lit top, dark belly).
#   O outline  L/M/D green light->dark  Y gold  F red fin  W claw  E eye  K mouth  R tongue
DRAGON_COLORS = {"O": "#07080a", "L": "#6fcf97", "M": "#2e8b5c", "D": "#1a553a",
                 "Y": GOLD, "F": "#d9573f", "W": BONE, "E": GOLD, "K": "#14090a", "R": "#7a2a22"}

DRAGON_HEAD_LEFT = [     # front-facing; left half, mirrored. Bottom-centre joins the neck
    "OO...........",
    "OLO..........",
    "OLLO.........",
    ".OLMO........",
    ".OLMMO......O",
    "..OLMMO....OL",
    "..OLMMMOOOOLY",
    "...OMMMLLLLMY",
    "...OMMMMMMMMY",
    "..OOMOOOMMMMM",
    ".OLOMYYOOMMMM",
    "OLMOMYYEYOMMM",
    ".OOOMMYYYOMMM",
    "...OMMMMMMMMM",
    "....OMMMMMMMM",
    ".....OMMMMOMM",
    ".....OFWFFFFF",
    ".....OFKKKKKK",
    "......OFKRRRR",
    "......OFWFFFF",
    ".......OMMMMM",
    "........OOOOO",
]
DRAGON_HEAD = [row + "".join({"L": "M"}.get(ch, ch) for ch in reversed(row))
               for row in DRAGON_HEAD_LEFT]
DRAGON_TAIL = [          # V fin with red trim; bottom-centre joins the body
    "F.......F",
    "FF.....FF",
    "FMF...FMF",
    ".FMF.FMF.",
    ".FMMFMMF.",
    "..FMMMF..",
    "...OMO...",
]
DRAGON_ARM_L = [         # reaches left, claws out
    "WW.....",
    ".WOOOO.",
    "WOMMMMO",
    ".WODDO.",
    "..OOO..",
]


def _sprite(rows, x, y, c, flip=False):
    out = []
    for r, row in enumerate(rows):
        row = row[::-1] if flip else row
        for q, ch in enumerate(row):
            if ch != ".":
                cls = ' class="eye"' if ch == "E" else ""
                out.append(f'<rect{cls} x="{x + q * c}" y="{y + r * c}" width="{c}" height="{c}" '
                           f'fill="{DRAGON_COLORS[ch]}"/>')
    return "".join(out)


def _spline(points, steps=24):
    """Catmull-Rom through points, returned as a dense polyline."""
    pts = [points[0]] + points + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for s in range(steps):
            u = s / steps
            out.append(tuple(
                0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * u
                       + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u * u
                       + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * u ** 3)
                for k in range(2)))
    out.append(points[-1])
    return out


def dragon(boxes, path, cell=5, radius=21, plate=46):
    """Returns (behind, front) SVG for the dragon body plus its head, arms and tail."""
    c = cell
    poly = _spline(path)
    seg_s = [0.0]
    for a, b in zip(poly, poly[1:]):
        seg_s.append(seg_s[-1] + math.dist(a, b))
    total = seg_s[-1]

    def in_front(x):
        for i, (bx, bw) in enumerate(boxes):
            if bx <= x <= bx + bw:
                left = x < bx + bw / 2
                return left if i % 2 == 0 else not left
        return True

    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    behind, front = [], []
    for gy in range(int((min(ys) - radius - 3 * c) // c), int((max(ys) + radius + c) // c) + 1):
        for gx in range(int((min(xs) - radius) // c), int((max(xs) + radius) // c) + 1):
            px, py = gx * c + c / 2, gy * c + c / 2
            best = None
            for i, (a, b) in enumerate(zip(poly, poly[1:])):
                dx, dy = b[0] - a[0], b[1] - a[1]
                L2 = dx * dx + dy * dy or 1e-9
                u = max(0.0, min(1.0, ((px - a[0]) * dx + (py - a[1]) * dy) / L2))
                qx, qy = a[0] + u * dx, a[1] + u * dy
                d = math.hypot(px - qx, py - qy)
                if best is None or d < best[0]:
                    L = math.sqrt(L2)
                    nx, ny = -dy / L, dx / L          # normal, flipped to point up
                    if ny > 0:
                        nx, ny = -nx, -ny
                    best = (d, seg_s[i] + u * L, (px - qx) * nx + (py - qy) * ny)
            d, s, off = best
            R = radius * min(1.0, 0.35 + s / 70)     # taper toward the tail
            col = None
            k = s % plate
            if d <= R:
                ring = ((k - plate / 2) / (plate * 0.36)) ** 2 + (off / (R * 0.6)) ** 2
                if R - d < c * 0.9 or k < c * 0.6:
                    col = "O"                          # outline and thin plate seams
                elif int(s // plate) % 2 == 1 and abs(ring - 1) < 0.38:
                    col = "Y"                          # gold oval on alternate plates
                elif off > R * 0.4:
                    col = "L"
                elif off < -R * 0.4:
                    col = "D"
                else:
                    col = "M"
            elif off > 0 and 40 < s < total - 30:
                f = s % (plate * 2)                    # swept-back fin on every other seam
                if f < 3 * c and d <= R + (3 * c - f) * 0.9:
                    col = "F"
            if col:
                rect = (f'<rect x="{gx * c}" y="{gy * c}" width="{c}" height="{c}" '
                        f'fill="{DRAGON_COLORS[col]}"/>')
                (front if in_front(px) else behind).append(rect)
    tx, ty = path[0]
    front.append(_sprite(DRAGON_TAIL, round(tx - 4.5 * c), round(ty - 7 * c + 2), c))
    ax, ay = path[-2]                          # arms grow out of the neck
    front.append(_sprite(DRAGON_ARM_L, round(ax - radius - 4 * c), round(ay - 3 * c), c))
    front.append(_sprite(DRAGON_ARM_L, round(ax + radius - c), round(ay - 6 * c), c, flip=True))
    nx, ny = path[-1]
    front.append(_sprite(DRAGON_HEAD, round(nx - 13 * c), round(ny - 19 * c), c))
    return "".join(behind), "".join(front)


def pipeline(x, y):
    """MODEL / POLICY / ACTION, with the dragon wrapped through them."""
    bw, bh, gap = 128, 64, 64
    specs = [
        ("MODEL", "PREDICTS", STEEL, STEEL_MD, "#0f1113", True),
        ("POLICY", "DECIDES", GOLD, GOLD, "#171306", False),
        ("ACTION", "ACTS", BONE, BONE, "#141414", False),
    ]
    boxes = [(x + i * (bw + gap), bw) for i in range(3)]
    (m0, _), (m1, _), (m2, _) = boxes
    top, bot = y - 24, y + bh + 24
    path = [
        (x - 42, y - 6),                       # tail tip (fin sits above)
        (x - 30, y + 40),
        (m0 + bw * 0.25, bot),
        (m0 + bw * 0.75, bot),
        (m1 - gap / 2, y + bh / 2),
        (m1 + bw * 0.25, top),
        (m1 + bw * 0.75, top),
        (m2 - gap / 2, y + bh / 2),
        (m2 + bw * 0.25, bot),
        (m2 + bw * 0.8, bot),
        (m2 + bw + 40, y + bh / 2 + 6),
        (m2 + bw + 56, y - 8),                 # neck top; head sits here
    ]
    behind, front = dragon(boxes, path)
    shapes, labels = [], []
    for (bx, _), (label, cap, edge, ink, fill, dashed) in zip(boxes, specs):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        sw = 3 if label == "POLICY" else 2
        shapes.append(
            f'<rect x="{bx + sw / 2}" y="{y + sw / 2}" width="{bw - sw}" height="{bh - sw}" '
            f'fill="{fill}" stroke="{edge}" stroke-width="{sw}"{dash}/>'
        )
        labels.append(pixel_text(label, bx + (bw - text_width(label, 3)) // 2, y + 13, 3, ink))
        labels.append(pixel_text(cap, bx + (bw - text_width(cap, 2)) // 2, y + 42, 2, MUTED))
    return behind + "".join(shapes) + front + "".join(labels)


def build_header():
    W, H = 1000, 306
    s = [svg_open(W, H)]
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # name
    s.append(pixel_text("SAYED SAJID ALI", 40, 36, 5, BONE))
    s.append(f'<rect class="blink" x="{40 + text_width("SAYED SAJID ALI", 5) + 12}" y="36" width="20" height="35" fill="{GOLD}"/>')

    s.append(pipeline(82, 136))

    # mask, with a plate behind it
    px = 7
    mw, mh = len(MASK[0]) * px, len(MASK) * px
    mx, my = W - mw - 40, (H - mh) // 2
    s.append(f'<rect x="{mx - 12}" y="{my - 12}" width="{mw + 24}" height="{mh + 24}" fill="{PANEL}" stroke="{EDGE}"/>')
    s.append(mask_svg(mx, my, px))

    sub = "SWE INTERN @ TELIT CINTERION / BACKEND & APPLIED AI"
    s.append(pixel_text(sub, 40, 270, 2, STEEL_LT))
    s.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{EDGE}"/>')
    s.append("</svg>")
    write("header.svg", "".join(s))


# ---------------------------------------------------------- about panel -----
ABOUT = [
    ("BEHIND THE MASK",
     "I'm Sajid, a CS grad (KIIT '26) and software engineer in Bengaluru. I build AI "
     "systems where the model never gets the final word: its predictions feed a "
     "deterministic layer that decides and acts safely, and the AI explains the reasoning "
     "on top. Co-author of an IEEE paper on ensemble learning."),
    ("CURRENTLY",
     "Software Engineer Intern at Telit Cinterion (Sep 2026 - present), working on "
     "backend and applied AI. After hours: Sentinel (cost-weighted fraud decisioning) "
     "and Paygate (a payment-auth state machine)."),
    ("THE CODE",
     "Models predict. Policy decides. The ML stays behind a mask of guardrails, state "
     "machines and hash-chained audit trails, and a model's confidence has to come with "
     "a reason: Grad-CAM, reason codes, evidence."),
    ("NEXT",
     "ML engineering, MLOps and LLM applications that hold up in real workflows. "
     "Open to roles in ML Engineering and Agentic AI."),
]


def build_about():
    W = 1000
    pad = 40
    heading_scale = 4
    line_h = 25
    wrap = 90
    blocks = []
    y = 44
    for i, (title, body) in enumerate(ABOUT):
        lines = textwrap.wrap(body, wrap)
        blocks.append((title, lines, y))
        y += 7 * heading_scale + 22 + len(lines) * line_h + 34
    H = y - 6
    s = [svg_open(W, H)]
    s.append(f'<rect width="{W}" height="{H}" fill="{PANEL}"/>')
    # faint scanlines for the CRT feel
    s.append(
        '<defs><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
        f'<rect width="4" height="1" fill="#ffffff" opacity=".018"/></pattern></defs>'
        f'<rect width="{W}" height="{H}" fill="url(#scan)"/>'
    )
    for i, (title, lines, by) in enumerate(blocks):
        s.append(pixel_text(title, pad, by, heading_scale, BONE))
        ty = by + 7 * heading_scale + 30
        for j, ln in enumerate(lines):
            s.append(
                f'<text x="{pad}" y="{ty + j * line_h}" fill="{TEXT}" font-family="{MONO}" '
                f'font-size="16.5" xml:space="preserve">{escape(ln)}</text>'
            )
    s.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{EDGE}"/>')
    s.append("</svg>")
    write("about.svg", "".join(s))


# ------------------------------------------------------ section headers -----
def build_section(name, label, seed):
    W, H = 1000, 64
    s = [svg_open(W, H)]
    s.append(f'<rect width="{W}" height="{H}" fill="{PANEL}"/>')
    s.append(pixel_text(label, 40, 18, 4, BONE))
    s.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{EDGE}"/>')
    s.append("</svg>")
    write(f"section-{name}.svg", "".join(s))


# -------------------------------------------------------- contact tiles -----
# Icon paths: Simple Icons (CC0).
ICONS = {
    "linkedin": "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
    "gmail": "M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z",
    "instagram": "M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.1565 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077",
    "github": "M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.22.405 1.46-.405 2.99-.405 4.46 0 2.21-.727 3.21-.405 3.21-.405.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.37-12-12-12",
}


def build_tile(key, label):
    W, H = 200, 110
    s = [svg_open(W, H, ".t:hover{fill:#d4a017}")]
    s.append(f'<rect width="{W}" height="{H}" fill="{PANEL}"/>')
    s.append(pixel_text(label, (W - text_width(label, 2)) // 2, 16, 2, STEEL_LT))
    s.append(f'<rect x="20" y="40" width="{W - 40}" height="1" fill="{EDGE}"/>')
    s.append(f'<g transform="translate({W // 2 - 18},55) scale(1.5)"><path d="{ICONS[key]}" fill="{GOLD}"/></g>')
    s.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{EDGE}"/>')
    s.append("</svg>")
    write(f"tile-{key}.svg", "".join(s))


# -------------------------------------------------------- project cards -----
PROJECTS = [
    ("sentinel", "01", "SENTINEL",
     "Return-abuse detection with cost-weighted decisioning. Two calibrated models, "
     "one deterministic policy engine, guardrails, and a hash-chained audit trail.",
     "PR-AUC 0.814 WITH GRAPH FEATURES",
     ["PYTHON", "GRAPH ML", "CALIBRATION"]),
    ("paygate", "02", "PAYGATE",
     "Card authorization gateway built around one pure state machine, for when the "
     "issuer goes silent mid-auth. Idempotent retries, reconciliation, property tests.",
     "APPLY(STATE, EVENT) -> STATE",
     ["PYTHON", "HYPOTHESIS", "FSM"]),
    ("brain-stroke-agent", "03", "STROKE AGENT",
     "3-CNN ensemble decides by majority vote on CT scans; Llama 3.3 70B via Groq "
     "writes the clinical report. Grad-CAM evidence for every prediction.",
     "< 15S END-TO-END ON CPU",
     ["PYTORCH", "GRAD-CAM", "LLAMA 3.3"]),
    ("Lunar-Navigation-System", "04", "LUNAR NAV",
     "SRResNet super-resolution + U-Net hazard segmentation. A physics-based A* "
     "planner vetoes unsafe paths. Real-time 3D command dashboard.",
     "92% ACCURACY, GPS-DENIED",
     ["PYTORCH", "U-NET", "A* SEARCH"]),
    ("cricket-score-predictor", "05", "IPL PREDICTOR",
     "IPL score prediction with ensemble learning (XGBoost, Random Forest) + SVM, "
     "validated with EDA and KNN checks on unseen data.",
     "PUBLISHED / IEEE ASSIC 2025",
     ["XGBOOST", "SKLEARN", "RESEARCH"]),
]


def build_card(slug, num, title, desc, metric, tags):
    W, H = 490, 250
    s = [svg_open(W, H)]
    s.append(f'<rect width="{W}" height="{H}" fill="{PANEL}"/>')
    s.append(f'<rect x="0" y="0" width="{W}" height="4" fill="{STEEL_DK}"/>')
    s.append(f'<rect x="0" y="0" width="{24 + len(slug) * 3}" height="4" fill="{GOLD}"/>')
    s.append(pixel_text(num, 28, 28, 2, GOLD))
    s.append(pixel_text(title, 28, 50, 4, BONE))
    for j, ln in enumerate(textwrap.wrap(desc, 54)):
        s.append(
            f'<text x="28" y="{126 + j * 20}" fill="{TEXT}" font-family="{MONO}" '
            f'font-size="13" xml:space="preserve">{escape(ln)}</text>'
        )
    s.append(pixel_text("> " + metric, 28, 196, 2, GOLD))
    tx = 28
    for t in tags:
        tw = len(t) * 7.2 + 18
        s.append(f'<rect x="{tx}" y="216" width="{tw:.0f}" height="20" fill="none" stroke="{STEEL}"/>')
        s.append(
            f'<text x="{tx + tw / 2:.0f}" y="230" text-anchor="middle" fill="{STEEL_LT}" '
            f'font-family="{MONO}" font-size="11" letter-spacing="1">{escape(t)}</text>'
        )
        tx += tw + 8
    s.append(
        f'<text x="{W - 28}" y="230" text-anchor="end" fill="{MUTED}" font-family="{MONO}" '
        f'font-size="11" letter-spacing="1">VIEW REPO &#8594;</text>'
    )
    s.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{EDGE}"/>')
    s.append("</svg>")
    write(f"card-{slug.lower()}.svg", "".join(s))


# --------------------------------------------------------------- footer -----
def build_footer():
    W, H = 1000, 120
    s = [svg_open(W, H)]
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    px = 3
    mw = len(MASK[0]) * px
    s.append(mask_svg(40, (H - len(MASK) * px) // 2, px, eye_glow=True))
    s.append(pixel_text("ALL CAPS. NO HALLUCINATIONS.", 40 + mw + 28, 38, 3, BONE))
    s.append(pixel_text("SAJID1108 / BUILT BEHIND THE MASK", 40 + mw + 28, 76, 2, MUTED))
    s.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{EDGE}"/>')
    s.append("</svg>")
    write("footer.svg", "".join(s))


if __name__ == "__main__":
    build_header()
    build_about()
    for name, label, seed in [
        ("contact", "COMMS", 7),
        ("work", "SELECTED WORK", 11),
        ("arsenal", "ARSENAL", 13),
        ("activity", "ACTIVITY", 17),
    ]:
        build_section(name, label, seed)
    for key, label in [("linkedin", "LINKEDIN"), ("gmail", "EMAIL"),
                       ("instagram", "INSTAGRAM"), ("github", "GITHUB")]:
        build_tile(key, label)
    for p in PROJECTS:
        build_card(*p)
    build_footer()
