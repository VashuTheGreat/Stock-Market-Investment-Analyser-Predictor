import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_technical_indicators(data, ticker=None):
    """Calculate technical indicators for a single ticker"""
    
    if isinstance(data.columns, pd.MultiIndex):
        if ticker and ticker in data.columns.levels[0]:
            df = data[ticker].copy()
        elif len(data.columns.levels) > 1 and ticker and ticker in data.columns.levels[1]:
            df = data.xs(ticker, level=1, axis=1).copy()
        elif data.columns.nlevels == 2:
            df = data.copy()
            df.columns = df.columns.get_level_values(0)
        else:
            raise ValueError(f"Ticker {ticker} not found in data")
    else:
        df = data.copy()
    
    close_prices = df['Close']
    
    ma_20 = close_prices.rolling(window=20).mean().values
    ma_50 = close_prices.rolling(window=50).mean().values
    
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = (100 - (100 / (1 + rs))).values
    
    returns = close_prices.pct_change(fill_method=None)
    volatility = returns.std() * np.sqrt(252) * 100  
    
    current_price = close_prices.iloc[-1].item()
    price_1m_ago = (close_prices.iloc[-21] if len(close_prices) > 21 else close_prices.iloc[0]).item()
    price_3m_ago = (close_prices.iloc[-63] if len(close_prices) > 63 else close_prices.iloc[0]).item()
    
    return_1m = ((current_price - price_1m_ago) / price_1m_ago) * 100
    return_3m = ((current_price - price_3m_ago) / price_3m_ago) * 100
    
    avg_volume = df['Volume'].mean().item()
    current_volume = df['Volume'].iloc[-1].item()
    volume_ratio = current_volume / avg_volume
    
    current_ma_20 = ma_20[-1].item() if len(ma_20) > 0 and not np.isnan(ma_20[-1]) else None
    current_ma_50 = ma_50[-1].item() if len(ma_50) > 0 and not np.isnan(ma_50[-1]) else None
    
    if current_ma_20 is not None and current_ma_50 is not None:
        if current_price > current_ma_20 > current_ma_50:
            trend = "Strong Uptrend"
        elif current_price > current_ma_20:
            trend = "Uptrend"
        elif current_price < current_ma_20 < current_ma_50:
            trend = "Strong Downtrend"
        else:
            trend = "Downtrend"
    else:
        trend = "Insufficient data"
    
    current_rsi = rsi[-1].item() if len(rsi) > 0 and not np.isnan(rsi[-1]) else None
    if current_rsi is not None:
        if current_rsi > 70:
            rsi_signal = "Overbought"
        elif current_rsi < 30:
            rsi_signal = "Oversold"
        else:
            rsi_signal = "Neutral"
    else:
        rsi_signal = "N/A"
    
    return {
        "current_price": round(current_price, 2),
        "ma_20": round(current_ma_20, 2) if current_ma_20 is not None else None,
        "ma_50": round(current_ma_50, 2) if current_ma_50 is not None else None,
        "rsi": round(current_rsi, 2) if current_rsi is not None else None,
        "rsi_signal": rsi_signal,
        "volatility": round(volatility, 2),
        "return_1m": round(return_1m, 2),
        "return_3m": round(return_3m, 2),
        "trend": trend,
        "avg_volume": int(avg_volume),
        "volume_ratio": round(volume_ratio, 2)
    }

def get_fundamental_data(ticker_symbol):
    """Fetch fundamental data from yfinance"""
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        return {
            "market_cap": info.get('marketCap', 'N/A'),
            "pe_ratio": round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 'N/A',
            "forward_pe": round(info.get('forwardPE', 0), 2) if info.get('forwardPE') else 'N/A',
            "beta": round(info.get('beta', 0), 2) if info.get('beta') else 'N/A',
            "dividend_yield": round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0,
            "eps": round(info.get('trailingEps', 0), 2) if info.get('trailingEps') else 'N/A',
            "profit_margin": round(info.get('profitMargins', 0) * 100, 2) if info.get('profitMargins') else 'N/A',
            "debt_to_equity": round(info.get('debtToEquity', 0), 2) if info.get('debtToEquity') else 'N/A',
            "sector": info.get('sector', 'N/A'),
            "industry": info.get('industry', 'N/A')
        }
    except Exception as e:
        print(f"Error fetching fundamental data for {ticker_symbol}: {e}")
        return {}

def generate_investment_signal(technical, fundamental):
    """Generate buy/hold/sell signal based on analysis"""
    score = 0
    
    if technical['trend'] in ["Strong Uptrend", "Uptrend"]:
        score += 2
    elif technical['trend'] in ["Strong Downtrend", "Downtrend"]:
        score -= 2
    
    if technical['rsi_signal'] == "Oversold":
        score += 1
    elif technical['rsi_signal'] == "Overbought":
        score -= 1
    
    if technical['return_3m'] > 10:
        score += 1
    elif technical['return_3m'] < -10:
        score -= 1
        
    if technical['volume_ratio'] > 1.5:
        score += 1
    
    if fundamental.get('pe_ratio') != 'N/A':
        if fundamental['pe_ratio'] < 20:
            score += 1
        elif fundamental['pe_ratio'] > 35:
            score -= 1
    
    if fundamental.get('beta') != 'N/A':
        if fundamental['beta'] < 1:
            score += 0.5
    
    if score >= 3:
        return "STRONG BUY"
    elif score >= 1:
        return "BUY"
    elif score <= -3:
        return "STRONG SELL"
    elif score <= -1:
        return "SELL"
    else:
        return "HOLD"

