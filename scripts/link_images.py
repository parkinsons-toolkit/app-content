#!/usr/bin/env python3
"""
Link extracted images to appropriate sections in markdown files
"""

import os
import re
from pathlib import Path
from collections import defaultdict

PAGES_DIR = Path("pages-content")
IMAGES_DIR = Path("images")

# Mapping of markdown files to their corresponding image directories
MD_TO_IMAGE_MAPPING = {
    "what-is-parkinsons.md": "what-is-parkinsons",
    "living-with-parkinsons.md": "living-with-parkinsons", 
    "new-diagnosis.md": "living-with-parkinsons",  # shares same page range
    "optimising-wellbeing.md": "optimising-wellbeing",
    "keeping-active.md": "keeping-active",
    "eating-well.md": "eating-well",
    "social-spiritual-life.md": "social-spiritual-life",
    "dealing-with-stress-and-challenges.md": "dealing-with-stress-challenges",
    "general-medical-advice.md": "general-medical-advice",
    "practical-advice.md": "practical-advice",
    "appointments-hospital-stays.md": "appointments-hospital-stays",
    "daily-living.md": "daily-living",
    "finances.md": "finances",
    "hobbies-pets.md": "hobbies-pets",
    "housing.md": "housing",
    "legal-matters.md": "legal-matters",
    "mobility.md": "mobility",
    "reading-writing-and-technology.md": "reading-writing-technology",
    "travel.md": "travel",
    "work-and-caring.md": "work-and-caring",
    "symptom-management.md": "symptom-management",
    "planning-future-care.md": "planning-future-care",
    "progression-of-symptoms.md": "progression-of-symptoms",
    "future-care-options.md": "future-care-options",
    "end-of-life.md": "end-of-life",
    "guidance-for-families-and-carers.md": "guidance-families-carers",
    "treatment-teams.md": "treatment-teams",
    "who-may-be-involved.md": "treatment-teams",  # shares same content
    "medication.md": "medication",
    "advanced-therapies-surgical-treatments.md": "advanced-therapies",
    "complementary-therapies.md": "complementary-therapies",
    "further-support.md": "further-support",
    "information-websites-apps.md": "further-support",  # shares same content
    "services-groups.md": "services-groups",
    "research.md": "research",
    "covid-19.md": "covid-19",
}

def get_meaningful_images(image_dir):
    """Get images that are likely to be meaningful content (not headers/footers)"""
    if not image_dir.exists():
        return []
    
    images = []
    for img_file in sorted(image_dir.glob("*.png")):
        # Skip header images (usually small and on every page)
        if "img_1.png" in img_file.name and img_file.stat().st_size < 50000:  # < 50KB likely header
            continue
        images.append(img_file)
    
    return images

def insert_image_strategically(content, image_path, image_name):
    """Insert image at strategic locations in the content"""
    lines = content.split('\n')
    
    # Look for good insertion points
    insertion_points = []
    
    for i, line in enumerate(lines):
        # After main headings (##)
        if line.startswith('## ') and i < len(lines) - 2:
            # Insert after heading and any immediate paragraph
            next_non_empty = i + 1
            while next_non_empty < len(lines) and not lines[next_non_empty].strip():
                next_non_empty += 1
            
            # Skip if next line is another heading
            if next_non_empty < len(lines) and not lines[next_non_empty].startswith('#'):
                # Find end of first paragraph
                para_end = next_non_empty
                while para_end < len(lines) and lines[para_end].strip() and not lines[para_end].startswith('#'):
                    para_end += 1
                insertion_points.append((para_end, f"strategic_after_heading_{i}"))
        
        # After lists that might benefit from visual aid
        if line.startswith('- ') or line.startswith('1. '):
            list_end = i + 1
            while list_end < len(lines) and (lines[list_end].startswith('- ') or lines[list_end].startswith('  ') or re.match(r'^\d+\.', lines[list_end])):
                list_end += 1
            if list_end > i + 2:  # Only for lists with multiple items
                insertion_points.append((list_end, f"after_list_{i}"))
    
    # If no good insertion points found, insert after first paragraph
    if not insertion_points:
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#') and i > 0:
                para_end = i + 1
                while para_end < len(lines) and lines[para_end].strip() and not lines[para_end].startswith('#'):
                    para_end += 1
                insertion_points.append((para_end, f"after_first_para_{i}"))
                break
    
    # Use the first good insertion point
    if insertion_points:
        insert_pos, reason = insertion_points[0]
        
        # Create image markdown with descriptive alt text
        alt_text = f"Illustration for {image_name.replace('_', ' ').replace('.png', '')}"
        img_markdown = f'\n<img src="{image_path}" alt="{alt_text}" width="400" style="float: left; margin-right: 20px; margin-bottom: 10px;">\n'
        
        # Insert the image
        lines.insert(insert_pos, img_markdown)
        
        # Add a clear div after a reasonable distance
        clear_div_pos = min(insert_pos + 8, len(lines))
        lines.insert(clear_div_pos, '\n<div style="clear: both;"></div>\n')
        
        print(f"  → Inserted image at position {insert_pos} ({reason})")
        return '\n'.join(lines)
    
    return content

