"""
News Collection for Stock Analysis
Collect financial news from multiple sources
"""

import feedparser
import requests
from typing import List, Dict
from datetime import datetime, timedelta
import yfinance as yf


class NewsCollector:
    """Collect news from various sources"""

    def __init__(self):
        self.sources = {
            "yahoo": self._get_yahoo_news,
            "rss": self._get_rss_news,
        }

    def get_news(self, ticker: str, limit: int = 10) -> List[Dict]:
        """
        Get news for a specific ticker from all sources
        """
        all_news = []

        # Get from Yahoo Finance (primary source)
        yahoo_news = self._get_yahoo_news(ticker)
        all_news.extend(yahoo_news)

        # Add RSS feeds if needed
        # rss_news = self._get_rss_news(ticker)
        # all_news.extend(rss_news)

        # Remove duplicates and sort by date
        seen_titles = set()
        unique_news = []
        for item in all_news:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                unique_news.append(item)

        # Sort by date (most recent first)
        unique_news.sort(key=lambda x: x.get('published', ''), reverse=True)

        return unique_news[:limit]

    def _get_yahoo_news(self, ticker: str) -> List[Dict]:
        """Get news from Yahoo Finance"""
        try:
            stock = yf.Ticker(ticker)
            news = stock.news

            formatted_news = []
            for item in news:
                formatted_news.append({
                    "title": item.get("title", "No title"),
                    "link": item.get("link", ""),
                    "published": datetime.fromtimestamp(
                        item.get("providerPublishTime", 0)
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "source": item.get("publisher", "Yahoo Finance"),
                    "summary": item.get("summary", "")[:200] + "..." if item.get("summary") else ""
                })

            return formatted_news

        except Exception as e:
            print(f"Error fetching Yahoo news for {ticker}: {e}")
            return []

    def _get_rss_news(self, ticker: str) -> List[Dict]:
        """Get news from RSS feeds"""
        rss_feeds = [
            f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}",
        ]

        news = []
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:
                    news.append({
                        "title": entry.get("title", "No title"),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "source": "RSS Feed",
                        "summary": entry.get("summary", "")[:200] + "..." if entry.get("summary") else ""
                    })
            except Exception as e:
                print(f"Error parsing RSS feed {feed_url}: {e}")
                continue

        return news

    def get_market_news(self, limit: int = 20) -> List[Dict]:
        """Get general market news"""
        try:
            # Use market indices for general news
            indices = ["^GSPC", "^DJI", "^IXIC"]
            all_news = []

            for index in indices:
                news = self._get_yahoo_news(index)
                all_news.extend(news)

            # Remove duplicates
            seen_titles = set()
            unique_news = []
            for item in all_news:
                if item['title'] not in seen_titles:
                    seen_titles.add(item['title'])
                    unique_news.append(item)

            return unique_news[:limit]

        except Exception as e:
            print(f"Error fetching market news: {e}")
            return []

    def search_news(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search news by keyword
        Note: This is a basic implementation using Google News RSS
        """
        try:
            # Google News RSS search
            query_encoded = query.replace(" ", "+")
            rss_url = f"https://news.google.com/rss/search?q={query_encoded}+stock&hl=en-US&gl=US&ceid=US:en"

            feed = feedparser.parse(rss_url)
            news = []

            for entry in feed.entries[:limit]:
                news.append({
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": entry.get("source", {}).get("title", "Google News"),
                    "summary": ""
                })

            return news

        except Exception as e:
            print(f"Error searching news for {query}: {e}")
            return []

    def get_trending_topics(self) -> List[str]:
        """Get trending stock market topics"""
        # This is a static list, could be enhanced with real trending analysis
        return [
            "Federal Reserve",
            "Interest Rates",
            "Inflation",
            "Earnings Reports",
            "Tech Stocks",
            "AI & Technology",
            "Energy Sector",
            "Banking Crisis",
            "Cryptocurrency",
            "Market Volatility"
        ]
