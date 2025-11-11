"""
Emotion Detector
Detects emotions in text for expressive TTS.
"""

from typing import Optional, Dict
import re


class EmotionDetector:
    """
    Detects emotions in text to guide TTS expression.
    """

    def __init__(self):
        """Initialize emotion detector."""
        self.emotion_keywords = {
            "happy": ["행복", "기쁜", "즐거운", "웃", "축하", "좋"],
            "sad": ["슬픈", "우울", "아픈", "눈물", "실망", "안타까운"],
            "angry": ["화", "분노", "짜증", "억울", "못마땅"],
            "surprised": ["놀란", "깜짝", "의외", "예상외"],
            "fear": ["무서운", "두려운", "겁", "공포"],
            "disgust": ["역겨운", "싫은", "불쾌"]
        }

    def detect(self, text: str) -> Dict[str, float]:
        """
        Detect emotions in text.

        Args:
            text: Input text

        Returns:
            Dictionary of emotion scores
        """
        emotions = {emotion: 0.0 for emotion in self.emotion_keywords.keys()}
        emotions["neutral"] = 0.5  # Default neutral score

        # Check for emotion keywords
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    emotions[emotion] += 0.2

        # Check punctuation
        if '!' in text:
            emotions["surprised"] += 0.1
            emotions["happy"] += 0.1
        if '?' in text:
            emotions["surprised"] += 0.05

        # Normalize scores
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v / total for k, v in emotions.items()}

        return emotions

    def get_primary_emotion(self, text: str) -> str:
        """
        Get primary emotion from text.

        Args:
            text: Input text

        Returns:
            Primary emotion name
        """
        emotions = self.detect(text)
        return max(emotions, key=emotions.get)

    def get_emotion_intensity(self, text: str) -> float:
        """
        Get overall emotion intensity.

        Args:
            text: Input text

        Returns:
            Intensity score (0.0-1.0)
        """
        emotions = self.detect(text)

        # Remove neutral and calculate intensity
        emotions_copy = emotions.copy()
        emotions_copy.pop("neutral", None)

        if not emotions_copy:
            return 0.0

        return max(emotions_copy.values())
