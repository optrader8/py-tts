"""
Integration tests for TTS system.
"""

import pytest
import numpy as np
from src.tts_engine import TTSEngine, create_tts_engine
from src.configs import TTSConfig


class TestTTSEngineIntegration:
    """Integration tests for TTSEngine."""

    def test_create_engine_with_mock(self):
        """Test creating TTS engine."""
        # Note: This will try to load Coqui TTS
        # In CI/CD, you may want to mock this
        config = TTSConfig(
            engine="coqui",
            language="ko",
            normalize_text=True,
            enhance_audio=False  # Disable to speed up tests
        )

        try:
            engine = TTSEngine(config=config)
            assert engine is not None
            assert engine.engine_name == "coqui"
        except Exception as e:
            # If Coqui TTS is not installed, skip
            pytest.skip(f"Coqui TTS not available: {e}")

    def test_list_engines(self):
        """Test listing available engines."""
        engines = TTSEngine.list_engines()

        assert isinstance(engines, list)
        assert len(engines) > 0
        assert "coqui" in engines
        assert "google" in engines

    def test_create_tts_engine_convenience(self):
        """Test convenience function."""
        try:
            engine = create_tts_engine(engine="coqui", language="ko")
            assert engine is not None
        except Exception:
            pytest.skip("Coqui TTS not available")

    def test_preprocessing_pipeline(self):
        """Test text preprocessing pipeline."""
        from src.preprocessing import TextNormalizer
        from src.preprocessing.korean_processor import KoreanProcessor

        normalizer = TextNormalizer(language="ko")
        processor = KoreanProcessor()

        text = "전화번호는 010-1234-5678입니다."

        # Normalize
        normalized = normalizer.normalize(text)
        assert isinstance(normalized, str)

        # Process
        processed = processor.process(normalized)
        assert isinstance(processed, str)

    def test_postprocessing_pipeline(self):
        """Test audio postprocessing pipeline."""
        from src.postprocessing import AudioEnhancer, NoiseReducer

        # Generate sample audio
        audio = np.random.randn(22050).astype(np.float32) * 0.5

        # Enhance
        enhancer = AudioEnhancer(sample_rate=22050)
        enhanced = enhancer.enhance(audio, normalize=True)

        assert isinstance(enhanced, np.ndarray)
        assert len(enhanced) == len(audio)

        # Reduce noise
        reducer = NoiseReducer(sample_rate=22050)
        cleaned = reducer.reduce_noise(enhanced)

        assert isinstance(cleaned, np.ndarray)

    def test_end_to_end_mock(self):
        """Test end-to-end synthesis with mock engine."""
        from src.engines.base import BaseTTSEngine

        class SimpleMockEngine(BaseTTSEngine):
            def load_model(self):
                self.initialized = True

            def synthesize(self, text: str, **kwargs) -> np.ndarray:
                samples = int(self.sample_rate * 1.0)  # 1 second
                return np.random.randn(samples).astype(np.float32) * 0.1

        # Temporarily add mock engine
        from src import tts_engine as tts_module
        original_engines = tts_module.TTSEngine.ENGINES.copy()
        tts_module.TTSEngine.ENGINES["mock"] = SimpleMockEngine

        try:
            # Create engine
            config = TTSConfig(
                engine="mock",
                language="ko",
                normalize_text=True,
                enhance_audio=True
            )

            engine = TTSEngine(config=config)

            # Synthesize
            text = "테스트 텍스트입니다."
            audio = engine.synthesize(text)

            assert isinstance(audio, np.ndarray)
            assert len(audio) > 0
            assert audio.dtype == np.float32

        finally:
            # Restore original engines
            tts_module.TTSEngine.ENGINES = original_engines
