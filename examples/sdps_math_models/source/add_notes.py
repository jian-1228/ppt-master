import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from pptx import Presentation
from deck import NOTES

path = Path(__file__).resolve().parent.parent / "SDPublicSchool_Maths_Models_ClassXI.pptx"
prs = Presentation(str(path))
for i, slide in enumerate(prs.slides, 1):
    note = NOTES.get(i, "")
    if note:
        slide.notes_slide.notes_text_frame.text = note
prs.save(str(path))
print("notes added:", len(prs.slides))
