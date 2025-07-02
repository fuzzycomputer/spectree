# SpecTree

A simple format for composable Markdown trees using `@` references.

## What is SpecTree?

SpecTree is Markdown with one addition: the `@` operator for referencing other Markdown files via transclusion. This enables you to build trees of instructions from modular, reusable components.

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

## Motivation

Read the [introductory blog post](https://fuzzycomputer.com/posts/spectree) for the conceptual background.

SpecTree is designed for organizing complex instructions, particularly for AI systems:

- **AI prompts** - Complex multi-step instructions with reusable parts
- **Project specifications** - Modular architecture, features, and requirements  
- **Design systems** - Reusable color palettes, typography, components

## License

MIT