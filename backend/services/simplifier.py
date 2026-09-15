"""
BhashaSetu - Text Simplifier Service (Task 5)
Foundation simplification layer for primary-school learners.

Current state (Step 2):
  This module provides a *clean interface* for simplification.
  The active implementation applies only safe, rule-based post-processing
  (whitespace, length checks) that does NOT alter meaning.

  A real simplification model (LLM, IndicBART, or similar) can be plugged
  into SimplifierService.simplify() in a later step without touching callers.

Design principles:
  - Never change facts or invent information.
  - Never silently pretend AI simplification is active when it is not.
  - Keep sentences short where possible without losing meaning.
  - Prefer simple vocabulary (future model responsibility).
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class SimplifierService:
    """
    Service that applies a simplification pass to translated text.

    Step 2 behaviour:
        Rule-based only. Returns the text with trivial cleanups.
        No LLM is invoked. The `model_active` property is False.

    Future upgrade path:
        Override `_run_model()` with a real LLM call (e.g. IndicBART,
        Gemini, or a fine-tuned T5 model). Set `_model_loaded = True`
        after successful model loading.
    """

    def __init__(self) -> None:
        self._model_loaded: bool = False
        logger.info(
            "SimplifierService initialised — rule-based mode "
            "(no simplification model loaded in Step 2)."
        )

    @property
    def model_active(self) -> bool:
        """True only when a real simplification model is loaded and ready."""
        return self._model_loaded

    def simplify(self, text: str, language: str = "pa") -> str:
        """
        Apply simplification to translated text.

        Parameters
        ----------
        text : str
            Translated text (in target language) to simplify.
        language : str
            Target language code — future models may use this.

        Returns
        -------
        str
            Simplified text. In Step 2, this is the input text after
            safe rule-based cleanups only.
        """
        if not text or not text.strip():
            return text

        if self._model_loaded:
            return self._run_model(text, language)

        # Rule-based fallback — safe, meaning-preserving cleanup only
        return self._rule_based_cleanup(text)

    def _rule_based_cleanup(self, text: str) -> str:
        """
        Safe, meaning-preserving post-processing rules.
        Applied even in Step 2 to keep output clean.
        """
        import re

        # Collapse multiple spaces
        cleaned = re.sub(r"[ \t]+", " ", text.strip())
        # Collapse 3+ newlines into 2
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned

    def _run_model(self, text: str, language: str) -> str:
        """
        Placeholder for real simplification model inference.
        Will be implemented in a future step when a simplification
        model (LLM or seq2seq) is integrated.
        """
        raise NotImplementedError(
            "Simplification model is declared as loaded but _run_model() "
            "has not been implemented. This is a programming error."
        )

    def status(self) -> dict:
        """Return a status dict suitable for API health/info endpoints."""
        return {
            "service": "simplifier",
            "model_active": self._model_loaded,
            "mode": "model" if self._model_loaded else "rule_based",
            "note": (
                "Simplification model not loaded. "
                "Rule-based cleanup only (Step 2 foundation)."
            ) if not self._model_loaded else "Simplification model active.",
        }
