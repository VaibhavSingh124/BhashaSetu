"""
BhashaSetu - Translation Module Tests (Step 2 — updated)

Test categories:
  Unit tests (class names without 'Integration') — mock the model layer;
    run anywhere without GPU/internet access.
  Integration tests (TestTranslateIntegration) — call the real model;
    require transformers + model weights (~300 MB download).

Running unit tests only (default CI behaviour):
  pytest -v -m "not integration"

Running integration tests:
  pytest -v -m integration

IMPORTANT:
  Unit tests mock ONLY TranslationService._run_model().
  Preprocessing, language validation, and pipeline logic are exercised
  without mocking so real bugs surface.
"""

import os
import sys
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

# ── Path setup ───────────────────────────────────────────────────────────────
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app  # noqa: E402

client = TestClient(app)

# Placeholder the mocked model always returns (real Punjabi text)
MOCK_TRANSLATION = "ਪਾਣੀ ਜੀਵਨ ਲਈ ਮਹੱਤਵਪੂਰਨ ਹੈ।"


# ---------------------------------------------------------------------------
# Helper — mock the model inference layer only
# ---------------------------------------------------------------------------
def mock_run_model(self, text: str, source: str, target: str) -> str:
    """Replaces TranslationService._run_model during unit tests."""
    return MOCK_TRANSLATION


# ===========================================================================
# UNIT TESTS — mock model, real pipeline logic
# ===========================================================================

