"""
Stock Market Data Collection using yfinance
Fetch real-time US stock market data
"""

import yfinance as yf
from typing import Dict, Optional, List
from datetime import datetime, timedelta


class StockData:
    """Handler for stock market data"""

    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """
        Get comprehensive stock information
        Returns: Dict with stock data or None if not found
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Get current price and change
            hist = stock.history(period="2d")
            if hist.empty:
                return None

            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', hist['Close'].iloc[0])
            change_percent = ((current_price - prev_close) / prev_close * 100) if prev_close else 0

            return {
                "ticker": ticker,
                "name": info.get("longName", ticker),
                "current_price": round(current_price, 2),
                "previous_close": round(prev_close, 2),
                "change_percent": round(change_percent, 2),
                "volume": info.get("volume", 0),
                "market_cap": info.get("marketCap", 0),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "pe_ratio": info.get("trailingPE", None),
                "dividend_yield": info.get("dividendYield", None),
                "52_week_high": info.get("fiftyTwoWeekHigh", None),
                "52_week_low": info.get("fiftyTwoWeekLow", None),
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
            stock = yf.Ticker(ticker)
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
