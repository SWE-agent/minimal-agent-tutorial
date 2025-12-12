# Minimal Agent Tutorial

> Source code for [minimal-agent.com](https://minimal-agent.com) — a tutorial that teaches you how to build an AI coding agent from scratch.

## What is this?

This repo contains the **documentation website** for the Minimal Agent tutorial. It's a static site built with MkDocs that teaches developers how to build a terminal-based AI agent in ~60 lines of Python.

**Looking for the actual agent code?**
- 📦 [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) — The full implementation (~74% on SWE-bench verified)
- 📄 [minimal-agent.com](https://minimal-agent.com) — The tutorial (copy-paste code from here)

## What the tutorial covers

- Querying LLM APIs (OpenAI, Anthropic, OpenRouter, LiteLLM)
- Parsing agent actions from model output
- Executing bash commands safely
- Building the agent loop
- System prompts and advanced patterns

## Local development

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open http://localhost:8000

## Contributing

The tutorial content is in `docs/index.md`. Edit that file and submit a PR.

This site uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) which supports admonitions, tabs, code highlighting, and more.
