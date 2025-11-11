# Quick Start Guide

Get started with Python TTS in 5 minutes!

## Installation

```bash
# Clone repository
git clone https://github.com/optrader8/py-tts.git
cd py-tts

# Install
pip install -e .

# Install Coqui TTS (recommended for beginners)
pip install TTS
```

## Basic Usage

### Python API

```python
from src.tts_engine import create_tts_engine

# Create TTS engine
tts = create_tts_engine(engine="coqui", language="ko")

# Synthesize speech
audio = tts.synthesize(
    "안녕하세요. 파이썬 TTS 프로젝트입니다.",
    output_path="output.wav"
)

print("Audio saved to output.wav")
```

### Command Line

```bash
# Basic synthesis
py-tts synthesize "안녕하세요" -o output.wav

# With options
py-tts synthesize "Hello World" \
    --engine coqui \
    --language en \
    --speed 1.2 \
    --output hello.wav

# Batch processing
py-tts batch input.txt -o output_dir/

# List available engines
py-tts engines

# List voices
py-tts list-voices --engine google
```

## Examples

### 1. Different Languages

```python
# Korean
tts_ko = create_tts_engine(engine="coqui", language="ko")
tts_ko.synthesize("안녕하세요", output_path="korean.wav")

# English
tts_en = create_tts_engine(engine="coqui", language="en")
tts_en.synthesize("Hello", output_path="english.wav")
```

### 2. Voice Customization

```python
from src.configs import TTSConfig

config = TTSConfig(
    engine="coqui",
    language="ko",
    speed=1.2,      # Faster
    pitch=2.0,      # Higher pitch
    enhance_audio=True
)

tts = TTSEngine(config=config)
audio = tts.synthesize("빠르고 높은 음성")
```

### 3. Batch Processing

```python
texts = [
    "첫 번째 문장",
    "두 번째 문장",
    "세 번째 문장"
]

tts = create_tts_engine(engine="coqui", language="ko")
audios = tts.synthesize_batch(texts, output_dir="output/")
```

### 4. Cloud TTS (Google)

```python
import os

# Set credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

# Create engine
tts = create_tts_engine(
    engine="google",
    voice_name="ko-KR-Wavenet-A"
)

audio = tts.synthesize("구글 클라우드 TTS", output_path="google.wav")
```

## Advanced Features

### Text Preprocessing

```python
from src.preprocessing import TextNormalizer

normalizer = TextNormalizer(language="ko")
text = "전화번호는 010-1234-5678입니다."
normalized = normalizer.normalize(text)
```

### Audio Enhancement

```python
from src.postprocessing import AudioEnhancer

enhancer = AudioEnhancer(sample_rate=22050)
enhanced = enhancer.enhance(
    audio,
    normalize=True,
    denoise=True,
    enhance_bass=True
)
```

### LLM Context Analysis

```python
import os
os.environ["OPENAI_API_KEY"] = "your-key"

config = TTSConfig(
    engine="coqui",
    use_llm_context=True  # Enable context analysis
)

tts = TTSEngine(config=config)

# Formal speech
audio = tts.synthesize("존경하는 여러분, 감사합니다.")

# Casual speech
audio = tts.synthesize("야, 오늘 뭐해?")
```

## Configuration

### Config File

```python
from src.configs import TTSConfig

# Create config
config = TTSConfig(
    engine="coqui",
    language="ko",
    sample_rate=22050,
    speed=1.0,
    pitch=0.0,
    normalize_text=True,
    enhance_audio=True,
    reduce_noise=False
)

# Save config
import json
with open("tts_config.json", "w") as f:
    json.dump(config.to_dict(), f, indent=2)

# Load config
with open("tts_config.json", "r") as f:
    config_dict = json.load(f)
    config = TTSConfig.from_dict(config_dict)
```

## Supported Engines

| Engine | Type | Quality | Speed | API Key |
|--------|------|---------|-------|---------|
| Coqui TTS | Local | ★★★★★ | ★★★ | ✗ |
| Google Cloud | Cloud | ★★★★★ | ★★★★★ | ✓ |
| Azure | Cloud | ★★★★★ | ★★★★★ | ✓ |
| Amazon Polly | Cloud | ★★★★ | ★★★★★ | ✓ |
| Piper | Local | ★★★ | ★★★★★ | ✗ |

## Next Steps

1. **Explore Examples**: `python examples/basic_usage.py`
2. **Read Full Docs**: See `docs/INSTALLATION.md`
3. **Try Different Engines**: Experiment with cloud services
4. **Customize**: Adjust speed, pitch, and enhancement settings

## Common Commands

```bash
# Development
make install-dev    # Install with dev dependencies
make test          # Run tests
make lint          # Check code style
make format        # Format code

# Usage
py-tts synthesize TEXT -o OUTPUT
py-tts batch INPUT_FILE -o OUTPUT_DIR
py-tts list-voices --engine ENGINE
py-tts analyze AUDIO_FILE
```

## Getting Help

- **Examples**: See `examples/` directory
- **Documentation**: See `docs/` directory
- **Issues**: https://github.com/optrader8/py-tts/issues
