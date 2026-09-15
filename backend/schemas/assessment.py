"""
BhashaSetu - Assessment Schemas
Pydantic data models for pronunciation evaluation and scoring endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class EvaluationRequest(BaseModel):
    """Request schema for pronunciation evaluation."""
    audio_base64: str = Field(..., min_length=1, description="Base64 encoded audio of user speech")
    reference_text: str = Field(..., min_length=1, description="Reference text/sentence spoken by user", examples=["ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ"])
    language: str = Field(default="pa", min_length=2, max_length=10, description="Language code of target sentence", examples=["pa"])


class EvaluationResponse(BaseModel):
    """Response schema for pronunciation evaluation."""
    status: str = Field(default="success", description="Response status")
    message: Optional[str] = Field(default="Module will be implemented in the next step", description="Status message")
    score: Optional[float] = Field(default=None, description="Pronunciation accuracy score between 0.0 and 100.0 (placeholder for Step 1)")
    feedback: Optional[str] = Field(default=None, description="Actionable phoneme/fluency feedback (placeholder for Step 1)")
