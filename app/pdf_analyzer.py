"""
PDF Analysis using LLM
Extract text from PDF and analyze with Llama 3.2 1B
"""

from PyPDF2 import PdfReader
from typing import Optional
import io


class PDFAnalyzer:
    """Extract and analyze PDF documents"""

    def __init__(self, llm_analyzer):
        """Initialize with LLM analyzer instance"""
        self.llm = llm_analyzer

    def extract_text(self, pdf_file: bytes) -> Optional[str]:
        """
        Extract text from PDF file
        Returns: Extracted text or None if failed
        """
        try:
            # Create PDF reader from bytes
            pdf_reader = PdfReader(io.BytesIO(pdf_file))

            # Extract text from all pages
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text

            if not text.strip():
                return None

            return text

        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return None

    def analyze_pdf(self, pdf_file: bytes, analysis_type: str = "summary") -> dict:
        """
        Analyze PDF content with LLM

        Args:
            pdf_file: PDF file as bytes
            analysis_type: 'summary', 'sentiment', 'financial', 'custom'

        Returns:
            Dict with analysis results
        """
        try:
            # Extract text
            text = self.extract_text(pdf_file)
            if not text:
                return {
                    "success": False,
                    "error": "Could not extract text from PDF"
                }

            # Truncate if too long (LLM context limit)
            max_length = 4000
            if len(text) > max_length:
                text = text[:max_length] + "\n\n[... truncated ...]"

            # Create analysis prompt based on type
            if analysis_type == "summary":
                prompt = f"""Analyze this document and provide a concise summary (3-5 sentences):

{text}

Summary:"""

            elif analysis_type == "sentiment":
                prompt = f"""Analyze the sentiment and tone of this document. Is it positive, negative, or neutral? Explain briefly.

{text}

Sentiment Analysis:"""

            elif analysis_type == "financial":
                prompt = f"""This appears to be a financial document. Extract key insights:
1. Main topics/companies mentioned
2. Financial metrics or numbers
3. Overall implications

{text}

Financial Analysis:"""

            else:  # custom
                prompt = f"""Analyze this document and provide key insights:

{text}

Analysis:"""

            # Generate analysis using LLM
            analysis = self.llm._generate(prompt, max_tokens=500)

            return {
                "success": True,
                "analysis": analysis,
                "text_length": len(text),
                "pages": len(text.split("--- Page")),
                "analysis_type": analysis_type
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def compare_with_stock(self, pdf_file: bytes, ticker: str, stock_info: dict) -> dict:
        """
        Analyze PDF in context of a specific stock
        Useful for earnings reports, news articles, etc.
        """
        try:
            text = self.extract_text(pdf_file)
            if not text:
                return {
                    "success": False,
                    "error": "Could not extract text from PDF"
                }

            # Truncate if needed
            max_length = 3000
            if len(text) > max_length:
                text = text[:max_length] + "\n\n[... truncated ...]"

            # Create comparison prompt
            prompt = f"""Analyze this document in relation to {ticker} stock:

Stock Info:
- Ticker: {ticker}
- Current Price: ${stock_info.get('current_price', 'N/A')}
- Change: {stock_info.get('change_percent', 'N/A')}%

Document Content:
{text}

Provide:
1. How does this document relate to {ticker}?
2. Key takeaways for investors
3. Potential impact on stock price (positive/negative/neutral)

Analysis:"""

            analysis = self.llm._generate(prompt, max_tokens=500)

            return {
                "success": True,
                "analysis": analysis,
                "ticker": ticker,
                "stock_price": stock_info.get('current_price')
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
