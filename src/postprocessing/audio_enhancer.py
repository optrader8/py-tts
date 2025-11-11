"""
Audio Enhancer
Enhances audio quality through various processing techniques.
"""

import numpy as np
from typing import Optional


class AudioEnhancer:
    """
    Enhances audio quality for TTS output.
    Includes normalization, equalization, and dynamic range processing.
    """

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize audio enhancer.

        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate

    def enhance(
        self,
        audio: np.ndarray,
        normalize: bool = True,
        denoise: bool = False,
        enhance_bass: bool = False,
        enhance_treble: bool = False
    ) -> np.ndarray:
        """
        Enhance audio quality.

        Args:
            audio: Input audio array
            normalize: Apply normalization
            denoise: Apply denoising
            enhance_bass: Enhance bass frequencies
            enhance_treble: Enhance treble frequencies

        Returns:
            Enhanced audio array
        """
        result = audio.copy()

        if normalize:
            result = self.normalize_audio(result)

        if denoise:
            result = self.denoise_audio(result)

        if enhance_bass or enhance_treble:
            result = self.equalize_audio(result, enhance_bass, enhance_treble)

        return result

    def normalize_audio(
        self,
        audio: np.ndarray,
        target_level: float = 0.95
    ) -> np.ndarray:
        """
        Normalize audio to target level.

        Args:
            audio: Input audio
            target_level: Target peak level (0.0-1.0)

        Returns:
            Normalized audio
        """
        max_val = np.abs(audio).max()

        if max_val > 0:
            audio = audio / max_val * target_level

        return audio

    def denoise_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply denoising to audio.

        Args:
            audio: Input audio

        Returns:
            Denoised audio
        """
        try:
            import noisereduce as nr
            # Apply noise reduction
            reduced_noise = nr.reduce_noise(
                y=audio,
                sr=self.sample_rate,
                stationary=True
            )
            return reduced_noise
        except ImportError:
            print("Warning: noisereduce not installed. Skipping denoising.")
            return audio
        except Exception as e:
            print(f"Warning: Denoising failed: {e}")
            return audio

    def equalize_audio(
        self,
        audio: np.ndarray,
        enhance_bass: bool = False,
        enhance_treble: bool = False
    ) -> np.ndarray:
        """
        Apply equalization to audio.

        Args:
            audio: Input audio
            enhance_bass: Enhance bass frequencies
            enhance_treble: Enhance treble frequencies

        Returns:
            Equalized audio
        """
        try:
            from scipy import signal

            # Simple EQ using filters
            if enhance_bass:
                # Low-pass emphasis
                sos = signal.butter(2, 500, 'lowpass', fs=self.sample_rate, output='sos')
                bass = signal.sosfilt(sos, audio)
                audio = audio + bass * 0.1

            if enhance_treble:
                # High-pass emphasis
                sos = signal.butter(2, 3000, 'highpass', fs=self.sample_rate, output='sos')
                treble = signal.sosfilt(sos, audio)
                audio = audio + treble * 0.1

            # Normalize after EQ
            audio = self.normalize_audio(audio)

            return audio

        except ImportError:
            print("Warning: scipy not available for EQ")
            return audio
        except Exception as e:
            print(f"Warning: Equalization failed: {e}")
            return audio

    def apply_compression(
        self,
        audio: np.ndarray,
        threshold: float = 0.5,
        ratio: float = 4.0
    ) -> np.ndarray:
        """
        Apply dynamic range compression.

        Args:
            audio: Input audio
            threshold: Compression threshold (0.0-1.0)
            ratio: Compression ratio

        Returns:
            Compressed audio
        """
        # Simple compression
        compressed = audio.copy()

        # Find samples above threshold
        above_threshold = np.abs(compressed) > threshold

        # Apply compression to samples above threshold
        compressed[above_threshold] = (
            np.sign(compressed[above_threshold]) * threshold +
            (np.abs(compressed[above_threshold]) - threshold) / ratio
        )

        return compressed

    def apply_reverb(
        self,
        audio: np.ndarray,
        room_size: float = 0.5,
        damping: float = 0.5
    ) -> np.ndarray:
        """
        Apply reverb effect (placeholder).

        Args:
            audio: Input audio
            room_size: Room size parameter (0.0-1.0)
            damping: Damping parameter (0.0-1.0)

        Returns:
            Audio with reverb
        """
        try:
            from pedalboard import Reverb
            import soundfile as sf

            # Apply reverb using pedalboard
            reverb = Reverb(room_size=room_size, damping=damping)
            processed = reverb(audio, self.sample_rate)

            return processed

        except ImportError:
            print("Warning: pedalboard not installed for reverb")
            return audio
        except Exception as e:
            print(f"Warning: Reverb failed: {e}")
            return audio

    def adjust_speed(
        self,
        audio: np.ndarray,
        speed: float = 1.0
    ) -> np.ndarray:
        """
        Adjust audio speed without changing pitch.

        Args:
            audio: Input audio
            speed: Speed multiplier (1.0 = normal, >1.0 = faster, <1.0 = slower)

        Returns:
            Speed-adjusted audio
        """
        if speed == 1.0:
            return audio

        try:
            import librosa
            return librosa.effects.time_stretch(audio, rate=speed)
        except ImportError:
            print("Warning: librosa not available for speed adjustment")
            return audio
        except Exception as e:
            print(f"Warning: Speed adjustment failed: {e}")
            return audio

    def adjust_pitch(
        self,
        audio: np.ndarray,
        n_steps: float = 0.0
    ) -> np.ndarray:
        """
        Adjust audio pitch without changing speed.

        Args:
            audio: Input audio
            n_steps: Number of semitones to shift

        Returns:
            Pitch-adjusted audio
        """
        if n_steps == 0.0:
            return audio

        try:
            import librosa
            return librosa.effects.pitch_shift(
                audio,
                sr=self.sample_rate,
                n_steps=n_steps
            )
        except ImportError:
            print("Warning: librosa not available for pitch adjustment")
            return audio
        except Exception as e:
            print(f"Warning: Pitch adjustment failed: {e}")
            return audio

    def trim_silence(
        self,
        audio: np.ndarray,
        threshold_db: float = -40.0
    ) -> np.ndarray:
        """
        Trim silence from beginning and end of audio.

        Args:
            audio: Input audio
            threshold_db: Silence threshold in dB

        Returns:
            Trimmed audio
        """
        try:
            import librosa
            trimmed, _ = librosa.effects.trim(
                audio,
                top_db=-threshold_db
            )
            return trimmed
        except ImportError:
            print("Warning: librosa not available for trimming")
            return audio
        except Exception as e:
            print(f"Warning: Trimming failed: {e}")
            return audio
