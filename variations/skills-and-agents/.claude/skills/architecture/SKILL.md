---
name: architecture
description: Software architecture guidelines, design principles, and project structure patterns for Python applications.
---

## Software Architecture

### Design Principles
- **Separation of concerns**: Keep business logic separate from I/O (input parsing, output formatting)
- **Single Responsibility**: Each module/class should have one reason to change
- **DRY (Don't Repeat Yourself)**: Extract shared logic into reusable functions
- **KISS (Keep It Simple)**: Choose the simplest solution that meets requirements
- **YAGNI (You Aren't Gonna Need It)**: Don't build features that aren't required

### Project Structure for CLI Applications
```
project/
├── main_module.py      # Core business logic (pure functions, no I/O)
├── cli.py              # CLI interface (argparse or input loop)
├── test_module.py      # Tests
└── requirements.txt    # Dependencies
```

For small projects, combining business logic and CLI into a single file is acceptable if the file stays under ~200 lines.

### Design Patterns for CLI Tools
- Parse all input in one place, validate it, then pass clean data to business logic
- Return results from functions rather than printing directly — this makes testing easier
- Use an enum or constants for operation types rather than raw strings
- Structure the main loop clearly: read → parse → validate → execute → display

### Requirements Gathering
1. **Identify core requirements**: What must the software do? List each functional requirement explicitly.
2. **Identify constraints**: Performance requirements, compatibility needs, deployment environment.
3. **Define the user interface**: How will users interact with the software?
4. **Identify edge cases**: What unusual inputs or conditions must be handled?
5. **Define success criteria**: How will you know the implementation is complete and correct?
6. **Prioritize**: Separate must-have from nice-to-have features. Implement must-haves first.
