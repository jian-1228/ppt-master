"""Render a Slide to a PNG preview with PIL (design QA only)."""
from __future__ import annotations

import math
import textwrap
from PIL import Image as PILImage, ImageDraw, ImageFont

from kit import (Slide, Rect, Oval, Poly, Line, Text, Image as ImgItem, Run, Para,
                 W, H, PX, FONT, FONT_M)

FONT_DIR = "/tmp/fonts/ttfs"
FAMILY = {
    "Segoe UI": {"r": "inter", "m": "inter"},
    "Segoe UI Semibold": {"r": "inter", "m": "inter"},
    "Cambria Math": {"r": "dejavu", "m": "dejavu"},
}

_cache: dict = {}


def hexc(c: str, opacity: float = 1.0):
    c = c.replace("#", "")
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return (r, g, b, int(round(opacity * 255)))


def load_font(family: str, bold: bool, size_px: int):
    fam = FAMILY.get(family, {"r": "inter", "m": "inter"})
    key = (fam["r"], bold, size_px)
    if key not in _cache:
        w = "700" if bold else "400"
        if fam["r"] == "dejavu":
            _cache[key] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size_px)
        else:
            _cache[key] = ImageFont.truetype(f"{FONT_DIR}/{fam['r']}-latin-{w}-normal.ttf", size_px)
    return _cache[key]


def pt_to_px(pt: float) -> float:
    return pt * PX / 72.0


import unicodedata
_MATH_CHARS = set("∪∩∈∉⊆⊂−√²³°∞≤≥≠×÷⟂∥∈")


def draw_glyph_safe(dr, txt, x, y, font, color, size_px):
    """Draw text, substituting vector art for glyphs the preview font lacks."""
    for ch in txt:
        if ch in "▸▹●○":
            c = x + measure(ch, font) / 2
            cy = y + size_px * 0.80
            if ch in "▸▹":
                dr.polygon([(c - size_px * 0.16, cy - size_px * 0.20), (c + size_px * 0.18, cy),
                            (c - size_px * 0.16, cy + size_px * 0.20)], fill=color)
                if ch == "○":
                    dr.ellipse((c - size_px * .22, cy - size_px * .22, c + size_px * .22, cy + size_px * .22), outline=color, width=2)
            else:
                dr.ellipse((c - size_px * .22, cy - size_px * .22, c + size_px * .22, cy + size_px * .22), outline=color, width=2)
        elif ch == "₹":
            w = measure("R", font)
            cy = y + size_px * 0.80
            dr.line((x + w * .15, cy - size_px * .52, x + w * .85, cy - size_px * .52), fill=color, width=3)
            dr.line((x + w * .15, y + size_px * .78, x + w * .72, y + size_px * .78), fill=color, width=3)
            dr.line((x + w * .15, y + size_px * .98, x + w * .50, y + size_px * .98), fill=color, width=3)
            dr.text((x, y), "₹", font=font, fill=color)
        else:
            dr.text((x, y), ch, font=font, fill=color)
        x += measure(ch, font)


def _math_split(txt: str):
    """Split a text run into (segment, is_math) pieces so symbols can use a fallback face."""
    if not any(ch in _MATH_CHARS for ch in txt):
        return [(txt, False)]
    out, buf, mode = [], "", None
    for ch in txt:
        m = ch in _MATH_CHARS
        if mode is None or m == mode:
            buf += ch
            mode = m
        else:
            out.append((buf, mode))
            buf, mode = ch, m
    if buf:
        out.append((buf, mode))
    return out


def measure(txt: str, font) -> float:
    if not txt:
        return 0.0
    if any(ch in _MATH_CHARS for ch in txt):
        size = getattr(font, "size", 16)
        mf = load_font("Cambria Math", False, int(size))
        total = 0.0
        for seg, is_math in _math_split(txt):
            total += (mf if is_math else font).getlength(seg)
        return total
    return font.getlength(txt)


def run_width(r, fnt) -> float:
    """Width of a styled run, including letter spacing."""
    base = measure(r.text, fnt)
    if r.spacing:
        base += max(len(r.text) - 1, 0) * r.spacing * PX / 72
    return base


