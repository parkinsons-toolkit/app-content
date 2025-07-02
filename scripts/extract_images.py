#!/usr/bin/env python3
"""
Extract images from PDF and save them to organized directories
"""

import re
import os
import shutil
from pathlib import Path
import pdfplumber
from PIL import Image
import io

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

def extract_images_from_pdf():
    """Extract all images from PDF and organize by section"""
    
    with pdfplumber.open(PDF) as pdf:
        total_images = 0
        
        for page_num, page in enumerate(pdf.pages):
            section = get_section_for_page(page_num)
            section_dir = IMAGES_DIR / section
            section_dir.mkdir(exist_ok=True)
            
            # Extract images using pdfplumber
            if hasattr(page, 'images') and page.images:
                for img_idx, img_obj in enumerate(page.images):
                    try:
                        # Get image data
                        if hasattr(img_obj, 'stream') and img_obj.stream:
                            img_data = img_obj.stream.get_data()
                        elif hasattr(img_obj, 'image'):
                            img_data = img_obj.image
                        else:
                            continue
                        
                        # Try to create PIL image
                        try:
                            pil_image = Image.open(io.BytesIO(img_data))
                        except Exception:
                            # Skip if can't process image
                            continue
                        
                        # Determine file extension
                        img_format = pil_image.format
                        if img_format == 'JPEG':
                            ext = '.jpg'
                        elif img_format == 'PNG':
                            ext = '.png'
                        else:
                            ext = '.png'  # Default to PNG
                        
                        # Save image with descriptive filename
                        img_filename = f"page_{page_num+1}_img_{img_idx+1}{ext}"
                        img_path = section_dir / img_filename
                        
                        # Convert to RGB if necessary (for JPEG)
                        if img_format == 'JPEG' and pil_image.mode in ('RGBA', 'LA'):
                            pil_image = pil_image.convert('RGB')
                        
                        pil_image.save(img_path, quality=90, optimize=True)
                        print(f"Saved: {section}/{img_filename}")
                        total_images += 1
                        
                    except Exception as e:
                        print(f"Error extracting image from page {page_num+1}: {e}")
                        continue
            
            # Alternative method using pypdfium2 (if available through pdfplumber)
            try:
                # Extract images using page.within_bbox method for figures/charts
                page_images = page.filter(lambda obj: obj.get('object_type') == 'image')
                for img_idx, img in enumerate(page_images):
                    # This is a more basic extraction - may need refinement
                    pass
            except Exception:
                pass
        
        print(f"\n✅ Extracted {total_images} images total")
        print(f"📁 Images organized in: {IMAGES_DIR}")
        
        # Create index file
        create_image_index()

def create_image_index():
    """Create an index of extracted images"""
    index_content = ["# Image Index\n"]
    
    for section_dir in sorted(IMAGES_DIR.iterdir()):
        if section_dir.is_dir():
            images = list(section_dir.glob("*.jpg")) + list(section_dir.glob("*.png"))
            if images:
                index_content.append(f"## {section_dir.name.replace('-', ' ').title()}\n")
                for img in sorted(images):
                    relative_path = f"images/{section_dir.name}/{img.name}"
                    index_content.append(f"- ![{img.stem}]({relative_path})\n")
                index_content.append("\n")
    
    with open(IMAGES_DIR / "IMAGE_INDEX.md", 'w') as f:
        f.writelines(index_content)
    
    print(f"📋 Created image index: {IMAGES_DIR}/IMAGE_INDEX.md")

if __name__ == "__main__":
    print("🔍 Extracting images from PDF...")
    extract_images_from_pdf()