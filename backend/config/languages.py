"""
BhashaSetu - Language Configuration (Step 2 — updated)
Centralised source of truth for supported language codes, names,
model mappings, and opus-mt language-tag mappings.

Design rules:
  - NEVER add a language here unless the active model genuinely supports it.
  - NEVER hard-code language logic inside routes/ or services/.
  - All code that needs language metadata must import from this module.

Current active model : Helsinki-NLP/opus-mt-en-mul  (MarianMT)
  - Supports 150+ languages from English via target-language tags (>>lang<<).
  - Runs on CPU (~300 MB weights).  No CUDA required.
  - Verified target-language tags are listed in MARIAN_TARGET_TAG below.

Planned upgrade: ai4bharat/IndicTrans2
  - Higher quality for Indic scripts.
  - Requires CUDA GPU + ~2–4 GB VRAM.
  - Swap out TRANSLATION_MODEL_MAP and MARIAN_TARGET_TAG when ready.
"""

from typing import Dict, Optional


# ---------------------------------------------------------------------------
# 1.  Supported language registry
#     Only languages that the active model actually handles.
#     "en" is always the source; all others are target languages.
# ---------------------------------------------------------------------------
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "en": "English",        # Source language only
    "pa": "Punjabi",        # Gurmukhi script  — verified: >>pan_Guru<<
    "hi": "Hindi",          # Devanagari       — verified: >>hin<<
    "bn": "Bengali",        # Bengali script   — verified: >>ben<<
    "mr": "Marathi",        # Devanagari       — verified: >>mar<<
    "ta": "Tamil",          # Tamil script     — verified: >>tam<<
    "te": "Telugu",         # Telugu script    — verified: >>tel<<
    "gu": "Gujarati",       # Gujarati script  — verified: >>guj<<
    "kn": "Kannada",        # Kannada script   — verified: >>kan<<
    "ml": "Malayalam",      # Malayalam script — verified: >>mal<<
    "ur": "Urdu",           # Perso-Arabic     — verified: >>urd<<
    # Activate additional languages after confirming model output quality:
    # "or": "Odia",         # >>ori<<
    # "as": "Assamese",     # >>asm<<
    # "si": "Sinhala",      # >>sin<<
}

# ---------------------------------------------------------------------------
# 2.  Supported translation pairs
#     The active model translates FROM English only.
#     Add reverse pairs (e.g. pa → en) once a reverse model is integrated.
# ---------------------------------------------------------------------------
SUPPORTED_PAIRS: set = {
    ("en", "pa"),
    ("en", "hi"),
    ("en", "bn"),
    ("en", "mr"),
    ("en", "ta"),
    ("en", "te"),
    ("en", "gu"),
    ("en", "kn"),
    ("en", "ml"),
    ("en", "ur"),
}

# ---------------------------------------------------------------------------
# 3.  HuggingFace model identifier for each translation direction.
#     opus-mt-en-mul handles all en→X pairs via a target-language tag.
#     Swap to IndicTrans2 here without touching any other file.
# ---------------------------------------------------------------------------
TRANSLATION_MODEL_MAP: Dict[tuple, str] = {
    # All en→ pairs share one model; the target language is set via a tag.
    ("en", "pa"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "hi"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "bn"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "mr"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "ta"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "te"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "gu"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "kn"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "ml"): "Helsinki-NLP/opus-mt-en-mul",
    ("en", "ur"): "Helsinki-NLP/opus-mt-en-mul",
}

# ---------------------------------------------------------------------------
# 4.  Marian target-language tags
#     opus-mt-en-mul expects the target language as a prefix token
#     in the form ">>lang_code<< <input text>".
#     Each code here was confirmed against tok.supported_language_codes.
# ---------------------------------------------------------------------------
MARIAN_TARGET_TAG: Dict[str, str] = {
    "pa": ">>pan_Guru<<",   # Punjabi (Gurmukhi script)
    "hi": ">>hin<<",        # Hindi
    "bn": ">>ben<<",        # Bengali
    "mr": ">>mar<<",        # Marathi
    "ta": ">>tam<<",        # Tamil
    "te": ">>tel<<",        # Telugu
    "gu": ">>guj<<",        # Gujarati
    "kn": ">>kan<<",        # Kannada
    "ml": ">>mal<<",        # Malayalam
    "ur": ">>urd<<",        # Urdu
}

# Human-readable engine name surfaced in API responses.
ACTIVE_ENGINE = "Helsinki-NLP/opus-mt-en-mul (MarianMT) — CPU inference"

# Notes for developers:
# ─────────────────────
# - The previous model (opus-mt-en-pun) was removed from HuggingFace Hub.
# - opus-mt-en-mul supports 150+ languages including all major Indic scripts.
# - For production quality on Indic scripts, IndicTrans2 is recommended.
# - IndicTrans2 requires ~2–4 GB VRAM and a CUDA-capable GPU.
# - To upgrade: update TRANSLATION_MODEL_MAP values and remove MARIAN_TARGET_TAG
#   (IndicTrans2 uses a different tokenisation approach).


# ---------------------------------------------------------------------------
# 5.  Helper functions — import these; do not inline language logic elsewhere.
# ---------------------------------------------------------------------------

def is_language_supported(code: str) -> bool:
    """Return True if the language code is in the supported registry."""
    return code in SUPPORTED_LANGUAGES


def is_pair_supported(source: str, target: str) -> bool:
    """Return True if the (source, target) translation pair is supported."""
    return (source, target) in SUPPORTED_PAIRS


def get_language_name(code: str) -> str:
    """Return the human-readable language name for a code, or 'Unknown'."""
    return SUPPORTED_LANGUAGES.get(code, "Unknown")


def get_marian_target_tag(target_language: str) -> Optional[str]:
    """
    Return the Marian target-language prefix tag for opus-mt-en-mul,
    e.g. '>>pan_Guru<<' for Punjabi.

    Returns None if the language has no tag (e.g. it uses a different model).
    """
    return MARIAN_TARGET_TAG.get(target_language)


def get_supported_languages() -> Dict[str, str]:
    """Return a dictionary of all supported language codes and their names."""
    return dict(SUPPORTED_LANGUAGES)


def get_supported_pairs() -> list[list[str]]:
    """Return a sorted list of supported [source, target] language pairs."""
    return sorted([[src, tgt] for src, tgt in SUPPORTED_PAIRS])

