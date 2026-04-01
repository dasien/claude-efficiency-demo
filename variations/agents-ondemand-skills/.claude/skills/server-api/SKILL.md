---
name: server-api
description: REST API development patterns using Flask or FastAPI, including routing, request validation, error handling, and API design best practices.
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
