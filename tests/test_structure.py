"""
BhashaSetu - Repository Structure & Import Verification Tests (Step 0)
"""

import sys
import os

# Add backend directory to Python sys.path for test execution
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)


def test_routes_importable():
    """Verify that route modules can be imported."""
    from routes import translation_router, speech_router, assessment_router, lessons_router
    assert translation_router is not None
    assert speech_router is not None
    assert assessment_router is not None
    assert lessons_router is not None


def test_services_importable():
    """Verify that service classes can be imported."""
    from services import TranslationService, ASRService, TTSService, EvaluatorService
    assert TranslationService is not None
    assert ASRService is not None
    assert TTSService is not None
    assert EvaluatorService is not None


def test_schemas_importable():
    """Verify that Pydantic schemas can be imported."""
    from schemas import (
        TranslationRequest, TranslationResponse,
        SpeechToTextRequest, SpeechToTextResponse,
        TextToSpeechRequest, TextToSpeechResponse,
        EvaluationRequest, EvaluationResponse,
        LessonUploadRequest, LessonUploadResponse,
    )
    assert TranslationRequest is not None
    assert TranslationResponse is not None
    assert SpeechToTextRequest is not None
    assert SpeechToTextResponse is not None
    assert TextToSpeechRequest is not None
    assert TextToSpeechResponse is not None
    assert EvaluationRequest is not None
    assert EvaluationResponse is not None
    assert LessonUploadRequest is not None
    assert LessonUploadResponse is not None

