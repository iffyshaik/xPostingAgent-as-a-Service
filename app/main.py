# app/main.py
"""
Entrypoint for the FastAPI application.
This initialises the app and includes routes such as authentication.
"""

from fastapi import FastAPI
from app.api import auth,  content_queue, agent_pipeline
# --- Swagger UI Bearer Token Setup (for clean Authorize button) ---
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

from fastapi.middleware.cors import CORSMiddleware


# This defines the type of security scheme Swagger UI should use.
# We're telling it to use HTTP Bearer tokens — the "Authorization: Bearer <token>" header.
security_scheme = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
}


# This function overrides the default OpenAPI generator used by FastAPI.
# It injects our security scheme globally into the API docs.
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    # Generate the standard OpenAPI schema
    openapi_schema = get_openapi(
        title="Your API",                           # Shown in Swagger UI
        version="1.0.0",
        description="Posting agent SaaS API",       # Describe your API
        routes=app.routes,
    )
    
    # Inject our custom BearerAuth scheme into the security definitions
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": security_scheme
    }
    
    # Apply BearerAuth as a global requirement for all endpoints
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title="Social Media Posting Agent API",
    version="0.1.0",
    description="Handles user authentication and future agent interactions."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Include the content_queue routes
app.include_router(content_queue.router)

# Set the app's OpenAPI generator to our custom one
app.openapi = custom_openapi

app.include_router(agent_pipeline.router)  

from app.api import content_requests  # 👈 add this

app.include_router(content_requests.router)  # 👈 add this too

#FOR TESTING
from app.api import user_config_seed
app.include_router(user_config_seed.router)

from app.api import dev_patch_summaries
app.include_router(dev_patch_summaries.router)

from app.api import users  # <- make sure this import is here
app.include_router(users.router)
