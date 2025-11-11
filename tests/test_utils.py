"""
Tests for utility modules.
"""

import pytest
import numpy as np
from src.utils import AudioUtils, AudioMetrics


class TestAudioUtils:
    """Tests for AudioUtils class."""

    @pytest.fixture
    def sample_audio(self):
        """Generate sample audio."""
        return np.random.randn(22050).astype(np.float32) * 0.5

    def test_normalize_audio(self, sample_audio):
        """Test audio normalization."""
        normalized = AudioUtils.normalize_audio(sample_audio, target_level=0.9)

        assert np.abs(normalized).max() <= 1.0
        assert np.abs(normalized).max() >= 0.85

    def test_save_and_load_audio(self, sample_audio, tmp_path):
        """Test saving and loading audio."""
        file_path = tmp_path / "test.wav"

        # Save
        AudioUtils.save_audio(sample_audio, str(file_path), sample_rate=22050)
        assert file_path.exists()

        # Load
        loaded_audio, sr = AudioUtils.load_audio(str(file_path))

        assert sr == 22050
        assert len(loaded_audio) == len(sample_audio)

    def test_concatenate_audio(self):
        """Test audio concatenation."""
        audio1 = np.ones(1000, dtype=np.float32) * 0.1
        audio2 = np.ones(1000, dtype=np.float32) * 0.2
        audio3 = np.ones(1000, dtype=np.float32) * 0.3

        concatenated = AudioUtils.concatenate_audio(
            [audio1, audio2, audio3],
            silence_duration=0.1,
            sample_rate=22050
        )

        # Should be longer than sum due to silence
        total_samples = 3000 + 2 * int(0.1 * 22050)
        assert len(concatenated) == total_samples

    def test_get_audio_duration(self, sample_audio):
        """Test getting audio duration."""
        duration = AudioUtils.get_audio_duration(sample_audio, sample_rate=22050)

        expected_duration = len(sample_audio) / 22050
        assert abs(duration - expected_duration) < 0.01

    def test_convert_to_stereo(self, sample_audio):
        """Test converting to stereo."""
        stereo = AudioUtils.convert_to_stereo(sample_audio)

        assert stereo.shape == (len(sample_audio), 2)

    def test_apply_fade(self, sample_audio):
        """Test applying fade in/out."""
        faded = AudioUtils.apply_fade(
            sample_audio,
            fade_in_duration=0.1,
            fade_out_duration=0.1,
            sample_rate=22050
        )

        assert len(faded) == len(sample_audio)
        # First sample should be close to 0 (faded in)
        assert abs(faded[0]) < abs(sample_audio[0])


class TestAudioMetrics:
    """Tests for AudioMetrics class."""

    @pytest.fixture
    def sample_audio(self):
        """Generate sample audio."""
        return np.random.randn(22050).astype(np.float32) * 0.5

    def test_calculate_rms(self, sample_audio):
        """Test RMS calculation."""
        rms = AudioMetrics.calculate_rms(sample_audio)

        assert isinstance(rms, float)
        assert rms > 0

    def test_calculate_peak_amplitude(self, sample_audio):
        """Test peak amplitude calculation."""
        peak = AudioMetrics.calculate_peak_amplitude(sample_audio)

        assert isinstance(peak, float)
        assert peak > 0
        assert peak <= 1.0

    def test_calculate_zero_crossing_rate(self, sample_audio):
        """Test zero crossing rate calculation."""
        zcr = AudioMetrics.calculate_zero_crossing_rate(sample_audio)

        assert isinstance(zcr, float)
        assert 0 <= zcr <= 1

    def test_calculate_snr(self, sample_audio):
        """Test SNR calculation."""
        snr = AudioMetrics.calculate_snr(sample_audio)

        assert isinstance(snr, float)

    def test_calculate_all_metrics(self, sample_audio):
        """Test calculating all metrics."""
        metrics = AudioMetrics.calculate_all_metrics(sample_audio, sample_rate=22050)

        assert isinstance(metrics, dict)
        assert "rms" in metrics
        assert "peak_amplitude" in metrics
        assert "zero_crossing_rate" in metrics
        assert "snr" in metrics
