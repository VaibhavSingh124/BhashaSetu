"""
BhashaSetu - Config Module
"""
from .languages import (
    SUPPORTED_LANGUAGES,
    SUPPORTED_PAIRS,
    TRANSLATION_MODEL_MAP,
    ACTIVE_ENGINE,
    is_language_supported,
    is_pair_supported,
    get_language_name,
)

__all__ = [
    "SUPPORTED_LANGUAGES",
    "SUPPORTED_PAIRS",
    "TRANSLATION_MODEL_MAP",
    "ACTIVE_ENGINE",
    "is_language_supported",
    "is_pair_supported",
    "get_language_name",
]
