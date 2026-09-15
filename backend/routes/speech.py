"""
BhashaSetu - Speech Routes
Handles HTTP endpoints for Speech Recognition (ASR) and Text-to-Speech (TTS).
Logic and AI model bindings will be implemented in subsequent steps.
"""

from fastapi import APIRouter, status
from schemas.speech import (
    SpeechToTextRequest,
    SpeechToTextResponse,
    TextToSpeechRequest,
    TextToSpeechResponse,
)

router = APIRouter(tags=["Speech"])


@router.post(
    "/speech-to-text",
    response_model=SpeechToTextResponse,
    status_code=status.HTTP_200_OK,
    summary="Convert spoken audio to text (ASR)",
    description="Transcribes audio input in supported Indic languages. Placeholder endpoint for Step 1 foundation.",
)
async def speech_to_text(request: SpeechToTextRequest) -> SpeechToTextResponse:
    """
    Convert speech audio to text transcription.
    Returns a standardized placeholder response during Step 1 foundation.
    """
    return SpeechToTextResponse(
        status="success",
        message="Module will be implemented in the next step",
        text=None,
    )


@router.post(
    "/text-to-speech",
    response_model=TextToSpeechResponse,
    status_code=status.HTTP_200_OK,
    summary="Synthesize text to speech audio (TTS)",
    description="Synthesizes input text into speech audio in supported Indic languages. Placeholder endpoint for Step 1 foundation.",
)
async def text_to_speech(request: TextToSpeechRequest) -> TextToSpeechResponse:
    """
    Synthesize text into speech audio.
    Returns a standardized placeholder response during Step 1 foundation.
    """
    return TextToSpeechResponse(
        status="success",
        message="Module will be implemented in the next step",
        audio_url=None,
    )
