# API Specification Reference

## Authentication Endpoints
```
POST /auth/register
POST /auth/login
POST /auth/logout
POST /auth/refresh
GET  /auth/me
```

## User Management
```
GET  /users/profile
PUT  /users/profile
GET  /users/configurations
PUT  /users/configurations
GET  /users/usage-stats
```

## Content Generation Workflow
```
POST   /content/requests                     # Submit topic
GET    /content/requests                     # List user requests
GET    /content/requests/{request_id}        # Detail view
DELETE /content/requests/{request_id}        # Delete request
POST   /content/requests/{request_id}/regenerate
```

## Content Queue
```
GET    /content/queue
GET    /content/queue/{content_id}
PUT    /content/queue/{content_id}/approve
POST   /content/queue/{content_id}/post
PUT    /content/queue/{content_id}/schedule
DELETE /content/queue/{content_id}
```

## Admin Endpoints
```
GET /admin/system-config
PUT /admin/system-config
GET /admin/users
GET /admin/usage-analytics
```

## API Standards
- All endpoints secured with Bearer JWT token unless public
- JSON request/response format
- Response object pattern:
```json
{
  "success": true,
  "data": {},
  "error": null
}
```

## Notes
- Return 401 for auth errors, 403 for forbidden, 422 for bad input
- Use pagination for list endpoints where applicable
- Rate-limit all modifying endpoints

---

> **Use this as a reference when wiring up frontend or API clients.**
