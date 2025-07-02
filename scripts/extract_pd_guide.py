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

PDF              = "Information.guide.V2.2_AB_SA_July.pdf"
OUT_DIR          = Path("markdown_sections")
OUT_DIR.mkdir(exist_ok=True)

def kebab(title: str) -> str:
    t = title.lower().replace("'s", "s").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

# manual page ranges (PDF page numbers start at 0)
RANGES = {
    "What is Parkinson's?"                       : (  5,   8),
    "Living with Parkinson's"                    : (  8,  13),
    "New Diagnosis"                              : (  8,  13),
    "Optimising Wellbeing"                       : ( 13,  15),
    "Keeping Active"                             : ( 15,  37),
    "Eating Well"                                : ( 39,  51),
    "Social & Spiritual Life"                    : ( 51,  58),
    "Dealing with Stress and Challenges"         : ( 58,  64),
    "General Medical Advice"                     : ( 64,  71),
    "Practical Advice"                           : ( 71,  73),
    "Appointments & Hospital Stays"              : ( 73,  87),
    "Daily Living"                               : ( 87, 103),
    "Finances"                                   : (103, 119),
    "Hobbies & Pets"                             : (119, 128),
    "Housing"                                    : (128, 138),
    "Legal Matters"                              : (138, 149),
    "Mobility"                                   : (149, 154),
    "Reading, Writing and Technology"            : (154, 162),
    "Travel"                                     : (162, 175),
    "Work and Caring"                            : (175, 182),
    "Symptom Management"                         : (182, 379),
    "Planning Future Care"                       : (379, 381),
    "Progression of Symptoms"                    : (381, 388),
    "Future Care Options"                        : (388, 404),
    "End of Life"                                : (404, 412),
    "Guidance for Families and Carers"           : (412, 437),
    "Treatment & Teams"                          : (437, 450),
    "Who May Be Involved?"                       : (437, 450),
    "Medication"                                 : (450, 464),
    "Advanced Therapies & Surgical Treatments"   : (464, 477),
    "Complementary Therapies"                    : (477, 486),
    "Further Support"                            : (486, 492),
    "Information, Websites & Apps"               : (486, 492),
    "Services & Groups"                          : (492, 502),
    "Research"                                   : (502, 511),
    "COVID- 19"                                  : (511, 514),
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