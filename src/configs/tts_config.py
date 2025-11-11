"""
TTS Configuration
Central configuration for TTS system.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class TTSConfig:
    """
    TTS Configuration class.
    """

    # Engine settings
    engine: str = "coqui"
    language: str = "ko"
    device: str = "cpu"

    # Audio settings
    sample_rate: int = 22050
    output_format: str = "wav"

    # Voice settings
    speaker_id: Optional[int] = None
    speaker_name: Optional[str] = None
    voice_name: Optional[str] = None

    # Prosody settings
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0

    # Style and emotion
    emotion: str = "neutral"
    style: Optional[str] = None

    # Processing options
    normalize_text: bool = True
    enhance_audio: bool = True
    reduce_noise: bool = False

    # Cloud API credentials
    google_credentials: Optional[str] = None
    azure_key: Optional[str] = None
    azure_region: Optional[str] = None
    aws_access_key: Optional[str] = None
    aws_secret_key: Optional[str] = None

    # Model paths
    model_cache_dir: str = "./data/models"

    # Advanced options
    use_phoneme_conversion: bool = False
    use_llm_context: bool = False

    # Additional config
    extra_config: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "engine": self.engine,
            "language": self.language,
            "device": self.device,
            "sample_rate": self.sample_rate,
            "output_format": self.output_format,
            "speaker_id": self.speaker_id,
            "speaker_name": self.speaker_name,
            "voice_name": self.voice_name,
            "speed": self.speed,
            "pitch": self.pitch,
            "volume": self.volume,
            "emotion": self.emotion,
            "style": self.style,
            "normalize_text": self.normalize_text,
            "enhance_audio": self.enhance_audio,
            "reduce_noise": self.reduce_noise,
            **self.extra_config
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "TTSConfig":
        """Create config from dictionary."""
        # Extract known fields
        known_fields = {
            k: v for k, v in config_dict.items()
            if k in cls.__dataclass_fields__
        }

        # Put unknown fields in extra_config
        extra_fields = {
            k: v for k, v in config_dict.items()
            if k not in cls.__dataclass_fields__
        }

        if extra_fields:
            known_fields["extra_config"] = extra_fields

        return cls(**known_fields)


# Engine-specific configurations
ENGINE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "coqui": {
        "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
        "vocoder_name": None,
        "supports_languages": ["ko", "en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh", "ja"],
        "supports_voice_cloning": True,
    },
    "google": {
        "default_voice": {
            "ko": "ko-KR-Wavenet-A",
            "en": "en-US-Wavenet-D"
        },
        "supports_ssml": True,
        "cloud_based": True,
    },
    "azure": {
        "default_voice": {
            "ko": "ko-KR-SunHiNeural",
            "en": "en-US-JennyNeural"
        },
        "supports_ssml": True,
        "supports_styles": True,
        "cloud_based": True,
    },
    "polly": {
        "default_voice": {
            "ko": "Seoyeon",
            "en": "Joanna"
        },
        "supports_ssml": True,
        "supports_neural": True,
        "cloud_based": True,
    },
    "piper": {
        "local": True,
        "fast": True,
        "low_resource": True,
    }
}


def get_default_config(engine: str = "coqui") -> TTSConfig:
    """
    Get default configuration for an engine.

    Args:
        engine: Engine name

    Returns:
        Default TTSConfig
    """
    config = TTSConfig(engine=engine)

    # Apply engine-specific defaults
    if engine in ENGINE_CONFIGS:
        engine_config = ENGINE_CONFIGS[engine]
        config.extra_config.update(engine_config)

    return config
