"""Scene primitives + theme for the S.D. Public School maths-model deck.

One scene description feeds two consumers:
  * render.py -> PIL preview (design QA, catches overflow)
  * emit.py   -> native DrawingML PPTX (fully editable in PowerPoint)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# ----------------------------------------------------------------- canvas
W, H = 13.3333, 7.5          # inches, 16:9
PX = 144.0                    # preview pixels per inch -> 1920x1080

# ----------------------------------------------------------------- palette
INK    = "0F1B2D"
INK2   = "33415A"
MUT    = "6B7A90"
FAINT  = "9AA8BA"
BG     = "FFFFFF"
PANEL  = "F4F7FC"
PANEL2 = "EAF0F9"
LINE   = "DCE4EF"
WHITE  = "FFFFFF"

BLUE   = "1D4ED8"
BLUE_D = "12327F"
BLUE_L = "DCE7FF"
YELLOW = "F7C531"
YELLOW_D = "B4801A"
YELLOW_L = "FFF3D2"
PINK   = "E8407E"
PINK_L = "FFE2EC"
CYAN   = "0EA5B7"

VIOLET = "6D3BD6"
VIOLET_D = "2B1466"
VIOLET_L = "E9E2FF"
ROSE   = "E11D48"
ROSE_L = "FFE4E9"
GOLD   = "C98A12"
GOLD_L = "FDF0D0"
TEAL   = "0F766E"

NAVY_BG = "0C1730"

# ----------------------------------------------------------------- fonts
FONT = "Segoe UI"
FONT_D = "Segoe UI"
FONT_M = "Cambria Math"      # symbols: union, intersection, element-of

# ----------------------------------------------------------------- scene
@dataclass
class Run:
    text: str
    size: float = 18
    bold: bool = False
    color: str = INK
    font: str = FONT
    italic: bool = False
    spacing: float = 0.0          # letter spacing, pt


@dataclass
class Para:
    runs: list[Run] = field(default_factory=list)
    align: str = "l"              # l / c / r
    space_before: float = 0.0     # pt
    space_after: float = 0.0      # pt
    line: float = 1.0             # multiple


@dataclass
class Rect:
    x: float; y: float; w: float; h: float
    fill: Optional[str] = None
    line: Optional[str] = None
    lw: float = 1.0
    radius: float = 0.0           # inches
    dash: Optional[str] = None
    shadow: bool = False
    opacity: float = 1.0


@dataclass
class Oval:
    x: float; y: float; w: float; h: float
    fill: Optional[str] = None
    line: Optional[str] = None
    lw: float = 1.0
    dash: Optional[str] = None
    shadow: bool = False
    opacity: float = 1.0


@dataclass
class Poly:
    pts: list[tuple[float, float]]
    fill: Optional[str] = None
    line: Optional[str] = None
    lw: float = 1.0
    dash: Optional[str] = None
    close: bool = True
    shadow: bool = False
    opacity: float = 1.0


@dataclass
class Line:
    x1: float; y1: float; x2: float; y2: float
    color: str = INK
    lw: float = 1.0
    dash: Optional[str] = None
    arrow: bool = False
    opacity: float = 1.0


@dataclass
class Text:
    x: float; y: float; w: float; h: float
    paras: list[Para]
    anchor: str = "t"             # t / m / b
    margin: float = 0.0
    name: str = ""


@dataclass
class Image:
    path: str
    x: float; y: float; w: float; h: float
    opacity: float = 1.0
    radius: float = 0.0


@dataclass
class Slide:
    items: list = field(default_factory=list)
    bg: str = BG
    notes: str = ""
    seconds: Optional[int] = None   # auto-advance

    def add(self, *items):
        for it in items:
            if isinstance(it, (list, tuple)):
                self.items.extend(it)
            else:
                self.items.append(it)
        return self


# ----------------------------------------------------------------- helpers
def T(text, size=18, bold=False, color=INK, font=FONT, italic=False, spacing=0.0):
    return Run(text, size, bold, color, font, italic, spacing)


def P(*runs, align="l", before=0.0, after=0.0, line=1.0):
    flat = []
    for r in runs:
        if isinstance(r, str):
            flat.append(Run(r))
        elif isinstance(r, (list, tuple)):
            flat.extend(r)
        else:
            flat.append(r)
    return Para(flat, align, before, after, line)


def L(*lines, **kw):
    """A stack of single-run paragraphs sharing one style."""
    size = kw.pop("size", 18)
    color = kw.pop("color", INK)
    bold = kw.pop("bold", False)
    font = kw.pop("font", FONT)
    align = kw.pop("align", "l")
    after = kw.pop("after", 0.0)
    line = kw.pop("line", 1.0)
    return [P(T(s, size, bold, color, font), align=align, after=after, line=line) for s in lines]


def text(x, y, w, h, paras, anchor="t", margin=0.0, name=""):
    if isinstance(paras, Para):
        paras = [paras]
    return Text(x, y, w, h, paras, anchor, margin, name)


# --- composite pieces -------------------------------------------------------
def pill(x, y, text_s, *, h=0.34, padx=0.20, size=11, color=WHITE, bg=BLUE,
         bold=True, spacing=1.2, font=FONT, radius=None):
    """Auto-width pill: width estimated from the label length."""
    est = padx * 2 + len(text_s) * size * 0.0105 + len(text_s) * spacing * 0.0139
    w = max(est, h * 1.05)
    rr = h / 2 if radius is None else radius
    return [
        Rect(x, y, w, h, fill=bg, radius=rr),
        text(x, y + 0.005, w, h - 0.01,
             [P(T(text_s, size, bold, color, font, spacing=spacing), align="c")],
             anchor="m"),
    ]


def rule(x, y, w, color=LINE, lw=1.0):
    return Line(x, y, x + w, y, color=color, lw=lw)


def dashed_rule(x, y, w, color=LINE, lw=1.0):
    return Line(x, y, x + w, y, color=color, lw=lw, dash="dash")


def arrow(x1, y1, x2, y2, color=INK, lw=1.6, dash=None):
    return Line(x1, y1, x2, y2, color=color, lw=lw, dash=dash, arrow=True)


def photo_frame(x, y, w, h, *, radius=0.10, label="Drop your photo here",
                sub="Insert ▸ Pictures", tint=PANEL, edge=LINE, accent=BLUE,
                size=15):
    """An obvious, tidy photo placeholder (frame + icon + hint)."""
    cx, cy = x + w / 2, y + h / 2
    icon = 0.34
    items = [
        Rect(x, y, w, h, fill=tint, radius=radius),
        Rect(x, y, w, h, fill=None, line=edge, lw=1.4, radius=radius, dash="dash"),
        # little camera frame
        Rect(cx - icon, cy - icon * 0.78 - 0.12, icon * 2, icon * 1.56,
             fill=WHITE, line=accent, lw=1.8, radius=0.08),
        Oval(cx - icon * 0.42, cy - icon * 0.30 - 0.12, icon * 0.84, icon * 0.84,
             line=accent, lw=1.8),
    ]
    items.append(text(x + 0.1, cy + icon * 0.62, w - 0.2, 0.34,
                      [P(T(label, size, True, INK2), align="c")], anchor="t"))
    items.append(text(x + 0.1, cy + icon * 0.62 + 0.30, w - 0.2, 0.28,
                      [P(T(sub, max(size - 3, 9), False, FAINT), align="c")], anchor="t"))
    return items


def big_number(x, y, w, num, *, size=150, color=WHITE, bold=True):
    return text(x, y, w, 1.9, [P(T(num, size, bold, color, spacing=-2), align="l")], anchor="t")


def lens_points(c1, r1, c2, r2, n=28):
    """Outline of the overlap of two circles (the Venn 'lens')."""
    import math
    x1, y1 = c1
    x2, y2 = c2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    a = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    h = math.sqrt(max(r1 * r1 - a * a, 0.0))
    bx, by = x1 + a * ux, y1 + a * uy
    px, py = -uy, ux
    p1 = (bx + h * px, by + h * py)
    p2 = (bx - h * px, by - h * py)

    def arc(c, r, s, e, steps):
        t0 = math.atan2(s[1] - c[1], s[0] - c[0])
        t1 = math.atan2(e[1] - c[1], e[0] - c[0])
        dt = (t1 - t0 + math.pi) % (2 * math.pi) - math.pi
        return [(c[0] + r * math.cos(t0 + dt * i / steps),
                 c[1] + r * math.sin(t0 + dt * i / steps)) for i in range(steps + 1)]

    return arc(c1, r1, p1, p2, n) + arc(c2, r2, p2, p1, n)[1:]
