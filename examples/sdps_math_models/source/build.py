import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import deck
from render import draw_slide, qa_slide
from emit import build

OUT = Path(__file__).resolve().parent.parent
prev = OUT / "preview"; prev.mkdir(exist_ok=True)
issues, slides = [], []
for i, fn in enumerate(deck.SLIDES, 1):
    s = fn(); slides.append(s)
    draw_slide(s).save(prev / f"{i:02d}.png")
    issues += qa_slide(i, s)

print("\n".join(issues) if issues else "QA: no overflow / out-of-canvas items")
out = OUT / "SDPublicSchool_Maths_Models_ClassXI.pptx"
build(slides, str(out), title="Two Maths Working Models — S.D. Public School")
print("built", len(slides), "slides")
