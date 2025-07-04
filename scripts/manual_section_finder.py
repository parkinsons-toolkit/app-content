#!/usr/bin/env python3
"""
manual_section_finder.py
------------------------
Manually scan through pages to find actual section headers, not TOC entries.
This approach looks for headers as standalone lines that match our section titles.
"""

import pdfplumber
import re
from pathlib import Path

PDF = "Information.guide.V2.2.accepted.changes.TR.pdf"

def find_sections_manually():
    """Manually scan for section headers starting after the TOC"""
    sections_found = {}
    
    with pdfplumber.open(PDF) as pdf:
        print(f"Scanning {len(pdf.pages)} pages for actual section headers...")
        
        # Start scanning from page 3 onwards (skip TOC)
        for page_num in range(3, len(pdf.pages)):
            text = pdf.pages[page_num].extract_text() or ""
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            if not lines:
                continue
                
            # Look for lines that could be section headers
            for line in lines[:10]:  # Check first 10 lines of each page
                line_clean = line.strip()
                
                # Skip very short or very long lines
                if len(line_clean) < 5 or len(line_clean) > 50:
                    continue
                
                # Look for patterns that suggest a header
                if (line_clean.endswith('?') or 
                    any(word in line_clean.lower() for word in ['parkinson', 'living', 'keeping', 'eating', 'social', 'stress', 'medical', 'practical', 'appointment', 'daily', 'finance', 'hobbies', 'housing', 'legal', 'mobility', 'reading', 'travel', 'work', 'symptom', 'planning', 'progression', 'future', 'end of life', 'guidance', 'treatment', 'medication', 'therapy', 'support', 'research', 'covid'])):
                    
                    print(f"Page {page_num}: '{line_clean}'")
                    
                    # Check if this looks like one of our target sections
                    if any(target.lower() in line_clean.lower() for target in [
                        "what is parkinson", "living with parkinson", "new diagnosis", "optimising wellbeing",
                        "keeping active", "eating well", "social", "spiritual", "stress", "challenges",
                        "general medical", "practical advice", "appointments", "hospital", "daily living",
                        "finances", "hobbies", "pets", "housing", "legal matters", "mobility",
                        "reading", "writing", "technology", "travel", "work", "caring",
                        "symptom management", "planning future", "progression", "future care",
                        "end of life", "guidance for families", "treatment", "teams", "who may be involved",
                        "medication", "advanced therapies", "surgical", "complementary therapies",
                        "further support", "information", "websites", "apps", "services", "groups",
                        "research", "covid"
                    ]):
                        if line_clean not in sections_found:
                            sections_found[line_clean] = page_num

def scan_specific_ranges():
    """Scan specific page ranges to identify exact section boundaries"""
    # Based on TOC, let's check specific ranges
    toc_ranges = {
        "What is Parkinson's?": 5,
        "Living with Parkinson's": 8,
        "New Diagnosis": 8,
        "Optimising Wellbeing": 12,
        "Keeping Active": 14,
        "Eating Well": 38,
        "Social & Spiritual Life": 49,
        "Dealing with Stress and Challenges": 57,
        "General Medical Advice": 63,
        "Practical Advice": 70,
        "Appointments & Hospital Stays": 72,
        "Daily Living": 86,
        "Finances": 102,
        "Hobbies & Pets": 118,
        "Housing": 127,
        "Legal Matters": 137,
        "Mobility": 147,
        "Reading, Writing and Technology": 153,
        "Travel": 160,
        "Work and Caring": 173,
        "Planning Future Care": 375,
        "Progression of Symptoms": 377,
        "Future Care Options": 383,
        "End of Life": 399,
        "Guidance for Families and Carers": 407,
        "Treatment & Teams": 432,
        "Who May Be Involved?": 432,
        "Medication": 446,
        "Advanced Therapies & Surgical Treatments": 459,
        "Complementary Therapies": 472,
        "Further Support": 481,
        "Information, Websites & Apps": 481,
        "Services & Groups": 488,
        "Research": 497,
        "COVID-19": 505
    }
    
    with pdfplumber.open(PDF) as pdf:
        verified_ranges = {}
        
        print("Verifying TOC page numbers by checking actual content...")
        
        for section, expected_page in toc_ranges.items():
            # Check pages around the expected page
            for check_page in range(max(0, expected_page-2), min(len(pdf.pages), expected_page+3)):
                text = pdf.pages[check_page].extract_text() or ""
                
                # Look for the section header
                if section.lower().replace("'s", "s") in text.lower().replace("'s", "s"):
                    # Check if this looks like a proper header (not just TOC reference)
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        line_clean = line.strip()
                        if (section.lower().replace("'s", "s") in line_clean.lower().replace("'s", "s") and
                            len(line_clean) < 100 and  # Not too long (likely not body text)
                            len(line_clean) > 5):      # Not too short
                            
                            verified_ranges[section] = check_page
                            print(f"✓ {section}: Page {check_page}")
                            print(f"  Header: '{line_clean}'")
                            
                            # Show some context
                            if i + 1 < len(lines):
                                next_line = lines[i + 1].strip()
                                if next_line:
                                    print(f"  Next: '{next_line[:100]}...'")
                            break
                    break
        
        return verified_ranges

def generate_final_ranges(verified_ranges):
    """Generate final ranges with proper end boundaries"""
    section_order = [
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
    
    final_ranges = {}
    
    with pdfplumber.open(PDF) as pdf:
        total_pages = len(pdf.pages)
        
        for i, section in enumerate(section_order):
            if section in verified_ranges:
                start_page = verified_ranges[section]
                
                # Find end page
                if i + 1 < len(section_order):
                    # Look for next section
                    next_section = section_order[i + 1]
                    if next_section in verified_ranges:
                        end_page = verified_ranges[next_section]
                    else:
                        # If next section not found, estimate
                        end_page = start_page + 10  # Default to 10 pages
                else:
                    # Last section
                    end_page = total_pages
                
                final_ranges[section] = (start_page, end_page)
                print(f"{section}: ({start_page}, {end_page})")
    
    return final_ranges

def main():
    if not Path(PDF).exists():
        print(f"PDF file {PDF} not found!")
        return
    
    print("=== Manual Section Finding ===")
    find_sections_manually()
    
    print("\n=== Verifying TOC Page Numbers ===")
    verified_ranges = scan_specific_ranges()
    
    print(f"\n=== Final Ranges (found {len(verified_ranges)} sections) ===")
    final_ranges = generate_final_ranges(verified_ranges)
    
    print("\n=== Python RANGES Dictionary ===")
    print("RANGES = {")
    for section, (start, end) in final_ranges.items():
        print(f'    "{section}"'.ljust(45) + f': ({start:3d}, {end:3d}),')
    print("}")

if __name__ == "__main__":
    main()