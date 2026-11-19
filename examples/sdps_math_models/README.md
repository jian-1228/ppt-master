# S.D. Public School — Two Maths Working Models (Class XI)

Editable PowerPoint deck for the Maths Exhibition 2025–26.
**Deliverable:** `SDPublicSchool_Maths_Models_ClassXI.pptx` (same folder as this README)

---

## What is in the deck (25 slides, 16:9)

| # | Slide | What to do with it |
|---|---|---|
| 01 | Cover | Nothing — team name already there |
| 02 | Why these two models | Optional wording edits |
| 03 | **Team — all 11 members** | Type the 11 real names |
| 04 | Project 01 divider — Sets | Nothing |
| 05 | Sets: what it is | Nothing |
| 06 | Sets: model photo | Replace the reference illustration with your photo |
| 07 | Sets: how it works | Nothing |
| 08 | Sets: the maths | Nothing |
| 09 | Sets: while making | Replace the 3 small photo frames |
| 10 | Sets: real life | Nothing |
| 11 | Project 02 divider — Conics | Nothing |
| 12 | Conics: what it is | Nothing |
| 13 | Conics: model photo | Replace the reference illustration with your photo |
| 14 | Conics: how it works | Nothing |
| 15 | Conics: the maths | Nothing |
| 16 | Conics: while making | Replace the 3 small photo frames |
| 17 | Conics: real life | Nothing |
| 18 | The two together (comparison) | Nothing |
| 19 | Sets: photo wall (6 frames) | Replace all 6 |
| 20 | Conics: photo wall (6 frames) | Replace all 6 |
| 21 | Materials | Nothing |
| 22 | What we learned | Optional — add your own lessons |
| 23 | Thank you | Nothing |
| 24 | How to edit this deck | Read it once |
| 25 | Slide index | Reference |

Every slide also has **speaker notes** with a one-line explanation of what to say.

---

## How to replace the photos (3 steps)

1. Click a **dashed photo frame** (the one that says "PHOTO — insert here").
2. **Insert ▸ Pictures ▸ This Device**, choose your photo.
3. With the photo still selected, drag its corners so it covers the frame.
   Then either delete the dashed frame, or right-click the frame ▸ **Send to Back**.

Tip: hold **Shift** while dragging a corner to keep the photo from stretching.

Reference illustrations on slides 04, 06, 09, 11, 13 and 16 are normal pictures —
click and press **Delete** once your own photo is in place.

---

## The 11 names — fill this in, then retype on slide 3

| Card | Role already written | Real name |
|---|---|---|
| Member 1 | Design & structure (Sets) | |
| Member 2 | Cutting & assembly (Sets) | |
| Member 3 | Mechanism & testing (Sets) | |
| Member 4 | Cone construction (Conics) | |
| Member 5 | Plane & syringe drive (Conics) | |
| Member 6 | Sections & finishing (Conics) | |
| Member 7 | Materials & purchase (Common) | |
| Member 8 | Decoration & display (Common) | |
| Member 9 | Photos & documentation (Common) | |
| Member 10 | Explaining to visitors (Common) | |
| Member 11 | Team lead & records (Common) | |

The small circles (M1–M11) are placeholders. If you want real photos there:
click a circle ▸ **Shape Format ▸ Shape Fill ▸ Picture**.

---

## Design system (so new slides match)

**Canvas:** 16:9 widescreen, 13.333 × 7.5 in
**Fonts:** Segoe UI (titles and body), Cambria Math (∪ ∩ ∈ and equations)
**Colour roles**

| Role | Hex | Used for |
|---|---|---|
| Navy | `0C1730` | Cover, reflection, thank-you backgrounds |
| Blue | `1D4ED8` | Project 01 accent |
| Violet | `6D3BD6` | Project 02 accent |
| Pink | `E8407E` | Intersection / highlight |
| Teal | `0F766E` | Common-work accent |
| Yellow | `F7C531` | Warm accent, callouts |
| Panel | `F4F7FC` | Card backgrounds |
| Line | `DCE4EF` | Hairlines and card borders |

**Type scale (pt):** slide title 37 · section number/tag 10.5 · card title 13–15 ·
body 11–13 · caption 9–10.5 · footer 9.5

To add a slide: **Home ▸ New Slide ▸ Blank**, then copy-paste an existing slide
and edit it. Nothing is locked, and there is no master/layout dependency.

---

## Reproducing the file

The generator lives in `source/` (not needed to use the deck):

```bash
cd examples/sdps_math_models/source
python3 build.py     # rebuilds previews + ../SDPublicSchool_Maths_Models_ClassXI.pptx
python3 add_notes.py # re-attaches speaker notes after a rebuild
```

The build writes the `.pptx` next to this README (plus a throwaway `preview/`
folder of PNGs you can delete).

- `kit.py` — scene primitives, palette, type scale
- `deck.py` — the 25 slides + speaker notes
- `emit.py` — native DrawingML writer (python-pptx)
- `render.py` — PIL preview + overflow QA

Validation performed: 981 native shapes, 6 pictures, 13,207 characters of real
text, 0 text overflow in PowerPoint metrics, and
`pptx_delivery_check.py` reports **passed** with no errors or advisories.
