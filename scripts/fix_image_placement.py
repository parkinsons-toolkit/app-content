#!/usr/bin/env python3
"""
Fix image placement to distribute images more naturally throughout markdown files
"""

import os
import re
from pathlib import Path

PAGES_DIR = Path("pages-content")

def fix_image_placement(content):
    """Fix stacked images by distributing them throughout the content"""
    lines = content.split('\n')
    
    # Find all image lines and their positions
    image_lines = []
    for i, line in enumerate(lines):
        if line.strip().startswith('<img src="../images/') and 'style="float: left;' in line:
            image_lines.append(i)
    
    if len(image_lines) <= 1:
        return content  # Nothing to fix
    
    # Remove all existing images and clear divs
    filtered_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Skip image lines and their associated clear divs
        if (line.strip().startswith('<img src="../images/') or 
            line.strip() == '<div style="clear: both;"></div>' or
            (line.strip() == '' and i > 0 and i < len(lines)-1 and 
             lines[i-1].strip().startswith('<img src="../images/'))):
            i += 1
            continue
        filtered_lines.append(line)
        i += 1
    
    # Get the image HTML from the original content
    images = []
    for i in image_lines:
        if i < len(lines):
            images.append(lines[i])
    
    # Find good insertion points in the filtered content
    insertion_points = []
    for i, line in enumerate(filtered_lines):
        # After main headings (##)
        if line.startswith('## '):
            # Look for end of the section's first paragraph
            para_start = i + 1
            while para_start < len(filtered_lines) and not filtered_lines[para_start].strip():
                para_start += 1
            
            para_end = para_start
            while (para_end < len(filtered_lines) and 
                   filtered_lines[para_end].strip() and 
                   not filtered_lines[para_end].startswith('#') and
                   not filtered_lines[para_end].startswith('- ') and
                   not re.match(r'^\d+\.', filtered_lines[para_end])):
                para_end += 1
            
            if para_end > para_start:  # Found a paragraph
                insertion_points.append(para_end)
        
        # After substantial lists
        elif line.startswith('- ') or re.match(r'^\d+\.', line):
            list_end = i + 1
            while (list_end < len(filtered_lines) and 
                   (filtered_lines[list_end].startswith('- ') or 
                    filtered_lines[list_end].startswith('  ') or
                    re.match(r'^\d+\.', filtered_lines[list_end]))):
                list_end += 1
            
            if list_end > i + 2:  # Multi-item list
                insertion_points.append(list_end)
    
    # Distribute images across insertion points
    if insertion_points and images:
        # Select evenly spaced insertion points
        num_images = min(len(images), 3)  # Limit to 3 images max
        if len(insertion_points) >= num_images:
            spacing = len(insertion_points) // num_images
            selected_points = [insertion_points[i * spacing] for i in range(num_images)]
        else:
            selected_points = insertion_points[:num_images]
        
        # Insert images at selected points (in reverse order to maintain indices)
        result_lines = filtered_lines[:]
        for i, (point, img_html) in enumerate(zip(reversed(selected_points), reversed(images[:len(selected_points)]))):
            # Insert image
            result_lines.insert(point, '')
            result_lines.insert(point + 1, img_html)
            result_lines.insert(point + 2, '')
            
            # Add clear div 6-8 lines later
            clear_pos = min(point + 8, len(result_lines))
            result_lines.insert(clear_pos, '')
            result_lines.insert(clear_pos + 1, '<div style="clear: both;"></div>')
            result_lines.insert(clear_pos + 2, '')
        
        return '\n'.join(result_lines)
    
    return '\n'.join(filtered_lines)

def fix_all_files():
    """Fix image placement in all markdown files"""
    for md_file in PAGES_DIR.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has stacked images
        if content.count('<img src="../images/') > 1:
            print(f"🔧 Fixing image placement in {md_file.name}")
            
            fixed_content = fix_image_placement(content)
            
            if fixed_content != content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"  ✅ Fixed {md_file.name}")
            else:
                print(f"  📝 No changes needed for {md_file.name}")

if __name__ == "__main__":
    print("🔧 Fixing image placement in markdown files...")
    fix_all_files()
    print("\n✅ Image placement fixing complete!")