"""
BhashaSetu - API Integration Tests (Step 1 Foundation)
Tests all foundation endpoints (GET /, POST /translate, POST /speech-to-text,
POST /text-to-speech, POST /evaluate, POST /lesson) verifying reachability and
standardized placeholder response structures.
"""

import os
import sys
from fastapi.testclient import TestClient

# Add backend directory to sys.path so modules can be imported
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from main import app  # noqa: E402

client = TestClient(app)


def test_root_health_check():
    """Verify GET / returns health status and running confirmation message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "BhashaSetu Backend is Running"


def test_translate_endpoint():
    """Verify POST /translate works with mocked model (Step 2 — real service connected)."""
    from unittest.mock import patch

    def mock_run_model(self, text, source, target):
        return "ਪਾਣੀ ਜੀਵਨ ਲਈ ਮਹੱਤਵਪੂਰਨ ਹੈ।"

    with patch("services.translator.TranslationService._run_model", new=mock_run_model):
        payload = {
            "text": "Hello",
            "source_language": "en",
            "target_language": "pa",
        }
        response = client.post("/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["source_language"] == "en"
    assert data["target_language"] == "pa"
    assert data["translation"] is not None


def test_translate_invalid_payload():
    """Verify POST /translate rejects incomplete request with 422."""
    response = client.post("/translate", json={})
    assert response.status_code == 422


def test_speech_to_text_endpoint():
    """Verify POST /speech-to-text accepts valid schema and returns placeholder."""
    payload = {
        "audio_base64": "UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
        "language": "pa",
    }
    response = client.post("/speech-to-text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Module will be implemented in the next step"
    assert data["text"] is None


def test_text_to_speech_endpoint():
    """Verify POST /text-to-speech accepts valid schema and returns placeholder."""
    payload = {
        "text": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ",
        "language": "pa",
        "voice_gender": "female",
    }
    response = client.post("/text-to-speech", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Module will be implemented in the next step"
    assert data["audio_url"] is None


def test_evaluate_endpoint():
    """Verify POST /evaluate accepts valid schema and returns placeholder."""
    payload = {
        "audio_base64": "UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
        "reference_text": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ",
        "language": "pa",
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Module will be implemented in the next step"
    assert data["score"] is None
    assert data["feedback"] is None


def test_lesson_endpoint():
    """Verify POST /lesson accepts valid schema and returns placeholder."""
    payload = {
        "title": "Basic Punjabi Greetings",
        "language": "pa",
        "level": "beginner",
        "content": "Lesson content on greetings and everyday phrases",
    }
    response = client.post("/lesson", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Module will be implemented in the next step"
    assert data["lesson_id"] is None
