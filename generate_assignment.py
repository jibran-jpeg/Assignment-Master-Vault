#!/usr/bin/env python3
"""
📄 Universal Assignment Document Generator
Generates academic assignments adhering strictly to the Anti-AI, APA 7th,
and institutional layout standards defined in the Assignment Master Vault.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
    from docx.oxml import OxmlElement, parse_xml
    from docx.oxml.ns import qn, nsdecls
except ImportError:
    print("[!] Error: 'python-docx' is required. Install via: pip install python-docx")
    sys.exit(1)

from setup_profile import ensure_profile, get_profile


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_shading(cell, color_hex="F0F0F0"):
    """Sets background shading of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)


def set_table_borders_apa(table):
    """
    Applies strict APA 7th Edition publication table borders:
    Top border (solid), header bottom border (solid), table bottom border (solid).
    Zero vertical borders, zero interior horizontal borders on body rows.
    """
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="none"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    # Add border underneath header row
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(tcBorders)


def add_page_number_field(run):
    """Appends dynamic Word PAGE field into a text run."""
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def build_assignment(
    course_title="Computer Science",
    course_code="CS-101",
    assignment_title="Assignment 01",
    instructor_name="Course Instructor",
    due_date="",
    questions_and_answers=None,
    output_filename=None,
    profile=None
):
    """Builds a complete, professional, Anti-AI compliant assignment DOCX and PDF."""
    if not profile:
        profile = ensure_profile()

    doc = Document()

    # --- 1. Page Margins & Borders ---
    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

        # Inject clean outer frame border
        sectPr = sec._sectPr
        bdr_xml = (
            r'<w:pgBorders %s w:offsetFrom="page">'
            r'<w:top w:val="single" w:sz="6" w:space="24" w:color="000000"/>'
            r'<w:left w:val="single" w:sz="6" w:space="24" w:color="000000"/>'
            r'<w:bottom w:val="single" w:sz="6" w:space="24" w:color="000000"/>'
            r'<w:right w:val="single" w:sz="6" w:space="24" w:color="000000"/>'
            r'</w:pgBorders>'
        ) % nsdecls("w")
        sectPr.append(parse_xml(bdr_xml))

        # Dynamic Footer
        footer = sec.footer
        p_f = footer.paragraphs[0]
        p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        campus_tag = profile.get("campus_code", profile.get("campus_name", "CAMPUS"))
        r_f1 = p_f.add_run(f"{course_title} | {campus_tag} | Page ")
        r_f1.font.name = "Times New Roman"
        r_f1.font.size = Pt(9)
        r_f1.font.color.rgb = RGBColor(100, 100, 100)
        add_page_number_field(p_f.add_run())

    # --- 2. Title / Cover Page (Pattern B: Institutional Title Block) ---
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run(profile.get("institution_name", "Academic Institution").upper())
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(14)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0, 0, 0)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run(profile.get("department", "Department of Computing"))
    r_dept.font.name = "Times New Roman"
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = RGBColor(60, 60, 60)

    doc.add_paragraph()  # Spacing

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run(course_title)
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 0, 0)

    p_asg = doc.add_paragraph()
    p_asg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_asg = p_asg.add_run(assignment_title)
    r_asg.font.name = "Times New Roman"
    r_asg.font.size = Pt(16)
    r_asg.font.bold = True
    r_asg.font.underline = True
    r_asg.font.color.rgb = RGBColor(0, 0, 0)

    if due_date:
        p_due = doc.add_paragraph()
        p_due.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_due = p_due.add_run(f"Due Date: {due_date}")
        r_due.font.name = "Times New Roman"
        r_due.font.size = Pt(11)
        r_due.font.bold = True
        r_due.font.color.rgb = RGBColor(180, 0, 0)

    for _ in range(3):
        doc.add_paragraph()

    # Slot Credentials Table
    slots_table = doc.add_table(rows=4, cols=2)
    slots_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    slots_table.autofit = False

    labels = [
        ("Submitted To:", instructor_name),
        ("Student Name:", profile.get("student_name", "")),
        ("Registration ID:", profile.get("student_id", "")),
        ("Degree & Section:", f"{profile.get('degree_program', '')} ({profile.get('class_section', '')})")
    ]

    for i, (label, val) in enumerate(labels):
        row = slots_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.5)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(0, 0, 0)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(0, 0, 0)
        
        # Add subtle bottom line to cell 1
        tcPr = c1._tc.get_or_add_tcPr()
        bdr = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="4" w:space="0" w:color="333333"/></w:tcBorders>')
        tcPr.append(bdr)

    # End of Page 1 Break
    doc.add_page_break()

    # --- 3. Body Content (Questions & Answers) ---
    if not questions_and_answers:
        # Default starter content
        questions_and_answers = [
            {
                "question": "Question 1: Theoretical Foundations and Architectural Principles",
                "marks": "10 Marks",
                "answer_type": "text",
                "content": (
                    "In computational system design, modular isolation guarantees high coherence while "
                    "minimizing inter-service dependencies. Unlike monolithic architectures that couple data "
                    "persistence with domain services, modern layered paradigms enforce separation of concerns. "
                    "This prevents regression cascading across independent application boundaries."
                )
            },
            {
                "question": "Question 2: Performance Evaluation and Empirical Metric Comparison",
                "marks": "10 Marks",
                "answer_type": "table",
                "table_title": "Table 1. Empirical Latency and Throughput Benchmarks",
                "headers": ["Architecture Variant", "Average Latency (ms)", "P99 Latency (ms)", "Throughput (RPS)"],
                "rows": [
                    ["Synchronous Monolith", "48.2", "112.5", "1,450"],
                    ["Asynchronous Pipeline", "18.4", "42.1", "4,820"],
                    ["Zero-Copy Event Stream", "7.1", "15.8", "12,900"]
                ]
            }
        ]

    for item in questions_and_answers:
        # Question Header
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(12)
        p_q.paragraph_format.space_after = Pt(4)
        
        q_run = p_q.add_run(item.get("question", ""))
        q_run.font.name = "Times New Roman"
        q_run.font.size = Pt(12)
        q_run.font.bold = True
        q_run.font.color.rgb = RGBColor(0, 0, 0)

        if "marks" in item and item["marks"]:
            m_run = p_q.add_run(f" [{item['marks']}]")
            m_run.font.name = "Times New Roman"
            m_run.font.size = Pt(11)
            m_run.font.italic = True
            m_run.font.color.rgb = RGBColor(80, 80, 80)

        # Answer Label
        p_ans_lbl = doc.add_paragraph()
        p_ans_lbl.paragraph_format.space_before = Pt(4)
        p_ans_lbl.paragraph_format.space_after = Pt(2)
        a_lbl = p_ans_lbl.add_run("Answer:")
        a_lbl.font.name = "Times New Roman"
        a_lbl.font.size = Pt(11)
        a_lbl.font.bold = True
        a_lbl.font.color.rgb = RGBColor(0, 0, 0)

        ans_type = item.get("answer_type", "text")
        if ans_type == "text":
            p_body = doc.add_paragraph()
            p_body.paragraph_format.space_before = Pt(2)
            p_body.paragraph_format.space_after = Pt(6)
            p_body.paragraph_format.line_spacing = 1.15
            b_run = p_body.add_run(item.get("content", ""))
            b_run.font.name = "Times New Roman"
            b_run.font.size = Pt(11)
            b_run.font.color.rgb = RGBColor(0, 0, 0)

        elif ans_type == "table":
            if "table_title" in item:
                p_tbl_lbl = doc.add_paragraph()
                p_tbl_lbl.paragraph_format.space_before = Pt(6)
                p_tbl_lbl.paragraph_format.space_after = Pt(2)
                t_lbl_run = p_tbl_lbl.add_run(item["table_title"])
                t_lbl_run.font.name = "Times New Roman"
                t_lbl_run.font.size = Pt(10.5)
                t_lbl_run.font.bold = True
                t_lbl_run.font.color.rgb = RGBColor(0, 0, 0)

            headers = item.get("headers", [])
            data_rows = item.get("rows", [])
            t = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders_apa(t)

            # Header row
            h_row = t.rows[0]
            # Enforce tblHeader
            trPr = h_row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

            for c_idx, h_text in enumerate(headers):
                cell = h_row.cells[c_idx]
                set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
                set_cell_shading(cell, "EAEAEA")
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                hr = p.add_run(h_text)
                hr.font.name = "Times New Roman"
                hr.font.size = Pt(10)
                hr.font.bold = True
                hr.font.color.rgb = RGBColor(0, 0, 0)

            # Data rows
            for r_idx, row_vals in enumerate(data_rows):
                row = t.rows[r_idx + 1]
                # cantSplit
                trPr = row._tr.get_or_add_trPr()
                trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

                bg_color = "F9F9F9" if (r_idx % 2 == 1) else "FFFFFF"
                for c_idx, val in enumerate(row_vals):
                    cell = row.cells[c_idx]
                    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
                    if bg_color != "FFFFFF":
                        set_cell_shading(cell, bg_color)
                    p = cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    dr = p.add_run(str(val))
                    dr.font.name = "Times New Roman"
                    dr.font.size = Pt(10)
                    dr.font.color.rgb = RGBColor(0, 0, 0)

            doc.add_paragraph()  # Spacing after table

    # --- 4. Save and Output Directory Resolution ---
    base_out = Path(profile.get("output_dir", "./output")).expanduser()
    subject_safe = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in course_title).strip()
    target_dir = base_out / subject_safe
    target_dir.mkdir(parents=True, exist_ok=True)

    if not output_filename:
        asg_safe = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in assignment_title).strip()
        output_filename = f"{asg_safe}.docx"

    docx_path = target_dir / output_filename
    doc.save(str(docx_path))
    print(f"\n✅ Document generated successfully: {docx_path}")

    # Compile to PDF via LibreOffice
    pdf_path = docx_path.with_suffix(".pdf")
    try:
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", str(docx_path), "--outdir", str(target_dir)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if pdf_path.exists():
            print(f"📄 PDF compiled successfully: {pdf_path}")
    except Exception as e:
        print(f"[!] Note: PDF conversion skipped (LibreOffice not available or failed: {e})")

    return docx_path, pdf_path