def wrap_runs(runs, font_sets, maxw):
    """Greedy wrap across styled runs; returns list of lines, each a list of (text,font,color)."""
    words = []
    for r, fnt in zip(runs, font_sets):
        parts = r.text.split(" ")
        for i, p in enumerate(parts):
            words.append((p + (" " if i < len(parts) - 1 else ""), fnt, r))
    lines, cur, curw = [], [], 0.0
    for wtext, fnt, r in words:
        wtxt = wtext.rstrip()
        wlen = run_width(r, fnt) * (len(wtext) / max(len(r.text), 1)) if r.spacing else measure(wtext, fnt)
        if cur and curw + wlen > maxw and wtxt:
            lines.append(cur)
            cur, curw = [], 0.0
            wtext = wtxt + (" " if wtext.endswith(" ") else "")
            wlen = measure(wtext, fnt)
        cur.append((wtext, fnt, r))
        curw += wlen
    if cur:
        lines.append(cur)
    return lines or [[]]


def layout_blocks(t: Text):
    """Return (blocks, total_height_px) for a Text item."""
    w, h = t.w * PX, t.h * PX
    blocks = []
    total = 0.0
    for para in t.paras:
        runs = para.runs or [Run("")]
        fonts = [load_font(r.font, r.bold, max(1, int(round(pt_to_px(r.size))))) for r in runs]
        natural = sum(run_width(r, f) for r, f in zip(runs, fonts))
        single = len(para.runs) == 1 and "\n" in para.runs[0].text
        if single:
            raw = para.runs[0].text.split("\n")
            lines = [[(ln, fonts[0], runs[0])] for ln in raw]
        elif natural <= w:
            lines = [[(r.text, f, r) for r, f in zip(runs, fonts)]]
        else:
            lines = wrap_runs(runs, fonts, w)
        leading = max((pt_to_px(r.size) for r in runs), default=16) * 1.22 * para.line
        blocks.append((para, lines, leading))
        total += para.space_before * PX / 72 + leading * len(lines) + para.space_after * PX / 72
    return blocks, total


def draw_text_block(dr, t: Text):
    x, y, w, h = (t.x * PX, t.y * PX, t.w * PX, t.h * PX)
    blocks, total = layout_blocks(t)

    cy = y
    if t.anchor == "m":
        cy = y + (h - total) / 2
    elif t.anchor == "b":
        cy = y + h - total

    for para, lines, leading in blocks:
        cy += para.space_before * PX / 72
        for line in lines:
            lw = sum(run_width(r, f) if txt else 0 for txt, f, r in line)
            lx = x + t.margin * PX
            if para.align == "c":
                lx = x + (w - lw) / 2
            elif para.align == "r":
                lx = x + w - lw - t.margin * PX
            for txt, f, r in line:
                if txt:
                    asc, desc = f.getmetrics()
                    dy = cy + (leading - (asc + desc)) / 2
                    if r.spacing:
                        cx = lx
                        for ch in txt:
                            for seg, is_math in _math_split(ch):
                                fnt = load_font("Cambria Math", r.bold, max(1, int(round(pt_to_px(r.size))))) if is_math else f
                                dr.text((cx, dy), seg, font=fnt, fill=hexc(r.color))
                                cx += measure(seg, fnt)
                            cx += r.spacing * PX / 72
                    else:
                        for seg, is_math in _math_split(txt):
                            fnt = load_font("Cambria Math", r.bold, max(1, int(round(pt_to_px(r.size))))) if is_math else f
                            dr.text((lx, dy), seg, font=fnt, fill=hexc(r.color))
                            lx += measure(seg, fnt)
                        if r.spacing:
                            lx -= r.spacing * PX / 72 * 0.0
            cy += leading
        cy += para.space_after * PX / 72


def rounded(dr, box, radius, fill=None, outline=None, width=1):
    dr.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=int(max(1, width)))


def draw_shadow_rect(img, dr, box, radius, color, spread=10):
    lay = PILImage.new("RGBA", img.size, (0, 0, 0, 0))
    d2 = ImageDraw.Draw(lay)
    r, g, b, a = color
    for i in range(spread, 0, -2):
        d2.rounded_rectangle(
            (box[0] - i * 0.5, box[1] + i * 0.9, box[2] + i * 0.5, box[3] + i * 0.75),
            radius=radius + i * 0.4, fill=(r, g, b, int(a * 0.30 * (1 - i / spread) + 4)))
    img.alpha_composite(lay)


