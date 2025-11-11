#!/usr/bin/env python
"""
Interactive Demo for Python TTS Project
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tts_engine import create_tts_engine, TTSEngine
from src.configs import TTSConfig
from src.preprocessing import TextNormalizer
from src.utils import AudioMetrics


def print_banner():
    """Print demo banner."""
    banner = """
╔══════════════════════════════════════════════════╗
║      Python TTS - Interactive Demo              ║
║      Multi-Engine Text-to-Speech System          ║
╚══════════════════════════════════════════════════╝
"""
    print(banner)


def print_menu():
    """Print main menu."""
    menu = """
Choose a demo:

1. Basic TTS (Coqui - Local)
2. Text Preprocessing Demo
3. Audio Enhancement Demo
4. Multi-Engine Comparison
5. Batch Processing Demo
6. Custom Voice Settings
7. Exit

"""
    print(menu)


def demo_basic_tts():
    """Demo 1: Basic TTS."""
    print("\n" + "="*50)
    print("Demo 1: Basic TTS with Coqui")
    print("="*50 + "\n")

    try:
        print("Initializing Coqui TTS engine...")
        tts = create_tts_engine(engine="coqui", language="ko")

        print("✓ Engine initialized")

        # Get text from user
        text = input("\nEnter text to synthesize (or press Enter for default): ").strip()
        if not text:
            text = "안녕하세요. 파이썬 TTS 프로젝트입니다."

        print(f"\nSynthesizing: '{text}'")

        # Create output directory
        Path("output").mkdir(exist_ok=True)

        # Synthesize
        audio = tts.synthesize(text, output_path="output/demo_basic.wav")

        print(f"\n✓ Success!")
        print(f"  Audio saved to: output/demo_basic.wav")
        print(f"  Duration: {len(audio) / 22050:.2f} seconds")
        print(f"  Samples: {len(audio)}")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nNote: This demo requires Coqui TTS. Install with: pip install TTS")


def demo_preprocessing():
    """Demo 2: Text Preprocessing."""
    print("\n" + "="*50)
    print("Demo 2: Text Preprocessing")
    print("="*50 + "\n")

    normalizer = TextNormalizer(language="ko")

    test_texts = [
        "전화번호는 010-1234-5678입니다.",
        "가격은 10000원입니다.",
        "오늘은 2024년 1월 1일입니다.",
        "방문하세요 https://example.com"
    ]

    print("Korean Text Normalization:\n")

    for text in test_texts:
        normalized = normalizer.normalize(text)
        print(f"Original  : {text}")
        print(f"Normalized: {normalized}\n")


def demo_audio_enhancement():
    """Demo 3: Audio Enhancement."""
    print("\n" + "="*50)
    print("Demo 3: Audio Enhancement")
    print("="*50 + "\n")

    try:
        from src.postprocessing import AudioEnhancer
        import numpy as np

        print("Creating sample audio...")

        # Generate sample audio
        tts = create_tts_engine(engine="coqui", language="ko")
        audio = tts.synthesize("오디오 향상 데모입니다.")

        print("✓ Audio generated")

        # Enhance
        enhancer = AudioEnhancer(sample_rate=22050)

        print("\nApplying enhancements...")
        enhanced = enhancer.enhance(
            audio,
            normalize=True,
            denoise=True,
            enhance_bass=False
        )

        print("✓ Enhancement complete")

        # Calculate metrics
        print("\nAudio Metrics:")
        metrics = AudioMetrics.calculate_all_metrics(enhanced, sample_rate=22050)

        for key, value in metrics.items():
            print(f"  {key}: {value:.4f}")

        # Save
        Path("output").mkdir(exist_ok=True)
        enhancer.save_audio(enhanced, "output/demo_enhanced.wav", sample_rate=22050)
        print(f"\n✓ Enhanced audio saved to: output/demo_enhanced.wav")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def demo_multi_engine():
    """Demo 4: Multi-Engine Comparison."""
    print("\n" + "="*50)
    print("Demo 4: Multi-Engine Comparison")
    print("="*50 + "\n")

    text = "이것은 멀티 엔진 비교 데모입니다."

    engines_to_test = [
        ("coqui", "Coqui TTS (Local)"),
    ]

    # Check for API keys
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        engines_to_test.append(("google", "Google Cloud TTS"))

    if os.getenv("AZURE_SPEECH_KEY"):
        engines_to_test.append(("azure", "Microsoft Azure TTS"))

    if os.getenv("AWS_ACCESS_KEY_ID"):
        engines_to_test.append(("polly", "Amazon Polly"))

    print(f"Testing {len(engines_to_test)} engine(s)...\n")

    Path("output").mkdir(exist_ok=True)

    for engine_name, display_name in engines_to_test:
        try:
            print(f"Testing {display_name}...")
            tts = create_tts_engine(engine=engine_name, language="ko")

            output_path = f"output/demo_{engine_name}.wav"
            audio = tts.synthesize(text, output_path=output_path)

            print(f"  ✓ Generated: {output_path}")
            print(f"    Duration: {len(audio) / 22050:.2f}s\n")

        except Exception as e:
            print(f"  ✗ Failed: {str(e)}\n")

    print("Comparison complete!")


def demo_batch_processing():
    """Demo 5: Batch Processing."""
    print("\n" + "="*50)
    print("Demo 5: Batch Processing")
    print("="*50 + "\n")

    texts = [
        "첫 번째 문장입니다.",
        "두 번째 문장입니다.",
        "세 번째 문장입니다.",
        "네 번째 문장입니다.",
        "다섯 번째 문장입니다."
    ]

    try:
        print(f"Processing {len(texts)} texts...")

        tts = create_tts_engine(engine="coqui", language="ko")

        Path("output/batch").mkdir(parents=True, exist_ok=True)

        audios = tts.synthesize_batch(texts, output_dir="output/batch")

        print(f"\n✓ Generated {len(audios)} audio files")
        print(f"  Output directory: output/batch/")

        total_duration = sum(len(audio) / 22050 for audio in audios)
        print(f"  Total duration: {total_duration:.2f} seconds")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def demo_custom_voice():
    """Demo 6: Custom Voice Settings."""
    print("\n" + "="*50)
    print("Demo 6: Custom Voice Settings")
    print("="*50 + "\n")

    text = "이것은 맞춤 설정 데모입니다."

    settings = [
        ("Normal", {"speed": 1.0, "pitch": 0.0}),
        ("Fast", {"speed": 1.5, "pitch": 0.0}),
        ("Slow", {"speed": 0.7, "pitch": 0.0}),
        ("High Pitch", {"speed": 1.0, "pitch": 5.0}),
        ("Low Pitch", {"speed": 1.0, "pitch": -5.0}),
    ]

    try:
        Path("output/custom").mkdir(parents=True, exist_ok=True)

        for name, params in settings:
            print(f"Generating '{name}' voice...")

            config = TTSConfig(
                engine="coqui",
                language="ko",
                speed=params["speed"],
                pitch=params["pitch"]
            )

            tts = TTSEngine(config=config)

            filename = name.lower().replace(" ", "_")
            output_path = f"output/custom/{filename}.wav"

            audio = tts.synthesize(text, output_path=output_path)

            print(f"  ✓ Saved: {output_path}\n")

        print("Custom voice generation complete!")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


def main():
    """Main demo loop."""
    print_banner()

    # Create output directory
    Path("output").mkdir(exist_ok=True)

    while True:
        print_menu()

        try:
            choice = input("Enter your choice (1-7): ").strip()

            if choice == "1":
                demo_basic_tts()
            elif choice == "2":
                demo_preprocessing()
            elif choice == "3":
                demo_audio_enhancement()
            elif choice == "4":
                demo_multi_engine()
            elif choice == "5":
                demo_batch_processing()
            elif choice == "6":
                demo_custom_voice()
            elif choice == "7":
                print("\nThank you for using Python TTS Demo!")
                print("Visit https://github.com/optrader8/py-tts for more information.\n")
                break
            else:
                print("\n✗ Invalid choice. Please enter 1-7.")

            input("\nPress Enter to continue...")
            print("\n" * 2)

        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {str(e)}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
