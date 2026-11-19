"""Full deck for S.D. Public School — two maths working models (Class XI).

25 slides, fully editable native PowerPoint shapes.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from kit import *  # noqa

A = Path(__file__).parent.parent / "assets"


def M(expr: str) -> str:
    """Space out set symbols so PowerPoint's math font renders them cleanly."""
    import re
    expr = re.sub(r"(?<![A-Za-z]) ?([∪∩⊆∈∉]) ?(?![A-Za-z])", r" \1 ", expr)
    expr = expr.replace("\\ ", " ").replace("  ", " ")
    return expr
SCHOOL = "S.D. PUBLIC SCHOOL"
TAG = "MATHS EXHIBITION 2025–26"

# ------------------------------------------------------------------ chrome
def footer(num, label):
    return [
        rule(0.85, 6.93, 4.2, LINE, 0.9),
        text(0.85, 7.03, 7.2, 0.3, [P(T(f"{SCHOOL}   ·   {label}", 9.5, True, FAINT, spacing=1.1))]),
        text(10.6, 7.03, 1.9, 0.3, [P(T(f"{num:02d}", 9.5, True, FAINT, spacing=1.0), align="r")]),
    ]


def section_head(tag, title, sub, accent, num, label):
    return [
        text(0.85, 0.52, 8.6, 0.3, [P(T(tag, 10.5, True, accent, spacing=2.0))]),
        text(0.85, 0.80, 11.6, 0.85, [P(T(title, 37, True, INK, spacing=-0.6))]),
        text(0.85, 1.60, 10.8, 0.5, [P(T(sub, 14.5, False, MUT))]),
        Rect(0.85, 2.16, 0.62, 0.055, fill=accent, radius=0.027),
        *footer(num, label),
    ]


def frame_photo(path, x, y, w, h, *, radius=0.14, border=WHITE, lw=3.5):
    """Photo with a clean white border + soft shadow built as shapes behind it."""
    return [
        Rect(x - 0.07, y - 0.07, w + 0.14, h + 0.14, fill=border, radius=radius + 0.04, shadow=True),
        Image(path, x, y, w, h),
    ]


def stat_tile(x, y, w, big, label, accent, tint, size=40, foot=None):
    items = [
        Rect(x, y, w, 0.80, fill=tint, radius=0.13),
        text(x + 0.20, y + 0.04, 0.76, 0.72, [P(T(big, size, True, accent, spacing=-1))], anchor="m"),
        text(x + 0.98 if w > 2.2 else x + 0.22, y + (0.16 if w > 2.2 else 0),
             w - 1.10 if w > 2.2 else w - 0.4, 0.72,
             [P(T(label, 10, True, INK2))],
             anchor="m" if w > 2.2 else "t"),
    ]
    if foot:
        items.append(text(x + 0.24, y + 1.16, w - 0.4, 0.3, [P(T(foot, 9, False, MUT))]))
    return items


def material_icon(i, x, y, d, acc):
    """A small drawn glyph per material, so the tiles are not blank blobs."""
    items = [Oval(x - 0.14, y - 0.14, d + 0.28, d + 0.28, fill=acc, opacity=0.10)]
    cx, cy = x + d / 2, y + d / 2
    if i == 0:      # foam board
        items += [Rect(x + 0.04, y + 0.02, d - 0.08, d - 0.04, fill=WHITE, line=acc, lw=1.6, radius=0.02),
                  Rect(x + 0.04, y + d - 0.16, d - 0.08, 0.12, fill=acc, opacity=0.35, radius=0.01)]
    elif i == 1:    # chart paper
        items += [Rect(x + 0.02, y + 0.02, d - 0.10, d - 0.12, fill=WHITE, line=acc, lw=1.4, radius=0.02),
                  Rect(x + 0.08, y + 0.08, d - 0.10, d - 0.12, fill=acc, opacity=0.30, radius=0.02)]
    elif i == 2:    # syringe
        items += [Rect(x + 0.02, cy - 0.06, d - 0.20, 0.12, fill=WHITE, line=acc, lw=1.4, radius=0.02),
                  Rect(x + d - 0.20, cy - 0.09, 0.05, 0.18, fill=acc, radius=0.01),
                  Line(x + d - 0.15, cy, x + d - 0.02, cy, color=acc, lw=1.6)]
    elif i == 3:    # level tube / rail
        items += [Rect(x + 0.02, cy - 0.04, d - 0.04, 0.08, fill=WHITE, line=acc, lw=1.2, radius=0.04),
                  Oval(x + d / 2 - 0.05, cy - 0.05, 0.10, 0.10, fill=acc)]
    elif i == 4:    # glue gun
        items += [Rect(x + 0.04, cy - 0.13, d - 0.22, 0.20, fill=WHITE, line=acc, lw=1.4, radius=0.05),
                  Rect(x + 0.02, cy + 0.06, 0.10, 0.16, fill=acc, radius=0.02),
                  Line(x + d - 0.18, cy - 0.03, x + d - 0.02, cy - 0.03, color=acc, lw=2.4)]
    elif i == 5:    # anabond tube
        items += [Poly([(cx - 0.13, cy - 0.16), (cx + 0.13, cy - 0.16), (cx + 0.13, cy + 0.10),
                        (cx, cy + 0.18), (cx - 0.13, cy + 0.10)], fill=WHITE, line=acc, lw=1.4),
                  Rect(cx - 0.03, cy - 0.22, 0.06, 0.07, fill=acc, radius=0.01)]
    elif i == 6:    # cutter
        items += [Poly([(x + 0.04, y + 0.06), (x + d - 0.06, y + d - 0.16), (x + d - 0.16, y + d - 0.06),
                        (x + 0.02, y + 0.16)], fill=WHITE, line=acc, lw=1.4)]
    elif i == 7:    # paint brush
        items += [Rect(x + d / 2 - 0.03, y + 0.02, 0.07, d * 0.5, fill=WHITE, line=acc, lw=1.2, radius=0.02),
                  Poly([(cx - 0.07, cy + 0.06), (cx + 0.07, cy + 0.06), (cx + 0.03, cy + 0.22),
                        (cx - 0.03, cy + 0.22)], fill=acc, opacity=0.75)]
    else:           # thread
        items += [Oval(x + 0.03, cy - 0.13, 0.26, 0.26, fill=None, line=acc, lw=1.5),
                  Line(x + 0.29, cy, x + d - 0.02, cy - 0.06, color=acc, lw=1.2, dash="dash")]
    return items


def check(x, y, accent=BLUE, size=0.28):
    return [Oval(x, y, size, size, fill=accent), text(x, y - 0.005, size, size,
            [P(T("✓", size * 34, True, WHITE), align="c")], anchor="m")]


def bullet_block(x, y, w, rows, accent, size=13.5, gap=0.60, bold_head=True):
    items = []
    cy = y
    for head, body in rows:
        items.append(Oval(x, cy + 0.075, 0.13, 0.13, fill=accent))
        items.append(text(x + 0.30, cy, w - 0.30, 0.30, [P(T(head, size + 1, bold_head, INK))]))
        if body:
            items.append(text(x + 0.30, cy + 0.28, w - 0.30, gap - 0.26, [P(T(body, size - 1, False, MUT))]))
        cy += gap
    return items


# ========================================================================
# 01 — COVER
# ========================================================================
def s01():
    s = Slide(bg=NAVY_BG)
    s.add(
        Rect(0, 0, 13.3333, 7.5, fill=NAVY_BG),
        # soft colour fields
        Oval(-1.6, 3.1, 8.4, 8.4, fill="12306B", opacity=0.75),
        Oval(7.2, -3.3, 9.2, 9.2, fill="2A1250", opacity=0.55),
        Oval(11.5, 1.4, 3.0, 3.0, fill=BLUE, opacity=0.14),
        Oval(6.4, 4.6, 2.6, 2.6, fill=PINK, opacity=0.13),
        # title block
        *pill(0.85, 0.95, "MATHS  ·  WORKING MODELS", h=0.36, size=11, bg=BLUE, color=WHITE),
        text(0.85, 1.52, 8.4, 1.9, [P(T("Two Models.", 54, True, WHITE, spacing=-1.2)),
                                    P(T("One Idea.", 54, True, WHITE, spacing=-1.2))]),
        text(0.85, 3.34, 7.9, 0.95,
             [P(T("Sets — Union & Intersection", 20, True, YELLOW)),
              P(T("Conic Sections — a double cone cut by a plane", 18, False, "BBD0EE"),
                before=6)]),
        Line(0.85, 4.66, 3.05, 4.66, color=BLUE, lw=2.2),
        text(0.85, 4.86, 8.2, 1.0,
             [P(T("S.D. PUBLIC SCHOOL", 15, True, WHITE, spacing=2.6)),
              P(T("Prepared by Team XI  ·  11 members  ·  Session 2025–26", 13, False, "9DBBE6"),
                before=7)]),
        text(0.85, 6.55, 7.0, 0.4,
             [P(T("MADE BY STUDENTS, EXPLAINED BY STUDENTS", 9.5, True, "6E8BC4", spacing=2.2))]),
    )
    # right: interlocking circles motif
    s.add(
        Oval(9.30, 1.55, 3.05, 3.05, fill=None, line=YELLOW, lw=2.6),
        Oval(10.55, 1.55, 3.05, 3.05, fill=None, line=PINK, lw=2.6),
        Oval(9.30, 1.55, 3.05, 3.05, fill=YELLOW, opacity=0.10),
        Oval(10.55, 1.55, 3.05, 3.05, fill=PINK, opacity=0.10),
    )
    s.add(text(11.9, 3.55, 0.9, 0.5, [P(T("∩", 26, True, WHITE, font=FONT_M), align="c")]))
    # cone miniature
    s.add(Poly([(11.05, 5.05), (11.95, 4.18), (12.32, 4.46), (12.42, 5.05)], fill="243A6B", line="48619C", lw=1.1))
    s.add(Poly([(12.42, 5.05), (12.32, 5.64), (11.95, 5.92), (11.05, 5.05)], fill="2E4880", line="48619C", lw=1.1))
    s.add(Line(10.55, 4.30, 12.85, 5.72, color=VIOLET_L, lw=2.0))
    s.add(text(10.55, 6.02, 2.4, 0.3, [P(T("circle · ellipse · parabola · hyperbola", 8.5, False, "7E97C4"), align="c")]))
    return s


