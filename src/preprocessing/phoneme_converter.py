"""
Phoneme Converter
Converts text to phonemes for TTS engines that require phoneme input.
"""

from typing import Optional, List


class PhonemeConverter:
    """
    Converts text to phonemes.
    Supports multiple languages and phoneme formats.
    """

    def __init__(self, language: str = "ko", backend: str = "auto"):
        """
        Initialize phoneme converter.

        Args:
            language: Language code ('ko', 'en', etc.)
            backend: Phoneme conversion backend ('auto', 'g2pk', 'epitran', etc.)
        """
        self.language = language
        self.backend = backend
        self.converter = None

        self._initialize_converter()

    def _initialize_converter(self) -> None:
        """
        Initialize the phoneme conversion backend.
        """
        if self.language == "ko":
            self._initialize_korean_converter()
        elif self.language == "en":
            self._initialize_english_converter()
        else:
            print(f"Warning: No phoneme converter available for language: {self.language}")

    def _initialize_korean_converter(self) -> None:
        """
        Initialize Korean phoneme converter.
        """
        try:
            # Try to use g2pk (Grapheme-to-Phoneme for Korean)
            from g2pk import G2p
            self.converter = G2p()
            self.backend = "g2pk"
            print("Korean phoneme converter initialized (g2pk)")
        except ImportError:
            print("Warning: g2pk not installed. Install with: pip install g2pk")
            print("Falling back to simple Korean phoneme conversion")
            self.backend = "simple"

    def _initialize_english_converter(self) -> None:
        """
        Initialize English phoneme converter.
        """
        try:
            # Try to use epitran
            import epitran
            self.converter = epitran.Epitran('eng-Latn')
            self.backend = "epitran"
            print("English phoneme converter initialized (epitran)")
        except ImportError:
            print("Warning: epitran not installed. Install with: pip install epitran")
            print("Falling back to simple English phoneme conversion")
            self.backend = "simple"

    def convert(self, text: str) -> str:
        """
        Convert text to phonemes.

        Args:
            text: Input text

        Returns:
            Phoneme representation
        """
        if self.language == "ko":
            return self._convert_korean(text)
        elif self.language == "en":
            return self._convert_english(text)
        else:
            return text

    def _convert_korean(self, text: str) -> str:
        """
        Convert Korean text to phonemes.

        Args:
            text: Korean text

        Returns:
            Phoneme representation
        """
        if self.backend == "g2pk" and self.converter:
            try:
                # g2pk converts to Korean phonemes
                phonemes = self.converter(text)
                return phonemes
            except Exception as e:
                print(f"Warning: g2pk conversion failed: {e}")
                return text
        else:
            # Simple fallback - return original text
            return text

    def _convert_english(self, text: str) -> str:
        """
        Convert English text to phonemes.

        Args:
            text: English text

        Returns:
            Phoneme representation (IPA)
        """
        if self.backend == "epitran" and self.converter:
            try:
                # epitran converts to IPA
                phonemes = self.converter.transliterate(text)
                return phonemes
            except Exception as e:
                print(f"Warning: epitran conversion failed: {e}")
                return text
        else:
            # Simple fallback
            return text

    def convert_to_ipa(self, text: str) -> str:
        """
        Convert text to International Phonetic Alphabet (IPA).

        Args:
            text: Input text

        Returns:
            IPA representation
        """
        return self.convert(text)

    def convert_to_arpabet(self, text: str) -> List[str]:
        """
        Convert English text to ARPABET phonemes.

        Args:
            text: English text

        Returns:
            List of ARPABET phonemes
        """
        if self.language != "en":
            raise ValueError("ARPABET conversion only available for English")

        try:
            # Try to use g2p_en for ARPABET
            from g2p_en import G2p
            g2p = G2p()
            phonemes = g2p(text)
            return phonemes
        except ImportError:
            print("Warning: g2p_en not installed. Install with: pip install g2p-en")
            return text.split()

    def get_phoneme_list(self, text: str) -> List[str]:
        """
        Get list of individual phonemes.

        Args:
            text: Input text

        Returns:
            List of phonemes
        """
        phoneme_str = self.convert(text)

        # Simple splitting (customize based on your phoneme format)
        if self.language == "ko":
            # Korean: each character might be a phoneme unit
            return list(phoneme_str)
        else:
            # Other languages: split by space
            return phoneme_str.split()

    def supports_language(self, language: str) -> bool:
        """
        Check if language is supported.

        Args:
            language: Language code

        Returns:
            True if supported
        """
        return language in ["ko", "en", "ja", "zh"]


class KoreanPhonemeConverter:
    """
    Specialized Korean phoneme converter with additional features.
    """

    def __init__(self):
        """Initialize Korean phoneme converter."""
        try:
            from g2pk import G2p
            self.g2p = G2p()
        except ImportError:
            self.g2p = None
            print("Warning: g2pk not available")

    def convert(self, text: str) -> str:
        """
        Convert Korean text to phonemes.

        Args:
            text: Korean text

        Returns:
            Phoneme representation
        """
        if self.g2p:
            return self.g2p(text)
        return text

    def apply_phonological_rules(self, text: str) -> str:
        """
        Apply Korean phonological rules.

        Args:
            text: Korean text

        Returns:
            Text with phonological rules applied
        """
        # This is handled by g2pk automatically
        return self.convert(text)


# Example usage
if __name__ == "__main__":
    # Korean example
    ko_converter = PhonemeConverter(language="ko")
    korean_text = "안녕하세요"
    korean_phonemes = ko_converter.convert(korean_text)
    print(f"Korean: {korean_text} -> {korean_phonemes}")

    # English example
    en_converter = PhonemeConverter(language="en")
    english_text = "Hello, how are you?"
    english_phonemes = en_converter.convert(english_text)
    print(f"English: {english_text} -> {english_phonemes}")
