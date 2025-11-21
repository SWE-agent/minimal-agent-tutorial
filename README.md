# Minimal Agent Website

This repository hosts the code for [minimal-agent.com](https://minimal-agent.com), a minimalistic one-page website that teaches you how to build a minimal AI agent for terminal use.

## Structure

- `tutorial.md` - Main content in Markdown format
- `template.html` - HTML template for the static site
- `static/` - Static assets (CSS, etc.)
- `build.py` - Python script to generate the static HTML website
- `output/` - Generated static website (git-ignored)

## Building the Site

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the site:
   ```bash
   python build.py
   ```

3. The generated site will be in the `output/` directory. Open `output/index.html` in your browser.

## Markdown Features

The site supports:
- Standard Markdown syntax
- Inline HTML content
- Code blocks with syntax highlighting
- Admonitions (notes, warnings, etc.)
- Tabbed content
- Collapsible sections (details/summary)

### Example Admonition

Use `!!!` syntax for admonitions:

```markdown
!!! note "This is a note"
    This is the content of the note.
```

### Example Tabbed Content

```markdown
=== "Tab 1"
    Content for tab 1

=== "Tab 2"
    Content for tab 2
```

### Example Foldout

```markdown
??? "Click to expand"
    Hidden content here
```

