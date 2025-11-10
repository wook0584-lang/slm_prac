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

            # Create analysis prompt based on type (Korean)
            if analysis_type == "summary":
                prompt = f"""이 문서를 분석하고 간결한 요약을 제공해주세요 (3-5문장, 한국어로):

{text}

요약:"""

            elif analysis_type == "sentiment":
                prompt = f"""이 문서의 감성과 어조를 분석해주세요. 긍정적인지, 부정적인지, 중립적인지 간단히 설명해주세요 (한국어로).

{text}

감성 분석:"""

            elif analysis_type == "financial":
                prompt = f"""이것은 재무 문서로 보입니다. 다음 핵심 인사이트를 추출해주세요 (한국어로):
1. 언급된 주요 주제/회사
2. 재무 지표 또는 수치
3. 전반적인 의미

{text}

재무 분석:"""

            else:  # custom
                prompt = f"""이 문서를 분석하고 핵심 인사이트를 제공해주세요 (한국어로):

{text}

분석:"""

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

            # Create comparison prompt (Korean)
            prompt = f"""이 문서를 {ticker} 주식과 연관하여 분석해주세요 (한국어로):

주식 정보:
- 티커: {ticker}
- 현재 가격: ${stock_info.get('current_price', 'N/A')}
- 변동: {stock_info.get('change_percent', 'N/A')}%

문서 내용:
{text}

다음을 제공해주세요:
1. 이 문서가 {ticker}와 어떻게 관련되어 있나요?
2. 투자자를 위한 핵심 포인트
3. 주가에 미칠 잠재적 영향 (긍정적/부정적/중립적)

분석:"""

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