def draw_slide(slide: Slide, scale: float = 1.0):
    Wp, Hp = int(W * PX * scale), int(H * PX * scale)
    img = PILImage.new("RGBA", (Wp, Hp), hexc(slide.bg))
    dr = ImageDraw.Draw(img)
    for it in slide.items:
        translucent = getattr(it, "opacity", 1.0) < 1.0
        if translucent:
            lay = PILImage.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
            _draw_item(ImageDraw.Draw(lay), lay, it, scale, opacity=it.opacity)
            img.alpha_composite(lay)
            dr = ImageDraw.Draw(img)
            continue
        _draw_item(dr, img, it, scale)
        dr = ImageDraw.Draw(img)
    return img.convert("RGB")


def _draw_item(dr, img, it, scale, opacity=1.0):
    if True:
        if isinstance(it, Rect):
            box = (it.x * PX * scale, it.y * PX * scale,
                   (it.x + it.w) * PX * scale, (it.y + it.h) * PX * scale)
            rad = it.radius * PX * scale
            if it.shadow:
                draw_shadow_rect(img, dr, box, rad, hexc("0A1830", 0.55))
                dr = ImageDraw.Draw(img)
            fill = hexc(it.fill, opacity) if it.fill else None
            if it.line:
                lw = max(1, it.lw * PX * scale / 72)
                if it.dash:
                    if rad > 2:
                        rounded(dr, box, rad, fill=fill)
                        _dash_round_rect(dr, box, rad, hexc(it.line, opacity), lw, it.dash)
                    else:
                        _dash_line(dr, box[0], box[1], box[2], box[1], hexc(it.line), lw, it.dash)
                        _dash_line(dr, box[0], box[3], box[2], box[3], hexc(it.line), lw, it.dash)
                        _dash_line(dr, box[0], box[1], box[0], box[3], hexc(it.line), lw, it.dash)
                        _dash_line(dr, box[2], box[1], box[2], box[3], hexc(it.line), lw, it.dash)
                else:
                    if rad > 2:
                        rounded(dr, box, rad, fill=fill, outline=hexc(it.line, opacity), width=lw)
                        fill = None
                    else:
                        dr.rectangle(box, fill=fill, outline=hexc(it.line, opacity), width=int(max(1, lw)))
                        fill = None
            if fill:
                if rad > 2:
                    rounded(dr, box, rad, fill=fill)
                else:
                    dr.rectangle(box, fill=fill)
        elif isinstance(it, Oval):
            box = (it.x * PX * scale, it.y * PX * scale,
                   (it.x + it.w) * PX * scale, (it.y + it.h) * PX * scale)
            if it.shadow:
                draw_shadow_rect(img, dr, box, box[3] - box[1], hexc("0A1830", 0.5))
                dr = ImageDraw.Draw(img)
            fill = hexc(it.fill, opacity) if it.fill else None
            lw = max(1, it.lw * PX * scale / 72)
            outline = hexc(it.line, it.opacity) if it.line else None
            if it.line and it.dash:
                _dash_ellipse(dr, box, outline, lw, it.dash)
                if fill:
                    dr.ellipse(box, fill=fill)
            else:
                dr.ellipse(box, fill=fill, outline=outline, width=int(lw))
        elif isinstance(it, Poly):
            pts = [(px * PX * scale, py * PX * scale) for px, py in it.pts]
            fill = hexc(it.fill, opacity) if it.fill else None
            outline = hexc(it.line, it.opacity) if it.line else None
            lw = max(1, int(it.lw * PX * scale / 72))
            if it.close:
                dr.polygon(pts, fill=fill, outline=outline)
                if it.line:
                    dr.line(pts + [pts[0]], fill=outline, width=lw, joint="curve")
            else:
                dr.line(pts, fill=outline or (0, 0, 0, 255), width=lw, joint="curve")
        elif isinstance(it, Line):
            x1, y1 = it.x1 * PX * scale, it.y1 * PX * scale
            x2, y2 = it.x2 * PX * scale, it.y2 * PX * scale
            col = hexc(it.color, opacity)
            lw = max(1, it.lw * PX * scale / 72)
            if it.dash:
                _dash_line(dr, x1, y1, x2, y2, col, lw, it.dash)
            else:
                dr.line((x1, y1, x2, y2), fill=col, width=int(round(lw)))
            if it.arrow:
                ang = math.atan2(y2 - y1, x2 - x1)
                ln = max(9, lw * 4.2)
                for s in (0.42, -0.42):
                    ex = x2 - ln * math.cos(ang - s)
                    ey = y2 - ln * math.sin(ang - s)
                    dr.line((x2, y2, ex, ey), fill=col, width=int(round(lw)))
        elif isinstance(it, ImgItem):
            im = PILImage.open(it.path).convert("RGBA")
            tw, th = int(it.w * PX * scale), int(it.h * PX * scale)
            im = im.resize((tw, th), PILImage.LANCZOS)
            if it.opacity < 1:
                a = im.getchannel("A").point(lambda v: int(v * it.opacity))
                im.putalpha(a)
            img.alpha_composite(im, (int(it.x * PX * scale), int(it.y * PX * scale)))
            dr = ImageDraw.Draw(img)
        elif isinstance(it, Text):
            draw_text_block(dr, it)


