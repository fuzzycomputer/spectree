# SpecTree Implementation Spec

This document provides additional implementation details for SpecTree beyond the basic concept described in README.md.

## File Resolution

### Path Resolution Rules
- Paths are resolved relative to the directory containing the referencing file
- Only relative paths are supported (no absolute paths)
- Parent directory references (`../`) are allowed
- Paths must use forward slashes (`/`) even on Windows
- The `.md` extension is required and must be explicit

### File System Boundaries
- References cannot escape the root directory of the initial file
- Symlinks are treated as regular files
- File system permissions should be respected

## Parsing Rules

### @ Operator Recognition
- `@` must be the first character on the line (column 0)
- No preceding whitespace is allowed
- The line must contain only `@` followed by the file path
- Empty lines before or after `@` references are preserved

### Invalid References
These should NOT be treated as transclusions:
- `  @file.md` (leading whitespace)
- `text @file.md` (not at start of line)
- `@@file.md` (double @)
- `@` (no path specified)
- `@file.txt` (non-markdown files)

## Processing Algorithm

### Resolution Steps
1. Parse the input file for `@` references
2. For each valid reference:
   - Resolve the relative path
   - Check for circular references
   - Read the referenced file
   - Recursively process any `@` references in that file
3. Replace each `@` reference with the resolved content
4. Preserve line endings from the original files

### Circular Reference Detection
- Maintain a stack of currently processing files
- If a file appears twice in the stack, it's a circular reference
- Circular references should result in an error, not infinite recursion

### Error Handling
When an error occurs:
- File not found: Include error message in output or fail entirely
- Circular reference: Fail with clear error message showing the cycle
- Permission denied: Fail with error message
- Invalid syntax: Leave the line unchanged (not treated as reference)

## Content Handling

### Character Encoding
- Assume UTF-8 encoding for all files
- Fail gracefully if encoding errors occur

### Whitespace
- Preserve all whitespace in content files
- Empty lines at the beginning or end of transcluded files are preserved

## Example Edge Cases

### Circular Reference
```
// a.md
@b.md

// b.md
@a.md
```
Error: Circular reference detected: a.md -> b.md -> a.md

### Missing File
```
// main.md
@nonexistent.md
```
Error: File not found: nonexistent.md

### Nested Folders
```
// main.md
@docs/overview.md

// docs/overview.md
@../shared/header.md
```
Valid: Resolves to shared/header.md relative to the original directory

## Future Considerations

These features are NOT part of the current spec but may be considered later:
- Remote URL support (`@https://example.com/file.md`)
- Partial file inclusion (`@file.md#section`)

## Implementation Notes

- Keep memory usage reasonable by streaming large files
- Consider maximum depth limits to prevent stack overflow
- File watching/hot reloading is outside the scope of core SpecTree