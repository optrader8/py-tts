"""
Coqui TTS Engine Implementation
High-quality multilingual TTS with voice cloning support.
"""

from typing import Optional, Dict, Any, List
import numpy as np
from .base import BaseTTSEngine, TTSInitializationError, TTSSynthesisError


class CoquiTTSEngine(BaseTTSEngine):
    """
    Coqui TTS Engine implementation.
    Supports high-quality multilingual speech synthesis.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Coqui TTS Engine.

        Args:
            config: Configuration dictionary
                - model_name: Name of the TTS model
                - vocoder_name: Name of the vocoder model
                - speaker_wav: Path to speaker reference audio (for voice cloning)
                - language: Target language code
        """
        super().__init__(config)

        self.model_name = self.config.get(
            "model_name",
            "tts_models/multilingual/multi-dataset/xtts_v2"
        )
        self.vocoder_name = self.config.get("vocoder_name", None)
        self.speaker_wav = self.config.get("speaker_wav", None)
        self.tts = None

        # Load model on initialization
        self.load_model()

    def load_model(self) -> None:
        """
        Load the Coqui TTS model.
        """
        try:
            from TTS.api import TTS

            print(f"Loading Coqui TTS model: {self.model_name}")

            # Initialize TTS
            self.tts = TTS(
                model_name=self.model_name,
                progress_bar=True,
                gpu=(self.device == "cuda")
            )

            # Get sample rate from model
            if hasattr(self.tts, 'synthesizer') and self.tts.synthesizer:
                self.sample_rate = self.tts.synthesizer.output_sample_rate

            self.initialized = True
            print(f"Coqui TTS model loaded successfully")
            print(f"Sample rate: {self.sample_rate} Hz")

        except ImportError:
            raise TTSInitializationError(
                "Coqui TTS not installed. Install with: pip install TTS"
            )
        except Exception as e:
            raise TTSInitializationError(f"Failed to load Coqui TTS model: {str(e)}")

    def synthesize(
        self,
        text: str,
        speaker: Optional[str] = None,
        language: Optional[str] = None,
        speed: float = 1.0,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from text.

        Args:
            text: Input text to synthesize
            speaker: Speaker name or ID
            language: Language code (e.g., 'ko', 'en')
            speed: Speech speed multiplier
            **kwargs: Additional parameters

        Returns:
            Audio data as numpy array
        """
        if not self.initialized:
            raise TTSSynthesisError("Model not initialized. Call load_model() first.")

        # Preprocess text
        text = self.preprocess_text(text)

        # Get language
        lang = language or self.language

        try:
            # Check if model supports multiple speakers
            if hasattr(self.tts, 'speakers') and self.tts.speakers:
                # Multi-speaker model
                if speaker is None:
                    speaker = self.tts.speakers[0] if self.tts.speakers else None

                audio = self.tts.tts(
                    text=text,
                    speaker=speaker,
                    language=lang
                )
            elif self.speaker_wav:
                # Voice cloning mode
                audio = self.tts.tts(
                    text=text,
                    speaker_wav=self.speaker_wav,
                    language=lang
                )
            else:
                # Single speaker model
                audio = self.tts.tts(
                    text=text,
                    language=lang
                )

            # Convert to numpy array
            if isinstance(audio, list):
                audio = np.array(audio, dtype=np.float32)

            # Apply speed adjustment if needed
            if speed != 1.0:
                audio = self._adjust_speed(audio, speed)

            # Postprocess audio
            audio = self.postprocess_audio(audio)

            return audio

        except Exception as e:
            raise TTSSynthesisError(f"Synthesis failed: {str(e)}")

    def _adjust_speed(self, audio: np.ndarray, speed: float) -> np.ndarray:
        """
        Adjust audio speed using time stretching.

        Args:
            audio: Input audio
            speed: Speed multiplier

        Returns:
            Speed-adjusted audio
        """
        try:
            import librosa
            return librosa.effects.time_stretch(audio, rate=speed)
        except ImportError:
            print("Warning: librosa not available for speed adjustment")
            return audio

    def get_available_speakers(self) -> List[str]:
        """
        Get list of available speakers for the model.

        Returns:
            List of speaker names
        """
        if not self.initialized:
            return []

        if hasattr(self.tts, 'speakers') and self.tts.speakers:
            return self.tts.speakers
        return []

    def get_available_languages(self) -> List[str]:
        """
        Get list of available languages for the model.

        Returns:
            List of language codes
        """
        if not self.initialized:
            return []

        if hasattr(self.tts, 'languages') and self.tts.languages:
            return self.tts.languages
        return []

    def clone_voice(
        self,
        text: str,
        speaker_wav: str,
        language: Optional[str] = None
    ) -> np.ndarray:
        """
        Clone a voice from a reference audio file.

        Args:
            text: Text to synthesize
            speaker_wav: Path to speaker reference audio
            language: Language code

        Returns:
            Audio data as numpy array
        """
        if not self.initialized:
            raise TTSSynthesisError("Model not initialized.")

        text = self.preprocess_text(text)
        lang = language or self.language

        try:
            audio = self.tts.tts(
                text=text,
                speaker_wav=speaker_wav,
                language=lang
            )

            if isinstance(audio, list):
                audio = np.array(audio, dtype=np.float32)

            audio = self.postprocess_audio(audio)
            return audio

        except Exception as e:
            raise TTSSynthesisError(f"Voice cloning failed: {str(e)}")

    def get_engine_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the engine.

        Returns:
            Dictionary with engine information
        """
        info = super().get_engine_info()
        info.update({
            "model_name": self.model_name,
            "vocoder_name": self.vocoder_name,
            "available_speakers": self.get_available_speakers(),
            "available_languages": self.get_available_languages(),
            "supports_voice_cloning": True
        })
        return info
