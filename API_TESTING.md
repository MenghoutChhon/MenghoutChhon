# API Testing Guide - Khmer AI/ML Platform

## Quick Start Testing

### Using cURL

#### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

#### 2. Test TTS (Text-to-Speech)

```bash
curl -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "សួស្តី",
    "language": "khmer"
  }'
```

#### 3. Test OCR

```bash
curl -X POST http://localhost:8000/api/ocr/extract \
  -F "file=@/path/to/image.jpg"
```

#### 4. Test Summarization

```bash
curl -X POST http://localhost:8000/api/llm/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "អត្ថបទវែងៗនៅទីនេះ...",
    "max_length": 150,
    "min_length": 30
  }'
```

#### 5. Test Video Generation

```bash
curl -X POST http://localhost:8000/api/video/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful sunset over Angkor Wat",
    "duration": 5,
    "resolution": "720p"
  }'
```

## Using Python Requests

### Setup

```bash
pip install requests
```

### Test Script

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Health Check
response = requests.get(f"{BASE_URL}/health")
print("Health Check:", response.json())

# 2. TTS Test
tts_data = {
    "text": "សួស្តី កម្ពុជា",
    "language": "khmer"
}
response = requests.post(f"{BASE_URL}/api/tts/synthesize", json=tts_data)
print("TTS Response:", response.json())

