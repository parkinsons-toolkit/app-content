#!/usr/bin/env python3
"""
find_page_ranges.py
------------------
Scans through the cleaned PDF to identify where each section starts
to help update the page ranges in extract_pd_guide.py
"""

import pdfplumber
import re
from pathlib import Path

PDF = "Information.guide.V2.2.accepted.changes.TR.pdf"

# The sections we're looking for
SECTIONS = [
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

def clean_text_for_matching(text):
    """Clean text for better matching"""
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    return text.lower()

def find_section_pages():
    """Find the page numbers where each section starts"""
    section_pages = {}
    
    with pdfplumber.open(PDF) as pdf:
        print(f"Scanning {len(pdf.pages)} pages...")
        
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            
            # Look for section headers
            for section in SECTIONS:
                # Try various matching patterns
                patterns = [
                    f"^{re.escape(section)}$",  # Exact match on its own line
                    f"^{re.escape(section)}\\s*$",  # With trailing whitespace
                    f"\\b{re.escape(section)}\\b",  # Word boundary match
                ]
                
                for pattern in patterns:
                    if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
                        if section not in section_pages:
                            section_pages[section] = page_num
                            print(f"Found '{section}' on page {page_num}")
                            break
    
    return section_pages

def show_table_of_contents():
    """Show the first few pages to help identify the table of contents"""
    with pdfplumber.open(PDF) as pdf:
        print("First 10 pages content (looking for table of contents):")
        print("=" * 80)
        
        for page_num in range(min(10, len(pdf.pages))):
            text = pdf.pages[page_num].extract_text() or ""
            print(f"\n--- PAGE {page_num} ---")
            # Show first few lines of each page
            lines = text.split('\n')[:20]
            for line in lines:
                if line.strip():
                    print(line.strip())

def main():
    if not Path(PDF).exists():
        print(f"PDF file {PDF} not found!")
        return
    
    print("Scanning for section headers...")
    section_pages = find_section_pages()
    
    print("\n" + "="*80)
    print("FOUND SECTIONS:")
    print("="*80)
    
    for section in SECTIONS:
        if section in section_pages:
            print(f"{section:<40} : Page {section_pages[section]}")
        else:
            print(f"{section:<40} : NOT FOUND")
    
    print("\n" + "="*80)
    print("TABLE OF CONTENTS SCAN:")
    print("="*80)
    show_table_of_contents()

if __name__ == "__main__":
    main()