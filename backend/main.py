import base64
import os 
import uuid 
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import boto3
import modal 
import requests 
from pydantic import BaseModel
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from prompts import LYRICS_GENERATOR_PROMPT, PROMPT_GENERATOR_PROMPT


# ===========================
# SECURITY SECTION
# ===========================

class BearerTokenAuth:
    """Bearer token authentication handler"""

    def __init__(self):
        self.security = HTTPBearer()
        self.valid_token = os.environ.get("API_BEARER_TOKEN")

        if not self.valid_token:
            raise ValueError("API_BEARER_TOKEN environment variable must be set")
    
    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """Validate bearer token"""
        if credentials.credentials != self.valid_token:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return credentials.credentials
    
# Initialize auth handler
bearer_auth = BearerTokenAuth()

# ===========================
# CONFIGURATION SECTION
# ===========================

@dataclass
class ModelConfig:
    """Configuration for AI models"""
    
    # Music Generation
    music_model_checkpoint_dir: str = "/models"
    music_model_dtype: str = "bfloat16"
    music_model_torch_compile: bool = False
    music_model_cpu_offload: bool = False
    music_model_overlapped_decode: bool = False

    # Large Language Model
    llm_model_id: str = "Qwen/Qwen2-7B-Instruct"
    llm_max_new_tokens: int = 512

    # Image Generation
    image_model_id: str = "stabilityai/sdxl-turbo"
    image_inference_steps: int = 2
    image_guidance_scale: float = 0.0

@dataclass
class InfrastructureConfig:
    """Configuration for infrastructure and deployment"""
    
    app_name: str = "music-generator"
    gpu_type: str = "L40S"
    scaledown_window: int = 15
    hf_cache_dir: str = "/.cache/huggingface"
    temp_output_dir: str = "/tmp/outputs"

    # Volume names
    model_volume_name: str = "ace-step-models"
    hf_cache_volume_name: str = "qwen-hf-cache"
    secret_name: str = "music-gen-secret"

@dataclass
class StorageConfig:
    """Configuration for Cloudflare R2 storage"""

    bucket_name_env: str = "R2_BUCKET_NAME"
    endpoint_url_env: str = "R2_ENDPOINT_URL"
    access_key_env: str = "R2_ACCESS_KEY_ID"
    secret_key_env: str = "R2_SECRET_ACCESS_KEY"
    region: str = "weur"

@dataclass
class AudioConfig:
    """Default audio generation parameters"""
    default_duration: float = 180.0
    default_seed: int = -1
    default_guidance_scale: float = 15.0
    default_infer_step: int = 60
    default_instrumental: bool = False


# Initialize configurations
MODEL_CONFIG = ModelConfig()
INFRA_CONFIG = InfrastructureConfig()
STORAGE_CONFIG = StorageConfig()
AUDIO_CONFIG = AudioConfig()


# ===========================
# DATA MODELS SECTION
# ===========================

class AudioGenerationBase(BaseModel):
    """Base model for audio generation parameters"""
    audio_duration: float = AUDIO_CONFIG.default_duration
    seed: int = AUDIO_CONFIG.default_seed
    guidance_scale: float = AUDIO_CONFIG.default_guidance_scale
    infer_step: int = AUDIO_CONFIG.default_infer_step
    instrumental: bool = AUDIO_CONFIG.default_instrumental


class GenerateFromDescriptionRequest(AudioGenerationBase):
    """Request model for generating music from description"""
    full_described_song: str


class GenerateWithCustomLyricsRequest(AudioGenerationBase):
    """Request model for generating music with custom lyrics"""
    prompt: str
    lyrics: str


class GenerateWithDescribedLyricsRequest(AudioGenerationBase):
    """Request model for generating music with described lyrics"""
    prompt: str
    described_lyrics: str


class GenerateMusicResponseR2(BaseModel):
    """Response model for music generation with R2 storage"""
    r2_key: str
    cover_image_r2_key: str
    categories: List[str]


class GenerateMusicResponse(BaseModel):
    """Response model for direct music generation"""
    audio_data: str


class AuthStatusResponse(BaseModel):
    """Response model for auth status check"""
    authenticated: bool
    message: str


# ===========================
# MODAL SETUP SECTION
# ===========================

app = modal.App(INFRA_CONFIG.app_name)

