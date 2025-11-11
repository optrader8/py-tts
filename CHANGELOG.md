# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Multiple TTS engine support:
  - Coqui TTS (local, high-quality)
  - Google Cloud TTS (WaveNet-based)
  - Microsoft Azure TTS (neural voices with styles)
  - Amazon Polly (AWS TTS service)
  - Piper TTS (fast, local)
- Text preprocessing modules:
  - TextNormalizer for number, date, URL normalization
  - PhonemeConverter with g2pk and epitran support
  - KoreanProcessor for Hangul processing
- Audio postprocessing:
  - AudioEnhancer for quality improvement
  - NoiseReducer for noise reduction
- LLM integration:
  - ContextAnalyzer for prosody adjustment
  - EmotionDetector for emotional expression
- Utility modules:
  - AudioUtils for audio operations
  - AudioMetrics for quality assessment
- Configuration management system
- Command-line interface
- Comprehensive test suite
- Documentation and guides
- GitHub Actions CI/CD
- Example scripts and demos

## [0.1.0] - 2024-11-11

### Added
- Initial release
- Basic TTS functionality
- Multi-engine architecture
- Korean language support
- Basic documentation

[Unreleased]: https://github.com/optrader8/py-tts/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/optrader8/py-tts/releases/tag/v0.1.0
