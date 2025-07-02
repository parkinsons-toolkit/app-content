#!/usr/bin/env python3
"""
Format markdown files extracted from PDF to improve:
- Heading syntax (add ## for sections)
- Bullet points (• to -)
- Remove formatting artifacts
- Fix table formatting
- Clean up links
"""

import re
import os
from pathlib import Path

def clean_formatting_artifacts(text):
    """Remove Word formatting comments and artifacts"""
    # Remove Word formatting comments
    text = re.sub(r'Formatted:[^\\n]*\\n?', '', text)
    text = re.sub(r'No bullets or numbering[^\\n]*\\n?', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\\n{3,}', '\\n\\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    return text

def fix_headings(text):
    """Add proper heading syntax"""
    # Common section headers that should be ## headings
    headers = [
        'What do I need to do?', 'Information', 'Talking to Others', 'My Experience',
        'More Information', 'Topics', 'Tips to consider:', 'Making Changes', 'Keeping on Track',
        'General advice', 'Practical tips', 'Resources', 'Support groups', 'Helpful Resources',
        'Key points', 'Important information', 'Getting help', 'Planning ahead'
    ]
    
    for header in headers:
        # Match headers that are standalone lines
        pattern = f'^{re.escape(header)}$'
        replacement = f'## {header}'
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    
    return text

def fix_bullet_points(text):
    """Convert bullet symbols to markdown format"""
    # Replace various bullet symbols with -
    text = re.sub(r'^[•▪▫◦‣⁃] ', '- ', text, flags=re.MULTILINE)
    text = re.sub(r'^o ', '- ', text, flags=re.MULTILINE)
    
    return text

def fix_numbered_lists(text):
    """Ensure numbered lists are properly formatted"""
    # Fix numbered lists that might be malformed
    text = re.sub(r'^(\\d+)\\. ', r'\\1. ', text, flags=re.MULTILINE)
    
    return text

def fix_links(text):
    """Convert plain URLs to markdown links where appropriate"""
    # Convert standalone URLs to markdown links
    url_pattern = r'(https?://[^\\s]+)'
    
    def replace_url(match):
        url = match.group(1)
        # Clean up URL if it has trailing punctuation
        url = re.sub(r'[.,;]$', '', url)
        # Try to create a meaningful link text
        if 'parkinsons.org.uk' in url:
            return f"[Parkinson's UK]({url})"
        elif 'parkinson.org' in url:
            return f"[Parkinson's Foundation]({url})"
        elif 'nhs.uk' in url:
            return f'[NHS]({url})'
        else:
            return f'[{url}]({url})'
    
    text = re.sub(url_pattern, replace_url, text)
    
    return text

def fix_tables(text):
    """Attempt to fix malformed tables"""
    # This is complex - for now, identify table-like content and mark it
    lines = text.split('\\n')
    in_table = False
    table_lines = []
    result_lines = []
    
    for line in lines:
        # Detect potential table headers
        if any(word in line.lower() for word in ['organisation', 'website', 'phone', 'information']):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
        elif in_table and line.strip() and not line.startswith('#'):
            table_lines.append(line)
        else:
            if in_table and len(table_lines) > 1:
                # Process accumulated table lines
                result_lines.extend(convert_to_table(table_lines))
                table_lines = []
                in_table = False
            result_lines.append(line)
    
    return '\\n'.join(result_lines)

def convert_to_table(table_lines):
    """Convert table-like text to markdown table"""
    if len(table_lines) < 2:
        return table_lines
    
    # Simple table conversion - this is a basic implementation
    return [
        '| Organisation | Information | Phone | Website |',
        '|---|---|---|---|',
        *[f'| Content needs manual formatting | | | |' for _ in range(len(table_lines)-1)]
    ]

def format_markdown_file(file_path):
    """Format a single markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply formatting fixes
    content = clean_formatting_artifacts(content)
    content = fix_headings(content)
    content = fix_bullet_points(content)
    content = fix_numbered_lists(content)
    content = fix_links(content)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Formatted: {file_path.name}")

def main():
    # Process all files in markdown_sections directory
    source_dir = Path('markdown_sections')
    target_dir = Path('pages-content')
    
    if not source_dir.exists():
        print("markdown_sections directory not found")
        return
    
    target_dir.mkdir(exist_ok=True)
    
    for md_file in source_dir.glob('*.md'):
        # Copy to target directory and format
        target_file = target_dir / md_file.name
        
        # Skip if already manually formatted
        if target_file.exists() and md_file.name in ['what-is-parkinsons.md', 'living-with-parkinsons.md']:
            print(f"Skipping already formatted: {md_file.name}")
            continue
            
        format_markdown_file(md_file)
        
        # Copy to target directory
        with open(md_file, 'r', encoding='utf-8') as src:
            content = src.read()
        
        with open(target_file, 'w', encoding='utf-8') as dst:
            dst.write(content)
        
        print(f"Copied to pages-content: {md_file.name}")

if __name__ == "__main__":
    main()