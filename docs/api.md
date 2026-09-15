# BhashaSetu API Documentation (Step 2 — Translation & NLP Module)

This document provides technical specifications for all available endpoints in the BhashaSetu FastAPI backend.

Interactive OpenAPI documentation is also served automatically:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Overview Table

| Method | Endpoint | Purpose | Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Backend health check | ✅ Live |
| `POST` | `/api/v1/translate` (or `/translate`) | Indic text translation (En → 10 languages) | ✅ Live (opus-mt-en-mul) |
| `GET` | `/api/v1/supported-languages` (or `/supported-languages`) | List supported languages and pairs | ✅ Live |
| `POST` | `/speech-to-text` | Speech recognition (ASR) | 🔜 Step 3 |
| `POST` | `/text-to-speech` | Speech synthesis (TTS) | 🔜 Step 3 |
| `POST` | `/evaluate` | Pronunciation assessment | 🔜 Step 4 |
| `POST` | `/lesson` | Lesson material upload | 🔜 Step 5 |


---

## Endpoint Details

### 1. Root Health Check

- **Endpoint**: `/`
- **HTTP Method**: `GET`
- **Purpose**: Verifies that the BhashaSetu backend service is alive and responding.
- **Request Body**: None

#### Response — `200 OK`
```json
{
  "status": "success",
  "message": "BhashaSetu Backend is Running"
}
```

---

### 2. Text Translation ✅ LIVE

- **Endpoint**: `/translate`
- **HTTP Method**: `POST`
- **Purpose**: Translates input text from English to one of 10 major Indic languages using a neural machine translation model.
- **Active Model**: `Helsinki-NLP/opus-mt-en-mul` (MarianMT multilingual, ~300 MB, CPU-capable)
- **Planned Model**: `ai4bharat/IndicTrans2` (higher quality; requires CUDA GPU — upgrade path ready)
- **Headers**: `Content-Type: application/json`

#### Supported Languages

| Code | Language | Script | Role | Model Tag |
| :--- | :--- | :--- | :--- | :--- |
| `en` | English | Latin | Source only | — |
| `pa` | Punjabi | Gurmukhi | Target | `>>pan_Guru<<` |
| `hi` | Hindi | Devanagari | Target | `>>hin<<` |
| `bn` | Bengali | Bengali | Target | `>>ben<<` |
| `mr` | Marathi | Devanagari | Target | `>>mar<<` |
| `ta` | Tamil | Tamil | Target | `>>tam<<` |
| `te` | Telugu | Telugu | Target | `>>tel<<` |
| `gu` | Gujarati | Gujarati | Target | `>>guj<<` |
| `kn` | Kannada | Kannada | Target | `>>kan<<` |
| `ml` | Malayalam | Malayalam | Target | `>>mal<<` |
| `ur` | Urdu | Perso-Arabic | Target | `>>urd<<` |

> **Note**: Reverse direction (e.g. `pa → en`) is not yet supported. A separate model or the reverse opus-mt pair would be required.

#### Request Body (`TranslationRequest`)

| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `string` | ✅ Yes | Input text (min 1 char) | `"Water is important for life."` |
| `source_language` | `string` | ✅ Yes | ISO source language code | `"en"` |
| `target_language` | `string` | ✅ Yes | ISO target language code | `"pa"` |

```json
{
  "text": "Water is important for life.",
  "source_language": "en",
  "target_language": "pa"
}
```

#### Response — `200 OK` (`TranslationResponse`)

| Field | Type | Description |
| :--- | :--- | :--- |
| `status` | `string` | `"success"` |
| `source_language` | `string` | Source language code (e.g. `"en"`) |
| `target_language` | `string` | Target language code (e.g. `"pa"`) |
| `original_text` | `string` | Preprocessed input text |
| `translated_text` | `string` | Translated output text |
| `simplified_text` | `string` | Simplified text output (beginner readability) |
| `translation` | `string` | Alias for `translated_text` (backward compatibility) |
| `engine` | `string` | Model used for inference |
| `message` | `string\|null` | Additional note, if any |

