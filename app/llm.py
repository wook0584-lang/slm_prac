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

        # Create prompt (Korean)
        prompt = f"""당신은 금융 분석가입니다. 이 주식을 간단히 분석해주세요.

티커: {ticker}
회사명: {company}
현재 가격: ${price}
변동: {change}%

최근 뉴스:
{news_text}

다음을 제공하세요:
1. 간단한 분석 (2-3문장, 한국어로)
2. 감성 분석 (Positive/Neutral/Negative)

간결하고 사실적으로 답변해주세요. 반드시 한국어로 작성하세요."""

        # Generate analysis
        response = self._generate(prompt, max_tokens=300)

        # Extract sentiment (support both English and Korean)
        sentiment = "Neutral"
        response_lower = response.lower()
        if any(word in response_lower for word in ["positive", "bullish", "긍정", "상승", "호재"]):
            sentiment = "Positive"
        elif any(word in response_lower for word in ["negative", "bearish", "부정", "하락", "악재"]):
            sentiment = "Negative"

        return {
            "summary": response,
            "sentiment": sentiment
        }

    def summarize_text(self, text: str) -> str:
        """Summarize news article or text"""
        prompt = f"""다음 텍스트를 2-3문장으로 요약해주세요 (한국어로):

{text[:1000]}

요약:"""

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

        prompt = f"""다음 주식들을 간단히 비교해주세요 (각 1-2문장씩, 한국어로):

{comparison}

어느 것이 투자하기 더 좋아 보이나요? 간결하게 답변해주세요."""

        return self._generate(prompt, max_tokens=200)
