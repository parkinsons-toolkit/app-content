#!/usr/bin/env python3
"""
Generate sitemap files for the Parkinson's Toolkit web app
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from datetime import datetime

PAGES_DIR = Path("pages-content")
BASE_URL = "https://parkinsons-toolkit.com"  # Replace with your actual domain

def get_title_from_md(file_path):
    """Extract title from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for first # heading
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    # Fallback to filename
    return file_path.stem.replace('-', ' ').title()

def get_description_from_md(file_path):
    """Extract description from markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip title and find first paragraph
    for line in lines[1:]:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('!['):
            # Clean up markdown syntax and truncate
            desc = re.sub(r'[*_`]', '', line)
            desc = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', desc)  # Convert links to text
            return desc[:150] + '...' if len(desc) > 150 else desc
    
    return ""

def categorize_page(filename):
    """Categorize pages based on filename"""
    categories = {
        'information': ['what-is-parkinsons', 'living-with-parkinsons', 'new-diagnosis'],
        'wellbeing': ['optimising-wellbeing', 'keeping-active', 'eating-well', 'social-spiritual-life'],
        'management': ['symptom-management', 'medication', 'general-medical-advice'],
        'daily-life': ['daily-living', 'mobility', 'reading-writing-and-technology', 'travel'],
        'support': ['dealing-with-stress-and-challenges', 'guidance-for-families-and-carers', 'further-support'],
        'legal-financial': ['finances', 'legal-matters', 'housing'],
        'treatment': ['treatment-teams', 'who-may-be-involved', 'advanced-therapies-surgical-treatments', 'complementary-therapies'],
        'planning': ['planning-future-care', 'future-care-options', 'end-of-life'],
        'activities': ['hobbies-pets', 'work-and-caring'],
        'healthcare': ['appointments-hospital-stays', 'progression-of-symptoms'],
        'resources': ['services-groups', 'information-websites-apps', 'research'],
        'special': ['covid-19', 'practical-advice']
    }
    
    for category, pages in categories.items():
        if filename in pages:
            return category
    return 'general'

def generate_json_sitemap():
    """Generate JSON sitemap for web app consumption"""
    sitemap = {
        "lastUpdated": datetime.now().isoformat(),
        "totalPages": 0,
        "categories": {},
        "pages": []
    }
    
    # Add home page
    sitemap["pages"].append({
        "url": "/",
        "slug": "home",
        "title": "Parkinson's Toolkit",
        "description": "Comprehensive information and support for people living with Parkinson's disease",
        "category": "home",
        "priority": 1.0,
        "lastModified": datetime.now().isoformat()[:10]
    })
    
    # Process all markdown files
    for md_file in sorted(PAGES_DIR.glob("*.md")):
        if md_file.name == "home.md":
            continue  # Already added
            
        slug = md_file.stem
        title = get_title_from_md(md_file)
        description = get_description_from_md(md_file)
        category = categorize_page(slug)
        
        page_data = {
            "url": f"/{slug}",
            "slug": slug,
            "title": title,
            "description": description,
            "category": category,
            "priority": 0.8 if category in ['information', 'wellbeing'] else 0.6,
            "lastModified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()[:10]
        }
        
        sitemap["pages"].append(page_data)
        
        # Group by category
        if category not in sitemap["categories"]:
            sitemap["categories"][category] = []
        sitemap["categories"][category].append({
            "slug": slug,
            "title": title,
            "url": f"/{slug}"
        })
    
    sitemap["totalPages"] = len(sitemap["pages"])
    
    # Write JSON sitemap
    with open("sitemap.json", 'w', encoding='utf-8') as f:
        json.dump(sitemap, f, indent=2, ensure_ascii=False)
    
    return sitemap

def generate_xml_sitemap():
    """Generate XML sitemap for search engines"""
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Add home page
    url_elem = ET.SubElement(urlset, "url")
    ET.SubElement(url_elem, "loc").text = BASE_URL + "/"
    ET.SubElement(url_elem, "lastmod").text = datetime.now().isoformat()[:10]
    ET.SubElement(url_elem, "priority").text = "1.0"
    ET.SubElement(url_elem, "changefreq").text = "weekly"
    
    # Process all markdown files
    for md_file in sorted(PAGES_DIR.glob("*.md")):
        if md_file.name == "home.md":
            continue
            
        slug = md_file.stem
        category = categorize_page(slug)
        
        url_elem = ET.SubElement(urlset, "url")
        ET.SubElement(url_elem, "loc").text = f"{BASE_URL}/{slug}"
        ET.SubElement(url_elem, "lastmod").text = datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()[:10]
        ET.SubElement(url_elem, "priority").text = "0.8" if category in ['information', 'wellbeing'] else "0.6"
        ET.SubElement(url_elem, "changefreq").text = "monthly"
    
    # Write XML sitemap
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)

def generate_navigation_config():
    """Generate navigation configuration for web app"""
    sitemap_data = generate_json_sitemap()
    
    nav_config = {
        "mainNavigation": [
            {"title": "Home", "url": "/", "category": "home"},
            {"title": "What is Parkinson's?", "url": "/what-is-parkinsons", "category": "information"},
            {"title": "Living with Parkinson's", "url": "/living-with-parkinsons", "category": "information"},
            {"title": "Symptom Management", "url": "/symptom-management", "category": "management"},
            {"title": "Keeping Active", "url": "/keeping-active", "category": "wellbeing"},
            {"title": "Support", "url": "/further-support", "category": "support"}
        ],
        "categories": {}
    }
    
    # Organize pages by category for dropdown menus
    for category, pages in sitemap_data["categories"].items():
        nav_config["categories"][category] = {
            "title": category.replace('-', ' ').title(),
            "pages": pages
        }
    
    # Write navigation config
    with open("navigation.json", 'w', encoding='utf-8') as f:
        json.dump(nav_config, f, indent=2, ensure_ascii=False)
    
    return nav_config

def main():
    print("🗺️  Generating sitemaps...")
    
    # Generate all sitemap formats
    sitemap_data = generate_json_sitemap()
    generate_xml_sitemap()
    nav_config = generate_navigation_config()
    
    print(f"✅ Generated sitemaps with {sitemap_data['totalPages']} pages")
    print(f"📁 Categories: {', '.join(sitemap_data['categories'].keys())}")
    print("📄 Files created:")
    print("   - sitemap.json (for web app)")
    print("   - sitemap.xml (for search engines)")
    print("   - navigation.json (for app navigation)")

if __name__ == "__main__":
    main()