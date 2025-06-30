from pathlib import Path
from typing import Set


class CircularReferenceError(Exception):
    """Raised when circular references are detected in SpecTree files."""
    pass


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
    return _render_recursive(path, set())


def _render_recursive(path: Path, processing_stack: Set[Path]) -> str:
    """
    Recursively render a SpecTree file.
    
    Args:
        path: Path to the current file being processed
        processing_stack: Set of files currently being processed (for cycle detection)
        
    Returns:
        The rendered content of the file
        
    Raises:
        FileNotFoundError: If a referenced file doesn't exist
        CircularReferenceError: If circular references are detected
    """
    # Resolve the path to handle symlinks and relative paths consistently
    resolved_path = path.resolve()
    
    # Check for circular references
    if resolved_path in processing_stack:
        raise CircularReferenceError(f"Circular reference detected involving: {resolved_path}")
    
    # Add current file to processing stack
    processing_stack = processing_stack | {resolved_path}
    
    try:
        # Read the file content
        content = path.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
    # Process each line
    lines = content.splitlines(keepends=True)
    result_lines = []
    
    for line in lines:
        # Check if line starts with @ (valid reference syntax)
        line_stripped = line.rstrip('\r\n')
        if line_stripped.startswith('@') and not line_stripped.startswith('@@'):
            # Extract the path after @
            ref_path_str = line_stripped[1:]
            
            # Validate reference syntax - must be entire line content after @, no leading whitespace
            if ref_path_str and ref_path_str.endswith('.md') and not ref_path_str.startswith('@') and not ref_path_str[0].isspace():
                # Resolve path relative to current file's directory
                ref_path = path.parent / ref_path_str
                
                try:
                    # Recursively render the referenced file
                    referenced_content = _render_recursive(ref_path, processing_stack)
                    # Preserve the line ending from the original line
                    line_ending = line[len(line_stripped):]
                    result_lines.append(referenced_content + line_ending)
                except FileNotFoundError:
                    # Re-raise with original reference for better error messages
                    raise FileNotFoundError(f"File not found: {ref_path_str}")
            else:
                # Invalid reference syntax - leave unchanged
                result_lines.append(line)
        else:
            # Not a reference - leave unchanged  
            result_lines.append(line)
    
    # Join lines back together
    return ''.join(result_lines)