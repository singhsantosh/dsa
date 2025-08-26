# docx_to_json.py
import json
from docx import Document
from docx.shared import RGBColor

def rgb_to_hex(rgb: RGBColor | None) -> str | None:
    if not rgb:
        return None
    return f"#{rgb.rgb}"  # rgb is already 6-hex like 'FF0000'

def run_to_dict(run):
    f = run.font
    obj = {
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
    return obj

def paragraph_alignment_name(p):
    a = p.alignment
    return a.name if a else None  # LEFT, CENTER, RIGHT, JUSTIFY, etc.

def paragraph_to_dict(p):
    # Style name carries important semantics (Heading 1, List Number, List Bullet, etc.)
    style_name = p.style.name if p.style else None
    # Level hint for headings / outline (if present)
    outline_level = None
    try:
        if p.style and p.style.paragraph_format and p.style.paragraph_format.outline_level is not None:
            outline_level = p.style.paragraph_format.outline_level
    except Exception:
        pass

    return {
        "type": "paragraph",
        "style": style_name,
        "alignment": paragraph_alignment_name(p),
        "outline_level": outline_level,
        "runs": [run_to_dict(r) for r in p.runs],
    }

def table_to_dict(t):
    rows = []
    for r in t.rows:
        row = []
        for c in r.cells:
            # flatten each cell as paragraph blocks
            cell_blocks = [paragraph_to_dict(p) for p in c.paragraphs]
            row.append({"blocks": cell_blocks})
        rows.append(row)
    return {"type": "table", "rows": rows}

def docx_to_json(docx_path: str) -> dict:
    doc = Document(docx_path)
    blocks = []
    # Walk the document body in order (paragraphs & tables)
    # python-docx exposes them separately; we stitch their original order via _element
    body_elems = []
    body = doc.element.body
    for child in body.iterchildren():
        body_elems.append(child)

    p_iter = iter(doc.paragraphs)
    t_iter = iter(doc.tables)

    for child in body_elems:
        tag = child.tag
        if tag.endswith('}p'):
            p = next(p_iter)
            blocks.append(paragraph_to_dict(p))
        elif tag.endswith('}tbl'):
            t = next(t_iter)
            blocks.append(table_to_dict(t))

    # Optional: section/page breaks (simple capture)
    # For now, just emit blocks above.

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
