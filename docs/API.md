# API Reference

Complete API reference for Python TTS.

## Core Classes

### TTSEngine

Main TTS engine with unified interface.

```python
from src.tts_engine import TTSEngine
from src.configs import TTSConfig

config = TTSConfig(engine="coqui", language="ko")
tts = TTSEngine(config=config)
audio = tts.synthesize("Hello World")
```

#### Methods

##### `__init__(engine, config=None)`

Initialize TTS engine.

**Parameters:**
- `engine` (str): Engine name ('coqui', 'google', 'azure', 'polly', 'piper')
- `config` (TTSConfig|dict, optional): Configuration object or dictionary

##### `synthesize(text, output_path=None, **kwargs)`

Synthesize speech from text.

**Parameters:**
- `text` (str): Input text to synthesize
- `output_path` (str, optional): Output file path
- `**kwargs`: Additional parameters (speed, pitch, voice, etc.)

**Returns:**
- `np.ndarray`: Audio data

**Example:**
```python
audio = tts.synthesize(
    "안녕하세요",
    output_path="output.wav",
    speed=1.2,
    pitch=2.0
)
```

##### `synthesize_batch(texts, output_dir=None, **kwargs)`

Synthesize multiple texts.

**Parameters:**
- `texts` (list): List of text strings
- `output_dir` (str, optional): Output directory
- `**kwargs`: Additional parameters

**Returns:**
- `list`: List of audio arrays

##### `list_available_voices()`

List available voices for current engine.

**Returns:**
- `list`: List of voice information

##### `set_voice(voice_name)`

Set voice for synthesis.

**Parameters:**
- `voice_name` (str): Voice name or ID

##### `set_language(language)`

Set language for synthesis.

**Parameters:**
- `language` (str): Language code ('ko', 'en', etc.)

## Configuration

### TTSConfig

Configuration class for TTS settings.

```python
from src.configs import TTSConfig

config = TTSConfig(
    engine="coqui",
    language="ko",
    speed=1.0,
    pitch=0.0,
    enhance_audio=True
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `engine` | str | "coqui" | TTS engine name |
| `language` | str | "ko" | Language code |
| `device` | str | "cpu" | Device ('cpu', 'cuda') |
| `sample_rate` | int | 22050 | Audio sample rate |
| `speed` | float | 1.0 | Speaking speed |
| `pitch` | float | 0.0 | Pitch adjustment |
| `volume` | float | 1.0 | Volume level |
| `emotion` | str | "neutral" | Emotion style |
| `normalize_text` | bool | True | Enable text normalization |
| `enhance_audio` | bool | True | Enable audio enhancement |
| `reduce_noise` | bool | False | Enable noise reduction |

## TTS Engines

### BaseTTSEngine

Base class for all TTS engines.

```python
from src.engines.base import BaseTTSEngine

class CustomEngine(BaseTTSEngine):
    def load_model(self):
        # Load model
        pass

    def synthesize(self, text, **kwargs):
        # Synthesize audio
        return audio
```

### CoquiTTSEngine

Coqui TTS engine implementation.

```python
from src.engines.coqui_tts import CoquiTTSEngine

engine = CoquiTTSEngine(config={
    "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
    "language": "ko"
})
```

#### Methods

##### `clone_voice(text, speaker_wav, language=None)`

Clone voice from reference audio.

**Parameters:**
- `text` (str): Text to synthesize
- `speaker_wav` (str): Path to reference audio
- `language` (str, optional): Language code

**Returns:**
- `np.ndarray`: Cloned voice audio

## Preprocessing

### TextNormalizer

Text normalization for TTS.

```python
from src.preprocessing import TextNormalizer

normalizer = TextNormalizer(language="ko")
normalized = normalizer.normalize("전화번호는 010-1234-5678입니다")
```

#### Methods

##### `normalize(text)`

Normalize text.

**Parameters:**
- `text` (str): Input text

**Returns:**
- `str`: Normalized text

### PhonemeConverter

Convert text to phonemes.

```python
from src.preprocessing import PhonemeConverter

