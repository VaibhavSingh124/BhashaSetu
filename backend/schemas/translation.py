"""
BhashaSetu - Translation Schemas
Pydantic data models for the translation endpoint.
"""

from typing import Optional
from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    """Request schema for text translation."""
    text: str = Field(..., min_length=1, description="Input text to be translated", examples=["Hello"])
    source_language: str = Field(..., min_length=2, max_length=10, description="Source language ISO/BCP-47 code", examples=["en"])
    target_language: str = Field(..., min_length=2, max_length=10, description="Target language ISO/BCP-47 code", examples=["pa"])


class TranslationResponse(BaseModel):
    """Response schema for text translation."""
    status: str = Field(default="success", description="Response status")
    message: Optional[str] = Field(default="Module will be implemented in the next step", description="Status message")
    translation: Optional[str] = Field(default=None, description="Translated text output (placeholder for Step 1)")
