"""
Main TTS Engine
Unified interface for all TTS engines.
"""

from typing import Optional, Dict, Any, Union
import numpy as np
from pathlib import Path

from .configs import TTSConfig
from .engines.base import BaseTTSEngine, TTSInitializationError
from .engines.coqui_tts import CoquiTTSEngine
from .engines.google_tts import GoogleTTSEngine
from .engines.azure_tts import AzureTTSEngine
from .engines.polly_tts import PollyTTSEngine
from .engines.piper_tts import PiperTTSEngine

from .preprocessing import TextNormalizer, PhonemeConverter
from .preprocessing.korean_processor import KoreanProcessor
from .postprocessing import AudioEnhancer, NoiseReducer
from .llm_integration import ContextAnalyzer, EmotionDetector


class TTSEngine:
    """
    Main TTS Engine with unified interface.
    Supports multiple backends and advanced features.
    """

    # Engine registry
    ENGINES = {
        "coqui": CoquiTTSEngine,
        "google": GoogleTTSEngine,
        "azure": AzureTTSEngine,
        "polly": PollyTTSEngine,
        "piper": PiperTTSEngine,
    }

    def __init__(
        self,
        engine: str = "coqui",
        config: Optional[Union[TTSConfig, Dict[str, Any]]] = None
    ):
        """
        Initialize TTS Engine.

        Args:
            engine: Engine name ('coqui', 'google', 'azure', 'polly', 'piper')
            config: Configuration (TTSConfig or dict)
        """
        # Parse config
        if config is None:
            self.config = TTSConfig(engine=engine)
        elif isinstance(config, dict):
            self.config = TTSConfig.from_dict(config)
        else:
            self.config = config

        # Update engine from config
        self.engine_name = self.config.engine

        # Initialize engine
        self.engine = self._create_engine()

        # Initialize processors
        self.text_normalizer = TextNormalizer(language=self.config.language)
        self.phoneme_converter = PhonemeConverter(language=self.config.language)
        self.korean_processor = KoreanProcessor() if self.config.language == "ko" else None

        # Initialize postprocessors
        self.audio_enhancer = AudioEnhancer(sample_rate=self.config.sample_rate)
        self.noise_reducer = NoiseReducer(sample_rate=self.config.sample_rate)

        # Initialize LLM integration
        self.context_analyzer = None
        self.emotion_detector = None

        if self.config.use_llm_context:
            self.context_analyzer = ContextAnalyzer()
            self.emotion_detector = EmotionDetector()

        print(f"TTS Engine initialized: {self.engine_name}")

    def _create_engine(self) -> BaseTTSEngine:
        """
        Create the TTS engine instance.

        Returns:
            TTS engine instance
        """
        engine_class = self.ENGINES.get(self.engine_name)

        if engine_class is None:
            raise TTSInitializationError(
                f"Unknown engine: {self.engine_name}. "
                f"Available engines: {list(self.ENGINES.keys())}"
            )

        # Prepare engine config
        engine_config = self.config.to_dict()

        try:
            return engine_class(config=engine_config)
        except Exception as e:
            raise TTSInitializationError(
                f"Failed to initialize {self.engine_name} engine: {str(e)}"
            )

    def synthesize(
        self,
        text: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> np.ndarray:
        """
        Synthesize speech from text.

        Args:
            text: Input text
            output_path: Optional output file path
            **kwargs: Additional parameters

        Returns:
            Audio data as numpy array
        """
        # Preprocess text
        if self.config.normalize_text:
            text = self._preprocess_text(text)

        # Analyze context with LLM if enabled
        prosody_params = {}
        if self.config.use_llm_context and self.context_analyzer:
            analysis = self.context_analyzer.analyze(text)
            prosody_params = self.context_analyzer.get_prosody_params(analysis)

        # Merge prosody params with kwargs
        synthesis_params = {
            "speed": prosody_params.get("rate", self.config.speed),
            "pitch": prosody_params.get("pitch", self.config.pitch),
            **kwargs
        }

        # Synthesize audio
        audio = self.engine.synthesize(text, **synthesis_params)

        # Postprocess audio
        if self.config.enhance_audio or self.config.reduce_noise:
            audio = self._postprocess_audio(audio)

        # Save if output path provided
        if output_path:
            self.save_audio(audio, output_path)

        return audio

    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text before synthesis.

        Args:
            text: Input text

        Returns:
            Preprocessed text
        """
        # Normalize text
        text = self.text_normalizer.normalize(text)

        # Korean-specific processing
        if self.korean_processor:
            text = self.korean_processor.process(text)

        # Phoneme conversion if enabled
        if self.config.use_phoneme_conversion:
            text = self.phoneme_converter.convert(text)

        return text

    def _postprocess_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Postprocess audio after synthesis.

        Args:
            audio: Input audio

        Returns:
            Postprocessed audio
        """
        # Noise reduction
        if self.config.reduce_noise:
            audio = self.noise_reducer.reduce_noise(audio)

        # Audio enhancement
        if self.config.enhance_audio:
            audio = self.audio_enhancer.enhance(
                audio,
                normalize=True,
                denoise=self.config.reduce_noise
            )

        return audio

    def save_audio(
        self,
        audio: np.ndarray,
        output_path: str,
        sample_rate: Optional[int] = None
    ) -> None:
        """
        Save audio to file.

        Args:
            audio: Audio data
            output_path: Output file path
            sample_rate: Sample rate (uses engine's rate if not provided)
        """
        sample_rate = sample_rate or self.config.sample_rate
        self.engine.save_audio(audio, output_path, sample_rate)

    def synthesize_batch(
        self,
        texts: list,
        output_dir: Optional[str] = None,
        **kwargs
    ) -> list:
        """
        Synthesize multiple texts.

        Args:
            texts: List of texts
            output_dir: Optional output directory
            **kwargs: Additional parameters

        Returns:
            List of audio arrays
        """
        results = []

        for i, text in enumerate(texts):
            output_path = None
            if output_dir:
                output_path = str(Path(output_dir) / f"audio_{i:03d}.wav")

            audio = self.synthesize(text, output_path, **kwargs)
            results.append(audio)

        return results

    def get_engine_info(self) -> Dict[str, Any]:
        """
        Get information about the current engine.

        Returns:
            Engine information dictionary
        """
        info = self.engine.get_engine_info()
        info.update({
            "config": self.config.to_dict(),
            "llm_enabled": self.config.use_llm_context,
            "preprocessing_enabled": self.config.normalize_text,
            "postprocessing_enabled": self.config.enhance_audio or self.config.reduce_noise
        })
        return info

    def list_available_voices(self) -> list:
        """
        List available voices for current engine.

        Returns:
            List of voice information
        """
        if hasattr(self.engine, 'list_voices'):
            return self.engine.list_voices()
        elif hasattr(self.engine, 'get_available_speakers'):
            return self.engine.get_available_speakers()
        else:
            print(f"Voice listing not supported for {self.engine_name}")
            return []

    def set_voice(self, voice_name: str) -> None:
        """
        Set voice for synthesis.

        Args:
            voice_name: Voice name or ID
        """
        self.config.voice_name = voice_name

        # Update engine config if supported
        if hasattr(self.engine, 'voice_name'):
            self.engine.voice_name = voice_name

    def set_language(self, language: str) -> None:
        """
        Set language for synthesis.

        Args:
            language: Language code
        """
        self.config.language = language
        self.engine.language = language

        # Reinitialize processors
        self.text_normalizer = TextNormalizer(language=language)
        self.phoneme_converter = PhonemeConverter(language=language)

    @classmethod
    def list_engines(cls) -> list:
        """
        List available engines.

        Returns:
            List of engine names
        """
        return list(cls.ENGINES.keys())


# Convenience function
def create_tts_engine(
    engine: str = "coqui",
    **kwargs
) -> TTSEngine:
    """
    Create a TTS engine with simple configuration.

    Args:
        engine: Engine name
        **kwargs: Configuration parameters

    Returns:
        TTSEngine instance
    """
    config = TTSConfig(engine=engine, **kwargs)
    return TTSEngine(engine=engine, config=config)
