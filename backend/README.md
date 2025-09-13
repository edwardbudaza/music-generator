# Music Generation API

A production-ready AI music generation service built with Modal, featuring advanced music synthesis using the ACE-Step model, automated lyrics generation, and cover art creation.

## 🎵 Features

- **AI Music Generation**: Powered by ACE-Step pipeline for high-quality audio synthesis
- **Intelligent Lyrics Generation**: Automated lyric creation using Qwen2-7B-Instruct
- **Cover Art Generation**: Automatic thumbnail creation with Stable Diffusion XL Turbo
- **Cloud Storage Integration**: Seamless file management with Cloudflare R2
- **Secure Authentication**: Bearer token-based API security
- **Scalable Infrastructure**: Auto-scaling deployment on Modal with GPU acceleration
- **Multiple Generation Modes**: Description-based, custom lyrics, and instrumental generation

## 🏗️ Solution Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client Apps   │────│   FastAPI        │────│   Modal Cloud   │
│                 │    │   Endpoints      │    │   (GPU Nodes)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                │                        │
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Bearer Token   │    │   AI Models     │
                       │   Authentication │    │   - ACE-Step    │
                       └──────────────────┘    │   - Qwen2-7B    │
                                              │   - SDXL Turbo  │
                                              └─────────────────┘
                                                       │
                                              ┌─────────────────┐
                                              │   Cloudflare    │
                                              │   R2 Storage    │
                                              └─────────────────┘
```

### Core Components

1. **Music Generation Engine**: ACE-Step pipeline for neural audio synthesis
2. **Language Model**: Qwen2-7B-Instruct for prompt enhancement and lyrics generation
3. **Image Generation**: Stable Diffusion XL Turbo for cover art creation
4. **Storage Layer**: Cloudflare R2 for scalable file storage
5. **Authentication**: Secure bearer token validation
6. **Deployment**: Modal serverless GPU infrastructure

## 🚀 Quick Start

### Prerequisites

- Python 3.11
- Modal account with GPU access
- Cloudflare R2 account
- Required dependencies (see `requirements.txt`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/edwardbudaza/music-generator.git
   cd music-generator/backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Modal CLI**
   ```bash
   pip install modal
   modal setup
   ```

## 🔧 Configuration & Setup

### Environment Variables

Create the following secrets in Modal:

#### 1. Cloudflare R2 Configuration
```bash
# R2 Storage Settings
R2_BUCKET_NAME=your-bucket-name
R2_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your-r2-access-key
R2_SECRET_ACCESS_KEY=your-r2-secret-key
```

#### 2. API Authentication
```bash
# Bearer Token for API Security
API_BEARER_TOKEN=your-secure-bearer-token
```

### Modal Secret Setup

1. **Create the secret in Modal:**
   ```bash
   modal secret create music-gen-secret
   ```

2. **Set the environment variables:**
   ```bash
   modal secret set music-gen-secret \
     R2_BUCKET_NAME="your-bucket-name" \
     R2_ENDPOINT_URL="https://your-account-id.r2.cloudflarestorage.com" \
     R2_ACCESS_KEY_ID="your-r2-access-key" \
     R2_SECRET_ACCESS_KEY="your-r2-secret-key" \
     API_BEARER_TOKEN="your-secure-bearer-token"
   ```

### Cloudflare R2 Setup

1. **Create R2 Bucket**
   - Log into Cloudflare dashboard
   - Go to R2 Object Storage
   - Create a new bucket
   - Note the bucket name and endpoint URL

2. **Generate API Tokens**
   - Create R2 API token with read/write permissions
   - Save the Access Key ID and Secret Access Key

### Modal Volumes Setup

The application uses two persistent volumes:

1. **Model Volume**: Stores the ACE-Step model checkpoints
   ```bash
   # This is created automatically when the app runs
   # Volume name: ace-step-models
   ```

2. **HuggingFace Cache Volume**: Caches downloaded models
   ```bash
   # This is created automatically when the app runs  
   # Volume name: qwen-hf-cache
   ```

## 📦 Deployment

### Production Deployment

1. **Deploy to Modal**
   ```bash
   modal deploy main.py
   ```

2. **Test the deployment**
   ```bash
   modal run main.py
   ```

3. **Monitor deployment**
   ```bash
   modal logs music-generator
   ```

### Configuration Options

The application supports various configuration parameters:

```python
# Model Configuration
MODEL_CONFIG = ModelConfig(
    music_model_checkpoint_dir="/models",
    llm_model_id="Qwen/Qwen2-7B-Instruct",
    image_model_id="stabilityai/sdxl-turbo",
    # ... other settings
)

