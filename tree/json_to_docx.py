# json_to_docx.py
import json, os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_LINE_SPACING
from docx.shared import Pt, RGBColor
from docx.oxml.shared import OxmlElement, qn
from docx.table import _Cell

ALIGN_MAP = {
    "LEFT": WD_ALIGN_PARAGRAPH.LEFT,
    "CENTER": WD_ALIGN_PARAGRAPH.CENTER,
    "RIGHT": WD_ALIGN_PARAGRAPH.RIGHT,
    "JUSTIFY": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

HIGHLIGHT_MAP = {k: getattr(WD_COLOR_INDEX, k) for k in WD_COLOR_INDEX.__members__}

def hex_to_rgbcolor(hexstr: str | None):
    if not hexstr:
        return None
    s = hexstr.strip().lstrip("#")
    if len(s) == 6:
        return RGBColor.from_string(s)
    return None

def apply_run_style(run, rdict):
    f = run.font
    f.bold = rdict.get("bold") or False
    f.italic = rdict.get("italic") or False
    f.underline = rdict.get("underline") or False
    if rdict.get("strike"):  # optional
        try:
            f.strike = True
        except Exception:
            pass
    if rdict.get("size_pt"):
        f.size = Pt(float(rdict["size_pt"]))
    if rdict.get("font"):
        f.name = rdict["font"]
    rgb = hex_to_rgbcolor(rdict.get("color"))
    if rgb:
        f.color.rgb = rgb
    hl = rdict.get("highlight")
    if hl and hl in HIGHLIGHT_MAP:
        f.highlight_color = HIGHLIGHT_MAP[hl]

def apply_paragraph_spacing(p, spacing_dict):
    if not spacing_dict:
        return
    pf = p.paragraph_format
    sb = spacing_dict.get("space_before_pt")
    sa = spacing_dict.get("space_after_pt")
    ls = spacing_dict.get("line_spacing")
    lr = spacing_dict.get("line_spacing_rule")

    if sb is not None:
        pf.space_before = Pt(float(sb))
    if sa is not None:
        pf.space_after = Pt(float(sa))

    # line spacing rule first, then value if MULTIPLE or EXACT values
    if lr:
        try:
            pf.line_spacing_rule = getattr(WD_LINE_SPACING, lr)
        except Exception:
            pass

    if ls is not None:
        # If rule is MULTIPLE, Word expects a float like 1.0, 1.15, 1.5, 2.0
        # If rule is AT_LEAST/EXACTLY, python-docx expects a length (pt).
        if pf.line_spacing_rule == WD_LINE_SPACING.MULTIPLE:
            pf.line_spacing = float(ls)
        else:
            # treat as points
            pf.line_spacing = Pt(float(ls))

def apply_list_numbering(p, list_dict):
    """
    Set w:numPr on the paragraph.
    IMPORTANT: the output doc must come from a template that already has
    the numbering definitions for these numId values.
    """
    if not list_dict:
        return
    num_id = list_dict.get("numId")
    ilvl = list_dict.get("ilvl", 0)
    if num_id is None:
        return

    pPr = p._p.get_or_add_pPr()
    # remove existing numPr if any
    for child in list(pPr):
        if child.tag == qn("w:numPr"):
            pPr.remove(child)

    numPr = OxmlElement("w:numPr")
    ilvl_el = OxmlElement("w:ilvl")
    ilvl_el.set(qn("w:val"), str(ilvl))
    numId_el = OxmlElement("w:numId")
    numId_el.set(qn("w:val"), str(num_id))
    numPr.append(ilvl_el)
    numPr.append(numId_el)
    pPr.append(numPr)

def add_paragraph_block(container, bdict):
    # container can be Document or _Cell
    p = container.add_paragraph("")
    # style first (so spacing defaults are correct if styles carry them)
    if bdict.get("style"):
        try:
            p.style = bdict["style"]
        except Exception:
            pass
    # alignment
    a = bdict.get("alignment")
    if a and a in ALIGN_MAP:
        p.alignment = ALIGN_MAP[a]

    # NEW: spacing
    apply_paragraph_spacing(p, bdict.get("spacing"))

    # runs
    for r in bdict.get("runs", []):
        run = p.add_run(r.get("text", ""))
        apply_run_style(run, r)

    # NEW: apply numbering last
    apply_list_numbering(p, bdict.get("list"))

    return p


def add_table_block(doc, bdict):
    rows = bdict["rows"]
    t = doc.add_table(rows=len(rows), cols=len(rows[0]) if rows else 0)
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            # replay cell blocks (paragraphs)
            # clear the default empty paragraph
            cell_obj = t.cell(ri, ci)
            cell_obj.text = ""
            for cb in cell.get("blocks", []):
                if cb.get("type") == "paragraph":
                    add_paragraph_block(cell_obj, cb)
    return t

# Allow add_paragraph_block to work with table cell as "doc-like"
from docx.table import _Cell
def add_paragraph_block(cell_or_doc, bdict):
    if isinstance(cell_or_doc, _Cell):
        p = cell_or_doc.add_paragraph("")
    else:
        p = cell_or_doc.add_paragraph("")
    if bdict.get("style"):
        try:
            p.style = bdict["style"]
        except Exception:
            pass
    a = bdict.get("alignment")
    if a and a in ALIGN_MAP:
        p.alignment = ALIGN_MAP[a]
    for r in bdict.get("runs", []):
        run = p.add_run(r.get("text", ""))
        apply_run_style(run, r)
    return p

def json_to_docx(json_path: str, docx_out: str, template: str | None = None):
    data = json.load(open(json_path, "r", encoding="utf-8"))
    doc = Document(template) if template else Document()
    for b in data["document"]["blocks"]:
        btype = b.get("type")
        if btype == "paragraph":
            add_paragraph_block(doc, b)
        elif btype == "table":
            add_table_block(doc, b)
        elif btype == "page_break":
            doc.add_page_break()
        else:
            # ignore unknown block types
            pass
    os.makedirs(os.path.dirname(docx_out) or ".", exist_ok=True)
    doc.save(docx_out)
    print(f"Wrote {docx_out}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python json_to_docx.py input.json output.docx [optional_template.docx]")
        raise SystemExit(2)
    in_json, out_docx = sys.argv[1], sys.argv[2]
    template = sys.argv[3] if len(sys.argv) > 3 else None
    json_to_docx(in_json, out_docx, template)
