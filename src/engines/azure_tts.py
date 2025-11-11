"""
Microsoft Azure Cognitive Services Speech TTS Engine
Custom neural voice support with high-quality synthesis.
"""

from typing import Optional, Dict, Any, List
import numpy as np
import os
from .base import BaseTTSEngine, TTSInitializationError, TTSSynthesisError


class AzureTTSEngine(BaseTTSEngine):
    """
    Microsoft Azure Text-to-Speech Engine implementation.
    Requires Azure Speech Service credentials.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Azure TTS Engine.

        Args:
            config: Configuration dictionary
                - subscription_key: Azure subscription key
                - region: Azure region (e.g., 'eastus')
                - voice_name: Voice name (e.g., 'ko-KR-SunHiNeural')
                - speaking_rate: Speaking rate adjustment
                - pitch: Pitch adjustment
                - style: Speaking style (e.g., 'cheerful', 'sad')
        """
        super().__init__(config)

        self.subscription_key = self.config.get(
            "subscription_key",
            os.getenv("AZURE_SPEECH_KEY")
        )
        self.region = self.config.get(
            "region",
            os.getenv("AZURE_SPEECH_REGION", "eastus")
        )
        self.voice_name = self.config.get("voice_name", "ko-KR-SunHiNeural")
        self.speaking_rate = self.config.get("speaking_rate", 1.0)
        self.pitch = self.config.get("pitch", 0)
        self.style = self.config.get("style", None)

        self.speech_config = None
        self.synthesizer = None

        self.load_model()

    def load_model(self) -> None:
        """
        Initialize Azure Speech synthesizer.
        """
        try:
            import azure.cognitiveservices.speech as speechsdk

            if not self.subscription_key:
                raise TTSInitializationError(
                    "Azure subscription key not provided. Set AZURE_SPEECH_KEY environment variable."
                )

            # Create speech config
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.subscription_key,
                region=self.region
            )

            # Set the voice name
            self.speech_config.speech_synthesis_voice_name = self.voice_name

            # Set output format to raw audio
            self.speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Raw24Khz16BitMonoPcm
            )

            # Create synthesizer
            self.synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=None  # Use in-memory result
            )

            self.speechsdk = speechsdk
            self.sample_rate = 24000  # Azure default for Raw24Khz16BitMonoPcm

            self.initialized = True
            print("Azure TTS initialized successfully")
            print(f"Voice: {self.voice_name}, Region: {self.region}")

        except ImportError:
            raise TTSInitializationError(
                "Azure Speech SDK not installed. Install with: pip install azure-cognitiveservices-speech"
            )
        except Exception as e:
            raise TTSInitializationError(f"Failed to initialize Azure TTS: {str(e)}")

    def synthesize(
        self,
        text: str,
        voice_name: Optional[str] = None,
        language: Optional[str] = None,
        speaking_rate: Optional[float] = None,
        pitch: Optional[int] = None,
        style: Optional[str] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from text.

        Args:
            text: Input text to synthesize
            voice_name: Voice name (e.g., 'ko-KR-SunHiNeural')
            language: Language code (auto-detected from voice)
            speaking_rate: Speaking rate (0.5-2.0)
            pitch: Pitch adjustment (-50 to +50 Hz)
            style: Speaking style (e.g., 'cheerful', 'sad')
            **kwargs: Additional parameters

        Returns:
            Audio data as numpy array
        """
        if not self.initialized:
            raise TTSSynthesisError("Azure TTS not initialized.")

        # Preprocess text
        text = self.preprocess_text(text)

        # Set parameters
        voice_name = voice_name or self.voice_name
        speaking_rate = speaking_rate or self.speaking_rate
        pitch = pitch or self.pitch
        style = style or self.style

        # Build SSML
        ssml = self._build_ssml(text, voice_name, speaking_rate, pitch, style)

        try:
            # Synthesize speech
            result = self.synthesizer.speak_ssml_async(ssml).get()

            # Check result
            if result.reason == self.speechsdk.ResultReason.SynthesizingAudioCompleted:
                # Convert audio data to numpy array
                audio = self._bytes_to_array(result.audio_data)
                audio = self.postprocess_audio(audio)
                return audio
            elif result.reason == self.speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                raise TTSSynthesisError(
                    f"Speech synthesis canceled: {cancellation.reason}\n"
                    f"Error details: {cancellation.error_details}"
                )
            else:
                raise TTSSynthesisError(f"Unexpected result reason: {result.reason}")

        except Exception as e:
            raise TTSSynthesisError(f"Azure TTS synthesis failed: {str(e)}")

    def _build_ssml(
        self,
        text: str,
        voice_name: str,
        speaking_rate: float,
        pitch: int,
        style: Optional[str]
    ) -> str:
        """
        Build SSML from parameters.

        Args:
            text: Text content
            voice_name: Voice name
            speaking_rate: Speaking rate
            pitch: Pitch adjustment
            style: Speaking style

        Returns:
            SSML string
        """
        # Adjust speaking rate for SSML (convert to percentage)
        rate_str = f"{int((speaking_rate - 1.0) * 100)}%"
        if speaking_rate >= 1.0:
            rate_str = f"+{rate_str}"

        # Adjust pitch for SSML
        pitch_str = f"{pitch:+d}Hz" if pitch != 0 else "0Hz"

        ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
                   xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="ko-KR">
            <voice name="{voice_name}">"""

        # Add style if supported
        if style:
            ssml += f'<mstts:express-as style="{style}">'

        ssml += f"""
                <prosody rate="{rate_str}" pitch="{pitch_str}">
                    {text}
                </prosody>"""

        if style:
            ssml += "</mstts:express-as>"

        ssml += """
            </voice>
        </speak>"""

        return ssml

    def _bytes_to_array(self, audio_bytes: bytes) -> np.ndarray:
        """
        Convert audio bytes to numpy array.

        Args:
            audio_bytes: Raw PCM audio data

        Returns:
            Audio data as numpy array
        """
        # Azure returns 16-bit PCM
        audio = np.frombuffer(audio_bytes, dtype=np.int16)
        # Convert to float32 and normalize
        audio = audio.astype(np.float32) / 32768.0
        return audio

    def synthesize_ssml(
        self,
        ssml: str,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from custom SSML.

        Args:
            ssml: SSML string
            **kwargs: Additional parameters

        Returns:
            Audio data as numpy array
        """
        if not self.initialized:
            raise TTSSynthesisError("Azure TTS not initialized.")

        try:
            result = self.synthesizer.speak_ssml_async(ssml).get()

            if result.reason == self.speechsdk.ResultReason.SynthesizingAudioCompleted:
                audio = self._bytes_to_array(result.audio_data)
                audio = self.postprocess_audio(audio)
                return audio
            else:
                raise TTSSynthesisError(f"SSML synthesis failed: {result.reason}")

        except Exception as e:
            raise TTSSynthesisError(f"Azure TTS SSML synthesis failed: {str(e)}")

    def list_voices(self, locale: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available voices.

        Args:
            locale: Filter by locale (e.g., 'ko-KR')

        Returns:
            List of voice information dictionaries
        """
        if not self.initialized:
            return []

        try:
            result = self.synthesizer.get_voices_async(locale).get()

            if result.reason == self.speechsdk.ResultReason.VoicesListRetrieved:
                voices = []
                for voice in result.voices:
                    voice_info = {
                        "name": voice.name,
                        "short_name": voice.short_name,
                        "gender": voice.gender.name,
                        "locale": voice.locale,
                        "local_name": voice.local_name,
                        "style_list": voice.style_list if hasattr(voice, 'style_list') else []
                    }
                    voices.append(voice_info)
                return voices
            else:
                print(f"Failed to list voices: {result.reason}")
                return []

        except Exception as e:
            print(f"Error listing voices: {str(e)}")
            return []

    def get_engine_info(self) -> Dict[str, Any]:
        """
        Get detailed information about the engine.

        Returns:
            Dictionary with engine information
        """
        info = super().get_engine_info()
        info.update({
            "voice_name": self.voice_name,
            "region": self.region,
            "speaking_rate": self.speaking_rate,
            "pitch": self.pitch,
            "style": self.style,
            "supports_ssml": True,
            "supports_styles": True,
            "cloud_based": True
        })
        return info