# ========================================================================
# 02 — WHY THESE MODELS
# ========================================================================
def s02():
    s = Slide(bg=BG)
    s.add(*section_head("BEFORE WE BEGIN", "Why these two models?",
                        "Both are Class XI ideas that are easy to memorise and hard to picture. We turned both into things you can hold.",
                        BLUE, 2, "INTRODUCTION"))
    s.add(
        Rect(0.85, 2.62, 6.05, 3.18, fill=PANEL, radius=0.18),
        Rect(7.28, 2.62, 5.20, 3.18, fill=PANEL, radius=0.18),
        *pill(1.15, 2.92, "MODEL 01", h=0.30, size=9.5, bg=BLUE),
        text(1.15, 3.36, 5.4, 0.5, [P(T("Sets", 27, True, INK))]),
        text(1.15, 3.86, 5.4, 0.6, [P(T("Union & Intersection", 14, True, BLUE))]),
        text(1.15, 4.36, 5.35, 1.6,
             [P(T("A textbook Venn diagram sits flat on the page. Ours moves — the two circles slide apart and back "
                  "together, so a visitor sees the intersection appear and disappear.", 13, False, INK2), line=1.32)]),
        *pill(7.58, 2.92, "MODEL 02", h=0.30, size=9.5, bg=VIOLET),
        text(7.58, 3.36, 4.4, 0.5, [P(T("Conic Sections", 27, True, INK))]),
        text(7.58, 3.86, 4.6, 0.6, [P(T("A plane cutting a cone", 14, True, VIOLET))]),
        text(7.58, 4.36, 4.55, 1.6,
             [P(T("Circle, ellipse, parabola and hyperbola look like four unrelated formulas until one moving plane "
                  "produces all four from the same cone.", 13, False, INK2), line=1.32)]),
    )
    s.add(
        *stat_tile(0.85, 6.06, 2.72, "2", "working models", BLUE, BLUE_L, 28),
        *stat_tile(3.71, 6.06, 2.72, "11", "team members", PINK, PINK_L, 28),
        *stat_tile(6.57, 6.06, 2.72, "4", "conic sections", VIOLET, VIOLET_L, 28),
        *stat_tile(9.43, 6.06, 3.05, "1", "shared display table", TEAL, "D9F2EF", 28),
    )
    return s


# ========================================================================
# 03 — THE TEAM (11 members)
# ========================================================================
def avatar(x, y, d, accent, initials, ring=WHITE):
    return [
        Oval(x - 0.05, y - 0.05, d + 0.10, d + 0.10, fill=ring),
        Oval(x, y, d, d, fill=accent),
        text(x, y, d, d, [P(T(initials, 17, True, WHITE), align="c")], anchor="m"),
    ]


def member_card(x, y, w, h, name, role, accent, tint, tag, initials):
    return [
        Rect(x, y, w, h, fill=WHITE, radius=0.14, line=LINE, lw=1.0, shadow=True),
        Rect(x, y, w, 0.10, fill=accent, radius=0.04),
        *avatar(x + w / 2 - 0.46, y + 0.22, 0.92, accent, initials),
        text(x + 0.06, y + 1.26, w - 0.12, 0.32, [P(T(name, 11.5, True, INK), align="c")]),
        text(x + 0.08, y + 1.56, w - 0.16, 0.34, [P(T(role, 8.6, False, MUT), align="c"), ], ),
        text(x + 0.06, y + h - 0.34, w - 0.12, 0.26,
             [P(T(tag, 7.5, True, accent, spacing=0.8), align="c")]),
    ]


def s03():
    s = Slide(bg=BG)
    s.add(*section_head("OUR TEAM", "Eleven of us, three teams",
                        "Three members built Model 01, three built Model 02, and five handled the work that made both projects presentable.",
                        INK, 3, "TEAM"))
    # legend
    leg = [("MODEL 01 · SETS · 3 MEMBERS", BLUE), ("MODEL 02 · CONICS · 3", VIOLET), ("COMMON WORK · 5", TEAL)]
    lx = 0.85
    for label, col in leg:
        wl = 0.42 + len(label) * 0.0915
        s.add(Rect(lx, 2.325, wl, 0.28, fill=col, radius=0.14),
              text(lx, 2.33, wl, 0.27, [P(T(label, 7.8, True, WHITE, spacing=0.9), align="c")], anchor="m"))
        lx += wl + 0.16

    w, h, gap = 1.835, 2.12, 0.098
    y1 = 2.66
    y2 = 4.90
    x0 = 0.85
    teams = [
        ("Member 1", "Design & structure", BLUE, BLUE_L, "MODEL 01", "M1"),
        ("Member 2", "Cutting & assembly", BLUE, BLUE_L, "MODEL 01", "M2"),
        ("Member 3", "Mechanism & testing", BLUE, BLUE_L, "MODEL 01", "M3"),
        ("Member 4", "Cone construction", VIOLET, VIOLET_L, "MODEL 02", "M4"),
        ("Member 5", "Plane & syringe drive", VIOLET, VIOLET_L, "MODEL 02", "M5"),
        ("Member 6", "Sections & finishing", VIOLET, VIOLET_L, "MODEL 02", "M6"),
        ("Member 7", "Materials & purchase", TEAL, "D9F2EF", "COMMON", "M7"),
        ("Member 8", "Decoration & display", TEAL, "D9F2EF", "COMMON", "M8"),
        ("Member 9", "Photos & documentation", TEAL, "D9F2EF", "COMMON", "M9"),
        ("Member 10", "Explaining to visitors", TEAL, "D9F2EF", "COMMON", "M10"),
        ("Member 11", "Team lead & records", TEAL, "D9F2EF", "COMMON", "M11"),
    ]
    for i, (nm, role, acc, tint, tag, ini) in enumerate(teams[:6]):
        x = x0 + i * (w + gap)
        s.add(*member_card(x, y1, w, h, nm, role, acc, tint, tag, ini))
    for i, (nm, role, acc, tint, tag, ini) in enumerate(teams[6:]):
        x = x0 + (i + 0.5) * (w + gap)
        s.add(*member_card(x, y2, w, h, nm, role, acc, tint, tag, ini))
    return s


# ========================================================================
# 04 — PROJECT 01 DIVIDER
# ========================================================================
def s04():
    s = Slide(bg=BLUE_D)
    s.add(
        Oval(8.6, -2.2, 7.4, 7.4, fill="1B4AA8", opacity=0.55),
        Oval(-2.0, 4.2, 6.4, 6.4, fill="1B4AA8", opacity=0.40),
        text(0.85, 1.10, 6.0, 0.4, [P(T("PROJECT 01  ·  SET THEORY", 12, True, YELLOW, spacing=2.6))]),
        text(0.85, 1.62, 7.2, 2.3, [P(T("Sets", 76, True, WHITE, spacing=-2)),
                                     P(T("Union & Intersection", 34, True, YELLOW))]),
        text(0.85, 4.20, 6.6, 1.4,
             [P(T("A working model that makes the intersection actually appear — then disappear again.",
                  15, False, "C9DBF8"), line=1.4)]),
        *pill(0.85, 5.70, "CLASS XI  ·  MATHEMATICS", h=0.34, size=10, bg=WHITE, color=BLUE_D),
        *pill(4.62, 5.70, "CHAPTER 1", h=0.34, size=10, bg="2A5CB8", color=WHITE),
        text(0.85, 6.72, 6.0, 0.3, [P(T("S.D. PUBLIC SCHOOL  ·  MATHS EXHIBITION 2025–26", 9, True, "7C9BD6", spacing=1.8))]),
        # venn hero
        Image(str(A / "sets_hero.png"), 7.55, 1.55, 5.45, 3.96),
    )
    return s