def link_images_to_markdown():
    """Link images to their corresponding markdown files"""
    
    for md_file, image_dir_name in MD_TO_IMAGE_MAPPING.items():
        md_path = PAGES_DIR / md_file
        image_dir = IMAGES_DIR / image_dir_name
        
        if not md_path.exists():
            print(f"⚠️  Markdown file not found: {md_file}")
            continue
        
        # Get meaningful images for this section
        meaningful_images = get_meaningful_images(image_dir)
        
        if not meaningful_images:
            print(f"📄 {md_file}: No suitable images found")
            continue
        
        # Read the markdown content
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"🖼️  Processing {md_file} ({len(meaningful_images)} images available)")
        
        # For each file, we'll add 1-3 strategically placed images
        images_to_add = meaningful_images[:3]  # Limit to 3 images per file
        
        updated_content = content
        images_added = 0
        
        for img_file in images_to_add:
            relative_path = f"../images/{image_dir_name}/{img_file.name}"
            
            # Skip if image already referenced in content
            if img_file.name in updated_content:
                continue
            
            updated_content = insert_image_strategically(updated_content, relative_path, img_file.name)
            images_added += 1
        
        # Write back the updated content
        if images_added > 0:
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"  ✅ Added {images_added} images to {md_file}")
        else:
            print(f"  📝 No new images added to {md_file}")

def create_image_reference_guide():
    """Create a guide showing which images are available for each section"""
    guide_content = ["# Image Reference Guide\n\n"]
    guide_content.append("This guide shows available images for each content section.\n\n")
    
    for md_file, image_dir_name in MD_TO_IMAGE_MAPPING.items():
        image_dir = IMAGES_DIR / image_dir_name
        if image_dir.exists():
            images = list(image_dir.glob("*.png"))
            if images:
                guide_content.append(f"## {md_file}\n")
                guide_content.append(f"**Image directory:** `images/{image_dir_name}/`\n")
                guide_content.append(f"**Available images:** {len(images)}\n\n")
                
                # Show first few images as examples
                for img in images[:5]:
                    relative_path = f"images/{image_dir_name}/{img.name}"
                    guide_content.append(f"- `{relative_path}`\n")
                
                if len(images) > 5:
                    guide_content.append(f"- ... and {len(images) - 5} more\n")
                guide_content.append("\n")
    
    # Write the guide
    with open(IMAGES_DIR / "LINKING_GUIDE.md", 'w', encoding='utf-8') as f:
        f.writelines(guide_content)
    
    print(f"📋 Created image reference guide: {IMAGES_DIR}/LINKING_GUIDE.md")

if __name__ == "__main__":
    print("🔗 Linking images to markdown files...")
    link_images_to_markdown()
    create_image_reference_guide()
    print("\n✅ Image linking complete!")