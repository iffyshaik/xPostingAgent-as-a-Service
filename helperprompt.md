We are building a social media posting agent saas tool. 
the current_context.md file gives you context on where we are. The master DevSpec has been broken down into indivual files, to make it easy to complete come in a session. after each session the current_context.md file should be updated. 

you must update the current_context file properly and include what the current file structure looks like, so its easy for the next session to pick up. You should also include all the function names and what they do in each file. This way we will avoid recreating functions in future sessions. 

Please refer to the supporting docs in the Project Files section for more context. 

Its important, that you do this step by step, guiding me through everything, including library installations. where mutliple files need to be created, please show me the name i should use and the code. 

please also put comment code in every single file so that we know what it does (especially at the top). Non-coder and students will learn from this. Please also follow the instructions written in the instructions section. 

Lets start by implementing phase1-db-setup.md


#########################################################################################


I'm continuing development on my SaaS project, xPostingAgent-as-a-Service.

It’s a multi-tenant platform that uses LLMs to turn user-submitted topics into social media content, based on user tone, style, and platform preferences.

---

✅ Here's what's already working (as of last session):

- 🔐 **Auth**: JWT login/logout works; routes protected via `AuthProvider` and `ProtectedRoute`
- 🧭 **Navigation**: Top navbar routes between Dashboard, Submit, Config, and Schedule pages
- 📝 **Submit Page** (`/submit`):
  - Form with topic, content type, platform
  - Supports `auto_post` and `include_citations` flags
  - Works end-to-end: sends data to backend `POST /content/requests`

- ⚙️ **Config Page** (`/config`):
  - Loads user config via `GET /users/configurations`
  - Saves updates via `PUT /users/configurations`
  - Fields: `persona`, `tone`, `style` (free text); `language`, `platform_preference`, `research_preference` (dropdowns)
  - Uses custom reusable `Input.tsx` and `Select.tsx`

- 🧠 Backend:
  - `get_current_user()` returns user ID as `int`, not a full object
  - `UserConfiguration` and `Request` models in place
  - Routes and schemas properly separated (Pydantic schemas live in `app/schemas/`)

---

📁 Relevant files already exist:

- `frontend/src/pages/SubmitTopic.tsx`
- `frontend/src/pages/UserConfig.tsx`
- `frontend/src/components/Input.tsx`, `Select.tsx`
- `app/api/users.py` — handles GET and PUT config routes
- `app/schemas/user_configurations.py` — contains `UpdateUserConfig`
- `app/models/user_configurations.py`
- `app/dependencies.py` — `get_current_user()` returns `int`

---

✅ What I want to do next:

➡️ Build the `/dashboard` page:
- Show all current content requests (status = pending, researching, summarizing, etc.)
- Show quota info (`GET /users/usage-stats`)
- Use `GET /content/requests` to load content request history

---

❗Important: Before writing any new code, please ask me:
> “Does this already exist?”  
> Check whether the route, file, or component already exists before assuming anything.

This helps avoid conflicts with existing models, routes, or structure.

Please guide me step by step, clearly, and comment all code so it’s easy for me to learn and understand.

Let’s begin with Step 1 of the dashboard when ready.