# ========================================================================
# 05 — WHAT IT IS
# ========================================================================
def s05():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 01   ·   WHAT IT IS", "One board, two circles, one moving part",
                        "Set theory is about belonging. This model shows belonging as something you can watch change.",
                        BLUE, 5, "PROJECT 01 · SETS"))
    # left: big venn diagram (movable story)
    s.add(
        Rect(0.85, 2.55, 6.25, 4.10, fill=PANEL, radius=0.18),
        Oval(1.55, 3.28, 2.62, 2.62, fill=YELLOW_L, line=YELLOW, lw=2.4),
        Oval(3.32, 3.28, 2.62, 2.62, fill=PINK_L, line=PINK, lw=2.4),
        Poly(lens_points((2.86, 4.59), 1.31, (4.63, 4.59), 1.31), fill=WHITE, line=GOLD, lw=1.4),
        text(1.72, 2.86, 1.3, 0.3, [P(T("SET A", 10.5, True, YELLOW_D, spacing=1.6))]),
        text(4.55, 2.86, 1.4, 0.3, [P(T("SET B", 10.5, True, PINK, spacing=1.6))]),
        text(3.06, 4.24, 0.62, 0.4,
             [P(T("A ∩ B", 12.5, True, GOLD, font=FONT_M), align="c")]),
        text(1.28, 6.02, 1.9, 0.3, [P(T("A − B", 10.5, True, YELLOW_D))]),
        text(4.82, 6.02, 1.6, 0.3, [P(T("B − A", 10.5, True, PINK))]),
        text(5.88, 4.36, 0.66, 0.3, [P(T("slide", 9, True, BLUE), align="c")]),
        arrow(5.95, 4.30, 6.72, 4.30, color=BLUE, lw=2.0),
    )
    # right: definition blocks
    s.add(
        *pill(7.42, 2.55, "IN ONE LINE", h=0.30, size=9.5, bg=BLUE_L, color=BLUE_D),
        text(7.42, 2.98, 5.0, 1.0,
             [P(T("A set is a well-defined collection of objects. The objects in it are called its elements.",
                  14.5, False, INK), line=1.34)]),
    )
    rows = [
        ("Union  ·  A ∪ B", "Every element that is in A, or in B, or in both."),
        ("Intersection  ·  A ∩ B", "Only the elements that are in both A and B at the same time."),
        ("Difference  ·  A − B", "The elements of A that are not in B."),
    ]
    cy = 4.06
    x = 7.42
    w = 5.06
    s.add(Rect(x, cy, w, 2.30, fill=WHITE, radius=0.14, line=LINE, lw=1.0))
    yy = cy + 0.16
    for i, (head, body) in enumerate(rows):
        s.add(text(x + 0.22, yy, w - 0.44, 0.30, [P(T(head, 12.5, True, BLUE_D, font=FONT_M))]))
        s.add(text(x + 0.22, yy + 0.27, w - 0.44, 0.40, [P(T(body, 11, False, MUT), line=1.2)]))
        yy += 0.72
        if i < 2:
            s.add(rule(x + 0.22, yy - 0.12, w - 0.44, PANEL2, 1))
    s.add(
        Rect(7.42, 6.50, 5.06, 0.42, fill=BLUE_L, radius=0.10),
        text(7.56, 6.50, 4.8, 0.42, [P(T("Empty set  { }   ·   Universal set U holds everything we discuss.",
                                          10, True, BLUE_D))], anchor="m"),
    )
    return s


# ========================================================================
# 06 — PROJECT PHOTO
# ========================================================================
def s06():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 01   ·   OUR MODEL", "The model on our table",
                        "Photograph the completed board from the front, with the syringes visible.",
                        BLUE, 6, "PROJECT 01 · SETS"))
    s.add(
        Rect(0.85, 2.48, 8.35, 4.18, fill=PANEL, radius=0.16, shadow=True),
        Image(str(A / "sets_hero.png"), 0.85, 2.48, 8.35, 4.18),
        Rect(0.85, 2.48, 8.35, 4.18, fill=None, line=WHITE, lw=3.0, radius=0.16),
    )
    s.add(*pill(1.15, 5.98, "REFERENCE PHOTO — replace with your photo", h=0.30, size=9, bg=NAVY_BG))
    s.add(text(10.62, 5.98, 1.9, 0.3, [P(T("S.D. PUBLIC SCHOOL", 9, True, WHITE, spacing=1.6), align="r")]))
    s.add(
        Rect(9.52, 2.48, 2.96, 4.18, fill=WHITE, radius=0.16, line=LINE, lw=1.0, shadow=True),
        Rect(9.52, 2.48, 2.96, 0.62, fill=BLUE_D, radius=0.10),
        text(9.52, 2.48, 2.96, 0.62, [P(T("S.D. PUBLIC SCHOOL", 10, True, WHITE, spacing=1.4), align="c")], anchor="m"),
        text(9.72, 3.28, 2.56, 0.6, [P(T("Maths Working Model", 11, True, INK))]),
        rule(9.72, 3.72, 2.56, LINE, 1),
        *L("Set theory: union & intersection", size=9.5, color=MUT)[:0],
        text(9.72, 3.86, 2.56, 2.4,
             [P(T("Set theory", 9, True, BLUE, spacing=1.2)),
              P(T("Union & intersection of two sets, shown with sliding circles and a syringe-driven mechanism.",
                  9.5, False, MUT), before=4, line=1.25),
              P(T("Team XI  ·  Class XI Science", 9, True, FAINT), before=10),
              P(T("Session 2025–26", 9, False, FAINT), before=2)]),
    )
    return s


# ========================================================================
# 07 — HOW IT WORKS
# ========================================================================
def s07():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 01   ·   HOW IT WORKS", "Push the plunger, watch the overlap",
                        "The whole model runs on air pressure — the same idea as a medical syringe, with water instead of medicine.",
                        BLUE, 7, "PROJECT 01 · SETS"))
    # left mechanism diagram
    s.add(Rect(0.85, 2.55, 7.05, 4.10, fill=PANEL, radius=0.18))
    # reservoir
    s.add(Rect(1.15, 2.86, 1.90, 1.30, fill=WHITE, radius=0.08, line=LINE, lw=1.2))
    s.add(Rect(1.22, 3.66, 1.76, 0.44, fill="BFE3F7", radius=0.06))
    s.add(text(1.15, 2.92, 1.9, 0.4, [P(T("WATER\nRESERVOIR", 8.5, True, BLUE_D), align="c")]))
    # tube from reservoir to left syringe
    s.add(Line(3.05, 3.52, 3.70, 3.52, color=CYAN, lw=5.0))
    s.add(Line(3.05, 3.52, 3.70, 3.52, color="DFF3FB", lw=2.0))
    # syringe body
    s.add(Rect(3.70, 3.34, 2.05, 0.40, fill=WHITE, radius=0.05, line=INK2, lw=1.2))
    s.add(Rect(3.74, 3.38, 1.30, 0.32, fill="CFE9F8", radius=0.04))
    s.add(Rect(5.75, 3.46, 0.30, 0.16, fill=INK2, radius=0.02))
    # plunger
    s.add(Rect(5.98, 3.42, 0.90, 0.22, fill=INK2, radius=0.04))
    s.add(Rect(6.80, 3.20, 0.14, 0.68, fill=INK2, radius=0.05))
    # arrow push
    s.add(arrow(7.02, 3.54, 7.52, 3.54, color=PINK, lw=2.0))
    s.add(text(6.98, 3.64, 0.78, 0.26, [P(T("PUSH", 8, True, PINK), align="c")]))
    # tube down to circle
    s.add(Line(5.90, 3.74, 5.90, 4.28, color=CYAN, lw=5.0))
    s.add(Line(5.90, 3.74, 5.90, 4.28, color="DFF3FB", lw=2.0))
    s.add(Line(5.90, 4.28, 4.62, 4.28, color=CYAN, lw=5.0))
    s.add(Line(5.90, 4.28, 4.62, 4.28, color="DFF3FB", lw=2.0))
    # before / after Venn states
    s.add(text(1.18, 4.38, 1.9, 0.26, [P(T("BEFORE", 8, True, FAINT, spacing=1.4))]))
    s.add(Oval(1.18, 4.66, 0.98, 0.98, fill=YELLOW_L, line=YELLOW, lw=1.6))
    s.add(Oval(2.06, 4.66, 0.98, 0.98, fill=PINK_L, line=PINK, lw=1.6))
    s.add(text(1.18, 5.72, 1.86, 0.26, [P(T("no overlap", 8.5, False, MUT))]))
    s.add(arrow(3.16, 5.15, 3.78, 5.15, color=INK2, lw=1.6))
    s.add(text(1.18, 5.98, 1.86, 0.26, [P(T("", 8))]))
    s.add(text(3.94, 4.38, 2.0, 0.26, [P(T("AFTER A PUSH", 8, True, BLUE, spacing=1.4))]))
    s.add(Oval(3.94, 4.66, 0.98, 0.98, fill=YELLOW_L, line=YELLOW, lw=1.6))
    s.add(Oval(4.52, 4.66, 0.98, 0.98, fill=PINK_L, line=PINK, lw=1.6))
    s.add(Poly(lens_points((4.43, 5.15), 0.49, (5.01, 5.15), 0.49), fill=WHITE, line=GOLD, lw=1.4))
    s.add(text(3.94, 5.72, 2.0, 0.26, [P(T("the lens is A ∩ B", 8.5, False, MUT))]))
    s.add(text(5.95, 3.86, 1.9, 0.3, [P(T("tube", 8.5, False, CYAN))]))
    s.add(text(1.15, 4.02, 1.9, 0.3, [P(T("water", 8.5, False, CYAN), align="c")]))
    # right: numbered steps
    steps = [
        ("Pressure moves the water", "Pressing the plunger pushes water out of the syringe and down the tube."),
        ("Water pushes the panel", "The tube ends behind a light panel fixed to the moving circle."),
        ("The circle slides", "One circle glides over the other, opening and closing the overlap."),
        ("Read the result", "At full push the overlap is largest: that white lens is A ∩ B."),
    ]
    cy = 2.55
    for i, (head, body) in enumerate(steps):
        s.add(Oval(8.28, cy + 0.02, 0.46, 0.46, fill=BLUE))
        s.add(text(8.28, cy + 0.02, 0.46, 0.46, [P(T(str(i + 1), 13, True, WHITE), align="c")], anchor="m"))
        s.add(text(8.98, cy, 3.55, 0.32, [P(T(head, 13, True, INK))]))
        s.add(text(8.98, cy + 0.30, 3.55, 0.55, [P(T(body, 10.5, False, MUT), line=1.22)]))
        if i < 3:
            s.add(Line(8.51, cy + 0.50, 8.51, cy + 0.98, color=BLUE_L, lw=2.0))
        cy += 1.02
    return s