```json
{
  "status": "success",
  "source_language": "en",
  "target_language": "pa",
  "original_text": "Water is important for life.",
  "translated_text": "ਜੀਵਨ ਲਈ ਪਾਣੀ ਜ਼ਰੂਰੀ ਹੈ ।",
  "simplified_text": "ਜੀਵਨ ਲਈ ਪਾਣੀ ਜ਼ਰੂਰੀ ਹੈ ।",
  "translation": "ਜੀਵਨ ਲਈ ਪਾਣੀ ਜ਼ਰੂਰੀ ਹੈ ।",
  "engine": "Helsinki-NLP/opus-mt-en-mul (MarianMT) — CPU inference",
  "message": null
}
```

#### Error Responses

| HTTP Status | Condition | Example detail |
| :--- | :--- | :--- |
| `400 Bad Request` | Empty or whitespace-only text | `"Input text is empty or contains only whitespace."` |
| `400 Bad Request` | Unsupported source language | `"Source language 'xx' is not supported."` |
| `400 Bad Request` | Unsupported target language | `"Target language 'zz' is not supported."` |
| `400 Bad Request` | Unsupported language pair | `"Translation from 'pa' to 'en' is not supported."` |
| `422 Unprocessable Entity` | Missing required field | Pydantic validation detail |
| `503 Service Unavailable` | Model load / inference failure | `"Translation service unavailable: Failed to load model..."` |

#### curl Examples

**English → Punjabi (`POST /api/v1/translate` or `POST /translate`)**
```bash
curl -X POST http://localhost:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Water is important for life.", "source_language": "en", "target_language": "pa"}'
```

**English → Hindi**
```bash
curl -X POST http://localhost:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Education is the key to success.", "source_language": "en", "target_language": "hi"}'
```

**English → Tamil**
```bash
curl -X POST http://localhost:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "The sun rises in the east.", "source_language": "en", "target_language": "ta"}'
```

---

### 3. Supported Languages ✅ LIVE

- **Endpoint**: `/supported-languages` (alias `/api/v1/supported-languages`)
- **HTTP Method**: `GET`
- **Purpose**: Returns the list of currently supported language codes, human-readable names, and supported translation direction pairs.
- **Request Body**: None

#### Response — `200 OK` (`SupportedLanguagesResponse`)
```json
{
  "status": "success",
  "supported_languages": {
    "en": "English",
    "pa": "Punjabi",
    "hi": "Hindi",
    "bn": "Bengali",
    "mr": "Marathi",
    "ta": "Tamil",
    "te": "Telugu",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "ur": "Urdu"
  },
  "supported_pairs": [
    ["en", "bn"],
    ["en", "gu"],
    ["en", "hi"],
    ["en", "kn"],
    ["en", "ml"],
    ["en", "mr"],
    ["en", "pa"],
    ["en", "ta"],
    ["en", "te"],
    ["en", "ur"]
  ]
}
```

#### curl Example
```bash
curl -X GET http://localhost:8000/api/v1/supported-languages
```


---

### 3. Speech-to-Text (ASR)

- **Endpoint**: `/speech-to-text`
- **HTTP Method**: `POST`
- **Purpose**: Accepts audio data and converts spoken Indic speech into text. Returns a standardized placeholder in Step 2.
- **Headers**: `Content-Type: application/json`

#### Request Body (`SpeechToTextRequest`):
| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `audio_base64` | `string` | Yes | Base64-encoded audio bytes | `"UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="` |
| `language` | `string` | No (default: `"pa"`) | Language code of the spoken audio | `"pa"` |

```json
{
  "audio_base64": "UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
  "language": "pa"
}
```

