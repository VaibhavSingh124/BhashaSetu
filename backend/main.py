"""
BhashaSetu - Main Backend Application Entry Point
Initializes the FastAPI application, registers middleware, and mounts API routers.
Logic and AI model bindings will be implemented in subsequent steps.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.translation import router as translation_router
from routes.speech import router as speech_router
from routes.assessment import router as assessment_router
from routes.lessons import router as lessons_router

# Initialize FastAPI application
app = FastAPI(
    title="BhashaSetu API",
    description="Scalable Indic Language Learning, Translation, and Speech Platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure Cross-Origin Resource Sharing (CORS)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health Check"])
async def root():
    """
    Root entry check providing service metadata.
    """
    return {
        "project": "BhashaSetu",
        "status": "online",
        "step": 0,
        "docs": "/docs"
    }


@app.get("/api/v1/health", tags=["Health Check"])
async def health_check():
    """
    API Health check endpoint for container orchestrators and monitoring.
    """
    return {
        "status": "healthy",
        "stage": "step_0_scaffolding"
    }


# Register modular routers under /api/v1 prefix
app.include_router(translation_router, prefix="/api/v1")
app.include_router(speech_router, prefix="/api/v1")
app.include_router(assessment_router, prefix="/api/v1")
app.include_router(lessons_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