# ========================================================================
# 08 — SETS: THE MATHS
# ========================================================================
def s08():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 01   ·   THE MATHS", "The formulas our model demonstrates",
                        "Everything the board shows can be written down in three lines of set notation.",
                        BLUE, 8, "PROJECT 01 · SETS"))
    cards = [
        ("A ∪ B", "Union", "x belongs to A ∪ B if x ∈ A or x ∈ B (or both).", "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)", YELLOW, YELLOW_D, YELLOW_L),
        ("A ∩ B", "Intersection", "x belongs to A ∩ B if x ∈ A and x ∈ B together.", "A ∩ B ⊆ A  and  A ∩ B ⊆ B", PINK, PINK, PINK_L),
        ("A − B", "Difference", "x belongs to A − B if x ∈ A but x ∉ B.", "A − B = A ∩ B′", TEAL, TEAL, "D9F2EF"),
    ]
    x = 0.85
    for sym, name, body, formula, acc, accd, tint in cards:
        s.add(Rect(x, 2.55, 3.85, 3.34, fill=WHITE, radius=0.16, line=LINE, lw=1.0, shadow=True))
        s.add(Rect(x, 2.55, 3.85, 0.10, fill=acc, radius=0.05))
        s.add(Rect(x + 0.28, 2.86, 1.02, 0.80, fill=tint, radius=0.12))
        s.add(text(x + 0.28, 2.86, 1.02, 0.80, [P(T(sym, 19, True, accd, font=FONT_M), align="c")], anchor="m"))
        s.add(text(x + 1.44, 2.96, 2.2, 0.4, [P(T(name, 16, True, INK))]))
        s.add(text(x + 0.28, 3.86, 3.30, 0.95, [P(T(body, 12, False, MUT), line=1.3)]))
        s.add(rule(x + 0.28, 4.86, 3.30, PANEL2, 1))
        s.add(text(x + 0.28, 5.00, 3.32, 0.72,
                   [P(T(formula, 11.5, True, accd, font=FONT_M), line=1.3)]))
        x += 4.06
    # worked example strip
    s.add(Rect(0.85, 6.06, 11.63, 0.78, fill=NAVY_BG, radius=0.12))
    s.add(text(1.12, 6.06, 2.0, 0.78, [P(T("WORKED EXAMPLE", 8.5, True, YELLOW, spacing=1.6))], anchor="m"))
    s.add(text(2.86, 6.06, 9.45, 0.78,
               [P([T("U = {1, 2, …, 10}    A = {1, 3, 5, 7}    B = {3, 4, 5, 6}", 10.5, False, WHITE, font=FONT_M)],
                  ), P([T("A ∪ B = {1, 3, 4, 5, 6, 7}    A ∩ B = {3, 5}    n(A ∪ B) = 6", 10.5, False, "9FC0F0", font=FONT_M)],
                       before=3)], anchor="m"))
    return s


# ========================================================================
# 09 — SETS: WHILE MAKING
# ========================================================================
def s09():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 01   ·   BEHIND THE SCENES", "While we were making it",
                        "Replace these frames with your own photos — the captions already tell the story.",
                        BLUE, 9, "PROJECT 01 · SETS"))
    s.add(
        Rect(0.85, 2.50, 5.05, 3.72, fill=PANEL, radius=0.16, shadow=True),
        Image(str(A / "making_hero.png"), 0.85, 2.50, 5.05, 3.72),
        Rect(0.85, 2.50, 5.05, 3.72, fill=None, line=WHITE, lw=3.0, radius=0.16),
        *pill(1.12, 5.72, "WORKSHOP — DAY 2", h=0.30, size=9, bg=NAVY_BG),
    )
    # three small photo frames with captions
    caps = [
        ("Measuring the circles", "Both circles had to be identical, so we traced one and cut the second from it."),
        ("Fixing the tube", "The tube needed a watertight seal — the first two attempts leaked."),
        ("Final colour work", "Yellow and pink were chosen so the overlap reads from across the hall."),
    ]
    x = 6.22
    for i, (head, body) in enumerate(caps):
        s.add(*photo_frame(x, 2.50, 1.92, 1.62, radius=0.10, label="PHOTO", sub="insert here", size=11))
        s.add(text(x, 4.24, 1.92, 0.34, [P(T(head, 10.5, True, INK))]))
        s.add(text(x, 4.56, 1.92, 1.0, [P(T(body, 8.8, False, MUT), line=1.24)]))
        x += 2.06
    # quote / lesson strip
    s.add(Rect(6.22, 5.70, 6.26, 0.90, fill=BLUE_L, radius=0.12))
    s.add(text(6.42, 5.70, 5.9, 0.90,
               [P(T("What we learned", 9.5, True, BLUE, spacing=1.4)),
                P(T("Measure twice, cut once — and always test the seal before the paint goes on.", 11.5, True, BLUE_D),
                  before=3)], anchor="m"))
    return s