#### Expected Response (`SpeechToTextResponse`):
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`
```json
{
  "status": "success",
  "message": "Module will be implemented in the next step",
  "text": null
}
```

---

### 4. Text-to-Speech (TTS)

- **Endpoint**: `/text-to-speech`
- **HTTP Method**: `POST`
- **Purpose**: Synthesizes natural spoken Indic audio from input text. Returns a standardized placeholder in Step 2.
- **Headers**: `Content-Type: application/json`

#### Request Body (`TextToSpeechRequest`):
| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `string` | Yes | Text string to synthesize into speech | `"ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ"` |
| `language` | `string` | No (default: `"pa"`) | Target Indic language code | `"pa"` |
| `voice_gender` | `string` | No (default: `"female"`) | Preferred voice (`"female"` or `"male"`) | `"female"` |

```json
{
  "text": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ",
  "language": "pa",
  "voice_gender": "female"
}
```

#### Expected Response (`TextToSpeechResponse`):
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`
```json
{
  "status": "success",
  "message": "Module will be implemented in the next step",
  "audio_url": null
}
```

---

### 5. Pronunciation Assessment & Evaluation

- **Endpoint**: `/evaluate`
- **HTTP Method**: `POST`
- **Purpose**: Evaluates spoken user audio against a target reference sentence to score pronunciation and fluency. Returns a standardized placeholder in Step 2.
- **Headers**: `Content-Type: application/json`

#### Request Body (`EvaluationRequest`):
| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `audio_base64` | `string` | Yes | Base64-encoded user spoken audio | `"UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="` |
| `reference_text` | `string` | Yes | The reference sentence the user was prompted to speak | `"ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ"` |
| `language` | `string` | No (default: `"pa"`) | Language code of the target sentence | `"pa"` |

```json
{
  "audio_base64": "UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
  "reference_text": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ",
  "language": "pa"
}
```

#### Expected Response (`EvaluationResponse`):
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`
```json
{
  "status": "success",
  "message": "Module will be implemented in the next step",
  "score": null,
  "feedback": null
}
```

---

### 6. Lesson Creation & Upload

- **Endpoint**: `/lesson`
- **HTTP Method**: `POST`
- **Purpose**: Uploads and registers new educational lesson units and language learning modules. Returns a standardized placeholder in Step 2.
- **Headers**: `Content-Type: application/json`

#### Request Body (`LessonUploadRequest`):
| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `title` | `string` | Yes | Title of the lesson unit | `"Basic Punjabi Greetings"` |
| `language` | `string` | No (default: `"pa"`) | Language code of the lesson | `"pa"` |
| `level` | `string` | No (default: `"beginner"`) | Learner proficiency level | `"beginner"` |
| `content` | `string` | Yes | Curriculum content or markdown | `"Lesson on greetings and everyday phrases"` |

```json
{
  "title": "Basic Punjabi Greetings",
  "language": "pa",
  "level": "beginner",
  "content": "Lesson on greetings and everyday phrases"
}
```

#### Expected Response (`LessonUploadResponse`):
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`
```json
{
  "status": "success",
  "message": "Module will be implemented in the next step",
  "lesson_id": null
}
```

---

## Error Handling

Validation errors (missing required fields or type mismatches) return standard HTTP `422 Unprocessable Entity` with field-level details generated by Pydantic:

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "text"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

---

## Model Limitations & Upgrade Path

| Constraint | Detail |
| :--- | :--- |
| GPU | Intel Iris Xe — **no CUDA** |
| Active model | `Helsinki-NLP/opus-mt-en-mul` (~300 MB, CPU) |
| Planned model | `ai4bharat/IndicTrans2` (~2–4 GB, requires CUDA GPU) |
| Translation quality | Good for primary-school sentences; may struggle with complex idioms |
| CPU inference speed | ~1–5 seconds per sentence on this hardware |
| Source language | English only (en → X) |
| Reverse direction | Not yet supported (would require a separate model) |

**To upgrade to IndicTrans2**: update `TRANSLATION_MODEL_MAP` and `MARIAN_TARGET_TAG` in `config/languages.py` and change the tokenizer/model class in `services/translator.py:_load_model()`. No other files need to change.