def analyze_stock(ticker_symbol, historical_data=None):
    """
    Main function to analyze a stock and return LLM-friendly summary
    
    Args:
        ticker_symbol: Stock ticker symbol (e.g., 'AAPL')
        historical_data: Optional pre-fetched historical data
    
    Returns:
        Dictionary with comprehensive analysis
    """
    
    if historical_data is None:
        start = datetime.now() - relativedelta(months=6)
        end = datetime.now()
        historical_data = yf.download(ticker_symbol, start=start, end=end, progress=False)
    
    technical = calculate_technical_indicators(historical_data, ticker_symbol)
    
    fundamental = get_fundamental_data(ticker_symbol)
    
    signal = generate_investment_signal(technical, fundamental)
    
    summary = {
        "ticker": ticker_symbol,
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "current_price": technical['current_price'],
        
        "technical_analysis": {
            "trend": technical['trend'],
            "price_vs_ma20": ("Above" if technical['current_price'] > technical['ma_20'] else "Below") if technical['ma_20'] is not None else "N/A",
            "price_vs_ma50": ("Above" if technical['current_price'] > technical['ma_50'] else "Below") if technical['ma_50'] is not None else "N/A",
            "rsi_value": technical['rsi'],
            "rsi_status": technical['rsi_signal'],
            "volatility": f"{technical['volatility']}% (Annualized)",
            "volume_status": "High" if technical['volume_ratio'] > 1.5 else "Normal" if technical['volume_ratio'] > 0.8 else "Low"
        },
        
        "performance": {
            "1_month_return": f"{technical['return_1m']}%",
            "3_month_return": f"{technical['return_3m']}%",
        },
        
        "fundamental_analysis": {
            "sector": fundamental.get('sector', 'N/A'),
            "industry": fundamental.get('industry', 'N/A'),
            "market_cap": fundamental.get('market_cap', 'N/A'),
            "pe_ratio": fundamental.get('pe_ratio', 'N/A'),
            "beta": fundamental.get('beta', 'N/A'),
            "dividend_yield": f"{fundamental.get('dividend_yield', 0)}%",
            "profit_margin": f"{fundamental.get('profit_margin', 'N/A')}%" if fundamental.get('profit_margin') != 'N/A' else 'N/A',
        },
        
        "risk_assessment": {
            "volatility_level": "High" if technical['volatility'] > 30 else "Moderate" if technical['volatility'] > 20 else "Low",
            "beta_interpretation": "Higher risk than market" if fundamental.get('beta', 1) != 'N/A' and fundamental.get('beta', 1) > 1.2 else "Lower risk than market" if fundamental.get('beta', 1) != 'N/A' and fundamental.get('beta', 1) < 0.8 else "Similar to market"
        },
        
        "investment_signal": signal,
        
        "key_insights": generate_key_insights(technical, fundamental, signal)
    }
    
    return summary

def generate_key_insights(technical, fundamental, signal):
    """Generate human-readable insights"""
    insights = []
    
    insights.append(f"Stock is in {technical['trend'].lower()} with current price at ${technical['current_price']}")
    
    if technical['rsi_signal'] == "Overbought":
        insights.append("RSI indicates overbought conditions - potential correction ahead")
    elif technical['rsi_signal'] == "Oversold":
        insights.append("RSI indicates oversold conditions - potential buying opportunity")
    
    if technical['return_3m'] > 15:
        insights.append(f"Strong 3-month performance of +{technical['return_3m']}%")
    elif technical['return_3m'] < -15:
        insights.append(f"Weak 3-month performance of {technical['return_3m']}%")
    
    if fundamental.get('pe_ratio') != 'N/A':
        if fundamental['pe_ratio'] < 15:
            insights.append(f"PE ratio of {fundamental['pe_ratio']} suggests undervaluation")
        elif fundamental['pe_ratio'] > 30:
            insights.append(f"PE ratio of {fundamental['pe_ratio']} suggests overvaluation")
    
    insights.append(f"Volatility is {technical['volatility']}% (annualized)")
    
    return insights

def analyze_multiple_stocks(ticker_list):
    """
    Analyze multiple stocks and return comparative analysis
    
    Args:
        ticker_list: List of ticker symbols
    
    Returns:
        Dictionary with analysis for each stock
    """
    start = datetime.now() - relativedelta(months=6)
    end = datetime.now()
    
    data = yf.download(ticker_list, start=start, end=end, group_by="ticker", progress=False)
    
    results = {}
    
    for ticker in ticker_list:
        try:
            analysis = analyze_stock(ticker, data)
            results[ticker] = analysis
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            results[ticker] = {"error": str(e)}
    
    return results

if __name__ == "__main__":
    print("=== Single Stock Analysis ===")
    result = analyze_stock("AAPL")
    print(f"\nTicker: {result['ticker']}")
    print(f"Signal: {result['investment_signal']}")
    print(f"\nKey Insights:")
    for insight in result['key_insights']:
        print(f"  • {insight}")

    print("\nPerformance:")
    print(f"  Current Price: ${result['current_price']}")
    print(f"  1M Return: {result['performance']['1_month_return']}")
    print(f"  3M Return: {result['performance']['3_month_return']}")    
    
    print("\n\n=== Multiple Stocks Analysis ===")
    stocks = ["AAPL", "MSFT", "GOOGL"]
    results = analyze_multiple_stocks(stocks)
    
    for ticker, analysis in results.items():
        if 'error' not in analysis:
            print(f"\n{ticker}: {analysis['investment_signal']}")
            print(f"  Price: ${analysis['current_price']}")
            print(f"  3M Return: {analysis['performance']['3_month_return']}")
            print("  Key Insights:")
            for i in analysis["key_insights"]:
                print("    •", i)