converter = PhonemeConverter(language="ko")
phonemes = converter.convert("안녕하세요")
```

### KoreanProcessor

Korean text processing.

```python
from src.preprocessing.korean_processor import KoreanProcessor

processor = KoreanProcessor()
processed = processor.process("한글 텍스트")
```

#### Methods

##### `decompose_hangul(text)`

Decompose Hangul to jamo.

##### `romanize(text, system='revised')`

Romanize Korean text.

##### `detect_korean(text)`

Detect if text contains Korean.

## Postprocessing

### AudioEnhancer

Audio quality enhancement.

```python
from src.postprocessing import AudioEnhancer

enhancer = AudioEnhancer(sample_rate=22050)
enhanced = enhancer.enhance(
    audio,
    normalize=True,
    denoise=True
)
```

#### Methods

##### `enhance(audio, normalize=True, denoise=False, enhance_bass=False, enhance_treble=False)`

Enhance audio quality.

##### `normalize_audio(audio, target_level=0.95)`

Normalize audio amplitude.

##### `adjust_speed(audio, speed=1.0)`

Adjust playback speed.

##### `adjust_pitch(audio, n_steps=0.0)`

Adjust pitch.

### NoiseReducer

Noise reduction.

```python
from src.postprocessing import NoiseReducer

reducer = NoiseReducer(sample_rate=22050)
cleaned = reducer.reduce_noise(audio)
```

## LLM Integration

### ContextAnalyzer

Analyze text context with LLM.

```python
from src.llm_integration import ContextAnalyzer

analyzer = ContextAnalyzer()
analysis = analyzer.analyze("존경하는 여러분")
```

#### Methods

##### `analyze(text, context=None)`

Analyze text for TTS.

**Returns:**
- `dict`: Analysis results (formality, emotion, style, rate, emphasis)

##### `get_prosody_params(analysis)`

Convert analysis to prosody parameters.

### EmotionDetector

Detect emotions in text.

```python
from src.llm_integration import EmotionDetector

detector = EmotionDetector()
emotions = detector.detect("너무 기쁩니다!")
primary = detector.get_primary_emotion("너무 기쁩니다!")
```

## Utilities

### AudioUtils

Audio utility functions.

```python
from src.utils import AudioUtils

# Load audio
audio, sr = AudioUtils.load_audio("input.wav")

# Save audio
AudioUtils.save_audio(audio, "output.wav", sample_rate=22050)

# Concatenate
combined = AudioUtils.concatenate_audio([audio1, audio2])
```

### AudioMetrics

Audio quality metrics.

```python
from src.utils import AudioMetrics

# Calculate metrics
metrics = AudioMetrics.calculate_all_metrics(audio, sample_rate=22050)

# Individual metrics
rms = AudioMetrics.calculate_rms(audio)
snr = AudioMetrics.calculate_snr(audio)
pesq = AudioMetrics.calculate_pesq(reference, degraded)
```

## CLI Commands

```bash
# Synthesize
py-tts synthesize TEXT -o OUTPUT

# Batch processing
py-tts batch INPUT_FILE -o OUTPUT_DIR

# List engines
py-tts engines

# List voices
py-tts list-voices --engine ENGINE

# Normalize text
py-tts normalize TEXT

# Analyze audio
py-tts analyze AUDIO_FILE
```

## Error Handling

### Exception Classes

```python
from src.engines.base import (
    TTSEngineError,
    TTSInitializationError,
    TTSSynthesisError
)

try:
    tts = TTSEngine(engine="invalid")
except TTSInitializationError as e:
    print(f"Failed to initialize: {e}")

try:
    audio = tts.synthesize("text")
except TTSSynthesisError as e:
    print(f"Synthesis failed: {e}")
```

## Examples

See `examples/` directory for complete examples:
- `basic_usage.py` - Basic TTS usage
- `advanced_usage.py` - Advanced features
- `demo.py` - Interactive demo
