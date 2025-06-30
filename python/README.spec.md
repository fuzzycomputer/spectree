# Python Implementation Spec

This specification describes implementation details for the SpecTree Python package.

The project is already configured with dependencies in pyproject.toml. Use the existing tools and patterns.

## Core Implementation

### The render() Function

The heart of SpecTree is a single pure function in `core.py`:

```python
def render(path: Path) -> str:
    """
    Render a SpecTree file by resolving all @ references.
    
    Args:
        path: Path to the root markdown file
        
    Returns:
        The complete rendered markdown as a string
        
    Raises:
        FileNotFoundError: If a referenced file doesn't exist
        CircularReferenceError: If circular references are detected
    """
```

This function:
- Takes a Path to a markdown file
- Recursively resolves all @ references
- Returns the complete document as a string
- Handles all edge cases described in the root README.spec.md

### Custom Exception

Define a custom exception for circular references:

```python
class CircularReferenceError(Exception):
    """Raised when circular references are detected in SpecTree files."""
    pass
```

### CLI Wrapper

The CLI in `cli.py` is a thin wrapper around render():
- Use Typer for argument parsing
- Use Rich for error formatting
- Support both file argument and stdin
- Output to stdout
- Errors to stderr with proper exit codes

## Implementation Notes

1. **Keep core.py pure**: No CLI concerns, just the algorithm
2. **Minimal CLI**: The CLI should be so simple it barely needs testing
3. **Path handling**: Use pathlib.Path throughout
4. **Error messages**: Clear, actionable error messages
5. **No external dependencies in core**: The render() function should only depend on Python stdlib