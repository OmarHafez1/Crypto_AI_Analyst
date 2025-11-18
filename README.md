# Crypto AI Analyst

**Crypto AI Analyst** is an AI-powered web app designed to help you analyze cryptocurrency data. It provides real-time market insights, connects news sentiment to market movements, and gives you AI-generated analysis to help you stay on top of the crypto world.

---

## Deployment

You can access **Crypto AI Analyst** online without needing to set up anything locally. Just visit the link below to start using the app:

[**Crypto AI Analyst - Live App**](https://cryptoaianalyst.streamlit.app/)

Simply log in, ask questions about cryptocurrencies, and get instant insights powered by AI.

---

## Features

* **Real-Time Cryptocurrency Prices**: View live prices of your favorite cryptocurrencies.
* **Market Sentiment Analysis**: Analyze the sentiment behind the latest crypto news and how it impacts the market.
* **AI Insights**: Get AI-powered analysis of crypto price movements and news trends.
* **Chat History**: Save your analysis sessions for future reference.

---

## How to Use

### 1. **Clone the Repository**

If you prefer running the app locally, you can clone this repository:

```bash
git clone https://github.com/your-username/crypto-ai-analyst.git
cd crypto-ai-analyst
```

### 2. **Set Up Your Environment**

Make sure you have `Python 3.7+` installed. Then, set up a virtual environment and install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. **Set Up Environment Variables**

To run the app, you’ll need to set up environment variables, such as your API keys.

Create a `.env` file in the root directory with your keys:

```
GOOGLE_API_KEY=your-google-api-key
CRYPTO_PANIC_API_KEY=your-cryptopanic-api-key
```

Replace `your-google-api-key` and `your-cryptopanic-api-key` with your actual API keys.

4. **Database Setup**: The app uses a PostgreSQL database to store chat sessions and user data. Configure the connection in your `.env` file for local or deployed environments.

---

### 4. **Running the App Locally**

Once your environment is set up, run the following command to start the app:

```bash
streamlit run app.py
```

The app will open in your browser, where you can start using the app immediately.

---

## How It Works

1. **Authentication**: Users log in or sign up to access the app, and their chat history is saved.
2. **Real-Time Data**: The app fetches live data from **CoinGecko** for prices and **CryptoPanic** for news.
3. **AI Analysis**: It uses **Google’s Gemini AI** to analyze both price data and news, providing valuable insights.
4. **Chat Sessions**: All conversations and analyses are saved in session history, which you can load later.

---

## Tech Stack

* **Frontend**: Streamlit (for the user interface)
* **Backend**: Python (for logic and data processing)
* **Database**: PostgreSQL (for saving user sessions and chat history)
* **AI**: Google Gemini (for language model-based analysis)

---

## Contributing

If you want to contribute to **Crypto AI Analyst**, feel free to fork the repo and submit a pull request with your changes. We welcome improvements, bug fixes, or new features!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Final Thoughts

Thanks for using **Crypto AI Analyst**! We hope this tool helps you stay updated on the latest in cryptocurrency markets and make informed decisions. If you have any questions or feedback, feel free to reach out!
