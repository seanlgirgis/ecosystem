#!/usr/bin/env python3
"""Resume Generator - Simplified for Ecosystem

Usage:
    python generate.py --target resume --format docx
    python generate.py --target tailored --layout data/resume_tailored.yaml
"""

import yaml
import sys
import argparse
from pathlib import Path

# Add parent dir to path for renderers
sys.path.insert(0, str(Path(__file__).parent))

from renderers.docx_renderer import DocxRenderer
from renderers.html_renderer import HtmlRenderer
from renderers.pdf_renderer import PdfRenderer
from renderers.md_renderer import MdRenderer


def load_yaml(path):
    """Safely loads a YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def resolve_references(content_list, store_data):
    """Merge layout config with store.yaml content."""
    if not store_data:
        return content_list
    
    resolved_list = []
    for block in content_list:
        block_copy = block.copy()
        config = block_copy.get('config', {}).copy()
        
        content_key = config.get('content_key')
        if content_key:
            store_item = store_data.get(content_key)
            if store_item:
                merged_config = store_item.copy()
                merged_config.update(config)
                config = merged_config
            else:
                print(f"WARNING: Content key '{content_key}' not found in store.")
        
        block_copy['config'] = config
        resolved_list.append(block_copy)
    return resolved_list


def generate_resume(layout_path, store_data, theme, output_dir, output_name):
    """Generate resume in all formats from layout."""
    
    base_dir = Path(__file__).parent
    
    # Load and resolve layout
    layout = load_yaml(layout_path)
    sections = layout.get('sections', [])
    resolved = resolve_references(sections, store_data)
    layout['sections'] = resolved
    
    # DOCX
    print(f"Generating DOCX: {output_name}.docx")
    renderer_docx = DocxRenderer(theme)
    renderer_docx.render(layout)
    renderer_docx.save(output_dir / f"{output_name}.docx")
    
    # HTML
    print(f"Generating HTML: {output_name}.html")
    renderer_html = HtmlRenderer(theme, base_dir)
    html_content = renderer_html.render(layout, mode='web')
    renderer_html.save(html_content, output_dir / f"{output_name}.html")
    
    # Markdown
    print(f"Generating MD: {output_name}.md")
    renderer_md = MdRenderer(theme)
    md_content = renderer_md.render(layout)
    renderer_md.save(md_content, output_dir / f"{output_name}.md")
    
    # PDF
    try:
        print(f"Generating PDF: {output_name}.pdf")
        html_for_pdf = renderer_html.render(layout, mode='pdf')
        renderer_pdf = PdfRenderer(theme)
        footer_config = layout.get('config', {}).get('footer')
        renderer_pdf.render_from_html(html_for_pdf, str(output_dir / f"{output_name}.pdf"), footer_config=footer_config)
    except Exception as e:
        print(f"PDF generation skipped: {e}")
    
    print(f"\nDone! Output: {output_dir}/{output_name}.*")


def main():
    parser = argparse.ArgumentParser(description="Resume Generator")
    parser.add_argument('--target', default='resume', help='Target layout file (without .yaml)')
    parser.add_argument('--format', default='all', help='Output format (docx, html, md, pdf, all)')
    parser.add_argument('--output', default='resume', help='Output filename')
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent
    
    # Load style
    style_path = base_dir / 'data' / 'style.yaml'
    theme = load_yaml(style_path).get('theme', {}) if style_path.exists() else {}
    
    # Load store
    store_path = base_dir / 'data' / 'store.yaml'
    store_data = load_yaml(store_path) if store_path.exists() else {}
    
    # Load layout
    layout_path = base_dir / 'data' / f"{args.target}.yaml"
    if not layout_path.exists():
        print(f"Error: Layout not found: {layout_path}")
        print(f"Available layouts in data/:")
        for f in (base_dir / 'data').glob('*.yaml'):
            print(f"  - {f.stem}")
        return
    
    # Generate
    output_dir = base_dir / 'output'
    output_dir.mkdir(exist_ok=True)
    
    generate_resume(layout_path, store_data, theme, output_dir, args.output)


if __name__ == "__main__":
    main()
