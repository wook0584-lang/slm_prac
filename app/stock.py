"""
Stock Market Data Collection using yfinance
Fetch real-time US stock market data
"""

import yfinance as yf
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import time
import requests


class StockData:
    """Handler for stock market data"""

    def __init__(self):
        """Initialize with rate limiting and custom session"""
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests (increased)

        # Create custom session with User-Agent to avoid 429 errors
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def _rate_limit(self):
        """Simple rate limiting to avoid 429 errors"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()

    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """
        Get comprehensive stock information
        Returns: Dict with stock data or None if not found
        """
        try:
            self._rate_limit()  # Rate limiting

            # Use download method instead of Ticker (more reliable)
            # Get recent price data
            hist = yf.download(ticker, period="5d", progress=False, session=self.session)

            if hist.empty:
                print(f"No data found for {ticker}")
                return None

            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change_percent = ((current_price - prev_close) / prev_close * 100) if prev_close else 0

            # Try to get additional info (optional, may fail)
            stock = yf.Ticker(ticker, session=self.session)
            try:
                info = stock.info
                name = info.get("longName", ticker)
                sector = info.get("sector", "N/A")
                industry = info.get("industry", "N/A")
                volume = info.get("volume", 0)
                market_cap = info.get("marketCap", 0)
                pe_ratio = info.get("trailingPE", None)
                dividend_yield = info.get("dividendYield", None)
                week_52_high = info.get("fiftyTwoWeekHigh", None)
                week_52_low = info.get("fiftyTwoWeekLow", None)
            except Exception as e:
                # If info fails, use minimal data from history
                print(f"Could not fetch detailed info for {ticker}, using basic data")
                name = ticker
                sector = "N/A"
                industry = "N/A"
                volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
                market_cap = 0
                pe_ratio = None
                dividend_yield = None
                week_52_high = float(hist['High'].max()) if 'High' in hist.columns else None
                week_52_low = float(hist['Low'].min()) if 'Low' in hist.columns else None

            return {
                "ticker": ticker,
                "name": name,
                "current_price": round(float(current_price), 2),
                "previous_close": round(float(prev_close), 2),
                "change_percent": round(float(change_percent), 2),
                "volume": volume,
                "market_cap": market_cap,
                "sector": sector,
                "industry": industry,
                "pe_ratio": pe_ratio,
                "dividend_yield": dividend_yield,
                "52_week_high": week_52_high,
                "52_week_low": week_52_low,
            }

        except Exception as e:
            print(f"Error fetching stock data for {ticker}: {e}")
            return None

    def get_price_history(self, ticker: str, period: str = "1mo") -> List[Dict]:
        """
        Get historical price data
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        try:
            self._rate_limit()  # Rate limiting
            stock = yf.Ticker(ticker, session=self.session)
            hist = stock.history(period=period)

            if hist.empty:
                return []

            # Convert to list of dicts
            history = []
            for date, row in hist.iterrows():
                history.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "open": round(row['Open'], 2),
                    "high": round(row['High'], 2),
                    "low": round(row['Low'], 2),
                    "close": round(row['Close'], 2),
                    "volume": int(row['Volume'])
                })

            return history

        except Exception as e:
            print(f"Error fetching price history for {ticker}: {e}")
            return []

    def get_multiple_stocks(self, tickers: List[str]) -> List[Dict]:
        """Get info for multiple stocks"""
        results = []
        for ticker in tickers:
            data = self.get_stock_info(ticker)
            if data:
                results.append(data)
            time.sleep(0.2)  # Extra delay for multiple requests
        return results

    def search_ticker(self, query: str) -> List[Dict]:
        """
        Search for stock tickers (basic implementation)
        Note: yfinance doesn't have native search, so this is limited
        """
        # Common US stocks mapping
        common_stocks = {
            "apple": "AAPL",
            "microsoft": "MSFT",
            "google": "GOOGL",
            "amazon": "AMZN",
            "tesla": "TSLA",
            "meta": "META",
            "facebook": "META",
            "nvidia": "NVDA",
            "berkshire": "BRK.B",
            "visa": "V",
            "jpmorgan": "JPM",
            "walmart": "WMT",
            "disney": "DIS",
            "netflix": "NFLX",
            "adobe": "ADBE",
            "salesforce": "CRM",
            "intel": "INTC",
            "amd": "AMD",
            "uber": "UBER",
            "twitter": "TWTR",
        }

        query_lower = query.lower()
        results = []

        # Search in common stocks
        for name, ticker in common_stocks.items():
            if query_lower in name or query_lower == ticker.lower():
                info = self.get_stock_info(ticker)
                if info:
                    results.append(info)

        # If exact ticker match
        if query.upper() not in [r['ticker'] for r in results]:
            info = self.get_stock_info(query.upper())
            if info:
                results.insert(0, info)

        return results[:10]  # Limit to 10 results

    def get_market_summary(self) -> Dict:
        """Get major indices summary"""
        indices = {
            "S&P 500": "^GSPC",
            "Dow Jones": "^DJI",
            "NASDAQ": "^IXIC",
        }

        summary = {}
        for name, ticker in indices.items():
            data = self.get_stock_info(ticker)
            if data:
                summary[name] = {
                    "price": data["current_price"],
                    "change_percent": data["change_percent"]
                }

        return summary