# Container image setup
image = (
    modal.Image.debian_slim()
    .apt_install("git")
    .pip_install_from_requirements("requirements.txt")
    .run_commands([
        "git clone https://github.com/ace-step/ACE-Step.git /tmp/ACE-Step",
        "cd /tmp/ACE-Step && pip install ."
    ])
    .env({"HF_HOME": INFRA_CONFIG.hf_cache_dir})
    .add_local_python_source("prompts")
)

# Volume setup
model_volume = modal.Volume.from_name(INFRA_CONFIG.model_volume_name, create_if_missing=True)
hf_volume = modal.Volume.from_name(INFRA_CONFIG.hf_cache_volume_name, create_if_missing=True)

# Secrets setup - now includes the API bearer token
music_gen_secrets = modal.Secret.from_name(INFRA_CONFIG.secret_name)


# ===========================
# UTILITY FUNCTIONS SECTION
# ===========================

class StorageManager:
    """Handles Cloudflare R2 storage operations"""
    
    def __init__(self):
        self.client = self._create_r2_client()
        self.bucket_name = os.environ[STORAGE_CONFIG.bucket_name_env]
    
    def _create_r2_client(self):
        """Create and configure Cloudflare R2 client"""
        return boto3.client(
            's3',
            endpoint_url=os.environ[STORAGE_CONFIG.endpoint_url_env],
            aws_access_key_id=os.environ[STORAGE_CONFIG.access_key_env],
            aws_secret_access_key=os.environ[STORAGE_CONFIG.secret_key_env],
            region_name=STORAGE_CONFIG.region
        )
    
    def upload_file(self, local_path: str, r2_key: str) -> str:
        """Upload file to Cloudflare R2 and return the key"""
        self.client.upload_file(local_path, self.bucket_name, r2_key)
        return r2_key
    
    def generate_unique_key(self, extension: str) -> str:
        """Generate a unique key for R2 storage"""
        return f"{uuid.uuid4()}.{extension.lstrip('.')}"


