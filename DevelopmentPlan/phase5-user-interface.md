# Phase 5: User Interface

## Purpose
Provide a user-facing UI for submitting topics, configuring preferences, reviewing generated content, and approving or scheduling posts.

---

## Core Pages

### 1. Dashboard
- Show active requests, drafts, scheduled posts
- Display usage stats: daily quota, history

### 2. Submit Topic
- Input field for topic
- Dropdowns for:
  - Content type (`thread`, `article`)
  - Platform (`x`, `typefully`)
- Advanced settings toggle (for tone, style, etc.)

### 3. User Configuration
- Persona: free-text
- Tone: dropdown
- Style: dropdown
- Language: dropdown
- Research preference: `general`, `science_heavy`, `balanced`
- Default platform: `x`, `typefully`

### 4. Request Detail View
- Original topic → Generated topic → Sources → Summary → Draft
- Edit & approve content (inline or modal editor)
- Show metadata:
  - Tweet count / Article length
  - Citation toggle

### 5. Scheduled Posts
- List view of upcoming scheduled content
- Option to reschedule, delete

---

## Authentication
- Login/register flow
- Store JWT in local storage
- Secure all API calls with Bearer token

## Frontend Tech Stack (suggested)
- **Framework**: React + TypeScript
- **UI Library**: Tailwind CSS + Headless UI
- **State Management**: React Query or Zustand
- **API Client**: Axios

---

## Completion Criteria
- [x] Can submit a topic with full user config
- [x] Can view and approve generated content
- [x] Can schedule or post content
- [x] UI state synced with backend

## Notes
- Add loading/success/error indicators for API calls
- Keep all content scoped to logged-in user only
- Use optimistic UI updates where applicable

---

> **Next: Admin dashboard and monitoring tools for production readiness.**
