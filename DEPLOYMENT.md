# LMN Platform - Deployment Guide

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

## Local Development

### Backend Setup

1. **System Requirements**
   - Python 3.10 or higher
   - 8GB RAM minimum (16GB recommended)
   - (Optional) NVIDIA GPU with CUDA support

2. **Installation**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run Development Server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Setup

1. **System Requirements**
   - Node.js 18 or higher
   - npm or yarn

2. **Installation**
```bash
cd frontend
npm install
```

3. **Environment Configuration**
Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Run Development Server**
```bash
npm run dev
```

5. **Access Application**
   - http://localhost:3000

## Docker Deployment

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 1.29+
- (Optional) NVIDIA Docker for GPU support

### Standard Deployment

1. **Clone Repository**
```bash
git clone https://github.com/MenghoutChhon/lmn.git
cd lmn
```

2. **Start Services**
```bash
docker-compose up -d
```

3. **View Logs**
```bash
docker-compose logs -f
```

4. **Stop Services**
```bash
docker-compose down
```

### GPU-Enabled Deployment

1. **Install NVIDIA Container Toolkit**
```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

2. **Update docker-compose.yml**
Add GPU support to backend service:
```yaml
backend:
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

## Cloud Deployment

### AWS Deployment

#### EC2 Instance Setup

1. **Launch EC2 Instance**
   - Instance Type: g4dn.xlarge (or higher)
   - AMI: Deep Learning AMI (Ubuntu)
   - Storage: 100GB EBS
   - Security Group: Open ports 80, 443, 8000, 3000

2. **Connect to Instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install Dependencies**
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose git
sudo usermod -aG docker ubuntu
```

4. **Deploy Application**
```bash
git clone https://github.com/MenghoutChhon/lmn.git
cd lmn
docker-compose up -d
```

#### ECS Deployment (Advanced)

1. **Create ECR Repositories**
```bash
aws ecr create-repository --repository-name lmn-backend
aws ecr create-repository --repository-name lmn-frontend
```

2. **Build and Push Images**
```bash
# Backend
cd backend
docker build -t lmn-backend .
docker tag lmn-backend:latest YOUR_ECR_URI/lmn-backend:latest
docker push YOUR_ECR_URI/lmn-backend:latest

# Frontend
cd ../frontend
docker build -t lmn-frontend .
docker tag lmn-frontend:latest YOUR_ECR_URI/lmn-frontend:latest
docker push YOUR_ECR_URI/lmn-frontend:latest
```

3. **Create ECS Task Definition and Service**
   - Use AWS Console or CLI to create task definitions
   - Configure load balancer
   - Set up auto-scaling

### Google Cloud Platform

1. **Create GKE Cluster**
```bash
gcloud container clusters create lmn-cluster \
  --num-nodes=2 \
  --machine-type=n1-standard-4 \
  --accelerator type=nvidia-tesla-t4,count=1
```

2. **Deploy with Kubernetes**
```bash
kubectl apply -f k8s/
```

### RunPod / Lambda Labs

1. **Create GPU Instance**
   - Select GPU: A4000 or higher
   - Template: PyTorch

2. **SSH into Instance**
```bash
ssh root@your-instance-ip
```

3. **Deploy Application**
```bash
git clone https://github.com/MenghoutChhon/lmn.git
cd lmn
docker-compose up -d
```

## Production Considerations

### Security

1. **Environment Variables**
```bash
# Never commit .env files
# Use secret management services:
# - AWS Secrets Manager
# - Google Secret Manager
# - HashiCorp Vault
```

2. **HTTPS/SSL**
```bash
# Use Let's Encrypt with Nginx
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

3. **API Rate Limiting**
Add to backend/main.py:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### Performance Optimization

1. **Model Caching**
   - Use Redis for caching model outputs
   - Implement request deduplication

2. **Load Balancing**
   - Use Nginx or AWS ALB
   - Multiple backend instances

3. **CDN**
   - CloudFront (AWS)
   - Cloud CDN (GCP)
   - Cloudflare

### Monitoring

1. **Application Monitoring**
```bash
# Install Prometheus + Grafana
docker run -d -p 9090:9090 prom/prometheus
docker run -d -p 3001:3000 grafana/grafana
```

2. **Log Aggregation**
   - ELK Stack (Elasticsearch, Logstash, Kibana)
   - CloudWatch (AWS)
   - Cloud Logging (GCP)

3. **Health Checks**
```python
# Already implemented in backend
GET /health
```

### Backup and Recovery

1. **Database Backups** (if applicable)
```bash
# Automated daily backups
crontab -e
0 2 * * * /path/to/backup-script.sh
```

2. **Model Versioning**
   - Use DVC (Data Version Control)
   - Store models in S3/GCS

### Cost Optimization

1. **Spot Instances**
   - Use AWS Spot or GCP Preemptible instances
   - Save up to 90% on compute costs

2. **Auto-Scaling**
   - Scale down during low traffic
   - Scale up during peak hours

3. **Model Optimization**
   - Use ONNX Runtime for faster inference
   - Quantize models to reduce memory usage

## Troubleshooting

### Common Issues

1. **Out of Memory**
```bash
# Reduce batch size
# Use model quantization
# Upgrade instance size
```

2. **Slow Model Loading**
```bash
# Use model caching
# Preload models on startup
```

3. **CORS Issues**
```python
# Update CORS settings in backend/main.py
allow_origins=["https://yourdomain.com"]
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/MenghoutChhon/lmn/issues
- Email: menghoutchhon003@gmail.com
