"""
BhashaSetu - Translation Service (Step 2 — updated)

Implements the full translation pipeline:
  Input text
    → Preprocessing
    → Language validation
    → Model inference  (Helsinki-NLP/opus-mt-en-mul, MarianMT)
    → Simplification pass
    → Final regional-language text

Model: Helsinki-NLP/opus-mt-en-mul
  - Supports English → 150+ languages via >>lang_tag<< prefix tokens.
  - CPU-capable, ~300 MB weights.  No CUDA required.
  - Verified Indic language tags: >>pan_Guru<< >>hin<< >>ben<< >>mar<<
    >>tam<< >>tel<< >>guj<< >>kan<< >>mal<< >>urd<<

Why NOT IndicTrans2 in Step 2?
  IndicTrans2 (ai4bharat/IndicTrans2) delivers higher quality for Indic
  scripts but requires:
    - CTranslate2 + CUDA GPU  OR  ~4 GB RAM at very slow CPU speed.
  The deployment machine has an Intel Iris Xe GPU (no CUDA) and ~16 GB RAM.
  opus-mt-en-mul shares the HuggingFace transformers API — swapping models
  requires only changing TRANSLATION_MODEL_MAP in config/languages.py and
  updating _load_model() below.

Thread safety:
  Models are loaded lazily on the first request per language pair and cached
  in _models / _tokenizers.  Inference is read-only after loading.
"""

from __future__ import annotations

import logging
from typing import Optional

from config.languages import (
    TRANSLATION_MODEL_MAP,
    is_language_supported,
    is_pair_supported,
    get_language_name,
    get_marian_target_tag,
    ACTIVE_ENGINE,
)
from utils.preprocessor import preprocess_text, is_text_empty
from services.simplifier import SimplifierService

logger = logging.getLogger(__name__)


class TranslationError(Exception):
    """Raised for domain-level translation failures."""


