"""Emit native, fully editable DrawingML PPTX from Slide specs."""
from __future__ import annotations

from pptx import Presentation
from pptx.util import Emu, Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from lxml import etree
import copy

from kit import (Slide, Rect, Oval, Poly, Line, Text, Image as ImgItem,
                 W, H, FONT, FONT_M, INK)

CW, CH = 12192000, 6858000     # 16:9 widescreen EMU
ALIGN = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}
ANCHOR = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}
DASH = {"dash": MSO_LINE_DASH_STYLE.DASH, "sysdash": MSO_LINE_DASH_STYLE.SQUARE_DOT,
        "dot": MSO_LINE_DASH_STYLE.ROUND_DOT, "lgdash": MSO_LINE_DASH_STYLE.LONG_DASH}


def E(inches: float) -> Emu:
    return Emu(int(round(inches * 914400)))


def rgb(h: str) -> RGBColor:
    h = h.replace("#", "")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _no_effects(shape):
    spPr = shape._element.spPr
    if spPr.find(qn("a:effectLst")) is None:
        spPr.append(etree.SubElement(spPr, qn("a:effectLst")))


def soft_shadow(shape, blur_pt=18, dist_pt=5, dir_deg=90, alpha=0.13):
    spPr = shape._element.spPr
    for tag in ("a:effectLst",):
        old = spPr.find(qn(tag))
        if old is not None:
            spPr.remove(old)
    eff = etree.SubElement(spPr, qn("a:effectLst"))
    shd = etree.SubElement(eff, qn("a:outerShdw"))
    shd.set("blurRad", str(int(blur_pt * 12700)))
    shd.set("dist", str(int(dist_pt * 12700)))
    shd.set("dir", str(int(dir_deg * 60000)))
    shd.set("algn", "ctr")
    shd.set("rotWithShape", "0")
    c = etree.SubElement(shd, qn("a:srgbClr"))
    c.set("val", "0A1830")
    a = etree.SubElement(c, qn("a:alpha"))
    a.set("val", str(int(alpha * 100000)))


def fix_geometry(shape, radius_in):
    """Force exact w/h and a true rounded rectangle for non-square boxes."""
    if radius_in and radius_in > 0:
        w, h = shape.width, shape.height
        short = min(w, h)
        val = min(0.5, max(0.0, (radius_in * 914400) / short)) if short else 0
        shape.adjustments[0] = val


def prepare_prs(prs, bg_color=None):
    prs.slide_width, prs.slide_height = Emu(CW), Emu(CH)
    # kill default placeholders / 4:3 geometry inherited from the template
    layout = prs.slide_layouts[6]
    for idx in range(len(prs.slide_layouts)):
        lay = prs.slide_layouts[idx]
        for sp in list(lay.shapes):
            sp._element.getparent().remove(sp._element)
        for mp in list(lay.placeholders):
            mp._element.getparent().remove(mp._element)
    master = prs.slide_master
    for sp in list(master.shapes):
        if sp.shape_type is not None and not sp.has_text_frame:
            try:
                sp._element.getparent().remove(sp._element)
            except Exception:
                pass
    for sp in list(master.placeholders):
        try:
            sp._element.getparent().remove(sp._element)
        except Exception:
            pass
    try:
        master.background.fill.solid()
        master.background.fill.fore_color.rgb = rgb(bg_color or "FFFFFF")
    except Exception:
        pass
    return prs


def new_prs():
    prs = Presentation()
    return prepare_prs(prs)


def add_slide(prs, bg="FFFFFF"):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    fill = s.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(bg)
    return s


def _apply_fill(shape, color, opacity=1.0):
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(color)
    if opacity < 1.0:
        srgb = shape.fill.fore_color._xFill.find(qn("a:srgbClr"))
        if srgb is not None:
            a = etree.SubElement(srgb, qn("a:alpha"))
            a.set("val", str(int(opacity * 100000)))


def _apply_line(shape, color, lw, dash=None):
    if color is None:
        shape.line.fill.background()
        return
    shape.line.color.rgb = rgb(color)
    shape.line.width = Pt(lw)
    if dash:
        shape.line.dash_style = DASH.get(dash, MSO_LINE_DASH_STYLE.DASH)


