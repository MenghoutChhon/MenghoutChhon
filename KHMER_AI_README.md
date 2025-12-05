# 🇰🇭 Khmer AI/ML Platform

A comprehensive AI/ML web platform for Khmer language processing, featuring Text-to-Speech, OCR, Summarization, and Video Generation capabilities.

## 🎯 Features

### 1. **Text-to-Speech (TTS)** 🔊
- Convert Khmer text to natural-sounding speech
- Powered by Meta's MMS-TTS model (`facebook/mms-tts-khm`)
- High-quality VITS-based speech synthesis

### 2. **Optical Character Recognition (OCR)** 📸
- Extract Khmer text from images
- Uses TrOCR fine-tuned model (`songhieng/khmer-trocr-ocr-v1.0`)
- Optimized for ID cards, documents, and printed text

### 3. **Text Summarization** 📝
- Summarize long Khmer text
- Powered by mT5 model (`Seanghay/khmer-mt5-summarization`)
- Customizable summary length

### 4. **Video Generation** 🎬
- Generate videos from text prompts
- Support for multiple state-of-the-art models:
  - Mochi 1 (10B+ parameters, MIT license)
  - Wan2.2-T2V-A14B (14B parameters)
  - HunyuanVideo (13B+ parameters)
  - LongCat Video, ByteDance Vidi2

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KHMER AI/ML WEB PLATFORM                 │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Next.js 14 + TypeScript + Tailwind CSS)         │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   TTS Module │  OCR Module  │  LLM Module  │  Video Gen     │
│  (MMS/VITS)  │  (TrOCR)     │  (mT5)       │  (Mochi/Wan2)  │
├──────────────┴──────────────┴──────────────┴────────────────┤
│  Backend API (FastAPI + Python 3.11)                        │
├─────────────────────────────────────────────────────────────┤
│  ML Inference (PyTorch + Transformers + ONNX)               │
├─────────────────────────────────────────────────────────────┤
│  GPU Infrastructure (CUDA / Cloud GPU)                      │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Project Structure

```
khmer-ai-platform/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── tts_router.py          # TTS endpoints
│   │   ├── ocr_router.py          # OCR endpoints
│   │   ├── llm_router.py          # Summarization endpoints
│   │   └── video_router.py        # Video generation endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── tts_model.py           # TTS model handler
│   │   ├── ocr_model.py           # OCR model handler
│   │   ├── summarization_model.py # Summarization model
│   │   └── video_model.py         # Video generation model
│   ├── main.py                    # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Home page
│   │   ├── layout.tsx             # Root layout
│   │   ├── globals.css
│   │   ├── tts/page.tsx           # TTS interface
│   │   ├── ocr/page.tsx           # OCR interface
│   │   ├── summarize/page.tsx     # Summarization interface
│   │   └── video/page.tsx         # Video generation interface
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- OR:
  - Python 3.11+
  - Node.js 18+
  - CUDA-capable GPU (optional, but recommended for video generation)

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/MenghoutChhon/MenghoutChhon.git
   cd MenghoutChhon
   ```

2. **Start the services**
   ```bash
   docker-compose up --build
   ```

3. **Access the platform**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the frontend**
   ```bash
   npm run dev
   ```

4. **Access the application**
   - Open http://localhost:3000 in your browser

## 📚 API Documentation

### TTS Endpoints

- `POST /api/tts/synthesize` - Convert text to speech
- `GET /api/tts/models` - List available TTS models

### OCR Endpoints

- `POST /api/ocr/extract` - Extract text from image
- `GET /api/ocr/models` - List available OCR models

### LLM Endpoints

- `POST /api/llm/summarize` - Summarize text
- `POST /api/llm/generate` - Generate text from prompt
- `GET /api/llm/models` - List available LLM models

### Video Endpoints

- `POST /api/video/generate` - Generate video from text
- `GET /api/video/models` - List available video models

Full API documentation is available at: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Model Configuration
TTS_MODEL=facebook/mms-tts-khm
OCR_MODEL=songhieng/khmer-trocr-ocr-v1.0
SUMMARIZATION_MODEL=Seanghay/khmer-mt5-summarization

# GPU Configuration
CUDA_VISIBLE_DEVICES=0
```

## 🎨 Tech Stack

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **ML Libraries**: PyTorch, Transformers, TTS
- **OCR**: EasyOCR, TrOCR

### DevOps
- **Containerization**: Docker, Docker Compose
- **Deployment**: Kubernetes-ready

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📈 Performance

- **TTS**: ~2-5 seconds per sentence
- **OCR**: ~1-3 seconds per image
- **Summarization**: ~3-10 seconds depending on text length
- **Video Generation**: Requires GPU (varies by model and duration)

## 🔒 Security Features

- CORS middleware for cross-origin requests
- Input validation using Pydantic
- File upload size limits
- Rate limiting (to be implemented)
- JWT authentication (to be implemented)

## 🚧 Roadmap

- [ ] Add user authentication and authorization
- [ ] Implement rate limiting
- [ ] Add database for storing user data
- [ ] Implement Celery for async task processing
- [ ] Add more Khmer language models
- [ ] Deploy video generation models
- [ ] Add batch processing capabilities
- [ ] Implement model fine-tuning interface
- [ ] Add monitoring and analytics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Meta AI** - MMS-TTS model
- **Hugging Face** - Model hosting and Transformers library
- **Khmer NLP Community** - TrOCR and mT5 fine-tuned models
- **Open-source video generation projects** - Mochi, Wan2.2, HunyuanVideo

## 📞 Contact

**Menghout Chhon**
- Email: menghoutchhon003@gmail.com
- LinkedIn: [linkedin.com/in/menghout-chhon](https://www.linkedin.com/in/menghout-chhon/)
- Location: Phnom Penh, Cambodia

## ⚠️ Important Notes

1. **Model Downloads**: First-time use will download models (can be several GB)
2. **GPU Requirements**: Video generation requires significant GPU resources (A100/H100 recommended)
3. **Memory**: Ensure sufficient RAM (16GB+ recommended) for running models
4. **Storage**: Allocate at least 20GB for model storage

## 🌟 Features in Detail

### Text-to-Speech
The TTS module uses Meta's Massively Multilingual Speech (MMS) model, which provides high-quality speech synthesis for Khmer language. The model is based on VITS architecture and produces natural-sounding speech.

### OCR
The OCR module uses TrOCR (Transformer-based OCR) fine-tuned specifically for Khmer text. It combines Vision Transformer for image understanding and RoBERTa for text generation.

### Summarization
The summarization module uses mT5 (multilingual T5) fine-tuned for Khmer text summarization. It can generate concise summaries while preserving the key information.

### Video Generation
The video generation module provides a framework for integrating state-of-the-art text-to-video models. Note: Requires significant GPU resources for deployment.

---

**Happy Coding! 🚀**
