# Minimal Agent Website

This repository hosts the code for [minimal-agent.com](https://minimal-agent.com), a minimalistic one-page website that teaches you how to build a minimal AI agent for terminal use.

## Structure

- `docs/index.md` - Main content in Markdown format
- `docs/stylesheets/` - Custom CSS for the site
- `mkdocs.yml` - MkDocs configuration
- `site/` - Generated static website (git-ignored)

## Building the Site

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Build the site:
   ```bash
   mkdocs build
   ```

3. The generated site will be in the `site/` directory. Open `site/index.html` in your browser.

## Development Mode

For live development with automatic rebuilding and hot reload:

```bash
mkdocs serve
```

This will:
- Start a local server at `http://localhost:8000`
- Watch for changes to markdown and configuration files
- Automatically rebuild and reload the site when files change
- No need to refresh your browser!

You can specify a custom port:

```bash
mkdocs serve -a localhost:3000
```

## Deployment

To deploy to GitHub Pages:

```bash
mkdocs gh-deploy
```

## Markdown Features

The site uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and supports:

- Standard Markdown syntax
- Inline HTML content
- Code blocks with syntax highlighting and line numbers
- Admonitions (notes, warnings, etc.)
- Tabbed content
- Collapsible sections (details/summary)
- Dark/light theme toggle

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
