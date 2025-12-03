#!/usr/bin/env python3
"""
Build script to convert Markdown files to static HTML website.
"""
import argparse
import http.server
import socketserver
import threading
import time
from pathlib import Path
import shutil
import markdown
from pygments.formatters import HtmlFormatter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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
    
    # Generate Pygments CSS for syntax highlighting (both light and dark themes)
    output_static = output_dir / "static"
    output_static.mkdir(exist_ok=True)
    
    # Light theme
    formatter_light = HtmlFormatter(style='default')
    pygments_css_light = formatter_light.get_style_defs('.highlight')
    with open(output_static / "pygments-light.css", "w") as f:
        f.write(pygments_css_light)
    
    # Dark theme
    formatter_dark = HtmlFormatter(style='github-dark')
    pygments_css_dark = formatter_dark.get_style_defs('.highlight')
    with open(output_static / "pygments-dark.css", "w") as f:
        f.write(pygments_css_dark)
    
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
            },
            # "pymdownx.superfences": {
            #     "legacy_tab_classes": True,
            # },
            "pymdownx.tabbed": {
                "alternate_style": True,
            },
        },
    )
    
    # Convert markdown to HTML
    html_content = md.convert(md_content)
    
    # Extract title from first H1 or use default
    title = "Minimal Agent"
    if md_content.strip().startswith("# "):
        title = md_content.split("\n")[0].replace("# ", "")
    
    # Get the table of contents from the markdown processor
    toc_html = md.toc if hasattr(md, 'toc') else ""
    
    # Read template
    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()
    
    # Replace placeholders in template
    final_html = template.replace("{{ title }}", title)
    final_html = final_html.replace("{{ content }}", html_content)
    final_html = final_html.replace("{{ toc }}", toc_html)
    
    # Write output HTML
    output_file = output_dir / "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"✓ Built site successfully!")
    print(f"  - Output: {output_file}")
    print(f"  - Open: file://{output_file.absolute()}")


class ChangeHandler(FileSystemEventHandler):
    """Watch for file changes and rebuild the site."""
    
    def __init__(self):
        self.last_build = 0
        self.debounce_seconds = 0.5
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only rebuild for relevant files
        relevant_extensions = {'.md', '.html', '.css', '.js'}
        file_path = Path(event.src_path)
        
        if file_path.suffix not in relevant_extensions:
            return
        
        # Debounce - avoid rebuilding too frequently
        current_time = time.time()
        if current_time - self.last_build < self.debounce_seconds:
            return
        
        self.last_build = current_time
        print(f"\n🔄 Detected change in {file_path.name}, rebuilding...")
        try:
            build_site()
            print("✓ Rebuild complete!")
        except Exception as e:
            print(f"✗ Build failed: {e}")


def serve_site(port=8000):
    """Start a local development server."""
    output_dir = Path("output")
    
    if not output_dir.exists():
        print("Building site first...")
        build_site()
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(output_dir), **kwargs)
        
        def log_message(self, format, *args):
            # Suppress standard server logs for cleaner output
            pass
    
    # Start file watcher in background
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()
    
    # Start HTTP server
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"\n🚀 Development server running at http://localhost:{port}")
        print("📝 Watching for file changes...")
        print("   Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Stopping server...")
            observer.stop()
            observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build static site from Markdown")
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start development server with live reload"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for development server (default: 8000)"
    )
    
    args = parser.parse_args()
    
    if args.serve:
        serve_site(args.port)
    else:
        build_site()