class TranslationService:
    """
    End-to-end translation pipeline service.

    Loads a HuggingFace MarianMT (or compatible) model on first use and
    exposes a single ``translate()`` method to callers.

    Model instances are cached by model name so that multiple language pairs
    that share the same underlying model (e.g. all en→X pairs on
    opus-mt-en-mul) load the weights only once.
    """

    def __init__(self) -> None:
        # Keyed by model_name string — multiple pairs can share one model.
        self._models: dict = {}
        self._tokenizers: dict = {}
        self._simplifier = SimplifierService()
        self._transformers_available: Optional[bool] = None
        logger.info("TranslationService initialised.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> dict:
        """
        Translate text from source_language to target_language.

        Parameters
        ----------
        text : str
            Raw user input text.
        source_language : str
            ISO/BCP-47 source language code (e.g. ``"en"``).
        target_language : str
            ISO/BCP-47 target language code (e.g. ``"pa"``).

        Returns
        -------
        dict with keys:
            status          : "success"
            source_language : str
            target_language : str
            original_text   : str  (preprocessed)
            translation     : str
            engine          : str  (model identifier)

        Raises
        ------
        ValueError
            For empty text, unsupported languages, or unsupported pairs.
        TranslationError
            For model-level inference failures.
        """
        # ── Stage 1: Preprocess ─────────────────────────────────────────
        cleaned_text = preprocess_text(text)
        if is_text_empty(cleaned_text):
            raise ValueError("Input text is empty or contains only whitespace.")

        # ── Stage 2: Language validation ─────────────────────────────────
        if not is_language_supported(source_language):
            raise ValueError(
                f"Source language '{source_language}' is not supported. "
                f"Supported source: en (English)."
            )
        if not is_language_supported(target_language):
            supported_targets = [
                f"{code} ({get_language_name(code)})"
                for code in ["pa", "hi", "bn", "mr", "ta", "te", "gu", "kn", "ml", "ur"]
            ]
            raise ValueError(
                f"Target language '{target_language}' is not supported. "
                f"Supported targets: {', '.join(supported_targets)}."
            )
        if not is_pair_supported(source_language, target_language):
            raise ValueError(
                f"Translation from '{source_language}' to '{target_language}' "
                f"is not supported. Supported direction: en → (pa, hi, bn, mr, "
                f"ta, te, gu, kn, ml, ur)."
            )

        # ── Stage 3: Model inference ─────────────────────────────────────
        raw_translation = self._run_model(cleaned_text, source_language, target_language)

        # ── Stage 4: Simplification pass ─────────────────────────────────
        final_translation = self._simplifier.simplify(raw_translation, target_language)

        return {
            "status": "success",
            "source_language": source_language,
            "target_language": target_language,
            "original_text": cleaned_text,
            "translation": final_translation,
            "engine": ACTIVE_ENGINE,
        }

    def status(self) -> dict:
        """Return a structured status dict for diagnostics."""
        return {
            "service": "translation",
            "engine": ACTIVE_ENGINE,
            "transformers_available": self._check_transformers(),
            "loaded_models": list(self._models.keys()),
            "simplifier": self._simplifier.status(),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check_transformers(self) -> bool:
        if self._transformers_available is None:
            try:
                import transformers  # noqa: F401
                self._transformers_available = True
            except ImportError:
                self._transformers_available = False
        return self._transformers_available

    def _load_model(self, model_name: str) -> None:
        """
        Lazy-load the HuggingFace model and tokenizer by model name.
        Called once per unique model name; subsequent calls use the cache.

        opus-mt-en-mul serves all en→X language pairs, so the weights are
        loaded only once regardless of how many target languages are used.

        To upgrade to IndicTrans2:
          1. Update TRANSLATION_MODEL_MAP in config/languages.py.
          2. Replace MarianMTModel / MarianTokenizer below with the
             IndicTrans2 equivalents (huggingface_hub or ai4bharat package).
          3. Adjust the tokenisation call in _run_model() if the API differs.
        """
        if model_name in self._models:
            return  # already loaded — shared across language pairs

        if not self._check_transformers():
            raise TranslationError(
                "The 'transformers' library is not installed. "
                "Run: pip install transformers sentencepiece torch"
            )

        try:
            from transformers import MarianMTModel, MarianTokenizer

            logger.info("Loading tokenizer: %s …", model_name)
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            logger.info("Loading model weights: %s …", model_name)
            model = MarianMTModel.from_pretrained(model_name)
            model.eval()  # inference mode — no gradient tracking needed

            self._tokenizers[model_name] = tokenizer
            self._models[model_name] = model
            logger.info("Model loaded successfully: %s", model_name)

        except Exception as exc:
            raise TranslationError(
                f"Failed to load translation model '{model_name}': {exc}"
            ) from exc

    def _run_model(self, text: str, source: str, target: str) -> str:
        """
        Run model inference for the given language pair.

        For opus-mt-en-mul the target language is specified by prepending a
        language tag token (e.g. ``>>pan_Guru<<``) to the input sentence.
        This tag tells the shared multilingual model which script to output.

        The tag is resolved via config.languages.get_marian_target_tag().
        If no tag is configured for a language (e.g. a future IndicTrans2
        pair) the raw text is passed unchanged.
        """
        pair = (source, target)
        model_name = TRANSLATION_MODEL_MAP.get(pair)
        if not model_name:
            raise TranslationError(
                f"No model mapping found for pair ({source}, {target}). "
                "Update TRANSLATION_MODEL_MAP in config/languages.py."
            )

        self._load_model(model_name)

        # Prepend Marian language-direction tag when one is configured.
        target_tag = get_marian_target_tag(target)
        tagged_text = f"{target_tag} {text}" if target_tag else text

        try:
            import torch

            tokenizer = self._tokenizers[model_name]
            model = self._models[model_name]

            inputs = tokenizer(
                [tagged_text],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            )

            with torch.no_grad():
                translated_tokens = model.generate(**inputs)

            translation: str = tokenizer.batch_decode(
                translated_tokens, skip_special_tokens=True
            )[0]

            logger.debug(
                "Translated (%s→%s) [model=%s]: %r → %r",
                source, target, model_name,
                text[:60], translation[:60],
            )
            return translation

        except Exception as exc:
            logger.error("Model inference error: %s", exc)
            raise TranslationError(f"Model inference failed: {exc}") from exc
