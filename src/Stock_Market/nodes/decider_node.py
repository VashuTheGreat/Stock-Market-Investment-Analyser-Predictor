from typing import Literal
from src.Stock_Market.models.state_model import State
from utils.asyncHandler import asyncHandler


@asyncHandler
async def should_continue(state:State)->Literal["tool_node","responder"]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
    messages=state['messages']
    last_message=messages[-1]

    if last_message.tool_calls:
        return "tool_node"
    
    return "responder"
