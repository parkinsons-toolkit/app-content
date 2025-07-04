"""
extract_pd_guide.py
-------------------
Reads the PDF "Information.guide.V2.2_AB_SA_July.pdf", slices it by
table-of-contents page ranges, and writes clean Markdown files
(one per TOC section) to `./markdown_sections/`, then zips them.

• lists/bullets are preserved
• images, page numbers, and Word comments ("Formatted: …") are dropped
• filenames are kebab-case ('what-is-parkinsons.md', …)

Run:  python extract_pd_guide.py
"""
import re, gc, shutil
from pathlib import Path
import pdfplumber

PDF              = "Information.guide.V2.2.accepted.changes.TR.pdf"
OUT_DIR          = Path("markdown_sections")
OUT_DIR.mkdir(exist_ok=True)

def kebab(title: str) -> str:
    t = title.lower().replace("'s", "s").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

# Page ranges based on Table of Contents (PDF page numbers start at 0, so subtract 1 from TOC)
RANGES = {
    "What is Parkinson's?"                       : (  4,   8),  # TOC: 5-8
    "Living with Parkinson's"                    : (  7,  12),  # TOC: 8-12 (overlaps with What is Parkinson's)
    "New Diagnosis"                              : (  7,  12),  # TOC: 8-12 (same as Living with Parkinson's)
    "Optimising Wellbeing"                       : ( 11,  14),  # TOC: 12-14
    "Keeping Active"                             : ( 13,  38),  # TOC: 14-38
    "Eating Well"                                : ( 37,  49),  # TOC: 38-49
    "Social & Spiritual Life"                    : ( 48,  57),  # TOC: 49-57
    "Dealing with Stress and Challenges"         : ( 56,  63),  # TOC: 57-63
    "General Medical Advice"                     : ( 62,  70),  # TOC: 63-70
    "Practical Advice"                           : ( 69,  72),  # TOC: 70-72
    "Appointments & Hospital Stays"              : ( 71,  86),  # TOC: 72-86
    "Daily Living"                               : ( 85, 102),  # TOC: 86-102
    "Finances"                                   : (101, 118),  # TOC: 102-118
    "Hobbies & Pets"                             : (117, 127),  # TOC: 118-127
    "Housing"                                    : (126, 137),  # TOC: 127-137
    "Legal Matters"                              : (136, 147),  # TOC: 137-147
    "Mobility"                                   : (146, 153),  # TOC: 147-153
    "Reading, Writing and Technology"            : (152, 160),  # TOC: 153-160
    "Travel"                                     : (159, 173),  # TOC: 160-173
    "Work and Caring"                            : (172, 180),  # TOC: 173-180
    "Symptom Management"                         : (179, 375),  # TOC: 180-375
    "Planning Future Care"                       : (374, 377),  # TOC: 375-377
    "Progression of Symptoms"                    : (376, 383),  # TOC: 377-383
    "Future Care Options"                        : (382, 399),  # TOC: 383-399
    "End of Life"                                : (398, 407),  # TOC: 399-407
    "Guidance for Families and Carers"           : (406, 432),  # TOC: 407-432
    "Treatment & Teams"                          : (431, 446),  # TOC: 432-446
    "Who May Be Involved?"                       : (431, 446),  # TOC: 432-446 (same as Treatment & Teams)
    "Medication"                                 : (445, 459),  # TOC: 446-459
    "Advanced Therapies & Surgical Treatments"   : (458, 472),  # TOC: 459-472
    "Complementary Therapies"                    : (471, 481),  # TOC: 472-481
    "Further Support"                            : (480, 488),  # TOC: 481-488
    "Information, Websites & Apps"               : (480, 488),  # TOC: 481-488 (same as Further Support)
    "Services & Groups"                          : (487, 497),  # TOC: 488-497
    "Research"                                   : (496, 505),  # TOC: 497-505
    "COVID-19"                                   : (504, 506),  # TOC: 505-end
}

def unwanted(line: str) -> bool:
    line = line.strip()
    return (
        not line
        or line.startswith(("Formatted:", "Image:"))
        or re.fullmatch(r"\d+", line) is not None  # page num
    )

with pdfplumber.open(PDF) as pdf:
    for title, (start, end) in RANGES.items():
        lines = []
        for p in range(start, min(end, len(pdf.pages))):
            txt = pdf.pages[p].extract_text() or ""
            lines.extend(ln.rstrip() for ln in txt.splitlines() if not unwanted(ln))
        md = f"# {title}\n\n" + "\n".join(lines).strip() + "\n"
        (OUT_DIR / f"{kebab(title)}.md").write_text(md, encoding="utf-8")
        gc.collect()

# zip them up
shutil.make_archive("pd_markdown_clean", "zip", OUT_DIR)
print("✅ All done!  →  pd_markdown_clean.zip")