class FileManager:
    """Handles temporary file operations"""
    
    def __init__(self, base_dir: str = INFRA_CONFIG.temp_output_dir):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
    
    def get_temp_path(self, filename: str = None) -> str:
        """Get temporary file path"""
        if filename is None:
            filename = f"{uuid.uuid4()}.tmp"
        return os.path.join(self.base_dir, filename)
    
    def cleanup_file(self, filepath: str) -> None:
        """Safely remove temporary file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except OSError:
            pass  # File might already be deleted


# ===========================
# MAIN APPLICATION CLASS
# ===========================

@app.cls(
    image=image,
    gpu=INFRA_CONFIG.gpu_type,
    volumes={
        "/models": model_volume,
        INFRA_CONFIG.hf_cache_dir: hf_volume
    },
    secrets=[music_gen_secrets],
    scaledown_window=INFRA_CONFIG.scaledown_window
)
class MusicGenServer:
    """Main music generation server class"""
    
    @modal.enter()
    def load_model(self):
        """Initialize all AI models and auth"""
        self._load_music_model()
        self._load_llm_model()
        self._load_image_model()
        
        # Initialize utility classes
        self.storage_manager = StorageManager()
        self.file_manager = FileManager()
        
        # Initialize authentication
        self.bearer_auth = BearerTokenAuth()
    
    def _load_music_model(self):
        """Load the ACE Step music generation model"""
        from acestep.pipeline_ace_step import ACEStepPipeline
        
        self.music_model = ACEStepPipeline(
            checkpoint_dir=MODEL_CONFIG.music_model_checkpoint_dir,
            dtype=MODEL_CONFIG.music_model_dtype,
            torch_compile=MODEL_CONFIG.music_model_torch_compile,
            cpu_offload=MODEL_CONFIG.music_model_cpu_offload,
            overlapped_decode=MODEL_CONFIG.music_model_overlapped_decode
        )
    
    def _load_llm_model(self):
        """Load the language model for text generation"""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_CONFIG.llm_model_id)
        self.llm_model = AutoModelForCausalLM.from_pretrained(
            MODEL_CONFIG.llm_model_id,
            torch_dtype="auto",
            device_map="auto",
            cache_dir=INFRA_CONFIG.hf_cache_dir
        )
    
    def _load_image_model(self):
        """Load the image generation model for thumbnails"""
        from diffusers import AutoPipelineForText2Image
        import torch
        
        self.image_pipe = AutoPipelineForText2Image.from_pretrained(
            MODEL_CONFIG.image_model_id,
            torch_dtype=torch.float16,
            variant="fp16",
            cache_dir=INFRA_CONFIG.hf_cache_dir
        )
        self.image_pipe.to("cuda")
    
    def _query_llm(self, question: str) -> str:
        """Query the language model with a question"""
        messages = [{"role": "user", "content": question}]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.llm_model.device)
        
        generated_ids = self.llm_model.generate(
            model_inputs.input_ids,
            max_new_tokens=MODEL_CONFIG.llm_max_new_tokens
        )
        
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        response = self.tokenizer.batch_decode(
            generated_ids, 
            skip_special_tokens=True
        )[0]
        
        return response
    
    def generate_prompt(self, description: str) -> str:
        """Generate music prompt from description"""
        full_prompt = PROMPT_GENERATOR_PROMPT.format(user_prompt=description)
        return self._query_llm(full_prompt)
    
    def generate_lyrics(self, description: str) -> str:
        """Generate lyrics from description"""
        full_prompt = LYRICS_GENERATOR_PROMPT.format(description=description)
        return self._query_llm(full_prompt)
    
    def generate_categories(self, description: str) -> List[str]:
        """Generate music categories from description"""
        prompt = (
            f"Based on the following music description, list 3-5 relevant genres or categories "
            f"as a comma-separated list. For example: Pop, Electronic, Sad, 80s. "
            f"Description: '{description}'"
        )
        
        response_text = self._query_llm(prompt)
        categories = [cat.strip() for cat in response_text.split(",") if cat.strip()]
        return categories
    
    def _generate_thumbnail(self, prompt: str) -> str:
        """Generate and upload thumbnail image to R2"""
        thumbnail_prompt = f"{prompt}, album cover art"
        
        image = self.image_pipe(
            prompt=thumbnail_prompt,
            num_inference_steps=MODEL_CONFIG.image_inference_steps,
            guidance_scale=MODEL_CONFIG.image_guidance_scale
        ).images[0]
        
        # Save image locally
        image_path = self.file_manager.get_temp_path(f"{uuid.uuid4()}.png")
        image.save(image_path)
        
        try:
            # Upload to R2
            image_r2_key = self.storage_manager.generate_unique_key("png")
            self.storage_manager.upload_file(image_path, image_r2_key)
            return image_r2_key
        finally:
            self.file_manager.cleanup_file(image_path)
    
    def _generate_and_upload_music(
        self,
        prompt: str,
        lyrics: str,
        audio_duration: float,
        infer_step: int,
        guidance_scale: float,
        seed: int
    ) -> str:
        """Generate music and upload to R2"""
        print(f"Generated lyrics: \n{lyrics}")
        print(f"Prompt: \n{prompt}")
        
        # Generate music locally
        audio_path = self.file_manager.get_temp_path(f"{uuid.uuid4()}.wav")
        
        self.music_model(
            prompt=prompt,
            lyrics=lyrics,
            audio_duration=audio_duration,
            infer_step=infer_step,
            guidance_scale=guidance_scale,
            save_path=audio_path,
            manual_seeds=str(seed)
        )
        
        try:
            # Upload to R2
            audio_r2_key = self.storage_manager.generate_unique_key("wav")
            self.storage_manager.upload_file(audio_path, audio_r2_key)
            return audio_r2_key
        finally:
            self.file_manager.cleanup_file(audio_path)
    
    def _generate_complete_music(
        self,
        prompt: str,
        lyrics: str,
        instrumental: bool,
        audio_duration: float,
        infer_step: int,
        guidance_scale: float,
        seed: int,
        description_for_categorization: str
    ) -> GenerateMusicResponseR2:
        """Complete music generation pipeline with R2 upload"""
        
        # Prepare lyrics
        final_lyrics = "[instrumental]" if instrumental else lyrics
        
        # Generate and upload audio
        audio_r2_key = self._generate_and_upload_music(
            prompt, final_lyrics, audio_duration, infer_step, guidance_scale, seed
        )
        
        # Generate and upload thumbnail
        cover_image_r2_key = self._generate_thumbnail(prompt)
        
        # Generate categories
        categories = self.generate_categories(description_for_categorization)
        
        return GenerateMusicResponseR2(
            r2_key=audio_r2_key,
            cover_image_r2_key=cover_image_r2_key,
            categories=categories
        )
    
    # ===========================
    # API ENDPOINTS SECTION
    # ===========================
    
    @modal.fastapi_endpoint(method="GET")
    def health(self) -> dict:
        """Health check endpoint (no authentication required)"""
        return {"status": "healthy", "service": "music-generator"}
    
    @modal.fastapi_endpoint(method="POST")
    def auth_status(self, token: str = Depends(bearer_auth)) -> AuthStatusResponse:
        """Check authentication status"""
        return AuthStatusResponse(
            authenticated=True,
            message="Authentication successful"
        )
    
    @modal.fastapi_endpoint(method="POST")
    def generate(self, token: str = Depends(bearer_auth)) -> GenerateMusicResponse:
        """Simple music generation endpoint for testing"""
        audio_path = self.file_manager.get_temp_path(f"{uuid.uuid4()}.wav")
        
        # Hardcoded example for testing
        self.music_model(
            prompt="electronic rap",
            lyrics="""[verse]
