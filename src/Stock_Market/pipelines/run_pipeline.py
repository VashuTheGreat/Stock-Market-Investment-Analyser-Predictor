
import sys
import os
import io



from src.Stock_Market.llm.llm_loader import llm
from logger import *



from langchain_core.messages import HumanMessage
from src.Stock_Market.graphs.builder import agent



class RunPipeline:
    def __init__(self):
        self.llm=llm
        self.agent=agent
    
    async def give_analysis(self,ticker_list:list=["AAPL", "MSFT", "GOOGL"]):
        messages=[HumanMessage(content=f"suggest me some stocks to buy of the following list: {ticker_list}")]
        result=await self.agent.ainvoke({"messages":messages, "news_": [], "llm_calls": 0})
        return result['messages'][-1].content

