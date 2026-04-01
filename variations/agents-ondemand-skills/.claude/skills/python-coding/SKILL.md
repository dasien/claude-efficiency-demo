---
name: python-coding
description: Python coding standards, style guidelines, and best practices for writing clean, idiomatic Python code.
---

## Python Coding Standards

### Style & Formatting
- Follow PEP 8 style guidelines strictly
- Use 4 spaces for indentation (never tabs)
- Maximum line length: 88 characters (Black formatter default)
- Use snake_case for functions and variables, PascalCase for classes
- Use UPPER_SNAKE_CASE for constants
- Add type hints to all function signatures

### Code Organization
- One class per file when classes are substantial
- Group imports: stdlib, third-party, local (separated by blank lines)
- Use `if __name__ == "__main__":` guard for executable scripts
- Keep functions focused — each should do one thing well
- Prefer composition over inheritance

### Error Handling
- Use specific exception types, never bare `except:`
- Raise exceptions early, catch them late
- Provide descriptive error messages that help the user understand what went wrong
- Use custom exception classes for domain-specific errors when appropriate

### Documentation
- Add docstrings to all public functions and classes (Google style)
- Include type information in docstrings when type hints aren't sufficient
- Write comments only for non-obvious logic — prefer self-documenting code

### Best Practices
- Use f-strings for string formatting (not % or .format())
- Prefer list comprehensions over map/filter for simple transformations
- Use `pathlib.Path` instead of `os.path` for file operations
- Use context managers (`with` statements) for resource management
- Prefer `dataclasses` or `namedtuple` over plain dicts for structured data
