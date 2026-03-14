
from src.Stock_Market.models.state_model import State
from langchain_core.messages import SystemMessage,HumanMessage
from src.Stock_Market.llm.llm_loader import llm
from utils.asyncHandler import asyncHandler
from src.Stock_Market.prompts import SENTIMENT_ANALYSIS_TOOL_PROMPT


@asyncHandler
async def sentiment_analyser(state:State):
    news_content=state.news_content
    result=llm.ainvoke([
                    SystemMessage(
                        content=SENTIMENT_ANALYSIS_TOOL_PROMPT ),
                    HumanMessage(content=news_content)
                ])
    return {"sentiment_analysis":result.content}