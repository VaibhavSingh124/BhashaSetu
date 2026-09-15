"""
BhashaSetu - Lesson Schemas
Pydantic data models for lesson creation and upload endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class LessonUploadRequest(BaseModel):
    """Request schema for uploading or creating a new lesson."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the lesson", examples=["Basic Punjabi Greetings"])
    language: str = Field(default="pa", min_length=2, max_length=10, description="Language code for the lesson", examples=["pa"])
    level: str = Field(default="beginner", description="Difficulty level (beginner/intermediate/advanced)", examples=["beginner"])
    content: str = Field(..., min_length=1, description="Lesson curriculum content or structured markdown", examples=["Lesson content on greetings and everyday phrases"])


class LessonUploadResponse(BaseModel):
    """Response schema for lesson upload."""
    status: str = Field(default="success", description="Response status")
    message: Optional[str] = Field(default="Module will be implemented in the next step", description="Status message")
    lesson_id: Optional[str] = Field(default=None, description="Generated identifier for uploaded lesson (placeholder for Step 1)")
