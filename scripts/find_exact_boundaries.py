#!/usr/bin/env python3
"""
find_exact_boundaries.py
------------------------
Scans through the PDF to find the exact start and end boundaries of each section
by looking for section headers and identifying where content transitions.
"""

import pdfplumber
import re
from pathlib import Path

PDF = "Information.guide.V2.2.accepted.changes.TR.pdf"

# Section headers in the order they appear
SECTION_HEADERS = [
    "What is Parkinson's?",
    "Living with Parkinson's",
    "New Diagnosis",
    "Optimising Wellbeing", 
    "Keeping Active",
    "Eating Well",
    "Social & Spiritual Life",
    "Dealing with Stress and Challenges",
    "General Medical Advice",
    "Practical Advice",
    "Appointments & Hospital Stays",
    "Daily Living",
    "Finances",
    "Hobbies & Pets",
    "Housing",
    "Legal Matters",
    "Mobility",
    "Reading, Writing and Technology",
    "Travel",
    "Work and Caring",
    "Symptom Management",
    "Planning Future Care",
    "Progression of Symptoms",
    "Future Care Options",
    "End of Life",
    "Guidance for Families and Carers",
    "Treatment & Teams",
    "Who May Be Involved?",
    "Medication",
    "Advanced Therapies & Surgical Treatments",
    "Complementary Therapies",
    "Further Support",
    "Information, Websites & Apps",
    "Services & Groups",
    "Research",
    "COVID-19"
]

def normalize_header(text):
    """Normalize header text for comparison"""
    # Remove extra whitespace, handle different dash types
    text = re.sub(r'\s+', ' ', text.strip())
    text = text.replace('–', '-').replace('—', '-')
    text = text.replace('COVID- 19', 'COVID-19')
    return text

def find_section_boundaries():
    """Find exact start and end boundaries for each section"""
    section_starts = {}
    section_content = {}
    
    with pdfplumber.open(PDF) as pdf:
        print(f"Scanning {len(pdf.pages)} pages for section boundaries...")
        
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = text.split('\n')
            
            # Look for section headers
            for line in lines:
                line_clean = normalize_header(line)
                
                # Check if this line matches any of our section headers
                for header in SECTION_HEADERS:
                    header_clean = normalize_header(header)
                    
                    # Try different matching strategies
                    if (line_clean == header_clean or 
                        line_clean.startswith(header_clean) or
                        header_clean in line_clean):
                        
                        # Only record if we haven't seen this section yet
                        if header not in section_starts:
                            section_starts[header] = page_num
                            section_content[header] = []
                            print(f"Found '{header}' starting on page {page_num}")
                            print(f"  Line: '{line.strip()}'")
                        break
    
    # Calculate end boundaries
    section_ranges = {}
    headers_found = [h for h in SECTION_HEADERS if h in section_starts]
    
    for i, header in enumerate(headers_found):
        start_page = section_starts[header]
        
        # End page is the start of the next section minus 1, or last page
        if i + 1 < len(headers_found):
            next_header = headers_found[i + 1]
            end_page = section_starts[next_header] - 1
        else:
            # Last section goes to end of document
            with pdfplumber.open(PDF) as pdf:
                end_page = len(pdf.pages) - 1
        
        section_ranges[header] = (start_page, end_page + 1)  # +1 for exclusive end
    
    return section_ranges

def verify_boundaries(section_ranges):
    """Verify the boundaries by showing content snippets"""
    print("\n" + "="*100)
    print("VERIFYING SECTION BOUNDARIES")
    print("="*100)
    
    with pdfplumber.open(PDF) as pdf:
        for header, (start, end) in section_ranges.items():
            print(f"\n{header}: Pages {start}-{end-1}")
            
            # Show start of section
            if start < len(pdf.pages):
                start_text = pdf.pages[start].extract_text() or ""
                start_lines = start_text.split('\n')[:10]  # First 10 lines
                print(f"  START (page {start}): {start_lines[0][:100]}...")
            
            # Show end of section
            if end - 1 < len(pdf.pages):
                end_text = pdf.pages[end - 1].extract_text() or ""
                end_lines = end_text.split('\n')[-10:]  # Last 10 lines
                print(f"  END (page {end-1}): ...{end_lines[-1][:100]}")
                
                # Show what comes next
                if end < len(pdf.pages):
                    next_text = pdf.pages[end].extract_text() or ""
                    next_lines = next_text.split('\n')[:3]  # First 3 lines of next page
                    print(f"  NEXT (page {end}): {next_lines[0][:100]}...")

def generate_ranges_code(section_ranges):
    """Generate the Python code for the RANGES dictionary"""
    print("\n" + "="*100)
    print("UPDATED RANGES DICTIONARY")
    print("="*100)
    
    print("RANGES = {")
    for header, (start, end) in section_ranges.items():
        print(f'    "{header}"'.ljust(45) + f': ({start:3d}, {end:3d}),')
    print("}")

def main():
    if not Path(PDF).exists():
        print(f"PDF file {PDF} not found!")
        return
    
    print("Finding exact section boundaries...")
    section_ranges = find_section_boundaries()
    
    print(f"\nFound {len(section_ranges)} sections")
    
    # Verify the boundaries
    verify_boundaries(section_ranges)
    
    # Generate the code
    generate_ranges_code(section_ranges)

if __name__ == "__main__":
    main()