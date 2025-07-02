#!/usr/bin/env python3
"""
Extract images from PDF using PyMuPDF (fitz) - more robust image extraction
"""

import fitz  # PyMuPDF
import os
from pathlib import Path

PDF = "Information.guide.V2.2_AB_SA_July.pdf"
IMAGES_DIR = Path("images")
IMAGES_DIR.mkdir(exist_ok=True)

# Section mapping for organizing images by content area
SECTION_RANGES = {
    "what-is-parkinsons": (5, 8),
    "living-with-parkinsons": (8, 13),
    "new-diagnosis": (8, 13),
    "optimising-wellbeing": (13, 15),
    "keeping-active": (15, 37),
    "eating-well": (39, 51),
    "social-spiritual-life": (51, 58),
    "dealing-with-stress-challenges": (58, 64),
    "general-medical-advice": (64, 71),
    "practical-advice": (71, 73),
    "appointments-hospital-stays": (73, 87),
    "daily-living": (87, 103),
    "finances": (103, 119),
    "hobbies-pets": (119, 128),
    "housing": (128, 138),
    "legal-matters": (138, 149),
    "mobility": (149, 154),
    "reading-writing-technology": (154, 162),
    "travel": (162, 175),
    "work-and-caring": (175, 182),
    "symptom-management": (182, 379),
    "planning-future-care": (379, 381),
    "progression-of-symptoms": (381, 388),
    "future-care-options": (388, 404),
    "end-of-life": (404, 412),
    "guidance-families-carers": (412, 437),
    "treatment-teams": (437, 450),
    "medication": (450, 464),
    "advanced-therapies": (464, 477),
    "complementary-therapies": (477, 486),
    "further-support": (486, 492),
    "services-groups": (492, 502),
    "research": (502, 511),
    "covid-19": (511, 514),
}

def get_section_for_page(page_num):
    """Determine which section a page belongs to"""
    for section, (start, end) in SECTION_RANGES.items():
        if start <= page_num < end:
            return section
    return "general"

def extract_images_with_fitz():
    """Extract images using PyMuPDF"""
    
    # Open PDF
    doc = fitz.open(PDF)
    total_images = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        section = get_section_for_page(page_num)
        section_dir = IMAGES_DIR / section
        section_dir.mkdir(exist_ok=True)
        
        # Get list of images on this page
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            try:
                # Get image data
                xref = img[0]  # xref number
                pix = fitz.Pixmap(doc, xref)
                
                # Skip if image is too small (likely decorative)
                if pix.width < 50 or pix.height < 50:
                    pix = None
                    continue
                
                # Determine file extension
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    ext = ".png"
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix = pix1
                    ext = ".png"
                
                # Create filename
                img_filename = f"page_{page_num+1}_img_{img_index+1}{ext}"
                img_path = section_dir / img_filename
                
                # Save image
                pix.save(img_path)
                print(f"Saved: {section}/{img_filename} ({pix.width}x{pix.height})")
                total_images += 1
                
                pix = None  # Clean up
                
            except Exception as e:
                print(f"Error extracting image {img_index+1} from page {page_num+1}: {e}")
                continue
    
    doc.close()
    
    print(f"\n✅ Extracted {total_images} images total")
    print(f"📁 Images organized in: {IMAGES_DIR}")
    
    # Create index file
    create_image_index()

def create_image_index():
    """Create an index of extracted images"""
    index_content = ["# Image Index\n\n"]
    
    for section_dir in sorted(IMAGES_DIR.iterdir()):
        if section_dir.is_dir():
            images = list(section_dir.glob("*.jpg")) + list(section_dir.glob("*.png"))
            if images:
                section_name = section_dir.name.replace('-', ' ').title()
                index_content.append(f"## {section_name}\n\n")
                for img in sorted(images):
                    relative_path = f"images/{section_dir.name}/{img.name}"
                    index_content.append(f"- ![{img.stem}]({relative_path})\n")
                index_content.append("\n")
    
    with open(IMAGES_DIR / "IMAGE_INDEX.md", 'w') as f:
        f.writelines(index_content)
    
    print(f"📋 Created image index: {IMAGES_DIR}/IMAGE_INDEX.md")

if __name__ == "__main__":
    print("🔍 Extracting images from PDF using PyMuPDF...")
    extract_images_with_fitz()