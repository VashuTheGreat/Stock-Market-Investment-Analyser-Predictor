import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.asyncHandler import asyncHandler

class StockAnalysis:
    def __init__(self, ticker=None):
        self.ticker = ticker
        self.data = None

    @asyncHandler
    async def fetch_data(self, ticker=None):
        t_symbol = ticker if ticker is not None else self.ticker
        start = datetime.now() - relativedelta(months=6)
        end = datetime.now()
        self.data = yf.download(t_symbol, start=start, end=end, progress=False)

    @asyncHandler
    async def calculate_technical_indicators(self, data=None, ticker=None):
        """Calculate technical indicators for a single ticker"""
        df_base = data if data is not None else self.data
        t_symbol = ticker if ticker is not None else self.ticker

        if isinstance(df_base.columns, pd.MultiIndex):
            if t_symbol and t_symbol in df_base.columns.levels[0]:
                df = df_base[t_symbol].copy()
            elif len(df_base.columns.levels) > 1 and t_symbol and t_symbol in df_base.columns.levels[1]:
                df = df_base.xs(t_symbol, level=1, axis=1).copy()
            elif df_base.columns.nlevels == 2:
                df = df_base.copy()
                df.columns = df_base.columns.get_level_values(0)
            else:
                raise ValueError(f"Ticker {t_symbol} not found in data")
        else:
            df = df_base.copy()
        
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

    @asyncHandler
    async def get_fundamental_data(self, ticker_symbol=None):
        """Fetch fundamental data from yfinance"""
        t_symbol = ticker_symbol if ticker_symbol is not None else self.ticker
        ticker = yf.Ticker(t_symbol)
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

    @asyncHandler
    async def generate_investment_signal(self, technical, fundamental):
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

    @asyncHandler
    async def generate_key_insights(self, technical, fundamental, signal):
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

    @asyncHandler
    async def analyze_stock(self, ticker_symbol, historical_data=None):
        """
        Main function to analyze a stock and return LLM-friendly summary
        """
        
        if historical_data is None:
            start = datetime.now() - relativedelta(months=6)
            end = datetime.now()
            historical_data = yf.download(ticker_symbol, start=start, end=end, progress=False)
        
        technical = await self.calculate_technical_indicators(data=historical_data, ticker=ticker_symbol)
        fundamental = await self.get_fundamental_data(ticker_symbol=ticker_symbol)
        signal = await self.generate_investment_signal(technical, fundamental)
        key_insights = await self.generate_key_insights(technical, fundamental, signal)

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
            
            "key_insights": key_insights
        }
        
        return summary

    @asyncHandler
    async def analyze_multiple_stocks(self, ticker_list):
        """
        Analyze multiple stocks and return comparative analysis
        """
        start = datetime.now() - relativedelta(months=6)
        end = datetime.now()
        
        data = yf.download(ticker_list, start=start, end=end, group_by="ticker", progress=False)
        
        results = {}
        
        for ticker in ticker_list:
            analysis = await self.analyze_stock(ticker, data)
            results[ticker] = analysis
        
        return results

if __name__ == "__main__":
    import asyncio
    async def main():
        analyzer = StockAnalysis()
        print("=== Single Stock Analysis ===")
        result = await analyzer.analyze_stock("AAPL")
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
        results = await analyzer.analyze_multiple_stocks(stocks)
        
        for ticker, analysis in results.items():
            if 'error' not in analysis:
                print(f"\n{ticker}: {analysis['investment_signal']}")
                print(f"  Price: ${analysis['current_price']}")
                print(f"  3M Return: {analysis['performance']['3_month_return']}")
                print("  Key Insights:")
                for i in analysis["key_insights"]:
                    print("    •", i)
    
    asyncio.run(main())
