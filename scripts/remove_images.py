#!/usr/bin/env python3
"""
Remove all image references from markdown files
"""

import re
from pathlib import Path

PAGES_DIR = Path("pages-content")

def remove_images_from_md(file_path):
    """Remove all image tags and clear divs from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove image tags
    content = re.sub(r'<img[^>]*>', '', content)
    
    # Remove clear divs
    content = re.sub(r'<div style="clear: both;"></div>', '', content)
    
    # Remove empty lines that might be left behind
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    print("🖼️  Removing images from markdown files...")
    
    files_processed = 0
    
    # Process all markdown files
    for md_file in PAGES_DIR.glob("*.md"):
        try:
            remove_images_from_md(md_file)
            files_processed += 1
            print(f"✅ Cleaned {md_file.name}")
        except Exception as e:
            print(f"❌ Error processing {md_file.name}: {e}")
    
    print(f"\n🎉 Processed {files_processed} markdown files")
    print("All image references have been removed from markdown files")

if __name__ == "__main__":
    main()