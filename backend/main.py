"""
BhashaSetu - Main Backend Application Entry Point
FastAPI application with CORS configuration, health check endpoint,
and modular router mounting for Step 1 project foundation.
"""

import os
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from routes.translation import router as translation_router
from routes.speech import router as speech_router
from routes.assessment import router as assessment_router
from routes.lessons import router as lessons_router

# Initialize FastAPI application with comprehensive metadata for Swagger/OpenAPI
app = FastAPI(
    title="BhashaSetu API",
    description=(
        "Scalable Indic Language Learning, Translation, and Speech Platform. "
        "Step 1: Project foundation with modular routing, Pydantic schemas, and placeholder endpoints."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# -----------------------------------------------------------------------------
# CORS Configuration (Task 4)
# Configured for local development with Flutter Web/Mobile and local frontend tools.
# Safe defaults prevent wildcard origin abuse unless explicitly specified in production.
# -----------------------------------------------------------------------------
DEFAULT_DEVELOPMENT_ORIGINS = [
    "http://localhost:3000",   # Standard React / Web dev server
    "http://localhost:8000",   # Local backend / Swagger UI
    "http://localhost:8080",   # Flutter Web default local port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]

env_allowed_origins = os.getenv("ALLOWED_ORIGINS")
if env_allowed_origins:
    origins = [origin.strip() for origin in env_allowed_origins.split(",") if origin.strip()]
else:
    origins = DEFAULT_DEVELOPMENT_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Health Check Endpoint (Task 5)
# -----------------------------------------------------------------------------
@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="Root Health Check",
    description="Returns backend running status and confirmation message.",
)
async def root():
    """
    Health check endpoint verifying the backend is online.
    """
    return {
        "status": "success",
        "message": "BhashaSetu Backend is Running"
    }


# -----------------------------------------------------------------------------
# Router Registrations (Task 2)
# Mounts /translate, /speech-to-text, /text-to-speech, /evaluate, /lesson
# -----------------------------------------------------------------------------
app.include_router(translation_router)
app.include_router(speech_router)
app.include_router(assessment_router)
app.include_router(lessons_router)


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
