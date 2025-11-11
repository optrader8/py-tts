"""
Basic TTS Usage Examples
"""

from src.tts_engine import TTSEngine, create_tts_engine
from src.configs import TTSConfig


def example_basic():
    """Basic TTS example."""
    print("=== Basic TTS Example ===\n")

    # Create TTS engine with Coqui
    tts = create_tts_engine(engine="coqui", language="ko")

    # Synthesize speech
    text = "안녕하세요. 파이썬 TTS 프로젝트입니다."
    audio = tts.synthesize(text, output_path="output/basic_example.wav")

    print(f"Audio shape: {audio.shape}")
    print(f"Duration: {len(audio) / 22050:.2f} seconds")


def example_with_config():
    """TTS with custom configuration."""
    print("\n=== TTS with Config Example ===\n")

    # Create custom config
    config = TTSConfig(
        engine="coqui",
        language="ko",
        speed=1.1,
        pitch=0.5,
        normalize_text=True,
        enhance_audio=True
    )

    # Create engine
    tts = TTSEngine(config=config)

    # Synthesize
    text = "설정을 사용한 음성 합성 예제입니다."
    audio = tts.synthesize(text, output_path="output/config_example.wav")

    print(f"Engine info: {tts.get_engine_info()}")


def example_batch():
    """Batch synthesis example."""
    print("\n=== Batch Synthesis Example ===\n")

    tts = create_tts_engine(engine="coqui", language="ko")

    texts = [
        "첫 번째 문장입니다.",
        "두 번째 문장입니다.",
        "세 번째 문장입니다."
    ]

    # Synthesize batch
    audios = tts.synthesize_batch(texts, output_dir="output/batch")

    print(f"Generated {len(audios)} audio files")


def example_multilingual():
    """Multilingual TTS example."""
    print("\n=== Multilingual Example ===\n")

    # Korean
    tts_ko = create_tts_engine(engine="coqui", language="ko")
    tts_ko.synthesize("안녕하세요", output_path="output/korean.wav")

    # English
    tts_en = create_tts_engine(engine="coqui", language="en")
    tts_en.synthesize("Hello, world!", output_path="output/english.wav")

    print("Generated Korean and English audio")


def example_with_emotion():
    """TTS with emotion detection."""
    print("\n=== Emotion Detection Example ===\n")

    config = TTSConfig(
        engine="coqui",
        language="ko",
        use_llm_context=False,  # Set to True if you have OpenAI API key
        emotion="happy"
    )

    tts = TTSEngine(config=config)

    texts = {
        "happy": "오늘 정말 기쁜 날이에요!",
        "sad": "너무 슬픈 소식이네요.",
        "neutral": "오늘 날씨는 맑습니다."
    }

    for emotion, text in texts.items():
        output_path = f"output/emotion_{emotion}.wav"
        audio = tts.synthesize(text, output_path=output_path)
        print(f"Generated {emotion} audio: {output_path}")


if __name__ == "__main__":
    import os

    # Create output directory
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/batch", exist_ok=True)

    # Run examples
    try:
        example_basic()
        example_with_config()
        example_batch()
        example_multilingual()
        example_with_emotion()

        print("\n=== All examples completed! ===")

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Note: Some engines require installation and API credentials.")
        print("Install Coqui TTS: pip install TTS")