# ========================================================================
# 10 — SETS: TAKING IT FURTHER
# ========================================================================
def s10():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 01   ·   WHY IT MATTERS", "Where sets show up in real life",
                        "Set theory is not a school-only idea — it is the language used to sort anything.",
                        BLUE, 10, "PROJECT 01 · SETS"))
    items = [
        ("Databases", "Filtering a list runs an intersection: customers who are from U.P. and bought last week.", BLUE, BLUE_L),
        ("Search engines", "A search joins your words with AND: pages containing all of them, not just one.", TEAL, "D9F2EF"),
        ("Attendance lists", "Present = Students ∩ Present-today. Absent = Students − Present.", PINK, PINK_L),
        ("Probability", "P(A ∪ B) = P(A) + P(B) − P(A ∩ B) — the counting formula behind every dice question.", VIOLET, VIOLET_L),
    ]
    x, y = 0.85, 2.55
    for i, (head, body, acc, tint) in enumerate(items):
        cx = x + (i % 2) * 5.92
        cy = y + (i // 2) * 1.78
        s.add(Rect(cx, cy, 5.62, 1.58, fill=WHITE, radius=0.16, line=LINE, lw=1.0))
        s.add(Rect(cx, cy, 0.09, 1.58, fill=acc, radius=0.045))
        s.add(text(cx + 0.34, cy + 0.20, 4.9, 0.34, [P(T(head, 14.5, True, INK))]))
        s.add(text(cx + 0.34, cy + 0.58, 4.95, 0.88, [P(T(body, 11, False, MUT), line=1.28)]))
    s.add(Rect(0.85, 6.30, 11.63, 0.46, fill=PANEL, radius=0.08))
    s.add(text(1.05, 6.32, 11.2, 0.42,
               [P(T("Every one of these is the same question our board answers: what belongs to both?", 10.5, True, INK2))],
               anchor="m"))
    return s


# ========================================================================
# 11 — PROJECT 02 DIVIDER
# ========================================================================
def s11():
    s = Slide(bg=VIOLET_D)
    s.add(
        Oval(8.9, -2.0, 7.0, 7.0, fill="3B1E8C", opacity=0.55),
        Oval(-1.8, 4.4, 6.0, 6.0, fill="3B1E8C", opacity=0.40),
        text(0.85, 1.10, 6.0, 0.4, [P(T("PROJECT 02  ·  CONIC SECTIONS", 12, True, "E9D5FF", spacing=2.4))]),
        text(0.85, 1.62, 7.4, 2.3, [P(T("Conics", 76, True, WHITE, spacing=-2)),
                                     P(T("A plane cuts a cone", 31, True, "E9D5FF"))]),
        text(0.85, 4.20, 6.5, 1.4,
             [P(T("One cone. Four curves. The only thing that changes is the angle at which the plane slices through.",
                  15, False, "D8CBF6"), line=1.4)]),
        *pill(0.85, 5.70, "CLASS XI  ·  MATHEMATICS", h=0.34, size=10, bg=WHITE, color=VIOLET_D),
        *pill(4.62, 5.70, "CHAPTER 11", h=0.34, size=10, bg="4C27A8", color=WHITE),
        text(0.85, 6.72, 6.2, 0.3, [P(T("S.D. PUBLIC SCHOOL  ·  MATHS EXHIBITION 2025–26", 9, True, "9C86D8", spacing=1.8))]),
        Image(str(A / "conics_hero.png"), 7.55, 1.55, 5.45, 3.96),
    )
    return s


# ========================================================================
# 12 — CONICS: WHAT IT IS
# ========================================================================
def cone_diagram(cx, cy, scale=1.0, color=VIOLET, tint="F3EEFF"):
    """Two nappe cone, symmetric about cy, apex at (cx, cy)."""
    hw, hh = 1.02 * scale, 1.20 * scale
    neck = 0.13 * scale
    items = [
        # upper nappe
        Poly([(cx - hw, cy - hh), (cx - neck, cy - 0.02), (cx + neck, cy - 0.02), (cx + hw, cy - hh)],
             fill=tint, line=color, lw=1.6),
        # lower nappe
        Poly([(cx - neck, cy + 0.02), (cx + neck, cy + 0.02), (cx + hw, cy + hh), (cx - hw, cy + hh)],
             fill=tint, line=color, lw=1.6),
        Oval(cx - hw, cy - hh - 0.12 * scale, hw * 2, 0.26 * scale, fill=tint, line=color, lw=1.6),
        Oval(cx - hw, cy + hh - 0.12 * scale, hw * 2, 0.26 * scale, fill=tint, line=color, lw=1.6),
        Line(cx, cy - hh - 0.34 * scale, cx, cy + hh + 0.34 * scale, color=MUT, lw=1.0, dash="dash"),
    ]
    return items


def s12():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 02   ·   WHAT IT IS", "Slice a double cone, get a curve",
                        "A conic section is the curve you get when a flat plane cuts through a cone — the shape depends only on the angle.",
                        VIOLET, 12, "PROJECT 02 · CONICS"))
    # diagram
    s.add(Rect(0.85, 2.55, 5.25, 4.10, fill=PANEL, radius=0.18))
    s.add(*cone_diagram(3.10, 4.55, 1.0))
    s.add(Poly([(2.42, 3.52), (4.34, 3.28), (4.34, 3.46), (2.42, 3.70)], fill=VIOLET, opacity=0.55))
    s.add(Line(1.75, 3.62, 4.55, 3.30, color=VIOLET, lw=1.6))
    s.add(text(4.30, 3.06, 1.6, 0.3, [P(T("cutting plane", 9, True, VIOLET))]))
    s.add(text(3.04, 5.64, 0.2, 0.3, [P(T("", 8))]))
    s.add(text(2.10, 6.28, 2.0, 0.3, [P(T("double cone (two nappes)", 9, False, MUT), align="c")]))
    s.add(text(0.95, 5.70, 1.9, 0.3, [P(T("axis", 9, False, MUT))]))

    # right: 4 shapes grid
    shapes = [
        ("Circle", "Plane ⊥ axis", "x² + y² = r²"),
        ("Ellipse", "Plane tilted, cuts one nappe", "x²/a² + y²/b² = 1"),
        ("Parabola", "Plane ∥ to a slant edge", "y² = 4ax"),
        ("Hyperbola", "Plane cuts both nappes", "x²/a² − y²/b² = 1"),
    ]
    x0, y0, cw, ch = 6.42, 2.55, 2.98, 1.94
    kinds = ["circle", "ellipse", "parabola", "hyperbola"]
    for i, (name, how, eq) in enumerate(shapes):
        cx = x0 + (i % 2) * (cw + 0.22)
        cy = y0 + (i // 2) * (ch + 0.22)
        s.add(Rect(cx, cy, cw, ch, fill=WHITE, radius=0.14, line=LINE, lw=1.0, shadow=True))
        s.add(*conic_icon(kinds[i], cx + cw - 0.62, cy + 0.72, VIOLET, r=0.30, lw=2.2))
        s.add(text(cx + 0.22, cy + 0.18, cw - 1.24, 0.34, [P(T(name, 14.5, True, INK))]))
        s.add(text(cx + 0.22, cy + 0.52, cw - 0.4, 0.30, [P(T(how, 9, False, MUT))]))
        s.add(rule(cx + 0.22, cy + 1.10, cw - 0.44, PANEL2, 1))
        s.add(text(cx + 0.22, cy + 1.22, cw - 0.4, 0.34,
                   [P(T(eq, 12, True, VIOLET, font=FONT_M))]))
        s.add(Oval(cx + cw - 0.62, cy + 0.16, 0.34, 0.34, fill=VIOLET_L))
        s.add(text(cx + cw - 0.62, cy + 0.16, 0.34, 0.34,
                   [P(T(str(i + 1), 10, True, VIOLET_D), align="c")], anchor="m"))
    return s


# ========================================================================
# 13 — CONICS PHOTO
# ========================================================================
def s13():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 02   ·   OUR MODEL", "The model on our table",
                        "Photograph the cone with the plane half-way, then again with the plane pulled out.",
                        VIOLET, 13, "PROJECT 02 · CONICS"))
    s.add(
        Rect(0.85, 2.48, 8.35, 4.18, fill=PANEL, radius=0.16, shadow=True),
        Image(str(A / "conics_hero.png"), 0.85, 2.48, 8.35, 4.18),
        Rect(0.85, 2.48, 8.35, 4.18, fill=None, line=WHITE, lw=3.0, radius=0.16),
        *pill(1.15, 5.98, "REFERENCE PHOTO — replace with your photo", h=0.30, size=9, bg=NAVY_BG),
    )
    s.add(
        Rect(9.52, 2.48, 2.96, 4.18, fill=WHITE, radius=0.16, line=LINE, lw=1.0, shadow=True),
        Rect(9.52, 2.48, 2.96, 0.62, fill=VIOLET_D, radius=0.10),
        text(9.52, 2.48, 2.96, 0.62, [P(T("S.D. PUBLIC SCHOOL", 10, True, WHITE, spacing=1.4), align="c")], anchor="m"),
        text(9.72, 3.28, 2.56, 0.6, [P(T("Maths Working Model", 11, True, INK))]),
        rule(9.72, 3.72, 2.56, LINE, 1),
        text(9.72, 3.86, 2.56, 2.4,
             [P(T("Conic sections", 9, True, VIOLET, spacing=1.2)),
              P(T("A double cone cut by a plane on a syringe-driven rail, producing all four conic curves.",
                  9.5, False, MUT), before=4, line=1.25),
              P(T("Team XI  ·  Class XI Science", 9, True, FAINT), before=10),
              P(T("Session 2025–26", 9, False, FAINT), before=2)]),
    )
    return s


# ========================================================================
# 14 — CONICS: HOW IT WORKS
# ========================================================================
def s14():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 02   ·   HOW IT WORKS", "The plane travels, the curve changes",
                        "The student never touches the cone. A syringe moves the plane along a rail — the angle does the rest.",
                        VIOLET, 14, "PROJECT 02 · CONICS"))
    # left: mechanism
    s.add(Rect(0.85, 2.55, 6.30, 4.10, fill=PANEL, radius=0.18))
    s.add(*cone_diagram(2.55, 4.60, 0.86))
    # vertical rail
    s.add(Rect(4.62, 2.95, 0.10, 3.30, fill="C9CEDA", radius=0.03))
    s.add(*[Rect(4.52, 4.48, 0.30, 0.26, fill=INK2, radius=0.04)])
    # plane at an angle, sliding up/down the rail
    s.add(Poly([(3.10, 4.02), (5.42, 3.62), (5.42, 3.86), (3.10, 4.26)], fill=VIOLET, opacity=0.62))
    s.add(arrow(4.77, 4.10, 4.77, 2.86, color=VIOLET, lw=1.8))
    s.add(arrow(4.77, 4.92, 4.77, 6.16, color=VIOLET, lw=1.8))
    # syringe
    s.add(Rect(5.30, 4.42, 1.15, 0.30, fill=WHITE, radius=0.04, line=INK2, lw=1.1))
    s.add(Rect(5.34, 4.46, 0.62, 0.22, fill="DDD6F6", radius=0.03))
    s.add(Rect(6.02, 4.27, 0.14, 0.60, fill=INK2, radius=0.04))
    s.add(Line(5.30, 4.57, 4.90, 4.57, color=INK2, lw=1.6))
    s.add(text(0.95, 2.66, 2.4, 0.3, [P(T("CONE", 8.5, True, VIOLET_D, spacing=1.6))]))
    s.add(text(3.98, 6.34, 2.2, 0.3, [P(T("rail + sliding plane", 8.5, True, MUT))]))
    s.add(text(5.28, 4.78, 1.4, 0.3, [P(T("syringe", 8.5, True, MUT))]))
    s.add(text(1.00, 6.34, 2.9, 0.3, [P(T("angle of the plane decides the curve", 8.5, True, VIOLET))]))

    # right: 4 states
    states = [
        ("Plane is horizontal", "Circle", "cut across the axis", "0c"),
        ("Plane tilts slightly", "Ellipse", "still cutting one nappe", "1c"),
        ("Plane parallel to edge", "Parabola", "the open curve appears", "2c"),
        ("Plane steepens", "Hyperbola", "now it cuts both nappes", "3c"),
    ]
    cy = 2.55
    for i, (when, shape, note, _) in enumerate(states):
        s.add(Rect(7.42, cy, 5.06, 0.92, fill=WHITE, radius=0.12, line=LINE, lw=1.0))
        s.add(Rect(7.42, cy, 0.09, 0.92, fill=VIOLET, radius=0.045))
        s.add(text(7.66, cy + 0.14, 2.5, 0.30, [P(T(when, 10, False, MUT))]))
        s.add(text(7.66, cy + 0.42, 2.5, 0.34, [P(T(shape, 15, True, VIOLET_D))]))
        s.add(text(10.05, cy + 0.30, 2.25, 0.5, [P(T(note, 9.5, True, INK2), align="r")]))
        cy += 1.00
    s.add(Rect(7.42, 6.62, 5.06, 0.0, fill=None))
    s.add(text(7.42, 6.60, 5.06, 0.30,
               [P(T("Same cone every time — only the angle changes.", 10, True, VIOLET))]))
    return s


