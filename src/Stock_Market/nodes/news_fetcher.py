
from src.Stock_Market.models.state_model import State
from langchain_core.messages import SystemMessage,HumanMessage
from src.Stock_Market.llm.llm_loader import llm
from utils.asyncHandler import asyncHandler
from src.Stock_Market.prompts import SENTIMENT_ANALYSIS_TOOL_PROMPT
from src.Stock_Market.tools.multiple_stock_analysis_tool import fetch_news_article

@asyncHandler
async def news_fetcher_node(state:State):
    """Fetches news for the tickers"""
    news_content=await tool.fetch_news_article(state.get('tickers', []))
    return {"news_content":news_content}