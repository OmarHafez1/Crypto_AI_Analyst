import os
import re

import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()


class CryptoAnalyzer:
    def __init__(self):
        self.gemini_key = os.getenv("GOOGLE_API_KEY")
        self.news_key = os.getenv("CRYPTO_PANIC_API_KEY")

        self.setup_ai()
        self.all_coins = self.load_all_coins()

        self.system_msg = SystemMessage(
            content="""You are a crypto market analyst. Analyze both prices and news together. 
        Connect news sentiment to price movements. Identify market trends and potential impacts.
        Write in clear, natural English without any LaTeX or markdown formatting.
        Use plain numbers like 3500 instead of $3,500.
        Do not use **bold** or *italic* formatting.
        Write in short, clear paragraphs."""
        )

    def setup_ai(self):
        try:
            self.ai = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=self.gemini_key,
                temperature=0.7,
            )
        except Exception:
            self.ai = None

    def load_all_coins(self):
        try:
            url = "https://api.coingecko.com/api/v3/coins/list"
            response = requests.get(url, timeout=10)
            coins = response.json()

            coin_data = {}
            for coin in coins:
                coin_data[coin["id"]] = {
                    "symbol": coin["symbol"].upper(),
                    "name": coin["name"],
                }

            return coin_data
        except Exception:
            return {}

    def find_coins(self, question):
        if not self.ai:
            return "bitcoin,ethereum"

        prompt = f"""Based on this question: "{question}"

        Find the most relevant cryptocurrency CoinGecko IDs. Return ONLY comma-separated IDs.

        Examples:
        "NEAR price" -> "near"
        "Polkadot analysis" -> "polkadot" 
        "Bitcoin and Ethereum" -> "bitcoin,ethereum"
        "SOL and ADA" -> "solana,cardano"

        Return just the IDs:"""

        try:
            response = self.ai.invoke([HumanMessage(content=prompt)])
            coin_ids = response.content.strip().lower()
            return coin_ids
        except Exception:
            return "bitcoin,ethereum"

    def get_related_questions(self, current_question, coins_found):
        if not self.ai:
            return []

        prompt = f"""Based on this conversation context:
        Current question: "{current_question}"
        Coins discussed: {coins_found}

        Generate 3-4 short, relevant follow-up questions that a user might ask next.
        Return each question on a new line, no numbering or bullets."""

        try:
            response = self.ai.invoke([HumanMessage(content=prompt)])
            questions = [q.strip() for q in response.content.split("\n") if q.strip()]
            return questions[:4]
        except Exception:
            return []

    def get_prices(self, coin_ids):
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": coin_ids,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            prices = []
            for coin_id, info in data.items():
                if "usd" in info:
                    coin_info = self.all_coins.get(coin_id, {})
                    display_name = coin_info.get(
                        "name", coin_id.replace("-", " ").title()
                    )
                    symbol = coin_info.get("symbol", coin_id.upper())

                    prices.append(
                        {
                            "name": display_name,
                            "symbol": symbol,
                            "price": info["usd"],
                            "change": info.get("usd_24h_change", 0),
                        }
                    )

            return prices
        except Exception:
            return []

    def get_news(self, coin_ids, limit=10):
        """Get news with multiple fallback strategies"""
        try:
            # Get symbols for the coins
            symbols = []
            for coin_id in coin_ids.split(","):
                coin_info = self.all_coins.get(coin_id.strip(), {})
                symbol = coin_info.get("symbol", coin_id[:3].upper())
                symbols.append(symbol)

            symbols_str = ",".join(symbols)

            # Try multiple strategies to get news
            strategies = [
                {"currencies": symbols_str, "filter": "popular"},
                {"currencies": symbols_str},
                {"currencies": "BTC,ETH"},  # Fallback to major coins
                {},  # General crypto news
            ]

            all_articles = []

            for params in strategies:
                if len(all_articles) >= limit:
                    break

                try:
                    url = "https://cryptopanic.com/api/v1/posts/"
                    params.update(
                        {
                            "auth_token": self.news_key,
                            "kind": "news",
                            "limit": limit,
                        }
                    )

                    response = requests.get(url, params=params, timeout=10)
                    data = response.json()

                    for item in data.get("results", []):
                        if item["title"] not in [a["title"] for a in all_articles]:
                            votes = item.get("votes", {})
                            positive = votes.get("positive", 0)
                            negative = votes.get("negative", 0)

                            all_articles.append(
                                {
                                    "title": item.get("title", ""),
                                    "source": item.get("source", {}).get(
                                        "title", "Unknown"
                                    ),
                                    "url": item.get("url", ""),
                                    "sentiment": positive - negative,
                                    "currencies": [
                                        c.get("code")
                                        for c in item.get("currencies", [])
                                    ],
                                }
                            )

                    if len(all_articles) >= 5:
                        break

                except Exception:
                    continue

            return all_articles[:limit]
        except Exception:
            return []

    def clean_text(self, text: str) -> str:
        # More comprehensive LaTeX and markdown removal
        text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
        text = re.sub(r"\$.*?\$", "", text)
        text = re.sub(r"\\[a-zA-Z]+\{.*?\}", "", text)
        text = re.sub(
            r"\\begin\{.*?\}.*?\\end\{.*?\}", "", text, flags=re.DOTALL
        )
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)
        text = re.sub(r"_(.*?)_", r"\1", text)
        text = re.sub(r"`(.*?)`", r"\1", text)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^\w\s.,!?;:()\-+]", "", text)
        text = re.sub(r"\n\s*\n", "\n\n", text)
        text = re.sub(r" +", " ", text)
        text = text.strip()

        return text

    def format_news_for_analysis(self, news):
        """Format news in a way that's useful for AI analysis"""
        if not news:
            return "No recent news available"

        formatted_news = ""
        for i, item in enumerate(news[:6]):
            clean_title = self.clean_text(item["title"])
            sentiment = (
                "Positive"
                if item["sentiment"] > 2
                else "Negative"
                if item["sentiment"] < -2
                else "Neutral"
            )
            currencies = (
                ", ".join(item["currencies"])
                if item["currencies"]
                else "General"
            )

            formatted_news += f"{i + 1}. {clean_title}\n"
            formatted_news += (
                f"   Source: {item['source']} | Sentiment: {sentiment} | "
                f"Currencies: {currencies}\n\n"
            )

        return formatted_news

    def analyze(self, question, history):
        if not self.gemini_key or not self.ai:
            return "Please check your API key setup", [], [], []

        try:
            coin_ids = self.find_coins(question)

            prices = self.get_prices(coin_ids)
            news = self.get_news(coin_ids)

            # Format market data for AI
            market_info = ""
            if prices:
                market_info += "**CURRENT PRICES:**\n"
                for coin in prices:
                    trend = "🟢" if coin["change"] > 0 else "🔴"
                    market_info += (
                        f"- {coin['name']} ({coin['symbol']}): "
                        f"${coin['price']:,.2f} {trend} "
                        f"{coin['change']:+.2f}%\n"
                    )
            else:
                market_info += "No price data available\n"

            # Format news for AI analysis
            news_analysis = self.format_news_for_analysis(news)

            messages = [self.system_msg]
            if history:
                messages.extend(history[-4:])

            prompt = f"""USER QUESTION: {question}

MARKET DATA:
{market_info}

LATEST NEWS & SENTIMENT:
{news_analysis}

ANALYSIS REQUEST:
Please analyze BOTH the price data and news together. 
- Connect news sentiment to price movements
- Identify potential catalysts from the news
- Provide market insights based on both data sources
- Suggest what to watch for based on current trends"""

            from langchain_core.messages import HumanMessage as _HumanMessage

            messages.append(_HumanMessage(content=prompt))

            response = self.ai.invoke(messages)

            clean_response = self.clean_text(response.content)

            # Generate related questions
            coin_names = [coin["name"] for coin in prices]
            related_questions = self.get_related_questions(question, coin_names)

            return clean_response, prices, news, related_questions

        except Exception as e:
            return f"Error: {str(e)}", [], [], []
