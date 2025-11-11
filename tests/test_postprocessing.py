"""
Tests for audio postprocessing modules.
"""

import pytest
import numpy as np
from src.postprocessing import AudioEnhancer, NoiseReducer


class TestAudioEnhancer:
    """Tests for AudioEnhancer class."""

    @pytest.fixture
    def sample_audio(self):
        """Generate sample audio."""
        return np.random.randn(22050).astype(np.float32) * 0.5

    def test_normalize_audio(self, sample_audio):
        """Test audio normalization."""
        enhancer = AudioEnhancer(sample_rate=22050)

        normalized = enhancer.normalize_audio(sample_audio, target_level=0.9)

        assert np.abs(normalized).max() <= 1.0
        assert np.abs(normalized).max() >= 0.85  # Close to target

    def test_enhance_audio(self, sample_audio):
        """Test audio enhancement."""
        enhancer = AudioEnhancer(sample_rate=22050)

        enhanced = enhancer.enhance(sample_audio, normalize=True)

        assert isinstance(enhanced, np.ndarray)
        assert len(enhanced) == len(sample_audio)
        assert np.abs(enhanced).max() <= 1.0

    def test_apply_compression(self, sample_audio):
        """Test dynamic range compression."""
        enhancer = AudioEnhancer(sample_rate=22050)

        # Create audio with high peaks
        audio = sample_audio.copy()
        audio[100:110] = 0.9

        compressed = enhancer.apply_compression(audio, threshold=0.5, ratio=4.0)

        assert isinstance(compressed, np.ndarray)
        assert len(compressed) == len(audio)

    def test_trim_silence(self, sample_audio):
        """Test silence trimming."""
        enhancer = AudioEnhancer(sample_rate=22050)

        # Add silence at beginning and end
        silence = np.zeros(1000, dtype=np.float32)
        audio_with_silence = np.concatenate([silence, sample_audio, silence])

        trimmed = enhancer.trim_silence(audio_with_silence, threshold_db=-40.0)

        # Trimmed should be shorter
        assert len(trimmed) <= len(audio_with_silence)


class TestNoiseReducer:
    """Tests for NoiseReducer class."""

    @pytest.fixture
    def sample_audio(self):
        """Generate sample audio with noise."""
        signal = np.sin(2 * np.pi * 440 * np.arange(22050) / 22050)
        noise = np.random.randn(22050) * 0.05
        return (signal + noise).astype(np.float32)

    def test_reduce_noise(self, sample_audio):
        """Test noise reduction."""
        reducer = NoiseReducer(sample_rate=22050)

        reduced = reducer.reduce_noise(sample_audio, stationary=True)

        assert isinstance(reduced, np.ndarray)
        assert len(reduced) == len(sample_audio)

    def test_wiener_filter(self, sample_audio):
        """Test Wiener filtering."""
        reducer = NoiseReducer(sample_rate=22050)

        filtered = reducer.wiener_filter(sample_audio)

        assert isinstance(filtered, np.ndarray)
        assert len(filtered) == len(sample_audio)
