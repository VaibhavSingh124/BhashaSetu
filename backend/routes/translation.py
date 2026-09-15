"""
BhashaSetu - Translation Routes (Step 2)
Connects /translate and /api/v1/translate to the TranslationService pipeline.
Provides /supported-languages and /api/v1/supported-languages registry query.
Handles all validation, language, and model errors with proper HTTP responses.
"""

import logging
from fastapi import APIRouter, HTTPException, status

from config.languages import get_supported_languages, get_supported_pairs
from schemas.translation import (
    TranslationRequest,
    TranslationResponse,
    SupportedLanguagesResponse,
)
from services.translator import TranslationService, TranslationError

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Translation"])

# Single shared service instance — model is loaded lazily on first request.
# This keeps startup fast and avoids loading unused models.
_translation_service = TranslationService()


@router.post(
    "/translate",
    response_model=TranslationResponse,
    status_code=status.HTTP_200_OK,
    summary="Translate text across Indic languages",
    description=(
        "Translates input text from the source language to the target language "
        "using a neural machine translation model. "
        "Supports English (en) to Punjabi (pa), Hindi (hi), Bengali (bn), "
        "Marathi (mr), Tamil (ta), Telugu (te), Gujarati (gu), Kannada (kn), "
        "Malayalam (ml), and Urdu (ur)."
    ),
)
@router.post(
    "/api/v1/translate",
    response_model=TranslationResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def translate(request: TranslationRequest) -> TranslationResponse:
    """
    POST /translate and POST /api/v1/translate

    Pipeline:
      1. Preprocess input text (whitespace normalisation).
      2. Validate language codes and pair support.
      3. Run MarianMT (Helsinki-NLP/opus-mt-en-mul) model inference.
      4. Apply simplification pass.
      5. Return structured response.

    Error responses:
      400 — empty text, unsupported language, unsupported pair.
      503 — model unavailable or inference failure.
    """
    logger.info(
        "POST /translate: source=%s, target=%s, text_len=%d",
        request.source_language,
        request.target_language,
        len(request.text),
    )

    try:
        result = _translation_service.translate(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
        )
        return TranslationResponse(**result)

    except ValueError as exc:
        # Validation errors: empty text, unsupported language/pair
        logger.warning("Translation validation error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except TranslationError as exc:
        # Model-level errors: model not available, inference failed
        logger.error("Translation model error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Translation service unavailable: {exc}",
        ) from exc

    except Exception as exc:
        # Unexpected errors — never swallow them silently
        logger.exception("Unexpected translation error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again.",
        ) from exc


@router.get(
    "/supported-languages",
    response_model=SupportedLanguagesResponse,
    status_code=status.HTTP_200_OK,
    summary="Get supported languages and language pairs",
    description="Returns dictionary of supported languages and list of supported translation direction pairs.",
)
@router.get(
    "/api/v1/supported-languages",
    response_model=SupportedLanguagesResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def get_languages() -> SupportedLanguagesResponse:
    """
    GET /supported-languages and GET /api/v1/supported-languages

    Returns all active supported language codes, names, and allowed pairs.
    """
    return SupportedLanguagesResponse(
        status="success",
        supported_languages=get_supported_languages(),
        supported_pairs=get_supported_pairs(),
    )
