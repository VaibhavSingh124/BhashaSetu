# BhashaSetu API Documentation (Step 1 Foundation)

This document provides technical specifications for all available endpoints in the BhashaSetu FastAPI backend foundation.

Interactive OpenAPI documentation is also served automatically:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Overview Table

| Method | Endpoint | Purpose | Request Body | Response Model |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Backend health check | None | `HealthCheckResponse` |
| `POST` | `/translate` | Indic text translation | `TranslationRequest` | `TranslationResponse` |
| `POST` | `/speech-to-text` | Speech recognition (ASR) | `SpeechToTextRequest` | `SpeechToTextResponse` |
| `POST` | `/text-to-speech` | Speech synthesis (TTS) | `TextToSpeechRequest` | `TextToSpeechResponse` |
| `POST` | `/evaluate` | Pronunciation assessment | `EvaluationRequest` | `EvaluationResponse` |
| `POST` | `/lesson` | Lesson material upload | `LessonUploadRequest` | `LessonUploadResponse` |

---

## Endpoint Details

### 1. Root Health Check

- **Endpoint**: `/`
- **HTTP Method**: `GET`
- **Purpose**: Verifies that the BhashaSetu backend service is alive, online, and responding to HTTP requests.
- **Headers**: None required.
- **Request Body**: None

#### Expected Response:
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`
```json
{
  "status": "success",
  "message": "BhashaSetu Backend is Running"
}
```

---

### 2. Text Translation

- **Endpoint**: `/translate`
- **HTTP Method**: `POST`
- **Purpose**: Translates text across Indic languages and English. Returns a standardized placeholder in Step 1.
- **Headers**: `Content-Type: application/json`

#### Request Body (`TranslationRequest`):
| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `string` | Yes | Input text to be translated | `"Hello"` |
| `source_language` | `string` | Yes | ISO/BCP-47 source language code | `"en"` |
| `target_language` | `string` | Yes | ISO/BCP-47 target language code | `"pa"` |

```json
{
  "text": "Hello",
  "source_language": "en",
  "target_language": "pa"
}
```

#### Expected Response (`TranslationResponse`):
- **Status Code**: `200 OK`
- **Content-Type**: `application/json`
```json
{
  "status": "success",
  "message": "Module will be implemented in the next step",
  "translation": null
}
```

---

### 3. Speech-to-Text (ASR)

- **Endpoint**: `/speech-to-text`
- **HTTP Method**: `POST`
- **Purpose**: Accepts audio data and converts spoken Indic speech into text. Returns a standardized placeholder in Step 1.
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
- **Purpose**: Synthesizes natural spoken Indic audio from input text. Returns a standardized placeholder in Step 1.
- **Headers**: `Content-Type: application/json`

#### Request Body (`TextToSpeechRequest`):
| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `text` | `string` | Yes | Text string to synthesize into speech | `"ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ"` |
| `language` | `string` | No (default: `"pa"`) | Target Indic language code | `"pa"` |
| `voice_gender` | `string` | No (default: `"female"`) | Preferred voice acoustic profile (`"female"` or `"male"`) | `"female"` |

```json
{
  "text": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ",
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
- **Purpose**: Evaluates spoken user audio against a target reference sentence to score pronunciation, phoneme accuracy, and fluency. Returns a standardized placeholder in Step 1.
- **Headers**: `Content-Type: application/json`

#### Request Body (`EvaluationRequest`):
| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `audio_base64` | `string` | Yes | Base64-encoded user spoken audio | `"UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="` |
| `reference_text` | `string` | Yes | The reference sentence the user was prompted to speak | `"ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ"` |
| `language` | `string` | No (default: `"pa"`) | Language code of the target sentence | `"pa"` |

```json
{
  "audio_base64": "UklGRi4AAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
  "reference_text": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ",
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
- **Purpose**: Uploads and registers new educational lesson units and language learning modules. Returns a standardized placeholder in Step 1.
- **Headers**: `Content-Type: application/json`

#### Request Body (`LessonUploadRequest`):
| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `title` | `string` | Yes | Title of the lesson unit | `"Basic Punjabi Greetings"` |
| `language` | `string` | No (default: `"pa"`) | Language code of the lesson | `"pa"` |
| `level` | `string` | No (default: `"beginner"`) | Learner proficiency level (`"beginner"`, `"intermediate"`, `"advanced"`) | `"beginner"` |
| `content` | `string` | Yes | Curriculum content, script, or markdown | `"Lesson on greetings and everyday phrases"` |

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

Validation errors (such as missing required fields or type mismatches) return standard HTTP `422 Unprocessable Entity` with field-level details generated by Pydantic:

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
