
import sys
import os
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv()
import asyncio
from src.Stock_Market.llm.llm_loader import llm
from logger import *



from langchain_core.messages import HumanMessage
from src.Stock_Market.graphs.builder import agent
async def give_analysis(ticker_list:list=["AAPL", "MSFT", "GOOGL"]):
    messages=[HumanMessage(content=f"suggest me some stocks to buy of the following list: {ticker_list}")]
    result=await agent.ainvoke({"messages":messages, "news_": [], "llm_calls": 0})
    return result['messages'][-1].content

if __name__ == "__main__":
    print(asyncio.run(give_analysis()))