"""
BhashaSetu - Speech Schemas
Pydantic data models for Speech-to-Text (ASR) and Text-to-Speech (TTS) endpoints.
"""

from typing import Optional
from pydantic import BaseModel, Field


class SpeechToTextRequest(BaseModel):
    """Request schema for speech-to-text (ASR)."""
    audio_base64: str = Field(..., min_length=1, description="Base64 encoded audio payload")
    language: str = Field(default="pa", min_length=2, max_length=10, description="Language code of spoken audio", examples=["pa"])


class SpeechToTextResponse(BaseModel):
    """Response schema for speech-to-text (ASR)."""
    status: str = Field(default="success", description="Response status")
    message: Optional[str] = Field(default="Module will be implemented in the next step", description="Status message")
    text: Optional[str] = Field(default=None, description="Transcribed text output (placeholder for Step 1)")


class TextToSpeechRequest(BaseModel):
    """Request schema for text-to-speech (TTS)."""
    text: str = Field(..., min_length=1, description="Text to synthesize into speech", examples=["ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ"])
    language: str = Field(default="pa", min_length=2, max_length=10, description="Target language code", examples=["pa"])
    voice_gender: Optional[str] = Field(default="female", description="Voice gender preference (female/male)", examples=["female"])


class TextToSpeechResponse(BaseModel):
    """Response schema for text-to-speech (TTS)."""
    status: str = Field(default="success", description="Response status")
    message: Optional[str] = Field(default="Module will be implemented in the next step", description="Status message")
    audio_url: Optional[str] = Field(default=None, description="URL or data identifier of synthesized audio (placeholder for Step 1)")
