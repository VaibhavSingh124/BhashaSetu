"""
BhashaSetu - Translation Routes (Task 2)
Connects POST /translate to the TranslationService pipeline.
Handles all validation, language, and model errors with proper HTTP responses.
"""

import logging
from fastapi import APIRouter, HTTPException, status

from schemas.translation import TranslationRequest, TranslationResponse
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
        "Currently supports: English (en) → Punjabi (pa)."
    ),
)
async def translate(request: TranslationRequest) -> TranslationResponse:
    """
    POST /translate

    Pipeline:
      1. Preprocess input text (whitespace normalisation).
      2. Validate language codes and pair support.
      3. Run MarianMT (Helsinki-NLP/opus-mt-en-pun) model inference.
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
