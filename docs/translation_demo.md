# Translation Flow — Demo Example (Step 2)

## Input

| Field | Value |
| :--- | :--- |
| **Text** | `"Water is important for life."` |
| **Source language** | English (`en`) |
| **Target language** | Punjabi (`pa`) |

---

## API Request

```http
POST /translate
Content-Type: application/json

{
  "text": "Water is important for life.",
  "source_language": "en",
  "target_language": "pa"
}
```

---

## Internal Pipeline

```
1. INPUT TEXT
   "Water is important for life."
           │
           ▼
2. PREPROCESSING  (utils/preprocessor.py)
   - Strip leading/trailing whitespace
   - Collapse multiple internal spaces into one
   - Remove zero-width Unicode characters (U+200B, U+FEFF …)
   - Normalise CRLF → LF
   → "Water is important for life."   (unchanged — already clean)

           │
           ▼
3. LANGUAGE VALIDATION  (config/languages.py)
   - "en" in SUPPORTED_LANGUAGES  ✓
   - "pa" in SUPPORTED_LANGUAGES  ✓
   - ("en", "pa") in SUPPORTED_PAIRS  ✓
   - Marian target tag for "pa": >>pan_Guru<<

           │
           ▼
4. TRANSLATION MODEL  (services/translator.py → _run_model)
   Active model : Helsinki-NLP/opus-mt-en-mul  (MarianMT multilingual)
   Planned model: ai4bharat/IndicTrans2  (requires CUDA GPU)

   Tagged input sent to tokenizer:
     ">>pan_Guru<< Water is important for life."

   Steps:
   - Tokenise with MarianTokenizer
   - model.generate() inference on CPU (~1–5 s per sentence)
   - Decode tokens → Gurmukhi text (skip_special_tokens=True)
   → "ਜੀਵਨ ਲਈ ਪਾਣੀ ਜ਼ਰੂਰੀ ਹੈ ।"

           │
           ▼
5. SIMPLIFICATION  (services/simplifier.py)
   - Step 2: rule-based cleanup only (no LLM active)
   - SimplifierService._rule_based_cleanup():
     · Collapse consecutive spaces
     · Collapse 3+ newlines into 2
   → "ਜੀਵਨ ਲਈ ਪਾਣੀ ਜ਼ਰੂਰੀ ਹੈ ।"   (unchanged — already clean)

           │
           ▼
6. API RESPONSE
```

---

## API Response

```json
{
  "status": "success",
  "source_language": "en",
  "target_language": "pa",
  "original_text": "Water is important for life.",
  "translation": "ਜੀਵਨ ਲਈ ਪਾਣੀ ਜ਼ਰੂਰੀ ਹੈ ।",
  "engine": "Helsinki-NLP/opus-mt-en-mul (MarianMT) — CPU inference",
  "message": null
}
```

---

## curl Command

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Water is important for life.", "source_language": "en", "target_language": "pa"}'
```

---

## More Examples (verified with real model)

| English Input | Target | Translation |
| :--- | :--- | :--- |
| `Water is important for life.` | Punjabi (`pa`) | `ਜੀਵਨ ਲਈ ਪਾਣੀ ਜ਼ਰੂਰੀ ਹੈ ।` |
| `Water is important for life.` | Hindi (`hi`) | `पानी ज़िंदगी के लिए ज़रूरी है ।` |
| `Water is important for life.` | Tamil (`ta`) | `தண்ணீர் வாழ்க்கையில் முக்கியம்.` |

---

## Error Scenarios

| Scenario | HTTP Status | Example detail |
| :--- | :--- | :--- |
| Empty text | `400` | `"Input text is empty or contains only whitespace."` |
| Unsupported source lang | `400` | `"Source language 'xx' is not supported."` |
| Unsupported target lang | `400` | `"Target language 'zz' is not supported."` |
| Unsupported pair (e.g. pa→en) | `400` | `"Translation from 'pa' to 'en' is not supported."` |
| Model unavailable | `503` | `"Translation service unavailable: Failed to load model..."` |

---

## Environment Limitations

| Constraint | Detail |
| :--- | :--- |
| GPU | Intel Iris Xe — **no CUDA** |
| RAM | ~16 GB total |
| Active model | `Helsinki-NLP/opus-mt-en-mul` (~300 MB, CPU) |
| Planned model | `ai4bharat/IndicTrans2` (~2–4 GB, requires CUDA GPU) |
| CPU inference speed | ~1–5 seconds per sentence on this hardware |
| Old model note | `Helsinki-NLP/opus-mt-en-pun` was removed from HuggingFace Hub; replaced by `opus-mt-en-mul` which covers all 10 Indic languages |

**To upgrade to IndicTrans2**: update `TRANSLATION_MODEL_MAP` in `config/languages.py`
and change the tokenizer/model class in `services/translator.py:_load_model()`.
No other files need to change.