Waves on the bass, pulsing in the speakers,
Turn the dial up, we chasing six-figure features,
Grinding on the beats, codes in the creases,
Digital hustler, midnight in sneakers.

[chorus]
Electro vibes, hearts beat with the hum,
Urban legends ride, we ain't ever numb,
Circuits sparking live, tapping on the drum,
Living on the edge, never succumb.""",
            audio_duration=AUDIO_CONFIG.default_duration,
            infer_step=AUDIO_CONFIG.default_infer_step,
            guidance_scale=AUDIO_CONFIG.default_guidance_scale,
            save_path=audio_path,
        )
        
        try:
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
            return GenerateMusicResponse(audio_data=audio_b64)
        finally:
            self.file_manager.cleanup_file(audio_path)
    
    @modal.fastapi_endpoint(method="POST")
    def generate_from_description(
        self, 
        request: GenerateFromDescriptionRequest,
        token: str = Depends(bearer_auth)
    ) -> GenerateMusicResponseR2:
        """Generate music from a full description"""
        prompt = self.generate_prompt(request.full_described_song)
        
        lyrics = ""
        if not request.instrumental:
            lyrics = self.generate_lyrics(request.full_described_song)
        
        return self._generate_complete_music(
            prompt=prompt,
            lyrics=lyrics,
            description_for_categorization=request.full_described_song,
            **request.model_dump(exclude={"full_described_song"})
        )
    
    @modal.fastapi_endpoint(method="POST")
    def generate_with_lyrics(
        self, 
        request: GenerateWithCustomLyricsRequest,
        token: str = Depends(bearer_auth)
    ) -> GenerateMusicResponseR2:
        """Generate music with custom lyrics"""
        return self._generate_complete_music(
            prompt=request.prompt,
            lyrics=request.lyrics,
            description_for_categorization=request.prompt,
            **request.model_dump(exclude={"prompt", "lyrics"})
        )
    
    @modal.fastapi_endpoint(method="POST")
    def generate_with_described_lyrics(
        self, 
        request: GenerateWithDescribedLyricsRequest,
        token: str = Depends(bearer_auth)
    ) -> GenerateMusicResponseR2:
        """Generate music with lyrics from description"""
        lyrics = ""
        if not request.instrumental:
            lyrics = self.generate_lyrics(request.described_lyrics)
        
        return self._generate_complete_music(
            prompt=request.prompt,
            lyrics=lyrics,
            description_for_categorization=request.prompt,
            **request.model_dump(exclude={"described_lyrics", "prompt"})
        )


# ===========================
# TESTING SECTION
# ===========================

@app.local_entrypoint()
def main():
    """Local testing entrypoint with authentication"""
    server = MusicGenServer()
    endpoint_url = server.generate_with_described_lyrics.get_web_url()
    
    # Get the bearer token from environment
    bearer_token = os.environ.get("API_BEARER_TOKEN")
    if not bearer_token:
        print("Error: API_BEARER_TOKEN environment variable not set")
        return
    
    request_data = GenerateWithDescribedLyricsRequest(
        prompt="rave, funk, 140BPM, disco",
        described_lyrics="lyrics about water bottles",
        guidance_scale=15
    )
    
    payload = request_data.model_dump()
    
    # Include bearer token in headers
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(endpoint_url, json=payload, headers=headers)
    response.raise_for_status()
    result = GenerateMusicResponseR2(**response.json())
    
    print(f"endpoint_url: {endpoint_url}")
    print(f"Success: {result.r2_key} {result.cover_image_r2_key} {result.categories}")