class TestTranslateEndpointUnit:
    """Unit tests for POST /translate — model layer is mocked."""

    def _post(self, payload: dict):
        with patch(
            "services.translator.TranslationService._run_model",
            new=mock_run_model,
        ):
            return client.post("/translate", json=payload)

    def test_valid_en_to_pa(self):
        """UNIT — valid English → Punjabi request returns success."""
        resp = self._post({
            "text": "Water is important for life.",
            "source_language": "en",
            "target_language": "pa",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "success"
        assert data["source_language"] == "en"
        assert data["target_language"] == "pa"
        assert data["original_text"] == "Water is important for life."
        assert data["translation"] == MOCK_TRANSLATION
        assert data["engine"] is not None

    def test_valid_en_to_hi(self):
        """UNIT — valid English → Hindi request returns success."""
        resp = self._post({
            "text": "Hello world.",
            "source_language": "en",
            "target_language": "hi",
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

    def test_valid_en_to_ta(self):
        """UNIT — valid English → Tamil request returns success."""
        resp = self._post({
            "text": "Education is the key to success.",
            "source_language": "en",
            "target_language": "ta",
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"

    def test_empty_text_returns_400(self):
        """UNIT — empty text must return HTTP 400."""
        resp = self._post({
            "text": "   ",
            "source_language": "en",
            "target_language": "pa",
        })
        assert resp.status_code == 400
        assert "empty" in resp.json()["detail"].lower()

    def test_invalid_source_language_returns_400(self):
        """UNIT — unsupported source language code returns 400."""
        resp = self._post({
            "text": "Hello world",
            "source_language": "xx",
            "target_language": "pa",
        })
        assert resp.status_code == 400

    def test_invalid_target_language_returns_400(self):
        """UNIT — unsupported target language code returns 400."""
        resp = self._post({
            "text": "Hello world",
            "source_language": "en",
            "target_language": "zz",
        })
        assert resp.status_code == 400

    def test_unsupported_language_pair_returns_400(self):
        """UNIT — supported individual codes but unsupported pair returns 400.
        pa → en is not configured (reverse direction not available yet).
        """
        resp = self._post({
            "text": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ",
            "source_language": "pa",
            "target_language": "en",
        })
        assert resp.status_code == 400

    def test_long_text_accepted(self):
        """UNIT — text with ~500 characters is accepted and translated."""
        long_text = "The water cycle is important. " * 17  # ~510 chars
        resp = self._post({
            "text": long_text.strip(),
            "source_language": "en",
            "target_language": "pa",
        })
        assert resp.status_code == 200
        assert resp.json()["translation"] == MOCK_TRANSLATION

    def test_special_characters_accepted(self):
        """UNIT — text with punctuation and special characters is handled."""
        resp = self._post({
            "text": "Hello, world! How are you? (Fine, thanks.)",
            "source_language": "en",
            "target_language": "pa",
        })
        assert resp.status_code == 200

    def test_missing_text_field_returns_422(self):
        """UNIT — missing required 'text' field returns 422 validation error."""
        resp = client.post("/translate", json={
            "source_language": "en",
            "target_language": "pa",
        })
        assert resp.status_code == 422

    def test_model_error_returns_503(self):
        """UNIT — model-layer exception is converted to HTTP 503."""
        from services.translator import TranslationError

        def fail_model(self, text, source, target):
            raise TranslationError("Simulated model failure")

        with patch(
            "services.translator.TranslationService._run_model",
            new=fail_model,
        ):
            resp = client.post("/translate", json={
                "text": "Water is life.",
                "source_language": "en",
                "target_language": "pa",
            })
        assert resp.status_code == 503
        assert "unavailable" in resp.json()["detail"].lower()

    def test_whitespace_preprocessing(self):
        """UNIT — extra whitespace in input is normalised before translation."""
        resp = self._post({
            "text": "  Water   is   important  for  life.  ",
            "source_language": "en",
            "target_language": "pa",
        })
        assert resp.status_code == 200
        # original_text in response must be normalised
        assert "  " not in resp.json()["original_text"]


# ===========================================================================
# UNIT TESTS — Preprocessor (no HTTP layer)
# ===========================================================================

class TestPreprocessor:
    """Unit tests for the text preprocessor utility."""

    def setup_method(self):
        from utils.preprocessor import preprocess_text, is_text_empty
        self.preprocess = preprocess_text
        self.is_empty = is_text_empty

    def test_strips_outer_whitespace(self):
        assert self.preprocess("  hello  ") == "hello"

    def test_collapses_internal_spaces(self):
        assert self.preprocess("water   is   life") == "water is life"

    def test_empty_string(self):
        assert self.is_empty("") is True
        assert self.is_empty("   ") is True

    def test_non_empty_string(self):
        assert self.is_empty("hello") is False

    def test_removes_zero_width_chars(self):
        text = "water\u200blife"
        result = self.preprocess(text)
        assert "\u200b" not in result

    def test_normalises_crlf(self):
        result = self.preprocess("line1\r\nline2")
        assert "\r" not in result


# ===========================================================================
# UNIT TESTS — Language config
# ===========================================================================

class TestLanguageConfig:
    """Unit tests for the language configuration module."""

    def setup_method(self):
        from config.languages import (
            is_language_supported,
            is_pair_supported,
            get_language_name,
            get_marian_target_tag,
        )
        self.is_supported = is_language_supported
        self.is_pair = is_pair_supported
        self.get_name = get_language_name
        self.get_tag = get_marian_target_tag

    def test_english_supported(self):
        assert self.is_supported("en") is True

    def test_punjabi_supported(self):
        assert self.is_supported("pa") is True

    def test_hindi_supported(self):
        assert self.is_supported("hi") is True

    def test_tamil_supported(self):
        assert self.is_supported("ta") is True

    def test_unknown_language_not_supported(self):
        assert self.is_supported("xx") is False
        assert self.is_supported("zz") is False

    def test_en_pa_pair_supported(self):
        assert self.is_pair("en", "pa") is True

    def test_en_hi_pair_supported(self):
        assert self.is_pair("en", "hi") is True

    def test_reverse_pair_not_supported(self):
        assert self.is_pair("pa", "en") is False

    def test_get_language_name(self):
        assert self.get_name("en") == "English"
        assert self.get_name("pa") == "Punjabi"
        assert self.get_name("hi") == "Hindi"
        assert self.get_name("xx") == "Unknown"

    def test_marian_tag_punjabi(self):
        assert self.get_tag("pa") == ">>pan_Guru<<"

    def test_marian_tag_hindi(self):
        assert self.get_tag("hi") == ">>hin<<"

    def test_marian_tag_unknown_returns_none(self):
        assert self.get_tag("xx") is None


# ===========================================================================
# UNIT TESTS — Simplifier (no model)
# ===========================================================================

class TestSimplifier:
    """Unit tests for the SimplifierService (rule-based mode)."""

    def setup_method(self):
        from services.simplifier import SimplifierService
        self.svc = SimplifierService()

    def test_model_not_active_by_default(self):
        assert self.svc.model_active is False

    def test_passthrough_on_clean_text(self):
        result = self.svc.simplify("ਪਾਣੀ ਜੀਵਨ ਲਈ ਮਹੱਤਵਪੂਰਨ ਹੈ।")
        assert result == "ਪਾਣੀ ਜੀਵਨ ਲਈ ਮਹੱਤਵਪੂਰਨ ਹੈ।"

    def test_collapses_whitespace(self):
        result = self.svc.simplify("ਪਾਣੀ   ਜੀਵਨ   ਲਈ")
        assert "  " not in result

    def test_empty_text(self):
        assert self.svc.simplify("") == ""
        assert self.svc.simplify("  ") == "  "

    def test_status_dict(self):
        status = self.svc.status()
        assert status["model_active"] is False
        assert status["mode"] == "rule_based"


# ===========================================================================
# INTEGRATION TESTS — require real model (~300 MB download on first run)
# ===========================================================================

@pytest.mark.integration
class TestTranslateIntegration:
    """
    Integration tests — call the real Helsinki-NLP/opus-mt-en-mul model.
    Skipped unless run with:  pytest -v -m integration

    Requires:
      - transformers, sentencepiece, torch installed (all in requirements.txt)
      - Internet access to download Helsinki-NLP/opus-mt-en-mul (~300 MB)
        OR the model already cached in ~/.cache/huggingface/
    """

    def test_real_en_to_pa_translation(self):
        """Integration — real model translates English → Punjabi (Gurmukhi)."""
        resp = client.post("/translate", json={
            "text": "Water is important for life.",
            "source_language": "en",
            "target_language": "pa",
        })
        assert resp.status_code == 200, f"Got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert data["status"] == "success"
        assert data["translation"] is not None
        assert len(data["translation"]) > 0
        # Result must contain Gurmukhi Unicode characters (U+0A00–U+0A7F)
        assert any("\u0a00" <= ch <= "\u0a7f" for ch in data["translation"]), (
            f"Expected Gurmukhi script, got: {data['translation']}"
        )

    def test_real_en_to_hi_translation(self):
        """Integration — real model translates English → Hindi (Devanagari)."""
        resp = client.post("/translate", json={
            "text": "Education is important.",
            "source_language": "en",
            "target_language": "hi",
        })
        assert resp.status_code == 200, f"Got {resp.status_code}: {resp.text}"
        data = resp.json()
        assert data["translation"] is not None
        # Result should contain Devanagari characters (U+0900–U+097F)
        assert any("\u0900" <= ch <= "\u097f" for ch in data["translation"]), (
            f"Expected Devanagari script, got: {data['translation']}"
        )
