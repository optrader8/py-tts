"""
Noise Reduction
Advanced noise reduction techniques for audio.
"""

import numpy as np
from typing import Optional


class NoiseReducer:
    """
    Noise reduction for TTS audio output.
    """

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize noise reducer.

        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate

    def reduce_noise(
        self,
        audio: np.ndarray,
        noise_profile: Optional[np.ndarray] = None,
        stationary: bool = True
    ) -> np.ndarray:
        """
        Reduce noise from audio.

        Args:
            audio: Input audio
            noise_profile: Noise profile (if None, estimated from audio)
            stationary: Whether noise is stationary

        Returns:
            Denoised audio
        """
        try:
            import noisereduce as nr

            reduced = nr.reduce_noise(
                y=audio,
                sr=self.sample_rate,
                stationary=stationary,
                y_noise=noise_profile
            )

            return reduced

        except ImportError:
            print("Warning: noisereduce not installed. Install with: pip install noisereduce")
            return audio
        except Exception as e:
            print(f"Warning: Noise reduction failed: {e}")
            return audio

    def spectral_subtraction(
        self,
        audio: np.ndarray,
        noise_factor: float = 2.0
    ) -> np.ndarray:
        """
        Apply spectral subtraction for noise reduction.

        Args:
            audio: Input audio
            noise_factor: Noise subtraction factor

        Returns:
            Denoised audio
        """
        try:
            from scipy import signal
            import librosa

            # Compute STFT
            D = librosa.stft(audio)

            # Estimate noise spectrum from first few frames
            noise_spec = np.mean(np.abs(D[:, :10]), axis=1, keepdims=True)

            # Subtract noise spectrum
            magnitude = np.abs(D)
            phase = np.angle(D)

            cleaned_magnitude = np.maximum(
                magnitude - noise_factor * noise_spec,
                0.1 * magnitude  # Don't subtract too much
            )

            # Reconstruct
            cleaned_D = cleaned_magnitude * np.exp(1j * phase)
            cleaned_audio = librosa.istft(cleaned_D)

            return cleaned_audio

        except ImportError:
            print("Warning: librosa/scipy not available for spectral subtraction")
            return audio
        except Exception as e:
            print(f"Warning: Spectral subtraction failed: {e}")
            return audio

    def wiener_filter(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply Wiener filtering for noise reduction.

        Args:
            audio: Input audio

        Returns:
            Filtered audio
        """
        try:
            from scipy.signal import wiener

            # Apply Wiener filter
            filtered = wiener(audio)

            return filtered

        except ImportError:
            print("Warning: scipy not available for Wiener filtering")
            return audio
        except Exception as e:
            print(f"Warning: Wiener filtering failed: {e}")
            return audio
