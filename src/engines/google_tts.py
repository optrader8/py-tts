"""
Google Cloud Text-to-Speech Engine Implementation
WaveNet-based high-quality cloud TTS service.
"""

from typing import Optional, Dict, Any, List
import numpy as np
import os
from .base import BaseTTSEngine, TTSInitializationError, TTSSynthesisError


class GoogleTTSEngine(BaseTTSEngine):
    """
    Google Cloud Text-to-Speech Engine implementation.
    Requires Google Cloud credentials.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Google TTS Engine.

        Args:
            config: Configuration dictionary
                - credentials_path: Path to Google Cloud credentials JSON
                - voice_name: Voice name (e.g., 'ko-KR-Wavenet-A')
                - speaking_rate: Speaking rate (0.25-4.0)
                - pitch: Pitch adjustment (-20.0 to 20.0)
                - audio_encoding: Audio encoding format
        """
        super().__init__(config)

        self.credentials_path = self.config.get(
            "credentials_path",
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        self.voice_name = self.config.get("voice_name", "ko-KR-Wavenet-A")
        self.speaking_rate = self.config.get("speaking_rate", 1.0)
        self.pitch = self.config.get("pitch", 0.0)
        self.audio_encoding = self.config.get("audio_encoding", "LINEAR16")

        self.client = None
        self.load_model()

    def load_model(self) -> None:
        """
        Initialize Google Cloud TTS client.
        """
        try:
            from google.cloud import texttospeech

            # Set credentials if provided
            if self.credentials_path:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path

            self.client = texttospeech.TextToSpeechClient()
            self.texttospeech = texttospeech

            self.initialized = True
            print("Google Cloud TTS initialized successfully")

        except ImportError:
            raise TTSInitializationError(
                "Google Cloud TTS not installed. Install with: pip install google-cloud-texttospeech"
            )
        except Exception as e:
            raise TTSInitializationError(
                f"Failed to initialize Google Cloud TTS: {str(e)}\n"
                "Make sure GOOGLE_APPLICATION_CREDENTIALS is set."
            )

    def synthesize(
        self,
        text: str,
        voice_name: Optional[str] = None,
        language: Optional[str] = None,
        speaking_rate: Optional[float] = None,
        pitch: Optional[float] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from text.

        Args:
            text: Input text to synthesize
            voice_name: Voice name (e.g., 'ko-KR-Wavenet-A')
            language: Language code (e.g., 'ko-KR')
            speaking_rate: Speaking rate (0.25-4.0)
            pitch: Pitch adjustment (-20.0 to 20.0)
            **kwargs: Additional parameters

        Returns:
            Audio data as numpy array
        """
        if not self.initialized:
            raise TTSSynthesisError("Client not initialized.")

        # Preprocess text
        text = self.preprocess_text(text)

        # Set parameters
        voice_name = voice_name or self.voice_name
        speaking_rate = speaking_rate or self.speaking_rate
        pitch = pitch or self.pitch

        # Determine language code from voice name if not provided
        if language is None:
            language = self._extract_language_from_voice(voice_name)

        try:
            # Set the text input
            synthesis_input = self.texttospeech.SynthesisInput(text=text)

            # Build the voice request
            voice = self.texttospeech.VoiceSelectionParams(
                language_code=language,
                name=voice_name
            )

            # Select the audio config
            audio_config = self.texttospeech.AudioConfig(
                audio_encoding=getattr(
                    self.texttospeech.AudioEncoding,
                    self.audio_encoding
                ),
                speaking_rate=speaking_rate,
                pitch=pitch
            )

            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Convert audio content to numpy array
            audio = self._bytes_to_array(response.audio_content)

            # Postprocess audio
            audio = self.postprocess_audio(audio)

            return audio

        except Exception as e:
            raise TTSSynthesisError(f"Google TTS synthesis failed: {str(e)}")

    def _bytes_to_array(self, audio_bytes: bytes) -> np.ndarray:
        """
        Convert audio bytes to numpy array.

        Args:
            audio_bytes: Audio data as bytes

        Returns:
            Audio data as numpy array
        """
        import io
        import soundfile as sf

        buffer = io.BytesIO(audio_bytes)
        audio, sample_rate = sf.read(buffer)

        # Update sample rate
        self.sample_rate = sample_rate

        return audio.astype(np.float32)

    def _extract_language_from_voice(self, voice_name: str) -> str:
        """
        Extract language code from voice name.

        Args:
            voice_name: Voice name (e.g., 'ko-KR-Wavenet-A')

        Returns:
            Language code (e.g., 'ko-KR')
        """
        parts = voice_name.split('-')
        if len(parts) >= 2:
            return f"{parts[0]}-{parts[1]}"
        return self.language

    def list_voices(self, language_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available voices.

        Args:
            language_code: Filter by language code (e.g., 'ko-KR')

        Returns:
            List of voice information dictionaries
        """
        if not self.initialized:
            return []

        try:
            # Fetch available voices
            response = self.client.list_voices(language_code=language_code)

            voices = []
            for voice in response.voices:
                voice_info = {
                    "name": voice.name,
                    "language_codes": voice.language_codes,
                    "ssml_gender": voice.ssml_gender.name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
                }
                voices.append(voice_info)

            return voices

        except Exception as e:
            print(f"Failed to list voices: {str(e)}")
            return []

    def synthesize_ssml(
        self,
        ssml: str,
        voice_name: Optional[str] = None,
        language: Optional[str] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from SSML (Speech Synthesis Markup Language).

        Args:
            ssml: SSML text
            voice_name: Voice name
            language: Language code
            **kwargs: Additional parameters

        Returns:
            Audio data as numpy array
        """
        if not self.initialized:
            raise TTSSynthesisError("Client not initialized.")

        voice_name = voice_name or self.voice_name
        language = language or self._extract_language_from_voice(voice_name)

        try:
            # Set the SSML input
            synthesis_input = self.texttospeech.SynthesisInput(ssml=ssml)

            # Build the voice request
            voice = self.texttospeech.VoiceSelectionParams(
                language_code=language,
                name=voice_name
            )

            # Select the audio config
            audio_config = self.texttospeech.AudioConfig(
                audio_encoding=getattr(
                    self.texttospeech.AudioEncoding,
                    self.audio_encoding
                )
            )

            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Convert to numpy array
            audio = self._bytes_to_array(response.audio_content)
            audio = self.postprocess_audio(audio)

            return audio

        except Exception as e:
            raise TTSSynthesisError(f"Google TTS SSML synthesis failed: {str(e)}")

    def get_engine_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the engine.

        Returns:
            Dictionary with engine information
        """
        info = super().get_engine_info()
        info.update({
            "voice_name": self.voice_name,
            "speaking_rate": self.speaking_rate,
            "pitch": self.pitch,
            "audio_encoding": self.audio_encoding,
            "supports_ssml": True,
            "cloud_based": True
        })
        return info
