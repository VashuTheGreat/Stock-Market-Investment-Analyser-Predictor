import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta

start = datetime.now() - relativedelta(months=6)
end = datetime.now()

def ticker_fetcher(*tickers):
    data = yf.download(
    tickers=tickers,
    start=start,
    end=end,
    group_by="ticker"
)   

    return data


def pattern_analyser_comparer(data):
        

if __name__=="__main__":
    print(ticker_fetcher("AAPL","MSFT","TSLA"))    