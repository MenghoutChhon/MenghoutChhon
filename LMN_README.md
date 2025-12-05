# 🇰🇭 LMN - Khmer AI/ML Platform

A comprehensive AI/ML web platform for Khmer language processing, featuring Text-to-Speech, OCR, Summarization, and Video Generation capabilities.

## 🚀 Features

- **🔊 Text-to-Speech (TTS)**: Convert Khmer text to natural speech using Meta's MMS model
- **📷 OCR**: Extract Khmer text from images using TrOCR
- **📝 Summarization**: Summarize Khmer text using mT5 and PrahokBART
- **🎬 Video Generation**: Generate videos from text prompts using Mochi 1 or Wan2.2

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LMN - KHMER AI/ML PLATFORM               │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Next.js 14 + Tailwind CSS)                      │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   TTS Module │  OCR Module  │  LLM Module  │  Video Gen     │
│  (MMS)       │  (TrOCR)     │  (mT5/BART)  │  (Mochi/Wan2.2)│
├──────────────┴──────────────┴──────────────┴────────────────┤
│  Backend API (FastAPI)                                      │
├─────────────────────────────────────────────────────────────┤
│  ML Inference (PyTorch + Transformers)                      │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure (Docker + GPU Support)                      │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Project Structure

```
lmn/
├── backend/
│   ├── api/
│   │   ├── tts_router.py      # TTS API endpoints
│   │   ├── ocr_router.py      # OCR API endpoints
│   │   ├── llm_router.py      # LLM API endpoints
│   │   └── video_router.py    # Video generation API
│   ├── models/
│   │   ├── tts_model.py       # TTS model implementation
│   │   ├── ocr_model.py       # OCR model implementation
│   │   ├── llm_model.py       # LLM model implementation
│   │   └── video_model.py     # Video generation model
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Backend Docker configuration
├── frontend/
│   ├── app/
│   │   ├── tts/              # TTS page
│   │   ├── ocr/              # OCR page
│   │   ├── summarize/        # Summarization page
│   │   ├── video/            # Video generation page
│   │   ├── layout.tsx        # Root layout
│   │   └── page.tsx          # Home page
│   ├── package.json          # Node.js dependencies
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   └── Dockerfile            # Frontend Docker configuration
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # This file
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **ML Framework**: PyTorch + Transformers
- **Models**:
  - TTS: `facebook/mms-tts-khm`
  - OCR: `songhieng/khmer-trocr-ocr-v1.0`
  - Summarization: `google/mt5-base`
  - Video: Mochi 1 / Wan2.2

### Frontend
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- (Optional) NVIDIA GPU with CUDA support for faster inference

### Using Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/MenghoutChhon/lmn.git
cd lmn
```

2. **Start the services**
```bash
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup

#### Backend

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

4. **Run the server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run development server**
```bash
npm run dev
```

4. **Open browser**
```
http://localhost:3000
```

## 📚 API Documentation

### TTS Endpoints

**POST** `/api/tts/synthesize`
```json
{
  "text": "ជំរាបសួរ",
  "speed": 1.0
}
```

### OCR Endpoints

**POST** `/api/ocr/recognize`
- Upload image file
- Returns recognized Khmer text

### LLM Endpoints

**POST** `/api/llm/summarize`
```json
{
  "text": "Long Khmer text...",
  "max_length": 150,
  "min_length": 50
}
```

**POST** `/api/llm/generate`
```json
{
  "prompt": "Your prompt...",
  "max_length": 200,
  "temperature": 0.7
}
```

### Video Generation Endpoints

**POST** `/api/video/generate`
```json
{
  "prompt": "A beautiful sunset over Angkor Wat",
  "duration": 5,
  "resolution": "720p",
  "fps": 30
}
```

**GET** `/api/video/status/{job_id}`
- Returns generation status

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend
PYTHONUNBUFFERED=1

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🎯 Models Used

### Text-to-Speech
- **Model**: Meta MMS TTS Khmer (`facebook/mms-tts-khm`)
- **Technology**: VITS (Variational Inference with adversarial learning for end-to-end Text-to-Speech)
- **Features**: Natural Khmer speech synthesis

### OCR
- **Model**: Khmer TrOCR (`songhieng/khmer-trocr-ocr-v1.0`)
- **Technology**: Vision Encoder-Decoder (ViT + RoBERTa)
- **Features**: High accuracy Khmer text recognition

### Summarization
- **Model**: mT5 Base (`google/mt5-base`)
- **Technology**: Multilingual T5
- **Features**: Text summarization and generation

### Video Generation (Placeholder)
- **Models**: Mochi 1, Wan2.2, HunyuanVideo
- **Note**: Requires significant GPU resources

## 🚧 Production Deployment

### Requirements
- GPU instance (AWS, GCP, or Azure)
- Minimum 16GB RAM
- CUDA-capable GPU for optimal performance

### Recommended Cloud Providers
- **RunPod**: Cost-effective GPU instances
- **Lambda Labs**: High-performance GPU cloud
- **Google Cloud**: Comprehensive AI/ML infrastructure

## 📝 TODO

- [ ] Implement user authentication
- [ ] Add rate limiting
- [ ] Deploy to cloud infrastructure
- [ ] Add model fine-tuning capabilities
- [ ] Implement caching for faster response
- [ ] Add support for batch processing
- [ ] Create mobile application

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Menghout Chhon**
- GitHub: [@MenghoutChhon](https://github.com/MenghoutChhon)
- LinkedIn: [Menghout Chhon](https://www.linkedin.com/in/menghout-chhon/)
- Email: menghoutchhon003@gmail.com

## 🙏 Acknowledgments

- Meta AI for the MMS TTS model
- Microsoft for TrOCR
- Google for mT5
- All contributors to the open-source AI/ML community

---

Made with ❤️ for the Khmer language community
