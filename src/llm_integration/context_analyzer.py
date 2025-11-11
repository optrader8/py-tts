"""
Context Analyzer
Analyzes text context using LLMs to improve TTS output.
"""

from typing import Optional, Dict, Any
import os


class ContextAnalyzer:
    """
    Analyzes text context to determine appropriate prosody for TTS.
    Uses LLMs to understand context, formality, and speaking style.
    """

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None
    ):
        """
        Initialize context analyzer.

        Args:
            model: LLM model to use
            api_key: API key for LLM service
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = None

        if self.api_key:
            self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize LLM client."""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            print("Context analyzer initialized with OpenAI")
        except ImportError:
            print("Warning: openai not installed. Install with: pip install openai")

    def analyze(
        self,
        text: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze text context.

        Args:
            text: Text to analyze
            context: Additional context

        Returns:
            Dictionary with analysis results
        """
        if not self.client:
            return self._simple_analysis(text)

        try:
            prompt = self._build_prompt(text, context)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a text analysis expert for TTS systems."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            result = response.choices[0].message.content
            return self._parse_analysis(result)

        except Exception as e:
            print(f"Warning: LLM analysis failed: {e}")
            return self._simple_analysis(text)

    def _build_prompt(self, text: str, context: Optional[str]) -> str:
        """Build prompt for LLM."""
        prompt = f"""Analyze the following text for TTS synthesis:

Text: "{text}"
"""

        if context:
            prompt += f"\nContext: {context}"

        prompt += """

Provide:
1. Formality level (formal/neutral/informal)
2. Emotion (neutral/happy/sad/angry/surprised)
3. Speaking style (narrative/conversational/instructional/dramatic)
4. Suggested speaking rate (slow/normal/fast)
5. Emphasis words (if any)

Format your response as:
Formality: <level>
Emotion: <emotion>
Style: <style>
Rate: <rate>
Emphasis: <words>
"""

        return prompt

    def _parse_analysis(self, result: str) -> Dict[str, Any]:
        """Parse LLM analysis result."""
        analysis = {
            "formality": "neutral",
            "emotion": "neutral",
            "style": "conversational",
            "rate": "normal",
            "emphasis": []
        }

        lines = result.strip().split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()

                if key == "formality":
                    analysis["formality"] = value
                elif key == "emotion":
                    analysis["emotion"] = value
                elif key == "style":
                    analysis["style"] = value
                elif key == "rate":
                    analysis["rate"] = value
                elif key == "emphasis":
                    analysis["emphasis"] = [w.strip() for w in value.split(',')]

        return analysis

    def _simple_analysis(self, text: str) -> Dict[str, Any]:
        """Simple rule-based analysis fallback."""
        analysis = {
            "formality": "neutral",
            "emotion": "neutral",
            "style": "conversational",
            "rate": "normal",
            "emphasis": []
        }

        # Simple rules
        if '?' in text:
            analysis["emotion"] = "curious"
        if '!' in text:
            analysis["emotion"] = "excited"
        if any(word in text.lower() for word in ['존경하는', '귀하', '귀사']):
            analysis["formality"] = "formal"
        if any(word in text.lower() for word in ['안녕', '야', '오']):
            analysis["formality"] = "informal"

        return analysis

    def get_prosody_params(self, analysis: Dict[str, Any]) -> Dict[str, float]:
        """
        Convert analysis to prosody parameters.

        Args:
            analysis: Analysis result

        Returns:
            Prosody parameters (rate, pitch, volume)
        """
        params = {
            "rate": 1.0,
            "pitch": 0.0,
            "volume": 1.0
        }

        # Adjust rate
        if analysis.get("rate") == "slow":
            params["rate"] = 0.8
        elif analysis.get("rate") == "fast":
            params["rate"] = 1.2

        # Adjust pitch based on emotion
        emotion = analysis.get("emotion", "neutral")
        if emotion == "happy" or emotion == "excited":
            params["pitch"] = 2.0
        elif emotion == "sad":
            params["pitch"] = -2.0

        return params
