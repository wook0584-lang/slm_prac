"""
Stock Analysis Web App with Llama 3.2 1B
FastAPI Backend
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from app.llm import LlamaAnalyzer
from app.stock_alphavantage import StockDataAlphaVantage
from app.stock import StockData  # Keep yfinance as fallback
from app.news import NewsCollector
from app.pdf_analyzer import PDFAnalyzer

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Stock Analysis with Llama 3.2 1B + PDF Analyzer",
    description="AI-powered stock market analysis and PDF document analysis using lightweight LLM",
    version="2.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
llm = LlamaAnalyzer()

# Use Alpha Vantage if API key is set, otherwise fallback to yfinance
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
if api_key and api_key != "your_api_key_here":
    stock_data = StockDataAlphaVantage()
    print("✓ Using Alpha Vantage API")
else:
    stock_data = StockData()
    print("⚠️  Using Yahoo Finance (fallback) - set ALPHA_VANTAGE_API_KEY for better reliability")

news_collector = NewsCollector()
pdf_analyzer = PDFAnalyzer(llm)


# Request/Response Models
class TickerRequest(BaseModel):
    ticker: str


class AnalysisResponse(BaseModel):
    ticker: str
    current_price: Optional[float]
    change_percent: Optional[float]
    summary: str
    sentiment: str
    news: List[dict]


# Routes
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "llm_model": "llama3.2:1b",
        "services": ["stock_data", "news_collector", "llm_analyzer"]
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: TickerRequest):
    """
    Analyze a stock ticker with LLM
    - Fetch stock data
    - Collect recent news
    - Generate AI analysis and sentiment
    """
    ticker = request.ticker.upper()

    try:
        # Get stock data
        stock_info = stock_data.get_stock_info(ticker)
        if not stock_info:
            raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")

        # Get news
        news_items = news_collector.get_news(ticker)

        # Generate LLM analysis
        analysis = llm.analyze_stock(ticker, stock_info, news_items)

        return AnalysisResponse(
            ticker=ticker,
            current_price=stock_info.get("current_price"),
            change_percent=stock_info.get("change_percent"),
            summary=analysis["summary"],
            sentiment=analysis["sentiment"],
            news=news_items[:5]  # Top 5 news items
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/trending")
async def get_trending_stocks():
    """Get trending US stocks"""
    trending = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
        "TSLA", "META", "BRK.B", "V", "JPM"
    ]
    return {"trending": trending}


@app.post("/api/summarize")
async def summarize_news(request: dict):
    """Summarize news article using LLM"""
    try:
        text = request.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        summary = llm.summarize_text(text)
        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    analysis_type: str = Form("summary")
):
    """
    Analyze PDF document with LLM

    Parameters:
    - file: PDF file to analyze
    - analysis_type: 'summary', 'sentiment', 'financial', or 'custom'
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Read PDF file
        pdf_content = await file.read()

        # Analyze with LLM
        result = pdf_analyzer.analyze_pdf(pdf_content, analysis_type)

        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "PDF analysis failed"))

        return {
            "success": True,
            "filename": file.filename,
            "analysis": result["analysis"],
            "analysis_type": result["analysis_type"],
            "pages": result.get("pages", 0),
            "text_length": result.get("text_length", 0)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/api/analyze-pdf-with-stock")
async def analyze_pdf_with_stock(
    file: UploadFile = File(...),
    ticker: str = Form(...)
):
    """
    Analyze PDF in context of a specific stock
    Useful for earnings reports, company presentations, etc.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Get stock info
        ticker = ticker.upper()
        stock_info = stock_data.get_stock_info(ticker)
        if not stock_info:
            raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")

        # Read PDF file
        pdf_content = await file.read()

        # Analyze with stock context
        result = pdf_analyzer.compare_with_stock(pdf_content, ticker, stock_info)

        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "PDF analysis failed"))

        return {
            "success": True,
            "filename": file.filename,
            "ticker": ticker,
            "stock_price": result.get("stock_price"),
            "analysis": result["analysis"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
