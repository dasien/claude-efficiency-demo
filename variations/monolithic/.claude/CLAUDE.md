# Project Guidelines

You are working on a Python software project. Follow all guidelines below when writing code, designing architecture, gathering requirements, and testing.

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

---

## Requirements Gathering

When starting a new feature or project:

1. **Identify core requirements**: What must the software do? List each functional requirement explicitly.
2. **Identify constraints**: Performance requirements, compatibility needs, deployment environment.
3. **Define the user interface**: How will users interact with the software? CLI args, interactive prompts, API, etc.
4. **Identify edge cases**: What unusual inputs or conditions must be handled?
5. **Define success criteria**: How will you know the implementation is complete and correct?
6. **Prioritize**: Separate must-have from nice-to-have features. Implement must-haves first.

Always confirm your understanding of requirements before writing code. Restate them in your own words.

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

---

## Tkinter GUI Development

### Application Structure
- Use a class-based approach with a main `App` class inheriting from `tk.Tk`
- Separate GUI layout from business logic using MVC or MVP pattern
- Initialize all widgets in a `_create_widgets()` method
- Bind events in a separate `_bind_events()` method

### Widget Layout
- Use `grid()` for complex layouts, `pack()` for simple vertical/horizontal stacking
- Never mix `grid()` and `pack()` in the same container
- Use `ttk` themed widgets over plain `tk` widgets for modern appearance
- Group related widgets in `LabelFrame` or `Frame` containers

### Layout Best Practices
```python
# Use grid with sticky for responsive layouts
self.entry = ttk.Entry(self.main_frame)
self.entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

# Configure column weights for resizing
self.main_frame.columnconfigure(0, weight=1)
```

### Event Handling
- Use `command=` parameter for button clicks
- Use `bind()` for keyboard events: `widget.bind('<Return>', handler)`
- Use `bind_all()` sparingly — prefer widget-specific bindings
- Event handlers should delegate to controller/business logic, not contain logic themselves
- Use `after()` for delayed or periodic operations, never `time.sleep()` in the main thread

### Common Patterns
```python
class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self._create_widgets()
        self._bind_events()

    def _create_widgets(self):
        self.display = ttk.Entry(self, font=("Courier", 18))
        self.display.grid(row=0, column=0, columnspan=4, sticky="ew")

    def _bind_events(self):
        self.bind('<Return>', self._on_calculate)
```

### Dialog and Messaging
- Use `messagebox.showerror()` for error dialogs
- Use `messagebox.showinfo()` for informational messages
- Use `simpledialog.askstring()` for simple text input
- For complex dialogs, create custom `Toplevel` windows

### Styling
- Use `ttk.Style()` for consistent theming
- Define styles at application startup, not per-widget
- Use named fonts via `tkFont.Font()` for consistent typography

### Threading
- Never perform long operations on the main thread — use `threading.Thread`
- Update GUI only from the main thread — use `after()` to schedule updates
- Use `queue.Queue` to communicate between worker threads and the main thread

### Testing GUI Code
- Separate all logic from GUI code to enable unit testing without Tkinter
- Test business logic independently
- For integration tests, use `tkinter.Tk()` in test fixtures with `update_idletasks()`
- Consider using `pytest-tk` for automated GUI testing

---

## REST API Development

### Framework Choice
- Use **FastAPI** for new projects — async support, automatic OpenAPI docs, Pydantic validation
- Use **Flask** for simpler projects or when async isn't needed
- Both support WSGI/ASGI deployment behind Gunicorn or Uvicorn

### API Design Principles
- Use RESTful resource naming: `/users`, `/users/{id}`, `/users/{id}/orders`
- Use HTTP methods correctly: GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)
- Return appropriate status codes: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 500 (Server Error)
- Use consistent JSON response format across all endpoints

### Request/Response Format
```python
# FastAPI example
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    price: float
    description: str | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    # Business logic here
    return ItemResponse(id=1, **item.dict())
```

### Error Handling
- Use HTTP status codes consistently
- Return error details in a standard format: `{"error": "message", "detail": "specifics"}`
- Use framework exception handlers for consistent error formatting
- Log server errors (5xx) but not client errors (4xx)

