"""
Tests for TTS engines.
"""

import pytest
import numpy as np
from src.engines.base import BaseTTSEngine, TTSEngineError
from src.configs import TTSConfig


class MockTTSEngine(BaseTTSEngine):
    """Mock TTS engine for testing."""

    def load_model(self):
        """Mock model loading."""
        self.initialized = True

    def synthesize(self, text: str, **kwargs) -> np.ndarray:
        """Mock synthesis."""
        # Return dummy audio
        duration = len(text) * 0.1
        samples = int(self.sample_rate * duration)
        return np.random.randn(samples).astype(np.float32) * 0.1


class TestBaseTTSEngine:
    """Tests for BaseTTSEngine class."""

    def test_engine_initialization(self):
        """Test engine initialization."""
        config = {"sample_rate": 22050, "language": "ko"}
        engine = MockTTSEngine(config=config)

        assert engine.sample_rate == 22050
        assert engine.language == "ko"
        assert engine.initialized is True

    def test_synthesize(self):
        """Test synthesis."""
        engine = MockTTSEngine()

        text = "테스트 텍스트"
        audio = engine.synthesize(text)

        assert isinstance(audio, np.ndarray)
        assert len(audio) > 0
        assert audio.dtype == np.float32

    def test_preprocess_text(self):
        """Test text preprocessing."""
        engine = MockTTSEngine()

        text = "  안녕하세요  "
        result = engine.preprocess_text(text)

        assert result == "안녕하세요"

    def test_postprocess_audio(self):
        """Test audio postprocessing."""
        engine = MockTTSEngine()

        # Create audio with high amplitude
        audio = np.ones(1000) * 2.0
        result = engine.postprocess_audio(audio)

        # Should be normalized
        assert np.abs(result).max() <= 1.0

    def test_get_engine_info(self):
        """Test getting engine info."""
        engine = MockTTSEngine(config={"language": "ko"})

        info = engine.get_engine_info()

        assert "engine_name" in info
        assert "sample_rate" in info
        assert "language" in info
        assert info["language"] == "ko"

    def test_save_audio(self, tmp_path):
        """Test saving audio to file."""
        engine = MockTTSEngine()

        audio = engine.synthesize("테스트")
        output_path = tmp_path / "test_output.wav"

        engine.save_audio(audio, str(output_path))

        assert output_path.exists()

    def test_audio_to_bytes(self):
        """Test converting audio to bytes."""
        engine = MockTTSEngine()

        audio = engine.synthesize("테스트")
        audio_bytes = engine.audio_to_bytes(audio)

        assert isinstance(audio_bytes, bytes)
        assert len(audio_bytes) > 0
