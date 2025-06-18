# Phase 6: Admin Dashboard & Analytics

## Purpose
Provide admin users with tools to manage system configurations, monitor usage, and troubleshoot failures.

---

## Admin Features

### 1. System Configuration
- Editable values from `system_configurations` table:
  - AI model defaults
  - Thread/article limits
  - Source thresholds
- Endpoint: `GET /admin/system-config`
- Endpoint: `PUT /admin/system-config`

### 2. User Management
- View all users
- Filter by subscription tier, usage level
- Deactivate/reactivate accounts
- Endpoint: `GET /admin/users`

### 3. Usage Analytics
- Daily active users
- Requests per day/week/month
- Top topics
- API quota stats (used vs. allowed)
- Endpoint: `GET /admin/usage-analytics`

### 4. Failure Logs
- View failed requests with error messages
- Investigate rate limit or LLM timeout issues
- Option to retry failed requests

### 5. Debug Tools
- Search by `request_id` or `user_id`
- View request → source → summary → content pipeline
- Download logs for support or bug reports

---

## UI Recommendations
- Role-based access control for `/admin` pages
- Graphs: Line charts (DAU), bar charts (topics), pie (platform usage)
- Notifications for high error rates or LLM failures

## Frontend Enhancements
- Admin tab in dashboard
- Use role claims in JWT to gate access

---

## Completion Criteria
- [x] Admins can view and update system config
- [x] Usage analytics and logs visible
- [x] Access gated by role and auth

## Notes
- Store admin actions in audit log table (future)
- Add background jobs to clean stale or failed content

---

> **Next: Performance tuning, security hardening, and deployment prep.**
