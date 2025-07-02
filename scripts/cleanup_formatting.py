#!/usr/bin/env python3
"""
Clean up remaining formatting artifacts in markdown files
"""

import re
import os
from pathlib import Path

def clean_artifacts(content):
    """Remove Word formatting artifacts"""
    # Remove Word formatting comments and artifacts
    content = re.sub(r'Formatted:[^\n]*\n?', '', content)
    content = re.sub(r'No bullets or numbering[^\n]*\n?', '', content)
    content = re.sub(r'Right: \d+ cm[^\n]*\n?', '', content)
    content = re.sub(r'Space After: \d+ pt[^\n]*\n?', '', content)
    
    # Remove excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r' {2,}', ' ', content)
    
    # Remove trailing whitespace
    lines = content.split('\n')
    lines = [line.rstrip() for line in lines]
    content = '\n'.join(lines)
    
    return content

def main():
    pages_dir = Path('pages-content')
    
    for md_file in pages_dir.glob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = clean_artifacts(content)
        
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Cleaned artifacts from: {md_file.name}")
        else:
            print(f"No artifacts found in: {md_file.name}")

if __name__ == "__main__":
    main()