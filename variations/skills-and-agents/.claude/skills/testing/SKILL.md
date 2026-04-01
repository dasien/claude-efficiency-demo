---
name: testing
description: Testing methodology, pytest best practices, and test organization for Python projects.
---

## Testing Methodology

### Testing Framework
- Use **pytest** as the testing framework
- Place tests in files named `test_*.py` or `*_test.py`
- Name test functions with `test_` prefix and descriptive names: `test_addition_with_positive_numbers`

### Test Organization
- Group related tests in classes (optional, but useful for organization)
- Use `@pytest.mark.parametrize` for testing multiple inputs with the same logic
- Keep test files alongside the code they test (not in a separate `tests/` directory for small projects)

### What to Test
- **Happy path**: Normal expected inputs produce correct outputs
- **Edge cases**: Zero, negative numbers, very large numbers, decimal precision
- **Error cases**: Invalid inputs, division by zero, missing arguments
- **Boundary conditions**: Empty input, whitespace-only input, special characters

### Test Best Practices
- Each test should test one thing and have a descriptive name
- Tests should be independent — no test should depend on another test's state
- Use `pytest.raises` for testing expected exceptions
- Prefer direct assertions over complex test logic
- Aim for 100% coverage of business logic functions

### Running Tests
Always use `python3` (not `python`) to run commands on this system.
```bash
python3 -m pytest -v                    # Verbose output
python3 -m pytest -v --tb=short         # Shorter tracebacks
python3 -m pytest test_file.py          # Run specific file
python3 -m pytest -k "test_name"        # Run specific test by name
```
