# 🚀 Deployment Guide - Khmer AI/ML Platform

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [GPU Setup](#gpu-setup)
5. [Troubleshooting](#troubleshooting)

## Local Development

### Backend Development

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Docker Deployment

### Local Docker Setup

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

### Production Docker Setup

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

## Cloud Deployment

### AWS Deployment

#### 1. EC2 Setup

```bash
# Launch EC2 instance (p3.2xlarge for GPU)
# Install Docker and Docker Compose

sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install NVIDIA Docker (for GPU)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | sudo tee /etc/yum.repos.d/nvidia-docker.repo
sudo yum install -y nvidia-docker2
sudo systemctl restart docker

# Clone repository
git clone https://github.com/MenghoutChhon/MenghoutChhon.git
cd MenghoutChhon

# Deploy
docker-compose up -d
```

#### 2. ECS Setup

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name khmer-ai-cluster

# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service --cluster khmer-ai-cluster --service-name khmer-ai-service --task-definition khmer-ai-task --desired-count 1
```

### Google Cloud Platform

```bash
# Create GKE cluster
gcloud container clusters create khmer-ai-cluster \
  --num-nodes=3 \
  --machine-type=n1-standard-4 \
  --accelerator type=nvidia-tesla-t4,count=1

# Deploy to GKE
kubectl apply -f kubernetes/

# Expose service
kubectl expose deployment khmer-ai --type=LoadBalancer --port=80
```

### Azure Deployment

```bash
# Create resource group
az group create --name khmer-ai-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group khmer-ai-rg \
  --name khmer-ai-cluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Deploy
kubectl apply -f kubernetes/
```

## GPU Setup

### NVIDIA GPU Setup

```bash
# Install NVIDIA drivers
sudo apt-get update
sudo apt-get install -y nvidia-driver-525

# Install CUDA
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
sudo sh cuda_11.8.0_520.61.05_linux.run

# Verify installation
nvidia-smi
nvcc --version

# Install cuDNN
# Download cuDNN from NVIDIA website
sudo dpkg -i cudnn-local-repo-*.deb
sudo apt-get update
sudo apt-get install libcudnn8
```

### Docker GPU Support

```yaml
# docker-compose.gpu.yml
version: '3.8'

services:
  backend:
    build: ./backend
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
    ports:
      - "8000:8000"
```

## Environment Configuration

### Production Environment Variables

```bash
# Backend (.env)
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://yourdomain.com
TTS_MODEL=facebook/mms-tts-khm
OCR_MODEL=songhieng/khmer-trocr-ocr-v1.0
SUMMARIZATION_MODEL=Seanghay/khmer-mt5-summarization
CUDA_VISIBLE_DEVICES=0
LOG_LEVEL=WARNING

# Frontend (.env)
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_NAME="Khmer AI/ML Platform"
```

## Monitoring and Logging

### Setup Prometheus

```bash
# Install Prometheus
docker run -d -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

### Setup Grafana

```bash
# Install Grafana
docker run -d -p 3001:3000 \
  grafana/grafana
```

### Application Logging

```python
# Add to backend/main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Scaling

### Horizontal Scaling

```bash
# Scale with Docker Compose
docker-compose up --scale backend=3

# Scale with Kubernetes
kubectl scale deployment khmer-ai-backend --replicas=5
```

### Load Balancing

```nginx
# nginx.conf
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

## Security

### SSL/TLS Setup

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

### Firewall Configuration

```bash
# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow backend port
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable
```

## Backup and Recovery

### Database Backup

```bash
# Backup PostgreSQL
docker exec -t postgres pg_dump -U username dbname > backup.sql

# Restore
docker exec -i postgres psql -U username dbname < backup.sql
```

### Model Backup

```bash
# Backup model cache
tar -czf models_backup.tar.gz /root/.cache/huggingface

# Restore
tar -xzf models_backup.tar.gz -C /
```

## Troubleshooting

### Common Issues

#### 1. Model Download Fails

```bash
# Set HuggingFace cache directory
export HF_HOME=/path/to/cache
export TRANSFORMERS_CACHE=/path/to/cache
```

#### 2. GPU Not Detected

```bash
# Check CUDA installation
nvidia-smi
nvcc --version

# Verify PyTorch CUDA support
python -c "import torch; print(torch.cuda.is_available())"
```

#### 3. CORS Errors

```python
# Update backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 4. Out of Memory

```python
# Reduce batch size or model size
# Use model quantization
from transformers import AutoModel

model = AutoModel.from_pretrained(
    model_name,
    load_in_8bit=True,
    device_map="auto"
)
```

## Performance Optimization

### Model Optimization

```python
# Use ONNX Runtime
from optimum.onnxruntime import ORTModelForSeq2SeqLM

model = ORTModelForSeq2SeqLM.from_pretrained(model_name)
```

### Caching

```python
# Add Redis caching
from redis import Redis
from functools import lru_cache

redis_client = Redis(host='localhost', port=6379)

@lru_cache(maxsize=1000)
def cached_inference(text):
    # Your inference code
    pass
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push
        run: |
          docker build -t khmer-ai .
          docker push khmer-ai:latest
      - name: Deploy
        run: |
          ssh user@server 'docker-compose pull && docker-compose up -d'
```

---

For additional support, please contact: menghoutchhon003@gmail.com
