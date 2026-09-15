"""
BhashaSetu - Translation Schemas (Step 2 — updated)
Pydantic request/response models for the /translate endpoint.
"""

from typing import Optional
from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    """Request schema for text translation."""
    text: str = Field(
        ...,
        min_length=1,
        description="Input text to be translated",
        examples=["Water is important for life."],
    )
    source_language: str = Field(
        ...,
        min_length=2,
        max_length=10,
        description="Source language ISO/BCP-47 code",
        examples=["en"],
    )
    target_language: str = Field(
        ...,
        min_length=2,
        max_length=10,
        description="Target language ISO/BCP-47 code",
        examples=["pa"],
    )


class TranslationResponse(BaseModel):
    """Response schema for text translation."""
    status: str = Field(default="success", description="Response status")
    source_language: str = Field(..., description="Source language code")
    target_language: str = Field(..., description="Target language code")
    original_text: str = Field(..., description="Preprocessed input text")
    translated_text: Optional[str] = Field(default=None, description="Translated output text")
    simplified_text: Optional[str] = Field(default=None, description="Simplified text output")
    translation: Optional[str] = Field(default=None, description="Alias for translated_text for backward compatibility")
    engine: Optional[str] = Field(default=None, description="Translation engine/model used")
    message: Optional[str] = Field(default=None, description="Additional status message, if any")


class SupportedLanguagesResponse(BaseModel):
    """Response schema for supported languages and language pairs."""
    status: str = Field(default="success", description="Response status")
    supported_languages: dict[str, str] = Field(..., description="Mapping of language codes to language names")
    supported_pairs: list[list[str]] = Field(..., description="List of supported [source, target] language pairs")

