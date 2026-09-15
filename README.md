# BhashaSetu (भाषासेतु)

**Bridging Languages, Connecting Communities**  
A modular, scalable platform for Indic language learning, speech-to-text, text-to-speech, translation, and interactive pronunciation assessment.

---

## 📌 Project Overview

**BhashaSetu** is designed to deliver accessible language education and real-time cross-lingual assistance. The architecture is engineered to support both connected cloud workflows and offline/edge edge-device deployments across diverse Indian linguistic contexts.

> **Status Notice (Step 0)**: This repository has been initialized with a clean, modular structure for collaborative team development. AI models, speech recognition, translation pipelines, database models, and offline syncing logic will be incrementally implemented in subsequent phases.

---

## 🗂️ Project Structure

```
BhashaSetu/
│
├── backend/                    # Core Python API server
│   ├── main.py                 # FastAPI application entry point & router registration
│   ├── requirements.txt        # Backend dependencies
│   ├── routes/                 # API route definitions
│   │   ├── translation.py      # Translation endpoints
│   │   ├── speech.py           # Speech recognition (ASR) & TTS endpoints
│   │   ├── assessment.py       # Pronunciation & knowledge evaluation endpoints
│   │   └── lessons.py          # Lesson delivery & curriculum endpoints
│   │
│   ├── services/               # Modular service layer (business & AI logic)
│   │   ├── translator.py       # Translation service wrapper
│   │   ├── asr.py              # Automatic Speech Recognition (ASR) service
│   │   ├── tts.py              # Text-to-Speech (TTS) synthesis service
│   │   └── evaluator.py        # Pronunciation & assessment scoring engine
│   │
│   ├── database/               # Data persistence layer
│   │   └── database.py         # DB connection, session management, and base schema
│   │
│   └── utils/                  # Reusable utility functions, helpers, and formatters
│
├── frontend/                   # Client application (Flutter / Mobile / Web)
│
├── models/                     # ML model storage directory (weights ignored in Git)
│   ├── translation/            # Indic translation model checkpoints
│   ├── speech/                 # ASR acoustic and language models
│   └── tts/                    # Speech synthesis vocoder and acoustic models
│
├── data/                       # Datasets, curriculum, and questions
│   ├── lessons/                # Structured lesson plans and multimedia references
│   └── questions/              # Assessment quizzes and evaluation benchmarks
│
├── tests/                      # Automated unit, integration, and performance tests
│
├── docs/                       # Technical architecture documentation and API specs
│
├── .gitignore                  # Git ignore specifications
├── README.md                   # Project overview and developer onboarding
└── .env.example                # Sample environment variables template
```

---

## 🚀 Getting Started for Developers

### 1. Prerequisites
- **Python**: 3.10 or higher
- **Git**: 2.30+
- **Flutter SDK** (for frontend development)

### 2. Setting Up the Backend
Clone the repository and navigate to the `backend/` directory:

```bash
cd backend
```

Create and activate a Python virtual environment:

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the sample environment file from the root directory:

```bash
# From repository root:
cp .env.example .env
```
Edit `.env` to configure your local database URL and service keys.

### 4. Running the Development Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Once running, visit:
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 🔒 Security & Contribution Rules

1. **No Secrets in Git**: Never commit `.env`, credentials, tokens, or API keys. Verify git staging before committing.
2. **No Large Binaries or Models**: Model checkpoints (`.pt`, `.bin`, `.safetensors`, `.onnx`) and heavy datasets must not be checked into Git. Use cloud bucket sync or scripts to fetch them.
3. **Module Isolation**:
   - `routes/` must strictly handle HTTP request validation and serialization.
   - `services/` encapsulates business logic, model inference, and external APIs.
   - `database/` manages database queries, migrations, and ORM abstractions.
4. **Testing**: Add unit tests in `tests/` for all new endpoints and services. Run `pytest` before raising pull requests.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
