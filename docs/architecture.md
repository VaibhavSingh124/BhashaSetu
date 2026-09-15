# BhashaSetu Architecture & Roadmap

This document outlines the high-level system architecture and roadmaps across upcoming development phases.

## 1. System Components
- **API Gateway / Backend Layer**: FastAPI asynchronous microservice providing RESTful contracts.
- **AI Service Layer**:
  - `Translator`: Cross-lingual Indic machine translation (e.g. IndicTrans2 / Bhashini / NLLB).
  - `ASR`: Acoustic modeling and speech-to-text decoding (e.g. Whisper / IndicWav2Vec).
  - `TTS`: Multi-speaker neural speech synthesis (e.g. Indic-TTS / VITS).
  - `Evaluator`: Pronunciation score, phoneme alignment, and speech fluency engine.
- **Client Layer**: Flutter mobile app supporting cross-platform (Android, iOS, Web) and local storage for offline lessons.

## 2. Phased Roadmap
- **Step 0**: Repository scaffolding, Git policies, environment templates, modular directory structure.
- **Step 1**: Core database models, migrations, and basic CRUD for lessons and user profiles.
- **Step 2**: Translation engine integration and evaluation pipelines.
- **Step 3**: Speech recognition (ASR) & Text-to-Speech (TTS) integration.
- **Step 4**: Pronunciation assessment and interactive feedback engine.
- **Step 5**: Offline synchronization & mobile client delivery.