### Validation
- Validate all input at the API boundary using Pydantic models (FastAPI) or marshmallow (Flask)
- Never trust client input — validate types, ranges, formats
- Return 422 Unprocessable Entity for validation failures
- Include field-level error details in validation error responses

### Authentication & Authorization
- Use JWT tokens for stateless authentication
- Implement middleware for auth checks
- Use dependency injection (FastAPI) or decorators (Flask) for route-level authorization
- Store secrets in environment variables, never in code

### Database Integration
- Use an ORM (SQLAlchemy) or query builder for database access
- Use connection pooling for production deployments
- Implement database migrations with Alembic
- Use transactions for multi-step operations

### Testing APIs
```python
# FastAPI testing
from fastapi.testclient import TestClient

def test_create_item():
    client = TestClient(app)
    response = client.post("/items", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201
    assert response.json()["name"] == "Widget"
```

### Documentation
- Use OpenAPI/Swagger for API documentation (automatic in FastAPI)
- Document all endpoints with descriptions, parameters, and response schemas
- Include example requests and responses
- Document error responses for each endpoint

### Performance
- Use async endpoints for I/O-bound operations
- Implement pagination for list endpoints: `?page=1&per_page=20`
- Use caching headers (ETag, Cache-Control) where appropriate
- Consider rate limiting for public APIs

---

## C# Coding Standards

### Naming Conventions
- **PascalCase** for classes, methods, properties, events, namespaces: `UserService`, `GetUserById`
- **camelCase** for local variables and parameters: `userName`, `orderId`
- **_camelCase** for private fields: `_userRepository`, `_logger`
- **IPascalCase** for interfaces: `IUserService`, `IRepository<T>`
- **UPPER_CASE** is NOT used in C# — use PascalCase for constants too: `MaxRetryCount`

### Code Organization
- One class per file, file name matches class name
- Use namespaces that mirror folder structure
- Order members: fields, constructors, properties, public methods, private methods
- Use `#region` sparingly — prefer smaller classes over regions

### Modern C# Features (C# 10+)
```csharp
// File-scoped namespaces
namespace MyApp.Services;

// Records for immutable data
public record UserDto(string Name, string Email, int Age);

// Pattern matching
var result = shape switch
{
    Circle c => Math.PI * c.Radius * c.Radius,
    Rectangle r => r.Width * r.Height,
    _ => throw new ArgumentException("Unknown shape")
};

// Nullable reference types
public string? GetMiddleName(int userId) { ... }
```

### Dependency Injection
- Register services in `Program.cs` or `Startup.cs`
- Use constructor injection — never `new` up dependencies directly
- Register as `Scoped` for request-lifetime, `Singleton` for app-lifetime, `Transient` for per-use
- Use `IOptions<T>` pattern for configuration

### Error Handling
- Use specific exception types: `ArgumentNullException`, `InvalidOperationException`
- Throw exceptions for exceptional conditions, not for flow control
- Use `Result<T>` pattern for expected failures (validation, business rules)
- Implement global exception middleware in ASP.NET Core
- Log exceptions with structured logging (Serilog, Microsoft.Extensions.Logging)

### Async/Await
- Use `async`/`await` for all I/O operations
- Suffix async methods with `Async`: `GetUserAsync()`
- Never use `.Result` or `.Wait()` — always await
- Use `CancellationToken` in async methods
- Prefer `ValueTask<T>` over `Task<T>` for hot paths that often complete synchronously

### LINQ Best Practices
- Prefer method syntax for complex queries, query syntax for joins
- Use `Any()` instead of `Count() > 0`
- Avoid multiple enumeration — materialize with `ToList()` when reused
- Use `Select()` for projections, `Where()` for filtering

### Testing with xUnit
```csharp
public class UserServiceTests
{
    [Fact]
    public async Task GetUser_ValidId_ReturnsUser()
    {
        var service = new UserService(mockRepo.Object);
        var result = await service.GetUserAsync(1);
        Assert.NotNull(result);
        Assert.Equal("John", result.Name);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task GetUser_InvalidId_ThrowsArgumentException(int id)
    {
        var service = new UserService(mockRepo.Object);
        await Assert.ThrowsAsync<ArgumentException>(() => service.GetUserAsync(id));
    }
}
```

