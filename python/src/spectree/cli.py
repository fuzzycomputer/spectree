#!/usr/bin/env python3
"""
SpecTree CLI - Composable Markdown files using @ references.
"""

import sys
import tempfile
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .core import render, CircularReferenceError


app = typer.Typer(
    name="spectree",
    help="Render SpecTree Markdown files by resolving @ references.",
    add_completion=False,
)

console = Console()
error_console = Console(stderr=True)


@app.command()
def main(
    file_path: Optional[str] = typer.Argument(
        None,
        help="Path to the markdown file to render. If not provided, reads from stdin.",
    )
) -> None:
    """
    Render a SpecTree file by resolving all @ references.
    
    Examples:
        spectree app.md
        cat app.md | spectree
        spectree app.md > output.md
    """
    try:
        if file_path:
            # Convert string to Path and validate
            path_obj = Path(file_path)
            if not path_obj.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            if not path_obj.is_file():
                raise FileNotFoundError(f"Path is not a file: {file_path}")
            
            # Render file from argument
            result = render(path_obj)
        else:
            # Read from stdin and render
            stdin_content = sys.stdin.read()
            
            # Create a temporary file in the current working directory
            # This allows relative references to work correctly
            current_dir = Path.cwd()
            with tempfile.NamedTemporaryFile(
                mode='w', 
                suffix='.md', 
                dir=current_dir,
                delete=False
            ) as tmp_file:
                tmp_file.write(stdin_content)
                tmp_file.flush()
                tmp_path = Path(tmp_file.name)
            
            try:
                result = render(tmp_path)
            finally:
                # Clean up temporary file
                tmp_path.unlink(missing_ok=True)
        
        # Output result to stdout
        print(result, end="")
        
    except FileNotFoundError as e:
        error_console.print(f"[red]Error:[/red] {e}", style="red")
        raise typer.Exit(1)
    
    except CircularReferenceError as e:
        error_console.print(f"[red]Error:[/red] {e}", style="red")
        raise typer.Exit(1)
    
    except Exception as e:
        error_console.print(f"[red]Unexpected error:[/red] {e}", style="red")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()