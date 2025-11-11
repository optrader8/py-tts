"""
Advanced TTS Usage Examples
"""

from src.tts_engine import TTSEngine
from src.configs import TTSConfig
from src.preprocessing import TextNormalizer
from src.postprocessing import AudioEnhancer, NoiseReducer
from src.utils import AudioUtils, AudioMetrics
import numpy as np


def example_text_preprocessing():
    """Text preprocessing example."""
    print("=== Text Preprocessing Example ===\n")

    normalizer = TextNormalizer(language="ko")

    texts = [
        "전화번호는 010-1234-5678입니다.",
        "가격은 10000원입니다.",
        "2024년 1월 1일",
        "https://example.com"
    ]

    for text in texts:
        normalized = normalizer.normalize(text)
        print(f"Original: {text}")
        print(f"Normalized: {normalized}\n")


def example_audio_postprocessing():
    """Audio postprocessing example."""
    print("\n=== Audio Postprocessing Example ===\n")

    # Generate sample audio
    tts = TTSEngine(engine="coqui", config=TTSConfig(language="ko"))
    audio = tts.synthesize("오디오 후처리 예제입니다.")

    # Enhance audio
    enhancer = AudioEnhancer(sample_rate=22050)
    enhanced = enhancer.enhance(
        audio,
        normalize=True,
        denoise=True,
        enhance_bass=True
    )

    # Calculate metrics
    metrics = AudioMetrics.calculate_all_metrics(enhanced, sample_rate=22050)

    print("Audio metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    # Save enhanced audio
    AudioUtils.save_audio(enhanced, "output/enhanced_audio.wav", sample_rate=22050)
    print("\nEnhanced audio saved to: output/enhanced_audio.wav")


def example_voice_cloning():
    """Voice cloning example (Coqui TTS)."""
    print("\n=== Voice Cloning Example ===\n")

    config = TTSConfig(
        engine="coqui",
        language="ko"
    )

    tts = TTSEngine(config=config)

    # Note: You need a reference audio file for voice cloning
    # Uncomment and modify the path if you have a reference audio
    """
    if hasattr(tts.engine, 'clone_voice'):
        audio = tts.engine.clone_voice(
            text="음성 복제 예제입니다.",
            speaker_wav="path/to/reference.wav",
            language="ko"
        )
        AudioUtils.save_audio(audio, "output/cloned_voice.wav")
        print("Cloned voice saved to: output/cloned_voice.wav")
    """

    print("Voice cloning requires Coqui TTS with XTTS model")
    print("Provide a reference audio file to clone a voice")


def example_cloud_tts():
    """Cloud TTS examples (requires API credentials)."""
    print("\n=== Cloud TTS Example ===\n")

    # Google Cloud TTS
    print("Google Cloud TTS:")
    print("  Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
    print("  config = TTSConfig(engine='google', voice_name='ko-KR-Wavenet-A')")

    # Azure TTS
    print("\nAzure TTS:")
    print("  Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION")
    print("  config = TTSConfig(engine='azure', voice_name='ko-KR-SunHiNeural')")

    # Amazon Polly
    print("\nAmazon Polly:")
    print("  Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
    print("  config = TTSConfig(engine='polly', voice_id='Seoyeon')")

    # Example (commented out - requires credentials)
    """
    # Google Cloud TTS
    config = TTSConfig(engine="google", voice_name="ko-KR-Wavenet-A")
    tts = TTSEngine(config=config)
    audio = tts.synthesize("구글 클라우드 TTS 예제입니다.")
    AudioUtils.save_audio(audio, "output/google_tts.wav")
    """


def example_llm_context():
    """LLM-based context analysis example."""
    print("\n=== LLM Context Analysis Example ===\n")

    # Note: Requires OpenAI API key
    print("LLM context analysis requires OpenAI API key")
    print("Set OPENAI_API_KEY environment variable")

    config = TTSConfig(
        engine="coqui",
        language="ko",
        use_llm_context=True  # Enable LLM context analysis
    )

    # Uncomment if you have OpenAI API key
    """
    tts = TTSEngine(config=config)

    # Formal speech
    formal_text = "존경하는 여러분, 오늘 이 자리에 함께해 주셔서 감사합니다."
    audio = tts.synthesize(formal_text, output_path="output/formal_speech.wav")

    # Casual speech
    casual_text = "야, 오늘 날씨 진짜 좋다!"
    audio = tts.synthesize(casual_text, output_path="output/casual_speech.wav")
    """

    print("LLM will analyze context and adjust prosody accordingly")


def example_audio_utilities():
    """Audio utilities example."""
    print("\n=== Audio Utilities Example ===\n")

    # Generate sample audios
    tts = TTSEngine(engine="coqui", config=TTSConfig(language="ko"))

    audio1 = tts.synthesize("첫 번째 문장입니다.")
    audio2 = tts.synthesize("두 번째 문장입니다.")
    audio3 = tts.synthesize("세 번째 문장입니다.")

    # Concatenate with silence
    concatenated = AudioUtils.concatenate_audio(
        [audio1, audio2, audio3],
        silence_duration=0.5,
        sample_rate=22050
    )

    # Apply fade
    faded = AudioUtils.apply_fade(
        concatenated,
        fade_in_duration=0.2,
        fade_out_duration=0.2,
        sample_rate=22050
    )

    # Save result
    AudioUtils.save_audio(faded, "output/concatenated.wav", sample_rate=22050)

    print(f"Concatenated audio duration: {AudioUtils.get_audio_duration(faded, 22050):.2f}s")
    print("Concatenated audio saved to: output/concatenated.wav")


if __name__ == "__main__":
    import os

    # Create output directory
    os.makedirs("output", exist_ok=True)

    # Run examples
    try:
        example_text_preprocessing()
        example_audio_postprocessing()
        example_voice_cloning()
        example_cloud_tts()
        example_llm_context()
        example_audio_utilities()

        print("\n=== Advanced examples completed! ===")

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Note: Some features require additional setup and API credentials.")
