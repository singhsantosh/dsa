# json_to_docx.py
import json, os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_LINE_SPACING
from docx.shared import Pt, RGBColor
from docx.table import _Cell
from docx.oxml.shared import OxmlElement, qn



ALIGN_MAP = {
    "LEFT": WD_ALIGN_PARAGRAPH.LEFT,
    "CENTER": WD_ALIGN_PARAGRAPH.CENTER,
    "RIGHT": WD_ALIGN_PARAGRAPH.RIGHT,
    "JUSTIFY": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

HIGHLIGHT_MAP = {k: getattr(WD_COLOR_INDEX, k) for k in WD_COLOR_INDEX.__members__}

def apply_paragraph_indents(p, indents_dict, list_dict):
    """
    Apply left/first-line indent only if this paragraph is NOT a list item.
    List levels already carry their own indentation—combining both causes double-indenting.
    """
    if not indents_dict:
        return
    if list_dict:  # skip to avoid double indent for numbered/bulleted items
        return
    pf = p.paragraph_format
    li = indents_dict.get("left_indent_pt")
    fi = indents_dict.get("first_line_indent_pt")
    if li is not None:
        pf.left_indent = Pt(float(li))
    if fi is not None:
        pf.first_line_indent = Pt(float(fi))

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
    if rdict.get("strike"):
        try: f.strike = True
        except Exception: pass
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
    if sb is not None: pf.space_before = Pt(float(sb))
    if sa is not None: pf.space_after  = Pt(float(sa))
    if lr:
        try: pf.line_spacing_rule = getattr(WD_LINE_SPACING, lr)
        except Exception: pass
    if ls is not None:
        if getattr(pf, "line_spacing_rule", None) == WD_LINE_SPACING.MULTIPLE:
            pf.line_spacing = float(ls)
        else:
            pf.line_spacing = Pt(float(ls))

def apply_list_numbering(p, list_dict):
    """Try true numbering first (requires numbering definitions); return True if applied."""
    if not list_dict:
        return False
    num_id = list_dict.get("numId")
    ilvl   = list_dict.get("ilvl", 0)
    if num_id is None:
        return False
    try:
        # Ensure numbering part exists; will if using a template with numbering
        _ = p.part.numbering_part
    except Exception:
        return False

    try:
        pPr = p._p.get_or_add_pPr()
        for child in list(pPr):
            if child.tag == qn("w:numPr"):
                pPr.remove(child)
        numPr = OxmlElement("w:numPr")
        ilvl_el = OxmlElement("w:ilvl");  ilvl_el.set(qn("w:val"), str(ilvl))
        numId_el = OxmlElement("w:numId"); numId_el.set(qn("w:val"), str(num_id))
        numPr.append(ilvl_el); numPr.append(numId_el)
        pPr.append(numPr)
        return True
    except Exception:
        return False

def fallback_list_style(p, list_dict):
    """If true numbering couldn't be applied, force a visible list via built-in styles."""
    if not list_dict:
        return
    fmt = (list_dict.get("fmt") or "").lower()
    try:
        if fmt == "bullet":
            p.style = "List Bullet"
        else:
            # treat decimal/alpha/roman etc. as numbered
            p.style = "List Number"
    except Exception:
        pass

def add_paragraph_block(container, bdict):
    p = (container.add_paragraph("") if not isinstance(container, _Cell) else container.add_paragraph(""))

    # style first (keeps default spacing if style defines it)
    if bdict.get("style"):
        try: p.style = bdict["style"]
        except Exception: pass

    # alignment + spacing
    a = bdict.get("alignment")
    if a and a in ALIGN_MAP: p.alignment = ALIGN_MAP[a]
    apply_paragraph_spacing(p, bdict.get("spacing"))

    # NEW: apply indents only for non-list paras
    apply_paragraph_indents(p, bdict.get("indents"), bdict.get("list"))

    # runs
    for r in bdict.get("runs", []):
        run = p.add_run(r.get("text", ""))
        apply_run_style(run, r)

    # numbering: true numPr or fallback style
    if not apply_list_numbering(p, bdict.get("list")):
        fallback_list_style(p, bdict.get("list"))

    return p


def add_table_block(doc, bdict):
    rows = bdict["rows"]
    t = doc.add_table(rows=len(rows), cols=len(rows[0]) if rows else 0)
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            cell_obj = t.cell(ri, ci)
            cell_obj.text = ""  # clear default paragraph
            for cb in cell.get("blocks", []):
                if cb.get("type") == "paragraph":
                    add_paragraph_block(cell_obj, cb)
    return t

def clear_document_body(doc):
    body = doc._element.body
    sectPr = None
    for child in list(body):
        if child.tag == qn("w:sectPr"):
            sectPr = child
        body.remove(child)
    if sectPr is not None:
        body.append(sectPr)

def remove_initial_blank_paragraph(doc):
    if len(doc.paragraphs) == 1 and doc.paragraphs[0].text == "":
        p = doc.paragraphs[0]._p
        p.getparent().remove(p)

def json_to_docx(json_path: str, docx_out: str, template: str | None = None, clear_body: bool = False):
    data = json.load(open(json_path, "r", encoding="utf-8"))
    doc = Document(template) if template else Document()

    if template and clear_body:
        clear_document_body(doc)  # only when explicitly requested
    else:
        remove_initial_blank_paragraph(doc)  # safe for new documents

    for b in data["document"]["blocks"]:
        # ...same as before...
        pass

    os.makedirs(os.path.dirname(docx_out) or ".", exist_ok=True)
    doc.save(docx_out) 

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python json_to_docx.py input.json output.docx [--use-template path/to/template.docx] [--clear]")
        raise SystemExit(2)

    in_json, out_docx = sys.argv[1], sys.argv[2]
    template = None
    clear_body = False

    args = sys.argv[3:]
    if "--use-template" in args:
        i = args.index("--use-template")
        template = args[i+1]
    if "--clear" in args:
        clear_body = True

    json_to_docx(in_json, out_docx, template, clear_body)
