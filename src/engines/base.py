"""
Base TTS Engine Class
Defines the interface for all TTS engines.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Union
import numpy as np
import soundfile as sf
import io
from pathlib import Path


class BaseTTSEngine(ABC):
    """
    Abstract base class for all TTS engines.

    All TTS engines should inherit from this class and implement
    the required methods.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the TTS engine.

        Args:
            config: Configuration dictionary for the engine
        """
        self.config = config or {}
        self.sample_rate = self.config.get("sample_rate", 22050)
        self.language = self.config.get("language", "ko")
        self.device = self.config.get("device", "cpu")
        self.initialized = False

    @abstractmethod
    def load_model(self) -> None:
        """
        Load the TTS model.
        Should be implemented by each engine.
        """
        pass

    @abstractmethod
    def synthesize(
        self,
        text: str,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from text.

        Args:
            text: Input text to synthesize
            **kwargs: Additional parameters (speed, pitch, emotion, etc.)

        Returns:
            Audio data as numpy array
        """
        pass

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text before synthesis.
        Can be overridden by specific engines.

        Args:
            text: Input text

        Returns:
            Preprocessed text
        """
        # Basic preprocessing
        text = text.strip()
        return text

    def postprocess_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Postprocess audio after synthesis.
        Can be overridden by specific engines.

        Args:
            audio: Input audio array

        Returns:
            Processed audio array
        """
        # Basic postprocessing (normalize)
        if len(audio) > 0:
            max_val = np.abs(audio).max()
            if max_val > 0:
                audio = audio / max_val * 0.95
        return audio

    def save_audio(
        self,
        audio: np.ndarray,
        output_path: Union[str, Path],
        sample_rate: Optional[int] = None
    ) -> None:
        """
        Save audio to file.

        Args:
            audio: Audio data as numpy array
            output_path: Output file path
            sample_rate: Sample rate (uses engine's default if not provided)
        """
        sample_rate = sample_rate or self.sample_rate
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        sf.write(str(output_path), audio, sample_rate)
        print(f"Audio saved to: {output_path}")

    def audio_to_bytes(
        self,
        audio: np.ndarray,
        sample_rate: Optional[int] = None,
        format: str = "WAV"
    ) -> bytes:
        """
        Convert audio array to bytes.

        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate
            format: Audio format (WAV, MP3, etc.)

        Returns:
            Audio data as bytes
        """
        sample_rate = sample_rate or self.sample_rate
        buffer = io.BytesIO()
        sf.write(buffer, audio, sample_rate, format=format)
        buffer.seek(0)
        return buffer.read()

    def get_engine_info(self) -> Dict[str, Any]:
        """
        Get information about the engine.

        Returns:
            Dictionary with engine information
        """
        return {
            "engine_name": self.__class__.__name__,
            "sample_rate": self.sample_rate,
            "language": self.language,
            "device": self.device,
            "initialized": self.initialized,
            "config": self.config
        }

    def set_config(self, config: Dict[str, Any]) -> None:
        """
        Update engine configuration.

        Args:
            config: New configuration dictionary
        """
        self.config.update(config)
        if "sample_rate" in config:
            self.sample_rate = config["sample_rate"]
        if "language" in config:
            self.language = config["language"]
        if "device" in config:
            self.device = config["device"]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(language={self.language}, sample_rate={self.sample_rate})"

    def __repr__(self) -> str:
        return self.__str__()


class TTSEngineError(Exception):
    """Base exception for TTS engine errors."""
    pass


class TTSInitializationError(TTSEngineError):
    """Exception raised when engine initialization fails."""
    pass


class TTSSynthesisError(TTSEngineError):
    """Exception raised when synthesis fails."""
    pass
