"""
BhashaSetu - Routes Module
Initializes and aggregates API routers for translation, speech, assessment, and lessons.
"""

from .translation import router as translation_router
from .speech import router as speech_router
from .assessment import router as assessment_router
from .lessons import router as lessons_router

__all__ = [
    "translation_router",
    "speech_router",
    "assessment_router",
    "lessons_router",
]
