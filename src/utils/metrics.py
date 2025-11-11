"""
Audio Metrics
Evaluation metrics for TTS quality assessment.
"""

import numpy as np
from typing import Optional, Dict


class AudioMetrics:
    """
    Metrics for evaluating TTS audio quality.
    """

    @staticmethod
    def calculate_snr(
        audio: np.ndarray,
        noise: Optional[np.ndarray] = None
    ) -> float:
        """
        Calculate Signal-to-Noise Ratio.

        Args:
            audio: Audio signal
            noise: Noise signal (if None, estimate from audio)

        Returns:
            SNR in dB
        """
        if noise is None:
            # Estimate noise from low-energy regions
            energy = np.abs(audio)
            threshold = np.percentile(energy, 10)
            noise = audio[energy < threshold]

        if len(noise) == 0:
            return float('inf')

        signal_power = np.mean(audio ** 2)
        noise_power = np.mean(noise ** 2)

        if noise_power == 0:
            return float('inf')

        snr = 10 * np.log10(signal_power / noise_power)
        return snr

    @staticmethod
    def calculate_rms(audio: np.ndarray) -> float:
        """
        Calculate Root Mean Square of audio.

        Args:
            audio: Audio data

        Returns:
            RMS value
        """
        return np.sqrt(np.mean(audio ** 2))

    @staticmethod
    def calculate_peak_amplitude(audio: np.ndarray) -> float:
        """
        Calculate peak amplitude.

        Args:
            audio: Audio data

        Returns:
            Peak amplitude
        """
        return np.abs(audio).max()

    @staticmethod
    def calculate_zero_crossing_rate(audio: np.ndarray) -> float:
        """
        Calculate zero crossing rate.

        Args:
            audio: Audio data

        Returns:
            Zero crossing rate
        """
        zero_crossings = np.where(np.diff(np.sign(audio)))[0]
        return len(zero_crossings) / len(audio)

    @staticmethod
    def calculate_spectral_centroid(
        audio: np.ndarray,
        sample_rate: int = 22050
    ) -> float:
        """
        Calculate spectral centroid.

        Args:
            audio: Audio data
            sample_rate: Sample rate

        Returns:
            Spectral centroid in Hz
        """
        try:
            import librosa

            spectral_centroids = librosa.feature.spectral_centroid(
                y=audio,
                sr=sample_rate
            )[0]

            return np.mean(spectral_centroids)

        except ImportError:
            print("Warning: librosa not available for spectral centroid")
            return 0.0

    @staticmethod
    def calculate_mfcc(
        audio: np.ndarray,
        sample_rate: int = 22050,
        n_mfcc: int = 13
    ) -> np.ndarray:
        """
        Calculate Mel-frequency cepstral coefficients.

        Args:
            audio: Audio data
            sample_rate: Sample rate
            n_mfcc: Number of MFCCs

        Returns:
            MFCC matrix
        """
        try:
            import librosa

            mfccs = librosa.feature.mfcc(
                y=audio,
                sr=sample_rate,
                n_mfcc=n_mfcc
            )

            return mfccs

        except ImportError:
            print("Warning: librosa not available for MFCC")
            return np.array([])

    @staticmethod
    def calculate_pesq(
        reference: np.ndarray,
        degraded: np.ndarray,
        sample_rate: int = 16000
    ) -> float:
        """
        Calculate PESQ (Perceptual Evaluation of Speech Quality).

        Args:
            reference: Reference audio
            degraded: Degraded audio
            sample_rate: Sample rate (must be 8000 or 16000)

        Returns:
            PESQ score
        """
        try:
            from pesq import pesq

            # PESQ requires 8000 or 16000 Hz
            if sample_rate not in [8000, 16000]:
                print(f"Warning: PESQ requires 8000 or 16000 Hz, got {sample_rate}")
                return 0.0

            score = pesq(sample_rate, reference, degraded, 'wb')
            return score

        except ImportError:
            print("Warning: pesq not available")
            return 0.0
        except Exception as e:
            print(f"Warning: PESQ calculation failed: {e}")
            return 0.0

    @staticmethod
    def calculate_stoi(
        reference: np.ndarray,
        degraded: np.ndarray,
        sample_rate: int = 16000
    ) -> float:
        """
        Calculate STOI (Short-Time Objective Intelligibility).

        Args:
            reference: Reference audio
            degraded: Degraded audio
            sample_rate: Sample rate

        Returns:
            STOI score (0-1)
        """
        try:
            from pystoi import stoi

            score = stoi(reference, degraded, sample_rate, extended=False)
            return score

        except ImportError:
            print("Warning: pystoi not available")
            return 0.0
        except Exception as e:
            print(f"Warning: STOI calculation failed: {e}")
            return 0.0

    @staticmethod
    def calculate_all_metrics(
        audio: np.ndarray,
        sample_rate: int = 22050
    ) -> Dict[str, float]:
        """
        Calculate all available metrics.

        Args:
            audio: Audio data
            sample_rate: Sample rate

        Returns:
            Dictionary of metrics
        """
        metrics = {}

        metrics["rms"] = AudioMetrics.calculate_rms(audio)
        metrics["peak_amplitude"] = AudioMetrics.calculate_peak_amplitude(audio)
        metrics["zero_crossing_rate"] = AudioMetrics.calculate_zero_crossing_rate(audio)
        metrics["snr"] = AudioMetrics.calculate_snr(audio)
        metrics["spectral_centroid"] = AudioMetrics.calculate_spectral_centroid(
            audio, sample_rate
        )

        return metrics
