
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
import operator

class State(TypedDict):
    messages:Annotated[list[BaseMessage],operator.add]
    llm_calls:int
    tools_by_name:dict
    news_content:str
    sentiment_analysis:str
    tickers:list[str]
    news_:Annotated[list[BaseMessage],operator.add]