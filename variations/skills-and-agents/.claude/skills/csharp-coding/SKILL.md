---
name: csharp-coding
description: C# coding standards, .NET patterns, and best practices for writing clean, maintainable C# applications.
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