# 3. OCR Test
with open('test_image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(f"{BASE_URL}/api/ocr/extract", files=files)
    print("OCR Response:", response.json())

# 4. Summarization Test
summary_data = {
    "text": "ប្រទេសកម្ពុជា ជារដ្ឋាភិបាលនៃរាជាណាចក្រកម្ពុជា...",
    "max_length": 150
}
response = requests.post(f"{BASE_URL}/api/llm/summarize", json=summary_data)
print("Summary Response:", response.json())

# 5. Video Generation Test
video_data = {
    "prompt": "A serene landscape with mountains",
    "duration": 5,
    "resolution": "720p"
}
response = requests.post(f"{BASE_URL}/api/video/generate", json=video_data)
print("Video Response:", response.json())

# 6. Get Available Models
models = requests.get(f"{BASE_URL}/api/tts/models")
print("Available TTS Models:", models.json())
```

## Using Postman

### Import Collection

Create a Postman collection with the following requests:

1. **GET** Health Check
   - URL: `http://localhost:8000/health`

2. **POST** TTS Synthesize
   - URL: `http://localhost:8000/api/tts/synthesize`
   - Body (JSON):
   ```json
   {
     "text": "សួស្តី",
     "language": "khmer"
   }
   ```

3. **POST** OCR Extract
   - URL: `http://localhost:8000/api/ocr/extract`
   - Body (form-data):
     - file: [select image file]

4. **POST** Summarize
   - URL: `http://localhost:8000/api/llm/summarize`
   - Body (JSON):
   ```json
   {
     "text": "Your long Khmer text here...",
     "max_length": 150,
     "min_length": 30
   }
   ```

5. **GET** Available Models
   - URL: `http://localhost:8000/api/tts/models`
   - URL: `http://localhost:8000/api/ocr/models`
   - URL: `http://localhost:8000/api/llm/models`
   - URL: `http://localhost:8000/api/video/models`

## Frontend Testing

### Manual Testing Steps

1. **Start the services**
   ```bash
   docker-compose up
   ```

2. **Access the frontend**
   - Open browser to http://localhost:3000

3. **Test TTS Page**
   - Navigate to http://localhost:3000/tts
   - Enter Khmer text
   - Click "Generate Speech"
   - Verify audio playback

4. **Test OCR Page**
   - Navigate to http://localhost:3000/ocr
   - Upload an image with Khmer text
   - Click "Extract Text"
   - Verify extracted text

5. **Test Summarization Page**
   - Navigate to http://localhost:3000/summarize
   - Enter long Khmer text
   - Adjust summary length
   - Click "Summarize Text"
   - Verify summary output

6. **Test Video Page**
   - Navigate to http://localhost:3000/video
   - Enter video description
   - Set duration and resolution
   - Click "Generate Video"
   - Check response

## Automated Testing

### Backend Unit Tests

Create `backend/tests/test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_tts_models():
    response = client.get("/api/tts/models")
    assert response.status_code == 200
    assert "models" in response.json()

def test_ocr_models():
    response = client.get("/api/ocr/models")
    assert response.status_code == 200
    assert "models" in response.json()

def test_llm_models():
    response = client.get("/api/llm/models")
    assert response.status_code == 200
    assert "models" in response.json()

# Run tests
# pytest backend/tests/test_api.py -v
```

### Frontend Component Tests

Create `frontend/__tests__/page.test.tsx`:

```typescript
import { render, screen } from '@testing-library/react'
import Home from '@/app/page'

describe('Home Page', () => {
  it('renders the main heading', () => {
    render(<Home />)
    const heading = screen.getByText(/Khmer AI\/ML Platform/i)
    expect(heading).toBeInTheDocument()
  })

  it('displays all feature cards', () => {
    render(<Home />)
    expect(screen.getByText(/Text-to-Speech/i)).toBeInTheDocument()
    expect(screen.getByText(/OCR/i)).toBeInTheDocument()
    expect(screen.getByText(/Summarization/i)).toBeInTheDocument()
    expect(screen.getByText(/Video Generation/i)).toBeInTheDocument()
  })
})
```

## Performance Testing

### Load Testing with Locust

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class KhmerAIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def health_check(self):
        self.client.get("/health")

    @task(2)
    def get_tts_models(self):
        self.client.get("/api/tts/models")

    @task(1)
    def synthesize_speech(self):
        self.client.post("/api/tts/synthesize", json={
            "text": "សួស្តី",
            "language": "khmer"
        })

# Run: locust -f locustfile.py --host=http://localhost:8000
```

### Load Testing with Apache Bench

```bash
# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test TTS endpoint
ab -n 100 -c 5 -p tts_payload.json -T application/json http://localhost:8000/api/tts/synthesize
```

## Integration Testing

### Docker Compose Test

```bash
# Start services
docker-compose up -d

# Wait for services to be ready
sleep 10

# Run tests
curl http://localhost:8000/health
curl http://localhost:3000

# Check logs
docker-compose logs backend
docker-compose logs frontend

# Cleanup
docker-compose down
```

## Common Test Scenarios

### Scenario 1: End-to-End TTS Flow

```bash
# 1. Check TTS models
curl http://localhost:8000/api/tts/models

# 2. Generate speech
curl -X POST http://localhost:8000/api/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "សួស្តី"}'

# 3. Verify response contains audio data
```

### Scenario 2: OCR Processing

```bash
# 1. Check OCR models
curl http://localhost:8000/api/ocr/models

# 2. Upload image and extract text
curl -X POST http://localhost:8000/api/ocr/extract \
  -F "file=@test_image.jpg"

# 3. Verify extracted text
```

### Scenario 3: Text Summarization

```bash
# 1. Get summarization models
curl http://localhost:8000/api/llm/models

# 2. Summarize text
curl -X POST http://localhost:8000/api/llm/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Long Khmer text...",
    "max_length": 150
  }'

# 3. Verify summary quality
```

## Troubleshooting Tests

### Backend Not Responding

```bash
# Check if backend is running
docker-compose ps

# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Frontend Connection Issues

```bash
# Check CORS settings in backend
# Verify API URL in frontend/.env

# Check frontend logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend
```

### Model Loading Errors

```bash
# Check model cache
ls -la ~/.cache/huggingface

# Clear cache and restart
rm -rf ~/.cache/huggingface
docker-compose restart backend
```

## Expected Response Times

- Health Check: < 50ms
- TTS Synthesis: 2-5 seconds
- OCR Extraction: 1-3 seconds
- Text Summarization: 3-10 seconds
- Video Generation: Varies (requires GPU)

---

For issues or questions, contact: menghoutchhon003@gmail.com
