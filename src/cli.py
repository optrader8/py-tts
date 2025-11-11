"""
Command-Line Interface for Python TTS
"""

import click
import sys
from pathlib import Path
from typing import Optional

from .tts_engine import TTSEngine
from .configs import TTSConfig


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Python TTS - Advanced Text-to-Speech System

    Supports multiple engines: Coqui, Google Cloud, Azure, Amazon Polly, Piper
    """
    pass


@cli.command()
@click.argument("text")
@click.option(
    "--engine", "-e",
    default="coqui",
    type=click.Choice(["coqui", "google", "azure", "polly", "piper"]),
    help="TTS engine to use"
)
@click.option(
    "--language", "-l",
    default="ko",
    help="Language code (ko, en, etc.)"
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    required=True,
    help="Output audio file path"
)
@click.option(
    "--speed",
    default=1.0,
    type=float,
    help="Speaking speed (0.5-2.0)"
)
@click.option(
    "--pitch",
    default=0.0,
    type=float,
    help="Pitch adjustment (-20 to +20)"
)
@click.option(
    "--voice",
    help="Voice name or ID"
)
@click.option(
    "--enhance/--no-enhance",
    default=True,
    help="Enable audio enhancement"
)
def synthesize(
    text: str,
    engine: str,
    language: str,
    output: str,
    speed: float,
    pitch: float,
    voice: Optional[str],
    enhance: bool
):
    """
    Synthesize speech from text.

    Example:
        py-tts synthesize "안녕하세요" -o output.wav
    """
    try:
        click.echo(f"Initializing {engine} TTS engine...")

        # Create config
        config = TTSConfig(
            engine=engine,
            language=language,
            speed=speed,
            pitch=pitch,
            voice_name=voice,
            enhance_audio=enhance
        )

        # Create TTS engine
        tts = TTSEngine(config=config)

        click.echo(f"Synthesizing: '{text}'")

        # Synthesize
        audio = tts.synthesize(text, output_path=output)

        click.echo(f"✓ Audio saved to: {output}")
        click.echo(f"  Duration: {len(audio) / tts.config.sample_rate:.2f}s")
        click.echo(f"  Sample rate: {tts.config.sample_rate} Hz")

    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--engine", "-e",
    default="coqui",
    type=click.Choice(["coqui", "google", "azure", "polly", "piper"]),
    help="TTS engine to use"
)
@click.option(
    "--language", "-l",
    default="ko",
    help="Language code"
)
@click.option(
    "--output-dir", "-o",
    type=click.Path(),
    required=True,
    help="Output directory for audio files"
)
def batch(input_file: str, engine: str, language: str, output_dir: str):
    """
    Batch synthesize from text file (one sentence per line).

    Example:
        py-tts batch input.txt -o output_dir/
    """
    try:
        # Read input file
        with open(input_file, "r", encoding="utf-8") as f:
            texts = [line.strip() for line in f if line.strip()]

        click.echo(f"Processing {len(texts)} texts...")

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Create TTS engine
        config = TTSConfig(engine=engine, language=language)
        tts = TTSEngine(config=config)

        # Synthesize batch
        with click.progressbar(
            enumerate(texts),
            length=len(texts),
            label="Synthesizing"
        ) as bar:
            for i, text in bar:
                output_path = Path(output_dir) / f"audio_{i:03d}.wav"
                tts.synthesize(text, output_path=str(output_path))

        click.echo(f"✓ Generated {len(texts)} audio files in: {output_dir}")

    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--engine", "-e",
    type=click.Choice(["coqui", "google", "azure", "polly", "piper"]),
    help="Filter by engine"
)
def list_voices(engine: Optional[str]):
    """
    List available voices for TTS engines.

    Example:
        py-tts list-voices --engine google
    """
    try:
        engines_to_check = [engine] if engine else ["coqui", "google", "azure", "polly"]

        for eng in engines_to_check:
            click.echo(f"\n{eng.upper()} Voices:")
            click.echo("-" * 40)

            try:
                config = TTSConfig(engine=eng)
                tts = TTSEngine(config=config)

                voices = tts.list_available_voices()

                if voices:
                    for voice in voices[:10]:  # Show first 10
                        if isinstance(voice, dict):
                            click.echo(f"  • {voice.get('name', voice.get('id', 'Unknown'))}")
                        else:
                            click.echo(f"  • {voice}")

                    if len(voices) > 10:
                        click.echo(f"  ... and {len(voices) - 10} more")
                else:
                    click.echo("  No voices available or listing not supported")

            except Exception as e:
                click.echo(f"  Error: {str(e)}")

    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def engines():
    """
    List available TTS engines.
    """
    available_engines = TTSEngine.list_engines()

    click.echo("Available TTS Engines:")
    click.echo("=" * 40)

    for eng in available_engines:
        click.echo(f"  • {eng}")

    click.echo("\nUse --engine flag to select an engine")


@cli.command()
@click.argument("text")
@click.option(
    "--language", "-l",
    default="ko",
    help="Language code"
)
def normalize(text: str, language: str):
    """
    Normalize text for TTS.

    Example:
        py-tts normalize "전화번호는 010-1234-5678입니다"
    """
    from .preprocessing import TextNormalizer

    normalizer = TextNormalizer(language=language)
    normalized = normalizer.normalize(text)

    click.echo("Original:")
    click.echo(f"  {text}")
    click.echo("\nNormalized:")
    click.echo(f"  {normalized}")


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True))
def analyze(audio_file: str):
    """
    Analyze audio file metrics.

    Example:
        py-tts analyze output.wav
    """
    from .utils import AudioUtils, AudioMetrics

    try:
        # Load audio
        audio, sr = AudioUtils.load_audio(audio_file)

        # Calculate metrics
        metrics = AudioMetrics.calculate_all_metrics(audio, sample_rate=sr)

        click.echo(f"Audio Analysis: {audio_file}")
        click.echo("=" * 40)
        click.echo(f"Duration: {AudioUtils.get_audio_duration(audio, sr):.2f}s")
        click.echo(f"Sample Rate: {sr} Hz")
        click.echo(f"Samples: {len(audio)}")
        click.echo("\nMetrics:")

        for key, value in metrics.items():
            click.echo(f"  {key}: {value:.4f}")

    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
