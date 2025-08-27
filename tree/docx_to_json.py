# docx_to_json.py
import json
from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_LINE_SPACING

def rgb_to_hex(rgb: RGBColor | None) -> str | None:
    if not rgb:
        return None
    return f"#{rgb.rgb}"

def run_to_dict(run):
    f = run.font
    return {
        "text": run.text or "",
        "bold": bool(f.bold),
        "italic": bool(f.italic),
        "underline": bool(f.underline),
        "strike": bool(getattr(f, "strike", False)),
        "size_pt": float(f.size.pt) if f.size else None,
        "font": f.name,
        "color": rgb_to_hex(f.color) if f.color else None,
        "highlight": getattr(f, "highlight_color", None).name if getattr(f, "highlight_color", None) else None,
    }

def paragraph_alignment_name(p):
    return p.alignment.name if p.alignment else None

def _get_num_fmt_for(p, doc):
    """
    Look up list number format ('decimal', 'bullet', etc.) for the paragraph's numId/ilvl.
    Returns (fmt, lvl_text) or (None, None) if not found.
    """
    pPr = p._p.pPr
    if pPr is None or pPr.numPr is None or pPr.numPr.numId is None:
        return None, None
    try:
        numId = int(pPr.numPr.numId.val)
        ilvl = int(pPr.numPr.ilvl.val) if pPr.numPr.ilvl is not None else 0
    except Exception:
        return None, None

    try:
        npart = doc.part.numbering_part
        root = npart.element
        # Find <w:num w:numId=numId> -> <w:abstractNumId> -> <w:abstractNum w:abstractNumId=...> -> <w:lvl w:ilvl=ilvl> -> <w:numFmt/@w:val>, <w:lvlText/@w:val>
        for num in root.findall(".//w:num", root.nsmap):
            nid = num.find("w:numId", root.nsmap)
            if nid is not None and int(nid.get("{%s}val" % root.nsmap["w"])) == numId:
                abs_id_el = num.find("w:abstractNumId", root.nsmap)
                if abs_id_el is None:
                    break
                abs_id = int(abs_id_el.get("{%s}val" % root.nsmap["w"]))
                for absnum in root.findall(".//w:abstractNum", root.nsmap):
                    aid = absnum.get("{%s}abstractNumId" % root.nsmap["w"])
                    if aid is not None and int(aid) == abs_id:
                        for lvl in absnum.findall("w:lvl", root.nsmap):
                            lvl_idx = int(lvl.get("{%s}ilvl" % root.nsmap["w"]))
                            if lvl_idx == ilvl:
                                numFmt = lvl.find("w:numFmt", root.nsmap)
                                lvlText = lvl.find("w:lvlText", root.nsmap)
                                fmt = numFmt.get("{%s}val" % root.nsmap["w"]) if numFmt is not None else None
                                txt = lvlText.get("{%s}val" % root.nsmap["w"]) if lvlText is not None else None
                                return fmt, txt
        return None, None
    except Exception:
        return None, None

def paragraph_to_dict(p, doc):
    style_name = p.style.name if p.style else None

    # spacing
    pf = p.paragraph_format
    space_before = float(pf.space_before.pt) if pf.space_before else None
    space_after  = float(pf.space_after.pt)  if pf.space_after  else None
    ls_val = pf.line_spacing
    try:
        line_spacing = float(ls_val) if ls_val is not None else None
    except Exception:
        line_spacing = float(getattr(ls_val, "pt", 0.0)) if ls_val else None
    line_rule = pf.line_spacing_rule.name if pf.line_spacing_rule else None

    # list
    list_info = None
    pPr = p._p.pPr
    if pPr is not None and pPr.numPr is not None and pPr.numPr.numId is not None:
        numId = int(pPr.numPr.numId.val)
        ilvl = int(pPr.numPr.ilvl.val) if pPr.numPr.ilvl is not None else 0
        fmt, lvl_text = _get_num_fmt_for(p, doc)
        list_info = {"numId": numId, "ilvl": ilvl, "fmt": fmt, "lvl_text": lvl_text}

    return {
        "type": "paragraph",
        "style": style_name,
        "alignment": paragraph_alignment_name(p),
        "spacing": {
            "space_before_pt": space_before,
            "space_after_pt": space_after,
            "line_spacing": line_spacing,
            "line_spacing_rule": line_rule,
        },
        "list": list_info,
        "runs": [run_to_dict(r) for r in p.runs],
    }

def table_to_dict(t, doc):
    rows = []
    for r in t.rows:
        row = []
        for c in r.cells:
            row.append({"blocks": [paragraph_to_dict(p, doc) for p in c.paragraphs]})
        rows.append(row)
    return {"type": "table", "rows": rows}

def docx_to_json(docx_path: str) -> dict:
    doc = Document(docx_path)
    blocks = []

    body_elems = list(doc.element.body.iterchildren())
    p_iter = iter(doc.paragraphs)
    t_iter = iter(doc.tables)

    for child in body_elems:
        if child.tag.endswith('}p'):
            p = next(p_iter)
            blocks.append(paragraph_to_dict(p, doc))
        elif child.tag.endswith('}tbl'):
            t = next(t_iter)
            blocks.append(table_to_dict(t, doc))

    return {"document": {"blocks": blocks}}

if __name__ == "__main__":
    import sys, os
    if len(sys.argv) < 3:
        print("Usage: python docx_to_json.py input.docx output.json")
        raise SystemExit(2)
    in_path, out_path = sys.argv[1], sys.argv[2]
    data = docx_to_json(in_path)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {out_path}")
