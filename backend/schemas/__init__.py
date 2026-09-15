"""
BhashaSetu - Schemas Module
Exports all Pydantic request and response models across domains.
"""

from .translation import TranslationRequest, TranslationResponse
from .speech import (
    SpeechToTextRequest,
    SpeechToTextResponse,
    TextToSpeechRequest,
    TextToSpeechResponse,
)
from .assessment import EvaluationRequest, EvaluationResponse
from .lessons import LessonUploadRequest, LessonUploadResponse

__all__ = [
    "TranslationRequest",
    "TranslationResponse",
    "SpeechToTextRequest",
    "SpeechToTextResponse",
    "TextToSpeechRequest",
    "TextToSpeechResponse",
    "EvaluationRequest",
    "EvaluationResponse",
    "LessonUploadRequest",
    "LessonUploadResponse",
]