def _dash_line(dr, x1, y1, x2, y2, color, width, dash):
    on, off = (10, 7) if dash == "dash" else (3, 5)
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    if ln == 0:
        return
    ux, uy = dx / ln, dy / ln
    t = 0.0
    while t < ln:
        e = min(t + on, ln)
        dr.line((x1 + ux * t, y1 + uy * t, x1 + ux * e, y1 + uy * e),
                fill=color, width=int(round(width)))
        t = e + off


def _dash_round_rect(dr, box, rad, color, width, dash):
    x0, y0, x1, y1 = box
    _dash_line(dr, x0 + rad, y0, x1 - rad, y0, color, width, dash)
    _dash_line(dr, x0 + rad, y1, x1 - rad, y1, color, width, dash)
    _dash_line(dr, x0, y0 + rad, x0, y1 - rad, color, width, dash)
    _dash_line(dr, x1, y0 + rad, x1, y1 - rad, color, width, dash)


def _dash_ellipse(dr, box, color, width, dash):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    on, off = (10, 7)
    n = max(24, int((rx + ry) / 2))
    step = 2 * math.pi / n
    k = 0
    while k < n:
        a0 = k * step
        a1 = min((k + on / 8) * step, 2 * math.pi)
        dr.arc(box, math.degrees(a0) - 90, math.degrees(a1) - 90,
               fill=color, width=int(round(width)))
        k += (on + off) / 8


# ------------------------------------------------------------------ QA
def qa_slide(idx: int, slide: Slide, tol: float = 0.02):
    """Report text overflow and out-of-canvas items."""
    issues = []
    for it in slide.items:
        if isinstance(it, Text):
            _, total_px = layout_blocks(it)
            total_in = total_px / PX
            if total_in > it.h + tol:
                snippet = "".join(r.text for p in it.paras for r in p.runs)[:46]
                issues.append(f"  [TEXT OVERFLOW] p{idx} box {it.x:.2f},{it.y:.2f} "
                              f"{it.w:.2f}x{it.h:.2f}: needs {total_in:.2f}in  '{snippet}'")
            if it.x < -0.05 or it.y < -0.05 or it.x + it.w > W + 0.05 or it.y + it.h > H + 0.05:
                issues.append(f"  [TEXT OUTSIDE] p{idx} box {it.x:.2f},{it.y:.2f} {it.w:.2f}x{it.h:.2f}")
        elif isinstance(it, (Rect, Oval, ImgItem)):
            if it.x < -0.06 or it.y < -0.06 or it.x + it.w > W + 0.06 or it.y + it.h > H + 0.06:
                issues.append(f"  [SHAPE OUTSIDE] p{idx} {type(it).__name__} "
                              f"{it.x:.2f},{it.y:.2f} {it.w:.2f}x{it.h:.2f}")
        elif isinstance(it, Poly):
            for px, py in it.pts:
                if px < -0.06 or py < -0.06 or px > W + 0.06 or py > H + 0.06:
                    issues.append(f"  [POLY OUTSIDE] p{idx} point {px:.2f},{py:.2f}")
                    break
        elif isinstance(it, Line):
            for px, py in ((it.x1, it.y1), (it.x2, it.y2)):
                if px < -0.06 or py < -0.06 or px > W + 0.06 or py > H + 0.06:
                    issues.append(f"  [LINE OUTSIDE] p{idx} point {px:.2f},{py:.2f}")
                    break
    return issues
