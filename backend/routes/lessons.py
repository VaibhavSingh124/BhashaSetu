"""
BhashaSetu - Lessons Routes
Handles HTTP endpoints for curriculum modules, structured lessons, and learning tracks.
Logic and database queries will be implemented in subsequent steps.
"""

from fastapi import APIRouter, status

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.get("/", status_code=status.HTTP_200_OK)
async def lessons_status():
    """
    Health / status check endpoint for lessons service.
    """
    return {
        "service": "lessons",
        "status": "initialized",
        "version": "v1"
    }


@router.get("/list", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def list_lessons():
    """
    List available lessons for a selected language track.
    Implementation deferred to Step 1+.
    """
    return {
        "message": "Lessons list endpoint placeholder. Logic will be implemented in subsequent steps."
    }
