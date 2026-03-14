from utils.asyncHandler import asyncHandler
from exception import MyException
import sys
from langchain.tools import tool
import logging
import json
from src.Stock_Market.utils.news_fetcher_utils import news_fetcher
from src.Stock_Market.components.stock_analysis import StockAnalysis

@tool
async def multi_stock_analyse(companiesTickers: list[str])->dict:
    """
    companiesTickers contains the tickers of the companies
    Args:
    companiesTickers: list of tickers
    """
    try:
        logging.info("Entered in the Multistock_analyser analyse method")
        analyzer = StockAnalysis()
        indian_stocks = await analyzer.analyze_multiple_stocks(companiesTickers) 
        result = {k: v for k, v in indian_stocks.items() if 'error' not in v}
        logging.info("Exited from the Multistock_analyser analyse method")
        return result
    except Exception as e:
        raise MyException(e,sys)

@tool
async def fetch_news_article(ticker:str)->dict:
    """
    ticker contains the ticker of the company
    Args:
    ticker: ticker of the company
    """
    try:
        logging.info("Entered in the sentence_analysis tool")
        news_content = await news_fetcher(ticker)
        news_content = json.dumps(news_content)
        logging.info("Exited from the sentence_analysis tool")
        return news_content
    except Exception as e:
        raise MyException(e,sys)