# ========================================================================
# 15 — CONICS: THE MATHS
# ========================================================================
def conic_icon(kind, cx, cy, color, r=0.42, lw=2.4):
    """Tiny glyph for each conic; r = half-size in inches."""
    if kind == "circle":
        return [Oval(cx - r, cy - r, r * 2, r * 2, fill=None, line=color, lw=lw)]
    if kind == "ellipse":
        return [Oval(cx - r * 1.30, cy - r * 0.78, r * 2.60, r * 1.56, fill=None, line=color, lw=lw)]
    if kind == "parabola":
        pts = []
        for i in range(41):
            t = -1 + 2 * i / 40
            pts.append((cx + t * r * 1.38, cy - (t * t) * r * 1.48 + r * 0.71))
        return [Poly(pts, fill=None, line=color, lw=lw, close=False)]
    # hyperbola: two branches opening left/right, fitted inside the 1.18in tile
    left, right = [], []
    span = r * 0.95
    for i in range(23):
        yy = (-1.0 + 2.0 * i / 22) * span
        xx = r * 0.38 + r * 0.71 * (yy / span) ** 2
        left.append((cx - xx, cy + yy))
        right.append((cx + xx, cy + yy))
    return [Poly(left, fill=None, line=color, lw=lw, close=False),
            Poly(right, fill=None, line=color, lw=lw, close=False)]


def s15():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 02   ·   THE MATHS", "Four curves, standard form",
                        "Each shape our plane produces has one standard equation to remember.",
                        VIOLET, 15, "PROJECT 02 · CONICS"))
    cards = [
        ("Circle", "circle", "x² + y² = r²", "Centre at origin, radius r. Every point is exactly r from the centre.", VIOLET, VIOLET_L),
        ("Ellipse", "ellipse", "x²/a² + y²/b² = 1", "a > b; foci on the major axis at (±c, 0) where c² = a² − b².", "E8407E", "FFE2EC"),
        ("Parabola", "parabola", "y² = 4ax", "Focus at (a, 0); directrix x = −a. Every point is equidistant from both.", CYAN, "DFF3FB"),
        ("Hyperbola", "hyperbola", "x²/a² − y²/b² = 1", "c² = a² + b²; two branches that never meet the asymptotes.", "E08A0B", "FDEBD0"),
    ]
    x0, y0, cw, ch = 0.85, 2.52, 2.90, 3.42
    for i, (name, kind, eq, note, acc, tint) in enumerate(cards):
        cx = x0 + i * (cw + 0.17)
        s.add(Rect(cx, y0, cw, ch, fill=WHITE, radius=0.16, line=LINE, lw=1.0, shadow=True))
        s.add(Rect(cx + 0.22, y0 + 0.20, cw - 0.44, 1.18, fill=tint, radius=0.12))
        s.add(*conic_icon(kind, cx + cw / 2, y0 + 0.79, acc))
        s.add(text(cx + 0.20, y0 + 1.50, cw - 0.4, 0.34, [P(T(name, 15, True, INK))]))
        s.add(text(cx + 0.20, y0 + 1.86, cw - 0.4, 0.40,
                   [P(T(eq, 13, True, acc if acc != "E08A0B" else GOLD, font=FONT_M))]))
        s.add(rule(cx + 0.20, y0 + 2.34, cw - 0.40, PANEL2, 1))
        s.add(text(cx + 0.20, y0 + 2.44, cw - 0.38, 0.86, [P(T(note, 9.5, False, MUT), line=1.26)]))
    # eccentricity strip
    s.add(Rect(0.85, 6.14, 11.63, 0.62, fill=PANEL, radius=0.10))
    s.add(text(1.10, 6.14, 11.2, 0.62,
               [P([T("Eccentricity tells them apart:  ", 11, True, INK2),
                   T("e = 0", 11, True, VIOLET), T(" (circle)  <  ", 11, False, MUT),
                   T("e < 1", 11, True, PINK), T(" (ellipse)  <  ", 11, False, MUT),
                   T("e = 1", 11, True, CYAN), T(" (parabola)  <  ", 11, False, MUT),
                   T("e > 1", 11, True, GOLD), T(" (hyperbola)", 11, False, MUT)])],
               anchor="m"))
    return s


# ========================================================================
# 16 — CONICS: WHILE MAKING
# ========================================================================
def s16():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 02   ·   BEHIND THE SCENES", "While we were making it",
                        "Replace these frames with your own photos — the captions already tell the story.",
                        VIOLET, 16, "PROJECT 02 · CONICS"))
    s.add(
        Rect(0.85, 2.50, 5.05, 3.72, fill=PANEL, radius=0.16, shadow=True),
        Image(str(A / "making_hero.png"), 0.85, 2.50, 5.05, 3.72),
        Rect(0.85, 2.50, 5.05, 3.72, fill=None, line=WHITE, lw=3.0, radius=0.16),
        *pill(1.12, 5.72, "WORKSHOP — DAY 3", h=0.30, size=9, bg=NAVY_BG),
    )
    caps = [
        ("Building the cone", "Four foam-board sectors glued into two nappes — the join at the apex was the tricky part."),
        ("The sliding rail", "A level tube became the rail, so the plane stays perfectly parallel to itself."),
        ("Sealing the syringe", "Anabond and glue-gun layers stopped the air leak that kept dropping the plane."),
    ]
    x = 6.22
    for head, body in caps:
        s.add(*photo_frame(x, 2.50, 1.92, 1.62, radius=0.10, label="PHOTO", sub="insert here", size=11))
        s.add(text(x, 4.24, 1.92, 0.34, [P(T(head, 10.5, True, INK))]))
        s.add(text(x, 4.56, 1.92, 1.0, [P(T(body, 8.8, False, MUT), line=1.24)]))
        x += 2.06
    s.add(Rect(6.22, 5.70, 6.26, 0.90, fill=VIOLET_L, radius=0.12))
    s.add(text(6.42, 5.70, 5.9, 0.90,
               [P(T("What we learned", 9.5, True, VIOLET, spacing=1.4)),
                P(T("Air is harder to control than water — the cone had to be perfectly balanced to slide smoothly.",
                  11.5, True, VIOLET_D), before=3)], anchor="m"))
    return s


# ========================================================================
# 17 — CONICS: TAKING IT FURTHER
# ========================================================================
def s17():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 02   ·   WHY IT MATTERS", "Where conics show up in real life",
                        "Satellites, headlights and stadium roofs all rely on the shapes our plane draws.",
                        VIOLET, 17, "PROJECT 02 · CONICS"))
    items = [
        ("Satellite dishes", "A parabolic reflector focuses every incoming signal onto one point — the focus.", VIOLET, VIOLET_L),
        ("Headlights", "The bulb sits at the focus of a parabolic mirror, so the beam leaves parallel.", CYAN, "DFF3FB"),
        ("Planetary orbits", "Planets travel on ellipses with the Sun at one focus — Kepler's first law.", PINK, PINK_L),
        ("Cooling towers", "Hyperbolic shells are strong and thin: the curve carries the load efficiently.", GOLD, GOLD_L),
        ("Whispering galleries", "Elliptic halls reflect a whisper from one focus straight to the other.", TEAL, "D9F2EF"),
        ("Lighthouses", "Hyperbolic lenses spread a point of light into a wide, even beam.", BLUE, BLUE_L),
    ]
    x0, y0, cw, ch, gx, gy = 0.85, 2.52, 3.78, 1.76, 0.16, 0.18
    for i, (head, body, acc, tint) in enumerate(items):
        cx = x0 + (i % 3) * (cw + gx)
        cy = y0 + (i // 3) * (ch + gy)
        s.add(Rect(cx, cy, cw, ch, fill=WHITE, radius=0.15, line=LINE, lw=1.0))
        s.add(Rect(cx, cy, cw, 0.08, fill=acc, radius=0.04))
        s.add(text(cx + 0.24, cy + 0.22, cw - 0.46, 0.34, [P(T(head, 13.5, True, INK))]))
        s.add(text(cx + 0.24, cy + 0.62, cw - 0.44, 1.00, [P(T(body, 11, False, MUT), line=1.28)]))
    s.add(text(0.85, 6.30, 11.6, 0.34,
               [P(T("The parabola is the one you use most: it is the only conic that turns a point of light into a parallel beam.",
                    10.5, True, INK2))]))
    return s


# ========================================================================
# 18 — COMPARISON
# ========================================================================
def s18():
    s = Slide(bg=BG)
    s.add(*section_head("THE TWO TOGETHER", "Side by side, but never mixed",
                        "Same subject, same class, two completely separate builds — here is the difference in one view.",
                        INK, 18, "COMPARISON"))
    s.add(
        Rect(0.85, 2.52, 5.70, 3.72, fill=BLUE_L, radius=0.18),
        Rect(6.78, 2.52, 5.70, 3.72, fill=VIOLET_L, radius=0.18),
        *pill(1.18, 2.80, "PROJECT 01", h=0.30, size=9.5, bg=BLUE),
        text(1.18, 3.20, 4.9, 0.56, [P(T("Sets", 28, True, BLUE_D))]),
        *pill(7.12, 2.80, "PROJECT 02", h=0.30, size=9.5, bg=VIOLET),
        text(7.12, 3.20, 4.9, 0.56, [P(T("Conic Sections", 28, True, VIOLET_D))]),
    )
    rows = [
        ("Key idea", "Belonging — what is in both sets", "Shape — what a plane cuts out"),
        ("Moving part", "One circle slides across another", "The plane slides along a rail"),
        ("Driven by", "Water pressure in a syringe", "Air pressure in a syringe"),
        ("You see", "The overlap open and close", "Four curves appear and change"),
        ("Formula", "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)", "x²/a² + y²/b² = 1"),
    ]
    cy = 4.02
    for i, (label, a, b) in enumerate(rows):
        if i % 2 == 0:
            s.add(Rect(0.85, cy - 0.06, 11.63, 0.44, fill="F8FAFE", radius=0.06))
        s.add(text(1.02, cy, 1.45, 0.32, [P(T(label, 10, True, MUT, spacing=0.8))]))
        s.add(text(2.55, cy, 3.95, 0.32, [P(T(a, 10.5, True, BLUE_D))]))
        s.add(text(6.95, cy, 5.50, 0.32, [P(T(b, 10.5, True, VIOLET_D))]))
        cy += 0.46
    s.add(Rect(0.85, 6.48, 11.63, 0.42, fill=WHITE, radius=0.08, line=LINE, lw=1.0))
    s.add(text(1.05, 6.48, 11.3, 0.42,
               [P(T("Both models are displayed separately — one table each, one explanation each.", 10.5, True, INK2))],
               anchor="m"))
    return s


# ========================================================================
# 19 — PHOTO WALL 01
# ========================================================================
def s19():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 01   ·   PHOTO WALL", "Sets — the build in pictures",
                        "Swap each frame for a photo from your phone; keep the captions underneath.",
                        BLUE, 19, "PROJECT 01 · SETS"))
    frames = [
        (0.85, 2.46, 3.78, 1.80, "01", "Planning the layout"),
        (4.79, 2.46, 3.78, 1.80, "02", "Cutting the circles"),
        (8.73, 2.46, 3.78, 1.80, "03", "Fixing the syringes"),
        (0.85, 4.66, 3.78, 1.80, "04", "Testing the slide"),
        (4.79, 4.66, 3.78, 1.80, "05", "Painting the sets"),
        (8.73, 4.66, 3.78, 1.80, "06", "Final display"),
    ]
    for x, y, w, h, num, cap in frames:
        s.add(*photo_frame(x, y, w, h, radius=0.10, label="PHOTO", sub="insert here", size=13))
        s.add(text(x, y + h + 0.06, 0.6, 0.26, [P(T(num, 9, True, BLUE, spacing=0.8))]))
        s.add(text(x + 0.44, y + h + 0.06, w - 0.44, 0.26, [P(T(cap, 9.5, True, INK2))]))
    return s


