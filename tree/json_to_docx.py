# json_to_docx.py
import json, os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.shared import Pt, RGBColor

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

def add_paragraph_block(doc, bdict):
    p = doc.add_paragraph("")
    # restore style first (important for lists/numbering/headings)
    if bdict.get("style"):
        try:
            p.style = bdict["style"]
        except Exception:
            # style might not exist in this template; fall back to Normal
            pass
    # alignment
    a = bdict.get("alignment")
    if a and a in ALIGN_MAP:
        p.alignment = ALIGN_MAP[a]
    # runs
    for r in bdict.get("runs", []):
        run = p.add_run(r.get("text", ""))
        apply_run_style(run, r)
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
