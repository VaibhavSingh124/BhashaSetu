"""
BhashaSetu - Lessons Routes
Handles HTTP endpoints for curriculum modules, structured lessons, and learning tracks.
Logic and database queries will be implemented in subsequent steps.
"""

from fastapi import APIRouter, status
from schemas.lessons import LessonUploadRequest, LessonUploadResponse

router = APIRouter(tags=["Lessons"])


@router.post(
    "/lesson",
    response_model=LessonUploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload or create a lesson",
    description="Registers new lesson materials and curriculum content. Placeholder endpoint for Step 1 foundation.",
)
async def create_lesson(request: LessonUploadRequest) -> LessonUploadResponse:
    """
    Create or upload a curriculum lesson.
    Returns a standardized placeholder response during Step 1 foundation.
    """
    return LessonUploadResponse(
        status="success",
        message="Module will be implemented in the next step",
        lesson_id=None,
    )