# ========================================================================
# 20 — PHOTO WALL 02
# ========================================================================
def s20():
    s = Slide(bg=BG)
    s.add(*section_head("PROJECT 02   ·   PHOTO WALL", "Conics — the build in pictures",
                        "Swap each frame for a photo from your phone; keep the captions underneath.",
                        VIOLET, 20, "PROJECT 02 · CONICS"))
    frames = [
        (0.85, 2.46, 3.78, 1.80, "01", "Marking the sectors"),
        (4.79, 2.46, 3.78, 1.80, "02", "Gluing the cone"),
        (8.73, 2.46, 3.78, 1.80, "03", "Fitting the rail"),
        (0.85, 4.66, 3.78, 1.80, "04", "Syringe connection"),
        (4.79, 4.66, 3.78, 1.80, "05", "Checking the cut"),
        (8.73, 4.66, 3.78, 1.80, "06", "Final display"),
    ]
    for x, y, w, h, num, cap in frames:
        s.add(*photo_frame(x, y, w, h, radius=0.10, label="PHOTO", sub="insert here", size=13))
        s.add(text(x, y + h + 0.06, 0.6, 0.26, [P(T(num, 9, True, VIOLET, spacing=0.8))]))
        s.add(text(x + 0.44, y + h + 0.06, w - 0.44, 0.26, [P(T(cap, 9.5, True, INK2))]))
    return s


