"""
Llama 3.2 1B Integration using Ollama
Lightweight LLM for stock analysis and news summarization
"""

import ollama
from typing import Dict, List
import json


class LlamaAnalyzer:
    """Wrapper for Llama 3.2 1B model using Ollama"""

    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model
        self._check_model()

    def _check_model(self):
        """Check if the model is available"""
        try:
            # Test connection
            ollama.list()
            print(f"✓ Ollama is running")
            print(f"✓ Using model: {self.model}")
        except Exception as e:
            print(f"⚠ Warning: Ollama might not be running - {e}")
            print("Please install Ollama and run: ollama pull llama3.2:1b")

    def _generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate text using Llama 3.2 1B"""
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "num_predict": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            )
            return response['response'].strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def analyze_stock(self, ticker: str, stock_info: Dict, news: List[Dict]) -> Dict:
        """
        Analyze stock with LLM
        Returns: {summary: str, sentiment: str}
        """
        # Prepare context
        news_text = "\n".join([
            f"- {item['title']}" for item in news[:5]
        ]) if news else "No recent news available."

        price = stock_info.get("current_price", "N/A")
        change = stock_info.get("change_percent", "N/A")
        company = stock_info.get("name", ticker)

        # Create prompt
        prompt = f"""You are a financial analyst. Analyze this stock briefly.

Ticker: {ticker}
Company: {company}
Current Price: ${price}
Change: {change}%

Recent News:
{news_text}

Provide:
1. Brief analysis (2-3 sentences)
2. Sentiment (Positive/Neutral/Negative)

Keep it concise and factual."""

        # Generate analysis
        response = self._generate(prompt, max_tokens=300)

        # Extract sentiment
        sentiment = "Neutral"
        response_lower = response.lower()
        if "positive" in response_lower or "bullish" in response_lower:
            sentiment = "Positive"
        elif "negative" in response_lower or "bearish" in response_lower:
            sentiment = "Negative"

        return {
            "summary": response,
            "sentiment": sentiment
        }

    def summarize_text(self, text: str) -> str:
        """Summarize news article or text"""
        prompt = f"""Summarize this text in 2-3 sentences:

{text[:1000]}

Summary:"""

        return self._generate(prompt, max_tokens=150)

    def get_sentiment(self, text: str) -> str:
        """Analyze sentiment of text"""
        prompt = f"""Analyze the sentiment of this text. Reply with only one word: Positive, Negative, or Neutral.

Text: {text[:500]}

Sentiment:"""

        response = self._generate(prompt, max_tokens=10)

        # Clean response
        sentiment = response.strip().split()[0] if response else "Neutral"
        if sentiment not in ["Positive", "Negative", "Neutral"]:
            sentiment = "Neutral"

        return sentiment

    def compare_stocks(self, tickers: List[str], stock_data: List[Dict]) -> str:
        """Compare multiple stocks"""
        comparison = "\n".join([
            f"{data['ticker']}: ${data.get('current_price', 'N/A')} ({data.get('change_percent', 'N/A')}%)"
            for data in stock_data
        ])

        prompt = f"""Compare these stocks briefly (1-2 sentences each):

{comparison}

Which looks better for investment? Keep it concise."""

        return self._generate(prompt, max_tokens=200)
