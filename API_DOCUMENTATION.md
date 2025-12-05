# LMN API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API does not require authentication. For production deployment, implement JWT or API key authentication.

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response**
```json
{
  "status": "healthy"
}
```

---

## Text-to-Speech (TTS)

### POST /api/tts/synthesize
Convert Khmer text to speech.

**Request Body**
```json
{
  "text": "ជំរាបសួរ ខ្ញុំឈ្មោះ មេងហួត",
  "speed": 1.0
}
```

**Parameters**
- `text` (string, required): Khmer text to synthesize
- `speed` (float, optional): Speech speed multiplier (0.5-2.0, default: 1.0)

**Response**
```json
{
  "audio_base64": "UklGRiQAAABXQVZFZm10...",
  "duration": 3.5,
  "text": "ជំរាបសួរ ខ្ញុំឈ្មោះ មេងហួត"
}
```

**Status Codes**
- 200: Success
- 400: Invalid input
- 503: Model not loaded

### GET /api/tts/status
Get TTS model status.

**Response**
```json
{
  "model_loaded": true,
  "model_name": "facebook/mms-tts-khm",
  "supported_language": "Khmer (khm)"
}
```

---

## Optical Character Recognition (OCR)

### POST /api/ocr/recognize
Recognize Khmer text from an image.

**Request**
- Content-Type: `multipart/form-data`
- Body: Image file (PNG, JPG, JPEG)

**Response**
```json
{
  "text": "កម្ពុជា",
  "confidence": 0.95,
  "detected_lines": ["កម្ពុជា"]
}
```

**Parameters**
- `file` (file, required): Image file containing Khmer text

**Status Codes**
- 200: Success
- 400: Invalid file type
- 503: Model not loaded

### POST /api/ocr/recognize_base64
Recognize text from base64 encoded image.

**Request Body**
```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUg..."
}
```

**Response**
```json
{
  "text": "កម្ពុជា",
  "confidence": 0.95,
  "detected_lines": ["កម្ពុជា"]
}
```

### GET /api/ocr/status
Get OCR model status.

**Response**
```json
{
  "model_loaded": true,
  "model_name": "songhieng/khmer-trocr-ocr-v1.0",
  "supported_language": "Khmer"
}
```

---

## Language Model (LLM)

### POST /api/llm/summarize
Summarize Khmer text.

**Request Body**
```json
{
  "text": "Long Khmer text to summarize...",
  "max_length": 150,
  "min_length": 50
}
```

**Parameters**
- `text` (string, required): Text to summarize
- `max_length` (integer, optional): Maximum summary length (default: 150)
- `min_length` (integer, optional): Minimum summary length (default: 50)

**Response**
```json
{
  "output": "Summary of the text...",
  "input_length": 500,
  "output_length": 120
}
```

**Status Codes**
- 200: Success
- 400: Invalid input
- 503: Model not loaded

### POST /api/llm/generate
Generate text based on a prompt.

**Request Body**
```json
{
  "prompt": "Write a story about...",
  "max_length": 200,
  "temperature": 0.7
}
```

**Parameters**
- `prompt` (string, required): Text prompt
- `max_length` (integer, optional): Maximum generation length (default: 200)
- `temperature` (float, optional): Sampling temperature 0.1-1.0 (default: 0.7)

**Response**
```json
{
  "output": "Generated text...",
  "input_length": 25,
  "output_length": 180
}
```

### GET /api/llm/status
Get LLM model status.

**Response**
```json
{
  "model_loaded": true,
  "models": {
    "summarization": "khmer-mt5-summarization",
    "generation": "PrahokBART"
  },
  "supported_language": "Khmer"
}
```

---

## Video Generation

### POST /api/video/generate
Generate video from text prompt.

**Request Body**
```json
{
  "prompt": "A beautiful sunset over Angkor Wat",
  "duration": 5,
  "resolution": "720p",
  "fps": 30
}
```

**Parameters**
- `prompt` (string, required): Video description
- `duration` (integer, optional): Video duration in seconds (3-10, default: 5)
- `resolution` (string, optional): Output resolution (480p/720p/1080p, default: 720p)
- `fps` (integer, optional): Frames per second (default: 30)

**Response**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Video generation started. Use /status/{job_id} to check progress."
}
```

**Status Codes**
- 200: Job created
- 400: Invalid input
- 503: Model not loaded

### GET /api/video/status/{job_id}
Check video generation status.

**Path Parameters**
- `job_id` (string, required): Job ID from generate endpoint

**Response (Processing)**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45
}
```

**Response (Completed)**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "video_url": "/api/video/download/550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (Failed)**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "error": "Error message"
}
```

**Status Codes**
- 200: Success
- 404: Job not found

### GET /api/video/models
Get available video generation models.

**Response**
```json
{
  "model_loaded": true,
  "available_models": ["Mochi 1", "Wan2.2"],
  "supported_resolutions": ["720p", "1080p"],
  "max_duration": 10
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid input parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error: detailed message"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Model not loaded"
}
```

---

## Rate Limiting

Currently, there is no rate limiting. For production:
- Implement per-IP rate limiting
- Recommended: 100 requests per minute per IP
- Use Redis for distributed rate limiting

---

## Examples

### Python Example

```python
import requests
import base64

# TTS Example
response = requests.post(
    "http://localhost:8000/api/tts/synthesize",
    json={"text": "ជំរាបសួរ", "speed": 1.0}
)
audio_data = base64.b64decode(response.json()["audio_base64"])
with open("output.wav", "wb") as f:
    f.write(audio_data)

# OCR Example
with open("image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/ocr/recognize",
        files={"file": f}
    )
print(response.json()["text"])

# Summarization Example
response = requests.post(
    "http://localhost:8000/api/llm/summarize",
    json={
        "text": "Long text...",
        "max_length": 150
    }
)
print(response.json()["output"])
```

### JavaScript Example

```javascript
// TTS Example
const response = await fetch('http://localhost:8000/api/tts/synthesize', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'ជំរាបសួរ', speed: 1.0})
});
const data = await response.json();
const audioBlob = base64ToBlob(data.audio_base64, 'audio/wav');

// OCR Example
const formData = new FormData();
formData.append('file', imageFile);
const response = await fetch('http://localhost:8000/api/ocr/recognize', {
  method: 'POST',
  body: formData
});
const data = await response.json();
console.log(data.text);
```

### cURL Examples

```bash
# TTS
curl -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text":"ជំរាបសួរ","speed":1.0}'

# OCR
curl -X POST http://localhost:8000/api/ocr/recognize \
  -F "file=@image.jpg"

# Summarization
curl -X POST http://localhost:8000/api/llm/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Long text...","max_length":150}'

# Video Generation
curl -X POST http://localhost:8000/api/video/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A sunset","duration":5}'
```

---

## WebSocket Support (Future)

Planned for real-time streaming:
- TTS streaming
- Video generation progress updates
- Real-time OCR

---

## Versioning

Current API Version: v1.0.0

For future versions, endpoints will be prefixed with version:
- `/api/v2/tts/synthesize`

---

## Support

For API issues:
- GitHub: https://github.com/MenghoutChhon/lmn/issues
- Email: menghoutchhon003@gmail.com
