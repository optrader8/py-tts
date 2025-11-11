"""
Audio Utilities
Helper functions for audio processing.
"""

import numpy as np
from typing import Optional, Tuple
import soundfile as sf
from pathlib import Path


class AudioUtils:
    """
    Utility functions for audio operations.
    """

    @staticmethod
    def load_audio(file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio from file.

        Args:
            file_path: Path to audio file

        Returns:
            Tuple of (audio data, sample rate)
        """
        audio, sr = sf.read(file_path)

        # Convert to mono if stereo
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        # Convert to float32
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)

        return audio, sr

    @staticmethod
    def save_audio(
        audio: np.ndarray,
        file_path: str,
        sample_rate: int = 22050
    ) -> None:
        """
        Save audio to file.

        Args:
            audio: Audio data
            file_path: Output file path
            sample_rate: Sample rate
        """
        # Create parent directory if it doesn't exist
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Save audio
        sf.write(file_path, audio, sample_rate)

    @staticmethod
    def resample_audio(
        audio: np.ndarray,
        orig_sr: int,
        target_sr: int
    ) -> np.ndarray:
        """
        Resample audio to different sample rate.

        Args:
            audio: Input audio
            orig_sr: Original sample rate
            target_sr: Target sample rate

        Returns:
            Resampled audio
        """
        if orig_sr == target_sr:
            return audio

        try:
            import librosa
            return librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)
        except ImportError:
            print("Warning: librosa not available for resampling")
            return audio

    @staticmethod
    def normalize_audio(
        audio: np.ndarray,
        target_level: float = 0.95
    ) -> np.ndarray:
        """
        Normalize audio to target level.

        Args:
            audio: Input audio
            target_level: Target peak level

        Returns:
            Normalized audio
        """
        max_val = np.abs(audio).max()

        if max_val > 0:
            audio = audio / max_val * target_level

        return audio

    @staticmethod
    def concatenate_audio(
        audio_list: list,
        silence_duration: float = 0.5,
        sample_rate: int = 22050
    ) -> np.ndarray:
        """
        Concatenate multiple audio segments with silence between them.

        Args:
            audio_list: List of audio arrays
            silence_duration: Duration of silence between segments (seconds)
            sample_rate: Sample rate

        Returns:
            Concatenated audio
        """
        silence_samples = int(silence_duration * sample_rate)
        silence = np.zeros(silence_samples, dtype=np.float32)

        result = []
        for i, audio in enumerate(audio_list):
            result.append(audio)
            if i < len(audio_list) - 1:
                result.append(silence)

        return np.concatenate(result)

    @staticmethod
    def split_audio_by_silence(
        audio: np.ndarray,
        sample_rate: int = 22050,
        threshold_db: float = -40.0
    ) -> list:
        """
        Split audio by silence.

        Args:
            audio: Input audio
            sample_rate: Sample rate
            threshold_db: Silence threshold in dB

        Returns:
            List of audio segments
        """
        try:
            import librosa

            # Split on silence
            intervals = librosa.effects.split(audio, top_db=-threshold_db)

            # Extract segments
            segments = [audio[start:end] for start, end in intervals]

            return segments

        except ImportError:
            print("Warning: librosa not available for splitting")
            return [audio]

    @staticmethod
    def get_audio_duration(audio: np.ndarray, sample_rate: int) -> float:
        """
        Get audio duration in seconds.

        Args:
            audio: Audio data
            sample_rate: Sample rate

        Returns:
            Duration in seconds
        """
        return len(audio) / sample_rate

    @staticmethod
    def convert_to_stereo(audio: np.ndarray) -> np.ndarray:
        """
        Convert mono audio to stereo.

        Args:
            audio: Mono audio

        Returns:
            Stereo audio
        """
        return np.stack([audio, audio], axis=1)

    @staticmethod
    def apply_fade(
        audio: np.ndarray,
        fade_in_duration: float = 0.1,
        fade_out_duration: float = 0.1,
        sample_rate: int = 22050
    ) -> np.ndarray:
        """
        Apply fade in/out to audio.

        Args:
            audio: Input audio
            fade_in_duration: Fade in duration (seconds)
            fade_out_duration: Fade out duration (seconds)
            sample_rate: Sample rate

        Returns:
            Audio with fade
        """
        fade_in_samples = int(fade_in_duration * sample_rate)
        fade_out_samples = int(fade_out_duration * sample_rate)

        # Apply fade in
        if fade_in_samples > 0:
            fade_in = np.linspace(0, 1, fade_in_samples)
            audio[:fade_in_samples] *= fade_in

        # Apply fade out
        if fade_out_samples > 0:
            fade_out = np.linspace(1, 0, fade_out_samples)
            audio[-fade_out_samples:] *= fade_out

        return audio
