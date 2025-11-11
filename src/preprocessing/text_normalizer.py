"""
Text Normalizer
Normalizes text for TTS synthesis including numbers, dates, abbreviations, etc.
"""

import re
from typing import Dict, Optional


class TextNormalizer:
    """
    Text normalization for TTS.
    Handles numbers, dates, URLs, abbreviations, etc.
    """

    def __init__(self, language: str = "ko"):
        """
        Initialize text normalizer.

        Args:
            language: Language code ('ko', 'en', etc.)
        """
        self.language = language

        # Number mappings
        self.korean_numbers = {
            '0': '영', '1': '일', '2': '이', '3': '삼', '4': '사',
            '5': '오', '6': '육', '7': '칠', '8': '팔', '9': '구'
        }

        self.english_numbers = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
        }

    def normalize(self, text: str) -> str:
        """
        Normalize text for TTS.

        Args:
            text: Input text

        Returns:
            Normalized text
        """
        # Basic cleanup
        text = text.strip()

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        if self.language == "ko":
            text = self._normalize_korean(text)
        elif self.language == "en":
            text = self._normalize_english(text)

        return text

    def _normalize_korean(self, text: str) -> str:
        """
        Korean-specific normalization.

        Args:
            text: Input Korean text

        Returns:
            Normalized text
        """
        # Convert numbers
        text = self._convert_korean_numbers(text)

        # Normalize currency
        text = self._normalize_korean_currency(text)

        # Normalize dates
        text = self._normalize_korean_dates(text)

        # Normalize phone numbers
        text = self._normalize_phone_numbers(text)

        # Normalize URLs
        text = self._normalize_urls(text)

        return text

    def _normalize_english(self, text: str) -> str:
        """
        English-specific normalization.

        Args:
            text: Input English text

        Returns:
            Normalized text
        """
        # Convert numbers
        text = self._convert_english_numbers(text)

        # Normalize abbreviations
        text = self._normalize_abbreviations(text)

        # Normalize URLs
        text = self._normalize_urls(text)

        return text

    def _convert_korean_numbers(self, text: str) -> str:
        """
        Convert Arabic numerals to Korean pronunciation.

        Args:
            text: Input text with numbers

        Returns:
            Text with numbers converted to Korean
        """
        # Simple digit-by-digit conversion
        # (In production, you would use a more sophisticated Korean number system)

        def replace_number(match):
            number_str = match.group(0)
            # For simple cases, convert digit by digit
            korean = ''.join(self.korean_numbers.get(d, d) for d in number_str)
            return korean

        # Convert standalone numbers
        text = re.sub(r'\b\d+\b', replace_number, text)

        return text

    def _convert_english_numbers(self, text: str) -> str:
        """
        Convert Arabic numerals to English words.

        Args:
            text: Input text with numbers

        Returns:
            Text with numbers converted to English words
        """
        def replace_number(match):
            number = int(match.group(0))

            # Handle numbers 0-20
            if number <= 20:
                words = ['zero', 'one', 'two', 'three', 'four', 'five',
                        'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
                        'twelve', 'thirteen', 'fourteen', 'fifteen',
                        'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']
                return words[number]

            # For larger numbers, use digit-by-digit (simplified)
            # In production, use a proper number-to-words library
            return ' '.join(self.english_numbers.get(d, d) for d in str(number))

        text = re.sub(r'\b\d+\b', replace_number, text)
        return text

    def _normalize_korean_currency(self, text: str) -> str:
        """
        Normalize Korean currency expressions.

        Args:
            text: Input text

        Returns:
            Normalized text
        """
        # ₩, 원
        text = re.sub(r'(\d+)\s*원', r'\1 원', text)
        text = re.sub(r'₩\s*(\d+)', r'\1 원', text)

        # 만원, 억원
        text = re.sub(r'(\d+)\s*만\s*원', r'\1만 원', text)
        text = re.sub(r'(\d+)\s*억\s*원', r'\1억 원', text)

        return text

    def _normalize_korean_dates(self, text: str) -> str:
        """
        Normalize Korean date expressions.

        Args:
            text: Input text

        Returns:
            Normalized text
        """
        # YYYY년 MM월 DD일
        text = re.sub(r'(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일',
                     r'\1년 \2월 \3일', text)

        return text

    def _normalize_phone_numbers(self, text: str) -> str:
        """
        Normalize phone number expressions.

        Args:
            text: Input text

        Returns:
            Normalized text
        """
        # Korean phone numbers: 010-1234-5678
        def replace_phone(match):
            phone = match.group(0)
            # Read digit by digit
            digits = re.sub(r'[^0-9]', '', phone)
            if self.language == "ko":
                korean = ' '.join(self.korean_numbers.get(d, d) for d in digits)
                return korean
            return phone

        text = re.sub(r'\b\d{2,3}[-\s]\d{3,4}[-\s]\d{4}\b', replace_phone, text)

        return text

    def _normalize_urls(self, text: str) -> str:
        """
        Normalize URL expressions.

        Args:
            text: Input text

        Returns:
            Normalized text
        """
        # Replace URLs with readable text
        text = re.sub(
            r'https?://[^\s]+',
            '링크' if self.language == "ko" else 'link',
            text
        )

        return text

    def _normalize_abbreviations(self, text: str) -> str:
        """
        Normalize common abbreviations.

        Args:
            text: Input text

        Returns:
            Normalized text
        """
        abbreviations = {
            "Dr.": "Doctor",
            "Mr.": "Mister",
            "Mrs.": "Missus",
            "Ms.": "Miss",
            "etc.": "et cetera",
            "e.g.": "for example",
            "i.e.": "that is"
        }

        for abbr, full in abbreviations.items():
            text = text.replace(abbr, full)

        return text

    def remove_special_characters(self, text: str, keep: str = "") -> str:
        """
        Remove special characters from text.

        Args:
            text: Input text
            keep: Characters to keep (e.g., ".,!?")

        Returns:
            Cleaned text
        """
        # Keep alphanumeric, whitespace, and specified characters
        pattern = f'[^\\w\\s{re.escape(keep)}]'
        if self.language == "ko":
            # Keep Korean characters
            pattern = f'[^\\w\\s가-힣{re.escape(keep)}]'

        text = re.sub(pattern, '', text)
        return text

    def expand_contractions(self, text: str) -> str:
        """
        Expand English contractions.

        Args:
            text: Input text

        Returns:
            Text with expanded contractions
        """
        if self.language != "en":
            return text

        contractions = {
            "can't": "cannot",
            "won't": "will not",
            "n't": " not",
            "'re": " are",
            "'ve": " have",
            "'ll": " will",
            "'d": " would",
            "'m": " am"
        }

        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)

        return text
