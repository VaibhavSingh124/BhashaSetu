"""
BhashaSetu - Speech Routes
Handles HTTP endpoints for Speech Recognition (ASR) and Text-to-Speech (TTS).
Logic and AI model bindings will be implemented in subsequent steps.
"""

from fastapi import APIRouter, status

router = APIRouter(prefix="/speech", tags=["Speech"])


@router.get("/", status_code=status.HTTP_200_OK)
async def speech_status():
    """
    Health / status check endpoint for speech service.
    """
    return {
        "service": "speech",
        "status": "initialized",
        "version": "v1"
    }


@router.post("/asr", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def speech_to_text():
    """
    Convert speech audio to text for supported Indic languages.
    Implementation deferred to Step 1+.
    """
    return {
        "message": "ASR endpoint placeholder. Logic will be implemented in subsequent steps."
    }


@router.post("/tts", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def text_to_speech():
    """
    Synthesize text into speech audio for supported Indic languages.
    Implementation deferred to Step 1+.
    """
    return {
        "message": "TTS endpoint placeholder. Logic will be implemented in subsequent steps."
    }
