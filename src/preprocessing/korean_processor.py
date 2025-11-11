"""
Korean Text Processor
Specialized processing for Korean text in TTS applications.
"""

import re
from typing import Optional, Dict


class KoreanProcessor:
    """
    Korean-specific text processing for TTS.
    Handles Hangul decomposition, romanization, and pronunciation rules.
    """

    def __init__(self):
        """Initialize Korean text processor."""
        self.jamo_available = False

        try:
            import jamo
            self.jamo = jamo
            self.jamo_available = True
        except ImportError:
            print("Warning: jamo library not available. Install with: pip install jamo")

    def process(self, text: str) -> str:
        """
        Process Korean text for TTS.

        Args:
            text: Input Korean text

        Returns:
            Processed text
        """
        # Normalize spacing
        text = self._normalize_spacing(text)

        # Handle special Korean patterns
        text = self._handle_korean_patterns(text)

        return text

    def _normalize_spacing(self, text: str) -> str:
        """
        Normalize Korean text spacing.

        Args:
            text: Input text

        Returns:
            Normalized text
        """
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)

        # Fix spacing around punctuation
        text = re.sub(r'\s*([,.!?;:])\s*', r'\1 ', text)

        return text.strip()

    def _handle_korean_patterns(self, text: str) -> str:
        """
        Handle special Korean language patterns.

        Args:
            text: Input text

        Returns:
            Processed text
        """
        # Handle honorific endings
        text = self._process_honorifics(text)

        # Handle particle variations
        text = self._process_particles(text)

        return text

    def _process_honorifics(self, text: str) -> str:
        """
        Process Korean honorific expressions.

        Args:
            text: Input text

        Returns:
            Processed text
        """
        # Keep honorifics as-is for natural pronunciation
        # This is a placeholder for more sophisticated processing
        return text

    def _process_particles(self, text: str) -> str:
        """
        Process Korean particles (조사).

        Args:
            text: Input text

        Returns:
            Processed text
        """
        # Korean particles are already handled well by g2pk
        # This is a placeholder for custom processing
        return text

    def decompose_hangul(self, text: str) -> str:
        """
        Decompose Hangul characters into jamo (자모).

        Args:
            text: Korean text with Hangul

        Returns:
            Text with decomposed jamo
        """
        if not self.jamo_available:
            return text

        try:
            return self.jamo.h2j(text)
        except Exception as e:
            print(f"Warning: Hangul decomposition failed: {e}")
            return text

    def compose_hangul(self, text: str) -> str:
        """
        Compose jamo into Hangul characters.

        Args:
            text: Text with jamo

        Returns:
            Composed Hangul text
        """
        if not self.jamo_available:
            return text

        try:
            return self.jamo.j2h(text)
        except Exception as e:
            print(f"Warning: Hangul composition failed: {e}")
            return text

    def romanize(self, text: str, system: str = "revised") -> str:
        """
        Romanize Korean text.

        Args:
            text: Korean text
            system: Romanization system ('revised', 'mccune', etc.)

        Returns:
            Romanized text
        """
        try:
            from hangul_romanize import Transliter
            from hangul_romanize.rule import academic

            if system == "revised":
                transliter = Transliter(academic)
                return transliter.translit(text)
            else:
                # Fallback to simple romanization
                return self._simple_romanize(text)
        except ImportError:
            print("Warning: hangul-romanize not available")
            return self._simple_romanize(text)

    def _simple_romanize(self, text: str) -> str:
        """
        Simple romanization fallback.

        Args:
            text: Korean text

        Returns:
            Romanized text
        """
        # Very basic romanization map
        basic_map = {
            'ㄱ': 'g', 'ㄴ': 'n', 'ㄷ': 'd', 'ㄹ': 'r', 'ㅁ': 'm',
            'ㅂ': 'b', 'ㅅ': 's', 'ㅇ': '', 'ㅈ': 'j', 'ㅊ': 'ch',
            'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 'h',
            'ㅏ': 'a', 'ㅓ': 'eo', 'ㅗ': 'o', 'ㅜ': 'u', 'ㅡ': 'eu',
            'ㅣ': 'i', 'ㅐ': 'ae', 'ㅔ': 'e', 'ㅚ': 'oe', 'ㅟ': 'wi'
        }

        result = []
        for char in text:
            if '가' <= char <= '힣':
                # Decompose and map
                if self.jamo_available:
                    jamos = self.jamo.h2j(char)
                    romanized = ''.join(basic_map.get(j, j) for j in jamos)
                    result.append(romanized)
                else:
                    result.append(char)
            else:
                result.append(char)

        return ''.join(result)

    def detect_korean(self, text: str) -> bool:
        """
        Detect if text contains Korean.

        Args:
            text: Input text

        Returns:
            True if Korean is detected
        """
        # Check for Hangul characters
        return bool(re.search(r'[가-힣]', text))

    def separate_korean_english(self, text: str) -> Dict[str, str]:
        """
        Separate Korean and English parts of text.

        Args:
            text: Mixed Korean-English text

        Returns:
            Dictionary with 'korean' and 'english' keys
        """
        korean_parts = re.findall(r'[가-힣]+', text)
        english_parts = re.findall(r'[a-zA-Z]+', text)

        return {
            'korean': ' '.join(korean_parts),
            'english': ' '.join(english_parts)
        }

    def normalize_korean_numbers(self, text: str) -> str:
        """
        Normalize Korean number expressions.

        Args:
            text: Text with Korean numbers

        Returns:
            Normalized text
        """
        # Convert Sino-Korean numbers to native Korean
        # (This is simplified - full implementation would be more complex)

        # 일, 이, 삼... (Sino-Korean)
        # 하나, 둘, 셋... (Native Korean)

        sino_to_native = {
            '일': '하나',
            '이': '둘',
            '삼': '셋',
            '사': '넷',
            '오': '다섯',
            '육': '여섯',
            '칠': '일곱',
            '팔': '여덟',
            '구': '아홉',
            '십': '열'
        }

        # This is context-dependent in real Korean
        # Here's a simplified version
        for sino, native in sino_to_native.items():
            # Only convert in certain contexts
            # (full implementation would need better context awareness)
            pass

        return text

    def apply_pronunciation_rules(self, text: str) -> str:
        """
        Apply Korean pronunciation rules.

        Args:
            text: Korean text

        Returns:
            Text with pronunciation rules applied
        """
        # Korean pronunciation rules:
        # - 연음 (liaison)
        # - 경음화 (tensification)
        # - 비음화 (nasalization)
        # - etc.

        # These are complex rules - typically handled by g2pk
        # This is a placeholder for custom rules

        return text

    def count_syllables(self, text: str) -> int:
        """
        Count Korean syllables.

        Args:
            text: Korean text

        Returns:
            Number of syllables
        """
        # Each Hangul character is typically one syllable
        korean_chars = re.findall(r'[가-힣]', text)
        return len(korean_chars)


# Example usage
if __name__ == "__main__":
    processor = KoreanProcessor()

    # Test text
    korean_text = "안녕하세요. 오늘 날씨가 좋네요."

    print(f"Original: {korean_text}")
    print(f"Processed: {processor.process(korean_text)}")
    print(f"Syllable count: {processor.count_syllables(korean_text)}")
    print(f"Romanized: {processor.romanize(korean_text)}")

    if processor.jamo_available:
        print(f"Decomposed: {processor.decompose_hangul('안녕')}")
