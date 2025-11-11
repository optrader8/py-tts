"""
Tests for configuration module.
"""

import pytest
from src.configs import TTSConfig, get_default_config


class TestTTSConfig:
    """Tests for TTSConfig class."""

    def test_default_config(self):
        """Test default configuration."""
        config = TTSConfig()

        assert config.engine == "coqui"
        assert config.language == "ko"
        assert config.sample_rate == 22050
        assert config.speed == 1.0

    def test_custom_config(self):
        """Test custom configuration."""
        config = TTSConfig(
            engine="google",
            language="en",
            sample_rate=16000,
            speed=1.2
        )

        assert config.engine == "google"
        assert config.language == "en"
        assert config.sample_rate == 16000
        assert config.speed == 1.2

    def test_to_dict(self):
        """Test converting config to dictionary."""
        config = TTSConfig(engine="azure", language="ko")
        config_dict = config.to_dict()

        assert isinstance(config_dict, dict)
        assert config_dict["engine"] == "azure"
        assert config_dict["language"] == "ko"

    def test_from_dict(self):
        """Test creating config from dictionary."""
        config_dict = {
            "engine": "polly",
            "language": "en",
            "speed": 0.9,
            "pitch": 2.0
        }

        config = TTSConfig.from_dict(config_dict)

        assert config.engine == "polly"
        assert config.language == "en"
        assert config.speed == 0.9
        assert config.pitch == 2.0

    def test_get_default_config(self):
        """Test getting default config for engine."""
        config = get_default_config(engine="coqui")

        assert config.engine == "coqui"
        assert isinstance(config, TTSConfig)
