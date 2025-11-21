#!/usr/bin/env python3
"""
Build script to convert Markdown files to static HTML website.
"""
import markdown
from pathlib import Path
import shutil


def build_site():
    """Convert tutorial.md to HTML and generate static site."""
    # Setup paths
    source_file = Path("tutorial.md")
    template_file = Path("template.html")
    output_dir = Path("output")
    static_dir = Path("static")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Copy static files to output
    if static_dir.exists():
        output_static = output_dir / "static"
        if output_static.exists():
            shutil.rmtree(output_static)
        shutil.copytree(static_dir, output_static)
    
    # Read markdown content
    with open(source_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    # Configure markdown with extensions
    md = markdown.Markdown(
        extensions=[
            "extra",  # Includes tables, fenced code blocks, etc.
            "codehilite",  # Syntax highlighting
            "toc",  # Table of contents
            "pymdownx.superfences",  # Better code blocks
            "pymdownx.tabbed",  # Tabbed content
            "pymdownx.details",  # Collapsible blocks (foldouts)
            "admonition",  # Admonitions (note, warning, etc.)
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "linenums": False,
            },
            "pymdownx.tabbed": {
                "alternate_style": True,
            },
        }
    )
    
    # Convert markdown to HTML
    html_content = md.convert(md_content)
    
    # Extract title from first H1 or use default
    title = "Minimal Agent"
    if md_content.strip().startswith("# "):
        title = md_content.split("\n")[0].replace("# ", "")
    
    # Read template
    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Replace placeholders in template
    final_html = template.replace("{{ title }}", title)
    final_html = final_html.replace("{{ content }}", html_content)
    
    # Write output HTML
    output_file = output_dir / "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"✓ Built site successfully!")
    print(f"  - Output: {output_file}")
    print(f"  - Open: file://{output_file.absolute()}")


if __name__ == "__main__":
    build_site()