def emit_shape(container, it):
    if isinstance(it, Rect):
        kind = MSO_SHAPE.ROUNDED_RECTANGLE if it.radius and it.radius > 0 else MSO_SHAPE.RECTANGLE
        sh = container.shapes.add_shape(kind, E(it.x), E(it.y), max(E(it.w), 1), max(E(it.h), 1))
        fix_geometry(sh, it.radius)
    elif isinstance(it, Oval):
        sh = container.shapes.add_shape(MSO_SHAPE.OVAL, E(it.x), E(it.y), max(E(it.w), 1), max(E(it.h), 1))
    elif isinstance(it, Poly):
        xs = [p[0] for p in it.pts]
        ys = [p[1] for p in it.pts]
        x0, y0 = min(xs), min(ys)
        w, h = max(max(xs) - x0, 0.008), max(max(ys) - y0, 0.008)
        fb = container.shapes.build_freeform(E(it.pts[0][0]), E(it.pts[0][1]), scale=1.0)
        fb.add_line_segments([(E(px), E(py)) for px, py in it.pts[1:]], close=it.close)
        sh = fb.convert_to_shape(origin_x=E(x0), origin_y=E(y0))
        sh.left, sh.top, sh.width, sh.height = E(x0), E(y0), E(w), E(h)
    elif isinstance(it, Line):
        x0, y0 = min(it.x1, it.x2), min(it.y1, it.y2)
        x1, y1 = max(it.x1, it.x2), max(it.y1, it.y2)
        if abs(it.x2 - it.x1) >= abs(it.y2 - it.y1):
            sh = container.shapes.add_connector(1, E(it.x1), E(it.y1), E(it.x2), E(it.y2))
            if it.x2 < it.x1:
                sh._element.spPr.find(qn("a:xfrm")).set("flipH", "1")
            if abs(it.y2 - it.y1) > 0.001 and it.y2 < it.y1:
                sh._element.spPr.find(qn("a:xfrm")).set("flipV", "1")
        else:
            sh = container.shapes.add_connector(1, E(it.x1), E(it.y1), E(it.x2), E(it.y2))
            if it.y2 < it.y1:
                sh._element.spPr.find(qn("a:xfrm")).set("flipV", "1")
            if it.x2 < it.x1:
                sh._element.spPr.find(qn("a:xfrm")).set("flipH", "1")
        sh.line.color.rgb = rgb(it.color)
        sh.line.width = Pt(it.lw)
        if it.dash:
            sh.line.dash_style = DASH.get(it.dash, MSO_LINE_DASH_STYLE.DASH)
        if it.arrow:
            ln = sh.line._get_or_add_ln()
            tail = etree.SubElement(ln, qn("a:tailEnd"))
            tail.set("type", "triangle")
            tail.set("w", "med")
            tail.set("len", "med")
        if it.opacity < 1:
            srgb = sh.line.color._xFill.find(qn("a:srgbClr"))
            if srgb is not None:
                a = etree.SubElement(srgb, qn("a:alpha"))
                a.set("val", str(int(it.opacity * 100000)))
        return sh

    if it.fill:
        _apply_fill(sh, it.fill, it.opacity)
    else:
        sh.fill.background()
    _apply_line(sh, it.line, it.lw, it.dash)
    if it.shadow:
        soft_shadow(sh)
    else:
        _no_effects(sh)
    sh.text_frame.word_wrap = True
    return sh


def emit_image(container, it):
    return container.shapes.add_picture(it.path, E(it.x), E(it.y), E(it.w), E(it.h))


def emit_text(container, t: Text):
    box = container.shapes.add_textbox(E(t.x), E(t.y), max(E(t.w), 1), max(E(t.h), 1))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = ANCHOR[t.anchor]
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Emu(int(t.margin * 914400)))
    for i, para in enumerate(t.paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = ALIGN[para.align]
        if para.space_before:
            p.space_before = Pt(para.space_before)
        if para.space_after:
            p.space_after = Pt(para.space_after)
        if para.line and para.line != 1.0:
            p.line_spacing = para.line
        for r in para.runs:
            run = p.add_run()
            run.text = r.text
            f = run.font
            f.size = Pt(r.size)
            f.bold = r.bold
            f.italic = r.italic
            f.name = r.font
            f.color.rgb = rgb(r.color)
            if r.spacing:
                rPr = run._r.get_or_add_rPr()
                rPr.set("spc", str(int(r.spacing * 100)))
            # make sure East-Asian/complex-script slots share the latin font
            rPr = run._r.get_or_add_rPr()
            for tag in ("a:ea", "a:cs"):
                el = rPr.find(qn(tag))
                if el is None:
                    el = etree.SubElement(rPr, qn(tag))
                el.set("typeface", r.font)
    return box


def build(slides: list[Slide], out_path: str, title="", author="S.D. Public School"):
    prs = new_prs()
    for s in slides:
        sl = add_slide(prs, s.bg)
        for it in s.items:
            if isinstance(it, Text):
                emit_text(sl, it)
            elif isinstance(it, ImgItem):
                emit_image(sl, it)
            else:
                emit_shape(sl, it)
        if s.notes:
            sl.notes_slide.notes_text_frame.text = s.notes
        if s.seconds:
            sl._element.set("data-auto", str(s.seconds))
    cp = prs.core_properties
    cp.title, cp.author, cp.subject = title, author, "Maths Working Models — Team Project"
    prs.save(out_path)
    return out_path
