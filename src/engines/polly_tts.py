"""
Amazon Polly TTS Engine Implementation
Neural TTS with SSML and lexicon support.
"""

from typing import Optional, Dict, Any, List
import numpy as np
import os
from .base import BaseTTSEngine, TTSInitializationError, TTSSynthesisError


class PollyTTSEngine(BaseTTSEngine):
    """
    Amazon Polly Text-to-Speech Engine implementation.
    Requires AWS credentials.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Polly TTS Engine.

        Args:
            config: Configuration dictionary
                - aws_access_key_id: AWS access key
                - aws_secret_access_key: AWS secret key
                - region_name: AWS region (e.g., 'us-east-1')
                - voice_id: Voice ID (e.g., 'Seoyeon' for Korean)
                - engine: 'standard' or 'neural'
                - output_format: Audio format (e.g., 'mp3', 'pcm')
        """
        super().__init__(config)

        self.aws_access_key_id = self.config.get(
            "aws_access_key_id",
            os.getenv("AWS_ACCESS_KEY_ID")
        )
        self.aws_secret_access_key = self.config.get(
            "aws_secret_access_key",
            os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.region_name = self.config.get(
            "region_name",
            os.getenv("AWS_REGION", "us-east-1")
        )
        self.voice_id = self.config.get("voice_id", "Seoyeon")  # Korean female voice
        self.engine = self.config.get("engine", "neural")  # 'standard' or 'neural'
        self.output_format = self.config.get("output_format", "pcm")

        self.polly_client = None
        self.load_model()

    def load_model(self) -> None:
        """
        Initialize Amazon Polly client.
        """
        try:
            import boto3

            # Create Polly client
            if self.aws_access_key_id and self.aws_secret_access_key:
                self.polly_client = boto3.client(
                    'polly',
                    aws_access_key_id=self.aws_access_key_id,
                    aws_secret_access_key=self.aws_secret_access_key,
                    region_name=self.region_name
                )
            else:
                # Use default credentials (from AWS CLI config or IAM role)
                self.polly_client = boto3.client('polly', region_name=self.region_name)

            # Set sample rate based on format
            if self.output_format == "pcm":
                self.sample_rate = 16000
            elif self.output_format == "mp3":
                self.sample_rate = 22050

            self.initialized = True
            print("Amazon Polly TTS initialized successfully")
            print(f"Voice: {self.voice_id}, Engine: {self.engine}, Region: {self.region_name}")

        except ImportError:
            raise TTSInitializationError(
                "boto3 not installed. Install with: pip install boto3"
            )
        except Exception as e:
            raise TTSInitializationError(f"Failed to initialize Amazon Polly: {str(e)}")

    def synthesize(
        self,
        text: str,
        voice_id: Optional[str] = None,
        language: Optional[str] = None,
        engine: Optional[str] = None,
        speaking_rate: Optional[float] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from text.

        Args:
            text: Input text to synthesize
            voice_id: Voice ID (e.g., 'Seoyeon', 'Joanna')
            language: Language code (optional, auto-detected from voice)
            engine: 'standard' or 'neural'
            speaking_rate: Speaking rate (0.5-2.0)
            **kwargs: Additional parameters

        Returns:
            Audio data as numpy array
        """
        if not self.initialized:
            raise TTSSynthesisError("Polly client not initialized.")

        # Preprocess text
        text = self.preprocess_text(text)

        # Set parameters
        voice_id = voice_id or self.voice_id
        engine = engine or self.engine

        # Build SSML if speaking rate is specified
        if speaking_rate and speaking_rate != 1.0:
            text = self._wrap_with_prosody(text, speaking_rate)
            text_type = "ssml"
        else:
            text_type = "text"

        try:
            # Synthesize speech
            response = self.polly_client.synthesize_speech(
                Text=text,
                TextType=text_type,
                OutputFormat=self.output_format,
                VoiceId=voice_id,
                Engine=engine,
                SampleRate=str(self.sample_rate) if self.output_format == "pcm" else None
            )

            # Read audio stream
            audio_stream = response['AudioStream'].read()

            # Convert to numpy array
            audio = self._bytes_to_array(audio_stream)

            # Postprocess audio
            audio = self.postprocess_audio(audio)

            return audio

        except Exception as e:
            raise TTSSynthesisError(f"Amazon Polly synthesis failed: {str(e)}")

    def _wrap_with_prosody(self, text: str, speaking_rate: float) -> str:
        """
        Wrap text with SSML prosody tags.

        Args:
            text: Input text
            speaking_rate: Speaking rate

        Returns:
            SSML string
        """
        # Convert rate to percentage
        rate_percent = int(speaking_rate * 100)

        ssml = f"""<speak>
            <prosody rate="{rate_percent}%">
                {text}
            </prosody>
        </speak>"""

        return ssml

    def _bytes_to_array(self, audio_bytes: bytes) -> np.ndarray:
        """
        Convert audio bytes to numpy array.

        Args:
            audio_bytes: Audio data as bytes

        Returns:
            Audio data as numpy array
        """
        if self.output_format == "pcm":
            # PCM is 16-bit signed integer
            audio = np.frombuffer(audio_bytes, dtype=np.int16)
            # Convert to float32 and normalize
            audio = audio.astype(np.float32) / 32768.0
        else:
            # For MP3, decode first
            import io
            import soundfile as sf

            buffer = io.BytesIO(audio_bytes)
            audio, sample_rate = sf.read(buffer)
            self.sample_rate = sample_rate

            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)

        return audio

    def synthesize_ssml(
        self,
        ssml: str,
        voice_id: Optional[str] = None,
        engine: Optional[str] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from SSML.

        Args:
            ssml: SSML string
            voice_id: Voice ID
            engine: 'standard' or 'neural'
            **kwargs: Additional parameters

        Returns:
            Audio data as numpy array
        """
        if not self.initialized:
            raise TTSSynthesisError("Polly client not initialized.")

        voice_id = voice_id or self.voice_id
        engine = engine or self.engine

        try:
            response = self.polly_client.synthesize_speech(
                Text=ssml,
                TextType="ssml",
                OutputFormat=self.output_format,
                VoiceId=voice_id,
                Engine=engine,
                SampleRate=str(self.sample_rate) if self.output_format == "pcm" else None
            )

            audio_stream = response['AudioStream'].read()
            audio = self._bytes_to_array(audio_stream)
            audio = self.postprocess_audio(audio)

            return audio

        except Exception as e:
            raise TTSSynthesisError(f"Amazon Polly SSML synthesis failed: {str(e)}")

    def list_voices(
        self,
        language_code: Optional[str] = None,
        engine: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List available voices.

        Args:
            language_code: Filter by language code (e.g., 'ko-KR')
            engine: Filter by engine ('standard' or 'neural')

        Returns:
            List of voice information dictionaries
        """
        if not self.initialized:
            return []

        try:
            kwargs = {}
            if language_code:
                kwargs['LanguageCode'] = language_code
            if engine:
                kwargs['Engine'] = engine

            response = self.polly_client.describe_voices(**kwargs)

            voices = []
            for voice in response.get('Voices', []):
                voice_info = {
                    "id": voice['Id'],
                    "name": voice['Name'],
                    "gender": voice['Gender'],
                    "language_code": voice['LanguageCode'],
                    "language_name": voice['LanguageName'],
                    "supported_engines": voice.get('SupportedEngines', [])
                }
                voices.append(voice_info)

            return voices

        except Exception as e:
            print(f"Failed to list voices: {str(e)}")
            return []

    def get_engine_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the engine.

        Returns:
            Dictionary with engine information
        """
        info = super().get_engine_info()
        info.update({
            "voice_id": self.voice_id,
            "engine_type": self.engine,
            "region": self.region_name,
            "output_format": self.output_format,
            "supports_ssml": True,
            "supports_lexicons": True,
            "cloud_based": True
        })
        return info
