# 📈 Stock Market Investment Analyser

A comprehensive AI-powered stock market analysis and prediction platform that combines technical analysis, sentiment analysis, and deep learning to provide intelligent investment recommendations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🤖 AI-Powered Analysis

- **Multi-Agent System**: Built with LangGraph for intelligent decision-making
- **Sentiment Analysis**: Real-time news sentiment analysis for stocks
- **Technical Analysis**: Comprehensive technical indicators (RSI, Moving Averages, Volatility)
- **Fundamental Analysis**: P/E ratio, market cap, beta, and more

### 📊 Advanced Visualizations

- **Candlestick Charts**: Interactive price action visualization
- **Technical Indicators**: Moving averages (MA100, MA200) and EMA charts
- **Volume Analysis**: Trading volume trends
- **Model Performance**: Visual comparison of predictions vs actual prices

### 🔮 Price Prediction

- **LSTM Deep Learning Model**: Pre-trained neural network for price forecasting
- **Multi-Stock Support**: Analyze and predict multiple stocks simultaneously
- **Historical Data**: Up to 2000 days of historical analysis

### 💎 Premium UI/UX

- **Modern Dark Theme**: Beautiful gradient-based design
- **Glassmorphism Effects**: Sleek, professional interface
- **Responsive Layout**: Optimized for all screen sizes
- **Interactive Cards**: Color-coded BUY/SELL/HOLD recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Stock_Market_investement_Analyser.git
   cd Stock_Market_investement_Analyser
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv myvenv

   # On Windows
   myvenv\Scripts\activate

   # On macOS/Linux
   source myvenv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:

   ```bash
   cp .env.example .env
   ```

   Add your API keys to `.env`:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Run the application**

   ```bash
   streamlit run app.py
   ```

6. **Open your browser**

   Navigate to `http://localhost:8501`

## 📖 Usage

### 1. Investment Analysis

1. Enter stock tickers in the sidebar (e.g., `AAPL, MSFT, GOOGL`)
2. Click **"🚀 Analyze Stocks"**
3. View AI-generated investment recommendations with:
   - Overall investment strategy
   - Individual stock analysis
   - BUY/SELL/HOLD signals with reasoning

### 2. Technical Charts & Predictions

1. Enter stock tickers in the sidebar
2. Click **"📈 Load Data & Show Plots for All Stocks"**
3. View comprehensive charts for each stock:

   - Candlestick charts
   - Price trends (Close, High)
   - Volume analysis
   - Moving averages (MA100, MA200)
   - Exponential moving averages
   - Model performance comparison

4. Click **"🔮 Predict Next Price for All Stocks"**
5. View AI predictions for next-day closing prices

## 🏗️ Project Structure

```
Stock_Market_investement_Analyser/
├── app.py                  # Main Streamlit application
├── main.py                 # LangGraph agent orchestration
├── analysis.py             # Technical & fundamental analysis
├── newsFetch.py           # News sentiment fetching
├── ticker.py              # Stock ticker utilities
├── stock_model.keras      # Pre-trained LSTM model
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🛠️ Technology Stack

### Backend

- **LangChain & LangGraph**: Multi-agent AI orchestration
- **Groq API**: Fast LLM inference
- **yFinance**: Real-time stock data
- **Pandas & NumPy**: Data processing
- **Keras/TensorFlow**: Deep learning predictions

### Frontend

- **Streamlit**: Interactive web application
- **Plotly**: Interactive candlestick charts
- **Matplotlib**: Technical indicator visualizations
- **Custom CSS**: Premium UI design

### AI/ML

- **LSTM Neural Network**: Time series prediction
- **Sentiment Analysis**: News-based market sentiment
- **Technical Indicators**: RSI, MA, EMA, Volatility
- **Multi-Agent System**: Coordinated analysis workflow

## 📊 Analysis Components

### Technical Analysis

- **Trend Detection**: Uptrend, Downtrend, Sideways
- **RSI (Relative Strength Index)**: Overbought/Oversold signals
- **Moving Averages**: MA20, MA50 for trend confirmation
- **Volatility**: Annualized price volatility
- **Volume Analysis**: Trading volume patterns
- **Price Performance**: 1-month and 3-month returns

### Fundamental Analysis

- **P/E Ratio**: Price-to-earnings valuation
- **Market Cap**: Company size classification
- **Beta**: Stock volatility vs market
- **Profit Margin**: Company profitability
- **Dividend Yield**: Income potential

### Sentiment Analysis

- **News Aggregation**: Latest company news
- **AI Sentiment Scoring**: Positive/Negative/Neutral classification
- **Impact Assessment**: News influence on stock price

## 🎯 Key Features Explained

### Multi-Agent AI System

The application uses LangGraph to create a sophisticated multi-agent workflow:

1. **LLM Call Agent**: Decides which tools to use
2. **Tool Node**: Executes technical and sentiment analysis
3. **Responder**: Generates structured investment recommendations

### Session State Management

Charts and analysis results persist across button clicks, providing a seamless user experience.

### Real-Time Data

All stock data is fetched in real-time from Yahoo Finance, ensuring up-to-date analysis.

## 🔐 Environment Variables

Create a `.env` file with the following:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from: [https://console.groq.com](https://console.groq.com)

## 📝 Requirements

```txt
langchain
langgraph
langchain-community
langchain-core
langchain-groq
pydantic
IPython
langchain-anthropic
python-dotenv
yfinance
streamlit
plotly
matplotlib
pandas
numpy
keras
tensorflow
scikit-learn
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. It should not be considered as financial advice. Always do your own research and consult with a qualified financial advisor before making investment decisions.

## 🙏 Acknowledgments

- **yFinance** for providing free stock market data
- **Groq** for fast LLM inference
- **Streamlit** for the amazing web framework
- **LangChain** for the AI orchestration framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ and AI**
