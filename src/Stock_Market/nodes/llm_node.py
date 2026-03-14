

from langchain_core.messages import SystemMessage
from src.Stock_Market.llm.llm_loader import llm
from utils.asyncHandler import asyncHandler
from src.Stock_Market.prompts import LLM_CALL_PROMPT
from src.Stock_Market.tools.multiple_stock_analysis_tool import multi_stock_analyse, fetch_news_article

tools=[multi_stock_analyse, fetch_news_article]

@asyncHandler
async def llm_call(state:dict):
    """LLM decides whether to call a tool or not"""

    state['tools_by_name']={tool.name:tool for tool in tools}


    model_with_tools=llm.bind_tools(tools)
    result = await model_with_tools.ainvoke(
                [
                    SystemMessage(
                        content=LLM_CALL_PROMPT
                    )
                    
                ]
                +state['messages']
            )
    return {
        "messages":[result],
        "llm_calls":state.get('llm_calls',0)+1,
        "tools_by_name": state['tools_by_name']
    }
