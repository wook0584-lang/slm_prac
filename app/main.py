"""
Stock Analysis Web App with Llama 3.2 1B
FastAPI Backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os

from app.llm import LlamaAnalyzer
from app.stock import StockData
from app.news import NewsCollector

# Initialize FastAPI app
app = FastAPI(
    title="Stock Analysis with Llama 3.2 1B",
    description="AI-powered stock market analysis using lightweight LLM",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
llm = LlamaAnalyzer()
stock_data = StockData()
news_collector = NewsCollector()


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
