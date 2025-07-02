# SpecTree Python Implementation

A Python CLI for SpecTree - composable Markdown files using @ references.

## Installation

First, install uv (fast Python package manager):

https://docs.astral.sh/uv/

Then install spectree:
```bash
# From PyPI (as a global CLI tool)
uv tool install spectree-md

# Or from source:
git clone https://github.com/fuzzycomputer/spectree
cd spectree/python
uv tool install .
```

## Usage

The CLI follows the Unix philosophy - pipe in, pipe out:

```bash
# Primary usage: stdin to stdout
cat app.md | spectree > output.md

# Convenience: file argument
spectree app.md > output.md

# Output to terminal
spectree app.md
```

## Project Structure

```
python/
├── README.md                # User-facing documentation
├── README.spec.md           # Implementation details
├── TESTING.spec.md          # Test spec
├── pyproject.toml           # Package configuration
├── src/
│   └── spectree/
│       ├── __init__.py
│       ├── core.py          # Core render() function
│       └── cli.py           # CLI wrapper
└── tests/
    ├── test_core.py         # Core logic tests
    └── test_cli.py          # CLI interface tests
```

## Development

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install in development mode with all dependencies
uv pip install -e ".[dev]"
```

## Testing

```bash
# Run all tests
pytest
```