### Project Structure
```
src/
├── MyApp.Api/           # ASP.NET Core web API
├── MyApp.Core/          # Domain models, interfaces
├── MyApp.Infrastructure/# Data access, external services
└── MyApp.Tests/         # Unit and integration tests
```

---

## SQL Development

### Schema Design
- Use singular table names: `user`, `order`, `product` (not `users`, `orders`)
- Every table must have a primary key — prefer `id BIGINT AUTO_INCREMENT`
- Use foreign keys to enforce referential integrity
- Add indexes on columns used in WHERE, JOIN, and ORDER BY clauses
- Use `NOT NULL` by default — only allow NULL when absence of a value is meaningful

### Naming Conventions
- **snake_case** for table and column names: `user_account`, `created_at`
- Prefix foreign keys with the referenced table: `user_id`, `order_id`
- Prefix boolean columns with `is_` or `has_`: `is_active`, `has_verified_email`
- Name indexes descriptively: `idx_user_email`, `idx_order_created_at`

### Query Best Practices
```sql
-- Always specify columns, never SELECT *
SELECT u.id, u.name, u.email
FROM user u
WHERE u.is_active = TRUE
ORDER BY u.created_at DESC
LIMIT 20 OFFSET 0;

-- Use JOINs explicitly, never implicit joins in WHERE
SELECT o.id, o.total, u.name
FROM order o
INNER JOIN user u ON u.id = o.user_id
WHERE o.status = 'completed';

-- Use parameterized queries to prevent SQL injection
-- NEVER concatenate user input into SQL strings
```

### Index Strategy
- Create indexes for columns in WHERE clauses used frequently
- Use composite indexes for multi-column queries (leftmost prefix rule)
- Don't over-index — each index slows down writes
- Use `EXPLAIN` to verify query plans and index usage
- Consider covering indexes for frequently-run queries

### Stored Procedures
```sql
CREATE PROCEDURE GetUserOrders(
    @UserId BIGINT,
    @Status VARCHAR(20) = NULL
)
AS
BEGIN
    SELECT o.id, o.total, o.created_at
    FROM [order] o
    WHERE o.user_id = @UserId
      AND (@Status IS NULL OR o.status = @Status)
    ORDER BY o.created_at DESC;
END;
```

### Migrations
- Use sequential, timestamped migration files: `001_create_user_table.sql`
- Every migration must be reversible — include both UP and DOWN scripts
- Never modify a migration that has been applied to production
- Test migrations against a copy of production data before deploying

### Transaction Management
```sql
BEGIN TRANSACTION;
    UPDATE account SET balance = balance - 100 WHERE id = 1;
    UPDATE account SET balance = balance + 100 WHERE id = 2;

    IF @@ERROR <> 0
        ROLLBACK;
    ELSE
        COMMIT;
```

### Performance Optimization
- Use `EXPLAIN ANALYZE` (PostgreSQL) or `SET STATISTICS IO ON` (SQL Server) to profile queries
- Avoid `SELECT *` — only fetch columns you need
- Use `EXISTS` instead of `IN` for subqueries with large result sets
- Batch large INSERT/UPDATE operations to avoid lock contention
- Use connection pooling in application code
- Consider read replicas for read-heavy workloads

### Common Anti-Patterns to Avoid
- **N+1 queries**: Use JOINs or batch fetching instead of looping queries
- **Missing indexes**: Profile slow queries and add targeted indexes
- **Over-normalization**: Denormalize for read performance when appropriate
- **Implicit type conversion**: Ensure WHERE clause types match column types
- **Large transactions**: Keep transactions as short as possible
- **No foreign keys**: Always use FKs unless you have a specific reason not to (e.g., partitioning)

### Data Types
- Use `VARCHAR(n)` for variable-length strings, `CHAR(n)` for fixed-length
- Use `DECIMAL(p,s)` for money/financial values, never `FLOAT`
- Use `TIMESTAMP WITH TIME ZONE` for dates (PostgreSQL) or `DATETIMEOFFSET` (SQL Server)
- Use `BOOLEAN` or `BIT` for true/false values
- Use `UUID`/`UNIQUEIDENTIFIER` for distributed IDs
