"""
Stock Market Data Collection using Alpha Vantage
More stable and reliable than Yahoo Finance
"""

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from typing import Dict, Optional, List
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()


class StockDataAlphaVantage:
    """Handler for stock market data using Alpha Vantage API"""

    def __init__(self):
        """Initialize with API key from environment"""
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key or self.api_key == "your_api_key_here":
            print("⚠️  Warning: ALPHA_VANTAGE_API_KEY not set in .env file")
            print("   Get your free API key at: https://www.alphavantage.co/support/#api-key")
            self.api_key = "demo"  # Use demo key as fallback

        self.ts = TimeSeries(key=self.api_key, output_format='pandas')
        self.fd = FundamentalData(key=self.api_key, output_format='json')
        self.last_request_time = 0
        self.min_request_interval = 12  # Alpha Vantage: 5 calls/min = 12 sec interval

    def _rate_limit(self):
        """Rate limiting for Alpha Vantage (5 calls/min for free tier)"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            wait_time = self.min_request_interval - time_since_last_request
            print(f"Rate limiting: waiting {wait_time:.1f}s...")
            time.sleep(wait_time)
        self.last_request_time = time.time()

    def get_stock_info(self, ticker: str) -> Optional[Dict]:
        """
        Get comprehensive stock information
        Returns: Dict with stock data or None if not found
        """
        try:
            self._rate_limit()

            # Get intraday data (most recent price)
            data, meta_data = self.ts.get_intraday(symbol=ticker, interval='5min', outputsize='compact')

            if data.empty:
                print(f"No data found for {ticker}")
                return None

            # Get latest price
            latest = data.iloc[0]
            prev = data.iloc[1] if len(data) > 1 else data.iloc[0]

            current_price = float(latest['4. close'])
            prev_close = float(prev['4. close'])
            change_percent = ((current_price - prev_close) / prev_close * 100) if prev_close else 0

            # Try to get company overview (contains name, sector, etc.)
            try:
                overview, _ = self.fd.get_company_overview(symbol=ticker)
                name = overview.get('Name', ticker)
                sector = overview.get('Sector', 'N/A')
                industry = overview.get('Industry', 'N/A')
                market_cap = int(overview.get('MarketCapitalization', 0))
                pe_ratio = float(overview.get('PERatio', 0)) if overview.get('PERatio') != 'None' else None
                dividend_yield = float(overview.get('DividendYield', 0)) if overview.get('DividendYield') != 'None' else None
                week_52_high = float(overview.get('52WeekHigh', 0)) if overview.get('52WeekHigh') != 'None' else None
                week_52_low = float(overview.get('52WeekLow', 0)) if overview.get('52WeekLow') != 'None' else None
            except:
                name = ticker
                sector = "N/A"
                industry = "N/A"
                market_cap = 0
                pe_ratio = None
                dividend_yield = None
                week_52_high = None
                week_52_low = None

            volume = int(latest['5. volume'])

            return {
                "ticker": ticker,
                "name": name,
                "current_price": round(current_price, 2),
                "previous_close": round(prev_close, 2),
                "change_percent": round(change_percent, 2),
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
        """
        try:
            self._rate_limit()

            # Map period to Alpha Vantage outputsize
            outputsize = 'full' if period in ['1y', '2y', '5y'] else 'compact'

            data, meta_data = self.ts.get_daily(symbol=ticker, outputsize=outputsize)

            if data.empty:
                return []

            # Convert to list of dicts
            history = []
            for date, row in data.iterrows():
                history.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "open": round(float(row['1. open']), 2),
                    "high": round(float(row['2. high']), 2),
                    "low": round(float(row['3. low']), 2),
                    "close": round(float(row['4. close']), 2),
                    "volume": int(row['5. volume'])
                })

            return history

        except Exception as e:
            print(f"Error fetching price history for {ticker}: {e}")
            return []