# ========================================================================
# 21 — MATERIALS
# ========================================================================
def s21():
    s = Slide(bg=BG)
    s.add(*section_head("COMMON WORK", "What both models were built from",
                        "Stationery shop and hardware store supplies — both models together cost under 1,200 rupees.",
                        TEAL, 21, "COMMON WORK"))
    mats = [
        ("Foam board", "Structure", "both", TEAL),
        ("Chart paper", "Colour surfaces", "both", TEAL),
        ("Syringes", "The drive", "both", BLUE),
        ("Level tube", "Rail for the plane", "02", VIOLET),
        ("Glue gun", "Joining", "both", TEAL),
        ("Anabond", "Sealing leaks", "02", VIOLET),
        ("Cutter & scissors", "Shaping", "both", TEAL),
        ("Paints & brushes", "Finishing", "both", TEAL),
        ("Thread", "Pulling parts", "01", BLUE),
    ]
    x0, y0, cw, ch, gx, gy = 0.85, 2.52, 3.78, 1.16, 0.16, 0.18
    for i, (name, use, proj, acc) in enumerate(mats):
        cx = x0 + (i % 3) * (cw + gx)
        cy = y0 + (i // 3) * (ch + gy)
        s.add(Rect(cx, cy, cw, ch, fill=WHITE, radius=0.13, line=LINE, lw=1.0))
        s.add(*material_icon(i, cx + 0.30, cy + 0.38, 0.40, acc))
        s.add(text(cx + 0.90, cy + 0.18, cw - 2.02, 0.34, [P(T(name, 11.5, True, INK))]))
        s.add(text(cx + 0.90, cy + 0.54, cw - 1.55, 0.30, [P(T(use, 9.5, False, MUT))]))
        tag = "BOTH" if proj == "both" else f"0{proj[-1]}" if proj in ("01", "02") else proj
        tag = {"both": "BOTH", "01": "MODEL 01", "02": "MODEL 02"}[proj]
        s.add(text(cx + cw - 1.10, cy + 0.20, 0.92, 0.26,
                   [P(T(tag, 7, True, acc, spacing=0.7), align="r")]))
    s.add(text(0.85, 6.34, 11.6, 0.3,
               [P(T("Safety note: cutters, glue guns and syringes were handled under a teacher's supervision only.",
                    10, True, MUT))]))
    return s


# ========================================================================
# 22 — WHAT WE LEARNED
# ========================================================================
def s22():
    s = Slide(bg=NAVY_BG)
    s.add(
        Oval(9.0, -2.4, 7.6, 7.6, fill="14294F", opacity=0.9),
        text(0.85, 0.75, 6.0, 0.36, [P(T("REFLECTION", 11, True, YELLOW, spacing=2.6))]),
        text(0.85, 1.16, 9.8, 1.0, [P(T("What this project actually taught us", 40, True, WHITE, spacing=-0.8))]),
        text(0.85, 2.12, 8.6, 0.5,
             [P(T("Four things we did not expect to learn from two cardboard models.", 14, False, "9DBBE6"))]),
    )
    items = [
        ("A formula is a description", "We memorised n(A ∪ B) for two years. Only after building it did we see it is just counting without double-counting."),
        ("Air leaks everywhere", "The conic plane dropped all afternoon until we sealed every joint. Pressure is unforgiving."),
        ("Visitors ask the hard questions", "Explaining to a Class VI student exposed exactly what we had only memorised."),
        ("Parallel work needs a plan", "Two teams, one table, one deadline — materials had to be shared, not fought over."),
    ]
    x0, y0, cw, ch, gx, gy = 0.85, 2.72, 5.62, 1.72, 0.38, 0.28
    for i, (head, body) in enumerate(items):
        cx = x0 + (i % 2) * (cw + gx)
        cy = y0 + (i // 2) * (ch + gy)
        s.add(Rect(cx, cy, cw, ch, fill="13233F", radius=0.14))
        s.add(text(cx + 0.26, cy + 0.18, 0.7, 0.4, [P(T(f"0{i+1}", 13, True, YELLOW, spacing=1.0))]))
        s.add(text(cx + 0.26, cy + 0.52, cw - 0.52, 0.34, [P(T(head, 14, True, WHITE))]))
        s.add(text(cx + 0.26, cy + 0.88, cw - 0.52, 0.72, [P(T(body, 10.5, False, "A8C2EE"), line=1.26)]))
    s.add(text(0.85, 6.86, 11.6, 0.3,
               [P(T("S.D. PUBLIC SCHOOL   ·   MATHS EXHIBITION 2025–26", 9, True, "5C79B0", spacing=2.0))]))
    return s


# ========================================================================
# 23 — THANK YOU
# ========================================================================
def s23():
    s = Slide(bg=BLUE_D)
    s.add(
        Oval(-1.8, -2.0, 7.0, 7.0, fill="1B4AA8", opacity=0.5),
        Oval(9.2, 3.4, 7.0, 7.0, fill="2A1250", opacity=0.35),
        Oval(9.55, 0.85, 2.5, 2.5, fill=None, line=YELLOW, lw=1.5, opacity=0.45),
        Oval(10.62, 0.85, 2.5, 2.5, fill=None, line=PINK, lw=1.5, opacity=0.45),
        text(0.85, 2.06, 8.0, 0.4, [P(T("THANK YOU", 10.5, True, YELLOW, spacing=3.4))]),
        text(0.85, 2.46, 11.9, 1.6, [P(T("Questions are the best part.", 43, True, WHITE, spacing=-1.2)),
                                     P(T("Please ask us about either model.", 43, True, WHITE, spacing=-1.2))]),
        text(0.85, 4.62, 8.6, 0.9,
             [P(T("We are happy to demonstrate the syringe mechanism and explain any step of the build.",
                  14, False, "C9DBF8"), line=1.35)]),
        Line(0.85, 5.66, 3.0, 5.66, color=YELLOW, lw=2.2),
        text(0.85, 5.86, 9.0, 0.6,
             [P(T("S.D. PUBLIC SCHOOL", 17, True, WHITE, spacing=3.0)),
              P(T("Mathematics  ·  Class XI  ·  Team of 11", 12, False, "9DBBE6"), before=6)]),
    )
    return s


# ========================================================================
# 24 — HOW TO EDIT
# ========================================================================
def s24():
    s = Slide(bg=BG)
    s.add(*section_head("TEMPLATE GUIDE", "How to edit this deck",
                        "Every element is a real PowerPoint shape or text box — nothing is a flat picture of text.",
                        TEAL, 24, "GUIDE"))
    steps = [
        ("Change names", "Team slide: click 'Member 1', type the real name. Repeat for all 11."),
        ("Replace photos", "Click a dashed frame, then Insert > Pictures > This Device, and draw it over the placeholder."),
        ("Edit text", "Anywhere: click once to select the box, again to place the cursor, then type."),
        ("Recolour", "Select a shape, then Shape Format > Shape Fill. Accent colours are listed on the right."),
        ("Add a slide", "Home > New Slide > Blank, then copy-paste an existing slide to keep the style."),
        ("Present", "Slide Show > From Beginning (F5). 16:9 widescreen is already set."),
    ]
    cy = 2.52
    heights = [0.64, 0.80, 0.64, 0.74, 0.64, 0.64]
    for i, (head, body) in enumerate(steps):
        s.add(Oval(0.85, cy + 0.02, 0.34, 0.34, fill=TEAL))
        s.add(text(0.85, cy + 0.02, 0.34, 0.34, [P(T(str(i + 1), 10, True, WHITE), align="c")], anchor="m"))
        s.add(text(1.34, cy - 0.02, 5.0, 0.32, [P(T(head, 12.5, True, INK))]))
        s.add(text(1.34, cy + 0.28, 5.42, heights[i] - 0.26, [P(T(body, 9.5, False, MUT), line=1.18)]))
        cy += heights[i] + 0.06
    # palette + fonts panel
    s.add(Rect(7.28, 2.50, 5.20, 2.44, fill=PANEL, radius=0.16))
    s.add(text(7.56, 2.70, 4.6, 0.3, [P(T("DECK COLOURS", 9, True, MUT, spacing=1.6))]))
    sw = [("Navy", NAVY_BG), ("Blue", BLUE), ("Pink", PINK), ("Violet", VIOLET), ("Teal", TEAL), ("Yellow", YELLOW)]
    for i, (nm, col) in enumerate(sw):
        sx = 7.56 + i * 0.80
        s.add(Rect(sx, 3.02, 0.62, 0.44, fill=col, radius=0.08))
        s.add(text(sx - 0.12, 3.50, 0.86, 0.26, [P(T(nm, 7.5, True, MUT), align="c")]))
    s.add(rule(7.56, 3.90, 4.64, LINE, 1))
    s.add(text(7.56, 4.02, 4.6, 0.3, [P(T("FONTS", 9, True, MUT, spacing=1.6))]))
    s.add(text(7.56, 4.30, 4.6, 0.30, [P(T("Segoe UI", 13, True, INK))]))
    s.add(text(9.90, 4.30, 2.4, 0.30, [P(T("titles & body", 9.5, False, MUT))]))
    s.add(text(7.56, 4.62, 4.6, 0.30, [P(T("Cambria Math", 13, True, INK, font=FONT_M))]))
    s.add(text(9.90, 4.62, 2.4, 0.30, [P(T("symbols & equations", 9.5, False, MUT))]))

    s.add(Rect(7.28, 5.16, 5.20, 1.44, fill=YELLOW_L, radius=0.16))
    s.add(text(7.56, 5.28, 4.7, 1.2,
               [P(T("TIP", 9, True, YELLOW_D, spacing=1.8)),
                P(T("Keep the dashed frames until you are done editing, then send them behind by dragging a "
                    "photo over them — or simply delete the frame once the picture is placed.",
                  9.5, False, "6B5518"), before=4, line=1.28)]))
    return s


# ========================================================================
# 25 — SLIDE INDEX
# ========================================================================
def s25():
    s = Slide(bg=PANEL)
    s.add(*section_head("APPENDIX", "What is on every slide",
                        "A one-page map of the deck, so you can jump straight to the slide you want to change.",
                        MUT, 25, "INDEX"))
    left = [
        ("01", "Cover"), ("02", "Why these models"), ("03", "Team — 11 members"),
        ("04", "Project 01 — Sets"), ("05", "Sets: what it is"), ("06", "Sets: model photo"),
        ("07", "Sets: how it works"), ("08", "Sets: the maths"), ("09", "Sets: while making"),
        ("10", "Sets: real life"), ("11", "Project 02 — Conics"), ("12", "Conics: what it is"),
    ]
    right = [
        ("13", "Conics: model photo"), ("14", "Conics: how it works"), ("15", "Conics: the maths"),
        ("16", "Conics: while making"), ("17", "Conics: real life"), ("18", "The two together"),
        ("19", "Sets: photo wall"), ("20", "Conics: photo wall"), ("21", "Materials"),
        ("22", "What we learned"), ("23", "Thank you"), ("24", "How to edit"),
    ]
    for col, rows in ((0.85, left), (6.85, right)):
        cy = 2.55
        for num, label in rows:
            s.add(text(col, cy, 0.55, 0.3, [P(T(num, 10, True, FAINT, spacing=0.6))]))
            s.add(text(col + 0.52, cy - 0.03, 4.6, 0.3, [P(T(label, 11, True, INK2))]))
            s.add(Line(col + 0.52, cy + 0.26, col + 5.30, cy + 0.26, color=LINE, lw=0.75))
            cy += 0.325
    s.add(text(0.85, 6.60, 8.0, 0.3, [P(T("25 SLIDES   ·   16:9 WIDESCREEN   ·   EVERY ELEMENT EDITABLE",
                                          8.5, True, FAINT, spacing=1.5))]))
    s.add(text(9.20, 6.84, 3.28, 0.3, [P(T("S.D. PUBLIC SCHOOL", 9, True, FAINT, spacing=1.4), align="r")]))
    return s


# ========================================================================
SLIDES = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13,
          s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25]

NAMES = [
    "01_cover", "02_why", "03_team", "04_p1_divider", "05_p1_what", "06_p1_photo",
    "07_p1_how", "08_p1_maths", "09_p1_making", "10_p1_real_life", "11_p2_divider",
    "12_p2_what", "13_p2_photo", "14_p2_how", "15_p2_maths", "16_p2_making",
    "17_p2_real_life", "18_comparison", "19_p1_wall", "20_p2_wall", "21_materials",
    "22_learned", "23_thanks", "24_edit_guide", "25_index",
]


# ------------------------------------------------------------------ notes
NOTES = {
1: "Welcome. Two working models, both from Class XI Mathematics. Each is displayed on its own, with its own explanation.",
2: "Both topics are easy to memorise and hard to picture, so we built each one as something a visitor can watch move.",
3: "Eleven members: three on the Sets model, three on the Conic Sections model, and five on the common work — materials, decoration, photos, explaining and records.",
4: "Project 01 — Sets. Union and intersection, shown with two circles that slide over each other.",
5: "A set is a well-defined collection. Union takes everything, intersection keeps only the common part, difference removes B from A.",
6: "Replace this reference image with your own photograph of the completed board.",
7: "Water pressure pushes a panel fixed to one circle, so the overlap opens and closes. Air is easier to demonstrate quickly; water gives smoother motion.",
8: "n(A ∪ B) = n(A) + n(B) − n(A ∩ B) — the middle is counted twice, so we subtract it once.",
9: "Swap the three frames for workshop photos. The captions describe typical build stages.",
10: "Every database filter, search query and attendance list is really this same question: what belongs to both?",
11: "Project 02 — Conic Sections. A plane cuts a double cone; the angle decides which curve appears.",
12: "Horizontal plane gives a circle, a slight tilt gives an ellipse, parallel to the slant edge gives a parabola, and a steeper tilt cuts both nappes for a hyperbola.",
13: "Replace this reference image with your own photograph of the cone and plane.",
14: "The syringe slides the plane along a rail. Only the angle changes; the cone never moves.",
15: "Standard forms. Eccentricity separates the four: 0 for a circle, below 1 for an ellipse, 1 for a parabola, above 1 for a hyperbola.",
16: "Swap the three frames for workshop photos of the cone build.",
17: "Dishes, headlights, orbits, cooling towers, whispering galleries, lighthouse lenses — all conics.",
18: "The two projects were displayed separately. This page only compares them; the explanations stayed separate.",
19: "Photo wall for Model 01. Replace each dashed frame with a photograph.",
20: "Photo wall for Model 02. Replace each dashed frame with a photograph.",
21: "Both models were built from cheap, local materials. Cutters and glue guns were used under supervision.",
22: "Reflection — what the build taught us beyond the syllabus.",
23: "Thank you. Questions welcome on either model.",
24: "This page is a guide for whoever edits the deck next: names, photos, colours, fonts.",
25: "Appendix index of all 25 slides.",
}
