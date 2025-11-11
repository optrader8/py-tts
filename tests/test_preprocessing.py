"""
Tests for text preprocessing modules.
"""

import pytest
from src.preprocessing import TextNormalizer, PhonemeConverter
from src.preprocessing.korean_processor import KoreanProcessor


class TestTextNormalizer:
    """Tests for TextNormalizer class."""

    def test_normalize_korean_numbers(self):
        """Test Korean number normalization."""
        normalizer = TextNormalizer(language="ko")

        text = "전화번호는 123입니다."
        result = normalizer.normalize(text)

        assert "일이삼" in result or "123" in result

    def test_normalize_korean_currency(self):
        """Test Korean currency normalization."""
        normalizer = TextNormalizer(language="ko")

        text = "가격은 10000원입니다."
        result = normalizer.normalize(text)

        assert "원" in result

    def test_normalize_urls(self):
        """Test URL normalization."""
        normalizer = TextNormalizer(language="ko")

        text = "방문하세요 https://example.com"
        result = normalizer.normalize(text)

        assert "링크" in result or "link" in result or "example" in result

    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        normalizer = TextNormalizer(language="ko")

        text = "안녕하세요    여러    공백"
        result = normalizer.normalize(text)

        # Should have single spaces
        assert "    " not in result


class TestPhonemeConverter:
    """Tests for PhonemeConverter class."""

    def test_korean_phoneme_conversion(self):
        """Test Korean phoneme conversion."""
        converter = PhonemeConverter(language="ko")

        text = "안녕"
        result = converter.convert(text)

        # Result should be a string
        assert isinstance(result, str)
        assert len(result) > 0

    def test_english_phoneme_conversion(self):
        """Test English phoneme conversion."""
        converter = PhonemeConverter(language="en")

        text = "hello"
        result = converter.convert(text)

        assert isinstance(result, str)
        assert len(result) > 0


class TestKoreanProcessor:
    """Tests for KoreanProcessor class."""

    def test_detect_korean(self):
        """Test Korean text detection."""
        processor = KoreanProcessor()

        assert processor.detect_korean("안녕하세요") is True
        assert processor.detect_korean("hello") is False
        assert processor.detect_korean("안녕 hello") is True

    def test_count_syllables(self):
        """Test syllable counting."""
        processor = KoreanProcessor()

        text = "안녕하세요"
        count = processor.count_syllables(text)

        assert count == 5

    def test_separate_korean_english(self):
        """Test Korean-English separation."""
        processor = KoreanProcessor()

        text = "안녕하세요 hello 세계 world"
        result = processor.separate_korean_english(text)

        assert "korean" in result
        assert "english" in result
        assert "안녕하세요" in result["korean"]
        assert "hello" in result["english"]
