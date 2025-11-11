# Installation Guide

Complete installation guide for Python TTS Project.

## Table of Contents

- [System Requirements](#system-requirements)
- [Basic Installation](#basic-installation)
- [TTS Engine Installation](#tts-engine-installation)
- [Optional Dependencies](#optional-dependencies)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- Python 3.8 or higher
- 4GB RAM
- 5GB disk space

### Recommended

- Python 3.10+
- 8GB+ RAM
- GPU with CUDA support (for faster synthesis)
- 10GB+ disk space (for models)

## Basic Installation

### 1. Clone Repository

```bash
git clone https://github.com/optrader8/py-tts.git
cd py-tts
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Package

```bash
# Basic installation
pip install -e .

# With development dependencies
pip install -e ".[dev]"

# With all engines
pip install -e ".[all]"
```

## TTS Engine Installation

### Coqui TTS (Local, Open Source)

**Recommended for:** High-quality local synthesis, voice cloning

```bash
pip install TTS
```

**Download models:**

```python
from TTS.api import TTS

# List available models
TTS.list_models()

# Download specific model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
```

**GPU Support:**

```bash
# Install PyTorch with CUDA
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Google Cloud TTS

**Recommended for:** High-quality cloud synthesis, WaveNet voices

**Setup:**

1. Create Google Cloud account
2. Enable Text-to-Speech API
3. Create service account and download credentials

```bash
pip install google-cloud-texttospeech

# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

**Usage:**

```python
from src.tts_engine import create_tts_engine

tts = create_tts_engine(
    engine="google",
    voice_name="ko-KR-Wavenet-A"
)
```

### Microsoft Azure TTS

**Recommended for:** Neural voices with emotion styles

**Setup:**

1. Create Azure account
2. Create Speech resource
3. Get subscription key and region

```bash
pip install azure-cognitiveservices-speech

# Set credentials
export AZURE_SPEECH_KEY="your-key"
export AZURE_SPEECH_REGION="eastus"
```

**Usage:**

```python
from src.tts_engine import create_tts_engine

tts = create_tts_engine(
    engine="azure",
    voice_name="ko-KR-SunHiNeural"
)
```

### Amazon Polly

**Recommended for:** AWS integration, neural voices

**Setup:**

1. Create AWS account
2. Create IAM user with Polly permissions
3. Configure AWS credentials

```bash
pip install boto3

# Configure AWS CLI
aws configure
# Or set environment variables
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
```

**Usage:**

```python
from src.tts_engine import create_tts_engine

tts = create_tts_engine(
    engine="polly",
    voice_id="Seoyeon"
)
```

### Piper TTS (Fast, Local)

**Recommended for:** Fast local synthesis, low resource usage

**Setup:**

1. Install ONNX Runtime

```bash
pip install onnxruntime  # CPU version
# or
pip install onnxruntime-gpu  # GPU version
```

2. Download Piper models

```bash
# Example: Download Korean model
wget https://github.com/rhasspy/piper/releases/download/v1.0.0/voice-ko-kr-x-low.tar.gz
tar -xvf voice-ko-kr-x-low.tar.gz
```

**Usage:**

```python
from src.tts_engine import create_tts_engine

tts = create_tts_engine(
    engine="piper",
    model_path="path/to/model.onnx",
    config_path="path/to/config.json"
)
```

## Optional Dependencies

### Korean Language Support

```bash
# g2pk (Grapheme to Phoneme for Korean)
pip install g2pk

# jamo (Korean character decomposition)
pip install jamo

# hangul-romanize (Romanization)
pip install hangul-romanize
```

### Audio Processing

```bash
# librosa (Audio analysis)
pip install librosa

# noisereduce (Noise reduction)
pip install noisereduce

# pedalboard (Audio effects)
pip install pedalboard

# PyRubberBand (Time/pitch stretching)
pip install pyrubberband
```

### LLM Integration

```bash
# OpenAI
pip install openai

# Anthropic Claude
pip install anthropic

# LangChain
pip install langchain langchain-community
```

### Audio Quality Metrics

```bash
# PESQ (Perceptual Evaluation of Speech Quality)
pip install pesq

# STOI (Short-Time Objective Intelligibility)
pip install pystoi
```

## Verification

### Check Installation

```bash
# Check package installation
python -c "import src; print('✓ Package installed')"

# Check CLI
py-tts --version

# List available engines
py-tts engines
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_config.py -v

# Run with coverage
pytest tests/ --cov=src
```

### Quick Test

```python
from src.tts_engine import create_tts_engine

# Test with Coqui TTS
tts = create_tts_engine(engine="coqui", language="ko")
audio = tts.synthesize("안녕하세요", output_path="test.wav")
print("✓ TTS working!")
```

## Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Error: ModuleNotFoundError: No module named 'src'
# Solution: Install in editable mode
pip install -e .
```

#### 2. CUDA/GPU Issues

```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall PyTorch with correct CUDA version
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

#### 3. Audio Playback Issues

```bash
# Install audio backend
# Linux
sudo apt-get install libsndfile1

# Mac
brew install libsndfile
```

#### 4. Korean Text Processing

```bash
# If g2pk fails to install
pip install --upgrade pip setuptools wheel
pip install g2pk
```

#### 5. Memory Issues

```python
# Use smaller batch sizes
# Enable model caching
config = TTSConfig(cache_models=True, model_cache_dir="./cache")
```

### Getting Help

- **Documentation**: Check docs/ directory
- **Issues**: Report at https://github.com/optrader8/py-tts/issues
- **Examples**: See examples/ directory

## Next Steps

1. **Try Examples**: Run `python examples/basic_usage.py`
2. **Read Documentation**: See `README.md` and `IDEA.md`
3. **Configure**: Set up API keys for cloud services
4. **Experiment**: Try different engines and settings

## Updates

```bash
# Update to latest version
git pull origin main
pip install -e . --upgrade
```