# Infrastructure Configuration  
INFRA_CONFIG = InfrastructureConfig(
    app_name="music-generator",
    gpu_type="L40S",  # GPU type for deployment
    scaledown_window=15,  # Auto-scaling timeout
    # ... other settings
)
```

## 🔌 API Endpoints

### Authentication
All endpoints (except `/health`) require bearer token authentication:
```
Authorization: Bearer your-api-bearer-token
```

### Available Endpoints

#### 1. Health Check
```http
GET /health
```
Returns service health status (no authentication required).

#### 2. Authentication Status
```http
POST /auth-status
```
Validates authentication credentials.

#### 3. Generate from Description
```http
POST /generate-from-description
```

**Request Body:**
```json
{
  "full_described_song": "A upbeat electronic dance track with energetic beats",
  "audio_duration": 180.0,
  "seed": -1,
  "guidance_scale": 15.0,
  "infer_step": 60,
  "instrumental": false
}
```

#### 4. Generate with Custom Lyrics
```http
POST /generate-with-lyrics
```

**Request Body:**
```json
{
  "prompt": "electronic rap, 140BPM",
  "lyrics": "Your custom lyrics here...",
  "audio_duration": 180.0,
  "seed": -1,
  "guidance_scale": 15.0,
  "infer_step": 60,
  "instrumental": false
}
```

#### 5. Generate with Described Lyrics
```http
POST /generate-with-described-lyrics
```

**Request Body:**
```json
{
  "prompt": "rave, funk, 140BPM, disco",
  "described_lyrics": "lyrics about summer nights and dancing",
  "audio_duration": 180.0,
  "seed": -1,
  "guidance_scale": 15.0,
  "infer_step": 60,
  "instrumental": false
}
```

### Response Format

All generation endpoints return:
```json
{
  "r2_key": "unique-audio-file-key.wav",
  "cover_image_r2_key": "unique-image-file-key.png", 
  "categories": ["Electronic", "Dance", "Upbeat"]
}
```

## 🎛️ Advanced Configuration

### Audio Generation Parameters

- **audio_duration**: Length of generated audio (default: 180.0 seconds)
- **seed**: Random seed for reproducible generation (default: -1 for random)
- **guidance_scale**: Controls adherence to prompt (default: 15.0)
- **infer_step**: Number of inference steps (default: 60)
- **instrumental**: Generate instrumental version (default: false)

### GPU Configuration

The service is optimized for L40S GPUs but can be configured for other GPU types:

```python
INFRA_CONFIG = InfrastructureConfig(
    gpu_type="A100",  # Options: "L40S", "A100", "T4"
    # ... other settings
)
```

### Scaling Configuration

```python
INFRA_CONFIG = InfrastructureConfig(
    scaledown_window=15,  # Seconds before scaling down
    # ... other settings
)
```

## 🔍 Monitoring & Troubleshooting

### Logs

Monitor application logs:
```bash
modal logs music-generator --follow
```

### Common Issues

1. **Authentication Errors**
   - Verify `API_BEARER_TOKEN` is set correctly in Modal secrets
   - Ensure bearer token is included in request headers

2. **R2 Storage Errors** 
   - Check R2 credentials and permissions
   - Verify bucket exists and is accessible

3. **GPU Memory Issues**
   - Reduce batch size or model parameters
   - Consider upgrading to higher-memory GPU

4. **Model Loading Failures**
   - Check internet connectivity for model downloads
   - Verify HuggingFace cache volume permissions

### Performance Optimization

- **Model Caching**: Models are cached in persistent volumes
- **GPU Optimization**: Configurable torch compile and CPU offload
- **Storage Optimization**: Efficient R2 upload with cleanup

## 🔒 Security Considerations

- **Authentication**: Bearer token validation on all endpoints
- **Environment Variables**: Sensitive data stored in Modal secrets
- **Network Security**: HTTPS-only communication
- **File Cleanup**: Temporary files automatically removed

## 📊 Resource Requirements

### Minimum Requirements
- **GPU**: NVIDIA L40S (recommended) or A100
- **Memory**: 32GB+ GPU memory for optimal performance
- **Storage**: 50GB+ for model caching
- **Network**: High-bandwidth for model downloads

### Recommended Production Setup
- **GPU**: L40S or A100 
- **Scaling**: Auto-scaling enabled with 15-seconds cooldown
- **Storage**: Persistent volumes for model caching
- **Monitoring**: Modal logs and health check endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License

## 🆘 Support

For support and questions:
- Check the troubleshooting section above
- Review Modal documentation at [modal.com/docs](https://modal.com/docs)
- Open an issue in the repository

---

**Note**: This service requires significant GPU resources and may incur substantial cloud computing costs. Monitor usage and set appropriate scaling limits for production deployments.