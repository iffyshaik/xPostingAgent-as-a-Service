# Development Guidelines

## Project Structure
```
/project_root/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Env + app settings
│   ├── database.py            # DB engine/session
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── api/                   # API routes
│   ├── agents/                # AI logic modules
│   ├── services/              # Business logic
│   ├── utils/                 # Helpers
│   └── tests/                 # Pytest test files
├── alembic/                   # DB migrations
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Coding Conventions
- Use **snake_case** for variables/functions
- Use **PascalCase** for class names
- Keep all user-specific DB queries filtered by `user_id`
- Use `datetime.utcnow()` (not `now()`) for all timestamps

---

## Error Handling
```python
try:
    # main logic
except SpecificError as e:
    logger.error(f"Failure: {e}", extra={"user_id": user_id, "request_id": request_id})
    raise HTTPException(status_code=400, detail="Something went wrong")
```
- Create custom exception classes for reusable error types
- Always log the error with relevant context

---

## Logging
- Use structured logging format (JSON or key-value)
- Log at stages: request → research → summary → content → post
- Always log:
  - `request_id`, `user_id`
  - stage name, error (if any), status

---

## Testing Strategy
- **Unit tests**: agents, services, utilities
- **Integration tests**: API endpoints
- Use **mocking** for:
  - External APIs (LLM, Google)
  - DB writes in unit tests
- Roll back DB in tests using transactions

---

## API Design
- Use FastAPI with Pydantic schemas for strict input/output
- Return JSON responses with `success`, `data`, and `error`
- Use `Depends(get_current_user)` for auth validation

---

## Deployment & CI/CD (Future)
- Linting: `black` + `isort`
- Type checking: `mypy`
- Optional: Add pre-commit hooks

---

> **These guidelines help maintain clarity, testability, and scalability across the codebase.**