def main():
    parser = argparse.ArgumentParser(description="Universal Assignment Builder")
    parser.add_argument("--course", default="Computer Science", help="Course Name")
    parser.add_argument("--code", default="CS-101", help="Course Code")
    parser.add_argument("--title", default="Assignment 01", help="Assignment Title")
    parser.add_argument("--instructor", default="Course Instructor", help="Instructor Name")
    parser.add_argument("--due", default="", help="Due Date")
    parser.add_argument("--interactive", action="store_true", help="Prompt interactively for assignment details")
    args = parser.parse_args()

    profile = ensure_profile()

    course = args.course
    code = args.code
    title = args.title
    instructor = args.instructor
    due = args.due

    if args.interactive:
        print("\n" + "=" * 60)
        print("📝 INTERACTIVE ASSIGNMENT SETUP")
        print("=" * 60)
        course = input(f"Course Title [{course}]: ").strip() or course
        code = input(f"Course Code [{code}]: ").strip() or code
        title = input(f"Assignment Title [{title}]: ").strip() or title
        instructor = input(f"Instructor Name [{instructor}]: ").strip() or instructor
        due = input(f"Due Date (optional): ").strip()

    build_assignment(
        course_title=course,
        course_code=code,
        assignment_title=title,
        instructor_name=instructor,
        due_date=due,
        profile=profile
    )


if __name__ == "__main__":
    main()
