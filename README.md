# SpecTree

A simple format for composable Markdown trees using `@` references.

## What is SpecTree?

SpecTree is Markdown with one addition: the `@` operator for referencing other Markdown files via transclusion. This enables you to build trees of instructions from modular, reusable components.

As my LLM prompts and specs have gotten more complex, I wanted a simple way to
make plain English instructions more composable and reusable.

## Example

Given this file structure:
```
specs/
├── app.md
├── stack.md
└── design/
    ├── system.md
    └── colors.md
```

Where `app.md` contains:
```markdown
# My App

@stack.md
@design/system.md
@design/colors.md
```

SpecTree resolves these references into a single, complete Markdown document.

## Syntax

- The `@` operator must be the first character on a line
- Followed by a relative path to a Markdown file
- Paths are resolved relative to the current file
- Circular references are not allowed

## Implementations

- [Python](./python) - Install with `pip install spectree-md`
- [JavaScript](./javascript) - Install with `npm install spectree` *(coming soon)*

## License

MIT